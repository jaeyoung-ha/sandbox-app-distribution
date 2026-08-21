# STEP 8. 동작 테스트

구축이 끝났으면 4가지 테스트로 전체 동작을 검증합니다.

## 테스트 4종

| # | 테스트 | 기대 결과 |
|---|---|---|
| 1 | 새 시크릿 창 → `https://CLOUDFRONT_DOMAIN` | Cognito 로그인 페이지로 이동 ✅ |
| 2 | 이메일 + 임시 비번 로그인 | 새 비번 설정 → **베이커리 앱 표시** ✅ |
| 3 | 로그인 전 소스 확인: `curl https://CLOUDFRONT_DOMAIN` (쿠키 없이) | 302 리다이렉트만 응답, **HTML 미전송** ✅ |
| 4 | `https://AMPLIFY_HOST` 직접 접속 | Basic Auth 401 차단 ✅ |

4개 모두 통과하면 구축 완료입니다. 🎉

## 문제 발생 시 — 로그 확인

Lambda@Edge 로그는 **접속자 근처 리전**에 쌓입니다 (한국 = ap-northeast-2). 로그 그룹 이름의 `us-east-1.` 접두어는 **함수의 홈 리전(us-east-1)** 을 뜻하며, 다른 리소스가 서울이어도 정상입니다:

```
CloudWatch(리전: ap-northeast-2) → 로그 그룹 → /aws/lambda/us-east-1.cjfv-bakery-edge-auth
```

## 자주 나오는 오류

| 증상 | 원인 / 조치 |
|---|---|
| 로그인 주소가 `https://https//...`로 깨짐 | 시크릿의 `cognitoDomain` 값에 `https://` 포함 → 스킴 없이 도메인만 저장 |
| 로그인 후 403 | ① origin-request 함수 미연결 → STEP 5-2 확인 ② 시크릿의 `basicUser`/`basicPass`가 Amplify 설정과 불일치 → 시크릿 값 수정 (5분 내 반영) |
| `redirect_mismatch` | 콜백 URL ≠ 실제 접속 주소 → 슬래시 유무 두 가지 다 등록 (STEP 5-3) |
| 무한 리다이렉트 | 시크릿의 Cognito 도메인/ClientID/Secret 오입력 → 시크릿 값 확인·수정 |
| 503 + 로그에 AccessDenied | Lambda 역할에 `secretsmanager:GetSecretValue` 정책 누락 (STEP 4-3) |
| 코드 수정이 반영 안 됨 | 새 버전 게시 + Behaviors에서 새 ARN 재연결 필요 (시크릿 값 변경은 재배포 불필요) |
| 관리자 Reset password 실패 | 이메일 verified 아님 → 사용자 속성에서 `email_verified = true` |

## 사용자 안내문 (복사해서 전달)

```
[베이커리 상권분석 PoC 접속 안내]
1. 접속 URL: https://CLOUDFRONT_DOMAIN
2. 로그인 화면에서 안내받은 회사 이메일 + 임시 비밀번호 입력
3. 최초 로그인 시 새 비밀번호로 변경
※ 등록된 계정만 접속 가능합니다. 사내 데이터 포함 — 외부 공유 금지.
```

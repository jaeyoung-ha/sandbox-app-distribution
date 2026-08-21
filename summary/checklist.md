# 체크리스트

전체 구축 과정의 완료 여부를 한눈에 확인합니다.

## 구축 (STEP 1~5)

- [ ] **STEP 1**: Amplify 배포 (원본 index.html), `AMPLIFY_HOST` 메모
- [ ] **STEP 2**: Amplify Basic Auth 잠금 (**아는 값**으로 아이디/비번 설정·보관), 직접 접속 401 확인
- [ ] **STEP 3**: ap-northeast-2(서울)에 User Pool (**Traditional, 시크릿 있음**) + 도메인 + OAuth 설정
- [ ] **STEP 4-1**: Secrets Manager에 시크릿 생성 (키 6개), ARN 메모
- [ ] **STEP 4**: 코드에 시크릿 이름 확인 → esbuild 번들 (SDK 제외, 1MB 미만) → IAM (신뢰정책 + GetSecretValue) → 함수 생성 → **버전 게시**
- [ ] **STEP 5**: CloudFront 생성 (CachingDisabled) → **Behaviors에서 viewer/origin-request 연결** → 콜백 URL 등록

## 사용자 운영 (STEP 6~7)

- [ ] **STEP 6**: 사용자 생성 (**Mark email as verified 체크**)
- [ ] **STEP 7**: 비번 재설정 절차 확인

## 테스트 (STEP 8)

- [ ] 테스트 4종 통과 (로그인 / 앱 표시 / 소스 미전송 / 우회 차단)
- [ ] 사용자 안내문 발송

## 놓치기 쉬운 것 Top 3

1. **Lambda 버전 게시** — 코드 수정 시 재번들 → 버전 게시 → CloudFront 재연결 3단계 필수
2. **Cognito 콜백 URL** — 슬래시 유무 두 가지 모두 등록, 접속 주소가 바뀌면 재등록
3. **Mark email as verified** — 사용자 생성 시 미체크하면 비밀번호 재설정 불가

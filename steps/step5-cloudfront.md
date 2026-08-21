# STEP 5. CloudFront 배포 생성 + 함수 연결

사용자가 접속할 CloudFront 배포를 만들고, 인증 함수를 연결합니다.

## 5-1. 배포 생성

1. **CloudFront** → **Create distribution**
2. **Origin domain**: `AMPLIFY_HOST` 입력 (예: `main.d1m0ctzydro7k9.amplifyapp.com` — 브랜치 접두사 포함)
3. **Origin protocol**: **HTTPS only**
4. **오리진 커스텀 헤더는 넣지 않습니다** (Basic Auth는 Lambda가 주입 — 중복 금지)
5. Default cache behavior:

| 항목 | 값 |
|---|---|
| Viewer protocol policy | Redirect HTTP to HTTPS |
| Cache policy | **CachingDisabled** (인증 콘텐츠 캐시 금지) |
| Origin request policy | None |

6. WAF: 선택 안 함(PoC) → **Create distribution**
7. 배포 도메인 메모 → `CLOUDFRONT_DOMAIN` (예: `d1a2b3c4.cloudfront.net`)

## 5-2. Lambda@Edge 함수 연결 (★ Behaviors 탭에서)

> ⚠️ 생성 마법사에는 이 메뉴가 **없습니다.** 배포 생성 후 Behaviors 탭에서 편집합니다 (실제 헤맨 부분).

1. 배포 → **Behaviors** 탭 → Default (`*`) 선택 → **Edit**
2. 맨 아래 **Function associations**:

| 트리거 | Function type | ARN |
|---|---|---|
| **Viewer request** | Lambda@Edge | `LAMBDA_VERSION_ARN` |
| **Origin request** | Lambda@Edge | **같은** `LAMBDA_VERSION_ARN` |

3. **Save changes** → 배포 상태가 Deployed 될 때까지 대기 (3~10분)

## 5-3. Cognito 콜백 URL 등록

1. Cognito(ap-northeast-2) → User Pool → App clients → `cjfv-bakery-edge` → **Login pages → Edit**
2. **Allowed callback URLs**: 아래 **둘 다** 추가 (STEP 3의 임시값 example.com 삭제)
   - `https://CLOUDFRONT_DOMAIN`
   - `https://CLOUDFRONT_DOMAIN/`
3. **Allowed sign-out URLs**: 동일하게 추가 → **Save**

> ⚠️ 콜백 URL이 실제 접속 주소와 다르면 로그인 시 `redirect_mismatch` 오류가 납니다. 슬래시 유무 두 가지를 모두 등록하는 이유입니다.

## 완료 확인

- [ ] 배포 생성 (HTTPS only + CachingDisabled)
- [ ] Behaviors에서 viewer-request / origin-request 에 같은 버전 ARN 연결
- [ ] Cognito 콜백/로그아웃 URL에 CloudFront 주소 등록 (슬래시 유무 둘 다)
- [ ] `CLOUDFRONT_DOMAIN` 메모 완료

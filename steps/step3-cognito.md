# STEP 3. Cognito 구성

사용자 로그인을 담당할 Cognito User Pool을 만듭니다.

> 🌎 콘솔 우측 상단 리전을 **아시아 태평양(서울) ap-northeast-2** 로 바꾸고 진행합니다.

## 3-1. User Pool + 앱 클라이언트 생성

1. **Cognito** → **Create user pool**
2. **Application type**: **Traditional web application** 선택

> ⚠️ **SPA가 아니라 Traditional입니다.** 인증 코드가 엣지 **서버**(Lambda@Edge)에서 실행되므로 **클라이언트 시크릿이 필요**합니다. 브라우저에서 인증하는 방식(SPA)과 반대입니다.

3. **Name your application**: `cjfv-bakery-edge`
4. 로그인 식별자: **Email** 체크
5. **Return URL**: 임시로 `https://example.com/` 입력 (STEP 5에서 CloudFront 주소로 교체)
6. 생성 완료 후 메모:
   - **User Pool ID** → `COGNITO_POOL_ID` (User pool overview에서 확인)
   - **App clients** → `cjfv-bakery-edge` → **Client ID** → `APP_CLIENT_ID`
   - **Client secret** (Show 클릭) → `APP_CLIENT_SECRET`

## 3-2. Cognito 도메인 확인/생성

로그인 페이지가 인터넷에 뜨려면 도메인이 필요합니다.

1. User Pool → **Branding → Domain** (또는 App integration → Domain)
2. 마법사가 자동 생성한 도메인이 있으면 메모만, 없으면 **Create Cognito domain** → 접두어 예) `cjfv-bakery-login`
3. `COGNITO_DOMAIN` 메모: `cjfv-bakery-login.auth.ap-northeast-2.amazoncognito.com`

> ⚠️ **`https://` 를 절대 포함하지 마세요.** Lambda 설정에 스킴이 들어가면 로그인 주소가 `https://https//...`로 깨집니다 (실제 겪은 버그).

## 3-3. OAuth 설정

1. App clients → `cjfv-bakery-edge` → **Login pages → Edit**
2. 아래 설정 후 저장:

| 항목 | 값 |
|---|---|
| Identity providers | **Cognito user pool** 체크 |
| OAuth 2.0 grant types | **Authorization code grant** 체크 |
| OpenID Connect scopes | **OpenID**, **Email**, **Profile** 체크 |

> Callback/Sign-out URL은 CloudFront 주소가 나온 뒤([STEP 5-3](steps/step5-cloudfront.md)) 등록합니다.

## 완료 확인

- [ ] Traditional 앱 클라이언트 생성 (시크릿 있음)
- [ ] `COGNITO_POOL_ID`, `APP_CLIENT_ID`, `APP_CLIENT_SECRET`, `COGNITO_DOMAIN` 메모 완료
- [ ] OAuth: Authorization code grant + OpenID/Email/Profile 설정

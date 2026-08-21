# 메모할 값 정리

구축을 진행하면서 아래 빈칸을 채워 나갑니다. 각 값이 어느 STEP에서 나오는지 표시돼 있습니다.

```
AMPLIFY_HOST      = main.__________.amplifyapp.com      (STEP 1, https:// 제외)
BASIC_USER        = cfedge                              (STEP 2)
BASIC_PASS        = ____________                        (STEP 2, 강한 랜덤값 — 반드시 "아는 값"으로 보관)
COGNITO_POOL_ID   = ap-northeast-2___________            (STEP 3)
APP_CLIENT_ID     = ____________                        (STEP 3)
APP_CLIENT_SECRET = ____________                        (STEP 3)
COGNITO_DOMAIN    = ______.auth.ap-northeast-2.amazoncognito.com   (STEP 3, ★https:// 절대 포함 금지)
SECRET_ARN        = arn:aws:secretsmanager:ap-northeast-2:...:secret:cjfv/bakery-edge-XXXXXX   (STEP 4-1, 서울)
LAMBDA_VERSION_ARN= arn:aws:lambda:us-east-1:...:function:____:N   (STEP 4, ★us-east-1 유일, 끝에 버전번호 필수)
CLOUDFRONT_DOMAIN = d__________.cloudfront.net          (STEP 5)
```

## 값별 주의사항

| 값 | 주의사항 |
|---|---|
| `BASIC_PASS` | Amplify는 저장된 비번을 **다시 보여주지 않습니다.** 시크릿에 저장하기 전까지 잃어버리지 않게 보관 |
| `COGNITO_DOMAIN` | **`https://` 를 절대 포함하지 마세요.** 스킴이 들어가면 로그인 주소가 깨집니다 |
| `LAMBDA_VERSION_ARN` | 끝의 **버전 번호(`:1`)까지** 포함해야 합니다. `$LATEST`는 CloudFront에 연결 불가 |

이 표를 메모장에 복사해두고 시작하는 것을 권장합니다.

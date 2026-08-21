# STEP 2. Amplify를 Basic Auth로 잠그기

CloudFront를 거치지 않은 **직접 접속을 차단**하기 위해 Amplify에 비밀번호를 겁니다.

> ⚠️ **반드시 "아는 값"으로 설정**하세요. Amplify가 저장한 자격증명은 나중에 역산할 수 없습니다. placeholder 그대로 쓰면 CloudFront와 불일치로 403이 납니다 (실제 겪은 이슈).

## 2-1. Access control 설정

1. Amplify 콘솔 → 베이커리 앱 → **Hosting → Access control**
2. **Manage access** → 브랜치(`main`)를 **Restricted - password required** 로 설정
3. Username: `cfedge` / Password: 강한 랜덤 문자열 입력 → 저장
4. `BASIC_USER` / `BASIC_PASS` 메모

> 💡 이 아이디/비번은 [STEP 4-1](steps/step4-lambda-edge.md)에서 **Secrets Manager에 저장**합니다 (코드에는 안 들어감). HTTP 규격상 필요한 base64 변환은 코드가 자동 수행합니다. Amplify는 저장된 비번을 다시 보여주지 않으므로, 시크릿에 저장하기 전까지 잃어버리지 않게 메모해 두세요.

## 완료 확인

- [ ] 브라우저에서 `https://AMPLIFY_HOST` 접속 시 **로그인 창(401)** 이 뜸
- [ ] `BASIC_USER` / `BASIC_PASS` 메모 완료

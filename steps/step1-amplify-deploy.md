# STEP 1. Amplify에 베이커리 앱 배포

앱을 원본 그대로 Amplify에 배포합니다.

> 이미 배포돼 있으면 URL만 메모하고 [STEP 2](steps/step2-basic-auth.md)로 이동하세요. 단, **브라우저 게이트 스크립트(방식 ①)가 들어간 버전이라면 원본으로 재배포**해야 합니다.

## 1-1. zip 파일 만들기

`index.html`이 **zip 최상단**에 오도록 압축합니다.

**macOS/Linux 터미널:**

```bash
cd "베이커리 상권분석 시스템/bakery-app"
zip -r ../bakery-app.zip . -x ".*"
```

**윈도우 PowerShell:**

```powershell
cd "베이커리 상권분석 시스템\bakery-app"
Compress-Archive -Path * -DestinationPath ..\bakery-app.zip -Force
```

> ⚠️ 윈도우 탐색기로 압축할 경우: **폴더가 아니라 폴더 안의 파일들을 전체 선택**해서 압축하세요. 폴더째 압축하면 zip을 풀었을 때 `index.html`이 한 겹 아래에 있어 Amplify가 404를 냅니다.

## 1-2. Amplify에 업로드

1. AWS 콘솔 → **Amplify** → **Create new app** → **Deploy without Git**
2. App name: `cjfv-bakery`, Branch: `main`
3. **Method: Drag and drop** → zip 드롭 → **Save and deploy**
   - 기존 앱 갱신이면: 해당 앱 → 브랜치 → **Deploy updates** 에 zip 드롭

## 1-3. URL 메모

생성된 URL을 메모합니다 → `AMPLIFY_HOST`

- 예: `main.d1m0ctzydro7k9.amplifyapp.com`
- **`https://` 는 제외**하고 메모

## 완료 확인

- [ ] 브라우저에서 `https://AMPLIFY_HOST` 접속 시 앱이 표시됨
- [ ] `AMPLIFY_HOST` 값 메모 완료

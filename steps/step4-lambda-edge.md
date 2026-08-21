# STEP 4. Lambda@Edge 함수 만들기

인증을 수행하는 엣지 함수를 만듭니다. 비밀값은 **Secrets Manager**에 보관합니다.

> **Secrets Manager를 쓰는 이유**
> - 코드/zip에 비밀값이 안 남음
> - **비번 교체 시 시크릿 값만 수정하면 끝** — Lambda 재번들·버전 게시·CloudFront 재연결 불필요 (5분 이내 자동 반영)
> - Lambda@Edge는 환경변수를 지원하지 않아, 런타임 조회 + 캐시가 표준 패턴 (비용: 시크릿 1개 월 $0.40 수준)

## 4-1. Secrets Manager에 설정값 저장

1. 콘솔 리전 **ap-northeast-2(서울)** 확인 → **Secrets Manager** → **Store a new secret**
2. Secret type: **Other type of secret** 선택
3. **Key/value pairs** 에 6개 입력 (메모한 값 그대로):

| Key | Value |
|---|---|
| `userPoolId` | STEP 3의 User Pool ID (`ap-northeast-2_xxxxxxx`) |
| `appClientId` | STEP 3의 Client ID |
| `appClientSecret` | STEP 3의 Client secret |
| `cognitoDomain` | STEP 3의 도메인 (★ `https://` 없이) |
| `basicUser` | `cfedge` |
| `basicPass` | STEP 2에서 설정한 실제 비밀번호 |

4. **Next** → Secret name: `cjfv/bakery-edge` → **Next** → 로테이션 설정 없이 → **Store**
5. 생성된 시크릿 클릭 → **Secret ARN** 메모 (4-3의 IAM 정책에 사용)

## 4-2. 코드 준비 (로컬 터미널)

> **사전 준비물**: [Node.js LTS](https://nodejs.org) 설치 (npm/npx 포함)

프로젝트 폴더 생성:

**macOS/Linux:**
```bash
mkdir cognito-edge && cd cognito-edge
npm init -y && npm install cognito-at-edge
```

**윈도우 PowerShell:**
```powershell
mkdir cognito-edge; cd cognito-edge
npm init -y; npm install cognito-at-edge
```

`index.js` 파일을 아래 내용으로 생성합니다. **코드에 넣을 값은 시크릿 이름 하나뿐**입니다.

```js
const { Authenticator } = require('cognito-at-edge');
const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

const SECRET_ID = 'cjfv/bakery-edge';   // ← 4-1에서 만든 시크릿 이름

const sm = new SecretsManagerClient({ region: 'ap-northeast-2' });  // ← 시크릿을 서울에 생성

// 시크릿 캐시 (5분) — 매 요청 조회 방지 + 시크릿 수정 시 5분 내 자동 반영
let cache = null;
let cachedAt = 0;
const TTL_MS = 5 * 60 * 1000;

async function getConfig() {
  if (cache && Date.now() - cachedAt < TTL_MS) return cache;
  const res = await sm.send(new GetSecretValueCommand({ SecretId: SECRET_ID }));
  const s = JSON.parse(res.SecretString);
  cache = {
    authenticator: new Authenticator({
      region: 'ap-northeast-2',            // ★ Cognito User Pool 리전 (서울)
      userPoolId: s.userPoolId,
      userPoolAppId: s.appClientId,
      userPoolAppSecret: s.appClientSecret,
      userPoolDomain: s.cognitoDomain,     // ★ https:// 없이 도메인만
    }),
    // base64 변환은 코드가 자동 수행
    basic: 'Basic ' + Buffer.from(`${s.basicUser}:${s.basicPass}`).toString('base64'),
  };
  cachedAt = Date.now();
  return cache;
}

exports.handler = async (event) => {
  const cf = event.Records[0].cf;
  const cfg = await getConfig();
  if (cf.config.eventType === 'origin-request') {
    // 오리진(Amplify) 직전: Host 교정 + Basic Auth 주입
    const req = cf.request;
    req.headers.host = [{ key: 'Host', value: req.origin.custom.domainName }];
    req.headers.authorization = [{ key: 'Authorization', value: cfg.basic }];
    return req;
  }
  // viewer-request: Cognito 인증
  return cfg.authenticator.handle(event);
};
```

### 번들 + zip 만들기

Lambda@Edge는 **1MB 제한**이 있어 esbuild 번들이 필수입니다. AWS SDK는 런타임 내장이라 번들에서 제외합니다.

**macOS/Linux:**
```bash
npx esbuild index.js --bundle --minify --platform=node --target=node20 \
  "--external:@aws-sdk/*" --outfile=dist/index.js
cd dist && zip ../fn.zip index.js && cd ..
ls -lh fn.zip   # 1MB 미만 확인 (보통 ~90KB)
```

> ⚠️ `--external:@aws-sdk/*` 는 반드시 **따옴표로 감싸세요.** macOS 기본 셸(zsh)이 `*`를 파일 검색 패턴으로 해석해 `no matches found` 오류가 납니다 (실제 겪은 오류).

**윈도우 PowerShell** (`zip` 명령이 없으므로 `Compress-Archive` 사용):
```powershell
npx esbuild index.js --bundle --minify --platform=node --target=node20 "--external:@aws-sdk/*" --outfile=dist/index.js
Compress-Archive -Path dist\index.js -DestinationPath fn.zip -Force
Get-Item fn.zip   # Length가 1MB(1048576) 미만인지 확인
```

## 4-3. IAM 역할 만들기

> 🌎 IAM은 글로벌이지만, 이 역할은 us-east-1의 Lambda@Edge에 연결됩니다. 인라인 정책의 Secret ARN 리전은 **ap-northeast-2(서울)** 입니다.

1. **IAM** → **Roles** → **Create role** → Trusted entity: **Lambda** → 정책 `AWSLambdaBasicExecutionRole` 연결 → 이름 `bakery-edge-role` → 생성
2. 생성된 역할 → **Trust relationships** 탭 → **Edit trust policy** → 아래로 교체 후 저장:

```json
{ "Version": "2012-10-17", "Statement": [{ "Effect": "Allow",
  "Principal": { "Service": ["lambda.amazonaws.com", "edgelambda.amazonaws.com"] },
  "Action": "sts:AssumeRole" }] }
```

> ⚠️ `edgelambda.amazonaws.com`이 없으면 CloudFront 연결 단계에서 오류가 납니다.

3. **Permissions** 탭 → **Add permissions → Create inline policy** → JSON 탭에 아래 입력 (Resource는 4-1의 **Secret ARN**으로 교체) → 이름 `read-bakery-edge-secret` → 생성:

```json
{ "Version": "2012-10-17", "Statement": [{ "Effect": "Allow",
  "Action": "secretsmanager:GetSecretValue",
  "Resource": "arn:aws:secretsmanager:ap-northeast-2:계정번호:secret:cjfv/bakery-edge-XXXXXX" }] }
```

## 4-4. 함수 생성

> 🌎 **여기서만 리전을 us-east-1(버지니아)로 바꿉니다.** 이 가이드에서 us-east-1에 만드는 리소스는 **이 Lambda 함수(+4-3의 IAM 역할)뿐**입니다. Secrets Manager(서울)와 리전이 달라도, 코드에서 `region: 'ap-northeast-2'`로 지정했으므로 정상 조회됩니다.

1. **Lambda** (리전 **us-east-1** 확인) → **Create function** → Author from scratch
2. Function name: `cjfv-bakery-edge-auth`, Runtime: **Node.js 20.x**, Execution role: `bakery-edge-role`
3. 생성 후 **Code** 탭 → **Upload from → .zip file** → `fn.zip` 업로드
4. **Configuration → General configuration → Edit** → Timeout **5초** → 저장

> 💡 **왜 콘솔 편집기에 붙여넣지 않고 zip으로 올리나?** 코드가 외부 라이브러리(`cognito-at-edge`)를 쓰기 때문에, esbuild로 라이브러리까지 합친 **번들 파일**을 올려야 동작합니다. 업로드 후 콘솔에서 코드가 한 줄로 뭉개져 보이는 것은 minify(압축) 때문이며 정상입니다 — **읽을 수 있는 원본은 로컬 `index.js`** 이고, 수정도 항상 로컬에서 합니다.

## 4-5. 버전 게시 (★ 필수)

1. **Actions → Publish new version** → Publish
2. 버전 ARN 메모 → `LAMBDA_VERSION_ARN` (예: `arn:aws:lambda:us-east-1:1234...:function:cjfv-bakery-edge-auth:1`)

> ⚠️ **코드를 수정할 때마다 3단계 반복**: ① 재번들·재업로드 → ② **새 버전 게시** → ③ CloudFront에 **새 버전 ARN 재연결**. 하나라도 빠지면 수정이 반영되지 않습니다.
>
> 💡 단, **비밀값(비번 등) 변경은 코드 수정이 아닙니다** — Secrets Manager에서 시크릿 값만 수정하면 5분 내 자동 반영됩니다.

## 완료 확인

- [ ] 시크릿 생성 (키 6개) + Secret ARN 메모
- [ ] `fn.zip` 1MB 미만 확인
- [ ] IAM 역할: 신뢰정책에 `edgelambda` 포함 + 시크릿 읽기 인라인 정책
- [ ] 함수 생성 + zip 업로드 + Timeout 5초
- [ ] **버전 게시** + `LAMBDA_VERSION_ARN` 메모

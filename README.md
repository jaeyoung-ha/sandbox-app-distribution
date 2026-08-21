# 사내 앱 배포 가이드

> **CloudFront + Lambda@Edge + Cognito** 로 AWS Amplify 앱에 로그인을 강제하는 콘솔 스텝별 가이드

## 이 가이드에서 만드는 것

- **베이커리 상권분석 시스템**(정적 HTML 단일 앱)을 AWS Amplify로 배포하고
- 앱 앞단에 **CloudFront + Lambda@Edge** 인증을 붙여, **로그인한 사용자만** 접근하도록 만듭니다
- 사용자 계정은 **Amazon Cognito**로 관리합니다 (개인별 계정, 관리자가 발급·회수)

## 이 방식의 특징

| 특징 | 설명 |
|---|---|
| 로그인 전 소스 미전송 | 인증되지 않은 요청에는 HTML이 브라우저로 **아예 전송되지 않습니다** |
| 앱 코드 무수정 | 인증은 엣지 서버(Lambda@Edge)에서 실행 — 앱 `index.html`은 한 줄도 고치지 않습니다 |
| 우회 접속 차단 | Amplify 원래 주소(`...amplifyapp.com`)로 직접 접속하면 Basic Auth(401)로 차단됩니다 |
| 개인별 계정 | 1인 1계정(이메일). 로그인 추적, 개인 단위 회수/비활성화 가능 |

## 진행 순서

1. **[전체 그림 이해하기](overview/architecture.md)** — 구조와 핵심 개념 (5분)
2. **[STEP 1~5](steps/step1-amplify-deploy.md)** — 구축 (Amplify → Cognito → Lambda@Edge → CloudFront)
3. **[STEP 6~7](steps/step6-create-users.md)** — 사용자 계정 운영
4. **[STEP 8](steps/step8-test.md)** — 동작 테스트

> ⚠️ **리전 주의**: **Lambda@Edge 함수(+IAM 역할)만 us-east-1 (버지니아 북부)** 에 만들고, 나머지(**Amplify·Cognito·Secrets Manager**)는 **ap-northeast-2 (서울)** 에 만듭니다. Lambda@Edge가 us-east-1을 강제하기 때문입니다. CloudFront는 글로벌 서비스입니다.

## 사전 준비물

- AWS 콘솔 접근 권한 (Amplify, Cognito, Lambda, CloudFront, Secrets Manager, IAM)
- [Node.js LTS](https://nodejs.org) 설치된 PC (macOS/윈도우 모두 가능)
- 배포할 앱 파일 (`index.html`)

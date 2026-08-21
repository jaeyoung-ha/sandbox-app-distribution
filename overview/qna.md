# 미팅 질의 답변 요약

PoC 관련 질의 5개 항목에 대한 결론 요약입니다.

## Q1. AWS Cognito 기반 PoC 실 사용자 계정 생성 방법

**가능.** 관리자가 Cognito 콘솔에서 개별 사용자 생성(이메일 + 임시 비번 + 초대 메일). 최초 로그인 시 본인 비번으로 강제 변경. → [STEP 6](steps/step6-create-users.md)

## Q2. PoC 애플리케이션 – Cognito 연동 방안

**CloudFront + Lambda@Edge 방식**으로 연동. 앱 앞단의 CloudFront가 모든 요청에서 인증을 강제하고, 미인증 사용자는 Cognito 로그인 페이지로 자동 이동.

- **앱 코드 무수정**
- **로그인 전 소스 미전송**
- **Amplify 직접 URL 우회 차단**

→ [STEP 1~5](steps/step1-amplify-deploy.md)

## Q3. 실 사용자 개별 계정 운영 가능 여부

**가능.** 1인 1계정(개별 이메일). 로그인 추적, 개인 단위 회수/비활성화 가능. 베이커리 앱 1개 + User Pool 1개로 운영.

## Q4. 관리자의 사용자 추가·비밀번호 재설정 권한

**가능.** `AmazonCognitoPowerUser`(또는 특정 User Pool로 좁힌 최소권한) 부여 시 콘솔에서 직접 수행.

| 작업 | 콘솔 위치 |
|---|---|
| 사용자 추가 | Users → Create user |
| 비밀번호 재설정 | 사용자 선택 → Actions → Reset password |
| 사용자 삭제/비활성화 | 사용자 선택 → Delete / Disable |

→ [STEP 6~7](steps/step6-create-users.md)

## Q5. 배포 URL 변경 절차

**가능.** 사용자 접속 주소는 CloudFront이므로, **커스텀 도메인을 CloudFront에 연결**(ACM 인증서 + CNAME + DNS)하면 됩니다. 변경 후 **Cognito 콜백 URL 재등록 필수**. (도메인 변경 절차는 별도 가이드로 진행)

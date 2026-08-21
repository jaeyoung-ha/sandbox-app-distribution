# STEP 6. 실 사용자 계정 생성

관리자가 Cognito 콘솔에서 사용자 계정을 발급합니다.

## 사용자 생성

1. Cognito(ap-northeast-2) → User Pool → **Users** 탭 → **Create user**
2. 입력:

| 항목 | 값 |
|---|---|
| Invitation message | **Send an email invitation** |
| Email address | 사용자 회사 이메일 |
| **Mark email address as verified** | ✅ **반드시 체크** |
| Temporary password | **Generate a password** 또는 직접 지정 |

3. **Create user** → 인원수만큼 반복

> ⚠️ **"Mark email address as verified"를 안 켜면** 나중에 관리자 비밀번호 재설정([STEP 7](steps/step7-reset-password.md))이 실패합니다. verified 이메일이 없으면 확인 코드를 발송할 수 없기 때문입니다.

## 사용자 흐름

1. 사용자는 초대 메일로 **임시 비밀번호**를 받음
2. 첫 로그인 시 **본인 비밀번호로 강제 변경**
3. 이후 같은 주소로 접속해 로그인만 하면 됨

## 계정 회수/차단

| 작업 | 콘솔 위치 |
|---|---|
| 삭제 (완전 회수) | Users → 대상 선택 → **Delete user** |
| 비활성화 (임시 차단) | Users → 대상 선택 → **Disable user** |

## 이메일 발송 한도

> 📧 SES 미연동 기본 설정에서는 하루 발송량 제한이 있습니다 (풀당 약 50통, 발신 `no-reply@verificationemail.com`). PoC 인원 수준이면 충분하지만, 하루에 대량 초대/재설정을 반복하면 메일이 안 갈 수 있습니다.

## 완료 확인

- [ ] 사용자 계정 생성 (verified 체크 포함)
- [ ] 초대 메일 수신 확인

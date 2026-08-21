# STEP 7. 비밀번호 재설정 (관리자)

사용자가 비밀번호를 잊었을 때 관리자가 재설정하는 방법입니다.

## 방법 1 — 콘솔 (권장)

1. Cognito(ap-northeast-2) → User Pool → **Users** → 대상 사용자 선택
2. **Actions → Reset password** → **Reset**

**동작:**
- 사용자에게 **확인 코드 발송** (1시간 유효)
- 사용자 상태가 `RESET_REQUIRED`로 변경
- 사용자는 로그인 화면의 비밀번호 찾기 흐름으로 새 비번 설정

> ⚠️ **전제**: 사용자 이메일이 **verified** 상태여야 합니다 ([STEP 6](steps/step6-create-users.md)에서 "Mark email address as verified"를 체크했으면 OK). verified가 아니면 재설정이 오류로 실패합니다.

## 방법 2 — CLI (즉시 지정)

AWS CLI 설치 + 관리자 자격증명 필요. macOS/윈도우 공통으로 동작하는 한 줄 명령입니다.

```bash
aws cognito-idp admin-set-user-password --user-pool-id ap-northeast-2_xxxxxxx --username user@example.com --password "임시비번!1" --region ap-northeast-2
```

- `--permanent` 추가 시 **영구 비번** (즉시 사용 가능)
- 없으면 **임시 비번** (첫 로그인 시 변경 강제)

## 완료 확인

- [ ] 재설정 절차 1회 테스트 (코드 수신 → 새 비번 설정 → 로그인)

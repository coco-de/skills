---
name: inspector/form
description: "폼 상태 및 유효성 검사 런타임 디버깅"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/form

> **Context Framework Note**: 폼 관련 문제 디버깅 시 활성화됩니다.

## Triggers

- 폼 제출 실패
- 유효성 검사 문제
- 필드 상태 확인

## MCP Tools

### form_list
현재 화면의 모든 폼을 나열합니다.

**응답 예시**:
```json
{
  "forms": [
    {
      "key": "loginForm",
      "fieldCount": 3,
      "isValid": false,
      "fields": ["email", "password", "rememberMe"]
    }
  ]
}
```

### form_get_state
특정 폼의 상세 상태를 반환합니다.

**파라미터**:
- `formKey`: 폼 키 (필수)

**응답 예시**:
```json
{
  "formKey": "loginForm",
  "state": {
    "isValid": false,
    "fields": {
      "email": {
        "value": "user@example",
        "isValid": false,
        "error": "올바른 이메일 형식이 아닙니다"
      },
      "password": {
        "value": "***",
        "isValid": true,
        "error": null
      }
    }
  }
}
```

### form_get_errors
폼의 모든 에러를 반환합니다.

### form_validate
폼을 수동으로 유효성 검사합니다.

## Common Diagnostics

### 폼 제출 안 됨
```
1. form_get_state → 현재 상태 확인
2. isValid: false인 경우 에러 확인
3. form_get_errors → 모든 에러 조회
4. 유효성 검사 로직 검토
```

### 유효성 검사 작동 안 함
```
1. form_validate → 수동 검사 실행
2. 에러 메시지 확인
3. validator 함수 로직 검토
```

### 필드 값 유지 안 됨
```
1. form_get_state → 필드 값 확인
2. TextEditingController 연결 확인
3. 폼 상태 복원 로직 검토
```

### 에러 메시지 안 보임
```
1. form_get_errors → 에러 존재 확인
2. ErrorText 위젯 렌더링 확인
3. AutovalidateMode 설정 확인
```

## Examples

### 폼 목록 확인

```
/inspector/form list
```

### 폼 상태 확인

```
/inspector/form state loginForm
```

### 폼 에러 확인

```
/inspector/form errors
```

### 수동 유효성 검사

```
/inspector/form validate loginForm
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-form.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`
- UI 인스펙터: `.claude/commands/inspector/ui.md`

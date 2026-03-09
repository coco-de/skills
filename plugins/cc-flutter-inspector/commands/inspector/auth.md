---
name: inspector/auth
description: "인증 상태 런타임 디버깅"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/auth

> **Context Framework Note**: 인증 관련 문제 디버깅 시 활성화됩니다.

## Triggers

- 로그인 문제
- 토큰 만료 이슈
- 인증 상태 확인

## MCP Tools

### auth_get_status
현재 인증 상태를 반환합니다.

**응답 예시**:
```json
{
  "isAuthenticated": true,
  "authMethod": "email",
  "tokenStatus": {
    "accessToken": {
      "exists": true,
      "expiresAt": "2024-01-01T12:00:00Z",
      "isExpired": false,
      "expiresIn": "45 minutes"
    },
    "refreshToken": {
      "exists": true,
      "expiresAt": "2024-01-08T10:00:00Z",
      "isExpired": false
    }
  }
}
```

### auth_get_user
현재 로그인된 사용자 정보를 반환합니다.

**응답 예시**:
```json
{
  "user": {
    "id": 123,
    "email": "user@example.com",
    "name": "홍길동",
    "roles": ["user", "premium"],
    "createdAt": "2023-06-15T10:00:00Z"
  }
}
```

## Common Diagnostics

### 로그인 안 됨
```
1. auth_get_status → 인증 상태 확인
2. tokenStatus 검증
3. 로그인 플로우 검토
```

### 401 Unauthorized 에러
```
1. auth_get_status → 토큰 만료 확인
2. refreshToken 상태 확인
3. 토큰 갱신 로직 검토
```

### 권한 부족 에러
```
1. auth_get_user → 사용자 역할 확인
2. 필요 권한과 비교
3. 권한 검사 로직 검토
```

### 자동 로그아웃 문제
```
1. auth_get_status → 토큰 만료 시간 확인
2. 세션 타임아웃 설정 확인
3. 토큰 갱신 타이밍 검토
```

## Examples

### 인증 상태 확인

```
/inspector/auth status
```

### 사용자 정보 확인

```
/inspector/auth user
```

### 토큰 상태 상세 확인

```
/inspector/auth token
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-auth.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`
- 네트워크 인스펙터: `.claude/commands/inspector/network.md`

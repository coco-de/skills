---
name: inspector/network
description: "HTTP 요청/응답 런타임 로깅 및 분석"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/network

> **Context Framework Note**: API 통신 문제 디버깅 시 활성화됩니다.

## Triggers

- API 호출 실패
- 네트워크 타임아웃
- 응답 데이터 문제

## MCP Tools

### network_get_logs
최근 HTTP 요청/응답 로그를 반환합니다.

**파라미터**:
- `limit`: 최대 개수 (기본 50)
- `method`: HTTP 메소드 필터 (GET, POST, PUT, DELETE)
- `path`: URL 경로 필터

**응답 예시**:
```json
{
  "logs": [
    {
      "id": "req_001",
      "timestamp": "2024-01-01T10:00:00Z",
      "method": "GET",
      "url": "https://api.example.com/users/123",
      "statusCode": 200,
      "duration": 245,
      "responseSize": 1024
    }
  ]
}
```

### network_get_errors
실패한 요청만 필터링하여 반환합니다.

### network_get_stats
네트워크 통계를 반환합니다.

### network_clear_logs
네트워크 로그를 초기화합니다.

## Common Diagnostics

### API 응답 느림
```
1. network_get_logs → duration 확인
2. 느린 요청 식별
3. 서버 성능 또는 네트워크 문제 판단
```

### 401 Unauthorized
```
1. network_get_errors → 401 에러 확인
2. requestHeaders의 Authorization 확인
3. /inspector/auth로 토큰 상태 확인
```

### 500 Server Error
```
1. network_get_errors → 상세 확인
2. responseBody에서 에러 메시지 확인
3. 요청 파라미터 검토
```

### 타임아웃
```
1. network_get_errors → timeout 에러 확인
2. 네트워크 연결 상태 확인
3. 타임아웃 설정값 검토
```

## Examples

### 최근 API 호출 확인

```
/inspector/network logs
```

### 특정 엔드포인트 필터링

```
/inspector/network logs --path /users
```

### 에러 요청만 확인

```
/inspector/network errors
```

### 네트워크 통계

```
/inspector/network stats
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-network.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`
- 인증 인스펙터: `.claude/commands/inspector/auth.md`

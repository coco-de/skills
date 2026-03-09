---
name: inspector/log
description: "앱 로그 런타임 관리 및 분석"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/log

> **Context Framework Note**: 앱 로그 분석 시 활성화됩니다.

## Triggers

- 에러 로그 확인
- 디버그 메시지 검색
- 로그 패턴 분석

## MCP Tools

### log_get_recent
최근 로그를 반환합니다.

**파라미터**:
- `limit`: 최대 개수 (기본 50)
- `level`: 로그 레벨 필터 (debug, info, warning, error)

**응답 예시**:
```json
{
  "logs": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "level": "info",
      "tag": "AuthBloc",
      "message": "User logged in successfully",
      "data": {"userId": 123}
    }
  ]
}
```

### log_get_errors
에러 로그만 필터링하여 반환합니다.

**파라미터**:
- `limit`: 최대 개수 (기본 20)
- `includeStackTrace`: 스택 트레이스 포함 여부

### log_search
로그에서 특정 패턴을 검색합니다.

**파라미터**:
- `query`: 검색 문자열 (필수)
- `tag`: 태그 필터
- `limit`: 최대 개수

### log_get_stats
로그 통계를 반환합니다.

### log_clear
로그를 초기화합니다.

## Common Diagnostics

### 반복되는 에러
```
1. log_get_errors → 에러 패턴 확인
2. 동일 태그에서 반복 발생 확인
3. 에러 컨텍스트 분석
```

### 성능 문제 추적
```
1. log_search query="slow" 또는 "timeout"
2. 관련 시간대 로그 분석
3. 병목 지점 식별
```

### 앱 크래시 원인
```
1. log_get_errors → 마지막 에러 확인
2. 스택 트레이스 분석
3. 에러 발생 직전 로그 추적
```

## Examples

### 최근 로그 확인

```
/inspector/log recent
```

### 에러 로그만 확인

```
/inspector/log errors
```

### 특정 키워드 검색

```
/inspector/log search auth
```

### 로그 통계

```
/inspector/log stats
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-log.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`

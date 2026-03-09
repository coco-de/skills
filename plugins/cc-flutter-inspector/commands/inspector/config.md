---
name: inspector/config
description: "설정 및 피처 플래그 런타임 디버깅"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/config

> **Context Framework Note**: 설정 및 피처 플래그 문제 디버깅 시 활성화됩니다.

## Triggers

- 환경 설정 확인
- 피처 플래그 상태
- 환경별 설정 검증

## MCP Tools

### config_get_all
모든 설정 값을 반환합니다.

**파라미터**:
- `includeSecrets`: 민감한 값 포함 여부 (마스킹)

**응답 예시**:
```json
{
  "config": {
    "apiBaseUrl": "https://api.example.com",
    "apiKey": "***masked***",
    "timeout": 30000,
    "cacheEnabled": true
  }
}
```

### config_get_value
특정 설정 값을 반환합니다.

**파라미터**:
- `key`: 설정 키 (필수)

### config_get_feature_flags
피처 플래그 상태를 반환합니다.

**응답 예시**:
```json
{
  "featureFlags": {
    "ui": {
      "darkModeEnabled": true,
      "newHomeLayout": false
    },
    "api": {
      "useNewEndpoint": true
    }
  }
}
```

### config_get_environment
현재 환경 정보를 반환합니다.

**응답 예시**:
```json
{
  "environment": {
    "name": "development",
    "isDebug": true,
    "flavor": "dev",
    "version": "1.0.0"
  }
}
```

## Common Diagnostics

### 피처가 동작하지 않음
```
1. config_get_feature_flags → 플래그 상태 확인
2. 해당 피처 플래그 값 확인
3. 플래그 조건 로직 검토
```

### 환경 설정 불일치
```
1. config_get_environment → 현재 환경 확인
2. config_get_all → 설정 값 확인
3. 예상 환경과 비교
```

### API 연결 문제
```
1. config_get_value key="apiBaseUrl" 확인
2. 올바른 엔드포인트인지 검증
3. 환경별 설정 차이 확인
```

## Examples

### 전체 설정 확인

```
/inspector/config all
```

### 특정 설정 확인

```
/inspector/config value apiBaseUrl
```

### 피처 플래그 확인

```
/inspector/config flags
```

### 환경 정보 확인

```
/inspector/config env
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-config.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`

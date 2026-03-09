---
name: inspector/bloc
description: "BLoC/Cubit 상태 런타임 추적"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/bloc

> **Context Framework Note**: BLoC 상태 관리 디버깅 시 활성화됩니다.

## Triggers

- 상태 변화 추적
- BLoC 이벤트 디버깅
- 상태 불일치 문제

## MCP Tools

### bloc_list_active
현재 활성화된 BLoC/Cubit 목록을 반환합니다.

**응답 예시**:
```json
{
  "blocs": [
    {"type": "AuthBloc", "state": "Authenticated"},
    {"type": "HomeBloc", "state": "Loaded"},
    {"type": "CartCubit", "state": "Empty"}
  ]
}
```

### bloc_get_state
특정 BLoC의 현재 상태를 반환합니다.

**응답 예시**:
```json
{
  "type": "HomeBloc",
  "state": {
    "status": "loaded",
    "items": 15,
    "selectedCategory": "all"
  }
}
```

### bloc_get_history
BLoC의 상태 변화 히스토리를 반환합니다.

### bloc_get_events
발생한 이벤트 히스토리를 반환합니다.

## Common Diagnostics

### 상태가 업데이트 안 됨
```
1. bloc_list_active → BLoC 존재 확인
2. bloc_get_events → 이벤트 발생 확인
3. bloc_get_history → 상태 변화 추적
```

### 예상과 다른 상태
```
1. bloc_get_state → 현재 상태 확인
2. bloc_get_history → 변화 과정 추적
3. 이벤트 핸들러 로직 검토
```

### BLoC 리빌드 과다
```
1. bloc_get_events → 이벤트 빈도 확인
2. buildWhen 조건 검토
3. 상태 비교 로직 확인
```

## Examples

### 활성 BLoC 목록 확인

```
/inspector/bloc list
```

### 특정 BLoC 상태 확인

```
/inspector/bloc state HomeBloc
```

### 이벤트 히스토리 확인

```
/inspector/bloc events AuthBloc
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-bloc.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`

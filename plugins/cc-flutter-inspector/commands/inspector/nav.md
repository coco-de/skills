---
name: inspector/nav
description: "GoRouter 네비게이션 런타임 디버깅"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/nav

> **Context Framework Note**: GoRouter 네비게이션 디버깅 시 활성화됩니다.

## Triggers

- 화면 전환 문제
- 라우트 파라미터 문제
- 딥링크 디버깅

## MCP Tools

### nav_get_current_route
현재 라우트 정보를 반환합니다.

### nav_get_history
네비게이션 히스토리 스택을 반환합니다.

### nav_get_params
현재 라우트의 파라미터를 반환합니다.

### nav_go
특정 경로로 이동합니다.

### nav_push
새 경로를 스택에 푸시합니다.

### nav_pop
현재 라우트를 팝합니다.

### nav_replace
현재 라우트를 대체합니다.

### nav_clear
네비게이션 스택을 초기화합니다.

## Common Diagnostics

### 화면 전환이 안 됨
```
1. nav_get_current_route → 현재 위치 확인
2. nav_get_history → 스택 상태 확인
3. 라우트 정의 검토
```

### 파라미터 전달 안 됨
```
1. nav_get_params → 현재 파라미터 확인
2. 전송 측 코드 검토
3. 수신 측 파싱 검토
```

### 뒤로가기 문제
```
1. nav_get_history → 스택 깊이 확인
2. nav_pop 테스트
3. popUntil 로직 검토
```

## Examples

### 현재 라우트 확인

```
/inspector/nav current
```

### 네비게이션 히스토리 확인

```
/inspector/nav history
```

### 특정 경로로 이동 테스트

```
/inspector/nav go /home
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-nav.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`

---
name: inspector/ui
description: "위젯 트리 런타임 검사 및 분석"
category: petmedi-development
complexity: simple
mcp-servers: [flutter-inspector]
---

# /inspector/ui

> **Context Framework Note**: UI 레이아웃 문제 디버깅 시 활성화됩니다.

## Triggers

- 레이아웃 오버플로우
- 위젯 트리 분석
- UI 구조 확인

## MCP Tools

### ui_get_widget_tree
현재 화면의 위젯 트리를 반환합니다.

**파라미터**:
- `depth`: 트리 깊이 (기본 5)
- `includeRenderObjects`: RenderObject 정보 포함

**응답 예시**:
```json
{
  "tree": {
    "type": "MaterialApp",
    "children": [
      {
        "type": "Scaffold",
        "children": [
          {"type": "AppBar", "properties": {"title": "Home"}},
          {"type": "ListView", "children": [...]}
        ]
      }
    ]
  }
}
```

### ui_find_widgets
특정 타입의 위젯을 검색합니다.

**파라미터**:
- `type`: 위젯 타입명 (예: Text, Container)
- `key`: 위젯 Key 값

### ui_get_screen_info
현재 화면 정보를 반환합니다.

### ui_find_overflow
오버플로우 문제가 있는 위젯을 찾습니다.

### ui_get_text_widgets
모든 텍스트 위젯과 내용을 반환합니다.

## Common Diagnostics

### 레이아웃 오버플로우
```
1. ui_find_overflow → 문제 위젯 식별
2. 해당 위젯 경로 확인
3. constraints vs size 비교
4. Expanded, Flexible, SingleChildScrollView 적용 제안
```

### 위젯 찾기 실패
```
1. ui_find_widgets type="TargetWidget"
2. 위젯 존재 여부 확인
3. 위젯 트리 경로 추적
4. 조건부 렌더링 로직 검토
```

### UI 성능 문제
```
1. ui_get_widget_tree → 깊이 확인
2. 불필요하게 깊은 중첩 식별
3. const 위젯 사용 여부 확인
4. /inspector/bloc로 리빌드 빈도 분석
```

### 반응형 레이아웃
```
1. ui_get_screen_info → 화면 크기 확인
2. 다양한 크기에서 ui_find_overflow 실행
3. MediaQuery 기반 조건 검토
```

## Examples

### 위젯 트리 확인

```
/inspector/ui tree
```

### 오버플로우 검사

```
/inspector/ui overflow
```

### 화면 정보 확인

```
/inspector/ui screen
```

### 텍스트 위젯 찾기

```
/inspector/ui texts
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector-ui.md`
- 마스터 인스펙터: `.claude/commands/inspector.md`
- BLoC 인스펙터: `.claude/commands/inspector/bloc.md`

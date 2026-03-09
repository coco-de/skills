---
name: flutter-ui
description: "Figma 디자인을 Flutter UI 컴포넌트로 변환 (CoUI 디자인 시스템)"
invoke: /flutter:ui
aliases: ["/ui", "/21", "/coui"]
category: petmedi-development
complexity: moderate
mcp-servers: [magic, figma-daisyui, serena]
---

# /flutter-ui

> **Context Framework Note**: Figma 디자인을 Flutter UI로 변환할 때 활성화됩니다.

## Triggers

- Figma 프레임/컴포넌트를 Flutter로 변환할 때
- CoUI 디자인 시스템 기반 UI 개발
- `/ui`, `/21` 키워드 사용 시

## Context Trigger Pattern

```
/flutter-ui {component_type} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `component_type` | ✅ | 컴포넌트 타입 | `button`, `card`, `form`, `page` |
| `--figma-node` | ❌ | Figma 노드 ID | `12:345` |
| `--name` | ❌ | 컴포넌트 이름 | `ProductCard` |
| `--feature` | ❌ | 소속 Feature | `home`, `store` |

## Execution Flow

```
┌─────────────────────────────────────────┐
│  1. Figma 노드 분석 (MCP: figma-daisyui)  │
├─────────────────────────────────────────┤
│  • get_selection / get_node_info        │
│  • extract_tailwind                     │
│  • scan_text_nodes                      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  2. CoUI 컴포넌트 매핑                    │
├─────────────────────────────────────────┤
│  • DaisyUI 클래스 → CoUI 위젯           │
│  • 색상 변수 → AppColors                │
│  • 타이포그래피 → AppTextStyles         │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  3. Flutter 코드 생성 (MCP: magic)       │
├─────────────────────────────────────────┤
│  • 21st_magic_component_builder         │
│  • Widget 구조 생성                      │
│  • 반응형 레이아웃 적용                   │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  4. 프로젝트 통합                         │
├─────────────────────────────────────────┤
│  • Feature 위젯 디렉토리에 배치           │
│  • Widgetbook UseCase 생성              │
│  • 테스트 파일 생성                       │
└─────────────────────────────────────────┘
```

## CoUI Design System

### 색상 매핑

```dart
// Figma Variable → Flutter
base-100     → AppColors.background
base-200     → AppColors.surface
base-300     → AppColors.surfaceVariant
primary      → AppColors.primary
secondary    → AppColors.secondary
accent       → AppColors.accent
neutral      → AppColors.neutral
```

### 컴포넌트 매핑

| Figma/DaisyUI | Flutter/CoUI |
|---------------|--------------|
| btn | CoButton |
| card | CoCard |
| input | CoTextField |
| modal | CoDialog |
| drawer | CoDrawer |
| navbar | CoAppBar |
| avatar | CoAvatar |
| badge | CoBadge |
| tabs | CoTabBar |

### 타이포그래피

```dart
// Text Styles
headline-lg  → AppTextStyles.headlineLarge
headline-md  → AppTextStyles.headlineMedium
body-lg      → AppTextStyles.bodyLarge
body-md      → AppTextStyles.bodyMedium
label-lg     → AppTextStyles.labelLarge
```

## Output Template

### Widget 파일

```dart
import 'package:flutter/material.dart';
import 'package:resources/resources.dart';

/// {component_name} 위젯
///
/// Figma: {figma_node_link}
class {ComponentName} extends StatelessWidget {
  const {ComponentName}({
    required this.title,
    this.onTap,
    super.key,
  });

  final String title;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return Container(
      // CoUI 디자인 시스템 적용
    );
  }
}
```

### Widgetbook UseCase

```dart
@UseCase(name: 'Default', type: {ComponentName})
Widget buildDefault(BuildContext context) {
  return const {ComponentName}(
    title: 'Sample Title',
  );
}
```

## MCP Integration

| 단계 | MCP 서버 | 도구 |
|------|----------|------|
| Figma 분석 | figma-daisyui | get_node_info, extract_tailwind |
| UI 생성 | magic | 21st_magic_component_builder |
| 코드 검색 | serena | find_symbol, search_for_pattern |

## 핵심 규칙

### Widget 구조
- `const` 생성자 우선
- `super.key` 항상 마지막 파라미터
- 재사용 가능한 작은 단위로 분리

### 스타일링
- 하드코딩 색상 금지 → `AppColors.*` 사용
- `withOpacity()` 금지 → `withValues(alpha:)` 사용
- 매직 넘버 금지 → 디자인 토큰 사용

### 반응형
- `LayoutBuilder` 또는 `MediaQuery` 활용
- 최소 터치 타겟 48x48

## Examples

### 버튼 컴포넌트 생성

```
/flutter-ui button --name PrimaryButton --feature common
```

### Figma 카드 변환

```
/flutter-ui card --figma-node 12:345 --name ProductCard --feature store
```

### 전체 페이지 변환

```
/flutter-ui page --figma-node 1:100 --name HomePage --feature home
```

## 참조

- 상세 구현: `.claude/agents/flutter-ui.md`
- CoUI 컴포넌트: `package/coui/`
- 색상 시스템: `package/resources/lib/src/core/theme/`

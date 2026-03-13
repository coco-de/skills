---
name: coui-keyboard-shortcut
description: Activate when creating keyboard shortcut displays with labels, shortcut lists for settings/help screens, or platform-aware key combination indicators using CouiKeyboardShortcut/ShortcutPlatform (Flutter) or KeyboardShortcut (Web) in CoUI Flutter or CoUI Web.
---

# CoUI KeyboardShortcut

## Overview

The KeyboardShortcut component displays keyboard shortcuts alongside descriptive labels. It is commonly used in settings screens, help sections, and sidebar menus to communicate keyboard combinations with automatic platform detection.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiKeyboardShortcut(
  shortcut: ['Ctrl', 'S'],
  label: '저장',
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `shortcut` | `List<String>` | required | List of keys comprising the shortcut |
| `label` | `String` | required | Descriptive text for the action |
| `platform` | `ShortcutPlatform` | `auto` | Platform styling (auto/mac/windows/linux) |

### With Platform Detection

```dart
CouiKeyboardShortcut(
  shortcut: ['Cmd', 'K'],
  label: '검색 열기',
  platform: ShortcutPlatform.auto,
)
```

### Shortcut List

```dart
Column(
  children: [
    CouiKeyboardShortcut(shortcut: ['Ctrl', 'Z'], label: '실행 취소'),
    CouiKeyboardShortcut(shortcut: ['Ctrl', 'Y'], label: '다시 실행'),
    CouiKeyboardShortcut(shortcut: ['Ctrl', 'C'], label: '복사'),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
KeyboardShortcut(
  shortcut: ['Ctrl', 'S'],
  label: '저장',
)
```

### Parameters

Same parameter structure as Flutter with identical property names.

## Common Patterns

### Platform Support

| Platform | Value | Symbols |
|----------|-------|---------|
| macOS | `ShortcutPlatform.mac` | cmd, opt, shift, ctrl |
| Windows | `ShortcutPlatform.windows` | Ctrl, Alt, Shift, Win |
| Linux | `ShortcutPlatform.linux` | Ctrl, Alt, Shift, Super |
| Auto | `ShortcutPlatform.auto` | System-appropriate symbols |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiKeyboardShortcut` | `KeyboardShortcut` |
| API | Identical parameters | Identical parameters |

### When to Use

- Settings screen shortcut reference
- Help page keyboard shortcuts
- Menu item trailing shortcut labels
- Command palette key bindings

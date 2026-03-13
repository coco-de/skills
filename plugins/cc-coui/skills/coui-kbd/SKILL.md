---
name: coui-kbd
description: Activate when creating keyboard key displays, shortcut key indicators, or key combination badges using CouiKbd/KbdSize (Flutter) or Kbd (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Kbd

## Overview

The Kbd component visually represents keyboard keys. It is designed for displaying keyboard shortcuts in help pages, command palettes, and shortcut guides. Multiple keys are rendered with a `+` separator.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
// Single key
CouiKbd(keys: ['Ctrl'])

// Key combination
CouiKbd(keys: ['Ctrl', 'C'])

// Complex shortcut
CouiKbd(keys: ['Ctrl', 'Shift', 'P'])
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `keys` | `List<String>` | required | List of key names to display |
| `size` | `KbdSize` | `KbdSize.md` | Component dimensions |

### Size Options

| Size | Description |
|------|-------------|
| `KbdSize.sm` | Compact size for secondary text |
| `KbdSize.md` | Standard size (default) |
| `KbdSize.lg` | Large size for emphasis |

### Mac-Style Keys

```dart
CouiKbd(keys: ['⌘', 'K'])
```

### Inline with Text

```dart
Text.rich(
  TextSpan(
    children: [
      TextSpan(text: '저장하려면 '),
      WidgetSpan(child: CouiKbd(keys: ['Ctrl', 'S'])),
      TextSpan(text: '를 누르세요.'),
    ],
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Kbd(keys: ['Ctrl'])
Kbd(keys: ['Ctrl', 'C'])
Kbd(keys: ['Ctrl', 'Shift', 'P'])
Kbd(keys: ['⌘', 'K'])
```

## Common Patterns

### Common Shortcut Keys

| Shortcut | Keys |
|----------|------|
| Copy | `['Ctrl', 'C']` |
| Paste | `['Ctrl', 'V']` |
| Select All | `['Ctrl', 'A']` |
| Save | `['Ctrl', 'S']` |
| Undo | `['Ctrl', 'Z']` |
| Command Palette (macOS) | `['⌘', 'K']` |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiKbd` | `Kbd` |
| Size support | `KbdSize` enum | `KbdSize` enum |
| Inline usage | `WidgetSpan` wrapping | Inline component |

### When to Use

- Keyboard shortcut help pages
- Command palette shortcut labels
- Settings and preferences displays
- Tutorial and documentation content

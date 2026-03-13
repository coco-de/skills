---
name: coui-command
description: Activate when creating command palettes, keyboard-centric navigation, search commands, or action menus using Command, Command, CommandInput, CommandList, CommandGroup, CommandItem in CoUI Flutter or CoUI Web.
---

# CoUI Command

## Overview

The Command component is a keyboard-centric command palette for fast navigation, search, and action execution. It comprises `CommandInput`, `CommandList`, `CommandGroup`, and `CommandItem` subcomponents. Flutter uses `Command` while Web uses `Command`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Command Palette

```dart
Command(
  placeholder: '명령어를 입력하세요...',
  emptyMessage: '결과가 없습니다.',
  commands: [
    CommandGroup(
      label: '페이지',
      items: [
        CommandItem(
          value: 'home',
          label: '홈으로 이동',
          icon: Icon(Icons.home),
          onSelect: handleNavigateHome,
        ),
        CommandItem(
          value: 'settings',
          label: '설정',
          icon: Icon(Icons.settings),
          onSelect: handleNavigateSettings,
        ),
      ],
    ),
    CommandGroup(
      label: '액션',
      items: [
        CommandItem(
          value: 'new',
          label: '새 항목 만들기',
          icon: Icon(Icons.add),
          shortcut: 'Ctrl+N',
          onSelect: handleCreateNew,
        ),
      ],
    ),
  ],
)
```

### Command Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `commands` | `List<CommandGroup>` | required | List of command groups to display |
| `onSelect` | `void Function(String)?` | `null` | Item selection handler |
| `placeholder` | `String` | `'검색...'` | Input field placeholder text |
| `emptyMessage` | `String` | `'결과 없음'` | Message when no search results |
| `filter` | `bool Function(String, String)?` | `null` | Custom filter function |

### CommandGroup Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Group heading text |
| `items` | `List<CommandItem>` | required | List of items in group |

### CommandItem Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Unique item identifier |
| `label` | `String` | required | Display text |
| `icon` | `Widget?` | `null` | Item icon |
| `shortcut` | `String?` | `null` | Keyboard shortcut display |
| `onSelect` | `VoidCallback?` | `null` | Selection callback |
| `disabled` | `bool` | `false` | Disabled state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Command

```dart
Command(
  placeholder: '명령어를 입력하세요...',
  emptyMessage: '결과가 없습니다.',
  commands: [
    CommandGroup(
      label: '페이지',
      items: [
        CommandItem(
          value: 'home',
          label: '홈으로 이동',
          icon: Icon(Icons.home),
          onSelect: handleNavigateHome,
        ),
        CommandItem(
          value: 'settings',
          label: '설정',
          icon: Icon(Icons.settings),
          onSelect: handleNavigateSettings,
        ),
      ],
    ),
  ],
)
```

## Common Patterns

### Subcomponents

- **CommandInput**: Search input field (auto-included in Command/Command)
- **CommandList**: Filtered results display area
- **CommandGroup**: Groups related items with headings
- **CommandItem**: Individual selectable command item

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `Command` | `Command` |
| API structure | Identical | Identical |

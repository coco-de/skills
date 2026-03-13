---
name: coui-dropdown-menu
description: Activate when creating dropdown action menus, trigger-based option lists, or button-triggered menu popups using CouiDropdownMenu, DropdownMenu, DropdownMenuItem, or DropdownPlacement in CoUI Flutter or CoUI Web.
---

# CoUI DropdownMenu

## Overview

The DropdownMenu component displays an options list when a trigger element is clicked. It supports various placement positions, offset configurations, icons, dividers, and destructive action styling.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic DropdownMenu

```dart
CouiDropdownMenu(
  trigger: CouiButton(
    onPressed: null,
    child: Row(
      children: [Text('Options'), Icon(Icons.arrow_drop_down)],
    ),
  ),
  onSelect: (value) {
    // Handle selected option
  },
  items: [
    DropdownMenuItem(value: 'option1', label: 'Option 1'),
    DropdownMenuItem(value: 'option2', label: 'Option 2'),
    DropdownMenuDivider(),
    DropdownMenuItem(value: 'option3', label: 'Option 3'),
  ],
)
```

### With Icons and Destructive Action

```dart
CouiDropdownMenu(
  trigger: IconButton(
    onPressed: null,
    icon: Icon(Icons.more_vert),
  ),
  onSelect: handleDropdownSelect,
  placement: DropdownPlacement.bottomEnd,
  offset: 8.0,
  items: [
    DropdownMenuItem(value: 'edit', label: 'Edit', icon: Icon(Icons.edit)),
    DropdownMenuItem(value: 'share', label: 'Share', icon: Icon(Icons.share)),
    DropdownMenuDivider(),
    DropdownMenuItem(
      value: 'delete',
      label: 'Delete',
      icon: Icon(Icons.delete),
      isDestructive: true,
    ),
  ],
)
```

### Key Classes

#### CouiDropdownMenu

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger` | `Widget` | required | Widget that opens the menu |
| `items` | `List<DropdownMenuEntry>` | required | Menu items list |
| `onSelect` | `void Function(String)?` | `null` | Item selection handler |
| `placement` | `DropdownPlacement` | `bottomStart` | Menu position |
| `offset` | `double` | `4.0` | Space between trigger and menu (px) |

#### DropdownMenuItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Value passed to onSelect |
| `label` | `String` | required | Item text |
| `icon` | `Widget?` | `null` | Item icon |
| `isDestructive` | `bool` | `false` | Destructive action styling |
| `isDisabled` | `bool` | `false` | Disabled state |

#### DropdownMenuDivider

Separator between menu items. No additional properties.

### DropdownPlacement

| Value | Description |
|-------|-------------|
| `bottomStart` | Bottom-left alignment (default) |
| `bottomEnd` | Bottom-right alignment |
| `topStart` | Top-left alignment |
| `topEnd` | Top-right alignment |

### User Actions Pattern

```dart
CouiDropdownMenu(
  trigger: CouiButton(
    onPressed: null,
    child: Text('More'),
  ),
  onSelect: (value) {
    switch (value) {
      case 'edit': editItem();
      case 'duplicate': duplicateItem();
      case 'archive': archiveItem();
      case 'delete': deleteItem();
    }
  },
  placement: DropdownPlacement.bottomEnd,
  items: [
    DropdownMenuItem(value: 'edit', label: 'Edit', icon: Icon(Icons.edit)),
    DropdownMenuItem(value: 'duplicate', label: 'Duplicate', icon: Icon(Icons.copy)),
    DropdownMenuItem(value: 'archive', label: 'Archive', icon: Icon(Icons.archive)),
    DropdownMenuDivider(),
    DropdownMenuItem(
      value: 'delete',
      label: 'Delete',
      icon: Icon(Icons.delete),
      isDestructive: true,
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic DropdownMenu

```dart
DropdownMenu(
  trigger: Button(
    onClick: null,
    child: Row(
      children: [Component.text('Options'), Icon(CouiIcons.chevronDown)],
    ),
  ),
  onSelect: handleDropdownSelect,
  items: [
    DropdownMenuItem(value: 'option1', label: 'Option 1'),
    DropdownMenuItem(value: 'option2', label: 'Option 2'),
    DropdownMenuDivider(),
    DropdownMenuItem(value: 'option3', label: 'Option 3'),
  ],
)
```

## Common Patterns

### DropdownMenu vs ContextMenu

| Feature | DropdownMenu | ContextMenu |
|---------|--------------|-------------|
| Trigger | Click on trigger widget | Right-click / long-press |
| Position | Relative to trigger | At cursor/press position |
| Use case | Action buttons, "more" menus | Right-click context actions |

### API Consistency

- Both Flutter and Web share the same structure: `trigger`, `items`, `onSelect`, and `placement`.
- Both support `DropdownMenuItem`, `DropdownMenuDivider`, icons, destructive, and disabled states.

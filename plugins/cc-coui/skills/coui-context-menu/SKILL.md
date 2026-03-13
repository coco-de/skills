---
name: coui-context-menu
description: Activate when creating right-click menus, long-press context actions, or contextual action lists using CouiContextMenu, ContextMenu, ContextMenuItem, or ContextMenuDivider in CoUI Flutter or CoUI Web.
---

# CoUI ContextMenu

## Overview

The ContextMenu component displays a context menu triggered by right-click (desktop) or long-press (mobile). It provides a selectable list of actions with support for icons, dividers, disabled states, and destructive action styling.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic ContextMenu

```dart
CouiContextMenu(
  onSelect: (value) {
    // Handle selected action
  },
  items: [
    ContextMenuItem(value: 'copy', label: 'Copy', icon: Icon(Icons.copy)),
    ContextMenuItem(value: 'cut', label: 'Cut', icon: Icon(Icons.cut)),
    ContextMenuDivider(),
    ContextMenuItem(value: 'paste', label: 'Paste', icon: Icon(Icons.paste)),
    ContextMenuDivider(),
    ContextMenuItem(
      value: 'delete',
      label: 'Delete',
      icon: Icon(Icons.delete),
      isDestructive: true,
    ),
  ],
  child: Container(
    padding: EdgeInsets.all(32),
    color: Colors.grey[100],
    child: Text('Right-click or long-press here'),
  ),
)
```

### Key Classes

#### CouiContextMenu

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Widget` | required | Target widget for context menu |
| `items` | `List<ContextMenuEntry>` | required | Menu item list |
| `onSelect` | `void Function(String)?` | `null` | Item selection handler |

#### ContextMenuItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Value passed to onSelect |
| `label` | `String` | required | Menu item text |
| `icon` | `Widget?` | `null` | Item icon |
| `isDestructive` | `bool` | `false` | Destructive action styling (red) |
| `isDisabled` | `bool` | `false` | Disabled state |

#### ContextMenuDivider

Separator between menu items. No additional properties.

### File Manager Pattern

```dart
CouiContextMenu(
  onSelect: (value) {
    switch (value) {
      case 'open': openFile(file);
      case 'rename': renameFile(file);
      case 'delete': deleteFile(file);
    }
  },
  items: [
    ContextMenuItem(value: 'open', label: 'Open', icon: Icon(Icons.open_in_new)),
    ContextMenuItem(value: 'rename', label: 'Rename', icon: Icon(Icons.edit)),
    ContextMenuDivider(),
    ContextMenuItem(
      value: 'delete',
      label: 'Delete',
      icon: Icon(Icons.delete),
      isDestructive: true,
    ),
  ],
  child: FileListItem(file: file),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic ContextMenu

```dart
ContextMenu(
  onSelect: handleContextMenuSelect,
  items: [
    ContextMenuItem(value: 'copy', label: 'Copy', icon: Icon(CouiIcons.copy)),
    ContextMenuItem(value: 'cut', label: 'Cut', icon: Icon(CouiIcons.cut)),
    ContextMenuDivider(),
    ContextMenuItem(value: 'paste', label: 'Paste', icon: Icon(CouiIcons.paste)),
    ContextMenuDivider(),
    ContextMenuItem(
      value: 'delete',
      label: 'Delete',
      isDestructive: true,
    ),
  ],
  child: Container(
    child: Component.text('Right-click here'),
  ),
)
```

## Common Patterns

### API Consistency

- Both Flutter and Web use the same structure: `child`, `items`, and `onSelect`.
- Both support `ContextMenuItem` with `value`, `label`, `icon`, `isDestructive`, and `isDisabled`.
- Both use `ContextMenuDivider` for visual separation between item groups.

### Key Notes

- On desktop, triggered by right-click. On mobile, triggered by long-press.
- Destructive items (`isDestructive: true`) are rendered in red to warn users.
- Disabled items are visually dimmed and non-interactive.

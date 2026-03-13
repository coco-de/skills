---
name: coui-menubar
description: Activate when creating desktop-style horizontal menu bars, application menu systems, or top-level menu navigation with nested dropdowns using CouiMenubar, Menubar, MenubarItem, MenubarMenu, or MenubarSeparator in CoUI Flutter or CoUI Web.
---

# CoUI Menubar

## Overview

The Menubar is a desktop application-style horizontal menu bar positioned at the top of the interface. It supports nested dropdown menus, keyboard shortcuts display, and keyboard navigation for building app-level menu systems.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Menubar

```dart
CouiMenubar(
  onSelect: (value) {
    switch (value) {
      case 'new': createNewFile();
      case 'open': openFile();
      case 'save': saveFile();
      case 'undo': undo();
      case 'redo': redo();
    }
  },
  items: [
    MenubarItem(
      label: 'File',
      menu: [
        MenubarMenu(value: 'new', label: 'New File'),
        MenubarMenu(value: 'open', label: 'Open'),
        MenubarSeparator(),
        MenubarMenu(value: 'save', label: 'Save'),
      ],
    ),
    MenubarItem(
      label: 'Edit',
      menu: [
        MenubarMenu(value: 'undo', label: 'Undo'),
        MenubarMenu(value: 'redo', label: 'Redo'),
      ],
    ),
  ],
)
```

### With Keyboard Shortcuts

```dart
CouiMenubar(
  onSelect: handleMenubarSelect,
  items: [
    MenubarItem(
      label: 'File',
      menu: [
        MenubarMenu(value: 'new', label: 'New File', shortcut: 'Cmd+N'),
        MenubarMenu(value: 'open', label: 'Open', shortcut: 'Cmd+O'),
        MenubarMenu(value: 'save', label: 'Save', shortcut: 'Cmd+S'),
      ],
    ),
    MenubarItem(
      label: 'Edit',
      menu: [
        MenubarMenu(value: 'undo', label: 'Undo', shortcut: 'Cmd+Z'),
        MenubarMenu(value: 'redo', label: 'Redo', shortcut: 'Cmd+Shift+Z'),
        MenubarSeparator(),
        MenubarMenu(value: 'cut', label: 'Cut', shortcut: 'Cmd+X'),
        MenubarMenu(value: 'copy', label: 'Copy', shortcut: 'Cmd+C'),
        MenubarMenu(value: 'paste', label: 'Paste', shortcut: 'Cmd+V'),
      ],
    ),
    MenubarItem(
      label: 'View',
      menu: [
        MenubarMenu(value: 'zoomIn', label: 'Zoom In', shortcut: 'Cmd++'),
        MenubarMenu(value: 'zoomOut', label: 'Zoom Out', shortcut: 'Cmd+-'),
        MenubarSeparator(),
        MenubarMenu(value: 'fullscreen', label: 'Full Screen', shortcut: 'Ctrl+Cmd+F'),
      ],
    ),
  ],
)
```

### Key Classes

#### CouiMenubar

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<MenubarItem>` | required | Top-level menu items |
| `onSelect` | `void Function(String)?` | `null` | Menu selection handler |

#### MenubarItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Display label on menu bar |
| `menu` | `List<MenubarEntry>` | required | Dropdown items on click |

#### MenubarMenu

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Value passed to onSelect |
| `label` | `String` | required | Menu item text |
| `shortcut` | `String?` | `null` | Keyboard shortcut display |
| `isDisabled` | `bool` | `false` | Disabled state |

#### MenubarSeparator

Divider between menu items. No additional properties.

### IDE Menubar Pattern

```dart
Column(
  children: [
    CouiMenubar(
      onSelect: handleMenuAction,
      items: [
        MenubarItem(label: 'File', menu: [
          MenubarMenu(value: 'newFile', label: 'New File', shortcut: 'Cmd+N'),
          MenubarMenu(value: 'newWindow', label: 'New Window', shortcut: 'Cmd+Shift+N'),
          MenubarSeparator(),
          MenubarMenu(value: 'save', label: 'Save', shortcut: 'Cmd+S'),
          MenubarMenu(value: 'saveAs', label: 'Save As...', shortcut: 'Cmd+Shift+S'),
          MenubarSeparator(),
          MenubarMenu(value: 'exit', label: 'Exit'),
        ]),
        MenubarItem(label: 'Edit', menu: [
          MenubarMenu(value: 'undo', label: 'Undo', shortcut: 'Cmd+Z'),
          MenubarMenu(value: 'redo', label: 'Redo', shortcut: 'Cmd+Shift+Z'),
        ]),
        MenubarItem(label: 'Help', menu: [
          MenubarMenu(value: 'docs', label: 'Documentation'),
          MenubarMenu(value: 'about', label: 'About'),
        ]),
      ],
    ),
    Expanded(child: editorContent),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Menubar

```dart
CouiMenubar(
  onSelect: handleMenubarSelect,
  items: [
    MenubarItem(
      label: 'File',
      menu: [
        MenubarMenu(value: 'new', label: 'New File'),
        MenubarMenu(value: 'open', label: 'Open'),
        MenubarSeparator(),
        MenubarMenu(value: 'save', label: 'Save'),
        MenubarMenu(value: 'saveAs', label: 'Save As'),
        MenubarSeparator(),
        MenubarMenu(value: 'exit', label: 'Exit'),
      ],
    ),
  ],
)
```

## Common Patterns

### API Consistency

- Both Flutter and Web use the same API structure: `items`, `onSelect`, `MenubarItem`, `MenubarMenu`, and `MenubarSeparator`.
- Keyboard shortcuts are display-only via `shortcut` string (e.g., `'Cmd+S'`). Actual key binding must be implemented separately.

### Menubar vs DropdownMenu

| Feature | Menubar | DropdownMenu |
|---------|---------|--------------|
| Layout | Horizontal bar with multiple top-level items | Single trigger button |
| Use case | App-level menu system (File, Edit, View) | Single action menu |
| Selection handler | Single `onSelect` for all items via `value` | Single `onSelect` per menu |

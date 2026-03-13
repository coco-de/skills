---
name: coui-switcher
description: Activate when creating view switchers, segmented controls, tab-style toggles, or filter selectors using CouiSwitcher, SwitcherVariant, or segmented buttons in CoUI Flutter or CoUI Web.
---

# CoUI Switcher

## Overview

The Switcher component enables users to transition between multiple views or content sections. It supports three style variants: Tabs (underline indicator), Buttons (segmented controls), and Pills (pill-shaped selection).

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Tabs Variant (Default)

```dart
CouiSwitcher(
  items: ['All', 'In Progress', 'Completed'],
  selectedIndex: _selectedIndex,
  onChanged: (index) {
    setState(() => _selectedIndex = index);
  },
)
```

### Buttons Variant

```dart
CouiSwitcher(
  items: ['List', 'Grid', 'Card'],
  selectedIndex: _selectedIndex,
  onChanged: (index) {
    setState(() => _selectedIndex = index);
  },
  variant: SwitcherVariant.buttons,
)
```

### Pills Variant

```dart
CouiSwitcher(
  items: ['Day', 'Week', 'Month', 'Year'],
  selectedIndex: _selectedIndex,
  onChanged: (index) {
    setState(() => _selectedIndex = index);
  },
  variant: SwitcherVariant.pills,
)
```

### Key Classes

#### CouiSwitcher

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<String>` | required | List of item labels |
| `selectedIndex` | `int` | required | Currently selected index |
| `onChanged` | `void Function(int)` | required | Selection change callback |
| `variant` | `SwitcherVariant` | `SwitcherVariant.tabs` | Style variant |

### View Mode Switcher Pattern

```dart
Column(
  children: [
    CouiSwitcher(
      items: ['List', 'Grid'],
      selectedIndex: _viewMode,
      onChanged: (index) => setState(() => _viewMode = index),
      variant: SwitcherVariant.buttons,
    ),
    Expanded(
      child: _viewMode == 0 ? const ListView() : const GridView(),
    ),
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
Switcher(
  items: ['All', 'In Progress', 'Completed'],
  selectedIndex: _selectedIndex,
  onChanged: (index) => setState(() => _selectedIndex = index),
)
```

### Buttons Variant

```dart
Switcher(
  items: ['List', 'Grid'],
  selectedIndex: _selectedIndex,
  onChanged: (index) => setState(() => _selectedIndex = index),
  variant: SwitcherVariant.buttons,
)
```

### Pills Variant

```dart
Switcher(
  items: ['Day', 'Week', 'Month'],
  selectedIndex: _selectedIndex,
  onChanged: (index) => setState(() => _selectedIndex = index),
  variant: SwitcherVariant.pills,
)
```

## Common Patterns

### Variant Guide

| Variant | Use Case | Visual Style |
|---------|----------|--------------|
| `tabs` | Content area top tabs | Bottom underline indicator |
| `buttons` | View mode switching | Segmented button group |
| `pills` | Filters, period selection | Pill-shaped selection highlight |

### API Consistency

- Both Flutter and Web use the same parameters: `items`, `selectedIndex`, `onChanged`, and `variant`.
- Both support `SwitcherVariant.tabs`, `SwitcherVariant.buttons`, and `SwitcherVariant.pills`.

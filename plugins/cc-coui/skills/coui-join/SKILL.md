---
name: coui-join
description: Activate when creating joined button groups, input-button combinations, or visually connected element groups using CouiJoin, Join, or shared-border layouts in CoUI Flutter or CoUI Web.
---

# CoUI Join

## Overview

The Join component combines multiple elements into a visual unit, sharing borders without separators. It is designed for grouping related controls like button groups, toolbar actions, and input-button combinations.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Horizontal Button Group

```dart
CouiJoin(
  direction: Axis.horizontal,
  children: [
    CouiButton(onPressed: () {}, child: const Icon(Icons.format_bold)),
    CouiButton(onPressed: () {}, child: const Icon(Icons.format_italic)),
    CouiButton(onPressed: () {}, child: const Icon(Icons.format_underline)),
  ],
)
```

### Input with Button

```dart
CouiJoin(
  children: [
    Expanded(
      child: CouiInput(
        placeholder: 'Search term',
        onChanged: (value) {},
      ),
    ),
    CouiButton(
      onPressed: () {},
      child: const Icon(Icons.search),
    ),
  ],
)
```

### Vertical Group

```dart
CouiJoin(
  direction: Axis.vertical,
  children: [
    CouiButton(onPressed: () {}, child: const Text('Top')),
    CouiButton(onPressed: () {}, child: const Text('Bottom')),
  ],
)
```

### Key Classes

#### CouiJoin

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `children` | `List<Widget>` | required | Widgets to combine |
| `direction` | `Axis` | `Axis.horizontal` | Combination direction |
| `separator` | `Widget?` | `null` | Optional widget between items |

### Toolbar Pattern

```dart
CouiJoin(
  children: [
    CouiButton(onPressed: () {}, child: const Icon(Icons.undo)),
    CouiButton(onPressed: () {}, child: const Icon(Icons.redo)),
    CouiButton(onPressed: () {}, child: const Icon(Icons.format_bold)),
    CouiButton(onPressed: () {}, child: const Icon(Icons.format_italic)),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Horizontal Button Group

```dart
Join(
  direction: 'horizontal',
  children: [
    Button(onPressed: () {}, child: Icon('bold')),
    Button(onPressed: () {}, child: Icon('italic')),
  ],
)
```

### Input with Button

```dart
Join(
  children: [
    Input(placeholder: 'Search', onChanged: handleSearchChanged),
    Button(onPressed: handleSearchPressed, child: Icon('search')),
  ],
)
```

## Common Patterns

### Use Cases

| Pattern | Description |
|---------|-------------|
| Button group | Toolbar or formatting actions |
| Search bar | Input field joined with search button |
| Pagination | Joined page number buttons |
| Segmented control | Mutually exclusive options |

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Direction type | `Axis.horizontal` enum | `'horizontal'` string |

### Shared Concepts

- Both platforms share `children`, `direction`, and `separator` parameters.
- Border radius is applied only to the first and last child, creating a unified visual group.

---
name: coui-chip
description: Activate when creating chips, tags, filter options, selectable labels, or removable tag elements using CouiChip/ChipVariant (Flutter) or Chip (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Chip

## Overview

The Chip component displays tags, filters, and selection states. It supports deletion buttons, avatars, and selection functionality with two variants: filled and outlined.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiChip(label: 'Flutter')
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Display text |
| `onDelete` | `VoidCallback?` | `null` | Removal button handler |
| `avatar` | `Widget?` | `null` | Left-side avatar widget |
| `variant` | `ChipVariant` | `filled` | Style variation (filled, outlined) |
| `selected` | `bool` | `false` | Selection state |
| `onSelected` | `void Function(bool)?` | `null` | Selection change handler |
| `disabled` | `bool` | `false` | Enable/disable state |

### Removable Chip

```dart
CouiChip(
  label: 'Dart',
  onDelete: handleDeleteDart,
)
```

### With Avatar

```dart
CouiChip(
  label: '홍길동',
  avatar: CircleAvatar(
    backgroundImage: NetworkImage('https://example.com/avatar.jpg'),
  ),
  onDelete: handleDeleteUser,
)
```

### Selectable Chip

```dart
CouiChip(
  label: '디자인',
  variant: ChipVariant.outlined,
  selected: isDesignSelected,
  onSelected: handleSelectDesign,
)
```

### Chip Group Pattern

```dart
Wrap(
  spacing: 8,
  children: [
    CouiChip(label: 'Flutter', onDelete: () => handleDelete('flutter')),
    CouiChip(label: 'Dart', onDelete: () => handleDelete('dart')),
    CouiChip(label: 'UI', onDelete: () => handleDelete('ui')),
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
Chip(label: 'Flutter')
```

### With Avatar and Delete

```dart
Chip(
  label: '홍길동',
  avatar: Avatar(src: 'https://example.com/avatar.jpg'),
  onDelete: handleDeleteUser,
)
```

### Selectable Chip

```dart
Chip(
  label: '디자인',
  variant: ChipVariant.outlined,
  selected: isDesignSelected,
  onSelected: handleSelectDesign,
)
```

## Common Patterns

### Variants

| Variant | Description | Use Case |
|---------|-------------|----------|
| `ChipVariant.filled` | Solid background (default) | Standard tag display |
| `ChipVariant.outlined` | Border-only | Filter selection interfaces |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiChip` | `Chip` |
| Avatar type | `Widget` | `Avatar` component |
| Layout spacing | `Wrap(spacing:)` | CSS `flex gap` classes |

### When to Use

- Tag lists and category labels
- Filter selection bars
- User/contact selection chips
- Removable search criteria

---
name: coui-skeleton
description: Activate when creating loading placeholders, skeleton screens, content shimmer effects, or placeholder layouts using Skeleton/SkeletonVariant (Flutter) or Skeleton (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Skeleton

## Overview

The Skeleton component displays placeholder content during data loading. It shows the layout of content in advance to visually communicate loading state to users. It supports rectangular, circular, and text variants.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Rectangular Skeleton

```dart
Skeleton(width: 200, height: 20)
```

### Constructors

- `Skeleton()` - Default rectangular shape
- `Skeleton.circle()` - Circular elements (avatars)
- `Skeleton.text()` - Multi-line text placeholders

### Default Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `width` | `double?` | `null` | Horizontal dimension |
| `height` | `double?` | `null` | Vertical dimension |
| `borderRadius` | `double` | `4.0` | Corner rounding |
| `variant` | `SkeletonVariant` | `rectangular` | Shape type |

### Circle Constructor

```dart
Skeleton.circle(size: 48)
```

| Parameter | Type | Description |
|-----------|------|-------------|
| `size` | `double` | Diameter (required) |

### Text Constructor

```dart
Skeleton.text(lines: 3)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `lines` | `int` | `3` | Number of text rows |
| `lineSpacing` | `double` | `8.0` | Gap between rows |
| `lastLineWidth` | `double?` | `null` | Final row width ratio (0.0-1.0) |

### Card Skeleton Layout

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Skeleton(width: double.infinity, height: 200, borderRadius: 12),
    SizedBox(height: 12),
    Skeleton.text(lines: 2),
    SizedBox(height: 8),
    Skeleton(width: 100, height: 16),
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
Skeleton(width: 200, height: 20)
Skeleton.circle(size: 48)
Skeleton.text(lines: 3)
```

### Card Skeleton

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    Skeleton(width: double.infinity, height: 200, borderRadius: 12),
    SizedBox(height: 12),
    Skeleton.text(lines: 2),
  ],
)
```

## Common Patterns

### Variants

| Variant | Constructor | Use Case |
|---------|-------------|----------|
| Rectangular | `Skeleton()` / `Skeleton()` | Images, cards, buttons |
| Circular | `.circle(size:)` | Avatars, icons |
| Text | `.text(lines:)` | Paragraphs, descriptions |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `Skeleton` | `Skeleton` |
| API | Identical constructors | Identical constructors |

### When to Use

- Initial page load placeholders
- List item loading states
- Card content shimmer effects
- Profile page loading skeletons

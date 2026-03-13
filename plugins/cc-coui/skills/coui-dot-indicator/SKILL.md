---
name: coui-dot-indicator
description: Activate when creating dot indicators, page indicators, carousel position dots, or pagination dots using CouiDotIndicator (Flutter) or DotIndicator (Web) in CoUI Flutter or CoUI Web.
---

# CoUI DotIndicator

## Overview

The DotIndicator uses dots to indicate the current position within a carousel, onboarding flow, or paginated content. It visually distinguishes active and inactive states through color and size variations.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiDotIndicator(count: 5, activeIndex: currentPage)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `count` | `int` | required | Total number of dots/pages |
| `activeIndex` | `int` | required | Currently active dot index (0-based) |
| `activeColor` | `Color?` | theme primary | Active dot color |
| `inactiveColor` | `Color?` | theme outline | Inactive dot color |
| `size` | `double` | `8.0` | Inactive dot diameter (pixels) |
| `activeSize` | `double?` | matches `size` | Active dot diameter |
| `spacing` | `double` | `6.0` | Gap between dots (pixels) |
| `onDotTap` | `void Function(int)?` | `null` | Callback when dot is tapped |

### Custom Colors

```dart
CouiDotIndicator(
  count: 3,
  activeIndex: currentPage,
  activeColor: Colors.blue,
  inactiveColor: Colors.grey.shade300,
)
```

### PageView Integration

```dart
PageView(
  onPageChanged: (index) => setState(() => currentPage = index),
  children: pages,
),
CouiDotIndicator(count: pages.length, activeIndex: currentPage)
```

### Size-Emphasized Variant

```dart
CouiDotIndicator(
  count: 4,
  activeIndex: 0,
  size: 8,
  activeSize: 12,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
DotIndicator(count: 5, activeIndex: currentPage)
```

### Custom Colors

```dart
DotIndicator(
  count: 3,
  activeIndex: currentPage,
  activeColor: Colors.blue,
  inactiveColor: Colors.grey.shade300,
)
```

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiDotIndicator` | `DotIndicator` |
| API | Identical parameters | Identical parameters |

### When to Use

- PageView/Carousel position indicators
- Onboarding step indicators
- Image gallery navigation
- Interactive page jumping via `onDotTap`

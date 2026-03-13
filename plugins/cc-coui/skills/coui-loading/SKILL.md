---
name: coui-loading
description: Activate when creating loading indicators, spinners, dot loaders, progress bars, or pulse animations using Loading/LoadingVariant/LoadingSize (Flutter) or Loading (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Loading

## Overview

The Loading component displays a loading indicator for ongoing operations. It supports four visual styles: spinner, dots, bar, and pulse, with configurable sizes and optional labels.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
Loading()
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `size` | `LoadingSize` | `medium` | Indicator dimensions |
| `variant` | `LoadingVariant` | `spinner` | Animation style |
| `color` | `Color?` | `null` | Custom color (defaults to theme primary) |
| `label` | `String?` | `null` | Optional text below indicator |

### With Variant

```dart
Loading(variant: LoadingVariant.dots)
```

### Customized

```dart
Loading(
  variant: LoadingVariant.spinner,
  size: LoadingSize.large,
  color: Colors.blue,
)
```

### With Label

```dart
Loading(
  variant: LoadingVariant.spinner,
  label: '데이터를 불러오는 중...',
)
```

### Bar Variant

```dart
Loading(
  variant: LoadingVariant.bar,
  size: LoadingSize.small,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Loading()

Loading(variant: LoadingVariant.dots)

Loading(
  variant: LoadingVariant.spinner,
  size: LoadingSize.large,
  color: Colors.blue,
)

Loading(
  variant: LoadingVariant.spinner,
  label: '데이터를 불러오는 중...',
)
```

## Common Patterns

### Variants

| Variant | Description |
|---------|-------------|
| `LoadingVariant.spinner` | Rotating circular spinner (default) |
| `LoadingVariant.dots` | Three dots highlighting sequentially |
| `LoadingVariant.bar` | Horizontal bar moving side-to-side |
| `LoadingVariant.pulse` | Element expanding/contracting rhythmically |

### Sizes

| Size | Dimension |
|------|-----------|
| `LoadingSize.small` | 16px |
| `LoadingSize.medium` | 24px (default) |
| `LoadingSize.large` | 40px |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `Loading` | `Loading` |
| API | Identical parameters | Identical parameters |

### When to Use

- Data fetching states
- Button loading states
- Page transition loading
- Overlay loading screens
- Async operation feedback

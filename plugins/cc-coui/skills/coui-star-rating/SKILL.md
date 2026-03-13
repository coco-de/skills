---
name: coui-star-rating
description: Activate when creating star ratings, review ratings, half-star ratings, or read-only rating displays using CouiStarRating, StarRating in CoUI Flutter or CoUI Web.
---

# CoUI StarRating

## Overview

The StarRating component enables users to input or display ratings using star icons. It supports interactive rating input, read-only display mode, half-star increments, and customizable star count and color. Flutter uses `CouiStarRating` while Web uses `StarRating`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Rating Input

```dart
CouiStarRating(
  value: userRating,
  onChanged: handleRatingChanged,
)
```

### Read-Only Display

```dart
CouiStarRating(
  value: productRating,
  readOnly: true,
  size: 20,
)
```

### Half-Star Support

```dart
CouiStarRating(
  value: reviewRating,
  onChanged: handleReviewRatingChanged,
  allowHalf: true,
  maxRating: 5,
  color: Colors.amber,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `double` | required | Current rating value |
| `onChanged` | `ValueChanged<double>?` | `null` | Rating change callback |
| `maxRating` | `int` | `5` | Maximum number of stars |
| `size` | `double` | `24.0` | Star icon size |
| `allowHalf` | `bool` | `false` | Enable half-star increments |
| `readOnly` | `bool` | `false` | Disable user interaction |
| `color` | `Color?` | `null` | Star color customization |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Rating

```dart
StarRating(
  value: userRating,
  onChanged: handleRatingChanged,
)
```

### Read-Only

```dart
StarRating(
  value: productRating,
  readOnly: true,
  size: 20,
)
```

### Half-Star

```dart
StarRating(
  value: reviewRating,
  onChanged: handleReviewRatingChanged,
  allowHalf: true,
  maxRating: 5,
)
```

## Common Patterns

### Variants

- **Standard Input**: Full-star rating selection
- **Half-Star Mode**: 0.5-increment ratings with `allowHalf: true`
- **Read-Only Display**: Static ratings with `readOnly: true`

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `CouiStarRating` | `StarRating` |
| API structure | Identical | Identical |

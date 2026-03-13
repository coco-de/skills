---
name: coui-number-ticker
description: Activate when creating animated number displays, rolling counters, statistic animations, or numeric value transitions using CouiNumberTicker (Flutter) or NumberTicker (Web) in CoUI Flutter or CoUI Web.
---

# CoUI NumberTicker

## Overview

NumberTicker animates numeric values with a smooth rolling effect. It is designed for statistics, counters, and dashboard metrics where animated number transitions enhance visual appeal.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiNumberTicker(value: 1234)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `num` | required | Numeric value to display |
| `duration` | `Duration` | `Duration(milliseconds: 600)` | Animation duration |
| `style` | `TextStyle?` | `null` | Text styling options |
| `prefix` | `String?` | `null` | Text before number |
| `suffix` | `String?` | `null` | Text after number |
| `decimalPlaces` | `int` | `0` | Decimal precision |
| `separator` | `String?` | `null` | Thousand separator (e.g., ',') |
| `curve` | `Curve` | `Curves.easeOut` | Animation easing |

### Styled with Duration

```dart
CouiNumberTicker(
  value: 99999,
  duration: Duration(milliseconds: 800),
  style: TextStyle(fontSize: 48, fontWeight: FontWeight.bold),
)
```

### Currency Display

```dart
CouiNumberTicker(
  value: 12450000,
  prefix: '₩',
  suffix: '원',
  separator: ',',
)
```

### Decimal Values

```dart
CouiNumberTicker(
  value: 3.14159,
  decimalPlaces: 2,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
NumberTicker(value: 1234)
```

### With Formatting

```dart
NumberTicker(
  value: 12450000,
  prefix: '₩',
  separator: ',',
  duration: Duration(milliseconds: 800),
)
```

### Parameters

Same parameter structure as Flutter with identical property names.

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiNumberTicker` | `NumberTicker` |
| API | Identical parameters | Identical parameters |

### When to Use

- Dashboard statistics cards
- Price tags with currency formatting
- Performance metrics displays
- Ratings and percentage indicators
- Counters that animate on value change

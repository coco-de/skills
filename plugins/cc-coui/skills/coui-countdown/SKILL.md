---
name: coui-countdown
description: Activate when creating countdown timers, time-remaining displays, event countdowns, or session timeout indicators using CouiCountdown/CountdownFormat (Flutter) or Countdown (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Countdown

## Overview

The Countdown component displays remaining time until a target date in days, hours, minutes, and seconds. It is designed for countdowns to events, sales, or time-sensitive operations.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiCountdown(
  targetDate: DateTime(2026, 12, 31, 23, 59, 59),
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `targetDate` | `DateTime` | required | Goal date/time for countdown |
| `onComplete` | `VoidCallback?` | `null` | Callback when countdown ends |
| `format` | `CountdownFormat` | `dhms` | Display format |
| `separator` | `String` | `':'` | Character separating time units |
| `style` | `TextStyle?` | `null` | Custom styling for timer text |

### With Completion Callback

```dart
CouiCountdown(
  targetDate: saleEndDate,
  onComplete: handleSaleEnd,
)
```

### Seconds-Only Display

```dart
CouiCountdown(
  targetDate: DateTime.now().add(Duration(seconds: 30)),
  format: CountdownFormat.secondsOnly,
  onComplete: handleTimeOut,
)
```

### Styled Timer

```dart
CouiCountdown(
  targetDate: launchDate,
  style: TextStyle(
    fontSize: 48,
    fontWeight: FontWeight.bold,
    letterSpacing: 4,
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Countdown(
  targetDate: DateTime(2026, 12, 31, 23, 59, 59),
)
```

### With Options

```dart
Countdown(
  targetDate: saleEndDate,
  onComplete: handleSaleEnd,
  format: CountdownFormat.dhms,
  separator: ':',
)
```

## Common Patterns

### Format Options

| Format | Output Example |
|--------|---------------|
| `CountdownFormat.dhms` (default) | `03:14:25:10` |
| `CountdownFormat.hms` | `14:25:10` |
| `CountdownFormat.ms` | `25:10` |
| `CountdownFormat.secondsOnly` | `1510` |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiCountdown` | `Countdown` |
| API | Identical parameters | Identical parameters |

### When to Use

- Event deadline displays
- Sale/promotion countdown timers
- Session timeout warnings
- Launch countdown pages
- Quiz/exam time limits

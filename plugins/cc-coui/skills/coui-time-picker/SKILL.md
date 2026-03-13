---
name: coui-time-picker
description: Activate when creating time pickers, hour/minute selectors, 12-hour or 24-hour time inputs, or time range selectors using CouiTimePicker, TimePicker, TimeFormat in CoUI Flutter or CoUI Web.
---

# CoUI TimePicker

## Overview

The TimePicker is a time selection component enabling selection of hours and minutes. It supports both 12-hour (AM/PM) and 24-hour formats with configurable minute intervals and time range restrictions. Flutter uses `CouiTimePicker` while Web uses `TimePicker`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic 24-Hour TimePicker

```dart
CouiTimePicker(
  value: selectedTime,
  onChanged: handleTimeChanged,
)
```

### 12-Hour Format with 15-Minute Intervals

```dart
CouiTimePicker(
  value: appointmentTime,
  onChanged: handleAppointmentTimeChanged,
  format: TimeFormat.h12,
  minuteInterval: 15,
)
```

### Time Range Restriction

```dart
CouiTimePicker(
  value: businessTime,
  onChanged: handleBusinessTimeChanged,
  minTime: TimeOfDay(hour: 9, minute: 0),
  maxTime: TimeOfDay(hour: 18, minute: 0),
  minuteInterval: 30,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `TimeOfDay?` | `null` | Currently selected time |
| `onChanged` | `ValueChanged<TimeOfDay>?` | `null` | Time change callback |
| `format` | `TimeFormat` | `TimeFormat.h24` | Time format (12h/24h) |
| `minuteInterval` | `int` | `1` | Minute selection increment |
| `minTime` | `TimeOfDay?` | `null` | Minimum selectable time |
| `maxTime` | `TimeOfDay?` | `null` | Maximum selectable time |
| `enabled` | `bool` | `true` | Enable/disable state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic TimePicker

```dart
TimePicker(
  value: selectedTime,
  onChanged: handleTimeChanged,
)
```

### 12-Hour Format with Intervals

```dart
TimePicker(
  value: appointmentTime,
  onChanged: handleAppointmentTimeChanged,
  format: '12h',
  minuteInterval: 15,
)
```

### Time Range Restriction

```dart
TimePicker(
  value: businessTime,
  onChanged: handleBusinessTimeChanged,
  minTime: '09:00',
  maxTime: '18:00',
)
```

## Common Patterns

### Format Variants

- **24-Hour Format** (default): Uses `TimeFormat.h24` (Flutter) or `'24h'` (Web)
- **12-Hour Format (AM/PM)**: Uses `TimeFormat.h12` (Flutter) or `'12h'` (Web)

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `CouiTimePicker` | `TimePicker` |
| Time value | `TimeOfDay` object | `TimeOfDay` or string |
| Format enum | `TimeFormat.h12` / `TimeFormat.h24` | `'12h'` / `'24h'` (string) |
| Min/max time | `TimeOfDay(hour: 9, minute: 0)` | `'09:00'` (string) |

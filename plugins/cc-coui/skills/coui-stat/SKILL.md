---
name: coui-stat
description: Activate when creating statistic displays, dashboard metrics, KPI cards, or trend indicators using Stat/StatTrend (Flutter) or Stat (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Stat

## Overview

The Stat component displays key numerical statistics in dashboards and reports. It combines a label, value, optional helper text, and trend indicators to present data comprehensively.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
Stat(
  label: '총 사용자',
  value: '128,450',
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Stat identifying text |
| `value` | `dynamic` | required | Numeric display (String or Widget) |
| `helpText` | `String?` | `null` | Secondary description beneath value |
| `trend` | `StatTrend?` | `null` | Direction indicator (up/down/neutral) |
| `trendValue` | `String?` | `null` | Percentage or change text |

### With Upward Trend

```dart
Stat(
  label: '이번 달 매출',
  value: '₩12,450,000',
  helpText: '지난 달 대비',
  trend: StatTrend.up,
  trendValue: '+12.5%',
)
```

### With Downward Trend

```dart
Stat(
  label: '이탈률',
  value: '3.2%',
  trend: StatTrend.down,
  trendValue: '-0.8%',
)
```

### Dashboard Grid Layout

```dart
GridView.count(
  crossAxisCount: 3,
  children: [
    Stat(label: '사용자', value: '12,450', trend: StatTrend.up, trendValue: '+5%'),
    Stat(label: '매출', value: '₩8.2M', trend: StatTrend.up, trendValue: '+12%'),
    Stat(label: '이탈률', value: '2.1%', trend: StatTrend.down, trendValue: '-0.3%'),
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
Stat(
  label: '총 사용자',
  value: '128,450',
)
```

### With Trend

```dart
Stat(
  label: '이번 달 매출',
  value: '₩12,450,000',
  helpText: '지난 달 대비',
  trend: StatTrend.up,
  trendValue: '+12.5%',
)
```

## Common Patterns

### Trend Variants

| Trend | Color | Use Case |
|-------|-------|----------|
| `StatTrend.up` | Green | Positive change |
| `StatTrend.down` | Red | Negative change |
| `StatTrend.neutral` | Gray | Stable metrics |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `Stat` | `Stat` |
| API | Identical parameters | Identical parameters |

### When to Use

- Dashboard KPI displays
- Analytics summary cards
- Financial metrics with trends
- Performance monitoring panels

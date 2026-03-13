---
name: coui-tracker
description: Activate when creating segmented progress trackers, uptime monitors, habit tracking displays, or streak visualizations using CouiTracker/TrackerSegment/TrackerStatus/TrackerSize/TrackerVariant (Flutter) or Tracker (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Tracker

## Overview

The Tracker is a visual progress component composed of multiple segments. It displays progress status using colored segments and is used for uptime monitoring, habit tracking, and streak displays.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiTracker(
  segments: [
    TrackerSegment(status: TrackerStatus.success),
    TrackerSegment(status: TrackerStatus.warning),
    TrackerSegment(status: TrackerStatus.error),
    TrackerSegment(status: TrackerStatus.idle),
  ],
  size: TrackerSize.medium,
)
```

### CouiTracker Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `segments` | `List<TrackerSegment>` | required | Segment configurations |
| `size` | `TrackerSize` | `medium` | Segment dimensions |
| `variant` | `TrackerVariant` | `default` | Visual style |

### TrackerSegment Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `status` | `TrackerStatus` | required | Segment state |
| `tooltip` | `String?` | `null` | Hover text display |

### With Tooltips

```dart
CouiTracker(
  segments: [
    TrackerSegment(status: TrackerStatus.success, tooltip: 'Day 1: 100%'),
    TrackerSegment(status: TrackerStatus.success, tooltip: 'Day 2: 99.9%'),
    TrackerSegment(status: TrackerStatus.warning, tooltip: 'Day 3: 95%'),
    TrackerSegment(status: TrackerStatus.error, tooltip: 'Day 4: 80%'),
  ],
)
```

### Dynamic Generation

```dart
CouiTracker(
  segments: List.generate(30, (i) => TrackerSegment(
    status: data[i] > 0.95
        ? TrackerStatus.success
        : data[i] > 0.8
            ? TrackerStatus.warning
            : TrackerStatus.error,
  )),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Tracker(
  segments: [
    TrackerSegment(status: TrackerStatus.success),
    TrackerSegment(status: TrackerStatus.success),
    TrackerSegment(status: TrackerStatus.warning),
  ],
)
```

## Common Patterns

### Status Types

| Status | Color | Description |
|--------|-------|-------------|
| `TrackerStatus.success` | Green | Completion/normal operation |
| `TrackerStatus.warning` | Yellow | Alert condition |
| `TrackerStatus.error` | Red | Failure state |
| `TrackerStatus.idle` | Gray | Inactive/future |

### Size Options

| Size | Height |
|------|--------|
| `TrackerSize.small` | 16px |
| `TrackerSize.medium` | 24px (default) |
| `TrackerSize.large` | 32px |

### Visual Variants

| Variant | Description |
|---------|-------------|
| `TrackerVariant.default` | Solid-colored segments |
| `TrackerVariant.gradient` | Segments with gradient effects |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiTracker` | `Tracker` |
| API | Identical parameters | Identical parameters |

### When to Use

- Uptime monitoring displays
- Habit tracking streaks
- Build/deployment status history
- Service health dashboards

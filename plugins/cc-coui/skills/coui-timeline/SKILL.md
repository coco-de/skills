---
name: coui-timeline
description: Activate when creating chronological event displays, activity logs, history views, or time-sequential layouts using CouiTimeline, Timeline, TimelineItem, or TimelineVariant in CoUI Flutter or CoUI Web.
---

# CoUI Timeline

## Overview

The Timeline component displays events or activities in chronological order using a visual time-sequential layout with connecting lines and dot indicators. It supports left, right, and alternating alignment variants.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Timeline

```dart
CouiTimeline(
  items: [
    TimelineItem(
      title: 'Project Started',
      subtitle: 'January 1, 2024',
      content: const Text('The project officially launched.'),
    ),
    TimelineItem(
      title: 'First Release',
      subtitle: 'March 15, 2024',
      content: const Text('Beta version was released.'),
    ),
    TimelineItem(
      title: 'Production Launch',
      subtitle: 'June 1, 2024',
      content: const Text('Version 1.0 went live.'),
    ),
  ],
)
```

### Alternate Alignment

```dart
CouiTimeline(
  items: companyHistory,
  variant: TimelineVariant.alternate,
  lineColor: Colors.indigo,
  dotColor: Colors.indigo,
)
```

### Right Alignment

```dart
CouiTimeline(
  items: notifications,
  variant: TimelineVariant.right,
)
```

### Key Classes

#### CouiTimeline

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<TimelineItem>` | required | Timeline item list |
| `variant` | `TimelineVariant` | `TimelineVariant.left` | Alignment mode |
| `lineColor` | `Color?` | `null` | Connecting line color |
| `dotColor` | `Color?` | `null` | Dot indicator color |

#### TimelineItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `String` | required | Event title |
| `subtitle` | `String?` | `null` | Date or secondary text |
| `content` | `Widget?` | `null` | Additional content |

### TimelineVariant

| Value | Description |
|-------|-------------|
| `left` | All items aligned to the left (default) |
| `right` | All items aligned to the right |
| `alternate` | Items alternate left and right |

### Activity Log Pattern

```dart
CouiTimeline(
  items: [
    TimelineItem(
      title: 'File uploaded',
      subtitle: '2 hours ago',
      content: const Text('report.pdf was uploaded by John'),
    ),
    TimelineItem(
      title: 'Comment added',
      subtitle: '5 hours ago',
      content: const Text('Jane commented on the document'),
    ),
    TimelineItem(
      title: 'Document created',
      subtitle: 'Yesterday',
      content: const Text('Initial draft was created'),
    ),
  ],
  variant: TimelineVariant.left,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Timeline

```dart
Timeline(
  items: [
    TimelineItem(
      title: 'Project Started',
      subtitle: '2024-01-01',
      content: Component.text('The project officially launched.'),
    ),
  ],
)
```

### Alternate Variant

```dart
Timeline(
  items: historyItems,
  variant: 'alternate',
)
```

## Common Patterns

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Variant type | `TimelineVariant.left` enum | `'left'` string |
| Content type | `Widget` | `Component` |

### Shared Concepts

- Both platforms support `items`, `variant` for alignment, and custom colors.
- Timeline items consist of `title`, optional `subtitle`, and optional `content`.
- The connecting line and dot indicators are automatically rendered between items.

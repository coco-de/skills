---
name: coui-refresh-trigger
description: Activate when creating pull-to-refresh interactions, refresh indicators, or scroll-triggered content updates using CouiRefreshTrigger, RefreshTrigger, or onRefresh in CoUI Flutter or CoUI Web.
---

# CoUI RefreshTrigger

## Overview

RefreshTrigger is a pull-to-refresh component that enables users to pull down on scrollable content to trigger updates. It implements iOS and Android-style refresh patterns with customizable displacement and indicator color.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic RefreshTrigger

```dart
CouiRefreshTrigger(
  onRefresh: () async {
    await fetchLatestData();
  },
  child: ListView.builder(
    itemCount: _items.length,
    itemBuilder: (context, index) => ListTile(
      title: Text(_items[index]),
    ),
  ),
)
```

### Custom Displacement and Color

```dart
CouiRefreshTrigger(
  onRefresh: () async {
    await fetchLatestData();
  },
  displacement: 60.0,
  color: Colors.blue,
  child: SingleChildScrollView(
    child: Column(
      children: _buildContentList(),
    ),
  ),
)
```

### Key Classes

#### CouiRefreshTrigger

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `onRefresh` | `Future<void> Function()` | required | Async handler when refresh triggers |
| `child` | `Widget` | required | Scrollable widget to wrap |
| `displacement` | `double` | `40.0` | Distance in pixels where indicator displays |
| `color` | `Color?` | `null` | Refresh indicator color |

### Feed Refresh Pattern

```dart
CouiRefreshTrigger(
  onRefresh: () async {
    final newItems = await api.fetchFeed();
    setState(() => _items = newItems);
  },
  child: ListView.builder(
    itemCount: _items.length,
    itemBuilder: (context, index) => FeedCard(item: _items[index]),
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic RefreshTrigger

```dart
RefreshTrigger(
  onRefresh: () async {
    await fetchLatestData();
  },
  child: ListView(
    children: _items.map((item) => ListTile(title: Component.text(item))).toList(),
  ),
)
```

## Common Patterns

### Variants

| Variant | Description |
|---------|-------------|
| Default | System refresh indicator |
| Custom Color | Brand-specific indicator coloring |
| Extended Displacement | Greater pull distance before triggering |

### Key Notes

- The `onRefresh` callback must return a `Future<void>`. The indicator remains visible until the future completes.
- The `child` must be a scrollable widget (ListView, SingleChildScrollView, etc.).
- Displacement controls how far down the indicator appears, not the trigger distance.

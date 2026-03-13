---
name: coui-status
description: Activate when creating status indicators, online/offline dots, user presence indicators, or system state displays using Status/StatusVariant/StatusSize (Flutter) or Status (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Status

## Overview

The Status component displays the current state of a user or system through a colored dot and optional label. Common use cases include chat applications, user lists, and server monitoring.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
Status(
  variant: StatusVariant.online,
  label: '온라인',
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `variant` | `StatusVariant` | required | State type |
| `label` | `String?` | `null` | Optional text description |
| `size` | `StatusSize` | `medium` | Component dimensions |
| `showDot` | `bool` | `true` | Controls dot visibility |

### Dot-Only Display

```dart
Status(
  variant: StatusVariant.busy,
  showDot: true,
)
```

### Large Away Status

```dart
Status(
  variant: StatusVariant.away,
  label: '자리 비움',
  size: StatusSize.large,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Status(variant: StatusVariant.online, label: '온라인')
Status(variant: StatusVariant.busy)
Status(variant: StatusVariant.offline, label: '오프라인')
```

## Common Patterns

### State Variants

| Variant | Color | Description |
|---------|-------|-------------|
| `StatusVariant.online` | Green | Available |
| `StatusVariant.offline` | Gray | Inactive |
| `StatusVariant.busy` | Red | Unavailable |
| `StatusVariant.away` | Yellow | Temporarily absent |

### Size Options

| Size | Dot Diameter |
|------|-------------|
| `StatusSize.small` | 6px |
| `StatusSize.medium` | 8px (default) |
| `StatusSize.large` | 12px |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `Status` | `Status` |
| Size support | `StatusSize` enum | `StatusSize` enum |

### When to Use

- User presence in chat applications
- Server/service health monitoring
- Contact list availability indicators
- System status dashboards

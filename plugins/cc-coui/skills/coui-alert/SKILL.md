---
name: coui-alert
description: Activate when creating alert messages, notification banners, status indicators, or dismissible info/success/warning/error alerts using CouiAlert, Alert, or AlertVariant in CoUI Flutter or CoUI Web.
---

# CoUI Alert

## Overview

The Alert component displays informational, success, warning, and error messages with visual distinction based on the alert type. It supports optional titles, custom icons, and dismissible behavior.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Info Alert

```dart
CouiAlert(
  title: 'Notice',
  description: 'A new update is available.',
  variant: AlertVariant.info,
)
```

### Success Alert (Dismissible)

```dart
CouiAlert(
  title: 'Save Complete',
  description: 'Your changes have been saved successfully.',
  variant: AlertVariant.success,
  closable: true,
  onDismiss: () {
    // Handle dismiss
  },
)
```

### Warning Alert

```dart
CouiAlert(
  description: 'Storage space is running low.',
  variant: AlertVariant.warning,
)
```

### Error Alert with Custom Icon

```dart
CouiAlert(
  title: 'Error Occurred',
  description: 'There was a problem processing your request. Please try again.',
  variant: AlertVariant.error,
  icon: const Icon(Icons.error_outline),
)
```

### Key Classes

#### CouiAlert

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `String?` | `null` | Alert heading |
| `description` | `String` | required | Alert message content |
| `variant` | `AlertVariant` | `AlertVariant.info` | Alert type |
| `icon` | `Widget?` | `null` | Custom icon widget |
| `onDismiss` | `VoidCallback?` | `null` | Dismiss callback |
| `closable` | `bool` | `false` | Show close button |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Alerts

```dart
Alert(
  title: 'Notice',
  description: 'A new update is available.',
  variant: 'info',
)

Alert(
  title: 'Save Complete',
  description: 'Your changes have been saved.',
  variant: 'success',
  closable: true,
  onDismiss: handleAlertDismissed,
)

Alert(
  title: 'Warning',
  description: 'Storage space is running low.',
  variant: 'warning',
)
```

## Common Patterns

### Alert Variants

| Variant | Use Case | Visual Style |
|---------|----------|--------------|
| `info` | System notifications, general information | Blue/neutral |
| `success` | Confirmed successful operations | Green |
| `warning` | Important considerations, potential issues | Yellow/orange |
| `error` | Problems requiring user attention | Red |

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Variant type | `AlertVariant.info` enum | `'info'` string |
| Parameters | Same names | Same names |

### Shared Concepts

- Both platforms support `title`, `description`, `variant`, `closable`, and `onDismiss`.
- `title` is optional; alerts can display description-only.
- When `closable` is true, a close button appears that triggers `onDismiss`.

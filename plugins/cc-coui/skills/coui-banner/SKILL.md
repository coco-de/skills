---
name: coui-banner
description: Activate when creating notification banners, alert bars, info/success/warning/error messages at top of page using Banner (Flutter) or Banner (Web) with BannerVariant in CoUI Flutter or CoUI Web.
---

# CoUI Banner

## Overview

The Banner component is a notification element displayed at the top of a page to communicate important information, warnings, errors, and success messages. It supports four variants: info, success, warning, and error.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
Banner(
  message: '시스템 점검이 예정되어 있습니다.',
  variant: BannerVariant.info,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | `String` | required | Text content displayed in the banner |
| `variant` | `BannerVariant` | `info` | Visual style variant (info, success, warning, error) |
| `onDismiss` | `VoidCallback?` | `null` | Close button handler; null hides dismiss button |
| `icon` | `Widget?` | `null` | Custom icon override (variant-specific default if omitted) |
| `action` | `Widget?` | `null` | Optional action widget displayed on the right |

### Success Banner with Dismiss

```dart
Banner(
  message: '저장이 완료되었습니다.',
  variant: BannerVariant.success,
  onDismiss: handleDismiss,
)
```

### Warning Banner with Action

```dart
Banner(
  message: '세션이 곧 만료됩니다.',
  variant: BannerVariant.warning,
  icon: Icon(Icons.warning_amber),
  action: Button.ghost(
    onPressed: handleExtendSession,
    child: Text('연장하기'),
  ),
  onDismiss: handleDismiss,
)
```

### Error Banner

```dart
Banner(
  message: '요청을 처리하는 중 오류가 발생했습니다.',
  variant: BannerVariant.error,
  onDismiss: handleDismiss,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Banner(
  message: '시스템 점검이 예정되어 있습니다.',
  variant: BannerVariant.info,
)
```

### With Dismiss and Action

```dart
Banner(
  message: '세션이 곧 만료됩니다.',
  variant: BannerVariant.warning,
  action: Button.ghost(
    onClick: handleExtendSession,
    child: Text('연장하기'),
  ),
  onDismiss: handleDismiss,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `message` | `String` | required | Text content |
| `variant` | `BannerVariant` | `info` | Visual variant |
| `onDismiss` | `VoidCallback?` | `null` | Dismiss handler |
| `icon` | `Component?` | `null` | Custom icon |
| `action` | `Component?` | `null` | Action widget |

## Common Patterns

### Variant Usage

| Variant | Use Case |
|---------|----------|
| `BannerVariant.info` | General information, announcements |
| `BannerVariant.success` | Successful operation completion |
| `BannerVariant.warning` | Situations requiring user attention |
| `BannerVariant.error` | Error or failure states |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `Banner` | `Banner` |
| Action button | `Button.ghost()` | `Button.ghost()` |
| Child type | `Widget` | `Component` |

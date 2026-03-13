---
name: coui-swiper
description: Activate when creating swipe-to-dismiss items, swipeable cards, or gesture-based navigation using CouiSwiper, Swiper, SwipeDirection, or onDismiss in CoUI Flutter or CoUI Web.
---

# CoUI Swiper

## Overview

The Swiper component enables dismissal or navigation through items using swipe gestures. It supports horizontal, vertical, or omnidirectional swiping with configurable thresholds, suitable for notifications, card decks, and feed interactions.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Swiper

```dart
CouiSwiper(
  onDismiss: () {
    // Handle item dismissed
  },
  child: ListTile(
    title: Text('New message'),
    subtitle: Text('Swipe to dismiss'),
  ),
)
```

### Horizontal Swipe

```dart
CouiSwiper(
  direction: SwipeDirection.horizontal,
  threshold: 0.4,
  onSwipe: (direction) {
    // Handle swipe direction
  },
  onDismiss: () {
    // Handle dismissed
  },
  child: Card(
    child: ListTile(title: Text('Swipeable item')),
  ),
)
```

### Vertical Swipe

```dart
CouiSwiper(
  direction: SwipeDirection.vertical,
  onDismiss: () {
    // Handle dismissed
  },
  child: FeedCard(content: 'Feed content'),
)
```

### Omnidirectional Swipe

```dart
CouiSwiper(
  direction: SwipeDirection.any,
  onSwipe: (direction) {
    // Handle any direction
  },
  onDismiss: () {
    // Handle dismissed
  },
  child: PhotoCard(imageUrl: 'url'),
)
```

### Key Classes

#### CouiSwiper

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Widget` | required | Target widget for swiping |
| `onSwipe` | `void Function(SwipeDirection)?` | `null` | Callback on swipe |
| `onDismiss` | `VoidCallback?` | `null` | Callback when dismissed past threshold |
| `direction` | `SwipeDirection` | `horizontal` | Permitted swipe direction |
| `threshold` | `double` | `0.3` | Dismissal trigger threshold (0.0-1.0) |

### SwipeDirection

| Value | Description |
|-------|-------------|
| `horizontal` | Left-right swiping |
| `vertical` | Up-down swiping |
| `any` | All directions |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Swiper

```dart
Swiper(
  onDismiss: handleDismissed,
  child: NotificationCard(
    title: 'New message',
    body: 'Swipe to dismiss',
  ),
)
```

### With Direction and Threshold

```dart
Swiper(
  direction: SwipeDirection.horizontal,
  threshold: 0.3,
  onSwipe: handleSwiped,
  onDismiss: handleDismissed,
  child: Card(child: Component.text('Swipeable item')),
)
```

## Common Patterns

### Use Cases

| Direction | Best For |
|-----------|----------|
| `horizontal` | Notification dismissal, card stacks |
| `vertical` | Feed navigation, pull-to-dismiss |
| `any` | Photo cards, tinder-style interactions |

### API Consistency

- Both Flutter and Web share the same parameters: `child`, `onSwipe`, `onDismiss`, `direction`, and `threshold`.
- The threshold value (0.0-1.0) determines how far the user must swipe before the dismiss callback fires.

---
name: coui-hover-card
description: Activate when creating hover-triggered info cards, user profile previews, or tooltip-like rich content popups using CouiHoverCard, HoverCard, or HoverCardSide in CoUI Flutter or CoUI Web.
---

# CoUI HoverCard

## Overview

The HoverCard component displays additional information in a card when hovering over a trigger element. It supports configurable open/close delays and placement positioning to prevent unintended display.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic HoverCard

```dart
CouiHoverCard(
  trigger: Text(
    '@username',
    style: TextStyle(color: Colors.blue),
  ),
  content: Column(
    mainAxisSize: MainAxisSize.min,
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      CouiAvatar(name: 'John Doe'),
      SizedBox(height: 8),
      Text('John Doe', style: TextStyle(fontWeight: FontWeight.bold)),
      Text('@johndoe'),
      Text('Flutter developer | CoUI contributor'),
    ],
  ),
)
```

### Advanced Configuration

```dart
CouiHoverCard(
  trigger: Icon(Icons.info_outline),
  content: Text('Additional information displayed here.'),
  side: HoverCardSide.top,
  openDelay: Duration(milliseconds: 500),
  closeDelay: Duration(milliseconds: 200),
)
```

### Key Classes

#### CouiHoverCard

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger` | `Widget` | required | Element that detects hover |
| `content` | `Widget` | required | Card content on hover |
| `openDelay` | `Duration` | 700ms | Delay before showing card |
| `closeDelay` | `Duration` | 300ms | Delay before hiding card |
| `side` | `HoverCardSide` | `bottom` | Card placement relative to trigger |

### User Profile Preview Pattern

```dart
CouiHoverCard(
  trigger: Text('@contributor'),
  content: Column(
    mainAxisSize: MainAxisSize.min,
    children: [
      Row(
        children: [
          CouiAvatar(name: 'Jane Smith'),
          SizedBox(width: 8),
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Jane Smith', style: TextStyle(fontWeight: FontWeight.bold)),
              Text('Senior Engineer'),
            ],
          ),
        ],
      ),
      SizedBox(height: 8),
      Text('Building great products with CoUI.'),
    ],
  ),
  openDelay: Duration(milliseconds: 300),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic HoverCard

```dart
HoverCard(
  trigger: Component.text('@username'),
  content: Column(
    children: [
      Avatar(name: 'John Doe'),
      Component.text('John Doe'),
    ],
  ),
)
```

### Advanced Configuration

```dart
HoverCard(
  trigger: Icon(CouiIcons.info),
  content: Component.text('Additional information'),
  side: HoverCardSide.top,
  openDelay: Duration(milliseconds: 300),
  closeDelay: Duration(milliseconds: 150),
)
```

## Common Patterns

### Position Options (HoverCardSide)

| Value | Description |
|-------|-------------|
| `top` | Display above the trigger |
| `right` | Display to the right |
| `bottom` | Display below (default) |
| `left` | Display to the left |

### API Consistency

- Both Flutter and Web share the same parameters: `trigger`, `content`, `openDelay`, `closeDelay`, and `side`.
- HoverCard is best suited for desktop/cursor-based interfaces where hover is available.
- For touch-based interactions, consider using Popover or Tooltip instead.

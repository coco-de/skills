---
name: coui-swap
description: Activate when creating animated toggle widgets, state-switching icons, or two-state visual toggles with rotation/flip effects using Swap, Swap, onChild, or offChild in CoUI Flutter or CoUI Web.
---

# CoUI Swap

## Overview

The Swap component is a toggle widget that switches between two visual states based on a boolean value. It displays different child widgets depending on whether the state is active or inactive, with optional rotation or flip animation effects.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Swap (Menu Toggle)

```dart
Swap(
  value: _isMenuOpen,
  onChanged: (value) {
    setState(() => _isMenuOpen = value);
  },
  onChild: const Icon(Icons.close),
  offChild: const Icon(Icons.menu),
)
```

### With Rotation Animation

```dart
Swap(
  value: _isFavorite,
  onChanged: (value) {
    setState(() => _isFavorite = value);
  },
  rotate: true,
  onChild: const Icon(Icons.favorite, color: Colors.red),
  offChild: const Icon(Icons.favorite_border),
)
```

### With Flip Animation

```dart
Swap(
  value: _isFlipped,
  onChanged: (value) {
    setState(() => _isFlipped = value);
  },
  flip: true,
  onChild: const Text('ON'),
  offChild: const Text('OFF'),
)
```

### Key Classes

#### Swap

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `bool` | required | Current state (true = on) |
| `onChanged` | `ValueChanged<bool>?` | `null` | State change callback |
| `onChild` | `Widget` | required | Widget shown when value is true |
| `offChild` | `Widget` | required | Widget shown when value is false |
| `rotate` | `bool` | `false` | Enable rotation animation |
| `flip` | `bool` | `false` | Enable flip animation |

### Theme Toggle Pattern

```dart
Swap(
  value: _isDarkMode,
  onChanged: (value) {
    setState(() => _isDarkMode = value);
    updateTheme(value);
  },
  rotate: true,
  onChild: const Icon(Icons.dark_mode),
  offChild: const Icon(Icons.light_mode),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Swap

```dart
Swap(
  value: isMenuOpen,
  onChanged: handleMenuToggled,
  onChild: Icon('close'),
  offChild: Icon('menu'),
)
```

### With Rotation

```dart
Swap(
  value: isFavorite,
  onChanged: handleFavoriteToggled,
  rotate: true,
  onChild: Icon('favorite'),
  offChild: Icon('favorite_border'),
)
```

## Common Patterns

### Use Cases

| Pattern | onChild | offChild | Animation |
|---------|---------|----------|-----------|
| Menu toggle | Close icon | Hamburger icon | Default |
| Favorite | Filled heart | Outline heart | `rotate: true` |
| Theme switch | Moon icon | Sun icon | `rotate: true` |
| Visibility | Eye-off icon | Eye icon | `flip: true` |

### API Consistency

- Both Flutter and Web share the same parameters: `value`, `onChanged`, `onChild`, `offChild`, `rotate`, and `flip`.
- Only one animation mode should be active (`rotate` or `flip`, not both).

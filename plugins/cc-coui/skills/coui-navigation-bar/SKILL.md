---
name: coui-navigation-bar
description: Activate when creating bottom navigation bars, tab bars, or primary section navigation using NavigationBar, NavigationBarItem, or NavigationBarVariant in CoUI Flutter or CoUI Web.
---

# CoUI NavigationBar

## Overview

The NavigationBar is a bottom navigation component for navigating between primary sections of an app. It combines icons and labels to visually indicate the current location. Supports filled and outlined variants, with optional label visibility control.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic NavigationBar

```dart
int _selectedIndex = 0;

NavigationBar(
  currentIndex: _selectedIndex,
  onTap: (index) {
    setState(() => _selectedIndex = index);
  },
  items: [
    NavigationBarItem(
      icon: Icon(Icons.home_outlined),
      activeIcon: Icon(Icons.home),
      label: 'Home',
    ),
    NavigationBarItem(
      icon: Icon(Icons.search_outlined),
      activeIcon: Icon(Icons.search),
      label: 'Search',
    ),
    NavigationBarItem(
      icon: Icon(Icons.person_outlined),
      activeIcon: Icon(Icons.person),
      label: 'Profile',
    ),
  ],
)
```

### Outlined Variant (No Labels)

```dart
NavigationBar(
  currentIndex: _selectedIndex,
  onTap: (index) {
    setState(() => _selectedIndex = index);
  },
  variant: NavigationBarVariant.outlined,
  showLabels: false,
  items: [
    NavigationBarItem(icon: Icon(Icons.home_outlined), label: 'Home'),
    NavigationBarItem(icon: Icon(Icons.search_outlined), label: 'Search'),
    NavigationBarItem(icon: Icon(Icons.settings_outlined), label: 'Settings'),
  ],
)
```

### Key Classes

#### NavigationBar

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<NavigationBarItem>` | required | Navigation item list |
| `currentIndex` | `int` | `0` | Currently selected item index |
| `onTap` | `void Function(int)?` | `null` | Item tap handler |
| `variant` | `NavigationBarVariant` | `filled` | Style variant (filled / outlined) |
| `showLabels` | `bool` | `true` | Label visibility toggle |

#### NavigationBarItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `icon` | `Widget` | required | Inactive state icon |
| `activeIcon` | `Widget?` | `null` | Active state icon (falls back to icon) |
| `label` | `String` | required | Item label text |

### Mobile App Pattern

```dart
Scaffold(
  body: pages[_selectedIndex],
  bottomNavigationBar: NavigationBar(
    currentIndex: _selectedIndex,
    onTap: (i) => setState(() => _selectedIndex = i),
    items: [
      NavigationBarItem(
        icon: Icon(Icons.home_outlined),
        activeIcon: Icon(Icons.home),
        label: 'Home',
      ),
      NavigationBarItem(
        icon: Icon(Icons.explore_outlined),
        activeIcon: Icon(Icons.explore),
        label: 'Explore',
      ),
      NavigationBarItem(
        icon: Icon(Icons.person_outlined),
        activeIcon: Icon(Icons.person),
        label: 'Profile',
      ),
    ],
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic NavigationBar

```dart
NavigationBar(
  currentIndex: _selectedIndex,
  onTap: (index) => setState(() => _selectedIndex = index),
  items: [
    NavigationBarItem(icon: Icon(CouiIcons.home), label: 'Home'),
    NavigationBarItem(icon: Icon(CouiIcons.search), label: 'Search'),
    NavigationBarItem(icon: Icon(CouiIcons.person), label: 'Profile'),
  ],
)
```

### Outlined Variant

```dart
NavigationBar(
  currentIndex: _selectedIndex,
  onTap: (index) => setState(() => _selectedIndex = index),
  variant: NavigationBarVariant.outlined,
  showLabels: true,
  items: [
    NavigationBarItem(icon: Icon(CouiIcons.home), label: 'Home'),
    NavigationBarItem(icon: Icon(CouiIcons.search), label: 'Search'),
  ],
)
```

## Common Patterns

### Variants

| Variant | Description |
|---------|-------------|
| `filled` | Default variant with filled background highlight on selected item |
| `outlined` | Border-only variant for minimal design |

### API Consistency

- Both Flutter and Web use `currentIndex`, `onTap`, and `items` parameters.
- Both support `NavigationBarVariant.filled` and `NavigationBarVariant.outlined`.
- Both support `showLabels` to toggle label visibility.
- Flutter `NavigationBarItem` supports `activeIcon` for distinct active state icons; Web uses the same `icon` for both states.

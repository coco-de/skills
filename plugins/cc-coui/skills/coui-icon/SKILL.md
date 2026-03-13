---
name: coui-icon
description: Activate when creating icons, vector icon displays, or using CouiIcons preset icons with CouiIcon (Flutter) or Icon (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Icon

## Overview

The Icon component provides a consistent set of vector icons through the `CouiIcons` preset. It supports customizable size, color, and semantic labeling for accessibility.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiIcon(
  icon: CouiIcons.home,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `icon` | `IconData` | required | The icon data to display |
| `size` | `double?` | `null` | Icon size in pixels; uses theme default if null |
| `color` | `Color?` | `null` | Icon color; uses theme color if null |
| `semanticLabel` | `String?` | `null` | Accessibility label for screen readers |

### With All Parameters

```dart
CouiIcon(
  icon: CouiIcons.delete,
  size: 20.0,
  color: Colors.red,
  semanticLabel: '삭제',
)
```

### Icon in Button Pattern

```dart
CouiButton(
  onPressed: handleShare,
  child: Row(
    children: [
      CouiIcon(icon: CouiIcons.share, size: 20.0),
      SizedBox(width: 8),
      Text('공유'),
    ],
  ),
)
```

### Available CouiIcons

Common icons include: `home`, `search`, `person`, `settings`, `notification`, `heart`, `star`, `share`, `edit`, `delete`, `copy`, `check`, `close`, `arrowRight`, `menu`, `calendar`, `clock`, `location`, `camera`.

### Size Guidelines

- Inline text: 16px
- Button icons: 20px
- Standard: 24px
- Emphasis: 32px
- Hero icons: 48px

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Icon(
  icon: CouiIcons.search,
  size: 24.0,
  color: Colors.blue,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `icon` | `IconData` | required | The icon data to display |
| `size` | `double?` | `null` | Icon size in pixels |
| `color` | `Color?` | `null` | Icon color |
| `semanticLabel` | `String?` | `null` | Accessibility label |

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiIcon` | `Icon` |
| Icon set | `CouiIcons` + system `Icons` | `CouiIcons` |
| Sizing | `size` param or theme default | `size` param |
| Color | `color` param or theme color | `color` param |

### When to Use

- Navigation icons in buttons and menus
- Status indicators alongside text
- Action icons in toolbars
- Decorative icons in cards and lists

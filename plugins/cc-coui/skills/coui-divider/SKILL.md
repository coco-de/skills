---
name: coui-divider
description: Activate when creating visual separators, horizontal/vertical dividers, labeled dividers, or content section separators using Divider/DividerOrientation (Flutter) or Divider (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Divider

## Overview

The Divider is a visual separator component that divides content areas. It supports horizontal and vertical orientations with customizable thickness, color, indentation, and optional centered labels.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
Divider()
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `orientation` | `DividerOrientation` | `horizontal` | Divider direction |
| `thickness` | `double` | `1.0` | Line width in pixels |
| `color` | `Color?` | `null` | Stroke color (uses theme if null) |
| `indent` | `double` | `0.0` | Starting edge spacing |
| `endIndent` | `double` | `0.0` | Trailing edge spacing |
| `label` | `Widget?` | `null` | Center-aligned widget |

### Vertical Divider

```dart
Divider(orientation: DividerOrientation.vertical)
```

### Custom Styling

```dart
Divider(
  thickness: 2,
  color: Colors.grey.shade300,
  indent: 16,
  endIndent: 16,
)
```

### With Label

```dart
Divider(label: Text('or'))
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Divider()
```

### Vertical Divider

```dart
Divider(orientation: DividerOrientation.vertical)
```

### With Label

```dart
Divider(label: Component.text('or'))
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `orientation` | `DividerOrientation` | `horizontal` | Direction |
| `thickness` | `double` | `1.0` | Line width |
| `color` | `Color?` | `null` | Stroke color |
| `indent` | `double` | `0.0` | Start spacing |
| `endIndent` | `double` | `0.0` | End spacing |
| `label` | `Component?` | `null` | Center widget |

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `Divider` | `Divider` |
| Label type | `Widget` | `Component` |
| API | Identical parameters | Identical parameters |

### When to Use

- Section separation in Column layouts
- Item delimitation within Row arrangements
- Content grouping with labeled dividers for form sections
- "OR" dividers between login options

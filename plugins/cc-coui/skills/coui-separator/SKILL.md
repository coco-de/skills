---
name: coui-separator
description: Activate when creating visual dividers, horizontal/vertical lines, labeled separators, or content section breaks using Separator, Separator, or SeparatorVariant in CoUI Flutter or CoUI Web.
---

# CoUI Separator

## Overview

The Separator is a visual divider component used to distinguish content areas. It supports horizontal and vertical orientations, optional centered text labels, and multiple line style variants (solid, dashed, dotted).

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Separator

```dart
Separator()
```

### With Label

```dart
Separator(
  label: 'OR',
)
```

### Vertical Separator

```dart
Separator(
  orientation: Axis.vertical,
)
```

### Dashed Variant

```dart
Separator(
  label: 'Social Login',
  variant: SeparatorVariant.dashed,
)
```

### Key Classes

#### Separator

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String?` | `null` | Text displayed at center |
| `orientation` | `Axis` | `Axis.horizontal` | Line direction |
| `variant` | `SeparatorVariant` | `SeparatorVariant.solid` | Line style |

### SeparatorVariant

| Value | Description |
|-------|-------------|
| `solid` | Continuous line (default) |
| `dashed` | Dashed line |
| `dotted` | Dotted line |

### Login Form Pattern

```dart
Column(
  children: [
    EmailLoginForm(),
    Gap.v(16),
    Separator(label: 'OR'),
    Gap.v(16),
    SocialLoginButtons(),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Separator

```dart
Separator()
```

### With Label

```dart
Separator(
  label: 'OR',
)
```

### Vertical Separator

```dart
Separator(
  orientation: 'vertical',
)
```

## Common Patterns

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Orientation type | `Axis.horizontal` enum | `'horizontal'` string |
| Variant type | `SeparatorVariant.solid` enum | String |

### Use Cases

- Separating form sections
- Dividing "OR" between login options
- Vertical dividers between inline content
- Visual breaks between card sections

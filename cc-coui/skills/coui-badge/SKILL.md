---
name: coui-badge
description: Activate when creating status badges, count indicators, label tags, or small inline indicators using Badge variants (primary, secondary, destructive, outline) in coui_flutter (PrimaryBadge, SecondaryBadge, OutlineBadge, DestructiveBadge) or coui_web (Badge.primary, Badge.secondary, Badge.destructive, Badge.outline).
---

# CoUI Badge

## Overview

Badge is a small inline indicator used for status labels, tags, counters, and category markers. Both Flutter and Web packages provide four variants: **primary**, **secondary**, **outline**, and **destructive**.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Badge Variants

#### PrimaryBadge

```dart
PrimaryBadge(child: const Text('New'))
```

#### SecondaryBadge

```dart
SecondaryBadge(child: const Text('Active'))
```

#### OutlineBadge

```dart
OutlineBadge(child: const Text('Draft'))
```

#### DestructiveBadge

```dart
DestructiveBadge(child: const Text('Error'))
```

### Notification Count Pattern

```dart
Row(
  children: [
    const Icon(Icons.notifications),
    Gap.h(4),
    PrimaryBadge(child: const Text('3')),
  ],
)
```

### Status Indicator Pattern

```dart
Row(
  children: [
    const Text('Status:'),
    Gap.h(8),
    SecondaryBadge(child: const Text('Running')),
  ],
)
```

### Tag List Pattern

```dart
Wrap(
  spacing: 4,
  runSpacing: 4,
  children: [
    PrimaryBadge(child: const Text('Flutter')),
    SecondaryBadge(child: const Text('Dart')),
    OutlineBadge(child: const Text('UI')),
  ],
)
```

### Table Status Cell Pattern

```dart
Row(
  children: [
    status == 'error'
        ? DestructiveBadge(child: const Text('Failed'))
        : SecondaryBadge(child: const Text('Success')),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Badge.primary(child: Component.text('New'))
```

### Badge Variants

```dart
Badge.primary(child: Component.text('Primary'))
Badge.secondary(child: Component.text('Secondary'))
Badge.destructive(child: Component.text('Destructive'))
Badge.outline(child: Component.text('Outline'))
```

Or use the default constructor:

```dart
Badge(
  variant: BadgeVariant.primary,
  child: Component.text('Custom'),
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Component` | required | Badge content |
| `variant` | `BadgeVariant?` | `defaultVariant` | Visual variant |

The badge renders as a `<span>` element by default.

### Status Indicators

```dart
div(
  [
    Badge.primary(child: Component.text('Active')),
    Badge.secondary(child: Component.text('Pending')),
    Badge.destructive(child: Component.text('Error')),
    Badge.outline(child: Component.text('Draft')),
  ],
  classes: 'flex gap-2',
)
```

### With Other Components

```dart
// In a card header
CardHeader(
  children: [
    div(
      [
        CardTitle(titleChild: Component.text('Notifications')),
        Badge.primary(child: Component.text('3')),
      ],
      classes: 'flex items-center gap-2',
    ),
  ],
)
```

### In a Table Cell

```dart
TableCell(
  child: Badge.secondary(child: Component.text('Published')),
)
```

### Custom Styled

```dart
Badge.primary(
  classes: 'text-lg px-4',
  child: Component.text('Featured'),
)
```

## Common Patterns

### Variant Mapping

| Variant | Flutter Widget | Web Constructor | Use Case |
|---------|---------------|-----------------|----------|
| Primary | `PrimaryBadge` | `Badge.primary()` | New items, active states, counts |
| Secondary | `SecondaryBadge` | `Badge.secondary()` | Running, pending, published |
| Outline | `OutlineBadge` | `Badge.outline()` | Draft, inactive, neutral |
| Destructive | `DestructiveBadge` | `Badge.destructive()` | Errors, failures, warnings |

### When to Use

- Status indicators (active, pending, error, draft)
- Notification counters
- Tag/category labels
- Table cell status markers

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Variant selection | Separate widget per variant | Named constructors or `variant` param |
| Child type | `Widget` (typically `Text`) | `Component` (typically `Component.text()`) |
| Layout spacing | `Gap.h()` / `Wrap(spacing:)` | CSS classes (`gap-2`, `flex`) |
| Custom styling | Widget properties | CSS classes via `classes` param |

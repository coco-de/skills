---
name: coui-fab
description: Activate when creating floating action buttons, FABs, extended FABs, or primary action buttons using Fab, Fab, FabVariant, FabSize in CoUI Flutter or CoUI Web.
---

# CoUI FAB

## Overview

The FAB (Floating Action Button) is a component that emphasizes key actions on the screen, supporting multiple size and style variations. Flutter uses `Fab` while Web uses `Fab`, both sharing the same API structure for variants and sizes.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic FAB

```dart
Fab(
  onPressed: handleCreate,
  icon: Icon(Icons.add),
)
```

### Extended FAB with Label

```dart
Fab(
  onPressed: handleCreate,
  icon: Icon(Icons.add),
  label: '새 항목',
  isExtended: true,
)
```

### Secondary Variant

```dart
Fab(
  onPressed: handleEdit,
  icon: Icon(Icons.edit),
  variant: FabVariant.secondary,
)
```

### Small Size FAB

```dart
Fab(
  onPressed: handleShare,
  icon: Icon(Icons.share),
  size: FabSize.small,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `onPressed` | `VoidCallback?` | `null` | Click handler; disabled if null |
| `icon` | `Widget` | required | Icon displayed inside button |
| `label` | `String?` | `null` | Text shown in extended FAB mode |
| `size` | `FabSize` | `FabSize.medium` | Button size option |
| `variant` | `FabVariant` | `FabVariant.primary` | Visual style variant |
| `isExtended` | `bool` | `false` | Whether to include label |
| `tooltip` | `String?` | `null` | Tooltip text content |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic FAB

```dart
Fab(
  onClick: handleCreate,
  icon: Icon(Icons.add),
)
```

### Extended FAB

```dart
Fab(
  onClick: handleCreate,
  icon: Icon(Icons.add),
  label: '새 항목',
  isExtended: true,
)
```

### Secondary Variant

```dart
Fab(
  onClick: handleEdit,
  icon: Icon(Icons.edit),
  variant: FabVariant.secondary,
)
```

## Common Patterns

### Variants

| Variant | Usage |
|---------|-------|
| `FabVariant.primary` | Most emphasized main action |
| `FabVariant.secondary` | Supporting actions |
| `FabVariant.tertiary` | Less important actions |

### Sizes

| Size | Constant | Dimensions |
|------|----------|------------|
| Small | `FabSize.small` | 40px |
| Medium | `FabSize.medium` | 56px |
| Large | `FabSize.large` | 96px |

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `Fab` | `Fab` |
| Click handler | `onPressed` | `onClick` |

---
name: coui-breadcrumb
description: Activate when creating breadcrumb navigation trails, hierarchical page paths, or location indicators using CouiBreadcrumb, Breadcrumb, or BreadcrumbItem in CoUI Flutter or CoUI Web.
---

# CoUI Breadcrumb

## Overview

The Breadcrumb component displays the current page location hierarchically, allowing users to navigate to parent pages. It supports custom separators and maximum item limits for deep navigation paths.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Breadcrumb

```dart
CouiBreadcrumb(
  items: [
    BreadcrumbItem(label: 'Home', onTap: () => navigateTo('/')),
    BreadcrumbItem(label: 'Category', onTap: () => navigateTo('/category')),
    BreadcrumbItem(label: 'Product List', onTap: () => navigateTo('/products')),
    BreadcrumbItem(label: 'Product Detail'),
  ],
)
```

### Custom Separator

```dart
CouiBreadcrumb(
  items: [
    BreadcrumbItem(label: 'Settings', onTap: () => navigateTo('/settings')),
    BreadcrumbItem(label: 'Account', onTap: () => navigateTo('/account')),
    BreadcrumbItem(label: 'Security'),
  ],
  separator: const Icon(Icons.chevron_right, size: 16),
)
```

### Limited Item Display

For deep navigation paths, limit visible items with ellipsis for omitted ones:

```dart
CouiBreadcrumb(
  items: deepNavigationPath,
  maxItems: 3,
  onItemTap: handleBreadcrumbNavigation,
)
```

### Key Classes

#### CouiBreadcrumb

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<BreadcrumbItem>` | required | Navigation path items |
| `separator` | `Widget?` | `null` | Custom separator widget |
| `maxItems` | `int?` | `null` | Max displayed items (omits excess) |
| `onItemTap` | `void Function(BreadcrumbItem)?` | `null` | Item tap callback |

#### BreadcrumbItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Display text |
| `onTap` | `VoidCallback?` | `null` | Tap handler |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Breadcrumb

```dart
Breadcrumb(
  items: [
    BreadcrumbItem(label: 'Home', href: '/'),
    BreadcrumbItem(label: 'Category', href: '/category'),
    BreadcrumbItem(label: 'Product Detail'),
  ],
)
```

### Custom Separator and Max Items

```dart
Breadcrumb(
  items: navigationPath,
  separator: '>',
  maxItems: 4,
  onItemTap: handleBreadcrumbNavigation,
)
```

### BreadcrumbItem (Web)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Display text |
| `href` | `String?` | `null` | Link URL |
| `isActive` | `bool` | `false` | Current page indicator |

Active items render as `<span>` with `aria-current="page"`. Non-active items with `href` render as `<a>` links.

## Common Patterns

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Navigation action | `onTap` callback | `href` string |
| Current page indicator | Last item (no `onTap`) | `isActive: true` |
| Separator | `Widget` (e.g., Icon) | `String` (e.g., `'>'`) |

### Shared Concepts

- Both platforms support `maxItems` to limit displayed items in deep paths.
- The last item typically represents the current page and is non-interactive.
- Default separator is a forward slash `/`.

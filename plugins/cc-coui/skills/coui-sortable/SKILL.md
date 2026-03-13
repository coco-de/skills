---
name: coui-sortable
description: Activate when creating sortable lists, drag-and-drop reordering, reorderable items, or draggable lists using CouiSortable, Sortable in CoUI Flutter or CoUI Web.
---

# CoUI Sortable

## Overview

The Sortable component enables drag-and-drop reordering of list items, supporting both vertical and horizontal orientations with optional drag handles and custom drag feedback. Flutter uses `CouiSortable<T>` with generic typing while Web uses `Sortable`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Drag Sorting

```dart
CouiSortable<String>(
  items: taskList,
  onReorder: handleTaskReorder,
  itemBuilder: (context, item, index) {
    return ListTile(
      title: Text(item),
    );
  },
)
```

### With Drag Handle

```dart
CouiSortable<TaskItem>(
  items: tasks,
  onReorder: handleTasksReorder,
  handle: const Icon(Icons.drag_handle),
  itemBuilder: (context, task, index) {
    return TaskCard(task: task);
  },
)
```

### Horizontal Orientation

```dart
CouiSortable<String>(
  items: categories,
  onReorder: handleCategoriesReorder,
  direction: Axis.horizontal,
  itemBuilder: (context, category, index) {
    return CategoryChip(label: category);
  },
)
```

### With Handle Icon Variant

```dart
CouiSortable<MenuItem>(
  items: menuItems,
  onReorder: handleMenuReorder,
  handle: const Icon(Icons.drag_indicator),
  itemBuilder: (context, item, index) {
    return MenuItemRow(item: item);
  },
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<T>` | required | List of items to sort |
| `onReorder` | `void Function(int oldIndex, int newIndex)` | required | Reorder callback |
| `itemBuilder` | `Widget Function(BuildContext, T, int)` | required | Widget builder for each item |
| `handle` | `Widget?` | `null` | Optional drag handle widget |
| `direction` | `Axis` | `Axis.vertical` | Sorting orientation |
| `feedback` | `Widget Function(T)?` | `null` | Widget displayed during drag |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Sortable

```dart
Sortable(
  items: taskList,
  onReorder: handleTaskReorder,
  itemBuilder: (item, index) => ListItem(text: item),
)
```

### Horizontal Direction

```dart
Sortable(
  items: tasks,
  onReorder: handleTasksReorder,
  direction: 'horizontal',
  itemBuilder: (item, index) => TaskCard(task: item),
)
```

## Common Patterns

### Variants

- **Handle Icon**: Adds visual drag affordance with `handle` widget
- **Horizontal**: Reorders left-to-right with `direction: Axis.horizontal`
- **Custom Feedback**: Shows custom widget during drag via `feedback`

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `CouiSortable<T>` | `Sortable` |
| Direction | `Axis.horizontal` | `'horizontal'` (string) |
| Item builder | `(BuildContext, T, int)` | `(T, int)` |
| Generic typing | Supports `<T>` | Untyped |

---
name: coui-resizable
description: Activate when creating resizable split panels, draggable dividers, or adjustable layout panes using CouiResizable, Resizable, initialSizes, or onResize in CoUI Flutter or CoUI Web.
---

# CoUI Resizable

## Overview

The Resizable component provides split panel layouts with drag-to-resize functionality. Users can adjust panel sizes using drag handles. It supports horizontal and vertical directions, min/max constraints, and nested layouts for complex IDE-style interfaces.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Horizontal Split

```dart
CouiResizable(
  direction: Axis.horizontal,
  initialSizes: [0.3, 0.7],
  children: [
    const SidebarPanel(),
    const MainContentPanel(),
  ],
)
```

### Vertical Split with Constraints

```dart
CouiResizable(
  direction: Axis.vertical,
  initialSizes: [0.6, 0.4],
  minSize: 100,
  maxSize: 600,
  onResize: (sizes) {
    // Handle panel resize
  },
  children: [
    const EditorPanel(),
    const TerminalPanel(),
  ],
)
```

### Three-Panel Layout

```dart
CouiResizable(
  direction: Axis.horizontal,
  initialSizes: [0.2, 0.6, 0.2],
  children: [
    const LeftPanel(),
    const CenterPanel(),
    const RightPanel(),
  ],
)
```

### Key Classes

#### CouiResizable

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `children` | `List<Widget>` | required | Panel widgets |
| `direction` | `Axis` | `Axis.horizontal` | Split direction |
| `initialSizes` | `List<double>` | required | Initial size ratios (sum = 1.0) |
| `minSize` | `double?` | `null` | Minimum panel size in pixels |
| `maxSize` | `double?` | `null` | Maximum panel size in pixels |
| `onResize` | `ValueChanged<List<double>>?` | `null` | Resize callback with new ratios |

### IDE Layout Pattern (Nested)

```dart
CouiResizable(
  direction: Axis.horizontal,
  initialSizes: [0.25, 0.75],
  minSize: 150,
  children: [
    const FileExplorerPanel(),
    CouiResizable(
      direction: Axis.vertical,
      initialSizes: [0.7, 0.3],
      children: [
        const CodeEditorPanel(),
        const TerminalPanel(),
      ],
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Horizontal Layout

```dart
Resizable(
  direction: 'horizontal',
  initialSizes: [30, 70],
  children: [
    SidebarPanel(),
    MainContentPanel(),
  ],
)
```

### Vertical Layout

```dart
Resizable(
  direction: 'vertical',
  initialSizes: [60, 40],
  minSize: 100,
  onResize: handlePanelResized,
  children: [
    EditorPanel(),
    TerminalPanel(),
  ],
)
```

## Common Patterns

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Direction type | `Axis.horizontal` enum | `'horizontal'` string |
| Size values | Ratios (0.0-1.0, sum = 1.0) | Percentages (0-100, sum = 100) |

### Shared Concepts

- Both platforms support `children`, `direction`, `initialSizes`, `minSize`, `maxSize`, and `onResize`.
- Panels can be nested for complex layouts (e.g., IDE with sidebar + editor + terminal).
- Drag handles appear automatically between panels.

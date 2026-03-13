---
name: coui-popover
description: Activate when creating popover overlays, floating panels anchored to widgets, or hover cards in CoUI Flutter or Web using PopoverController, PopoverOverlayHandler, or HoverCard.
---

# CoUI Popover

## Overview

Floating overlay panels anchored to trigger widgets. Supports programmatic control, alignment options, and hover cards.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### PopoverController

Programmatic control over popovers:

```dart
final _controller = PopoverController();

// Show popover
unawaited(
  _controller.show<void>(
    context: context,
    alignment: Alignment.bottomCenter,
    anchorAlignment: Alignment.topCenter,
    builder: (context) {
      return Card(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Popover Content').bold,
            Gap.v(8),
            const Text('Additional details here'),
          ],
        ),
      );
    },
  ),
);

// Close popover
_controller.close();
```

### Alignment

Control where the popover appears relative to the anchor:

```dart
// Below the widget
_controller.show<void>(
  context: context,
  alignment: Alignment.bottomCenter,      // popover position
  anchorAlignment: Alignment.topCenter,   // anchor point
  builder: (context) => myContent,
);

// Above the widget
_controller.show<void>(
  context: context,
  alignment: Alignment.topCenter,
  anchorAlignment: Alignment.bottomCenter,
  builder: (context) => myContent,
);

// To the right
_controller.show<void>(
  context: context,
  alignment: Alignment.centerRight,
  anchorAlignment: Alignment.centerLeft,
  builder: (context) => myContent,
);
```

### PopoverOverlayHandler

Low-level overlay handler for popover display:

```dart
const PopoverOverlayHandler().show<void>(
  context: context,
  alignment: Alignment.bottomCenter,
  anchorAlignment: Alignment.topCenter,
  modal: true,
  builder: (context) => myPopoverContent,
);
```

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `BuildContext` | Anchor context |
| `alignment` | `AlignmentGeometry` | Popover position |
| `anchorAlignment` | `AlignmentGeometry?` | Anchor point |
| `builder` | `WidgetBuilder` | Content builder |
| `modal` | `bool` | Block background interaction |
| `offset` | `Offset?` | Position offset |
| `widthConstraint` | `PopoverConstraint` | Width behavior |
| `heightConstraint` | `PopoverConstraint` | Height behavior |

### PopoverConstraint

```dart
PopoverConstraint.flexible  // Fit content (default)
PopoverConstraint.anchorFixedSize  // Match anchor width
```

### OverlayBarrier

Configure the backdrop behind the popover:

```dart
_controller.show<void>(
  context: context,
  alignment: Alignment.bottomCenter,
  overlayBarrier: const OverlayBarrier(
    barrierColor: Colors.black54,
    borderRadius: BorderRadius.circular(8),
    padding: EdgeInsets.all(4),
  ),
  builder: (context) => myContent,
);
```

### HoverCard

Shows a card on hover (desktop pattern):

```dart
HoverCard(
  child: const Text('Hover over me'),
  builder: (context) {
    return Card(
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text('Hover Card Title').bold,
          Gap.v(8),
          const Text('Detailed information shown on hover'),
        ],
      ),
    );
  },
)
```

### Info Button Pattern

```dart
class InfoPopover extends StatefulWidget {
  const InfoPopover({super.key});

  @override
  State<InfoPopover> createState() => _InfoPopoverState();
}

class _InfoPopoverState extends State<InfoPopover> {
  final _controller = PopoverController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return IconButton.ghost(
      icon: const Icon(Icons.info_outline),
      onPressed: () {
        unawaited(
          _controller.show<void>(
            context: context,
            alignment: Alignment.bottomCenter,
            anchorAlignment: Alignment.topCenter,
            builder: (context) {
              return Card(
                padding: const EdgeInsets.all(16),
                child: const Text('Helpful information'),
              );
            },
          ),
        );
      },
      density: ButtonDensity.icon,
    );
  }
}
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Popover(
  trigger: Button(onClick: null, child: Component.text('Info')),
  child: Column(
    children: [
      Component.text('Popover Title'),
      Component.text('Popover content here.'),
    ],
  ),
)
```

### Placement

```dart
Popover(
  placement: PopoverPlacement.top,
  trigger: Icon(Icons.info),
  child: Component.text('Above the trigger'),
)
```

Available placements: `top`, `bottom`, `left`, `right`, `topStart`, `bottomEnd`.

### Hover Trigger

Web popovers use CSS `group-hover:block` for hover-based display.

### Web Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `trigger` | `Component` | required | Widget that opens the popover |
| `child` | `Component` | required | Popover content |
| `placement` | `PopoverPlacement` | `bottom` | Display position |

### Web Limitations

- Static positioning (no anchor tracking)
- No auto-invert when exceeding viewport
- Fixed width (`w-72`)
- No modal mode

## Common Patterns

### Platform Differences

| Feature | Flutter | Web |
|---------|---------|-----|
| Trigger mode | `PopoverController.show()` imperative | CSS `group-hover:block` hover-based |
| Position | `alignment` + `anchorAlignment` with viewport auto-calculation | CSS absolute + `PopoverPlacement` |
| Auto-invert | Supported via `allowInvertHorizontal/Vertical` | Not supported |
| Anchor tracking | Real-time tracking with `follow: true` | Static positioning |
| Animation | Scale(0.9->1.0) + Fade transition | Immediate display |
| Size constraints | 5 `PopoverConstraint` modes | Fixed width (w-72) |
| Modal mode | `modal: true` creates barrier | Not supported |

### Shared Concepts

- Always dispose `PopoverController` in `dispose()` (Flutter).
- Use `unawaited()` when calling `_controller.show()` from sync functions (Flutter).
- Choose `PopoverConstraint.anchorFixedSize` for dropdowns that match trigger width (Flutter).
- Use `HoverCard` for desktop hover interactions (Flutter).

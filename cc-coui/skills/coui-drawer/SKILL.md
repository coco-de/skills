---
name: coui-drawer
description: Use when creating side drawers, bottom sheets, sliding overlay panels, slide-out navigation, or overlay sidebars in CoUI Flutter (DrawerWrapper, SheetWrapper, showDrawer) or CoUI Web (Drawer component with DrawerSide).
---

# CoUI Drawer

## Overview

Drawer components provide sliding overlay panels from screen edges. Used for navigation menus, settings panels, and bottom sheets. Both Flutter and Web implementations support left, right, top, and bottom positions with backdrop overlays and smooth animations.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Show a Drawer

Use the overlay system to show drawers:

```dart
showDrawer(
  context: context,
  position: DrawerPosition.left,
  builder: (context, extraSize, padding, size, stackIndex) {
    return Container(
      width: 300,
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Drawer Title').bold.large,
          Gap.v(16),
          const Text('Drawer content goes here'),
          const Spacer(),
          PrimaryButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  },
)
```

### DrawerPosition

```dart
DrawerPosition.left    // Slide from left
DrawerPosition.right   // Slide from right
DrawerPosition.top     // Slide from top
DrawerPosition.bottom  // Slide from bottom (sheet behavior)
```

### Bottom Sheet

```dart
showDrawer(
  context: context,
  position: DrawerPosition.bottom,
  builder: (context, extraSize, padding, size, stackIndex) {
    return Container(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text('Sheet Title').bold.large,
          Gap.v(16),
          const Text('Sheet content'),
          Gap.v(24),
          SizedBox(
            width: double.infinity,
            child: PrimaryButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Done'),
            ),
          ),
        ],
      ),
    );
  },
)
```

### DrawerTheme

```dart
const DrawerTheme(
  surfaceOpacity: 0.9,
  surfaceBlur: 10.0,
  barrierColor: Colors.black54,
  showDragHandle: true,
)
```

### DrawerBuilder Signature

```dart
typedef DrawerBuilder = Widget Function(
  BuildContext context,
  Size extraSize,      // Additional size from transforms
  EdgeInsets padding,  // Safe area padding
  Size size,           // Total size constraints
  int stackIndex,      // Stack position (for layered drawers)
);
```

### Features

- **Swipe to dismiss**: Drag the drawer to close it
- **Drag handle**: Optional visual handle for dragging
- **Stacked drawers**: Multiple drawers can layer on top
- **Barrier**: Configurable backdrop behind drawer
- **Animation**: Smooth slide-in/out transitions (350ms default)
- **Safe area**: Respects device safe areas

### Settings Drawer Pattern (Flutter)

```dart
showDrawer(
  context: context,
  position: DrawerPosition.right,
  builder: (context, extraSize, padding, size, stackIndex) {
    return Container(
      width: 320,
      padding: EdgeInsets.only(
        top: padding.top + 16,
        bottom: padding.bottom + 16,
        left: 16,
        right: 16,
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Settings').bold.large,
              IconButton.ghost(
                icon: const Icon(Icons.close),
                onPressed: () => Navigator.pop(context),
                density: ButtonDensity.icon,
              ),
            ],
          ),
          Gap.v(24),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Notifications'),
              Toggle(value: true, onChanged: (v) {}),
            ],
          ),
          const Divider(),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Dark Mode'),
              Toggle(value: false, onChanged: (v) {}),
            ],
          ),
        ],
      ),
    );
  },
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Drawer(
  open: true,
  onClose: () => setState(() => isDrawerOpen = false),
  child: div(
    [Component.text('Drawer content here')],
  ),
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `open` | `bool` | required | Whether drawer is visible |
| `onClose` | `DrawerCloseCallback?` | `null` | Close callback |
| `side` | `DrawerSide` | `DrawerSide.left` | Position |
| `child` | `Component?` | `null` | Drawer content |

### DrawerSide Enum

| Value | Description | CSS |
|-------|-------------|-----|
| `left` | Left panel, 3/4 width, max-w-sm | `inset-y-0 left-0` |
| `right` | Right panel, 3/4 width, max-w-sm | `inset-y-0 right-0` |
| `top` | Top panel, full width | `inset-x-0 top-0` |
| `bottom` | Bottom panel, full width | `inset-x-0 bottom-0` |

### Rendered Structure

When `open` is `true`:
1. Backdrop overlay with blur effect
2. Drawer panel with header (title + close button) and content area
3. `role="dialog"` and `aria-modal="true"` for accessibility

When `open` is `false`: renders `Component.empty()`.

### Navigation Drawer Example

```dart
class DrawerExample extends StatefulComponent {
  @override
  State<DrawerExample> createState() => _DrawerExampleState();
}

class _DrawerExampleState extends State<DrawerExample> {
  bool isOpen = false;

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield div(
      [
        Button.outline(
          onPressed: () => setState(() => isOpen = true),
          child: Component.text('Open Drawer'),
        ),
        Drawer(
          open: isOpen,
          side: DrawerSide.left,
          onClose: () => setState(() => isOpen = false),
          child: div(
            [
              Menu(
                [
                  MenuTitle([Component.text('Navigation')]),
                  MenuItem([Component.text('Home')], href: '/'),
                  MenuItem([Component.text('About')], href: '/about'),
                  MenuItem([Component.text('Contact')], href: '/contact'),
                ],
                ariaLabel: 'Drawer navigation',
              ),
            ],
          ),
        ),
      ],
    );
  }
}
```

### Settings Drawer Pattern (Web)

```dart
Drawer(
  open: isOpen,
  side: DrawerSide.right,
  onClose: () => setState(() => isOpen = false),
  child: div(
    [
      Component.element(
        tag: 'h3',
        classes: 'text-lg font-semibold mb-4',
        children: [Component.text('Settings')],
      ),
      SwitchField(
        label: 'Dark mode',
        checked: isDark,
        onChanged: (v) => setState(() => isDark = v),
      ),
      SwitchField(
        label: 'Notifications',
        checked: notifs,
        onChanged: (v) => setState(() => notifs = v),
      ),
    ],
    classes: 'space-y-4',
  ),
)
```

### Bottom Sheet Style (Web)

```dart
Drawer(
  open: isOpen,
  side: DrawerSide.bottom,
  onClose: () => setState(() => isOpen = false),
  child: div(
    [
      Component.text('Bottom sheet content'),
      Button.primary(
        onPressed: () => setState(() => isOpen = false),
        block: true,
        child: Component.text('Close'),
      ),
    ],
    classes: 'space-y-4',
  ),
)
```

## Common Patterns

### Position Mapping

| Position | Flutter | Web |
|----------|---------|-----|
| Left | `DrawerPosition.left` | `DrawerSide.left` |
| Right | `DrawerPosition.right` | `DrawerSide.right` |
| Top | `DrawerPosition.top` | `DrawerSide.top` |
| Bottom | `DrawerPosition.bottom` | `DrawerSide.bottom` |

### API Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Show method | `showDrawer()` function | `Drawer()` component with `open` bool |
| Close method | `Navigator.pop(context)` | Set `open = false` via callback |
| Position enum | `DrawerPosition` | `DrawerSide` |
| Content param | `builder` callback | `child` component |
| Backdrop | `barrierColor` in theme | Built-in blur overlay |
| Accessibility | Platform native | `role="dialog"`, `aria-modal="true"` |

### Typical Use Cases

- **Navigation menu**: Left drawer with menu items (default position)
- **Settings panel**: Right drawer with toggles and form controls
- **Bottom sheet**: Bottom drawer for confirmations or quick actions
- **Top panel**: Top drawer for notifications or alerts

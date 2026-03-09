---
name: coui-tooltip
description: Activate when adding hover tooltips, contextual help text, info popups on hover, or hint overlays using Tooltip, TooltipContainer, or InstantTooltip in coui_flutter or coui_web.
---

# CoUI Tooltip

## Overview

The Tooltip component provides contextual information on hover. In Flutter it uses a builder pattern with `TooltipContainer` for styled content and supports positioning, animation delays, and theming. In Web it uses a simpler string-based API with CSS `group-hover` transitions.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Tooltip

```dart
Tooltip(
  tooltip: (context) => TooltipContainer(
    child: const Text('Save your changes'),
  ),
  child: IconButton.primary(
    icon: const Icon(Icons.save),
    onPressed: () {},
  ),
)
```

### Key Parameters

#### Tooltip

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Widget` | required | Trigger widget |
| `tooltip` | `WidgetBuilder` | required | Tooltip content builder |
| `alignment` | `AlignmentGeometry` | `topCenter` | Tooltip position |
| `anchorAlignment` | `AlignmentGeometry` | `bottomCenter` | Anchor point |
| `waitDuration` | `Duration` | 500ms | Delay before showing |
| `showDuration` | `Duration` | 200ms | Animation duration |
| `minDuration` | `Duration` | 0ms | Min display time |

### TooltipContainer

Styled container for tooltip content:

```dart
TooltipContainer(
  child: const Text('Tooltip text'),
)

// Custom styling
TooltipContainer(
  backgroundColor: Colors.blue,
  borderRadius: BorderRadius.circular(4),
  padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  child: const Text('Custom tooltip'),
)
```

#### TooltipContainer Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Tooltip content |
| `backgroundColor` | `Color?` | Background (default: primary) |
| `borderRadius` | `BorderRadiusGeometry?` | Corner radius |
| `padding` | `EdgeInsetsGeometry?` | Internal padding |
| `surfaceBlur` | `double?` | Blur effect |
| `surfaceOpacity` | `double?` | Opacity effect |

### Positioning

```dart
// Above the widget (default)
Tooltip(
  alignment: Alignment.topCenter,
  anchorAlignment: Alignment.bottomCenter,
  tooltip: (context) => TooltipContainer(child: const Text('Above')),
  child: myWidget,
)

// Below the widget
Tooltip(
  alignment: Alignment.bottomCenter,
  anchorAlignment: Alignment.topCenter,
  tooltip: (context) => TooltipContainer(child: const Text('Below')),
  child: myWidget,
)

// To the right
Tooltip(
  alignment: Alignment.centerRight,
  anchorAlignment: Alignment.centerLeft,
  tooltip: (context) => TooltipContainer(child: const Text('Right')),
  child: myWidget,
)
```

### InstantTooltip

Shows immediately on hover without delay:

```dart
InstantTooltip(
  tooltipBuilder: (context) => TooltipContainer(
    child: const Text('Instant tooltip'),
  ),
  child: const Icon(Icons.info),
)
```

### TooltipTheme

Theme-level customization:

```dart
const TooltipTheme(
  backgroundColor: Colors.black87,
  borderRadius: BorderRadius.circular(4),
  padding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  surfaceBlur: 10.0,
  surfaceOpacity: 0.9,
)
```

### Icon Button with Tooltip Pattern

```dart
Tooltip(
  tooltip: (context) => TooltipContainer(
    child: const Text('Delete this item'),
  ),
  child: IconButton.destructive(
    icon: const Icon(Icons.delete),
    onPressed: () {},
    density: ButtonDensity.icon,
  ),
)
```

### Toolbar with Tooltips Pattern

```dart
Row(
  children: [
    Tooltip(
      tooltip: (context) => TooltipContainer(child: const Text('Bold')),
      child: IconButton.ghost(
        icon: const Icon(Icons.format_bold),
        onPressed: () {},
        density: ButtonDensity.icon,
      ),
    ),
    Tooltip(
      tooltip: (context) => TooltipContainer(child: const Text('Italic')),
      child: IconButton.ghost(
        icon: const Icon(Icons.format_italic),
        onPressed: () {},
        density: ButtonDensity.icon,
      ),
    ),
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
Tooltip(
  content: 'Add to library',
  triggerChild: Button.outline(child: Component.text('+')),
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `content` | `String` | required | Tooltip text |
| `triggerChild` | `Component` | required | Element that triggers tooltip |

### How It Works

The Tooltip wraps `triggerChild` and a tooltip `<span>` in a container `<div>`. The tooltip text appears on hover using CSS `group-hover` visibility transitions.

Rendered structure:
```html
<div class="relative inline-block">
  <!-- triggerChild -->
  <span class="... invisible group-hover:visible opacity-0 group-hover:opacity-100 transition-opacity">
    Tooltip text
  </span>
</div>
```

### Button Tooltip

```dart
Tooltip(
  content: 'Delete this item',
  triggerChild: Button.destructive(
    onPressed: () => handleDelete(),
    child: Component.text('Delete'),
  ),
)
```

### Icon Tooltip

```dart
Tooltip(
  content: 'More information',
  triggerChild: span(
    [Component.text('?')],
    classes: 'inline-flex items-center justify-center w-5 h-5 rounded-full border text-xs cursor-help',
  ),
)
```

### Custom Styled

```dart
Tooltip(
  content: 'Custom tooltip',
  classes: 'bg-primary text-primary-foreground',
  triggerChild: Component.text('Hover me'),
)
```

### Toolbar with Tooltips Pattern

```dart
div(
  [
    Tooltip(
      content: 'Bold',
      triggerChild: Button.ghost(
        shape: ButtonShape.square,
        size: CoButtonSize.sm,
        child: Component.text('B'),
      ),
    ),
    Tooltip(
      content: 'Italic',
      triggerChild: Button.ghost(
        shape: ButtonShape.square,
        size: CoButtonSize.sm,
        child: Component.text('I'),
      ),
    ),
    Tooltip(
      content: 'Underline',
      triggerChild: Button.ghost(
        shape: ButtonShape.square,
        size: CoButtonSize.sm,
        child: Component.text('U'),
      ),
    ),
  ],
  classes: 'flex gap-1',
)
```

## Common Patterns

| Aspect | Flutter | Web |
|--------|---------|-----|
| Tooltip content | `WidgetBuilder` (rich content) | `String` (text only) |
| Trigger parameter | `child` | `triggerChild` |
| Positioning | `alignment` / `anchorAlignment` | CSS-based (fixed above) |
| Delay control | `waitDuration`, `showDuration` | CSS transition (automatic) |
| Instant variant | `InstantTooltip` widget | N/A |
| Theming | `TooltipTheme` | `classes` parameter |
| Styled container | `TooltipContainer` | Built-in `<span>` |

Both platforms share the same `Tooltip` class name. Choose the import based on your target platform. For toolbar patterns, wrap each action button individually with a Tooltip for per-button hints.

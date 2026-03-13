---
name: coui-button
description: Activate when creating buttons, handling click/tap events, or choosing button variants (PrimaryButton, SecondaryButton, OutlineButton, GhostButton, DestructiveButton, LinkButton, TextButton, IconButton, ButtonGroup) in CoUI Flutter or CoUI Web.
---

# CoUI Button

## Overview

Button components provide clickable actions across CoUI Flutter and CoUI Web. Both platforms share the same variant set (primary, secondary, outline, ghost, destructive, link, text) with platform-specific APIs: Flutter uses dedicated widget classes (e.g., `PrimaryButton`), while Web uses named constructors on a single `Button` class (e.g., `Button.primary`).

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Button Variants

#### PrimaryButton
Main call-to-action button with filled background.

```dart
PrimaryButton(
  onPressed: () {},
  child: const Text('Submit'),
)
```

#### SecondaryButton
Secondary action button.

```dart
SecondaryButton(
  onPressed: () {},
  child: const Text('Secondary'),
)
```

#### OutlineButton
Button with border, no fill.

```dart
OutlineButton(
  onPressed: () {},
  child: const Text('Outlined'),
)
```

#### GhostButton
Transparent background button.

```dart
GhostButton(
  onPressed: () {},
  child: const Text('Ghost'),
)
```

#### DestructiveButton
Danger/warning action button (red themed).

```dart
DestructiveButton(
  onPressed: () {},
  child: const Text('Delete'),
)
```

#### LinkButton
Link-styled text button.

```dart
LinkButton(
  onPressed: () {},
  child: const Text('Learn more'),
)
```

#### TextButton
Plain text button.

```dart
TextButton(
  onPressed: () {},
  child: const Text('Text'),
)
```

### Flutter Parameters

All button variants share these parameters:

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Button content, usually `Text` |
| `onPressed` | `VoidCallback?` | Tap handler. `null` = disabled |
| `leading` | `Widget?` | Widget before text (icon) |
| `trailing` | `Widget?` | Widget after text (icon) |
| `isLoading` | `bool` | Shows spinner and disables clicks (default: false) |
| `enabled` | `bool` | Enable/disable button |
| `density` | `ButtonDensity?` | Size density variant |
| `style` | `ButtonStyle?` | Custom styling |

### ButtonDensity

Controls the button's height and padding:

```dart
enum ButtonDensity {
  normal,      // Default size
  comfortable, // Slightly larger
  dense,       // Reduced padding
  compact,     // Minimal padding
  icon,        // Square icon-only size
}
```

### Loading State

```dart
PrimaryButton(
  isLoading: true,
  onPressed: () {},
  child: const Text('Saving...'),
)
```

When `isLoading` is true, the button displays a spinner and ignores click events.

### Icons with Buttons

```dart
// Leading icon
PrimaryButton(
  onPressed: () {},
  leading: const Icon(Icons.save),
  child: const Text('Save'),
)

// Trailing icon
SecondaryButton(
  onPressed: () {},
  trailing: const Icon(Icons.arrow_forward),
  child: const Text('Next'),
)
```

### IconButton

Icon-only button with variant constructors:

```dart
IconButton.primary(
  icon: const Icon(Icons.add),
  onPressed: () {},
  density: ButtonDensity.icon,
)

IconButton.ghost(
  icon: const Icon(Icons.more_vert),
  onPressed: () {},
  density: ButtonDensity.icon,
)

IconButton.destructive(
  icon: const Icon(Icons.delete),
  onPressed: () {},
  density: ButtonDensity.icon,
)

IconButton.text(
  icon: const Icon(Icons.copy),
  onPressed: () {},
  density: ButtonDensity.compact,
)
```

### Disabled State (Flutter)

Omit `onPressed` or pass `null`:

```dart
const PrimaryButton(child: Text('Disabled'))

PrimaryButton(
  onPressed: null,
  child: const Text('Also Disabled'),
)
```

### Full Width Button

```dart
// Using expanded parameter
PrimaryButton(
  expanded: true,
  onPressed: () {},
  child: const Text('Full Width'),
)

// Or using SizedBox
SizedBox(
  width: double.infinity,
  child: PrimaryButton(
    onPressed: () {},
    child: const Text('Full Width'),
  ),
)
```

### ButtonGroup

Group multiple buttons together:

```dart
ButtonGroup(
  children: [
    OutlineButton(onPressed: () {}, child: const Text('Left')),
    OutlineButton(onPressed: () {}, child: const Text('Center')),
    OutlineButton(onPressed: () {}, child: const Text('Right')),
  ],
)
```

### Button Row Pattern

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.end,
  children: [
    GhostButton(
      onPressed: () => Navigator.pop(context),
      child: const Text('Cancel'),
    ),
    Gap.h(8),
    PrimaryButton(
      onPressed: () {},
      child: const Text('Confirm'),
    ),
  ],
)
```

### Form Submit (Flutter)

```dart
Column(
  children: [
    const TextField(placeholder: Text('Name')),
    Gap.v(16),
    PrimaryButton(
      onPressed: () {},
      child: const Text('Submit'),
    ),
  ],
)
```

### Delete Confirmation (Flutter)

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.end,
  children: [
    GhostButton(
      onPressed: () => Navigator.pop(context),
      child: const Text('Cancel'),
    ),
    Gap.h(8),
    DestructiveButton(
      onPressed: () {
        // delete logic
        Navigator.pop(context);
      },
      child: const Text('Delete'),
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Button Variants

Use named constructors for each variant:

```dart
Button.primary(child: Component.text('Primary'))
Button.secondary(child: Component.text('Secondary'))
Button.outline(child: Component.text('Outline'))
Button.ghost(child: Component.text('Ghost'))
Button.link(child: Component.text('Link'))
Button.text(child: Component.text('Text'))        // alias for ghost
Button.destructive(child: Component.text('Delete'))
```

Or use the default constructor with `variant` parameter:

```dart
Button(
  variant: ButtonVariant.primary,
  child: Component.text('Primary'),
)
```

### Web Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Component` | required | Button content |
| `onPressed` | `VoidCallback?` | `null` | Click handler |
| `enabled` | `bool` | `true` | Whether button responds to interactions |
| `leading` | `Component?` | `null` | Icon/component before content |
| `trailing` | `Component?` | `null` | Icon/component after content |
| `size` | `CoButtonSize?` | `null` | Button size (xs, sm, md, lg, xl) |
| `shape` | `ButtonShape?` | `null` | Shape (rectangle, square, circle) |
| `variant` | `ButtonVariant?` | `defaultVariant` | Visual variant |
| `htmlType` | `ButtonHtmlType?` | `button` | HTML type attribute |
| `wide` | `bool` | `false` | Fixed wide width (w-48) |
| `block` | `bool` | `false` | Full width (w-full) |
| `onHover` | `void Function(bool)?` | `null` | Hover state callback |
| `onFocus` | `void Function(bool)?` | `null` | Focus state callback |

### Sizes

```dart
Button.primary(size: CoButtonSize.xs, child: Component.text('XS'))
Button.primary(size: CoButtonSize.sm, child: Component.text('SM'))
Button.primary(size: CoButtonSize.md, child: Component.text('MD'))
Button.primary(size: CoButtonSize.lg, child: Component.text('LG'))
Button.primary(size: CoButtonSize.xl, child: Component.text('XL'))
```

### Shapes

```dart
Button.primary(shape: ButtonShape.rectangle, child: Component.text('Rect'))
Button.primary(shape: ButtonShape.square, child: Component.text('+'))
Button.primary(shape: ButtonShape.circle, child: Component.text('+'))
```

### Icons (Web)

```dart
Button.primary(
  leading: span([Component.text('>')]),
  child: Component.text('Next'),
)

Button.outline(
  trailing: span([Component.text('*')]),
  child: Component.text('Star'),
)
```

### Disabled State (Web)

```dart
Button.primary(
  enabled: false,
  child: Component.text('Disabled'),
)
```

When disabled, the button gets `disabled` and `tabindex="-1"` attributes and `aria-disabled="true"`.

### Full Width / Wide (Web)

```dart
Button.primary(
  block: true,  // Full width (w-full)
  child: Component.text('Full Width'),
)

Button.primary(
  wide: true,  // Fixed wide (w-48)
  child: Component.text('Wide'),
)
```

### HTML Type

```dart
Button.primary(
  htmlType: ButtonHtmlType.submit,
  child: Component.text('Submit Form'),
)
```

Available: `ButtonHtmlType.button`, `ButtonHtmlType.submit`, `ButtonHtmlType.reset`.

### Event Handling (Web)

```dart
Button.primary(
  onPressed: () => handleClick(),
  onHover: (isHovered) => handleHover(isHovered),
  onFocus: (isFocused) => handleFocus(isFocused),
  child: Component.text('Interactive'),
)
```

### Custom Tag

Render as a different HTML element (e.g., anchor):

```dart
Button.primary(
  tag: 'a',
  attributes: {'href': '/page'},
  child: Component.text('Link Button'),
)
```

When `tag` is not `'button'`, a `role="button"` attribute is automatically added.

## Common Patterns

### Shared Variants

Both platforms support the same seven variants:

| Variant | Flutter Class | Web Constructor |
|---------|--------------|-----------------|
| Primary | `PrimaryButton` | `Button.primary` |
| Secondary | `SecondaryButton` | `Button.secondary` |
| Outline | `OutlineButton` | `Button.outline` |
| Ghost | `GhostButton` | `Button.ghost` |
| Destructive | `DestructiveButton` | `Button.destructive` |
| Link | `LinkButton` | `Button.link` |
| Text | `TextButton` | `Button.text` |

### Shared Parameters

Both platforms support `child`, `onPressed`, `leading`, and `trailing` with the same semantics. Disabled state is achieved by omitting/nullifying `onPressed` (Flutter) or setting `enabled: false` (Web).

### Content Model

- **Flutter**: `child` is a `Widget` (typically `Text(...)`)
- **Web**: `child` is a `Component` (typically `Component.text(...)`)

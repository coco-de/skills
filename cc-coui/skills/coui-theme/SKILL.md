---
name: coui-theme
description: Activate when configuring CoUI theming across Flutter or Web — ThemeData, ColorScheme, Typography, RadiusScale, design tokens, light/dark mode, DaisyUI themes, ThemeController components, CSS variables, or adaptive scaling.
---

# CoUI Theme

## Overview

CoUI provides a unified theming system across Flutter and Web platforms. Both share DaisyUI-inspired semantic color tokens and radius scales, but differ in implementation: Flutter uses a `Theme` widget with `ThemeData`, while Web uses DaisyUI CSS themes with `ThemeController` components.

## Flutter (coui_flutter)

### Theme Widget

coui_flutter uses its own `Theme` widget (not Flutter's `ThemeData`). Wrap your app:

```dart
import 'package:coui_flutter/coui_flutter.dart';

Theme(
  data: const ThemeData(),  // light theme
  child: MyApp(),
)

Theme(
  data: const ThemeData.dark(),  // dark theme
  child: MyApp(),
)
```

### Accessing Theme

```dart
final theme = Theme.of(context);
final colors = theme.colorScheme;
final typo = theme.typography;
final scaling = theme.scaling;
```

### ThemeData Constructor

```dart
const ThemeData({
  ColorScheme colorScheme = ColorSchemes.lightDefaultColor,
  ComponentThemeData? componentTheme,
  IconThemeProperties iconTheme = const IconThemeProperties(),
  TargetPlatform? platform,
  RadiusScale radiusScale = const RadiusScale.daisyUI(),
  double scaling = 1,
  double? surfaceBlur,
  double? surfaceOpacity,
  Typography typography = const Typography.geist(),
})
```

### ColorScheme

Access semantic colors:

```dart
final cs = theme.colorScheme;

cs.primary        // Primary brand color
cs.primaryContent // Text on primary
cs.neutral        // Neutral/border color
cs.base100        // Background level 1
cs.base200        // Background level 2 (muted text)
cs.base300        // Background level 3
cs.baseContent    // Default text color
cs.brightness     // Brightness.light or .dark
```

Built-in schemes:
- `ColorSchemes.lightDefaultColor` (default light)
- `ColorSchemes.darkDefaultColor` (default dark)

### Typography

```dart
const ThemeData(
  typography: const Typography.geist(),  // default
)
```

Access text styles via extensions:
```dart
theme.typography.xs    // extra small
theme.typography.sm    // small
theme.typography.base  // base
theme.typography.lg    // large
```

Or use widget extensions:
```dart
const Text('Hello').xs
const Text('Hello').sm
const Text('Hello').lg
```

### RadiusScale (DaisyUI Semantic)

```dart
theme.radiusBox       // cards, dialogs, panels
theme.radiusField     // inputs, form elements
theme.radiusSelector  // buttons, interactive elements

theme.borderRadiusBox
theme.borderRadiusField
theme.borderRadiusSelector
```

### Scaling

```dart
theme.scaling  // default 1.0
```

All components respect `theme.scaling` for consistent sizing across platforms.

### AdaptiveScaling

Automatically scale for mobile/desktop:

```dart
AdaptiveScaler(
  scaling: AdaptiveScaling.mobile,  // 1.25x
  child: MyWidget(),
)

// Or use defaults based on platform
AdaptiveScaler(
  scaling: AdaptiveScaler.defaultScalingOf(context),
  child: MyWidget(),
)
```

### AnimatedTheme

Smoothly transition between themes:

```dart
AnimatedTheme(
  data: isDark ? const ThemeData.dark() : const ThemeData(),
  duration: const Duration(milliseconds: 300),
  child: MyApp(),
)
```

### ComponentTheme

Apply component-level theme overrides:

```dart
Theme(
  data: ThemeData(
    componentTheme: ComponentThemeData(
      // Override specific component themes
    ),
  ),
  child: MyApp(),
)
```

### IconThemeProperties

Control icon sizes at theme level:

```dart
theme.iconTheme.small   // IconThemeData(size: 16)
theme.iconTheme.medium  // IconThemeData(size: 20)
theme.iconTheme.large   // IconThemeData(size: 24)
theme.iconTheme.xLarge  // IconThemeData(size: 32)
```

### ThemeMode

```dart
enum ThemeMode { dark, light, system }
```

### copyWith Pattern

```dart
final customTheme = theme.copyWith(
  colorScheme: () => myColorScheme,
  typography: () => const Typography.geist(),
  scaling: () => 1.25,
);
```

Note: `copyWith` uses `ValueGetter` lambdas (not direct values).

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### CoTheme Enum

Available themes via the `CoTheme` enum:

```dart
enum CoTheme {
  light, dark, system,
  cupcake, bumblebee, emerald, corporate, synthwave, retro,
  cyberpunk, valentine, halloween, garden, forest, aqua,
  lofi, pastel, fantasy, wireframe, black, luxury, dracula,
  cmyk, autumn, business, acid, lemonade, night, coffee,
  winter, dim, nord, sunset,
}
```

Each theme value maps to a DaisyUI theme name string via `CoTheme.value`.

### ThemeControllerCheckbox

A toggle/checkbox for switching between two themes:

```dart
ThemeControllerCheckbox(
  value: CoTheme.dark,
  toggleTheme: CoTheme.light,
  isChecked: false,
  onThemeChanged: (theme) => print('Theme: ${theme.value}'),
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `CoTheme` | required | Primary theme when checked |
| `toggleTheme` | `CoTheme?` | `null` | Alternative theme when unchecked (defaults to light) |
| `isChecked` | `bool` | `false` | Whether the controller is checked |
| `onThemeChanged` | `ThemeChangedCallback?` | `null` | Callback on theme change |
| `asToggle` | `bool` | `true` | Render as toggle switch vs checkbox |
| `name` | `String?` | `null` | HTML name attribute |

As toggle switch (default):

```dart
ThemeControllerCheckbox(
  value: CoTheme.dark,
  toggleTheme: CoTheme.light,
  asToggle: true,  // default
  onThemeChanged: (theme) {},
)
```

As checkbox:

```dart
ThemeControllerCheckbox(
  value: CoTheme.dark,
  toggleTheme: CoTheme.light,
  asToggle: false,
  onThemeChanged: (theme) {},
)
```

### ThemeControllerRadio

A radio button for selecting one theme from a group:

```dart
ThemeControllerRadio(
  value: CoTheme.dark,
  name: 'theme-group',
  isChecked: currentTheme == CoTheme.dark,
  onThemeChanged: (theme) => print('Theme: ${theme.value}'),
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `CoTheme` | required | Theme to activate when selected |
| `name` | `String` | required | Radio group name |
| `isChecked` | `bool` | `false` | Whether this radio is checked |
| `onThemeChanged` | `ThemeChangedCallback?` | `null` | Callback on theme change |
| `asButton` | `bool` | `false` | Render as button style |

Theme radio group example:

```dart
div(
  [
    ThemeControllerRadio(
      value: CoTheme.light,
      name: 'theme-selector',
      isChecked: true,
      onThemeChanged: handleThemeChange,
    ),
    ThemeControllerRadio(
      value: CoTheme.dark,
      name: 'theme-selector',
      onThemeChanged: handleThemeChange,
    ),
    ThemeControllerRadio(
      value: CoTheme.cupcake,
      name: 'theme-selector',
      onThemeChanged: handleThemeChange,
    ),
  ],
  classes: 'flex gap-2',
)
```

As button style:

```dart
ThemeControllerRadio(
  value: CoTheme.retro,
  name: 'theme-buttons',
  asButton: true,
  onThemeChanged: (theme) {},
)
```

### HTML Theme Integration

DaisyUI themes work via the `data-theme` attribute on the HTML element. The ThemeController components set `data-toggle-theme` and `data-set-theme` attributes that integrate with DaisyUI's theme switching JavaScript.

Ensure your HTML root element has:

```html
<html data-theme="light">
```

### Theme CSS Variables

DaisyUI themes define CSS variables like:
- `--p` (primary), `--pf` (primary focus), `--pc` (primary content)
- `--s` (secondary), `--a` (accent), `--n` (neutral)
- `--b1` (base-100), `--b2` (base-200), `--b3` (base-300)
- `--bc` (base-content)

Use Tailwind classes that reference these: `bg-primary`, `text-primary-foreground`, `bg-base-100`, etc.

## Common Patterns

### Semantic Color Tokens (shared across platforms)

Both Flutter and Web use DaisyUI-inspired semantic color tokens:

| Token | Flutter (`ColorScheme`) | Web (CSS Variable) | Purpose |
|-------|------------------------|-------------------|---------|
| primary | `cs.primary` | `--p` / `bg-primary` | Brand color |
| primary-content | `cs.primaryContent` | `--pc` / `text-primary-content` | Text on primary |
| neutral | `cs.neutral` | `--n` / `bg-neutral` | Neutral/border |
| base-100 | `cs.base100` | `--b1` / `bg-base-100` | Background level 1 |
| base-200 | `cs.base200` | `--b2` / `bg-base-200` | Background level 2 |
| base-300 | `cs.base300` | `--b3` / `bg-base-300` | Background level 3 |
| base-content | `cs.baseContent` | `--bc` / `text-base-content` | Default text |

### Light/Dark Mode

Both platforms support light, dark, and system modes:

```dart
// Flutter
Theme(data: const ThemeData(), child: app)       // light
Theme(data: const ThemeData.dark(), child: app)   // dark

// Web
ThemeControllerCheckbox(value: CoTheme.dark, toggleTheme: CoTheme.light)
```

### DaisyUI Radius Scale

Both platforms share the DaisyUI semantic radius scale with three levels:
- **Box** — cards, dialogs, panels
- **Field** — inputs, form elements
- **Selector** — buttons, interactive elements

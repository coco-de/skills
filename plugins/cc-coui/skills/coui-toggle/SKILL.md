---
name: coui-toggle
description: Activate when creating on/off switches, toggle controls, or controlled toggles in CoUI Flutter or Web using Toggle, ControlledToggle, ToggleController, or Switch.
---

# CoUI Toggle

## Overview

On/off switch controls with optional labels, controller support, and theming.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Toggle

```dart
bool isEnabled = false;

Toggle(
  value: isEnabled,
  onChanged: (value) {
    setState(() => isEnabled = value);
  },
)
```

### Toggle with Labels

```dart
Toggle(
  value: isEnabled,
  onChanged: (value) => setState(() => isEnabled = value),
  leading: const Text('Dark Mode'),
)

Toggle(
  value: isEnabled,
  onChanged: (value) => setState(() => isEnabled = value),
  trailing: const Text('Notifications'),
)
```

### Switch (Alias)

`Switch` is an alias for `Toggle`:

```dart
Switch(
  value: isEnabled,
  onChanged: (value) => setState(() => isEnabled = value),
)
```

### ControlledToggle

Higher-level toggle with built-in state management:

#### With Controller

```dart
final controller = ToggleController(false);

ControlledToggle(
  controller: controller,
  trailing: const Text('Auto-save'),
)

// Programmatic control
controller.toggle();
controller.value = true;
```

#### With Callback

```dart
ControlledToggle(
  initialValue: false,
  onChanged: (value) {
    print('Toggled: $value');
  },
  trailing: const Text('Notifications'),
)
```

### ToggleController

Reactive controller extending `ValueNotifier<bool>`:

```dart
final controller = ToggleController(false);

// Toggle
controller.toggle();  // false -> true -> false

// Set directly
controller.value = true;

// Listen
controller.addListener(() {
  print('Value: ${controller.value}');
});
```

### Disabled Toggle

```dart
Toggle(
  value: true,
  onChanged: null,
  enabled: false,
  trailing: const Text('Locked'),
)
```

### Key Parameters

#### Toggle

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `bool` (required) | Current state |
| `onChanged` | `ValueChanged<bool>?` (required) | Change callback |
| `leading` | `Widget?` | Widget before toggle |
| `trailing` | `Widget?` | Widget after toggle |
| `enabled` | `bool?` | Enable/disable |
| `activeColor` | `Color?` | Track color when on |
| `inactiveColor` | `Color?` | Track color when off |
| `activeThumbColor` | `Color?` | Thumb color when on |
| `inactiveThumbColor` | `Color?` | Thumb color when off |
| `gap` | `double?` | Spacing to labels |
| `borderRadius` | `BorderRadiusGeometry?` | Track corner radius |

### ToggleTheme

```dart
const ToggleTheme(
  activeColor: Colors.green,
  inactiveColor: Colors.grey,
  activeThumbColor: Colors.white,
  inactiveThumbColor: Colors.white,
  disabledColor: Colors.grey,
  disabledThumbColor: Colors.white,
  disabledOpacity: 0.5,
  gap: 8.0,
  borderRadius: BorderRadius.circular(12),
)
```

### Settings Page Pattern

```dart
Card(
  child: Column(
    children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text('Notifications'),
          Toggle(
            value: notifications,
            onChanged: (v) => setState(() => notifications = v),
          ),
        ],
      ),
      const Divider(),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text('Dark Mode'),
          Toggle(
            value: darkMode,
            onChanged: (v) => setState(() => darkMode = v),
          ),
        ],
      ),
      const Divider(),
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text('Auto-save'),
          Toggle(
            value: autoSave,
            onChanged: (v) => setState(() => autoSave = v),
          ),
        ],
      ),
    ],
  ),
)
```

### Feature Toggle Pattern

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Features').lg.bold,
    Gap.v(12),
    Toggle(
      value: feature1,
      onChanged: (v) => setState(() => feature1 = v),
      leading: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.speed, size: 20),
          Gap.h(8),
          const Text('Performance Mode'),
        ],
      ),
    ),
    Gap.v(8),
    Toggle(
      value: feature2,
      onChanged: (v) => setState(() => feature2 = v),
      leading: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Icon(Icons.analytics, size: 20),
          Gap.h(8),
          const Text('Analytics'),
        ],
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

### Basic Toggle

```dart
Toggle(
  checked: isDarkMode,
  onChanged: (checked) => setState(() => isDarkMode = checked),
)
```

### With Label

```dart
Toggle(
  checked: isNotificationEnabled,
  onChanged: (checked) => handleNotificationToggle(checked),
  label: 'Notifications',
)
```

### Sizes

```dart
Toggle(checked: value, onChanged: handler, size: ToggleSize.sm)
Toggle(checked: value, onChanged: handler, size: ToggleSize.md)  // default
Toggle(checked: value, onChanged: handler, size: ToggleSize.lg)
```

### Disabled

```dart
Toggle(
  checked: true,
  disabled: true,
)
```

### Web Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `checked` | `bool` | required | Current state |
| `onChanged` | `ToggleCallback?` | `null` | State change callback |
| `label` | `String?` | `null` | Label text |
| `size` | `ToggleSize` | `md` | Toggle size (sm/md/lg) |
| `disabled` | `bool` | `false` | Disable toggle |

### Accessibility

Toggle renders as a `<button>` with `role="switch"` and `aria-checked` attributes. Focus indicator uses `focus-visible:ring-2` CSS.

### Settings List (Web)

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Settings')),
    ),
    CardContent(
      children: [
        SwitchField(
          label: 'Dark mode',
          checked: isDarkMode,
          onChanged: (v) => setState(() => isDarkMode = v),
        ),
        SwitchField(
          label: 'Push notifications',
          description: 'Receive push notifications on your device.',
          checked: pushEnabled,
          onChanged: (v) => setState(() => pushEnabled = v),
        ),
      ],
    ),
  ],
)
```

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| State property | `value: bool` | `checked: bool` |
| Disabled property | `enabled: bool` | `disabled: bool` |
| Callback type | `ValueChanged<bool>?` | `ToggleCallback` |
| State management | `ToggleController` | Props-based |
| Animation | 100ms easeInOut | CSS transition |
| ARIA support | Flutter semantics | `role="switch"` |
| Form integration | `FormValueSupplier` mixin | `SwitchField` component |

### Shared Concepts

- Use `Toggle` for basic on/off, `ControlledToggle` for self-managed state (Flutter).
- `Switch` is an alias for `Toggle` in Flutter — use whichever reads better.
- Use `ToggleController` for programmatic control and listening (Flutter only).
- Always provide a label for accessibility on both platforms.

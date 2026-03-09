---
name: coui-checkbox
description: Activate when creating checkboxes, tri-state checkboxes, controlled checkboxes, radio buttons, toggle switches, or switch fields using Checkbox, ControlledCheckbox, CheckboxController, CheckboxState, Radio, RadioGroup, Toggle, SwitchField in CoUI Flutter or Web.
---

# CoUI Checkbox

## Overview

Checkbox components for boolean and selection inputs across CoUI Flutter and Web platforms. Flutter provides `Checkbox` and `ControlledCheckbox` with a `CheckboxController` for reactive state management. Web provides `Checkbox`, `Radio`, `RadioGroup`, `Toggle`, and `SwitchField` for HTML-based form inputs with accessibility attributes.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Checkbox

```dart
Checkbox(
  state: isChecked ? CheckboxState.checked : CheckboxState.unchecked,
  onChanged: (state) {
    setState(() {
      isChecked = state == CheckboxState.checked;
    });
  },
  trailing: const Text('Accept terms'),
)
```

### CheckboxState

```dart
enum CheckboxState {
  checked,       // Checkmark shown
  indeterminate, // Dash/square shown
  unchecked,     // Empty box
}
```

### Checkbox Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `state` | `CheckboxState` (required) | Current state |
| `onChanged` | `ValueChanged<CheckboxState>?` (required) | State change callback |
| `leading` | `Widget?` | Widget before checkbox |
| `trailing` | `Widget?` | Widget after checkbox |
| `tristate` | `bool` | Enable indeterminate state (default: false) |
| `enabled` | `bool?` | Enable/disable |
| `size` | `double?` | Checkbox size |
| `gap` | `double?` | Spacing to leading/trailing |
| `activeColor` | `Color?` | Checked background color |
| `borderColor` | `Color?` | Unchecked border color |
| `borderRadius` | `BorderRadiusGeometry?` | Corner radius |

### ControlledCheckbox

Higher-level checkbox with built-in state management:

#### With Controller

```dart
final controller = CheckboxController(CheckboxState.unchecked);

ControlledCheckbox(
  controller: controller,
  trailing: const Text('Enable feature'),
)

// Programmatic control
controller.check();
controller.uncheck();
controller.toggle();
controller.indeterminate();

// Read state
controller.isChecked;
controller.isUnchecked;
controller.isIndeterminate;
```

#### With Callback

```dart
ControlledCheckbox(
  initialValue: CheckboxState.unchecked,
  onChanged: (state) {
    print('State: $state');
  },
  trailing: const Text('Newsletter'),
)
```

### CheckboxController

Reactive controller extending `ValueNotifier<CheckboxState>`:

```dart
final controller = CheckboxController(CheckboxState.unchecked);

// Methods
controller.check();           // -> checked
controller.uncheck();         // -> unchecked
controller.toggle();          // checked <-> unchecked
controller.indeterminate();   // -> indeterminate
controller.toggleTristate();  // checked -> unchecked -> indeterminate -> checked

// Properties
controller.isChecked;       // bool
controller.isUnchecked;     // bool
controller.isIndeterminate; // bool

// Listen to changes
controller.addListener(() {
  print('Value: ${controller.value}');
});
```

### Tri-State Checkbox

```dart
Checkbox(
  state: currentState,
  onChanged: (state) {
    setState(() => currentState = state);
  },
  tristate: true,
  trailing: const Text('Select all'),
)
```

### Terms Agreement Pattern

```dart
Column(
  children: [
    Checkbox(
      state: termsAgreed ? CheckboxState.checked : CheckboxState.unchecked,
      onChanged: (state) => setState(() {
        termsAgreed = state == CheckboxState.checked;
      }),
      trailing: const Text('I agree to the terms'),
    ),
    Gap.v(8),
    Checkbox(
      state: privacyAgreed ? CheckboxState.checked : CheckboxState.unchecked,
      onChanged: (state) => setState(() {
        privacyAgreed = state == CheckboxState.checked;
      }),
      trailing: const Text('I agree to the privacy policy'),
    ),
    Gap.v(16),
    PrimaryButton(
      onPressed: termsAgreed && privacyAgreed ? () {} : null,
      child: const Text('Continue'),
    ),
  ],
)
```

### CheckboxTheme

```dart
const CheckboxTheme(
  activeColor: Colors.blue,
  borderColor: Colors.grey,
  size: 20.0,
  gap: 12.0,
  borderRadius: BorderRadius.circular(4),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Checkbox

#### Basic Usage

```dart
Checkbox(
  checked: true,
  onChanged: (checked) => print('Checked: $checked'),
)
```

#### With Label

```dart
Checkbox(
  label: 'Accept terms and conditions',
  checked: isAccepted,
  onChanged: (checked) => setState(() => isAccepted = checked),
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `checked` | `bool` | `false` | Whether checked |
| `disabled` | `bool` | `false` | Whether disabled |
| `indeterminate` | `bool` | `false` | Mixed state |
| `label` | `String?` | `null` | Text label |
| `onChanged` | `CheckboxCallback?` | `null` | State change callback |
| `name` | `String?` | `null` | Form field name |
| `value` | `String?` | `null` | Form value |

#### Indeterminate State

```dart
Checkbox(
  indeterminate: true,
  onChanged: (checked) => handleChange(checked),
)
```

Sets `aria-checked="mixed"` for accessibility.

### Radio

#### Basic Usage

```dart
Radio(
  value: 'option1',
  groupValue: selectedValue,
  onChanged: (value) => print('Selected: $value'),
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Radio button value |
| `groupValue` | `String?` | `null` | Currently selected in group |
| `disabled` | `bool` | `false` | Whether disabled |
| `onChanged` | `RadioCallback?` | `null` | Selection callback |
| `name` | `String?` | `null` | Group identifier |

#### RadioGroup

```dart
RadioGroup(
  groupValue: selectedSize,
  onChanged: (value) => setState(() => selectedSize = value),
  children: [
    Radio(value: 'sm', groupValue: selectedSize, name: 'size'),
    Radio(value: 'md', groupValue: selectedSize, name: 'size'),
    Radio(value: 'lg', groupValue: selectedSize, name: 'size'),
  ],
)
```

#### Labeled Radio Options

```dart
div(
  [
    Component.element(
      tag: 'label',
      classes: 'flex items-center gap-2 cursor-pointer',
      children: [
        Radio(value: 'light', groupValue: theme, name: 'theme'),
        Component.text('Light'),
      ],
    ),
    Component.element(
      tag: 'label',
      classes: 'flex items-center gap-2 cursor-pointer',
      children: [
        Radio(value: 'dark', groupValue: theme, name: 'theme'),
        Component.text('Dark'),
      ],
    ),
  ],
  classes: 'space-y-2',
)
```

### Toggle

A switch-style toggle component:

```dart
Toggle(
  checked: true,
  onChanged: (checked) => print('Toggled: $checked'),
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `checked` | `bool` | `false` | Whether toggle is on |
| `disabled` | `bool` | `false` | Whether disabled |
| `onChanged` | `ToggleCallback?` | `null` | State change callback |

Toggle renders as a `<button>` with `role="switch"` and `aria-checked` attributes.

### SwitchField

A switch with integrated label and optional description:

```dart
SwitchField(
  label: 'Enable notifications',
  checked: true,
  onChanged: (value) => print('Changed: $value'),
)
```

#### With Description

```dart
SwitchField(
  label: 'Marketing emails',
  description: 'Receive emails about new products and features.',
  checked: false,
  onChanged: (value) => handleChange(value),
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Field label |
| `checked` | `bool` | `false` | Whether switch is on |
| `onChanged` | `SwitchFieldCallback?` | `null` | Change callback |
| `description` | `String?` | `null` | Helper text |
| `disabled` | `bool` | `false` | Whether disabled |

### Settings Form Example

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
        SwitchField(
          label: 'Email digest',
          description: 'Receive a weekly summary email.',
          checked: emailDigest,
          onChanged: (v) => setState(() => emailDigest = v),
        ),
      ],
    ),
  ],
)
```

## Common Patterns

### State Model Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Checked state | `CheckboxState.checked` | `checked: true` |
| Unchecked state | `CheckboxState.unchecked` | `checked: false` |
| Indeterminate | `CheckboxState.indeterminate` | `indeterminate: true` |
| Label/text | `trailing: Text(...)` | `label: 'text'` |
| Disabled | `enabled: false` | `disabled: true` |
| State callback | `ValueChanged<CheckboxState>` | `CheckboxCallback` (bool) |

### Tri-State / Indeterminate

Both platforms support a third "indeterminate" state for parent checkboxes controlling a group of children. Flutter uses `tristate: true` with a `CheckboxState` enum; Web uses a separate `indeterminate: true` boolean which maps to `aria-checked="mixed"`.

### Controller Pattern (Flutter only)

Flutter provides `CheckboxController` (extends `ValueNotifier<CheckboxState>`) for programmatic control with methods like `check()`, `uncheck()`, `toggle()`, and `toggleTristate()`. Web manages state externally via the `checked` and `indeterminate` props.

### Additional Web Components

Web extends beyond basic checkboxes with `Radio`, `RadioGroup`, `Toggle`, and `SwitchField` for common boolean/selection form patterns. These have no direct Flutter equivalents in this component set.

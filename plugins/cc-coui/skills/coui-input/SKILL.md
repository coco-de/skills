---
name: coui-input
description: Activate when creating text input fields, textareas, or handling input features (password toggle, clear, copy, paste, spinner, autocomplete) in coui_flutter or coui_web. Covers Input, TextField, TextArea, Textarea, form input events (onInput, onChange), and input validation.
---

# CoUI Input

## Overview

CoUI provides text input components for both Flutter and Web platforms. While the API surface differs between platforms, both share the concept of an `Input` component for single-line text and a `TextArea`/`Textarea` for multi-line text. Flutter uses a widget-based composable feature system; Web uses HTML-native attributes and event callbacks.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### TextField

Primary text input widget. `Input` is an alias for `TextField`.

#### Basic Usage

```dart
// Simple text field
const TextField(placeholder: Text('Enter name'))

// Using Input alias
Input(placeholder: 'Email')
```

#### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `placeholder` | `Widget?` | Placeholder widget |
| `controller` | `TextEditingController?` | Text controller |
| `onChanged` | `ValueChanged<String>?` | Change callback |
| `leading` | `Widget?` | Leading widget (icon) |
| `trailing` | `Widget?` | Trailing widget |
| `obscureText` | `bool` | Password mode |
| `enabled` | `bool?` | Enable/disable |
| `features` | `List<InputFeature>?` | Input features |
| `filled` | `bool?` | Filled background |

#### With Icons

```dart
// Search input
TextField(
  placeholder: const Text('Search...'),
  leading: const Icon(Icons.search),
  onChanged: (value) {},
)

// Password input
const TextField(
  placeholder: Text('Password'),
  leading: Icon(Icons.lock),
  obscureText: true,
)
```

#### With Controller

```dart
final controller = TextEditingController();

TextField(
  controller: controller,
  placeholder: const Text('Message'),
)

// Read value
print(controller.text);
```

### TextArea

Multi-line text input:

```dart
const TextArea(
  placeholder: Text('Enter description'),
  minLines: 3,
  maxLines: 6,
)
```

### Input Features

Extend TextField behavior with composable features.

#### Password Toggle

```dart
const TextField(
  placeholder: Text('Password'),
  obscureText: true,
  features: [
    InputPasswordToggleFeature(),
  ],
)

// Hold-to-peek mode
const TextField(
  obscureText: true,
  features: [
    InputPasswordToggleFeature(mode: PasswordPeekMode.hold),
  ],
)
```

#### Clear Button

```dart
const TextField(
  placeholder: Text('Search'),
  features: [
    InputClearFeature(),
  ],
)
```

#### Copy / Paste Buttons

```dart
const TextField(
  features: [
    InputCopyFeature(),
    InputPasteFeature(),
  ],
)
```

#### Spinner (Numeric)

```dart
const TextField(
  features: [
    InputSpinnerFeature(step: 1.0),
  ],
)
```

#### Leading/Trailing Features

```dart
const TextField(
  features: [
    InputLeadingFeature(Icon(Icons.email)),
    InputTrailingFeature(Text('.com')),
  ],
)
```

#### Hint Popup

```dart
TextField(
  features: [
    InputHintFeature(
      popupBuilder: (context) => const Text('Enter your full name'),
    ),
  ],
)
```

#### AutoComplete

```dart
TextField(
  features: [
    InputAutoCompleteFeature(
      querySuggestions: (query) => ['Apple', 'Banana', 'Cherry']
          .where((s) => s.toLowerCase().contains(query.toLowerCase())),
      child: const TextField(placeholder: Text('Fruit')),
    ),
  ],
)
```

#### Revalidate

```dart
const TextField(
  features: [
    InputRevalidateFeature(),
  ],
)
```

### Feature Position & Visibility

```dart
// Position control
const InputClearFeature(position: InputFeaturePosition.leading)
const InputCopyFeature(position: InputFeaturePosition.trailing) // default

// Visibility control
const InputClearFeature(
  visibility: InputFeatureVisibility.editing,
)
```

### TextFieldTheme

```dart
const TextFieldTheme(
  border: Border(...),
  borderRadius: BorderRadius.circular(8),
  filled: true,
  focusBorderColor: Colors.blue,
  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
)
```

### Flutter Login Form Example

```dart
Column(
  children: [
    const TextField(
      placeholder: Text('Email'),
      leading: Icon(Icons.email),
    ),
    Gap.v(16),
    const TextField(
      placeholder: Text('Password'),
      leading: Icon(Icons.lock),
      obscureText: true,
      features: [InputPasswordToggleFeature()],
    ),
    Gap.v(24),
    PrimaryButton(
      onPressed: () {},
      child: const Text('Login'),
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Input Component

#### Basic Usage

```dart
Input(
  placeholder: 'Enter your email',
  type: 'email',
  onInput: (value) => print('Input: $value'),
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `type` | `String` | `'text'` | HTML input type |
| `placeholder` | `String?` | `null` | Placeholder text |
| `value` | `String?` | `null` | Initial value |
| `name` | `String?` | `null` | Form field name |
| `disabled` | `bool` | `false` | Disable the input |
| `required` | `bool` | `false` | Mark as required |
| `onInput` | `InputValueCallback?` | `null` | Fires on each keystroke |
| `onChange` | `InputValueCallback?` | `null` | Fires on blur after change |
| `variant` | `InputVariant?` | `defaultVariant` | Visual variant |
| `pattern` | `String?` | `null` | Validation regex pattern |
| `minLength` | `int?` | `null` | Minimum character length |
| `maxLength` | `int?` | `null` | Maximum character length |
| `min` | `num?` | `null` | Minimum value (for number) |
| `max` | `num?` | `null` | Maximum value (for number) |
| `title` | `String?` | `null` | Tooltip/validation message |

#### Variants

```dart
Input(placeholder: 'Default input')
Input.primary(placeholder: 'Primary input')
Input.error(placeholder: 'Error state input')
```

#### Input Types

```dart
Input(type: 'text', placeholder: 'Text')
Input(type: 'email', placeholder: 'Email')
Input(type: 'password', placeholder: 'Password')
Input(type: 'number', placeholder: 'Number', min: 0, max: 100)
Input(type: 'tel', placeholder: 'Phone')
Input(type: 'url', placeholder: 'URL')
Input(type: 'search', placeholder: 'Search...')
Input(type: 'date')
Input(type: 'time')
```

#### Validation

```dart
Input(
  type: 'email',
  required: true,
  placeholder: 'Email *',
  pattern: r'[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$',
  title: 'Enter a valid email address',
)

Input(
  type: 'text',
  minLength: 3,
  maxLength: 50,
  placeholder: 'Username (3-50 chars)',
)
```

#### Event Handling

```dart
Input(
  placeholder: 'Type here',
  onInput: (value) {
    // Fires on every keystroke
    print('Current value: $value');
  },
  onChange: (value) {
    // Fires when input loses focus and value changed
    print('Final value: $value');
  },
)
```

### Textarea Component

#### Basic Usage

```dart
Textarea(
  placeholder: 'Type your message here.',
  rows: 4,
)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `placeholder` | `String?` | `null` | Placeholder text |
| `value` | `String?` | `null` | Initial value |
| `disabled` | `bool` | `false` | Disable the textarea |
| `required` | `bool` | `false` | Mark as required |
| `rows` | `int?` | `null` | Visible text lines |
| `cols` | `int?` | `null` | Visible text columns |
| `onInput` | `TextareaCallback?` | `null` | Fires on each keystroke |
| `onChange` | `TextareaCallback?` | `null` | Fires on blur |
| `name` | `String?` | `null` | Form field name |
| `maxLength` | `int?` | `null` | Maximum character length |

#### Examples

```dart
// With initial value
Textarea(
  value: 'Default text content',
  rows: 6,
  onInput: (value) => print(value),
)

// Disabled
Textarea(
  placeholder: 'Read only...',
  disabled: true,
  rows: 3,
)

// With validation
Textarea(
  placeholder: 'Comment (required)',
  required: true,
  maxLength: 500,
  name: 'comment',
  rows: 4,
)
```

### Web Contact Form Example

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Contact Form')),
    ),
    CardContent(
      children: [
        div(
          [
            Component.element(
              tag: 'label',
              classes: 'text-sm font-medium',
              children: [Component.text('Name')],
            ),
            Input(
              placeholder: 'Your name',
              required: true,
              name: 'name',
            ),
          ],
          classes: 'space-y-2',
        ),
        div(
          [
            Component.element(
              tag: 'label',
              classes: 'text-sm font-medium',
              children: [Component.text('Message')],
            ),
            Textarea(
              placeholder: 'Your message...',
              rows: 4,
              name: 'message',
            ),
          ],
          classes: 'space-y-2 mt-4',
        ),
      ],
    ),
    CardFooter(
      child: Button.primary(
        htmlType: ButtonHtmlType.submit,
        child: Component.text('Send'),
      ),
    ),
  ],
)
```

## Common Patterns

| Concept | Flutter (coui_flutter) | Web (coui_web) |
|---------|----------------------|----------------|
| Single-line input | `TextField` / `Input` (alias) | `Input` |
| Multi-line input | `TextArea` (Widget) | `Textarea` (Component) |
| Placeholder | `placeholder: Text('...')` (Widget) | `placeholder: '...'` (String) |
| Disable | `enabled: false` | `disabled: true` |
| Password | `obscureText: true` + `InputPasswordToggleFeature` | `type: 'password'` |
| Change callback | `onChanged: (value) {}` | `onInput: (value) {}` (keystroke) / `onChange: (value) {}` (blur) |
| Validation | Via form validators or `InputRevalidateFeature` | HTML5 attrs: `required`, `pattern`, `minLength`, `maxLength` |
| Clear button | `InputClearFeature()` | Manual trailing icon |
| Theming | `TextFieldTheme` | `InputVariant` |

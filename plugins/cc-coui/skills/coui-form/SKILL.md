---
name: coui-form
description: Activate when creating form validation, form fields with labels and error messages, or using validators in CoUI Flutter or Web with Form, FormField, FormLabel, Validator, or ValidationResult.
---

# CoUI Form

## Overview

Form validation system with composable validators, async validation, and field-level error display.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Form Widget

Wrap form fields for validation:

```dart
final formKey = GlobalKey<FormState>();

Form(
  key: formKey,
  child: Column(
    children: [
      FormField<String>(
        label: const Text('Email'),
        validator: RequiredValidator<String>() & EmailValidator(),
        child: const TextField(placeholder: Text('Enter email')),
      ),
      Gap.v(16),
      FormField<String>(
        label: const Text('Password'),
        validator: RequiredValidator<String>() & MinLengthValidator(8),
        child: const TextField(
          placeholder: Text('Enter password'),
          obscureText: true,
        ),
      ),
      Gap.v(24),
      PrimaryButton(
        onPressed: () {
          if (formKey.currentState?.validate() ?? false) {
            // form is valid
          }
        },
        child: const Text('Submit'),
      ),
    ],
  ),
)
```

### FormField

Wraps an input with label, hint, and error display:

```dart
FormField<String>(
  label: const Text('Username'),
  hint: const Text('Enter your username'),
  validator: RequiredValidator<String>(),
  child: const TextField(placeholder: Text('Username')),
)
```

#### FormField Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Input widget |
| `label` | `Widget?` | Field label |
| `hint` | `Widget?` | Help text below input |
| `validator` | `Validator<T>?` | Validation logic |

### FormLabel

Standalone label widget for form fields:

```dart
FormLabel(
  child: const Text('Email Address'),
)
```

### Built-in Validators

#### RequiredValidator

```dart
RequiredValidator<String>()
```

#### EmailValidator

```dart
EmailValidator()
```

#### MinLengthValidator

```dart
MinLengthValidator(8) // minimum 8 characters
```

### Combining Validators

Use `&` (AND) or `|` (OR) operators:

```dart
// All must pass
final validator = RequiredValidator<String>() &
    MinLengthValidator(8) &
    EmailValidator();

// At least one must pass
final validator = EmailValidator() | PhoneValidator();

// Negate
final notEmpty = ~EmptyValidator();
```

### Custom Validator

```dart
class AgeValidator extends Validator<int> {
  const AgeValidator();

  @override
  FutureOr<ValidationResult?> validate(
    BuildContext context,
    int? value,
    FormValidationMode lifecycle,
  ) {
    if (value == null || value < 18) {
      return ValidationResult('Must be 18 or older');
    }
    return null; // valid
  }
}
```

### Async Validator

```dart
class UniqueEmailValidator extends Validator<String> {
  const UniqueEmailValidator();

  @override
  Future<ValidationResult?> validate(
    BuildContext context,
    String? value,
    FormValidationMode lifecycle,
  ) async {
    if (value == null) return null;
    final exists = await checkEmailExists(value);
    if (exists) {
      return ValidationResult('Email already registered');
    }
    return null;
  }
}
```

### FormValidationMode

Controls when validation triggers:

```dart
enum FormValidationMode {
  onSubmit,   // Only on form submit
  onChange,   // On every value change
  onBlur,     // When field loses focus
}
```

### Registration Form Pattern

```dart
Form(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.stretch,
    children: [
      const Text('Create Account').x2Large.bold,
      Gap.v(24),
      FormField<String>(
        label: const Text('Full Name'),
        validator: RequiredValidator<String>(),
        child: const TextField(placeholder: Text('John Doe')),
      ),
      Gap.v(16),
      FormField<String>(
        label: const Text('Email'),
        validator: RequiredValidator<String>() & EmailValidator(),
        child: const TextField(
          placeholder: Text('john@example.com'),
          leading: Icon(Icons.email),
        ),
      ),
      Gap.v(16),
      FormField<String>(
        label: const Text('Password'),
        hint: const Text('At least 8 characters'),
        validator: RequiredValidator<String>() & MinLengthValidator(8),
        child: const TextField(
          placeholder: Text('Password'),
          obscureText: true,
          features: [InputPasswordToggleFeature()],
        ),
      ),
      Gap.v(24),
      PrimaryButton(
        onPressed: () {},
        child: const Text('Sign Up'),
      ),
    ],
  ),
)
```

### FormController

Programmatic form state management:

```dart
final controller = FormController();

// Access values
final name = controller.getValue(nameKey);
final allValues = controller.values;

// Check errors
final errors = controller.errors;
final nameError = controller.getSyncError(nameKey);

// Revalidate
controller.revalidate(context, FormValidationMode.submitted);
```

### Cross-Field Validation

```dart
FormField<String>(
  key: confirmPasswordKey,
  label: const Text('Confirm Password'),
  validator: CompareWith(
    passwordKey,
    compare: (confirm, password) => confirm == password,
    message: 'Passwords do not match',
  ),
  child: const TextField(
    placeholder: Text('Confirm password'),
    obscureText: true,
  ),
)
```

### Built-in Validators (Complete List)

- `NotEmptyValidator` / `RequiredValidator<String>` - non-empty check
- `EmailValidator` - email format
- `MinLengthValidator(n)` - minimum length
- `SafePasswordValidator` - strong password rules
- `CompareWith<T>` - cross-field comparison
- `ConditionalValidator<T>` - custom conditions

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### CoForm

Web forms use `CoForm`, an HTML `<form>` wrapper:

```dart
CoForm(
  onSubmit: handleSubmit,
  children: [
    div(
      [
        Component.element(
          tag: 'label',
          classes: 'text-sm font-medium',
          children: [Component.text('Name')],
        ),
        Input(placeholder: 'Enter name', required: true, name: 'name'),
      ],
      classes: 'space-y-2',
    ),
    div(
      [
        Component.element(
          tag: 'label',
          classes: 'text-sm font-medium',
          children: [Component.text('Email')],
        ),
        Input(type: 'email', placeholder: 'Enter email', required: true, name: 'email'),
      ],
      classes: 'space-y-2',
    ),
    Button.primary(
      htmlType: ButtonHtmlType.submit,
      child: Component.text('Submit'),
    ),
  ],
)
```

### Web Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `onSubmit` | `VoidCallback?` | `null` | Form submission callback |
| `action` | `String?` | `null` | HTML form action URL |
| `method` | `String?` | `null` | HTTP method (GET/POST) |
| `novalidate` | `bool` | `false` | Disable HTML validation |
| `autocomplete` | `String?` | `null` | Autocomplete behavior |

### Web Validation

Web uses HTML5 native validation attributes: `required`, `pattern`, `minLength`, `maxLength`, `min`, `max`.

## Common Patterns

### Platform Differences

| Item | Flutter | Web |
|------|---------|-----|
| Class name | `Form` + `FormController` | `CoForm` (HTML `<form>` wrapper) |
| State management | `FormController` centralized | HTML form event-based |
| Value access | `controller.getValue(key)` | HTML form data |
| Field wrapper | `FormField<T>`, `FormInline<T>` | No separate wrapper |
| Async validation | `FutureOr<ValidationResult?>` supported | Basic validators only |
| Cross-field validation | `CompareWith`, `shouldRevalidate` | Pattern validators only |
| Validator combination | Operators (`&`, `|`, `~`) | Basic combination |
| HTML attributes | None | `action`, `method`, `novalidate`, `autocomplete` |

### Shared Concepts

- Combine validators with `&` (AND) and `|` (OR) operators (Flutter).
- Use `FormValidationMode` to control validation timing (Flutter).
- Return `null` from validators to indicate valid input (Flutter).
- Use async validators for server-side checks (e.g., unique email) (Flutter).

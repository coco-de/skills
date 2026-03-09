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

## Web (coui_web)

> **Not yet implemented.** Form validation is currently Flutter-only. Web implementation is planned.

## Common Patterns

- Combine validators with `&` (AND) and `|` (OR) operators.
- Use `FormValidationMode` to control validation timing.
- Return `null` from validators to indicate valid input.
- Use async validators for server-side checks (e.g., unique email).

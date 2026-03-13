---
name: coui-validation-badge
description: Activate when creating form validation indicators, password strength checkers, input validation status displays, or valid/invalid state badges using ValidationBadge (Flutter) or ValidationBadge (Web) in CoUI Flutter or CoUI Web.
---

# CoUI ValidationBadge

## Overview

The ValidationBadge presents input validation results through icons and text labels. It is designed to communicate form field validation states visually, such as password strength indicators or email format verification.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
ValidationBadge(
  isValid: true,
  label: '사용 가능한 이메일입니다.',
)

ValidationBadge(
  isValid: false,
  label: '이미 사용 중인 이메일입니다.',
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `isValid` | `bool` | required | Validation status (true = success, false = failure) |
| `label` | `String` | required | Text describing the validation condition |
| `showIcon` | `bool` | `true` | Controls icon visibility |

### Without Icon

```dart
ValidationBadge(
  isValid: true,
  label: '8자 이상',
  showIcon: false,
)
```

### Password Validation Checklist

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    ValidationBadge(isValid: password.length >= 8, label: '8자 이상'),
    ValidationBadge(isValid: hasUpperCase, label: '대문자 포함'),
    ValidationBadge(isValid: hasNumber, label: '숫자 포함'),
    ValidationBadge(isValid: hasSpecialChar, label: '특수문자 포함'),
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
ValidationBadge(
  isValid: true,
  label: '사용 가능한 이메일입니다.',
)

ValidationBadge(
  isValid: false,
  label: '이미 사용 중인 이메일입니다.',
)
```

### Multiple Validation Conditions

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    ValidationBadge(isValid: password.length >= 8, label: '8자 이상'),
    ValidationBadge(isValid: hasUpperCase, label: '대문자 포함'),
    ValidationBadge(isValid: hasNumber, label: '숫자 포함'),
  ],
)
```

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `ValidationBadge` | `ValidationBadge` |
| API | Identical parameters | Identical parameters |

### When to Use

- Password strength indicators
- Email/username availability checks
- Form field validation feedback
- Real-time input validation checklists

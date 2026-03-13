---
name: coui-input-otp
description: Activate when creating OTP inputs, PIN code fields, verification code inputs, or one-time password fields using CouiInputOtp, InputOtp in CoUI Flutter or CoUI Web.
---

# CoUI InputOtp

## Overview

The InputOtp is a separated input field component for entering OTP authentication codes or PIN numbers character-by-character. It supports configurable length, obscured text for PINs, and auto-focus behavior. Flutter uses `CouiInputOtp` while Web uses `InputOtp`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic OTP Input (6 digits)

```dart
CouiInputOtp(
  length: 6,
  onCompleted: handleOtpCompleted,
)
```

### PIN Format (4 digits)

```dart
CouiInputOtp(
  length: 4,
  obscureText: true,
  autofocus: true,
  onCompleted: handlePinCompleted,
  onChanged: handlePinChanged,
)
```

### With Completion Callback

```dart
CouiInputOtp(
  length: 6,
  autofocus: true,
  onCompleted: (otp) {
    unawaited(authService.verifyOtp(otp));
  },
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `length` | `int` | `6` | Number of OTP digits |
| `onCompleted` | `ValueChanged<String>?` | `null` | Completion callback (all digits entered) |
| `onChanged` | `ValueChanged<String>?` | `null` | Change callback |
| `obscureText` | `bool` | `false` | Hide input values (for PIN) |
| `autofocus` | `bool` | `false` | Auto-focus first field |
| `keyboardType` | `TextInputType` | `TextInputType.number` | Keyboard type |
| `enabled` | `bool` | `true` | Enable/disable state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic OTP Input

```dart
InputOtp(
  length: 6,
  onCompleted: handleOtpCompleted,
)
```

### PIN Mode

```dart
InputOtp(
  length: 4,
  obscureText: true,
  autofocus: true,
  onCompleted: handlePinCompleted,
)
```

## Common Patterns

### Variants

- **SMS Authentication (6-digit)**: Standard verification code entry with `length: 6`
- **PIN Entry (4-digit)**: Password-style masking with `obscureText: true` and `length: 4`

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `CouiInputOtp` | `InputOtp` |
| API structure | Identical | Identical |

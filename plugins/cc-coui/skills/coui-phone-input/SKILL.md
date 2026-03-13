---
name: coui-phone-input
description: Activate when creating phone number inputs, country code selectors, international phone fields, or dial code inputs using PhoneInput, PhoneInput in CoUI Flutter or CoUI Web.
---

# CoUI PhoneInput

## Overview

The PhoneInput is a form component for entering phone numbers with country code selection. It automatically applies country-specific formatting based on the selected country. Flutter uses `PhoneInput` while Web uses `PhoneInput`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Phone Number Input

```dart
PhoneInput(
  value: phoneNumber,
  onChanged: handlePhoneChanged,
  defaultCountry: 'KR',
)
```

### With Dial Code Display and Validation

```dart
PhoneInput(
  value: phoneNumber,
  onChanged: handlePhoneChanged,
  defaultCountry: 'KR',
  showDialCode: true,
  validator: (value) {
    if (value == null || value.isEmpty) return '전화번호를 입력하세요';
    return null;
  },
)
```

### With Country Restrictions

```dart
PhoneInput(
  value: phoneNumber,
  onChanged: handlePhoneChanged,
  countries: ['KR', 'US', 'JP', 'CN'],
  defaultCountry: 'KR',
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String?` | `null` | Current phone number value |
| `onChanged` | `ValueChanged<String>?` | `null` | Change callback handler |
| `defaultCountry` | `String` | `'KR'` | Default country code (ISO 3166-1) |
| `countries` | `List<String>?` | `null` | Allowed countries list; null permits all |
| `showDialCode` | `bool` | `true` | Display country dial code |
| `validator` | `String? Function(String?)?` | `null` | Validation function |
| `enabled` | `bool` | `true` | Enable/disable state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic PhoneInput

```dart
PhoneInput(
  value: phoneNumber,
  onChanged: handlePhoneChanged,
  defaultCountry: 'KR',
)
```

### With Multiple Countries

```dart
PhoneInput(
  value: phoneNumber,
  onChanged: handlePhoneChanged,
  defaultCountry: 'KR',
  showDialCode: true,
  countries: ['KR', 'US', 'JP'],
)
```

## Common Patterns

### Variants

- **Domestic Only**: `countries: ['KR']` with `defaultCountry: 'KR'`
- **International**: `showDialCode: true` with multiple country options

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `PhoneInput` | `PhoneInput` |
| API structure | Identical | Identical |

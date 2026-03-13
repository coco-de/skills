---
name: coui-fieldset
description: Activate when creating fieldsets, form groups, form sections, or grouped form fields with legends using Fieldset, Fieldset in CoUI Flutter or CoUI Web.
---

# CoUI Fieldset

## Overview

The Fieldset is a container component that groups related form fields logically and visually, with a legend title and optional description. It can also disable all contained fields at once. Flutter uses `Fieldset` while Web uses `Fieldset`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Fieldset

```dart
Fieldset(
  legend: '기본 정보',
  children: [
    Input(label: '이름', onChanged: handleNameChanged),
    Input(label: '이메일', onChanged: handleEmailChanged),
  ],
)
```

### With Description

```dart
Fieldset(
  legend: '결제 정보',
  description: '안전하게 암호화되어 처리됩니다',
  children: [
    Input(label: '카드 번호', onChanged: handleCardNumberChanged),
    Input(label: '유효기간', onChanged: handleExpiryChanged),
    Input(label: 'CVV', onChanged: handleCvvChanged),
  ],
)
```

### Disabled Fieldset

```dart
Fieldset(
  legend: '배송 정보',
  disabled: true,
  children: [
    Input(label: '주소', onChanged: handleAddressChanged),
    Input(label: '우편번호', onChanged: handleZipCodeChanged),
  ],
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `legend` | `String` | required | Fieldset title |
| `children` | `List<Widget>` | required | List of form field widgets to group |
| `disabled` | `bool` | `false` | Whether to disable entire fieldset |
| `description` | `String?` | `null` | Supplementary description text |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Fieldset

```dart
Fieldset(
  legend: '기본 정보',
  children: [
    Input(label: '이름', onChanged: handleNameChanged),
    Input(label: '이메일', onChanged: handleEmailChanged),
  ],
)
```

### With Description

```dart
Fieldset(
  legend: '결제 정보',
  description: '안전하게 암호화되어 처리됩니다',
  disabled: false,
  children: [
    Input(label: '카드 번호', onChanged: handleCardNumberChanged),
  ],
)
```

## Common Patterns

### Use Cases

- **Account Information**: Group authentication fields (name, email, password)
- **Payment Details**: Group card fields with encryption description
- **Read-Only Sections**: Use `disabled: true` for non-editable field groups

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `Fieldset` | `Fieldset` |
| Child inputs | `Input` | `Input` |
| API structure | Identical | Identical |

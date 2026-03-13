---
name: coui-radio-group
description: Activate when creating radio button groups, single-select option lists, or radio inputs using RadioGroup, Radio, RadioGroup, RadioItem, RadioOrientation in CoUI Flutter or CoUI Web.
---

# CoUI RadioGroup

## Overview

The RadioGroup is a form component for selecting one option from multiple items, supporting vertical and horizontal layouts. Flutter uses `RadioGroup<T>` with generic typing while Web uses `RadioGroup`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Vertical RadioGroup

```dart
RadioGroup<String>(
  value: selectedGender,
  onChanged: handleGenderChanged,
  label: '성별',
  items: [
    RadioItem(value: 'male', label: '남성'),
    RadioItem(value: 'female', label: '여성'),
    RadioItem(value: 'other', label: '기타'),
  ],
)
```

### Horizontal Layout

```dart
RadioGroup<String>(
  value: selectedSize,
  onChanged: handleSizeChanged,
  orientation: RadioOrientation.horizontal,
  items: [
    RadioItem(value: 'sm', label: 'S'),
    RadioItem(value: 'md', label: 'M'),
    RadioItem(value: 'lg', label: 'L'),
    RadioItem(value: 'xl', label: 'XL'),
  ],
)
```

### Individual Radio Usage

```dart
Radio<String>(
  value: 'option1',
  groupValue: selectedOption,
  onChanged: handleOptionChanged,
  label: '옵션 1',
)
```

### Plan Selection

```dart
RadioGroup<String>(
  value: selectedPlan,
  onChanged: handlePlanChanged,
  label: '요금제 선택',
  items: [
    RadioItem(value: 'basic', label: '베이직'),
    RadioItem(value: 'pro', label: '프로'),
    RadioItem(value: 'enterprise', label: '엔터프라이즈'),
  ],
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `T?` | `null` | Currently selected value |
| `onChanged` | `ValueChanged<T>?` | `null` | Selection change callback |
| `items` | `List<RadioItem<T>>` | required | List of radio items |
| `orientation` | `RadioOrientation` | `RadioOrientation.vertical` | Layout direction |
| `label` | `String?` | `null` | Group label |
| `enabled` | `bool` | `true` | Enable/disable state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic RadioGroup

```dart
RadioGroup(
  value: selectedGender,
  onChanged: handleGenderChanged,
  label: '성별',
  items: [
    RadioItem(value: 'male', label: '남성'),
    RadioItem(value: 'female', label: '여성'),
    RadioItem(value: 'other', label: '기타'),
  ],
)
```

### Horizontal Orientation

```dart
RadioGroup(
  value: selectedSize,
  onChanged: handleSizeChanged,
  orientation: 'horizontal',
  items: [
    RadioItem(value: 'sm', label: 'S'),
    RadioItem(value: 'md', label: 'M'),
    RadioItem(value: 'lg', label: 'L'),
  ],
)
```

## Common Patterns

### Layout Variants

- **Vertical (default)**: Standard stacked arrangement, one item per line
- **Horizontal**: Side-by-side arrangement using `RadioOrientation.horizontal` (Flutter) or `'horizontal'` (Web)

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `RadioGroup<T>` | `RadioGroup` |
| Generic typing | Supports `<T>` | String-based |
| Orientation | `RadioOrientation.horizontal` | `'horizontal'` (string) |
| Individual radio | `Radio<T>` | `Radio` |

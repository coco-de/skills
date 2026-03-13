---
name: coui-chip-input
description: Activate when creating chip inputs, tag inputs, multi-value text inputs, or token fields using CouiChipInput, ChipInput in CoUI Flutter or CoUI Web.
---

# CoUI ChipInput

## Overview

The ChipInput is a multi-item input component where users type text and press Enter to add items as chips (tags). It supports maximum chip limits, input validation, and individual add/remove callbacks. Flutter uses `CouiChipInput` while Web uses `ChipInput`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Chip Input

```dart
CouiChipInput(
  values: selectedTags,
  onChanged: handleTagsChanged,
  placeholder: '태그 입력 후 Enter',
)
```

### With Maximum Chips Limit

```dart
CouiChipInput(
  values: selectedSkills,
  onChanged: handleSkillsChanged,
  onAdd: handleSkillAdded,
  onRemove: handleSkillRemoved,
  placeholder: '스킬 추가',
  maxChips: 5,
)
```

### With Input Validation

```dart
CouiChipInput(
  values: emailList,
  onChanged: handleEmailListChanged,
  placeholder: '이메일 추가',
  validator: (value) {
    final emailRegex = RegExp(r'^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$');
    if (!emailRegex.hasMatch(value)) return '유효한 이메일을 입력하세요';
    return null;
  },
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `values` | `List<String>` | required | Current chip list |
| `onChanged` | `ValueChanged<List<String>>?` | `null` | List change callback |
| `onAdd` | `ValueChanged<String>?` | `null` | Chip addition callback |
| `onRemove` | `ValueChanged<String>?` | `null` | Chip removal callback |
| `placeholder` | `String?` | `null` | Input field placeholder |
| `maxChips` | `int?` | `null` | Maximum number of chips |
| `validator` | `String? Function(String)?` | `null` | Input validation function |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic ChipInput

```dart
ChipInput(
  values: selectedTags,
  onChanged: handleTagsChanged,
  placeholder: '태그 입력 후 Enter',
)
```

### With Max Chips

```dart
ChipInput(
  values: selectedSkills,
  onChanged: handleSkillsChanged,
  maxChips: 5,
  placeholder: '스킬 추가',
)
```

## Common Patterns

### Use Cases

- **Tag Input**: `maxChips: 10` with placeholder "태그를 입력하세요"
- **Email Recipients**: Use `validator` for email format validation

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `CouiChipInput` | `ChipInput` |
| API structure | Identical | Identical |

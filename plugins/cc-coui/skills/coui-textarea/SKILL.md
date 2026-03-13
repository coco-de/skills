---
name: coui-textarea
description: Activate when creating multi-line text inputs, auto-expanding text areas, or text fields with character limits using CouiTextArea, TextArea, TextAreaResize in CoUI Flutter or CoUI Web.
---

# CoUI TextArea

## Overview

The TextArea is a multi-line text input component that supports auto-height adjustment and character limit features. Flutter uses `CouiTextArea` while Web uses `TextArea`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic TextArea

```dart
CouiTextArea(
  value: description,
  onChanged: handleDescriptionChanged,
  placeholder: '내용을 입력하세요',
)
```

### With Character Limit

```dart
CouiTextArea(
  value: comment,
  onChanged: handleCommentChanged,
  placeholder: '댓글을 입력하세요',
  maxLength: 500,
  maxLines: 6,
  minLines: 3,
)
```

### Auto-Expanding

```dart
CouiTextArea(
  value: note,
  onChanged: handleNoteChanged,
  minLines: 2,
  maxLines: null, // unlimited expansion
  resize: TextAreaResize.vertical,
)
```

### With Character Counter

```dart
CouiTextArea(
  value: bio,
  onChanged: handleBioChanged,
  placeholder: '자기소개를 입력하세요',
  maxLength: 200,
  minLines: 3,
  maxLines: 6,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Current text value |
| `onChanged` | `ValueChanged<String>?` | `null` | Change callback handler |
| `placeholder` | `String?` | `null` | Placeholder text display |
| `maxLines` | `int?` | `4` | Maximum line count (null = unlimited) |
| `minLines` | `int?` | `1` | Minimum line count |
| `maxLength` | `int?` | `null` | Maximum character count |
| `resize` | `TextAreaResize` | `TextAreaResize.none` | Resize direction control |
| `enabled` | `bool` | `true` | Enable/disable state |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic TextArea

```dart
TextArea(
  value: description,
  onChanged: handleDescriptionChanged,
  placeholder: '내용을 입력하세요',
)
```

### With Configuration

```dart
TextArea(
  value: comment,
  onChanged: handleCommentChanged,
  maxLength: 500,
  maxLines: 6,
  minLines: 3,
  resize: 'vertical',
)
```

## Common Patterns

### Variants

- **Character counter**: Use `maxLength` to display a character counter
- **Auto-expanding**: Set `maxLines: null` for unlimited vertical expansion

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `CouiTextArea` | `TextArea` |
| Resize type | `TextAreaResize.vertical` | `'vertical'` (string) |

---
name: coui-autocomplete
description: Activate when creating autocomplete inputs, search suggestions, async search fields, or typeahead components using AutoComplete, AutoComplete in CoUI Flutter or CoUI Web.
---

# CoUI AutoComplete

## Overview

The AutoComplete component displays suggestion lists based on user input, supporting both static suggestion lists and async search functions with debounce. Flutter uses `AutoComplete` while Web uses `AutoComplete`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic AutoComplete

```dart
AutoComplete(
  suggestions: ['Apple', 'Banana', 'Cherry', 'Grape'],
  onSelected: handleFruitSelected,
  labelText: '과일 검색',
)
```

### Async Search

```dart
AutoComplete(
  asyncSearch: (query) async {
    final results = await searchApi.search(query);
    return results.map((r) => r.name).toList();
  },
  onSelected: handleResultSelected,
  debounceMs: 300,
  labelText: '검색어 입력',
)
```

### Custom Filter

```dart
AutoComplete(
  suggestions: cityList,
  filter: (item, query) => item.toLowerCase().startsWith(query.toLowerCase()),
  onSelected: handleCitySelected,
  labelText: '도시 선택',
)
```

### Static List with Max Suggestions

```dart
AutoComplete(
  suggestions: countries,
  onSelected: handleCountrySelected,
  labelText: '국가 선택',
  maxSuggestions: 8,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `suggestions` | `List<String>?` | `null` | Static suggestion list |
| `onSelected` | `ValueChanged<String>?` | `null` | Selection callback |
| `labelText` | `String?` | `null` | Input field label |
| `filter` | `bool Function(String, String)?` | `null` | Custom filter function |
| `asyncSearch` | `Future<List<String>> Function(String)?` | `null` | Async search function |
| `debounceMs` | `int` | `300` | Search delay in milliseconds |
| `maxSuggestions` | `int` | `5` | Maximum suggestions to display |
| `onChanged` | `ValueChanged<String>?` | `null` | Input change callback |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic AutoComplete

```dart
AutoComplete(
  suggestions: ['Apple', 'Banana', 'Cherry', 'Grape'],
  onSelected: handleFruitSelected,
  label: '과일 검색',
)
```

### Async Search

```dart
AutoComplete(
  asyncSearch: (query) async {
    final results = await searchApi.search(query);
    return results.map((r) => r.name).toList();
  },
  onSelected: handleResultSelected,
  debounceMs: 300,
  label: '검색어 입력',
)
```

## Common Patterns

### Static vs Async

- **Static List**: Use `suggestions` for small, known lists
- **Async Search**: Use `asyncSearch` with `debounceMs` for server-side search

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `AutoComplete` | `AutoComplete` |
| Label prop | `labelText` | `label` |

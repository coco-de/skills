---
name: coui-select
description: Activate when creating dropdown select menus, multi-select pickers, select groups, option lists, or handling selection change events in CoUI Flutter or Web using Select, SelectItem, SelectGroup, SelectLabel, or SelectOption.
---

# CoUI Select

## Overview

The Select component provides dropdown selection menus across both Flutter and Web platforms. Flutter offers rich features including multi-select, searchable options, grouped items, and theme customization. Web provides a lightweight native `<select>` element wrapper with placeholder and form integration support.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Select

```dart
String? selectedValue;

Select<String>(
  value: selectedValue,
  placeholder: const Text('Select an option'),
  onChanged: (value) {
    setState(() {
      selectedValue = value;
    });
  },
  items: [
    SelectItem(value: 'apple', label: const Text('Apple')),
    SelectItem(value: 'banana', label: const Text('Banana')),
    SelectItem(value: 'cherry', label: const Text('Cherry')),
  ],
)
```

### SelectItem

Each option in the dropdown:

```dart
SelectItem<String>(
  value: 'option1',
  label: const Text('Option 1'),
)
```

### Grouped Select

Use `SelectGroup` and `SelectLabel` for categorized options:

```dart
Select<String>(
  value: selected,
  onChanged: (v) => setState(() => selected = v),
  children: [
    const SelectLabel(child: Text('Fruits')),
    SelectItem(value: 'apple', label: const Text('Apple')),
    SelectItem(value: 'banana', label: const Text('Banana')),
    const SelectLabel(child: Text('Vegetables')),
    SelectItem(value: 'carrot', label: const Text('Carrot')),
    SelectItem(value: 'broccoli', label: const Text('Broccoli')),
  ],
)
```

### Multi-Select

Use a `Set` or `List` for multiple values:

```dart
Set<String> selectedValues = {};

Select<String>.multiple(
  value: selectedValues,
  placeholder: const Text('Select items'),
  onChanged: (values) {
    setState(() {
      selectedValues = values;
    });
  },
  items: [
    SelectItem(value: 'a', label: const Text('Option A')),
    SelectItem(value: 'b', label: const Text('Option B')),
    SelectItem(value: 'c', label: const Text('Option C')),
  ],
)
```

### Search in Select

```dart
Select<String>(
  value: selected,
  onChanged: (v) => setState(() => selected = v),
  searchable: true,
  searchPlaceholder: const Text('Search...'),
  items: items,
)
```

### SelectTheme

Theme-level customization:

```dart
const SelectTheme(
  popupConstraints: BoxConstraints(maxHeight: 300),
  popoverAlignment: AlignmentDirectional.topCenter,
  popoverAnchorAlignment: AlignmentDirectional.bottomCenter,
  borderRadius: BorderRadius.circular(8),
  padding: EdgeInsets.symmetric(horizontal: 12, vertical: 8),
  canUnselect: true,
  autoClosePopover: true,
  disableHoverEffect: false,
  color: Colors.white,
)
```

### SelectController

Programmatic control for single selection:

```dart
final controller = SelectController<String>();

// Open/close dropdown programmatically
controller.open();
controller.close();

// Set value
controller.value = 'apple';
```

### MultiSelectController

State management for multi-selection:

```dart
final controller = MultiSelectController<String>();

Select<String>.multiple(
  controller: controller,
  onChanged: (values) {
    print('Selected: $values');
  },
  items: items,
)
```

### Flutter Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `T?` | Currently selected value |
| `onChanged` | `ValueChanged<T?>?` | Selection callback |
| `placeholder` | `Widget?` | Placeholder when nothing selected |
| `items` | `List<SelectItem<T>>?` | List of selectable items |
| `children` | `List<Widget>?` | Custom children (for groups/labels) |
| `enabled` | `bool` | Enable/disable select |
| `popupConstraints` | `BoxConstraints?` | Popup size constraints |

### Flutter Form Field Pattern

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Country').sm.bold,
    Gap.v(4),
    Select<String>(
      value: selectedCountry,
      placeholder: const Text('Choose a country'),
      onChanged: (value) {
        setState(() => selectedCountry = value);
      },
      items: [
        SelectItem(value: 'kr', label: const Text('South Korea')),
        SelectItem(value: 'us', label: const Text('United States')),
        SelectItem(value: 'jp', label: const Text('Japan')),
      ],
    ),
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
Select(
  options: [
    SelectOption('apple', 'Apple'),
    SelectOption('banana', 'Banana'),
    SelectOption('orange', 'Orange'),
  ],
  onChanged: (value) => print('Selected: $value'),
)
```

### SelectOption

```dart
const SelectOption(String value, String label)
```

- `value`: The submitted value
- `label`: The display text

### With Placeholder

```dart
Select(
  placeholder: 'Choose a fruit...',
  options: [
    SelectOption('apple', 'Apple'),
    SelectOption('banana', 'Banana'),
    SelectOption('orange', 'Orange'),
  ],
  onChanged: (value) => handleSelection(value),
)
```

The placeholder renders as a disabled, selected `<option>` element.

### Pre-selected Value

```dart
Select(
  value: 'banana',
  options: [
    SelectOption('apple', 'Apple'),
    SelectOption('banana', 'Banana'),
    SelectOption('orange', 'Orange'),
  ],
)
```

### Disabled State

```dart
Select(
  disabled: true,
  value: 'apple',
  options: [
    SelectOption('apple', 'Apple'),
    SelectOption('banana', 'Banana'),
  ],
)
```

### Web Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `options` | `List<SelectOption>` | required | List of select options |
| `value` | `String?` | `null` | Currently selected value |
| `disabled` | `bool` | `false` | Whether select is disabled |
| `onChanged` | `SelectCallback?` | `null` | Callback when selection changes |
| `name` | `String?` | `null` | Form field name |
| `placeholder` | `String?` | `null` | Placeholder option text |

### Web Form Pattern

```dart
div(
  [
    Component.element(
      tag: 'label',
      classes: 'text-sm font-medium',
      children: [Component.text('Country')],
    ),
    Select(
      name: 'country',
      placeholder: 'Select your country',
      options: [
        SelectOption('us', 'United States'),
        SelectOption('uk', 'United Kingdom'),
        SelectOption('kr', 'South Korea'),
        SelectOption('jp', 'Japan'),
      ],
      onChanged: (value) => handleCountryChange(value),
    ),
  ],
  classes: 'space-y-2',
)
```

### Dynamic Options

```dart
Select(
  options: items.map((item) => SelectOption(item.id, item.name)).toList(),
  value: selectedId,
  onChanged: (value) => setState(() => selectedId = value),
)
```

## Common Patterns

### Shared Concepts

Both Flutter and Web Select components share these core concepts:

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `Select<T>` | `Select` |
| Option item | `SelectItem(value, label)` | `SelectOption(value, label)` |
| Current value | `value: T?` | `value: String?` |
| Change callback | `onChanged: ValueChanged<T?>?` | `onChanged: SelectCallback?` |
| Placeholder | `placeholder: Widget?` | `placeholder: String?` |
| Disabled state | `enabled: false` | `disabled: true` |

### Platform Differences

- **Typing**: Flutter uses generics (`Select<String>`, `Select<int>`), Web uses `String` values only.
- **Multi-select**: Flutter supports `Select.multiple()`, Web does not have built-in multi-select.
- **Search**: Flutter supports `searchable: true`, Web relies on native browser behavior.
- **Grouping**: Flutter uses `SelectLabel` and `SelectGroup` widgets, Web uses flat option lists.
- **Theming**: Flutter has `SelectTheme` for visual customization, Web uses CSS classes.

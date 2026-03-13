---
name: coui-date-picker
description: Activate when creating date picker inputs, date range pickers, or controlled date selection using DatePicker, DateRangePicker, or ControlledDatePicker in CoUI Flutter or Web.
---

# CoUI DatePicker

## Overview

Date selection components for single dates and date ranges. Supports popover and dialog modes with calendar view integration.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic DatePicker

```dart
DateTime? selectedDate;

DatePicker(
  value: selectedDate,
  onChanged: (date) {
    setState(() => selectedDate = date);
  },
)
```

### DateRangePicker

Select a date range:

```dart
DateTime? startDate;
DateTime? endDate;

DateRangePicker(
  start: startDate,
  end: endDate,
  onChanged: (start, end) {
    setState(() {
      startDate = start;
      endDate = end;
    });
  },
)
```

### ControlledDatePicker

Higher-level date picker with controller support:

```dart
ControlledDatePicker(
  initialValue: DateTime.now(),
  onChanged: (date) {
    print('Selected: $date');
  },
)
```

### DatePickerTheme

```dart
const DatePickerTheme(
  mode: PromptMode.popover,
  initialView: CalendarView.month,
  initialViewType: CalendarViewType.grid,
  popoverAlignment: Alignment.bottomCenter,
  popoverAnchorAlignment: Alignment.topCenter,
  popoverPadding: EdgeInsets.all(8),
)
```

### PromptMode

Controls how the date picker opens:

```dart
PromptMode.popover  // Opens as popover (default)
PromptMode.dialog   // Opens as modal dialog
```

### Key Parameters

#### DatePicker

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `DateTime?` | Selected date |
| `onChanged` | `ValueChanged<DateTime?>?` | Selection callback |
| `initialView` | `CalendarView?` | Starting calendar view |
| `mode` | `PromptMode?` | Popover or dialog |

#### DateRangePicker

| Parameter | Type | Description |
|-----------|------|-------------|
| `start` | `DateTime?` | Range start date |
| `end` | `DateTime?` | Range end date |
| `onChanged` | `Function(DateTime?, DateTime?)` | Range callback |

### Form Field with DatePicker Pattern

```dart
FormField<DateTime>(
  label: const Text('Birth Date'),
  child: DatePicker(
    value: birthDate,
    onChanged: (date) => setState(() => birthDate = date),
  ),
)
```

### Date Range Filter Pattern

```dart
Card(
  padding: const EdgeInsets.all(16),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Filter by Date').bold,
      Gap.v(12),
      DateRangePicker(
        start: filterStart,
        end: filterEnd,
        onChanged: (start, end) {
          setState(() {
            filterStart = start;
            filterEnd = end;
          });
          // Apply filter
        },
      ),
    ],
  ),
)
```

### Event Scheduling Pattern

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Schedule Event').x2Large.bold,
    Gap.v(16),
    const TextField(placeholder: Text('Event name')),
    Gap.v(12),
    Row(
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('Start Date').sm.bold,
              Gap.v(4),
              DatePicker(
                value: eventStart,
                onChanged: (d) => setState(() => eventStart = d),
              ),
            ],
          ),
        ),
        Gap.h(12),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const Text('End Date').sm.bold,
              Gap.v(4),
              DatePicker(
                value: eventEnd,
                onChanged: (d) => setState(() => eventEnd = d),
              ),
            ],
          ),
        ),
      ],
    ),
  ],
)
```

### DatePickerController

```dart
final controller = DatePickerController();
controller.value = DateTime(2024, 3, 15);
print(controller.value); // 2024-03-15
```

Based on `ValueNotifier`, integrates with `ComponentController` mixin for forms.

### Date State Validation

```dart
DatePicker(
  value: selectedDate,
  stateBuilder: (date) {
    if (date.isBefore(DateTime.now())) return DateState.disabled;
    if (holidays.contains(date)) return DateState.disabled;
    return DateState.enabled;
  },
  onChanged: (date) => setState(() => selectedDate = date),
)
```

### View Switching

- `initialViewType`: starting view (date/month/year)
- `initialView`: starting month (e.g., `CalendarView(2024, 3)`)
- Header click transitions date -> month -> year views

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

Uses native HTML `<input type="date">`:

```dart
DatePicker(
  value: selectedDate,
  onChange: (value) => handleDateChange(value),
)
```

### With Min/Max

```dart
DatePicker(
  value: selectedDate,
  onChange: (value) => handleDateChange(value),
  min: '2024-01-01',
  max: '2024-12-31',
)
```

### Web Limitations

- Uses browser's native date picker UI
- Values passed as ISO 8601 strings (YYYY-MM-DD)
- Range selection not supported
- No custom calendar view or view switching
- Validation limited to `min`/`max` attributes

## Common Patterns

### Platform Differences

| Feature | Flutter | Web |
|---------|---------|-----|
| Calendar UI | Custom DatePickerDialog | Native `<input type="date">` |
| Value type | `DateTime?` | `String` (ISO 8601) |
| Display mode | `PromptMode` (dialog/popover) | Browser native |
| Range selection | `DateRangePicker` + `DateTimeRange` | Not supported |
| Validation | `DateStateBuilder` callback | `min`/`max` attributes only |
| View switching | 3-step (date->month->year) | Browser default |
| Controller | `DatePickerController` (ValueNotifier) | None |
| Responsive | Dual calendar (>=500px) | Browser default |

### Shared Concepts

- Use `DatePicker` for single date selection, `DateRangePicker` for ranges (Flutter only).
- Wrap with `FormField` for form validation integration.
- Choose `PromptMode.popover` for inline forms, `PromptMode.dialog` for mobile (Flutter).

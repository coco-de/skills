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

## Web (coui_web)

> **Not yet implemented.** DatePicker is currently Flutter-only. Web implementation is planned.

## Common Patterns

- Use `DatePicker` for single date selection, `DateRangePicker` for ranges.
- Wrap with `FormField` for form validation integration.
- Choose `PromptMode.popover` for inline forms, `PromptMode.dialog` for mobile.

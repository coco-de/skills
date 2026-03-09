---
name: coui-calendar
description: Use when creating calendar widgets, date pickers, date selection interfaces, range date selection, or month-view calendar grids using Calendar, SingleCalendarValue, or RangeCalendarValue in CoUI Flutter or Web.
---

# CoUI Calendar

## Overview

The Calendar component provides date selection UI for both Flutter and Web platforms. Flutter supports single and range selection with multiple view modes (day, month, year, decade). Web provides a month-view grid calendar with single date selection, navigation, and accessibility support.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Single Date Selection

```dart
DateTime? selectedDate;

Calendar(
  value: selectedDate != null
      ? SingleCalendarValue(selectedDate!)
      : null,
  onChanged: (value) {
    setState(() {
      if (value is SingleCalendarValue) {
        selectedDate = value.date;
      }
    });
  },
)
```

### Range Date Selection

```dart
DateTime? startDate;
DateTime? endDate;

Calendar(
  value: startDate != null && endDate != null
      ? RangeCalendarValue(startDate!, endDate!)
      : null,
  onChanged: (value) {
    setState(() {
      if (value is RangeCalendarValue) {
        startDate = value.start;
        endDate = value.end;
      }
    });
  },
)
```

### CalendarView

Controls the time period shown:

```dart
enum CalendarView {
  day,     // Day view
  month,   // Month view (default)
  year,    // Year selection
  decade,  // Decade selection
}
```

### CalendarViewType

Layout style:

```dart
enum CalendarViewType {
  grid,     // Grid layout
  list,     // List layout
  compact,  // Compact layout
}
```

### CalendarTheme

```dart
const CalendarTheme(
  arrowIconColor: Colors.blue,
  selectedColor: Colors.blue,
  todayColor: Colors.grey,
  todayTextColor: Colors.black,
  rangeSelectionColor: Colors.blue.withOpacity(0.2),
  rangeSelectionTextColor: Colors.blue,
)
```

### Key Parameters (Flutter)

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `CalendarValue?` | Selected date(s) |
| `onChanged` | `ValueChanged<CalendarValue>?` | Selection callback |
| `initialView` | `CalendarView?` | Starting view |
| `viewType` | `CalendarViewType?` | Layout type |

### Calendar Value Types

#### SingleCalendarValue

```dart
final value = SingleCalendarValue(DateTime(2024, 3, 15));
value.date  // DateTime
```

#### RangeCalendarValue

```dart
final value = RangeCalendarValue(
  DateTime(2024, 3, 1),
  DateTime(2024, 3, 15),
);
value.start  // DateTime
value.end    // DateTime
```

### Date Display Pattern (Flutter)

```dart
Card(
  padding: const EdgeInsets.all(16),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Select Date').bold,
      Gap.v(12),
      Calendar(
        value: selectedDate != null
            ? SingleCalendarValue(selectedDate!)
            : null,
        onChanged: (value) {
          if (value is SingleCalendarValue) {
            setState(() => selectedDate = value.date);
          }
        },
      ),
      if (selectedDate != null) ...[
        Gap.v(12),
        Text('Selected: ${selectedDate!.toLocal()}').small.base200,
      ],
    ],
  ),
)
```

## Web (coui_web)

### When to Use

- Adding a date picker interface
- Creating a month-view calendar grid
- Handling date selection events

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Calendar(
  selectedDate: DateTime.now(),
  onDateSelected: (date) => print('Selected: $date'),
)
```

### Key Parameters (Web)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `selectedDate` | `DateTime?` | `null` | Currently selected date |
| `onDateSelected` | `DateSelectCallback?` | `null` | Date selection callback |
| `minDate` | `DateTime?` | `null` | Minimum selectable date |
| `maxDate` | `DateTime?` | `null` | Maximum selectable date |

### Features

- Month/year header with previous/next navigation buttons
- Weekday labels (Su, Mo, Tu, We, Th, Fr, Sa)
- Day grid with proper month offset
- Selected date highlighting with `bg-primary text-primary-foreground`
- Hover effect on days with `hover:bg-accent hover:text-accent-foreground`
- Bordered, rounded container (`p-3 rounded-md border`)

### Accessibility

- Container has `role="application"` and `aria-label="Calendar"`
- Each day button has `aria-label` with ISO 8601 date
- Selected day has `aria-selected="true"`
- Navigation buttons have `aria-label` ("Previous month", "Next month")

### Display Month

The calendar displays the month of `selectedDate`. If `selectedDate` is `null`, it defaults to the current month (`DateTime.now()`).

### Pre-selected Date

```dart
Calendar(
  selectedDate: DateTime(2026, 3, 15),
  onDateSelected: (date) => handleDateSelection(date),
)
```

### In a Card (Web)

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Select Date')),
    ),
    CardContent(
      child: Calendar(
        selectedDate: selectedDate,
        onDateSelected: (date) => setState(() => selectedDate = date),
      ),
    ),
  ],
)
```

### Date Picker with Display (Web)

```dart
class DatePickerExample extends StatefulComponent {
  @override
  State<DatePickerExample> createState() => _DatePickerExampleState();
}

class _DatePickerExampleState extends State<DatePickerExample> {
  DateTime? selectedDate;

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield div(
      [
        div(
          [
            Component.text(
              selectedDate != null
                  ? 'Selected: ${selectedDate!.year}-${selectedDate!.month}-${selectedDate!.day}'
                  : 'No date selected',
            ),
          ],
          classes: 'text-sm text-muted-foreground mb-4',
        ),
        Calendar(
          selectedDate: selectedDate,
          onDateSelected: (date) => setState(() => selectedDate = date),
        ),
      ],
    );
  }
}
```

### Side by Side Date Range (Web)

```dart
div(
  [
    div(
      [
        Component.element(
          tag: 'label',
          classes: 'text-sm font-medium',
          children: [Component.text('Start Date')],
        ),
        Calendar(
          selectedDate: startDate,
          onDateSelected: (date) => setState(() => startDate = date),
        ),
      ],
    ),
    div(
      [
        Component.element(
          tag: 'label',
          classes: 'text-sm font-medium',
          children: [Component.text('End Date')],
        ),
        Calendar(
          selectedDate: endDate,
          onDateSelected: (date) => setState(() => endDate = date),
        ),
      ],
    ),
  ],
  classes: 'flex gap-4',
)
```

## Common Patterns

### State Management

Both platforms use `setState` for date selection state. Track selected date(s) as nullable instance variables and update them in the selection callback.

### Single vs Range Selection

| Feature | Flutter | Web |
|---------|---------|-----|
| Single date | `SingleCalendarValue` wrapper | Direct `DateTime?` parameter |
| Range selection | `RangeCalendarValue(start, end)` | Two side-by-side `Calendar` instances |
| Callback | `onChanged: (CalendarValue)` | `onDateSelected: (DateTime)` |
| Null state | `value: null` | `selectedDate: null` |

### Date Constraints

| Feature | Flutter | Web |
|---------|---------|-----|
| Min/max date | Via theme/config | `minDate` / `maxDate` parameters |
| View modes | `CalendarView` enum (day/month/year/decade) | Month view only |
| Layout variants | `CalendarViewType` enum (grid/list/compact) | Grid only |

### Display in Card

Both platforms support embedding the calendar in a `Card` component. Flutter uses `child:` with `Column`, while Web uses `CardHeader`/`CardContent` with `children:`.

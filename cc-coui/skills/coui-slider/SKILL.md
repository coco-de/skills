---
name: coui-slider
description: Activate when creating range sliders, value sliders, or controlled sliders in CoUI Flutter or Web using Slider, SliderController, or SliderValue.
---

# CoUI Slider

## Overview

Value selection via draggable thumbs. Supports single values, ranges, and discrete steps.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Slider

```dart
double value = 0.5;

Slider(
  value: SliderValue.single(value),
  onChanged: (v) {
    setState(() => value = v.value);
  },
)
```

### SliderValue

Represents slider state for single or range values:

```dart
// Single value
SliderValue.single(0.5)

// Range value (two thumbs)
SliderValue.ranged(0.2, 0.8)
```

### With Min/Max

```dart
Slider(
  value: SliderValue.single(50),
  min: 0,
  max: 100,
  onChanged: (v) {
    setState(() => currentValue = v.value);
  },
)
```

### With Divisions (Steps)

```dart
Slider(
  value: SliderValue.single(50),
  min: 0,
  max: 100,
  divisions: 10,  // steps of 10
  onChanged: (v) {
    setState(() => currentValue = v.value);
  },
)
```

### Range Slider

```dart
double start = 20;
double end = 80;

Slider(
  value: SliderValue.ranged(start, end),
  min: 0,
  max: 100,
  onChanged: (v) {
    setState(() {
      start = v.start;
      end = v.end;
    });
  },
)
```

### SliderController

Reactive controller for programmatic control:

```dart
final controller = SliderController(SliderValue.single(0.5));

// Listen to changes
controller.addListener(() {
  print('Value: ${controller.value}');
});

// Programmatic control
controller.setValue(0.75);
controller.setRange(0.2, 0.8);
```

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `value` | `SliderValue` (required) | Current slider value |
| `onChanged` | `ValueChanged<SliderValue>?` | Change callback |
| `min` | `double` | Minimum value (default: 0.0) |
| `max` | `double` | Maximum value (default: 1.0) |
| `divisions` | `int?` | Number of discrete steps |

### Volume Control Pattern

```dart
Row(
  children: [
    const Icon(Icons.volume_down),
    Gap.h(8),
    Expanded(
      child: Slider(
        value: SliderValue.single(volume),
        onChanged: (v) => setState(() => volume = v.value),
      ),
    ),
    Gap.h(8),
    const Icon(Icons.volume_up),
  ],
)
```

### Price Range Filter Pattern

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Price Range').bold,
    Gap.v(8),
    Slider(
      value: SliderValue.ranged(minPrice, maxPrice),
      min: 0,
      max: 1000,
      divisions: 100,
      onChanged: (v) {
        setState(() {
          minPrice = v.start;
          maxPrice = v.end;
        });
      },
    ),
    Gap.v(4),
    Text('\$${minPrice.round()} - \$${maxPrice.round()}').small.base200,
  ],
)
```

## Web (coui_web)

> **Not yet implemented.** Slider is currently Flutter-only. Web implementation is planned.

## Common Patterns

- Use `SliderValue.single()` for single values, `SliderValue.ranged()` for ranges.
- Set `divisions` for discrete step values.
- Use `SliderController` for programmatic control and value listening.

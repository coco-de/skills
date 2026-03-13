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

### Hint Value

```dart
Slider(
  value: SliderValue.single(volume),
  hintValue: recommendedVolume,
  onChanged: (v) => setState(() => volume = v.value),
)
```

Provides a visual preview of a recommended value on the track.

### Keyboard Navigation

Configure arrow key step size:

```dart
Slider(
  value: SliderValue.single(50),
  min: 0,
  max: 100,
  increaseStep: 5,
  decreaseStep: 5,
  onChanged: (v) => setState(() => currentValue = v.value),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Slider

Uses native HTML `<input type="range">` with custom visual overlay:

```dart
Slider(
  value: volume,
  onChange: (value) => handleVolumeChange(value),
  min: 0,
  max: 100,
)
```

### With Step

```dart
Slider(
  value: rating,
  onChange: (value) => handleRating(value),
  min: 0,
  max: 5,
  step: 1,
)
```

### Show Value Label

```dart
Slider(
  value: temperature,
  onChange: (value) => handleTemp(value),
  min: 16,
  max: 30,
  showValue: true,
)
```

### Web Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `double` | required | Current value |
| `onChange` | `ValueChanged<double>?` | `null` | Value change callback |
| `min` | `double` | `0` | Minimum value |
| `max` | `double` | `100` | Maximum value |
| `step` | `double?` | `null` | Step size |
| `showValue` | `bool` | `false` | Display current value label |

## Common Patterns

### Platform Differences

| Feature | Flutter | Web |
|---------|---------|-----|
| Value model | `SliderValue` (single/ranged) | `double` single only |
| Controller | `SliderController` (ValueNotifier) | None |
| Range slider | `SliderValue.ranged()` | Not supported |
| Divisions | `divisions` + tick marks | `step` attribute |
| Hint value | `hintValue` visual preview | Not supported |
| Track rendering | Custom `GestureDetector` + painting | `<input type="range">` + CSS overlay |
| Keyboard | `increaseStep`/`decreaseStep` custom | Browser native |
| Value display | Via external widget | `showValue: true` |
| Theme | `SliderTheme` (trackHeight, thumbSize) | Tailwind CSS |

### Shared Concepts

- Use `SliderValue.single()` for single values, `SliderValue.ranged()` for ranges (Flutter).
- Set `divisions` (Flutter) or `step` (Web) for discrete step values.
- Use `SliderController` for programmatic control and value listening (Flutter only).

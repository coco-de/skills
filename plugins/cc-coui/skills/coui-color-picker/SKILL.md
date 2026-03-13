---
name: coui-color-picker
description: Activate when creating color pickers, color selectors, hex/rgb/hsl color inputs, or color swatches using ColorPicker, ColorPicker, ColorFormat in CoUI Flutter or CoUI Web.
---

# CoUI ColorPicker

## Overview

The ColorPicker is a color selection component that allows selecting and editing colors in various formats (HEX, RGB, HSL). It supports alpha channel, preset colors, and color code input fields. Flutter uses `ColorPicker` while Web uses `ColorPicker`.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Color Picker

```dart
ColorPicker(
  value: selectedColor,
  onChanged: handleColorChanged,
)
```

### With Alpha Channel and Input

```dart
ColorPicker(
  value: selectedColor,
  onChanged: handleColorChanged,
  showAlpha: true,
  showInput: true,
  format: ColorFormat.hex,
)
```

### With Preset Colors

```dart
ColorPicker(
  value: selectedColor,
  onChanged: handleColorChanged,
  presetColors: [
    Colors.red,
    Colors.green,
    Colors.blue,
    Colors.yellow,
    Colors.purple,
  ],
)
```

### HEX Format

```dart
ColorPicker(
  value: brandColor,
  onChanged: handleBrandColorChanged,
  format: ColorFormat.hex,
  showInput: true,
)
```

### RGB Format

```dart
ColorPicker(
  value: fillColor,
  onChanged: handleFillColorChanged,
  format: ColorFormat.rgb,
  showAlpha: true,
)
```

### HSL Format

```dart
ColorPicker(
  value: themeColor,
  onChanged: handleThemeColorChanged,
  format: ColorFormat.hsl,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `Color` | required | Currently selected color |
| `onChanged` | `ValueChanged<Color>?` | `null` | Color change callback |
| `showAlpha` | `bool` | `false` | Display alpha channel slider |
| `showInput` | `bool` | `true` | Display color code input field |
| `presetColors` | `List<Color>?` | `null` | List of preset colors |
| `format` | `ColorFormat` | `ColorFormat.hex` | Color display format (hex/rgb/hsl) |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic ColorPicker

```dart
ColorPicker(
  value: selectedColor,
  onChanged: handleColorChanged,
)
```

### With Alpha, Input, and Presets

```dart
ColorPicker(
  value: selectedColor,
  onChanged: handleColorChanged,
  showAlpha: true,
  showInput: true,
  format: 'hex',
  presetColors: ['#FF0000', '#00FF00', '#0000FF'],
)
```

## Common Patterns

### Format Variants

| Format | Flutter | Web |
|--------|---------|-----|
| HEX | `ColorFormat.hex` | `'hex'` |
| RGB | `ColorFormat.rgb` | `'rgb'` |
| HSL | `ColorFormat.hsl` | `'hsl'` |

### Platform Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Component | `ColorPicker` | `ColorPicker` |
| Color type | `Color` object | `Color` or hex string |
| Format enum | `ColorFormat.hex` | `'hex'` (string) |
| Preset colors | `List<Color>` | `List<String>` (hex strings) |

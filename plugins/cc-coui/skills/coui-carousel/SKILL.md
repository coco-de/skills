---
name: coui-carousel
description: Activate when creating image carousels, slideshows, content sliders with autoplay, indicators, or arrow navigation using Carousel/CarouselItem (Flutter) or Carousel/CarouselItem (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Carousel

## Overview

The Carousel component displays images or arbitrary content in slide format. It supports autoplay, dot indicators, arrow navigation, looping, and slide change callbacks.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
Carousel(
  items: [
    CarouselItem(child: Image.network('url1')),
    CarouselItem(child: Image.network('url2')),
  ],
  showIndicator: true,
  showArrows: true,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<CarouselItem>` | required | Slides to display |
| `autoPlay` | `bool` | `false` | Enable automatic advancement |
| `interval` | `Duration` | `Duration(seconds: 4)` | Time between auto-advance |
| `showIndicator` | `bool` | `true` | Display bottom dot indicators |
| `showArrows` | `bool` | `true` | Display navigation arrows |
| `onChanged` | `void Function(int)?` | `null` | Callback when slide changes |
| `initialIndex` | `int` | `0` | Starting slide position |
| `loop` | `bool` | `true` | Enable infinite cycling |

### Auto-Advancing Carousel

```dart
Carousel(
  items: items,
  autoPlay: true,
  interval: Duration(seconds: 3),
  onChanged: (index) => handleSlideChange(index),
)
```

### Indicators Only (No Arrows)

```dart
Carousel(
  items: items,
  showArrows: false,
  showIndicator: true,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Carousel(
  items: [
    CarouselItem(child: Image.network('url1')),
    CarouselItem(child: Image.network('url2')),
  ],
  showIndicator: true,
  showArrows: true,
)
```

### Parameters

Same parameter structure as Flutter with identical property names and defaults.

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Main widget | `Carousel` | `Carousel` |
| Item widget | `CarouselItem` | `CarouselItem` |
| API | Identical parameters | Identical parameters |

### When to Use

- Image galleries and product showcases
- Onboarding screens with multiple steps
- Hero banners with rotating content
- Testimonial or feature highlight sliders

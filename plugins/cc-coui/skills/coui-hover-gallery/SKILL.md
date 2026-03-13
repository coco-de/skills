---
name: coui-hover-gallery
description: Activate when creating hover image galleries, product image previews, or sequential image transition displays on hover using CouiHoverGallery (Flutter) or HoverGallery (Web) in CoUI Flutter or CoUI Web.
---

# CoUI HoverGallery

## Overview

HoverGallery is a gallery component that sequentially transitions between images when the user hovers over it. It is designed for product previews, portfolio cards, and similar use cases requiring image preview effects.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiHoverGallery(
  images: [
    'https://example.com/image1.jpg',
    'https://example.com/image2.jpg',
    'https://example.com/image3.jpg',
  ],
  width: 300,
  height: 200,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `images` | `List<String>` | required | Collection of image URLs |
| `width` | `double` | required | Gallery container width |
| `height` | `double` | required | Gallery container height |
| `borderRadius` | `double` | `0.0` | Corner roundness |
| `imageBuilder` | `Widget Function(String, int)?` | `null` | Custom image widget builder |
| `interval` | `Duration` | `400ms` | Time between image transitions |
| `fit` | `BoxFit` | `BoxFit.cover` | Image scaling behavior |

### With Rounded Corners

```dart
CouiHoverGallery(
  images: productImages,
  width: 240,
  height: 240,
  borderRadius: 12,
)
```

### Custom Image Builder

```dart
CouiHoverGallery(
  images: productImages,
  width: 320,
  height: 200,
  imageBuilder: (url, index) => Image.network(
    url,
    fit: BoxFit.cover,
  ),
)
```

### Product Card Integration

```dart
CouiCard(
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      CouiHoverGallery(
        images: product.images,
        width: double.infinity,
        height: 200,
        borderRadius: 8,
      ),
      Padding(
        padding: const EdgeInsets.all(12),
        child: Text(product.name),
      ),
    ],
  ),
)
```

### Grid Layout Pattern

```dart
GridView.builder(
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 3,
    mainAxisSpacing: 12,
    crossAxisSpacing: 12,
  ),
  itemBuilder: (context, index) => CouiHoverGallery(
    images: portfolioItems[index].screenshots,
    width: 200,
    height: 150,
    borderRadius: 8,
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
HoverGallery(
  images: [
    'https://example.com/product-1.jpg',
    'https://example.com/product-2.jpg',
    'https://example.com/product-3.jpg',
  ],
  width: 300,
  height: 200,
)
```

### With Border Radius

```dart
HoverGallery(
  images: productImages,
  width: 240,
  height: 240,
  borderRadius: 12,
)
```

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiHoverGallery` | `HoverGallery` |
| API | Identical parameters | Identical parameters |

### When to Use

- Product image previews in e-commerce
- Portfolio card hover effects
- Image gallery thumbnails
- Catalog grid displays

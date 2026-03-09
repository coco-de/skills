---
name: coui-text
description: Activate when styling text in CoUI Flutter or Web using text extensions like .bold, .large, .base200, .primary, .x2Large, .muted, or chaining text modifiers.
---

# CoUI Text

## Overview

Text styling via chainable extensions for size, weight, color, and decoration.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Text Extensions

coui_flutter provides extensions on `Widget` for text styling. Chain them for combined effects.

### Size Extensions

```dart
const Text('Extra Small').xs       // xs - extra small
const Text('Small').sm             // sm - small
const Text('Base').base            // base - default
const Text('Large').lg             // lg - large
const Text('XLarge').xLarge        // xLarge
const Text('2XLarge').x2Large      // x2Large
const Text('3XLarge').x3Large      // x3Large
const Text('4XLarge').x4Large      // x4Large
const Text('5XLarge').x5Large      // x5Large
const Text('6XLarge').x6Large      // x6Large
const Text('7XLarge').x7Large      // x7Large
```

Note: LLM guide uses `.xSmall`, `.small`, `.large` etc. but actual extensions are `.xs`, `.sm`, `.lg`. Both forms may work depending on the version. When in doubt use `.xs`, `.sm`, `.lg`.

### Weight Extensions

```dart
const Text('Bold').bold            // FontWeight.w700
const Text('SemiBold').semiBold    // FontWeight.w600
const Text('Medium').medium        // FontWeight.w500
const Text('Regular').regular      // FontWeight.w400
const Text('Light').light          // FontWeight.w300
```

### Color Extensions

```dart
const Text('Muted').base200         // Muted/secondary color
const Text('Primary').primary       // Primary brand color
const Text('Destructive').destructive // Error/danger color
const Text('Foreground').primaryForeground // Primary foreground
```

### Decoration Extensions

```dart
const Text('Underline').underline    // Text underline
const Text('Italic').italic          // Italic style
const Text('Strike').lineThrough     // Strikethrough
```

### Font Family Extensions

```dart
const Text('Sans').sans   // Sans-serif font
const Text('Code').mono   // Monospace font
```

### Chaining

Chain multiple modifiers. Recommended order: size -> weight -> color.

```dart
const Text('Page Title').x3Large.bold
const Text('Section Header').lg.semiBold
const Text('Body Text').base
const Text('Caption').sm.base200
const Text('Error').sm.bold.destructive
const Text('Code Block').mono.sm

// Complex chains
const Text('Dashboard').x3Large.bold.primary
const Text('Welcome back!').base.base200
const Text('5 new notifications').sm.medium
```

### Common Typography Patterns

#### Page Header
```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Dashboard').x3Large.bold,
    Gap.v(4),
    const Text('Welcome back, John!').base200,
  ],
)
```

#### Section Header
```dart
const Text('Recent Activity').lg.semiBold
```

#### Card Title
```dart
const Text('Project Name').bold
```

#### Helper/Caption Text
```dart
const Text('Last updated 2 hours ago').xs.base200
```

#### Error Message
```dart
const Text('Invalid email address').sm.destructive
```

#### Inline Code
```dart
const Text('flutter run').mono.sm
```

### Full Page Typography Example

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Dashboard').x3Large.bold,
    Gap.v(4),
    const Text('Overview of your account').base200,
    Gap.v(24),
    const Text('Statistics').lg.semiBold,
    Gap.v(12),
    const Text('Total Users: 1,234').base,
    Gap.v(4),
    const Text('+12% from last month').sm.base200,
    Gap.v(24),
    const Text('Recent Activity').lg.semiBold,
    Gap.v(12),
    const Text('John created a new project').sm,
    Gap.v(4),
    const Text('2 minutes ago').xs.base200,
  ],
)
```

## Web (coui_web)

> **Not yet implemented.** Text styling extensions are currently Flutter-only. Web implementation is planned.

## Common Patterns

- Chain order: size -> weight -> color (e.g., `.x2Large.bold.primary`).
- Use `.base200` for muted/secondary text.
- Use `.mono` for code snippets.
- Use `.destructive` for error messages.

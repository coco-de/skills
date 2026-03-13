---
name: coui-steps
description: Activate when creating read-only step progress indicators, delivery tracking displays, or stage completion visuals using Steps, Steps, StepsVariant, or StepsSize in CoUI Flutter or CoUI Web.
---

# CoUI Steps

## Overview

The Steps component is a read-only progress indicator that displays stage completion status. Unlike Stepper (which is interactive), Steps is purely visual and shows where a process currently stands without user interaction.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Number Variant (Default)

```dart
Steps(
  steps: ['Order Placed', 'Payment Done', 'Preparing', 'Shipping', 'Delivered'],
  current: 2,
  variant: StepsVariant.number,
)
```

### Dot Variant

```dart
Steps(
  steps: ['Step 1', 'Step 2', 'Step 3'],
  current: 1,
  variant: StepsVariant.dot,
  size: StepsSize.sm,
)
```

### Simple Variant

```dart
Steps(
  steps: ['Request', 'Review', 'Approval'],
  current: 0,
  variant: StepsVariant.simple,
)
```

### Key Classes

#### Steps

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `steps` | `List<String>` | required | List of stage names |
| `current` | `int` | required | Current stage index |
| `variant` | `StepsVariant` | `StepsVariant.number` | Display format |
| `size` | `StepsSize` | `StepsSize.md` | Size option |

### StepsVariant

| Value | Description |
|-------|-------------|
| `number` | Numbered circles for each step |
| `dot` | Small dot indicators |
| `simple` | Minimal text-based display |

### StepsSize

| Value | Description |
|-------|-------------|
| `sm` | Small |
| `md` | Medium (default) |
| `lg` | Large |

### Delivery Tracking Pattern

```dart
Card(
  child: Column(
    children: [
      Text('Order #12345', style: TextStyle(fontWeight: FontWeight.bold)),
      Gap.v(16),
      Steps(
        steps: ['Ordered', 'Confirmed', 'Shipped', 'Delivered'],
        current: 2,
        variant: StepsVariant.number,
      ),
    ],
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Steps

```dart
Steps(
  steps: ['Order Placed', 'Payment Done', 'Preparing', 'Delivered'],
  current: 2,
  variant: 'number',
)
```

### Dot Variant

```dart
Steps(
  steps: ['Step 1', 'Step 2', 'Step 3'],
  current: 1,
  variant: 'dot',
  size: 'sm',
)
```

## Common Patterns

### Steps vs Stepper

| Feature | Steps | Stepper |
|---------|-------|---------|
| Interaction | Read-only | Interactive (clickable) |
| Use case | Status display, tracking | Multi-step forms, wizards |
| Callback | None | `onStepTap` |

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Variant type | `StepsVariant.number` enum | `'number'` string |
| Size type | `StepsSize.md` enum | `'md'` string |

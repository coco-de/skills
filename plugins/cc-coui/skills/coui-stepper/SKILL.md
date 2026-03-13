---
name: coui-stepper
description: Activate when creating multi-step forms, wizard flows, step-by-step processes, or interactive step navigation using Stepper, Stepper, StepItem, or StepperOrientation in CoUI Flutter or CoUI Web.
---

# CoUI Stepper

## Overview

The Stepper component displays and navigates through multi-step processes such as registration, payment, or onboarding flows. It shows current progress and allows users to move between stages interactively.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Horizontal Stepper

```dart
Stepper(
  currentStep: _currentStep,
  onStepTap: (step) {
    setState(() => _currentStep = step);
  },
  steps: [
    StepItem(title: 'Basic Info', subtitle: 'Name and email'),
    StepItem(title: 'Address', subtitle: 'Shipping address'),
    StepItem(title: 'Payment', subtitle: 'Card details'),
    StepItem(title: 'Confirm', subtitle: 'Review order'),
  ],
)
```

### Vertical Stepper

```dart
Stepper(
  currentStep: _currentStep,
  onStepTap: (step) {
    setState(() => _currentStep = step);
  },
  orientation: StepperOrientation.vertical,
  steps: [
    StepItem(title: 'Create Account'),
    StepItem(title: 'Set Up Profile'),
    StepItem(title: 'Complete'),
  ],
)
```

### Key Classes

#### Stepper

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `steps` | `List<StepItem>` | required | Step list |
| `currentStep` | `int` | required | Current step index |
| `onStepTap` | `ValueChanged<int>?` | `null` | Step tap callback |
| `orientation` | `StepperOrientation` | `horizontal` | Layout direction |

#### StepItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `String` | required | Step title |
| `subtitle` | `String?` | `null` | Optional subtitle |

### Checkout Flow Pattern

```dart
Column(
  children: [
    Stepper(
      currentStep: _currentStep,
      onStepTap: (step) => setState(() => _currentStep = step),
      steps: [
        StepItem(title: 'Cart'),
        StepItem(title: 'Shipping'),
        StepItem(title: 'Payment'),
        StepItem(title: 'Done'),
      ],
    ),
    Expanded(child: _stepPages[_currentStep]),
    Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        if (_currentStep > 0)
          OutlineButton(
            onPressed: () => setState(() => _currentStep--),
            child: const Text('Back'),
          ),
        PrimaryButton(
          onPressed: () => setState(() => _currentStep++),
          child: Text(_currentStep < 3 ? 'Next' : 'Complete'),
        ),
      ],
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Stepper

```dart
Stepper(
  currentStep: currentStep,
  onStepTap: handleStepTapped,
  steps: [
    StepItem(title: 'Basic Info'),
    StepItem(title: 'Address'),
    StepItem(title: 'Payment'),
    StepItem(title: 'Confirm'),
  ],
)
```

### Vertical Variant

```dart
Stepper(
  currentStep: currentStep,
  orientation: 'vertical',
  steps: checkoutSteps,
)
```

## Common Patterns

### Stepper vs Steps

| Feature | Stepper | Steps |
|---------|---------|-------|
| Interactivity | Clickable steps (`onStepTap`) | Read-only display |
| Use case | Multi-step forms, wizards | Progress indicators |
| Navigation | Users can jump between steps | No user interaction |

### API Consistency

- Both Flutter and Web use `steps`, `currentStep`, `onStepTap`, and `orientation`.
- Flutter uses `StepperOrientation.vertical` enum; Web uses `'vertical'` string.

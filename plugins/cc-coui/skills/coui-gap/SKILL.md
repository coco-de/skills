---
name: coui-gap
description: Activate when adding consistent spacing between widgets, using design-token gaps, or inserting blank space in Row/Column/Flex using Gap, Gap.sm, Gap.md, Gap.lg, or Gap.v/Gap.h in CoUI Flutter or CoUI Web.
---

# CoUI Gap

## Overview

The Gap component is a spacing utility that adds consistent gaps between child widgets within layout widgets like Row, Column, and Flex. It uses design tokens for standardized spacing across the application.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Vertical Spacing in Column

```dart
Column(
  children: [
    const Text('Title'),
    const Gap.md(),
    const Text('Content'),
    const Gap.lg(),
    CouiButton(
      onPressed: () {},
      child: const Text('Submit'),
    ),
  ],
)
```

### Horizontal Spacing in Row

```dart
Row(
  children: [
    const Icon(Icons.person),
    const Gap.sm(),
    const Text('Username'),
    const Spacer(),
    const Gap.sm(),
    CouiButton(
      onPressed: () {},
      child: const Text('Edit'),
    ),
  ],
)
```

### Custom Size

```dart
const Gap(size: 24)
```

### Key Classes

#### Gap

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `size` | `double` | required | Spacing size in pixels |
| `direction` | `Axis?` | `null` | Gap direction (auto-detects parent) |

### Named Constructors

| Constructor | Size | Use Case |
|-------------|------|----------|
| `Gap.xs()` | 4px | Very small spacing |
| `Gap.sm()` | 8px | Small spacing |
| `Gap.md()` | 16px | Default spacing |
| `Gap.lg()` | 24px | Large spacing |
| `Gap.xl()` | 32px | Extra large spacing |

### Static Helpers

Convenience methods for explicit direction:

```dart
Gap.v(16)  // Vertical gap of 16px
Gap.h(8)   // Horizontal gap of 8px
```

### Form Layout Pattern

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Name'),
    const Gap.xs(),
    TextField(placeholder: Text('Enter your name')),
    const Gap.md(),
    const Text('Email'),
    const Gap.xs(),
    TextField(placeholder: Text('Enter your email')),
    const Gap.lg(),
    CouiButton(
      onPressed: () {},
      child: const Text('Submit'),
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Usage

The web implementation provides the same named constructors and sizing approach:

```dart
div(
  [
    Component.text('Title'),
    Gap.md(),
    Component.text('Content'),
    Gap.lg(),
    Button(child: Component.text('Submit')),
  ],
  classes: 'flex flex-col',
)
```

## Common Patterns

### Spacing Scale

| Token | Size | Typical Use |
|-------|------|-------------|
| `xs` | 4px | Tight spacing (label-to-input) |
| `sm` | 8px | Compact spacing (icon-to-text) |
| `md` | 16px | Standard spacing (form fields) |
| `lg` | 24px | Generous spacing (sections) |
| `xl` | 32px | Wide spacing (major sections) |

### API Consistency

- Both Flutter and Web use the same named constructors: `Gap.xs()`, `Gap.sm()`, `Gap.md()`, `Gap.lg()`, `Gap.xl()`.
- Custom sizes are supported via `Gap(size: value)`.
- Gap auto-detects parent direction when `direction` is null.

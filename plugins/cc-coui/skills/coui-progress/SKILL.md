---
name: coui-progress
description: Activate when creating progress bars, loading indicators, spinners, or circular/radial progress displays using Progress, LinearProgressIndicator, CircularProgressIndicator, Loading, or RadialProgress in coui_flutter or coui_web.
---

# CoUI Progress

## Overview

Progress components display task completion, loading states, and metrics across both Flutter and Web platforms. Each platform provides linear progress bars and circular/spinner indicators with platform-appropriate APIs.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Progress

Customizable linear progress bar:

```dart
Progress(value: 0.6)
```

#### With Min/Max

```dart
Progress(
  value: 60,
  min: 0,
  max: 100,
)
```

#### Key Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `double` (required) | - | Current progress |
| `min` | `double` | 0.0 | Minimum value |
| `max` | `double` | 1.0 | Maximum value |
| `color` | `Color?` | primary | Progress bar color |
| `backgroundColor` | `Color?` | muted | Track color |
| `borderRadius` | `BorderRadiusGeometry?` | theme default | Corner radius |
| `minHeight` | `double?` | 8.0 | Bar height |

### LinearProgressIndicator

Linear loading indicator:

```dart
// Determinate
LinearProgressIndicator(value: 0.75)

// Indeterminate (animated)
const LinearProgressIndicator()
```

### CircularProgressIndicator

Circular loading spinner:

```dart
// Determinate
CircularProgressIndicator(value: 0.5)

// Indeterminate (animated)
const CircularProgressIndicator()
```

### ProgressTheme

```dart
const ProgressTheme(
  color: Colors.blue,
  backgroundColor: Colors.grey,
  borderRadius: BorderRadius.circular(4),
  minHeight: 6.0,
)
```

### File Upload Pattern

```dart
Card(
  padding: const EdgeInsets.all(16),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          const Text('Uploading file...').sm,
          Text('${(progress * 100).round()}%').sm.base200,
        ],
      ),
      Gap.v(8),
      Progress(value: progress),
    ],
  ),
)
```

### Loading State Pattern

```dart
isLoading
    ? const Center(child: CircularProgressIndicator())
    : MyContent()
```

### RadialProgress (Flutter)

```dart
RadialProgress(
  value: 0.75,
  child: const Text('75%'),
)
```

Custom painter renders background circle + progress arc, starting at 12 o'clock. Default size: 80px, stroke: 8px.

### Multi-Segment Progress (Flutter)

```dart
Progress.multi(
  segments: [
    ProgressSegment(value: 0.3, color: Colors.green),
    ProgressSegment(value: 0.2, color: Colors.orange),
    ProgressSegment(value: 0.1, color: Colors.red),
  ],
)
```

### Multi-Step Progress Pattern

```dart
Column(
  crossAxisAlignment: CrossAxisAlignment.start,
  children: [
    const Text('Storage Usage').sm.bold,
    Gap.v(8),
    Progress(
      value: 7.2,
      max: 10.0,
      color: Colors.blue,
    ),
    Gap.v(4),
    const Text('7.2 GB of 10 GB used').xs.base200,
  ],
)
```

### Stats Dashboard Pattern

```dart
Row(
  children: [
    Expanded(
      child: Column(
        children: [
          const Text('CPU').sm.base200,
          Gap.v(4),
          Progress(value: 0.72, color: Colors.orange),
          Gap.v(2),
          const Text('72%').xs,
        ],
      ),
    ),
    Gap.h(16),
    Expanded(
      child: Column(
        children: [
          const Text('Memory').sm.base200,
          Gap.v(4),
          Progress(value: 0.45, color: Colors.green),
          Gap.v(2),
          const Text('45%').xs,
        ],
      ),
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Progress (Linear Bar)

```dart
Progress(value: 60)  // 60% complete
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `double` | `0` | Current progress value |
| `min` | `double` | `0` | Minimum value |
| `max` | `double` | `100` | Maximum value |

#### Custom Range

```dart
Progress(value: 3, min: 0, max: 10)
```

#### Accessibility

Progress automatically includes:
- `role="progressbar"`
- `aria-valuenow`, `aria-valuemin`, `aria-valuemax`

#### Examples

```dart
// File upload progress
Progress(value: uploadPercent)

// Step progress
Progress(value: 2, min: 0, max: 5)

// Custom styled
Progress(
  value: 75,
  classes: 'h-2',
)
```

### Loading (Spinner)

```dart
Loading()          // Default 16px spinner
Loading(size: 24)  // Custom size
Loading(size: 32)  // Larger spinner
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `size` | `int` | `16` | Spinner size in pixels |

#### Examples

```dart
// In a button
Button.primary(
  enabled: false,
  leading: Loading(size: 16),
  child: Component.text('Loading...'),
)

// Centered loading state
div(
  [Loading(size: 32)],
  classes: 'flex items-center justify-center p-8',
)

// With text
div(
  [
    Loading(size: 24),
    Component.text('Loading data...'),
  ],
  classes: 'flex items-center gap-2',
)
```

### RadialProgress (Circular)

```dart
RadialProgress(value: 75, showValueText: true)
```

#### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `double` | required | Progress 0-100 |
| `showValueText` | `bool` | `false` | Show percentage text |
| `size` | `String?` | `null` | Diameter CSS value (e.g., "12rem") |
| `thickness` | `String?` | `null` | Ring thickness (e.g., "2px") |
| `children` | `List<Component>?` | `null` | Custom inner content |
| `style` | `List<RadialProgressStyling>?` | `null` | Styling utilities |

#### Custom Size and Thickness

```dart
RadialProgress(
  value: 60,
  size: '8rem',
  thickness: '4px',
  showValueText: true,
)
```

#### Custom Inner Content

```dart
RadialProgress(
  value: 80,
  size: '10rem',
  children: [
    div(
      [
        span([Component.text('80')], classes: 'text-2xl font-bold'),
        span([Component.text('points')], classes: 'text-xs'),
      ],
      classes: 'flex flex-col items-center',
    ),
  ],
)
```

#### Accessibility

RadialProgress includes:
- `role="progressbar"`
- `aria-valuenow`

### Progress Dashboard Example

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Project Status')),
    ),
    CardContent(
      children: [
        div(
          [
            div(
              [
                Component.text('Tasks'),
                Component.text('75%'),
              ],
              classes: 'flex justify-between text-sm mb-1',
            ),
            Progress(value: 75),
          ],
          classes: 'space-y-1',
        ),
        div(
          [
            div(
              [
                Component.text('Budget'),
                Component.text('40%'),
              ],
              classes: 'flex justify-between text-sm mb-1',
            ),
            Progress(value: 40),
          ],
          classes: 'space-y-1 mt-4',
        ),
        div(
          [
            RadialProgress(value: 75, showValueText: true, size: '5rem'),
            RadialProgress(value: 40, showValueText: true, size: '5rem'),
          ],
          classes: 'flex gap-4 mt-6 justify-center',
        ),
      ],
    ),
  ],
)
```

### Loading States Pattern

```dart
// Conditional loading
if (isLoading)
  div(
    [Loading(size: 32)],
    classes: 'flex justify-center p-8',
  )
else
  div([/* actual content */])
```

## Common Patterns

### API Differences

| Feature | Flutter | Web |
|---------|---------|-----|
| Linear progress | `Progress(value: 0.6)` | `Progress(value: 60)` |
| Default max | `1.0` | `100` |
| Spinner | `CircularProgressIndicator()` | `Loading()` |
| Circular progress | `CircularProgressIndicator(value: 0.5)` | `RadialProgress(value: 50)` |
| Theming | `ProgressTheme` | CSS classes |
| Indeterminate linear | `LinearProgressIndicator()` | Not available |

### Shared Concepts

- Both platforms provide a `Progress` widget with `value`, `min`, `max` parameters.
- Both support determinate (with value) and indeterminate (spinner) loading states.
- Both follow the pattern of wrapping progress indicators with labels and percentage text for dashboard UIs.

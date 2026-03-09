---
name: coui-card
description: Activate when creating card containers for grouping related content. Covers Flutter Card/SurfaceCard with borders, shadows, surface effects and Web Card with header, title, description, content, footer sections, and hoverable effects.
---

# CoUI Card

## Overview

Card is a container component for grouping related content with visual boundaries. Flutter provides `Card` and `SurfaceCard` with border/shadow/blur styling. Web provides a structured card with `CardHeader`, `CardTitle`, `CardDescription`, `CardContent`, and `CardFooter` sub-components.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Card

Basic container for grouping related content:

```dart
Card(
  child: Column(
    children: [
      const Text('Title').bold.large,
      Gap.v(8),
      const Text('Card content here'),
    ],
  ),
)
```

#### With Padding

```dart
Card(
  padding: const EdgeInsets.all(16),
  child: const Text('Padded card'),
)
```

### SurfaceCard

Card with blur/opacity surface effects:

```dart
SurfaceCard(
  child: const Text('Surface effect card'),
)

SurfaceCard(
  surfaceBlur: 10.0,
  surfaceOpacity: 0.8,
  borderRadius: BorderRadius.circular(12),
  child: const Text('Blurred card'),
)
```

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Card content |
| `padding` | `EdgeInsetsGeometry?` | Internal padding |
| `borderRadius` | `BorderRadiusGeometry?` | Corner radius |
| `borderColor` | `Color?` | Border color |
| `borderWidth` | `double?` | Border width |
| `filled` | `bool` | Fill background |
| `fillColor` | `Color?` | Background color |
| `boxShadow` | `List<BoxShadow>?` | Shadow effects |
| `clipBehavior` | `Clip` | Clip behavior |

SurfaceCard adds:

| Parameter | Type | Description |
|-----------|------|-------------|
| `surfaceOpacity` | `double?` | Background opacity |
| `surfaceBlur` | `double?` | Blur intensity |

### Project Card Pattern

```dart
Card(
  padding: const EdgeInsets.all(24),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Create Project').semiBold,
      Gap.v(4),
      const Text('Deploy your new project quickly').base200.small,
      Gap.v(24),
      const TextField(placeholder: Text('Project name')),
      Gap.v(16),
      const TextField(placeholder: Text('Description')),
      Gap.v(24),
      Row(
        mainAxisAlignment: MainAxisAlignment.end,
        children: [
          OutlineButton(
            onPressed: () {},
            child: const Text('Cancel'),
          ),
          Gap.h(8),
          PrimaryButton(
            onPressed: () {},
            child: const Text('Create'),
          ),
        ],
      ),
    ],
  ),
)
```

### List Item Card Pattern

```dart
Card(
  child: Row(
    children: [
      Avatar(initials: 'JD'),
      Gap.h(12),
      Expanded(
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text('John Doe').bold,
            const Text('john@example.com').small.base200,
          ],
        ),
      ),
      IconButton.ghost(
        icon: const Icon(Icons.more_vert),
        onPressed: () {},
      ),
    ],
  ),
)
```

### Stats Card Pattern

```dart
Card(
  padding: const EdgeInsets.all(16),
  child: Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      const Text('Revenue').small.base200,
      Gap.v(4),
      const Text('\$45,231.89').x2Large.bold,
      Gap.v(4),
      const Text('+20.1% from last month').xSmall.base200,
    ],
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
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Card Title')),
    ),
    CardContent(
      child: Component.text('Card content goes here.'),
    ),
    CardFooter(
      child: Button.primary(child: Component.text('Action')),
    ),
  ],
)
```

### Components

#### Card (Container)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `children` | `List<Component>?` | `null` | Card sections |
| `child` | `Component?` | `null` | Single child alternative |
| `variant` | `CardVariant?` | `defaultVariant` | Visual variant |

#### Card.hoverable

Creates a card with hover effects:

```dart
Card.hoverable(
  children: [
    CardHeader(child: CardTitle(titleChild: Component.text('Hover me'))),
    CardContent(child: Component.text('This card has hover effects.')),
  ],
)
```

#### CardHeader

Flex column layout with padding (`p-6`):

```dart
CardHeader(
  children: [
    CardTitle(titleChild: Component.text('Title')),
    CardDescription(
      descriptionChild: Component.text('Description'),
    ),
  ],
)
```

#### CardTitle

Renders an `<h3>` with `text-2xl font-semibold`:

```dart
CardTitle(titleChild: Component.text('My Title'))
```

Parameter: `titleChild: Component` (required).

#### CardDescription

Renders a `<p>` with `text-sm text-muted-foreground`:

```dart
CardDescription(
  descriptionChild: Component.text('A brief description.'),
)
```

Parameter: `descriptionChild: Component` (required).

#### CardContent

Content area with padding (`p-6 pt-0`):

```dart
CardContent(
  children: [
    Input(placeholder: 'Name'),
    Input(placeholder: 'Email', type: 'email'),
  ],
)
```

#### CardFooter

Footer with flex layout (`flex items-center p-6 pt-0`):

```dart
CardFooter(
  children: [
    Button.outline(child: Component.text('Cancel')),
    Button.primary(child: Component.text('Save')),
  ],
)
```

### Complete Example

```dart
Card(
  children: [
    CardHeader(
      children: [
        CardTitle(titleChild: Component.text('Create Project')),
        CardDescription(
          descriptionChild: Component.text(
            'Deploy your new project in one click.',
          ),
        ),
      ],
    ),
    CardContent(
      children: [
        div(
          [
            Component.element(
              tag: 'label',
              classes: 'text-sm font-medium',
              children: [Component.text('Name')],
            ),
            Input(placeholder: 'Project name', name: 'name'),
          ],
          classes: 'space-y-2',
        ),
        div(
          [
            Component.element(
              tag: 'label',
              classes: 'text-sm font-medium',
              children: [Component.text('Framework')],
            ),
            Select(
              placeholder: 'Select a framework',
              options: [
                SelectOption('next', 'Next.js'),
                SelectOption('svelte', 'SvelteKit'),
                SelectOption('astro', 'Astro'),
              ],
            ),
          ],
          classes: 'space-y-2 mt-4',
        ),
      ],
    ),
    CardFooter(
      children: [
        Button.outline(child: Component.text('Cancel')),
        Button.primary(child: Component.text('Deploy')),
      ],
    ),
  ],
)
```

### Card Grid Layout

```dart
div(
  [
    Card(child: CardContent(child: Component.text('Card 1'))),
    Card(child: CardContent(child: Component.text('Card 2'))),
    Card(child: CardContent(child: Component.text('Card 3'))),
  ],
  classes: 'grid grid-cols-1 md:grid-cols-3 gap-4',
)
```

## Common Patterns

| Pattern | Flutter | Web |
|---------|---------|-----|
| Container | `Card(child: ...)` | `Card(children: [...])` |
| Title | Text extension `.bold.large` | `CardTitle(titleChild: ...)` |
| Description | Text extension `.base200.small` | `CardDescription(descriptionChild: ...)` |
| Content area | Direct `child` widget | `CardContent(child: ...)` |
| Footer actions | `Row` with buttons | `CardFooter(children: [...])` |
| Padding | `padding` parameter | Built-in via CSS classes |
| Hover effect | N/A (use GestureDetector) | `Card.hoverable(...)` |
| Surface blur | `SurfaceCard(surfaceBlur: ...)` | N/A |
| Grid layout | `GridView` / `Wrap` | `div([...], classes: 'grid ...')` |

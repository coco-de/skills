---
name: coui-accordion
description: Use when creating collapsible content sections, expandable panels, FAQ-style accordions, or toggle lists using Accordion and AccordionItem in CoUI Flutter or CoUI Web.
---

# CoUI Accordion

## Overview

The Accordion component provides collapsible content sections where users can expand and collapse panels. It is commonly used for FAQ lists, settings panels, and any UI that benefits from progressive disclosure. Both Flutter and Web implementations support single-expansion behavior, initial open state, and smooth transitions.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Accordion

Only one item can be expanded at a time:

```dart
Accordion(
  items: [
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('Section 1'),
      ),
      content: const Text('Content for section 1'),
    ),
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('Section 2'),
      ),
      content: const Text('Content for section 2'),
    ),
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('Section 3'),
      ),
      content: const Text('Content for section 3'),
    ),
  ],
)
```

### Initially Expanded Item

```dart
AccordionItem(
  trigger: AccordionTrigger(
    child: const Text('Open by default'),
  ),
  content: const Text('This section starts expanded'),
  expanded: true,
)
```

### Key Classes

#### Accordion

Container that manages mutual exclusion of expanded items.

| Parameter | Type | Description |
|-----------|------|-------------|
| `items` | `List<Widget>` (required) | List of AccordionItem widgets |

#### AccordionItem

Individual expandable section.

| Parameter | Type | Description |
|-----------|------|-------------|
| `trigger` | `AccordionTrigger` (required) | Clickable header |
| `content` | `Widget` (required) | Expandable content |
| `expanded` | `bool` | Initially expanded |

#### AccordionTrigger

Clickable header that toggles expansion.

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Header content |

### FAQ Pattern

```dart
Accordion(
  items: [
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('What is CoUI?'),
      ),
      content: const Text(
        'CoUI is a modern UI component library for Flutter '
        'with 80+ production-ready components.',
      ),
    ),
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('How do I install it?'),
      ),
      content: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Add to pubspec.yaml:'),
          Gap.v(8),
          const Text('coui_flutter: ^0.1.0').mono,
        ],
      ),
    ),
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('Is it free?'),
      ),
      content: const Text('Yes, CoUI is open source.'),
    ),
  ],
)
```

### Settings Panel Pattern

```dart
Accordion(
  items: [
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('Account Settings'),
      ),
      content: Column(
        children: [
          const TextField(placeholder: Text('Display name')),
          Gap.v(12),
          const TextField(placeholder: Text('Email')),
        ],
      ),
    ),
    AccordionItem(
      trigger: AccordionTrigger(
        child: const Text('Notifications'),
      ),
      content: Column(
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Email notifications'),
              Toggle(value: true, onChanged: (v) {}),
            ],
          ),
          Gap.v(8),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              const Text('Push notifications'),
              Toggle(value: false, onChanged: (v) {}),
            ],
          ),
        ],
      ),
    ),
  ],
)
```

### AccordionTheme

```dart
AccordionTheme(
  duration: Duration(milliseconds: 300),
  curve: Curves.easeInOut,
)
```

### Flutter Features

- **Single expansion**: Only one item open at a time (default behavior)
- **Multiple expansion**: Use the `allowMultiple` parameter for multiple items to be open simultaneously
- **Smooth animation**: Configurable expand/collapse animations via `AccordionTheme`
- **Visual dividers**: Automatic separators between items
- **Keyboard navigation**: Enter/Space to toggle, Tab to navigate between headers
- **Theming**: Via `AccordionTheme` (duration, curve, arrowIcon)

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Accordion(
  children: [
    AccordionItem(
      title: 'Is it accessible?',
      content: Component.text('Yes. It follows WAI-ARIA design patterns.'),
    ),
    AccordionItem(
      title: 'Is it styled?',
      content: Component.text('Yes. It uses Tailwind CSS for styling.'),
    ),
    AccordionItem(
      title: 'Is it animated?',
      content: Component.text('Yes. Transitions are built-in.'),
    ),
  ],
)
```

### Key Classes

#### Accordion

Container that holds AccordionItem children. Renders a full-width `<div>`.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `children` | `List<Component>` | required | AccordionItem components |

#### AccordionItem

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `String` | required | Header text |
| `content` | `Component` | required | Collapsible content |
| `isOpen` | `bool` | `false` | Whether item is expanded |

### Open by Default

```dart
AccordionItem(
  title: 'Open Section',
  content: Component.text('This section starts expanded.'),
  isOpen: true,
)
```

### Rendered Structure

Each AccordionItem renders:
- A `<button>` trigger with title text and chevron icon
- Content `<div>` (only when `isOpen` is `true`)
- Bottom border via `border-b` class

### FAQ Example

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Frequently Asked Questions')),
    ),
    CardContent(
      child: Accordion(
        children: [
          AccordionItem(
            title: 'What payment methods do you accept?',
            content: Component.text(
              'We accept Visa, Mastercard, and PayPal.',
            ),
            isOpen: true,
          ),
          AccordionItem(
            title: 'How long does shipping take?',
            content: Component.text(
              'Standard shipping takes 5-7 business days.',
            ),
          ),
          AccordionItem(
            title: 'Can I return my order?',
            content: Component.text(
              'Yes, returns are accepted within 30 days.',
            ),
          ),
        ],
      ),
    ),
  ],
)
```

### With Rich Content

```dart
AccordionItem(
  title: 'Getting Started',
  content: div(
    [
      p([Component.text('Follow these steps:')]),
      ol(
        [
          li([Component.text('Install the package')]),
          li([Component.text('Import the library')]),
          li([Component.text('Use components')]),
        ],
        classes: 'list-decimal pl-4 space-y-1',
      ),
    ],
    classes: 'space-y-2',
  ),
)
```

### Controlled Accordion

Manage open state externally:

```dart
class ControlledAccordion extends StatefulComponent {
  @override
  State<ControlledAccordion> createState() => _ControlledAccordionState();
}

class _ControlledAccordionState extends State<ControlledAccordion> {
  int? openIndex;

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield Accordion(
      children: [
        for (final (i, item) in faqItems.indexed)
          AccordionItem(
            title: item.question,
            content: Component.text(item.answer),
            isOpen: i == openIndex,
          ),
      ],
    );
  }
}
```

## Common Patterns

- **Single expansion** is the default behavior on both platforms. Only one item is open at a time.
- **Initial open state** is supported via `expanded: true` (Flutter) or `isOpen: true` (Web).
- **FAQ lists** are the most common use case -- pair Accordion with text-based question/answer items.
- **Settings panels** work well with Accordion for grouping related form fields under collapsible headers.
- Both platforms render a chevron icon in the trigger that rotates on expand/collapse.

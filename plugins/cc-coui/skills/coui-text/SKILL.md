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

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### StyledText

Renders a `<span>` with Tailwind CSS classes:

```dart
StyledText('Hello')
StyledText.h1('Page Title')
StyledText.h2('Section Heading')
StyledText.h3('Subheading')
StyledText.h4('Minor Heading')
StyledText.body('Body text')
StyledText.muted('Secondary text')
StyledText.inlineCode('flutter run')
StyledText.blockQuote('A quote')
```

### StyledText CSS Classes

| Variant | CSS Classes |
|---------|-------------|
| `h1` | `text-4xl font-extrabold tracking-tight lg:text-5xl` |
| `h2` | `text-3xl font-semibold tracking-tight` |
| `h3` | `text-2xl font-semibold tracking-tight` |
| `h4` | `text-xl font-semibold tracking-tight` |
| `body` | `leading-7` |
| `muted` | `text-sm text-muted-foreground` |
| `inlineCode` | `rounded bg-muted px-[0.3rem] py-[0.2rem] font-mono text-sm` |

### TextBlock

Renders semantic HTML tags (`<p>`, `<h1>`-`<h6>`, `<blockquote>`):

```dart
TextBlock.h1('Page Title')   // <h1>
TextBlock.p('Body text')     // <p>
```

### Link Component

```dart
Link(
  href: 'https://example.com',
  onTap: handleTap,
  underline: true,
  child: Text('Link text'),
)
```

Default styling: primary color + underline. Customizable via `LinkTheme`.

### Web Example

```dart
div(
  [
    StyledText.h1('Page Title'),
    StyledText.muted('Last updated 3 hours ago'),
    StyledText.body('Main content text here.'),
    StyledText.inlineCode('flutter run'),
  ],
  classes: 'space-y-4',
)
```

## Common Patterns

### Platform Differences

| Item | Flutter | Web |
|------|---------|-----|
| Text component | `Text` + extensions | `StyledText` + `TextBlock` |
| Size system | `.xs`, `.sm`, `.lg` extensions | Tailwind CSS (`text-sm`, `text-4xl`) |
| Semantics | Flutter Semantics | HTML `<h1>`-`<h6>`, `<p>` |
| Font modifiers | `.sans`, `.mono` extensions | CSS `font-mono`, `font-sans` |
| Links | `Link` widget (href, onTap) | `<a>` HTML tag |
| Inline code | `.mono.sm` extensions | `StyledText.inlineCode` CSS |
| Selectable text | `SelectableText` widget | Browser native selection |

### Shared Concepts

- Chain order: size -> weight -> color (e.g., `.x2Large.bold.primary`) in Flutter.
- Use `.base200` (Flutter) or `StyledText.muted` (Web) for muted/secondary text.
- Use `.mono` (Flutter) or `StyledText.inlineCode` (Web) for code snippets.
- Use `.destructive` for error messages (Flutter).

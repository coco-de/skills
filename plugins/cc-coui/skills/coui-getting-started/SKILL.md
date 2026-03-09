---
name: coui-getting-started
description: Activate when setting up a new project with CoUI (Flutter or Web), adding coui_flutter or coui_web dependency, creating basic app structure, understanding component naming conventions, imports, installation, or getting started with cross-platform UI development.
---

# CoUI Getting Started

## Overview

CoUI is a cross-platform UI component library providing consistent design components for both Flutter (native/mobile) and Web (Jaspr/HTML) targets. Both packages share naming conventions and component categories but differ in rendering approach: `coui_flutter` renders Flutter widgets while `coui_web` renders HTML/CSS via the Jaspr framework.

## Flutter (coui_flutter)

### Installation

Add to `pubspec.yaml`:

```yaml
dependencies:
  coui_flutter: ^0.1.0
```

### Single Import

All components are available from one import:

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

Do NOT import individual component files.

### Naming Convention

coui_flutter components have NO "Co" prefix. Never use `CoButton`, `CoCard`, `CoInput`, etc.

| Wrong | Correct |
|-------|---------|
| `CoButton` | `PrimaryButton` |
| `CoAvatar` | `Avatar` |
| `CoCard` | `Card` |
| `CoInput` | `Input` / `TextField` |
| `CoDialog` | `Dialog` |

Variants are expressed as class names: `PrimaryButton`, `SecondaryButton`, `GhostButton`, `DestructiveButton`.

### Basic App Structure

```dart
import 'package:flutter/material.dart';
import 'package:coui_flutter/coui_flutter.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'CoUI Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const MyHomePage(),
    );
  }
}

class MyHomePage extends StatelessWidget {
  const MyHomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('CoUI Flutter')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text('Welcome').x2Large.bold,
            Gap.v(8),
            const Text('Build with CoUI Flutter').base200,
            Gap.v(24),
            PrimaryButton(
              onPressed: () {},
              child: const Text('Get Started'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Flutter Key Patterns

#### Spacing

Use `Gap` instead of `SizedBox`:

```dart
Gap.v(16)  // vertical 16px
Gap.h(8)   // horizontal 8px
```

#### Text Styling

Chain extensions on Text widgets:

```dart
const Text('Title').x2Large.bold
const Text('Subtitle').small.base200
```

#### Disabled State

Omit `onPressed` or pass `null`:

```dart
const PrimaryButton(child: Text('Disabled'))
```

### Flutter Component Categories

- **Control**: PrimaryButton, SecondaryButton, GhostButton, IconButton
- **Display**: Avatar, Badge, Card, Divider, Gap, Calendar, Progress
- **Form**: TextField, Input, TextArea, Checkbox, Toggle, Select, Slider, DatePicker
- **Layout**: Accordion, Card, Table, Alert
- **Menu**: ContextMenu, DropdownMenu, Menubar
- **Navigation**: NavigationBar, NavigationRail, Tabs, Pagination
- **Overlay**: Dialog, Toast, Tooltip, Drawer, Popover
- **Text**: Text extensions (.bold, .large, .base200)

## Web (coui_web)

### Installation

Add to `pubspec.yaml`:

```yaml
dependencies:
  coui_web:
    path: ../coui_web  # or published version
  jaspr: ^0.x.x
```

### Single Import

All components are available through one import:

```dart
import 'package:coui_web/coui_web.dart';
```

### Core Concepts

#### Jaspr Framework (Not Flutter)

CoUI Web uses the Jaspr framework. Components render to HTML/CSS, not Flutter widgets.

- Use `Component` tree (like React/HTML), NOT Flutter's Widget tree
- Components extend `StatelessComponent` via `UiComponent`
- Use `Component.text('hello')` instead of `Text('hello')`
- Use Jaspr HTML helpers: `div()`, `span()`, `button()`, `a()`, `p()`, `nav()`, `ul()`, `li()`

#### UiComponent Base Class

All CoUI Web components extend `UiComponent`, which is a `StatelessComponent`:

```dart
abstract class UiComponent extends StatelessComponent {
  const UiComponent(
    this.children, {
    this.child,
    required this.tag,
    this.style,
    this.id,
    this.classes,
    this.css,
    Map<String, String>? attributes,
    this.onClick,
    this.onInput,
    this.onChange,
    // ...
  });
}
```

#### Common UiComponent Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `key` | `Key?` | Jaspr reconciliation key |
| `id` | `String?` | HTML id attribute |
| `classes` | `String?` | Additional CSS classes |
| `css` | `Styles?` | Inline CSS styles |
| `attributes` | `Map<String, String>?` | Custom HTML attributes |
| `tag` | `String` | HTML tag (has default per component) |

### Building a Page

```dart
import 'package:coui_web/coui_web.dart';
import 'package:jaspr/jaspr.dart';

class MyPage extends StatelessComponent {
  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield div(
      [
        Card(
          children: [
            CardHeader(
              child: CardTitle(titleChild: Component.text('Welcome')),
            ),
            CardContent(
              child: Button.primary(
                onPressed: () => print('Clicked!'),
                child: Component.text('Get Started'),
              ),
            ),
          ],
        ),
      ],
      classes: 'container mx-auto p-4',
    );
  }
}
```

### Web Key Patterns

#### Child Patterns

Components use two child patterns:

1. **Single child**: `child: Component` parameter
2. **Multiple children**: `children: List<Component>` parameter
3. **Named content**: e.g., `titleChild:`, `triggerChild:`, `descriptionChild:`

Never provide both `child` and `children` to the same component.

#### Styling with DaisyUI/Tailwind

CoUI Web components use Tailwind CSS utility classes and DaisyUI component classes internally. Add custom classes via the `classes` parameter:

```dart
Button.primary(
  classes: 'mt-4 shadow-lg',
  child: Component.text('Styled Button'),
)
```

#### Inline Styles

Use `css` parameter for inline styles:

```dart
div(
  [Component.text('Custom styled')],
  styles: Styles(raw: {'max-width': '600px'}),
)
```

#### Event Handling

Components expose typed callbacks:

```dart
Button.primary(
  onPressed: () => handleClick(),
  onHover: (isHovered) => handleHover(isHovered),
  child: Component.text('Interactive'),
)

Input(
  onInput: (value) => handleInput(value),
  onChange: (value) => handleChange(value),
)
```

#### CSS Conflict: `css` vs `styles`

In Jaspr, `css` is a top-level function. When inside a `UiComponent` subclass, use `this.css` to reference the component's inline styles parameter:

```dart
// Inside a UiComponent build method:
return Component.element(
  tag: tag,
  styles: this.css,  // Use this.css, not just css
  // ...
);
```

#### Variant System (Named Constructors)

```dart
Button.primary(child: text('Primary'))
Button.secondary(child: text('Secondary'))
Button.outline(child: text('Outline'))
Button.ghost(child: text('Ghost'))
Button.link(child: text('Link'))
Button.destructive(child: text('Destructive'))
```

#### copyWith Pattern

All components implement `copyWith` for immutable modifications:

```dart
final button = Button.primary(child: Component.text('Hello'));
final modified = button.copyWith(classes: 'extra-class');
```

## Common Patterns

### Shared Across Both Platforms

1. **Single import**: Both packages expose all components through a single barrel import (`coui_flutter.dart` / `coui_web.dart`). Never import individual files.

2. **No "Co" prefix**: Components use descriptive names directly -- `Button`, `Card`, `Avatar`, not `CoButton`, `CoCard`, `CoAvatar`.

3. **Variant expression**: Both platforms express variants through type-safe constructors or class names rather than string parameters.

4. **Component categories**: Both packages organize components into the same categories -- Control, Display, Form, Layout, Menu, Navigation, Overlay, and Text.

5. **Disabled state**: Omit or null-out callback parameters (`onPressed`, `onTap`) to disable interactive components.

6. **Handler naming**: Follow the `handle[A-Z]+` pattern for handler functions (e.g., `handleTap`, `handleSubmit`), not `_onTap` or `onTap`.

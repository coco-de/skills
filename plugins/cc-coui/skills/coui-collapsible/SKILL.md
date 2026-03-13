---
name: coui-collapsible
description: Activate when creating collapsible sections, expandable panels, or toggle-to-reveal content areas using CouiCollapsible, Collapsible, isExpanded, or onToggle in CoUI Flutter or CoUI Web.
---

# CoUI Collapsible

## Overview

The Collapsible component provides a toggleable content area that expands and collapses when users click the header. Unlike Accordion (which manages mutual exclusion across items), Collapsible is a single standalone expand/collapse unit.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Collapsible

```dart
CouiCollapsible(
  title: 'Details',
  child: const Text('Detailed content is displayed here.'),
)
```

### Controlled State

```dart
CouiCollapsible(
  title: 'Terms and Conditions',
  isExpanded: _isTermsExpanded,
  onToggle: () {
    setState(() => _isTermsExpanded = !_isTermsExpanded);
  },
  child: const TermsContent(),
)
```

### With Custom Icon

```dart
CouiCollapsible(
  title: 'Filter Options',
  isExpanded: _isFilterExpanded,
  onToggle: () {
    setState(() => _isFilterExpanded = !_isFilterExpanded);
  },
  icon: const Icon(Icons.tune),
  child: FilterPanel(),
)
```

### Key Classes

#### CouiCollapsible

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `String` | required | Header title text |
| `child` | `Widget` | required | Content shown when expanded |
| `isExpanded` | `bool` | `false` | Current expanded state |
| `onToggle` | `VoidCallback?` | `null` | Callback on state change |
| `icon` | `Widget?` | `null` | Optional icon before the title |

### Settings Panel Pattern

```dart
Column(
  children: [
    CouiCollapsible(
      title: 'Advanced Settings',
      icon: const Icon(Icons.settings),
      isExpanded: _showAdvanced,
      onToggle: () => setState(() => _showAdvanced = !_showAdvanced),
      child: Column(
        children: [
          TextField(placeholder: Text('API Key')),
          Gap.v(8),
          Toggle(value: _debugMode, onChanged: (v) => setState(() => _debugMode = v)),
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

### Basic Collapsible

```dart
Collapsible(
  title: 'Details',
  child: Component.text('Detailed content is displayed here.'),
)
```

### Controlled State

```dart
Collapsible(
  title: 'Terms and Conditions',
  isExpanded: isTermsExpanded,
  onToggle: handleTermsToggled,
  child: TermsContent(),
)
```

## Common Patterns

### Collapsible vs Accordion

| Feature | Collapsible | Accordion |
|---------|-------------|-----------|
| Scope | Single section | Multiple sections |
| Mutual exclusion | No | Yes (one open at a time) |
| Use case | Standalone expandable area | FAQ lists, grouped sections |

### API Consistency

- Both Flutter and Web use `title`, `isExpanded`, `onToggle`, and `child`.
- Collapsible is uncontrolled by default (manages its own state). Pass `isExpanded` and `onToggle` for controlled behavior.

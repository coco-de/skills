---
name: coui-code-snippet
description: Activate when creating code displays, syntax-highlighted code blocks, or copyable code examples using CodeSnippet/CodeSnippetTheme (Flutter) or CodeSnippet (Web) in CoUI Flutter or CoUI Web.
---

# CoUI CodeSnippet

## Overview

The CodeSnippet component renders code with syntax highlighting. It supports line numbers, copy functionality, multiple themes, and various programming languages.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CodeSnippet(
  code: 'void main() { print("Hello, CoUI!"); }',
  language: 'dart',
  showLineNumbers: true,
  showCopyButton: true,
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `code` | `String` | required | The code content to display |
| `language` | `String` | `'plaintext'` | Programming language for syntax highlighting |
| `showLineNumbers` | `bool` | `false` | Toggle line number visibility |
| `showCopyButton` | `bool` | `true` | Toggle copy button visibility |
| `theme` | `CodeSnippetTheme` | `light` | Visual theme (light or dark) |
| `maxHeight` | `double?` | `null` | Maximum height with scrolling |
| `onCopy` | `VoidCallback?` | `null` | Callback triggered on copy action |

### Dark Theme

```dart
CodeSnippet(
  code: 'const x = 42;',
  language: 'javascript',
  theme: CodeSnippetTheme.dark,
  showLineNumbers: true,
)
```

### With Max Height

```dart
CodeSnippet(
  code: longCodeString,
  language: 'dart',
  maxHeight: 300,
  showCopyButton: true,
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
CodeSnippet(
  code: 'const x = 42;',
  language: 'javascript',
  showLineNumbers: true,
  showCopyButton: true,
  theme: CodeSnippetTheme.dark,
)
```

### Parameters

Same parameter structure as Flutter with identical property names.

## Common Patterns

### Supported Languages

Dart, JavaScript, TypeScript, Python, Kotlin, Swift, HTML, CSS, JSON, YAML, Bash, SQL.

### Theme Variants

| Theme | Description |
|-------|-------------|
| `CodeSnippetTheme.light` | Light background (default) |
| `CodeSnippetTheme.dark` | Dark background for enhanced visibility |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CodeSnippet` | `CodeSnippet` |
| API | Identical parameters | Identical parameters |

### When to Use

- Documentation code examples
- API response previews
- Configuration file displays
- Tutorial and learning content

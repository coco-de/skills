---
name: coui-empty-state
description: Activate when creating empty state views, no-data placeholders, empty list indicators, or zero-state screens with icons, titles, descriptions, and action buttons using EmptyState (Flutter) or EmptyState (Web) in CoUI Flutter or CoUI Web.
---

# CoUI EmptyState

## Overview

The EmptyState component displays a visual guide when content areas or lists are empty. It combines an icon, title, description, and optional action button to inform users and provide next steps.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
EmptyState(
  icon: Icon(Icons.inbox_outlined, size: 48),
  title: 'No messages received',
  description: 'New messages will appear here when they arrive.',
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `icon` | `Widget?` | `null` | Icon widget displayed at top |
| `title` | `String` | required | Heading text |
| `description` | `String?` | `null` | Supporting explanatory text |
| `action` | `Widget?` | `null` | Action button at bottom |

### With Action Button

```dart
EmptyState(
  icon: Icon(Icons.folder_open_outlined, size: 48),
  title: 'No files',
  description: 'Upload files or create folders to get started.',
  action: Button.primary(
    onPressed: handleUpload,
    child: Text('Upload File'),
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
EmptyState(
  icon: Icon(Icons.inbox_outlined, size: 48),
  title: 'No messages received',
  description: 'New messages will appear here when they arrive.',
)
```

### With Action

```dart
EmptyState(
  icon: Icon(Icons.folder_open_outlined, size: 48),
  title: 'No files',
  description: 'Upload files or create folders to get started.',
  action: Button.primary(
    onClick: handleUpload,
    child: Text('Upload File'),
  ),
)
```

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `EmptyState` | `EmptyState` |
| Action button | `Button.primary()` | `Button.primary()` |
| Child types | `Widget` | `Component` |

### When to Use

- Empty lists or data tables
- Search results with no matches
- Error states with retry actions
- First-time user onboarding prompts

---
name: coui-toast
description: Use when showing temporary notification messages, snackbar-style alerts, toast popups, success/error messages, or dismissible alerts using ToastLayer, showToast, or Toast in coui_flutter or coui_web.
---

# CoUI Toast

## Overview

Toast provides temporary notification messages that appear and auto-dismiss. Both Flutter and Web implementations share the concept of a Toast component with title, description/child, and dismiss behavior, but differ in API surface and rendering approach.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Setup: ToastLayer

Wrap your app or page with `ToastLayer` to enable toasts:

```dart
ToastLayer(
  child: MyApp(),
)
```

### showToast

Display a toast notification:

```dart
showToast(
  context: context,
  builder: (context) {
    return Toast(
      child: const Text('Changes saved successfully'),
    );
  },
)
```

### Toast with Title and Description

```dart
showToast(
  context: context,
  builder: (context) {
    return Toast(
      title: const Text('Scheduled'),
      child: const Text('Meeting set for tomorrow at 3 PM'),
    );
  },
)
```

### Toast with Action

```dart
showToast(
  context: context,
  builder: (context) {
    return Toast(
      title: const Text('Item deleted'),
      child: const Text('The item has been removed'),
      action: GhostButton(
        onPressed: () {
          // undo logic
        },
        child: const Text('Undo'),
      ),
    );
  },
)
```

### ToastTheme

Theme-level customization:

```dart
const ToastTheme(
  toastWidth: 320.0,
  showDuration: Duration(seconds: 5),
  maxStackedEntries: 3,
  collapsedOffsetY: 12.0,
  padding: EdgeInsets.all(24.0),
)
```

### showToast Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `context` | `BuildContext` | Build context |
| `builder` | `WidgetBuilder` | Toast content builder |
| `duration` | `Duration?` | Auto-dismiss duration |
| `alignment` | `AlignmentGeometry?` | Toast position |

### ToastLayer Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | App content |
| `maxStackedEntries` | `int?` | Max visible toasts |
| `alignment` | `AlignmentGeometry?` | Default toast position |

### Stacked Toasts

Multiple toasts stack vertically. Older toasts collapse behind newer ones. Configure with `maxStackedEntries`.

#### Expand Modes

Control how stacked toasts behave:

```dart
const ToastTheme(
  expandMode: ToastExpandMode.expandOnHover,  // Unfolds all toasts on mouse hover (default)
  // expandMode: ToastExpandMode.expandAlways,  // Permanently displays all toasts expanded
  // expandMode: ToastExpandMode.expandNever,   // Shows only topmost toast
  maxStackedEntries: 3,
  collapsedScale: 0.9,       // Overlapped toast size ratio
  collapsedOpacity: 0.8,     // Overlapped toast transparency
)
```

#### Gesture Dismissal

Swipe gesture with 50% or greater movement threshold triggers close.

### Auto-Dismiss

Toasts auto-dismiss after 5 seconds by default. Override with `duration`:

```dart
showToast(
  context: context,
  duration: const Duration(seconds: 10),
  builder: (context) {
    return Toast(child: const Text('Long toast'));
  },
)
```

### Swipe to Dismiss

Users can swipe toasts horizontally to dismiss them.

### Success/Error Pattern (Flutter)

```dart
// Success
showToast(
  context: context,
  builder: (context) => Toast(
    title: const Text('Success'),
    child: const Text('Profile updated'),
  ),
);

// Error
showToast(
  context: context,
  builder: (context) => Toast(
    title: const Text('Error'),
    child: const Text('Failed to save changes'),
  ),
);
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Toast(
  title: 'Success',
  description: 'Your changes have been saved.',
  onDismiss: () => print('Dismissed'),
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `title` | `String` | required | Toast title |
| `description` | `String?` | `null` | Optional description text |
| `variant` | `ToastVariant` | `default_` | Visual variant |
| `onDismiss` | `ToastDismissCallback?` | `null` | Dismiss callback |

### Variants

```dart
// Default toast
Toast(
  title: 'Notification',
  description: 'Something happened.',
)

// Destructive toast
Toast(
  title: 'Error',
  description: 'Something went wrong.',
  variant: ToastVariant.destructive,
)
```

### With Dismiss Button

When `onDismiss` is provided, a close button appears on hover:

```dart
Toast(
  title: 'File uploaded',
  description: 'document.pdf was uploaded successfully.',
  onDismiss: () => removeToast(),
)
```

### Title Only

```dart
Toast(title: 'Saved!')
```

### Accessibility

Toast automatically includes:
- `role="status"` attribute
- `aria-live="polite"` for screen reader announcements

### Toast Container Pattern

Toasts are typically rendered in a fixed container:

```dart
div(
  [
    for (final toast in activeToasts)
      Toast(
        title: toast.title,
        description: toast.description,
        variant: toast.isError ? ToastVariant.destructive : ToastVariant.default_,
        onDismiss: () => dismissToast(toast.id),
      ),
  ],
  classes: 'fixed bottom-4 right-4 z-50 flex flex-col gap-2',
)
```

### Complete Example (Web)

```dart
class ToastManager extends StatefulComponent {
  @override
  State<ToastManager> createState() => _ToastManagerState();
}

class _ToastManagerState extends State<ToastManager> {
  final toasts = <({String id, String title, String? desc, bool isError})>[];

  void showToast(String title, {String? description, bool isError = false}) {
    final id = DateTime.now().millisecondsSinceEpoch.toString();
    setState(() {
      toasts.add((id: id, title: title, desc: description, isError: isError));
    });
  }

  void dismissToast(String id) {
    setState(() {
      toasts.removeWhere((t) => t.id == id);
    });
  }

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield div(
      [
        Button.primary(
          onPressed: () => showToast('Saved!', description: 'Changes saved.'),
          child: Component.text('Show Toast'),
        ),
        div(
          [
            for (final toast in toasts)
              Toast(
                title: toast.title,
                description: toast.desc,
                variant: toast.isError
                    ? ToastVariant.destructive
                    : ToastVariant.default_,
                onDismiss: () => dismissToast(toast.id),
              ),
          ],
          classes: 'fixed bottom-4 right-4 z-50 flex flex-col gap-2 w-80',
        ),
      ],
    );
  }
}
```

## Common Patterns

| Aspect | Flutter | Web |
|--------|---------|-----|
| Setup | `ToastLayer` wrapper required | Manual container positioning |
| Show toast | `showToast(context, builder)` | Instantiate `Toast(...)` directly |
| Title | `title: Text('...')` (Widget) | `title: '...'` (String) |
| Description | `child: Text('...')` (Widget) | `description: '...'` (String) |
| Variants | Styled via `ToastTheme` | `ToastVariant.default_`, `.destructive` |
| Dismiss | Swipe gesture, auto-dismiss | `onDismiss` callback, manual removal |
| Stacking | Built-in via `maxStackedEntries` | Manual via container layout |
| Actions | `action` parameter (Widget) | Not built-in |
| Accessibility | Framework-managed | `role="status"`, `aria-live="polite"` |

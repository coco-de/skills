---
name: coui-dialog
description: Use when creating modal dialogs, alert dialogs, confirmation prompts, overlay content panels, or using showDialog, Dialog, ModalBackdrop, ModalContainer, DialogOverlayHandler, DialogContent, DialogHeader, DialogFooter, DialogTitle, DialogDescription in CoUI Flutter or Web.
---

# CoUI Dialog

## Overview

Dialog components for displaying modal content, confirmation prompts, and overlay panels. Flutter uses `showDialog` with `Dialog`, `ModalBackdrop`, and `ModalContainer` widgets. Web uses a declarative `Dialog` component with `DialogContent`, `DialogHeader`, `DialogFooter`, `DialogTitle`, and `DialogDescription` sub-components.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### showDialog

Display a modal dialog. This is coui_flutter's own `showDialog`, not Flutter's.

```dart
showDialog(
  context: context,
  builder: (context) {
    return Dialog(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text('Title').bold.large,
          Gap.v(16),
          const Text('Dialog content goes here.'),
          Gap.v(24),
          Row(
            mainAxisAlignment: MainAxisAlignment.end,
            children: [
              GhostButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Cancel'),
              ),
              Gap.h(8),
              PrimaryButton(
                onPressed: () => Navigator.pop(context),
                child: const Text('Confirm'),
              ),
            ],
          ),
        ],
      ),
    );
  },
);
```

### showDialog Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `context` | `BuildContext` | required | Build context |
| `builder` | `WidgetBuilder` | required | Dialog content builder |
| `barrierDismissible` | `bool` | `true` | Tap outside to dismiss |
| `barrierColor` | `Color?` | transparent | Backdrop color |
| `useRootNavigator` | `bool` | `true` | Use root navigator |
| `useSafeArea` | `bool` | `true` | Respect safe areas |
| `fullScreen` | `bool` | `false` | Full-screen mode |
| `alignment` | `AlignmentGeometry?` | center | Dialog position |

### Return Values

```dart
final result = await showDialog<String>(
  context: context,
  builder: (context) {
    return Dialog(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Text('Choose an option'),
          Gap.v(16),
          PrimaryButton(
            onPressed: () => Navigator.pop(context, 'confirmed'),
            child: const Text('Confirm'),
          ),
          Gap.v(8),
          GhostButton(
            onPressed: () => Navigator.pop(context, 'cancelled'),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  },
);

if (result == 'confirmed') {
  // handle confirmation
}
```

### ModalBackdrop

Adds a barrier behind dialog content:

```dart
ModalBackdrop(
  barrierColor: const Color.fromRGBO(0, 0, 0, 0.8),
  modal: true,
  surfaceClip: true,
  child: MyDialogContent(),
)
```

#### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Content above backdrop |
| `barrierColor` | `Color?` | Backdrop color (default: black 80%) |
| `modal` | `bool?` | Block interaction (default: true) |
| `surfaceClip` | `bool?` | Clip surface effects |
| `borderRadius` | `BorderRadiusGeometry?` | Cutout corner radius |
| `fadeAnimation` | `Animation<double>?` | Fade animation |

### ModalContainer

Styled container for modal content with surface effects:

```dart
ModalContainer(
  padding: const EdgeInsets.all(24),
  borderRadius: BorderRadius.circular(12),
  filled: true,
  child: Column(
    children: [
      const Text('Modal Title'),
      const Text('Modal content'),
    ],
  ),
)
```

### ModalBackdropTheme

Theme-level customization:

```dart
const ModalBackdropTheme(
  barrierColor: Color.fromRGBO(0, 0, 0, 0.5),
  borderRadius: BorderRadius.circular(12),
  modal: true,
  surfaceClip: true,
)
```

### Focus Trapping

Dialog uses `FocusTrap` to confine keyboard focus within the dialog:

- First focusable element receives automatic focus on open
- Tab/Shift+Tab cycles through focusable elements within the dialog only
- Previous focus element is restored when dialog closes
- Escape key dismisses the dialog (if `barrierDismissible` is `true`)

### Animation

Dialog transitions use scale and fade transformations:

- Default transition duration: ~300ms
- Customizable via `DialogRoute` transition parameters

### Full-Screen Dialog

```dart
showDialog(
  context: context,
  fullScreen: true,
  builder: (context) {
    return Dialog(
      child: MyFullScreenContent(),
    );
  },
);
```

### DialogOverlayHandler

For programmatic dialog control through the overlay system:

```dart
const DialogOverlayHandler().show<String>(
  context: context,
  alignment: Alignment.center,
  builder: (context) => MyCustomDialog(),
);
```

### Flutter Delete Confirmation Pattern

```dart
void handleDelete(BuildContext context) {
  showDialog(
    context: context,
    builder: (context) {
      return Dialog(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Delete Item').bold.large,
            Gap.v(8),
            const Text('This action cannot be undone.').base200,
            Gap.v(24),
            Row(
              mainAxisAlignment: MainAxisAlignment.end,
              children: [
                GhostButton(
                  onPressed: () => Navigator.pop(context),
                  child: const Text('Cancel'),
                ),
                Gap.h(8),
                DestructiveButton(
                  onPressed: () {
                    // perform delete
                    Navigator.pop(context);
                  },
                  child: const Text('Delete'),
                ),
              ],
            ),
          ],
        ),
      );
    },
  );
}
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Dialog(
  open: true,
  children: [
    DialogContent(
      children: [
        DialogHeader(
          children: [
            DialogTitle(titleChild: Component.text('Are you sure?')),
            DialogDescription(
              descriptionChild: Component.text('This action cannot be undone.'),
            ),
          ],
        ),
        DialogFooter(
          children: [
            Button.outline(
              onPressed: () => handleCancel(),
              child: Component.text('Cancel'),
            ),
            Button.primary(
              onPressed: () => handleConfirm(),
              child: Component.text('Continue'),
            ),
          ],
        ),
      ],
    ),
  ],
)
```

### Components

#### Dialog (Container)

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `open` | `bool` | `false` | Whether dialog is visible |
| `children` | `List<Component>?` | `null` | Typically one DialogContent |
| `child` | `Component?` | `null` | Single child alternative |

When `open` is `false`, renders an empty fragment. When `true`, renders an overlay backdrop and centered content wrapper.

#### DialogContent

The main content container with styled appearance:

```dart
DialogContent(
  children: [
    DialogHeader(child: ...),
    // content
    DialogFooter(child: ...),
  ],
)
```

#### DialogHeader

Flex column layout with spacing for title and description:

```dart
DialogHeader(
  children: [
    DialogTitle(titleChild: Component.text('Title')),
    DialogDescription(
      descriptionChild: Component.text('Description text'),
    ),
  ],
)
```

#### DialogTitle

Renders an `<h2>` element with semibold styling. Parameter: `titleChild: Component` (required).

```dart
DialogTitle(titleChild: Component.text('Dialog Title'))
```

#### DialogDescription

Renders a `<p>` element with muted foreground text. Parameter: `descriptionChild: Component` (required).

```dart
DialogDescription(
  descriptionChild: Component.text('A brief description.'),
)
```

#### DialogFooter

Flex layout with responsive column/row orientation:

```dart
DialogFooter(
  children: [
    Button.outline(child: Component.text('Cancel')),
    Button.primary(child: Component.text('Save')),
  ],
)
```

### Web Delete Confirmation Pattern

```dart
class ConfirmDialog extends StatelessComponent {
  const ConfirmDialog({
    required this.isOpen,
    required this.onConfirm,
    required this.onCancel,
  });

  final bool isOpen;
  final VoidCallback onConfirm;
  final VoidCallback onCancel;

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield Dialog(
      open: isOpen,
      children: [
        DialogContent(
          children: [
            DialogHeader(
              children: [
                DialogTitle(
                  titleChild: Component.text('Delete Item'),
                ),
                DialogDescription(
                  descriptionChild: Component.text(
                    'This will permanently delete the item. This action cannot be undone.',
                  ),
                ),
              ],
            ),
            DialogFooter(
              children: [
                Button.outline(
                  onPressed: onCancel,
                  child: Component.text('Cancel'),
                ),
                Button.destructive(
                  onPressed: onConfirm,
                  child: Component.text('Delete'),
                ),
              ],
            ),
          ],
        ),
      ],
    );
  }
}
```

### Dialog with Form Content

```dart
Dialog(
  open: true,
  children: [
    DialogContent(
      children: [
        DialogHeader(
          children: [
            DialogTitle(titleChild: Component.text('Edit Profile')),
            DialogDescription(
              descriptionChild: Component.text('Update your profile information.'),
            ),
          ],
        ),
        div(
          [
            Input(placeholder: 'Name', name: 'name'),
            Input(placeholder: 'Email', type: 'email', name: 'email'),
          ],
          classes: 'space-y-4 py-4',
        ),
        DialogFooter(
          children: [
            Button.primary(
              onPressed: () => handleSave(),
              child: Component.text('Save changes'),
            ),
          ],
        ),
      ],
    ),
  ],
)
```

## Common Patterns

| Concern | Flutter | Web |
|---------|---------|-----|
| Import | `package:coui_flutter/coui_flutter.dart` | `package:coui_web/coui_web.dart` |
| Show dialog | `showDialog(context, builder)` | `Dialog(open: true, ...)` |
| Dismiss | `Navigator.pop(context)` | Toggle `open` to `false` |
| Return value | `Navigator.pop(context, value)` | Callback parameters |
| Cancel button | `GhostButton` | `Button.outline` |
| Confirm button | `PrimaryButton` | `Button.primary` |
| Destructive button | `DestructiveButton` | `Button.destructive` |
| Backdrop | `ModalBackdrop` widget | Built into `Dialog` |
| Content container | `ModalContainer` | `DialogContent` |
| Title | Text with `.bold.large` | `DialogTitle` |
| Description | Text with `.base200` | `DialogDescription` |
| Footer layout | `Row` with `MainAxisAlignment.end` | `DialogFooter` |
| Full-screen | `showDialog(fullScreen: true)` | N/A |
| Theming | `ModalBackdropTheme` | CSS custom properties |

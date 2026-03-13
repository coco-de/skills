---
name: coui-file-input
description: Activate when creating file inputs, file upload fields, file pickers, or file icon mappings using FileInput, FileIconProviderData, FileInputStyling in CoUI Flutter or CoUI Web.
---

# CoUI FileInput

## Overview

The FileInput component enables users to select and upload files. Flutter provides `FileInput` for file selection and `FileIconProviderData` for mapping file extensions to icons. Web provides a styled `FileInput` with color, size, and ghost variants. The implementations differ significantly between platforms.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic File Input

```dart
FileInput(
  onFilesSelected: (files) => print('Selected: ${files.length}'),
)
```

### Image-Only Input

```dart
FileInput(
  accept: 'image/*',
  onFilesSelected: handleImageSelected,
)
```

### Multiple File Selection

```dart
FileInput(
  multiple: true,
  accept: '.pdf, .doc, .docx',
  onFilesSelected: handleFilesSelected,
)
```

### FileIconProviderData (File Icon Utility)

```dart
final iconProvider = FileIconProviderData(
  icons: {
    'pdf': Icon(BootstrapIcons.filetypePdf),
    'doc': Icon(BootstrapIcons.fileWord),
  },
);

final icon = iconProvider.buildIcon('pdf');
```

### Display Selected Files with Icons

```dart
Column(children: [
  FileInput(
    multiple: true,
    accept: '.pdf, .doc',
    onFilesSelected: (files) => setState(() => selectedFiles = files),
  ),
  for (final file in selectedFiles)
    Row(children: [
      iconProvider.buildIcon(file.name.split('.').last),
      Text(file.name),
    ]),
])
```

### FileInput Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `onFilesSelected` | `ValueChanged<FileList>?` | `null` | File selection callback |
| `name` | `String?` | `null` | Form field name |
| `disabled` | `bool` | `false` | Disable input |
| `accept` | `String?` | `null` | Allowed file types (e.g., `image/*`, `.pdf`) |
| `multiple` | `bool` | `false` | Allow multiple file selection |
| `style` | `List<FileInputStyling>?` | `null` | Style list |

### FileIconProviderData Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `builder` | `FileIconBuilder?` | `null` | Custom icon builder based on extension |
| `icons` | `Map<String, Widget>?` | `null` | Extension-to-icon mapping |

### Default Icon Mappings

| Extension | Icon |
|-----------|------|
| `.pdf` | `BootstrapIcons.filetypePdf` |
| `.doc, .docx` | `BootstrapIcons.fileWord` |
| `.xls, .xlsx` | `BootstrapIcons.fileExcel` |
| `.ppt, .pptx` | `BootstrapIcons.filePpt` |
| `.zip, .rar` | `BootstrapIcons.fileZip` |
| `.jpg, .jpeg, .png, .gif` | `BootstrapIcons.fileImage` |
| `.mp3, .wav` | `BootstrapIcons.fileMusic` |
| `.mp4, .avi, .mkv` | `BootstrapIcons.filePlay` |
| Other | `BootstrapIcons.file` |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic File Input

```dart
FileInput(
  onFilesSelected: handleFileSelected,
)
```

### With Accept and Multiple

```dart
FileInput(
  multiple: true,
  accept: '.pdf, .jpg, .png',
  onFilesSelected: (files) {
    for (var i = 0; i < files.length; i++) {
      uploadFile(files.item(i)!);
    }
  },
)
```

### Color Variants

```dart
FileInput(style: [FileInput.primary])
FileInput(style: [FileInput.secondary])
FileInput(style: [FileInput.success])
FileInput(style: [FileInput.error])
```

Available colors: `neutral`, `primary`, `secondary`, `accent`, `info`, `success`, `warning`, `error`

### Size Variants

```dart
FileInput(style: [FileInput.xs])   // Extra Small
FileInput(style: [FileInput.sm])   // Small
FileInput(style: [FileInput.md])   // Medium (default)
FileInput(style: [FileInput.lg])   // Large
FileInput(style: [FileInput.xl])   // Extra Large
```

### Ghost Variant

```dart
FileInput(style: [FileInput.ghost])
FileInput(style: [FileInput.ghost, FileInput.primary])
```

### Combined Styles

```dart
FileInput(
  style: [FileInput.primary, FileInput.lg],
  multiple: true,
  accept: '.pdf, .jpg, .png',
  onFilesSelected: handleFilesSelected,
)
```

### Web Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `onFilesSelected` | `Callback` | `null` | File selection handler |
| `name` | `String?` | `null` | Form field identifier |
| `disabled` | `bool` | `false` | Disable interaction |
| `accept` | `String?` | `null` | MIME types or extensions filter |
| `multiple` | `bool` | `false` | Enable multi-select |
| `style` | `List<FileInputStyling>?` | `null` | Style modifiers (color, size, ghost) |

## Common Patterns

### Accessibility

| Key | Action |
|-----|--------|
| `Tab` | Focus FileInput |
| `Enter` / `Space` | Open file selection dialog |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| File selection | Platform-specific | Browser `<input type="file">` |
| Icon mapping | `FileIconProviderData` with 9 icon types | Not supported |
| Color variants | Not supported | 8 colors (neutral through error) |
| Size variants | Not supported | 5 sizes (xs through xl) |
| Ghost style | Not supported | `FileInput.ghost` |

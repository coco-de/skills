---
name: coui-mockup
description: Activate when creating device frame mockups, browser window frames, phone previews, code editor frames, or desktop window simulations using MockupBrowser/MockupPhone/MockupCode/MockupWindow (Flutter) or MockupBrowser/MockupPhone/MockupCode/MockupWindow (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Mockup

## Overview

The Mockup component simulates device frames and application interfaces. It wraps content to appear like actual devices or app screens for visual presentations in documentation, landing pages, and screenshots.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Available Widgets

- `MockupBrowser` - Browser window frame
- `MockupPhone` - Mobile device frame
- `MockupCode` - Code editor frame
- `MockupWindow` - Desktop application window

### Browser Mockup

```dart
MockupBrowser(
  url: 'https://coui.cocode.im',
  title: 'CoUI Design System',
  child: Image.asset('assets/screenshots/dashboard.png'),
)
```

#### Browser Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Widget` | required | Content inside frame |
| `url` | `String?` | `null` | Address bar URL |
| `title` | `String?` | `null` | Page title in tab |

### Phone Mockup

```dart
MockupPhone(
  child: Scaffold(
    appBar: AppBar(title: Text('App Screen')),
    body: Center(child: Text('Content')),
  ),
)
```

### Code Editor Mockup

```dart
MockupCode(
  child: Text('void main() { runApp(const MyApp()); }'),
)
```

### Desktop Window Mockup

```dart
MockupWindow(
  title: 'My App',
  child: Container(padding: EdgeInsets.all(16)),
)
```

#### Window Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Widget` | required | Content inside frame |
| `title` | `String?` | `null` | Title bar text |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Browser Frame

```dart
MockupBrowser(
  url: 'https://coui.cocode.im',
  title: 'CoUI Design System',
  child: ImageComponent(),
)
```

### Phone Preview

```dart
MockupPhone(
  child: AppScreenshot(),
)
```

### Code Block Display

```dart
MockupCode(
  child: CodeBlock(code: 'const hello = "world";'),
)
```

### Desktop Window

```dart
MockupWindow(
  title: 'My App',
  child: content,
)
```

## Common Patterns

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Browser | `MockupBrowser` | `MockupBrowser` |
| Phone | `MockupPhone` | `MockupPhone` |
| Code | `MockupCode` | `MockupCode` |
| Window | `MockupWindow` | `MockupWindow` |

### When to Use

- Documentation screenshots with device frames
- Landing page product visuals
- Code example presentations in editor frames
- Responsive design showcase across device types
- Marketing and promotional material

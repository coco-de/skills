---
name: coui-link
description: Activate when creating text links, navigation links, external URL links, or styled hyperlinks using CouiLink/LinkVariant (Flutter) or Link (Web) in CoUI Flutter or CoUI Web.
---

# CoUI Link

## Overview

The Link component is a text widget for navigating to internal or external URLs. It supports multiple visual variants and automatically displays an external link icon for external URLs.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

```dart
CouiLink(
  onTap: handleNavigateToProfile,
  child: Text('프로필 보기'),
)
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `child` | `Widget` | required | Widget displayed as the link |
| `href` | `String?` | `null` | Target URL for navigation |
| `onTap` | `VoidCallback?` | `null` | Callback for tap events |
| `variant` | `LinkVariant` | `defaultVariant` | Visual style variant |
| `isExternal` | `bool` | `false` | Opens externally in new window |

### External Link

```dart
CouiLink(
  href: 'https://coui.cocode.im',
  isExternal: true,
  child: Text('CoUI 문서'),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Link(
  href: '/profile',
  child: Text('프로필 보기'),
)
```

### External Link

```dart
Link(
  href: 'https://coui.cocode.im',
  isExternal: true,
  child: Text('CoUI 문서'),
)
```

## Common Patterns

### Variants

| Variant | Description |
|---------|-------------|
| `LinkVariant.defaultVariant` | Primary link color with hover underline |
| `LinkVariant.underline` | Always displays underline; for body text |
| `LinkVariant.muted` | Lower contrast for secondary information |
| `LinkVariant.external` | Auto-displays external icon |

### Platform Differences

| Aspect | Flutter | Web |
|--------|---------|-----|
| Widget name | `CouiLink` | `Link` |
| Navigation | `onTap` callback or `href` | `href` string |
| Child type | `Widget` | `Component` |

### When to Use

- Inline text links within paragraphs
- Navigation links in menus and sidebars
- External resource references
- Footer links and legal text

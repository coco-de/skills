---
name: coui-tabs
description: Use when creating tab navigation, tab lists, tab panes, or tabbed content panels in CoUI Flutter or Web using Tabs, TabList, TabItem, TabPane, TabsTrigger, or TabsContent.
---

# CoUI Tabs

## Overview

CoUI provides tab components for both Flutter and Web platforms. Both share index-based `TabList` and `TabPane` APIs, while Web additionally offers a value-based shadcn-style `Tabs` approach. Use tabs to organize content into switchable panels.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Tabs

```dart
int selectedIndex = 0;

Tabs(
  index: selectedIndex,
  tabs: [
    const Text('Tab 1'),
    const Text('Tab 2'),
    const Text('Tab 3'),
  ],
  onChanged: (index) {
    setState(() => selectedIndex = index);
  },
  children: [
    const Text('Content for Tab 1'),
    const Text('Content for Tab 2'),
    const Text('Content for Tab 3'),
  ],
)
```

### TabList

Lower-level tab bar without content panes:

```dart
TabList(
  index: selectedIndex,
  onChanged: (index) => setState(() => selectedIndex = index),
  children: [
    TabItem(child: const Text('Overview')),
    TabItem(child: const Text('Analytics')),
    TabItem(child: const Text('Settings')),
  ],
)
```

### TabPane

Content area that responds to tab selection:

```dart
TabPane(
  index: selectedIndex,
  children: [
    const OverviewPage(),
    const AnalyticsPage(),
    const SettingsPage(),
  ],
)
```

### TabsTheme

Theme-level customization:

```dart
const TabsTheme(
  backgroundColor: Colors.grey,
  borderRadius: BorderRadius.circular(8),
  containerPadding: EdgeInsets.all(4),
  tabPadding: EdgeInsets.symmetric(vertical: 4, horizontal: 16),
  activeColor: Colors.blue,
  inactiveColor: Colors.grey,
  expand: true,  // tabs fill available width
)
```

### Tabs with Icons Pattern

```dart
Tabs(
  index: selectedIndex,
  onChanged: (i) => setState(() => selectedIndex = i),
  tabs: [
    Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Icon(Icons.home, size: 16),
        Gap.h(4),
        const Text('Home'),
      ],
    ),
    Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        const Icon(Icons.settings, size: 16),
        Gap.h(4),
        const Text('Settings'),
      ],
    ),
  ],
  children: [
    const HomePage(),
    const SettingsPage(),
  ],
)
```

### Full-Width Tabs Pattern

```dart
TabList(
  index: selectedIndex,
  onChanged: (i) => setState(() => selectedIndex = i),
  expand: true,
  children: [
    TabItem(child: const Text('Tab 1')),
    TabItem(child: const Text('Tab 2')),
    TabItem(child: const Text('Tab 3')),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Three Tab Approaches

CoUI Web provides three tab components:

1. **Tabs** (shadcn-style): Value-based with TabsList, TabsTrigger, TabsContent
2. **TabList**: Index-based horizontal tab bar (coui_flutter compatible)
3. **TabPane**: Boxed tab panel with integrated tab bar and content

### 1. Tabs (shadcn-style)

```dart
Tabs(
  defaultValue: 'tab1',
  children: [
    TabsList(
      children: [
        TabsTrigger(value: 'tab1', label: 'Account'),
        TabsTrigger(value: 'tab2', label: 'Settings'),
      ],
    ),
    TabsContent(
      value: 'tab1',
      isActive: true,
      child: Component.text('Account settings content'),
    ),
    TabsContent(
      value: 'tab2',
      child: Component.text('General settings content'),
    ),
  ],
)
```

#### TabsTrigger Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Tab identifier |
| `label` | `String` | required | Display text |
| `isActive` | `bool` | `false` | Whether tab is active |

#### TabsContent Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `value` | `String` | required | Matching tab identifier |
| `child` | `Component?` | `null` | Tab panel content |
| `isActive` | `bool` | `false` | Whether to show content |

When `isActive` is `false`, TabsContent renders an empty fragment.

### 2. TabList (Index-based)

A horizontal tab bar with index-based selection, compatible with coui_flutter API:

```dart
TabList(
  index: 0,
  onChanged: (i) => setState(() => currentTab = i),
  children: [
    Component.text('Overview'),
    Component.text('Details'),
    Component.text('Settings'),
  ],
)
```

#### TabList Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `index` | `int` | required | Currently selected tab (0-based) |
| `onChanged` | `void Function(int)?` | `null` | Tab selection callback |
| `children` | `List<Component>` | required | Tab button contents |

### 3. TabPane (Boxed Panel)

Combines tab navigation and content display in a bordered container:

```dart
TabPane(
  index: 0,
  labels: ['Overview', 'Details', 'Settings'],
  onChanged: (i) => setState(() => activeTab = i),
  children: [
    Component.text('Overview content'),
    Component.text('Details content'),
    Component.text('Settings content'),
  ],
)
```

#### TabPane Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `index` | `int` | required | Active tab index (0-based) |
| `labels` | `List<String>` | required | Tab button labels |
| `onChanged` | `void Function(int)?` | `null` | Tab selection callback |
| `children` | `List<Component>` | required | Content for each panel |

### Complete Web Example with TabList

```dart
class MyTabbedPage extends StatefulComponent {
  @override
  State<MyTabbedPage> createState() => _MyTabbedPageState();
}

class _MyTabbedPageState extends State<MyTabbedPage> {
  int currentTab = 0;

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield div(
      [
        TabList(
          index: currentTab,
          onChanged: (i) => setState(() => currentTab = i),
          children: [
            Component.text('Profile'),
            Component.text('Notifications'),
            Component.text('Security'),
          ],
        ),
        div(
          [
            if (currentTab == 0) Component.text('Profile settings...'),
            if (currentTab == 1) Component.text('Notification preferences...'),
            if (currentTab == 2) Component.text('Security options...'),
          ],
          classes: 'p-4',
        ),
      ],
    );
  }
}
```

## Common Patterns

### Shared API (Flutter & Web)

Both platforms support the index-based `TabList` and `TabPane` components with compatible APIs:

- **`index`**: 0-based integer for the active tab
- **`onChanged`**: Callback receiving the new tab index
- **`children`**: List of tab contents or tab items

### State Management

Both platforms use `setState` for tab switching:

```dart
int currentTab = 0;

// In callback:
onChanged: (i) => setState(() => currentTab = i),
```

### Platform Differences

| Feature | Flutter | Web |
|---------|---------|-----|
| High-level component | `Tabs` (index + tabs/children) | `Tabs` (value-based, shadcn-style) |
| Tab bar | `TabList` with `TabItem` children | `TabList` with `Component` children |
| Content panel | `TabPane` (index + children) | `TabPane` (index + labels + children) |
| Theme support | `TabsTheme` | CSS-based styling |
| Full-width mode | `expand: true` on `TabList` | N/A |
| Value-based tabs | N/A | `TabsTrigger` + `TabsContent` |

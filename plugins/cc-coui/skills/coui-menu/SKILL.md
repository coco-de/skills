---
name: coui-menu
description: Use when creating context menus, dropdown menus, menu bars, navigation menus, or sidebar menus using Menu, MenuButton, MenuItem, MenuGroup, MenuSubmenu, Menubar, ContextMenu, DropdownMenu, NavigationMenu in CoUI Flutter or Web.
---

# CoUI Menu

## Overview

Menu components provide context menus, dropdown menus, menu bars, and navigation menus across Flutter and Web platforms. Flutter uses widget-based composition (MenuButton, MenuGroup, Menubar), while Web offers both CoUI navigation menus (Menu, MenuItem, MenuSubmenu) and interactive menus (DropdownMenu, ContextMenu).

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### ContextMenu

Right-click menu:

```dart
ContextMenu(
  items: [
    MenuButton(
      onPressed: (context) {},
      leading: const Icon(Icons.copy),
      child: const Text('Copy'),
    ),
    MenuButton(
      onPressed: (context) {},
      leading: const Icon(Icons.cut),
      child: const Text('Cut'),
    ),
    MenuButton(
      onPressed: (context) {},
      leading: const Icon(Icons.paste),
      child: const Text('Paste'),
    ),
  ],
  child: Container(
    padding: const EdgeInsets.all(32),
    child: const Text('Right-click here'),
  ),
)
```

### DropdownMenu

Dropdown triggered by a button:

```dart
DropdownMenu(
  items: [
    MenuButton(
      onPressed: (context) {},
      child: const Text('Profile'),
    ),
    MenuButton(
      onPressed: (context) {},
      child: const Text('Settings'),
    ),
    MenuButton(
      onPressed: (context) {},
      child: const Text('Logout'),
    ),
  ],
  child: OutlineButton(
    onPressed: () {},
    trailing: const Icon(Icons.expand_more),
    child: const Text('Menu'),
  ),
)
```

### MenuButton

Individual menu item:

```dart
MenuButton(
  onPressed: (context) {
    // handle menu action
  },
  leading: const Icon(Icons.edit),
  trailing: MenuShortcut(activator: const SingleActivator(LogicalKeyboardKey.keyE, control: true)),
  child: const Text('Edit'),
)
```

#### MenuButton Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `onPressed` | `void Function(BuildContext)?` | Action callback |
| `child` | `Widget` (required) | Menu item label |
| `leading` | `Widget?` | Icon before label |
| `trailing` | `Widget?` | Shortcut/icon after label |
| `enabled` | `bool` | Enable/disable item |

### Menubar

Horizontal menu bar (app-level):

```dart
Menubar(
  items: [
    MenuGroup(
      label: const Text('File'),
      children: [
        MenuButton(
          onPressed: (context) {},
          child: const Text('New'),
        ),
        MenuButton(
          onPressed: (context) {},
          child: const Text('Open'),
        ),
        MenuButton(
          onPressed: (context) {},
          child: const Text('Save'),
        ),
      ],
    ),
    MenuGroup(
      label: const Text('Edit'),
      children: [
        MenuButton(
          onPressed: (context) {},
          child: const Text('Undo'),
        ),
        MenuButton(
          onPressed: (context) {},
          child: const Text('Redo'),
        ),
      ],
    ),
  ],
)
```

### MenuGroup

Groups menu items with a label (creates sub-menus):

```dart
MenuGroup(
  label: const Text('View'),
  children: [
    MenuButton(
      onPressed: (context) {},
      child: const Text('Zoom In'),
    ),
    MenuButton(
      onPressed: (context) {},
      child: const Text('Zoom Out'),
    ),
  ],
)
```

### MenuShortcut

Display keyboard shortcut hint:

```dart
MenuButton(
  onPressed: (context) {},
  trailing: MenuShortcut(
    activator: const SingleActivator(
      LogicalKeyboardKey.keyS,
      control: true,
    ),
  ),
  child: const Text('Save'),
)
```

### MenuTheme

```dart
const MenuTheme(
  itemPadding: EdgeInsets.symmetric(horizontal: 8, vertical: 4),
  subMenuOffset: Offset(8, -4),
)
```

### NavigationMenu

Navigation-style dropdown menu for website-style navigation.

### User Menu Pattern (Flutter)

```dart
DropdownMenu(
  items: [
    MenuButton(
      onPressed: (context) {},
      leading: const Icon(Icons.person),
      child: const Text('Profile'),
    ),
    MenuButton(
      onPressed: (context) {},
      leading: const Icon(Icons.settings),
      child: const Text('Settings'),
    ),
    const Divider(),
    MenuButton(
      onPressed: (context) {},
      leading: const Icon(Icons.logout),
      child: const Text('Sign out'),
    ),
  ],
  child: Avatar(initials: 'JD'),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Menu

A container for navigation links using CoUI's menu classes.

#### Basic Vertical Menu

```dart
Menu(
  [
    MenuItem([Component.text('Home')], href: '/'),
    MenuItem([Component.text('About')], href: '/about'),
    MenuItem([Component.text('Contact')], href: '/contact'),
  ],
  ariaLabel: 'Main navigation',
)
```

#### With Title

```dart
Menu(
  [
    MenuTitle([Component.text('Navigation')]),
    MenuItem([Component.text('Dashboard')], href: '/dashboard'),
    MenuItem([Component.text('Settings')], href: '/settings'),
  ],
)
```

#### Horizontal Menu

```dart
Menu(
  [
    MenuItem([Component.text('Home')], href: '/'),
    MenuItem([Component.text('Products')], href: '/products'),
    MenuItem([Component.text('About')], href: '/about'),
  ],
  style: [Menu.horizontal],
  ariaLabel: 'Top navigation',
)
```

#### Menu Sizes

```dart
Menu([...], style: [Menu.xs])
Menu([...], style: [Menu.sm])
Menu([...], style: [Menu.md])  // default
Menu([...], style: [Menu.lg])
Menu([...], style: [Menu.xl])
```

#### Active and Disabled Items

```dart
MenuItem([Component.text('Current')], isActive: true)
MenuItem([Component.text('Unavailable')], isDisabled: true)
```

#### With Click Handler

```dart
MenuItem(
  [Component.text('Logout')],
  onClick: (_) => handleLogout(),
)
```

### MenuSubmenu (Collapsible)

```dart
Menu(
  [
    MenuItem([Component.text('Home')], href: '/'),
    MenuSubmenu(
      label: Component.text('Products'),
      children: [
        MenuItem([Component.text('Electronics')], href: '/electronics'),
        MenuItem([Component.text('Clothing')], href: '/clothing'),
      ],
    ),
  ],
)
```

#### Submenu Initially Open

```dart
MenuSubmenu(
  label: Component.text('Settings'),
  initiallyOpen: true,
  children: [
    MenuItem([Component.text('Profile')], href: '/settings/profile'),
    MenuItem([Component.text('Security')], href: '/settings/security'),
  ],
)
```

### MenuHoverSubmenu (for horizontal menus)

```dart
MenuHoverSubmenu(
  label: Component.text('Services'),
  children: [
    MenuItem([Component.text('Consulting')]),
    MenuItem([Component.text('Development')]),
  ],
)
```

### Dropdown Toggle (JS-controlled)

```dart
li([
  MenuDropdownToggle([Component.text('Theme')]),
  MenuDropdownContent([
    MenuItem([Component.text('Light')]),
    MenuItem([Component.text('Dark')]),
  ]),
])
```

### DropdownMenu (shadcn-style)

```dart
DropdownMenu(
  trigger: Button.outline(child: Component.text('Options')),
  items: [
    DropdownMenuItem(label: 'Edit', onSelect: () => handleEdit()),
    DropdownMenuItem(label: 'Duplicate', onSelect: () => handleDuplicate()),
    DropdownMenuItem(
      label: 'Delete',
      onSelect: () => handleDelete(),
      disabled: true,
    ),
  ],
)
```

#### DropdownMenuItem Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Item text |
| `onSelect` | `MenuItemCallback?` | `null` | Click callback |
| `icon` | `Component?` | `null` | Optional icon |
| `disabled` | `bool` | `false` | Whether disabled |

### ContextMenu (Right-click)

```dart
ContextMenu(
  triggerChild: div(
    [Component.text('Right-click me')],
    classes: 'border rounded-md p-8 text-center',
  ),
  items: [
    ContextMenuItem(label: 'Copy', shortcut: 'Ctrl+C', onSelect: () {}),
    ContextMenuItem(label: 'Paste', shortcut: 'Ctrl+V', onSelect: () {}),
    ContextMenuItem(label: 'Delete', onSelect: () {}, disabled: true),
  ],
)
```

#### ContextMenuItem Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Item text |
| `onSelect` | `ContextMenuItemCallback?` | `null` | Click callback |
| `icon` | `Component?` | `null` | Optional icon |
| `shortcut` | `String?` | `null` | Keyboard shortcut display |
| `disabled` | `bool` | `false` | Whether disabled |

### Sidebar Navigation Example (Web)

```dart
div(
  [
    Menu(
      [
        MenuTitle([Component.text('Main')]),
        MenuItem([Component.text('Dashboard')], href: '/', isActive: true),
        MenuItem([Component.text('Analytics')], href: '/analytics'),
        MenuTitle([Component.text('Settings')]),
        MenuSubmenu(
          label: Component.text('Account'),
          initiallyOpen: true,
          children: [
            MenuItem([Component.text('Profile')], href: '/profile'),
            MenuItem([Component.text('Billing')], href: '/billing'),
          ],
        ),
        MenuItem([Component.text('Logout')], onClick: (_) => logout()),
      ],
      style: [Menu.sm],
      ariaLabel: 'Sidebar navigation',
    ),
  ],
  classes: 'w-64 border-r h-full',
)
```

## Common Patterns

### Component Mapping

| Concept | Flutter | Web |
|---------|---------|-----|
| Menu container | `Menubar` | `Menu` |
| Menu item | `MenuButton` | `MenuItem` |
| Submenu group | `MenuGroup` | `MenuSubmenu` / `MenuHoverSubmenu` |
| Context menu | `ContextMenu` (wraps child) | `ContextMenu` (wraps triggerChild) |
| Dropdown menu | `DropdownMenu` (wraps child button) | `DropdownMenu` (uses trigger param) |
| Shortcut display | `MenuShortcut` widget | `shortcut` string parameter |
| Disabled state | `enabled: false` on MenuButton | `isDisabled: true` / `disabled: true` |
| Active state | N/A | `isActive: true` on MenuItem |

### Key Differences

- **Callback signatures**: Flutter `onPressed` receives `BuildContext`; Web `onSelect`/`onClick` varies by component.
- **Item composition**: Flutter uses widget children (`leading`, `trailing`, `child`); Web uses string `label` or component children.
- **Styling**: Flutter uses `MenuTheme`; Web uses CoUI size/style classes (`Menu.sm`, `Menu.horizontal`).
- **Navigation**: Web `MenuItem` supports `href` for routing; Flutter uses callback-based navigation.

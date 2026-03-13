---
name: coui-navigation
description: Activate when creating navigation bars, navigation rails, sidebars, breadcrumbs, or pagination in CoUI Flutter or Web using NavigationBar, NavigationRail, NavigationSidebar, Breadcrumb, or Pagination.
---

# CoUI Navigation

## Overview

Navigation components for building app shells, page navigation, and wayfinding across both Flutter and Web platforms. Shared components include NavigationBar and Pagination. Flutter adds NavigationRail and NavigationSidebar; Web adds Breadcrumb.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### NavigationBar

Bottom or top navigation bar:

```dart
int selectedIndex = 0;

NavigationBar(
  index: selectedIndex,
  onChanged: (index) {
    setState(() => selectedIndex = index);
  },
  children: [
    NavigationBarItem(
      icon: const Icon(Icons.home),
      label: const Text('Home'),
    ),
    NavigationBarItem(
      icon: const Icon(Icons.search),
      label: const Text('Search'),
    ),
    NavigationBarItem(
      icon: const Icon(Icons.person),
      label: const Text('Profile'),
    ),
  ],
)
```

### NavigationBarAlignment

```dart
enum NavigationBarAlignment {
  center,
  end,
  spaceAround,
  spaceBetween,
  spaceEvenly,
  start,
}
```

### NavigationRail

Vertical side navigation (icon-focused):

```dart
NavigationRail(
  index: selectedIndex,
  onChanged: (index) {
    setState(() => selectedIndex = index);
  },
  children: [
    NavigationRailItem(
      icon: const Icon(Icons.home),
      label: const Text('Home'),
    ),
    NavigationRailItem(
      icon: const Icon(Icons.analytics),
      label: const Text('Analytics'),
    ),
    NavigationRailItem(
      icon: const Icon(Icons.settings),
      label: const Text('Settings'),
    ),
  ],
)
```

### NavigationRailAlignment

```dart
enum NavigationRailAlignment {
  center,
  end,
  start,
}
```

### NavigationSidebar

Full sidebar navigation with labels and sections:

```dart
NavigationSidebar(
  index: selectedIndex,
  onChanged: (index) {
    setState(() => selectedIndex = index);
  },
  children: [
    NavigationLabel(child: const Text('Main')),
    NavigationSidebarItem(
      leading: const Icon(Icons.dashboard),
      child: const Text('Dashboard'),
    ),
    NavigationSidebarItem(
      leading: const Icon(Icons.people),
      child: const Text('Users'),
    ),
    NavigationLabel(child: const Text('Settings')),
    NavigationSidebarItem(
      leading: const Icon(Icons.settings),
      child: const Text('General'),
    ),
    NavigationSidebarItem(
      leading: const Icon(Icons.security),
      child: const Text('Security'),
    ),
  ],
)
```

### Pagination (Flutter)

```dart
Pagination(
  page: currentPage,
  totalPages: 10,
  onChanged: (page) {
    setState(() => currentPage = page);
  },
)
```

### NavigationContainerType

```dart
enum NavigationContainerType {
  bar,      // Horizontal bar
  rail,     // Vertical rail (icons)
  sidebar,  // Expandable sidebar
}
```

### Label Display Modes

```dart
NavigationBar(labelType: NavigationLabelType.all, ...)       // All show labels
NavigationBar(labelType: NavigationLabelType.selected, ...)  // Only selected shows label
NavigationRail(labelType: NavigationLabelType.tooltip, ...)  // Tooltip on hover
NavigationSidebar(labelType: NavigationLabelType.expanded, ...) // Labels when expanded
```

### Item Components

- `NavigationItem` - Selectable item (icon + label)
- `NavigationButton` - Non-selectable, click action only
- `NavigationLabel` - Section label (non-selectable)
- `NavigationDivider` - Visual separator
- `NavigationGap` - Spacing element

### Surface Effects

```dart
NavigationBar(
  surfaceBlur: 10.0,
  surfaceOpacity: 0.8,
  backgroundColor: Colors.white.withOpacity(0.5),
  children: items,
)
```

### NavigationBarTheme

```dart
const NavigationBarTheme(
  backgroundColor: Colors.white,
  alignment: NavigationBarAlignment.spaceAround,
)
```

### App Shell Pattern (Flutter)

```dart
Scaffold(
  body: Row(
    children: [
      NavigationSidebar(
        index: selectedIndex,
        onChanged: (i) => setState(() => selectedIndex = i),
        children: [
          NavigationSidebarItem(
            leading: const Icon(Icons.home),
            child: const Text('Home'),
          ),
          NavigationSidebarItem(
            leading: const Icon(Icons.settings),
            child: const Text('Settings'),
          ),
        ],
      ),
      Expanded(
        child: pages[selectedIndex],
      ),
    ],
  ),
)
```

### Mobile App Pattern (Flutter)

```dart
Scaffold(
  body: pages[selectedIndex],
  bottomNavigationBar: NavigationBar(
    index: selectedIndex,
    onChanged: (i) => setState(() => selectedIndex = i),
    children: [
      NavigationBarItem(
        icon: const Icon(Icons.home),
        label: const Text('Home'),
      ),
      NavigationBarItem(
        icon: const Icon(Icons.explore),
        label: const Text('Explore'),
      ),
      NavigationBarItem(
        icon: const Icon(Icons.person),
        label: const Text('Profile'),
      ),
    ],
  ),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### NavigationBar (Web)

A bottom-style navigation bar with icon/label items:

```dart
NavigationBar(
  currentIndex: 0,
  onIndexChanged: (index) => print('Selected: $index'),
  items: [
    NavigationItem(label: 'Home'),
    NavigationItem(label: 'Search'),
    NavigationItem(label: 'Profile'),
  ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<NavigationItem>` | required | Navigation items |
| `currentIndex` | `int` | `0` | Selected item index |
| `onIndexChanged` | `NavigationCallback?` | `null` | Selection callback |

#### NavigationItem

```dart
NavigationItem(label: 'Home')
NavigationItem(icon: iconComponent, label: 'Home')
NavigationItem(icon: iconComponent)  // icon only
```

At least one of `icon` or `label` must be provided.

#### With Icons

```dart
NavigationBar(
  currentIndex: activeIndex,
  onIndexChanged: (i) => setState(() => activeIndex = i),
  items: [
    NavigationItem(
      icon: span([Component.text('H')], classes: 'text-lg'),
      label: 'Home',
    ),
    NavigationItem(
      icon: span([Component.text('S')], classes: 'text-lg'),
      label: 'Search',
    ),
    NavigationItem(
      icon: span([Component.text('P')], classes: 'text-lg'),
      label: 'Profile',
    ),
  ],
)
```

Active item gets `bg-accent text-accent-foreground` styling and `aria-current="page"`.

### Breadcrumb

A breadcrumb navigation trail (Web only):

```dart
Breadcrumb(
  items: [
    BreadcrumbItem(label: 'Home', href: '/'),
    BreadcrumbItem(label: 'Products', href: '/products'),
    BreadcrumbItem(label: 'Laptop', isActive: true),
  ],
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `items` | `List<BreadcrumbItem>` | required | Breadcrumb items |
| `separator` | `String` | `'/'` | Separator character |

#### BreadcrumbItem Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `label` | `String` | required | Display text |
| `href` | `String?` | `null` | Link URL |
| `isActive` | `bool` | `false` | Current page indicator |

Active items render as `<span>` with `aria-current="page"`. Non-active items with `href` render as `<a>` links.

#### Custom Separator

```dart
Breadcrumb(
  separator: '>',
  items: [
    BreadcrumbItem(label: 'Home', href: '/'),
    BreadcrumbItem(label: 'Settings', isActive: true),
  ],
)
```

### Pagination (Web)

```dart
Pagination(
  page: 1,
  totalPages: 10,
  onPageChanged: (page) => print('Page: $page'),
)
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `page` | `int` | required | Current page (1-indexed) |
| `totalPages` | `int` | required | Total number of pages |
| `onPageChanged` | `PageChangeCallback?` | `null` | Page change callback |

#### Behavior

- Shows previous/next buttons with chevron icons
- If `totalPages <= 7`: shows all page numbers
- If `totalPages > 7`: shows first, current, last with ellipsis
- Previous button disabled on page 1
- Next button disabled on last page
- Active page gets `bg-primary text-primary-foreground` styling and `aria-current="page"`

#### Full Example

```dart
class PaginatedList extends StatefulComponent {
  @override
  State<PaginatedList> createState() => _PaginatedListState();
}

class _PaginatedListState extends State<PaginatedList> {
  int currentPage = 1;
  static const totalPages = 20;

  @override
  Iterable<Component> build(BuildContext context) sync* {
    yield div(
      [
        div(
          [Component.text('Page $currentPage content')],
          classes: 'p-4',
        ),
        Pagination(
          page: currentPage,
          totalPages: totalPages,
          onPageChanged: (page) => setState(() => currentPage = page),
        ),
      ],
    );
  }
}
```

### Combined Navigation Layout (Web)

```dart
div(
  [
    Breadcrumb(
      items: [
        BreadcrumbItem(label: 'Dashboard', href: '/'),
        BreadcrumbItem(label: 'Users', isActive: true),
      ],
    ),
    Card(
      children: [
        CardContent(child: Table(children: [/* ... */])),
        CardFooter(
          child: Pagination(
            page: currentPage,
            totalPages: totalPages,
            onPageChanged: handlePageChange,
          ),
        ),
      ],
    ),
    NavigationBar(
      currentIndex: activeNav,
      onIndexChanged: handleNavChange,
      items: [
        NavigationItem(label: 'Home'),
        NavigationItem(label: 'Users'),
        NavigationItem(label: 'Settings'),
      ],
    ),
  ],
  classes: 'space-y-4',
)
```

## Common Patterns

### API Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Selected index prop | `index` | `currentIndex` |
| Selection callback | `onChanged` | `onIndexChanged` |
| Items container | `children` (widgets) | `items` (data objects) |
| Bar item type | `NavigationBarItem` | `NavigationItem` |
| Pagination callback | `onChanged` | `onPageChanged` |

### Shared Concepts

- Both platforms use integer-based index selection for NavigationBar.
- Both platforms provide Pagination with `page` and `totalPages` parameters.
- Flutter uses widget composition (`Icon`, `Text` widgets); Web uses data classes (`label` strings, optional `icon` components).
- NavigationRail and NavigationSidebar are Flutter-only; Breadcrumb is Web-only.

### Responsive Navigation Pattern (Flutter)

```dart
LayoutBuilder(
  builder: (context, constraints) {
    final isDesktop = constraints.maxWidth >= 1024;
    final isTablet = constraints.maxWidth >= 768;

    return Row(children: [
      if (isDesktop)
        NavigationSidebar(
          expanded: true,
          index: selectedIndex,
          onChanged: handleNavSelect,
          children: navItems,
        )
      else if (isTablet)
        NavigationRail(
          index: selectedIndex,
          onChanged: handleNavSelect,
          children: navItems,
        ),
      Expanded(child: pageContent),
    ]);
  },
)
```

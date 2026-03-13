---
name: coui-pagination
description: Activate when creating page navigation controls, paginated lists, or multi-page content navigation using CouiPagination, Pagination, or onPageChanged in CoUI Flutter or CoUI Web.
---

# CoUI Pagination

## Overview

The Pagination component enables navigation through large content divided into multiple pages. It displays the current page, supports previous/next navigation, and optionally includes first/last page buttons with configurable sibling count.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Pagination

```dart
CouiPagination(
  totalPages: 10,
  currentPage: _currentPage,
  onPageChanged: (page) {
    setState(() => _currentPage = page);
  },
)
```

### Advanced Configuration

```dart
CouiPagination(
  totalPages: 20,
  currentPage: _currentPage,
  onPageChanged: (page) {
    setState(() => _currentPage = page);
  },
  siblingCount: 2,
  showFirstLast: true,
  showPrevNext: true,
)
```

### Key Classes

#### CouiPagination

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `totalPages` | `int` | required | Total page count |
| `currentPage` | `int` | required | Active page (1-indexed) |
| `onPageChanged` | `void Function(int)` | required | Page change callback |
| `siblingCount` | `int` | `1` | Adjacent page buttons shown |
| `showFirstLast` | `bool` | `false` | Show jump-to-first/last buttons |
| `showPrevNext` | `bool` | `true` | Show previous/next buttons |

### Paginated List Pattern

```dart
Column(
  children: [
    Expanded(
      child: ListView.builder(
        itemCount: itemsPerPage,
        itemBuilder: (context, index) {
          final itemIndex = (_currentPage - 1) * itemsPerPage + index;
          return ListTile(title: Text(items[itemIndex]));
        },
      ),
    ),
    CouiPagination(
      totalPages: (items.length / itemsPerPage).ceil(),
      currentPage: _currentPage,
      onPageChanged: (page) => setState(() => _currentPage = page),
    ),
  ],
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Pagination

```dart
Pagination(
  totalPages: 10,
  currentPage: _currentPage,
  onPageChanged: (page) => setState(() => _currentPage = page),
)
```

### Advanced Configuration

```dart
Pagination(
  totalPages: 20,
  currentPage: _currentPage,
  onPageChanged: (page) => setState(() => _currentPage = page),
  siblingCount: 2,
  showFirstLast: true,
  showPrevNext: true,
)
```

### Paginated Table Pattern

```dart
div(
  [
    Card(
      children: [
        CardContent(child: Table(children: [/* table rows */])),
        CardFooter(
          child: Pagination(
            page: currentPage,
            totalPages: totalPages,
            onPageChanged: handlePageChange,
          ),
        ),
      ],
    ),
  ],
)
```

## Common Patterns

### Variants

| Variant | Description |
|---------|-------------|
| Default | Numeric buttons with previous/next controls |
| Extended | Includes first/last page jump buttons (`showFirstLast: true`) |
| Wide Sibling | Expanded range of page numbers around current (`siblingCount: 2+`) |

### Behavior

- Previous button is disabled on page 1.
- Next button is disabled on the last page.
- When `totalPages <= 7`, all page numbers are shown.
- When `totalPages > 7`, ellipsis is used between first, current range, and last.
- Active page is visually highlighted.

### API Consistency

- Both Flutter and Web share `totalPages`, `currentPage`, `onPageChanged`, `siblingCount`, `showFirstLast`, and `showPrevNext` parameters.

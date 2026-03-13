---
name: coui-table
description: Activate when creating data tables, sortable tables, tabular data displays, or table layouts with headers, rows, footers, and cells using Table, TableHeader, TableBody, TableRow, TableHead, TableCell in CoUI Flutter or Web.
---

# CoUI Table

## Overview

The Table component displays tabular data with headers, body rows, and optional footers. Both Flutter and Web packages provide a `Table` widget with similar structure but platform-specific APIs.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Table

```dart
Table(
  header: TableRow(
    children: [
      TableCell(child: const Text('Name').bold),
      TableCell(child: const Text('Email').bold),
      TableCell(child: const Text('Status').bold),
    ],
  ),
  children: [
    TableRow(
      children: [
        TableCell(child: const Text('John Doe')),
        TableCell(child: const Text('john@example.com')),
        TableCell(child: SecondaryBadge(child: const Text('Active'))),
      ],
    ),
    TableRow(
      children: [
        TableCell(child: const Text('Jane Smith')),
        TableCell(child: const Text('jane@example.com')),
        TableCell(child: OutlineBadge(child: const Text('Pending'))),
      ],
    ),
  ],
)
```

### Table with Footer

```dart
Table(
  header: TableRow(
    children: [
      TableCell(child: const Text('Item').bold),
      TableCell(child: const Text('Amount').bold),
    ],
  ),
  children: [
    TableRow(
      children: [
        TableCell(child: const Text('Product A')),
        TableCell(child: const Text('\$99.00')),
      ],
    ),
    TableRow(
      children: [
        TableCell(child: const Text('Product B')),
        TableCell(child: const Text('\$49.00')),
      ],
    ),
  ],
  footer: TableRow(
    children: [
      TableCell(child: const Text('Total').bold),
      TableCell(child: const Text('\$148.00').bold),
    ],
  ),
)
```

### User Management Table Pattern

```dart
Table(
  header: TableRow(
    children: [
      TableCell(child: const Text('User').bold),
      TableCell(child: const Text('Role').bold),
      TableCell(child: const Text('Status').bold),
      TableCell(child: const Text('Actions').bold),
    ],
  ),
  children: users.map((user) => TableRow(
    children: [
      TableCell(
        child: Row(
          children: [
            Avatar(initials: Avatar.getInitials(user.name)),
            Gap.h(8),
            Text(user.name),
          ],
        ),
      ),
      TableCell(child: Text(user.role)),
      TableCell(
        child: user.active
            ? SecondaryBadge(child: const Text('Active'))
            : OutlineBadge(child: const Text('Inactive')),
      ),
      TableCell(
        child: IconButton.ghost(
          icon: const Icon(Icons.more_vert),
          onPressed: () {},
          density: ButtonDensity.icon,
        ),
      ),
    ],
  )).toList(),
)
```

### Flutter Key Classes

#### Table

Top-level container.

| Parameter | Type | Description |
|-----------|------|-------------|
| `header` | `TableRow?` | Header row |
| `children` | `List<TableRow>` | Data rows |
| `footer` | `TableRow?` | Footer row |

#### TableRow

A single row.

| Parameter | Type | Description |
|-----------|------|-------------|
| `children` | `List<Widget>` | Cells in the row |

#### TableCell

A single cell.

| Parameter | Type | Description |
|-----------|------|-------------|
| `child` | `Widget` (required) | Cell content |

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
Table(
  children: [
    TableHeader(
      children: [
        TableRow(
          children: [
            TableHead(child: Component.text('Name')),
            TableHead(child: Component.text('Email')),
            TableHead(child: Component.text('Status')),
          ],
        ),
      ],
    ),
    TableBody(
      children: [
        TableRow(
          children: [
            TableCell(child: Component.text('John Doe')),
            TableCell(child: Component.text('john@example.com')),
            TableCell(child: Badge.primary(child: Component.text('Active'))),
          ],
        ),
        TableRow(
          children: [
            TableCell(child: Component.text('Jane Smith')),
            TableCell(child: Component.text('jane@example.com')),
            TableCell(child: Badge.secondary(child: Component.text('Pending'))),
          ],
        ),
      ],
    ),
  ],
)
```

### Dynamic Data Table

```dart
Table(
  children: [
    TableHeader(
      children: [
        TableRow(
          children: columns
              .map((col) => TableHead(child: Component.text(col)))
              .toList(),
        ),
      ],
    ),
    TableBody(
      children: [
        for (final row in data)
          TableRow(
            children: columns
                .map((col) => TableCell(child: Component.text(row[col] ?? '')))
                .toList(),
          ),
      ],
    ),
  ],
)
```

### With Actions Column

```dart
Table(
  children: [
    TableHeader(
      children: [
        TableRow(
          children: [
            TableHead(child: Component.text('Name')),
            TableHead(child: Component.text('Role')),
            TableHead(child: Component.text('Actions')),
          ],
        ),
      ],
    ),
    TableBody(
      children: [
        for (final user in users)
          TableRow(
            children: [
              TableCell(
                child: div(
                  [
                    Avatar.initials(
                      Avatar.getInitials(user.name),
                      size: AvatarSize.sm,
                    ),
                    Component.text(user.name),
                  ],
                  classes: 'flex items-center gap-2',
                ),
              ),
              TableCell(child: Component.text(user.role)),
              TableCell(
                child: div(
                  [
                    Button.ghost(
                      size: CoButtonSize.sm,
                      onPressed: () => editUser(user),
                      child: Component.text('Edit'),
                    ),
                    Button.ghost(
                      size: CoButtonSize.sm,
                      onPressed: () => deleteUser(user),
                      child: Component.text('Delete'),
                    ),
                  ],
                  classes: 'flex gap-1',
                ),
              ),
            ],
          ),
      ],
    ),
  ],
)
```

### In a Card

```dart
Card(
  children: [
    CardHeader(
      child: CardTitle(titleChild: Component.text('Users')),
    ),
    CardContent(
      child: Table(
        children: [
          TableHeader(children: [/* ... */]),
          TableBody(children: [/* ... */]),
        ],
      ),
    ),
  ],
)
```

### Web Components Reference

| Component | HTML Element | Default Styling |
|-----------|-------------|-----------------|
| `Table` | `<table>` | `w-full caption-bottom text-sm` |
| `TableHeader` | `<thead>` | Row border styling |
| `TableBody` | `<tbody>` | Last-row border removal |
| `TableRow` | `<tr>` | Border, `hover:bg-muted/50`, selected state |
| `TableHead` | `<th>` | `h-12 px-4 text-left align-middle font-medium text-muted-foreground` |
| `TableCell` | `<td>` | `p-4 align-middle` |

### Web Common Parameters

Each web table component accepts:

| Parameter | Type | Description |
|-----------|------|-------------|
| `children` | `List<Component>?` | Child components |
| `child` | `Component?` | Single child (TableHead, TableCell) |
| `classes` | `String?` | Additional CSS classes |
| `id` | `String?` | HTML id |
| `css` | `Styles?` | Inline styles |
| `attributes` | `Map<String, String>?` | Custom attributes |

## Common Patterns

### Structural Differences

| Concept | Flutter | Web |
|---------|---------|-----|
| Header | `Table(header: TableRow(...))` | `TableHeader(children: [TableRow(...)])` |
| Header cell | `TableCell(child: Text('x').bold)` | `TableHead(child: Component.text('x'))` |
| Body rows | `Table(children: [...])` | `TableBody(children: [...])` |
| Footer | `Table(footer: TableRow(...))` | Not yet supported |
| Text | `Text('...')` | `Component.text('...')` |
| Badge | `SecondaryBadge(...)` / `OutlineBadge(...)` | `Badge.primary(...)` / `Badge.secondary(...)` |
| Avatar | `Avatar(initials: ...)` | `Avatar.initials(..., size: AvatarSize.sm)` |
| Ghost button | `IconButton.ghost(...)` | `Button.ghost(size: CoButtonSize.sm, ...)` |

### Advanced Features (Flutter)

#### Selectable Rows

```dart
Table(
  header: headerRow,
  children: users.map((user) => TableRow(
    selected: selectedUsers.contains(user),
    children: [/* cells */],
  )).toList(),
)
```

Selected rows change background color for visual feedback.

#### Frozen Cells

```dart
Table(
  header: headerRow,
  children: rows,
  frozenCells: FrozenTableData(
    frozenRows: [TableRef(0)],     // Header frozen
    frozenColumns: [TableRef(0)],  // First column frozen
  ),
)
```

Header and first column remain visible during scrolling.

#### Cell Merging

```dart
TableCell(
  columnSpan: 2,  // 2-column merge
  rowSpan: 3,     // 3-row merge
  child: Text('Merged cell'),
)
```

#### Sizing Options

- `FlexTableSize` - flexible sizing
- `FixedTableSize` - fixed pixel sizing
- `IntrinsicTableSize` - content-based sizing

### Shared Patterns

- Both use `TableRow` with a `children` list of cells.
- Both use `TableCell` for body data cells with a `child` parameter.
- Dynamic rows can be built with `.map().toList()` or collection `for`.
- User tables commonly pair Avatar + name in the first column and action buttons in the last column.

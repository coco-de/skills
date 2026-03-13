---
name: coui-tree
description: Activate when creating hierarchical tree views, file explorers, organizational charts, or nested category selectors using Tree, Tree, TreeNode, showCheckbox, or expandAll in CoUI Flutter or CoUI Web.
---

# CoUI Tree

## Overview

The Tree component displays and navigates hierarchical data in a tree structure. It supports expand/collapse, node selection, and optional checkboxes, making it suitable for file explorers, category trees, and organizational charts.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Tree

```dart
Tree(
  nodes: [
    TreeNode(
      id: 'root',
      label: 'Project',
      children: [
        TreeNode(id: 'src', label: 'src', children: [
          TreeNode(id: 'main', label: 'main.dart'),
          TreeNode(id: 'app', label: 'app.dart'),
        ]),
        TreeNode(id: 'test', label: 'test'),
      ],
    ),
  ],
  onNodeTap: (node) {
    // Handle node selection
  },
  onExpand: (node) {
    // Handle node expansion
  },
)
```

### With Checkboxes

```dart
Tree(
  nodes: categoryTree,
  showCheckbox: true,
  selectable: true,
  onNodeTap: (node) {
    // Handle category selected
  },
)
```

### Fully Expanded

```dart
Tree(
  nodes: fileStructure,
  expandAll: true,
  onNodeTap: handleNodeTapped,
)
```

### Key Classes

#### Tree

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `nodes` | `List<TreeNode>` | required | Tree node list |
| `onNodeTap` | `ValueChanged<TreeNode>?` | `null` | Node tap callback |
| `onExpand` | `ValueChanged<TreeNode>?` | `null` | Node expand callback |
| `showCheckbox` | `bool` | `false` | Show checkboxes |
| `selectable` | `bool` | `false` | Allow node selection |
| `expandAll` | `bool` | `false` | Expand all nodes initially |

#### TreeNode

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `id` | `String` | required | Unique node identifier |
| `label` | `String` | required | Display text |
| `children` | `List<TreeNode>?` | `null` | Child nodes |

### File Explorer Pattern

```dart
Tree(
  nodes: [
    TreeNode(id: 'lib', label: 'lib', children: [
      TreeNode(id: 'src', label: 'src', children: [
        TreeNode(id: 'widgets', label: 'widgets', children: [
          TreeNode(id: 'button', label: 'button.dart'),
          TreeNode(id: 'card', label: 'card.dart'),
        ]),
        TreeNode(id: 'models', label: 'models', children: [
          TreeNode(id: 'user', label: 'user.dart'),
        ]),
      ]),
      TreeNode(id: 'main', label: 'main.dart'),
    ]),
    TreeNode(id: 'test', label: 'test', children: [
      TreeNode(id: 'widget_test', label: 'widget_test.dart'),
    ]),
  ],
  onNodeTap: (node) => openFile(node.id),
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Tree

```dart
Tree(
  nodes: fileStructure,
  onNodeTap: handleNodeTapped,
)
```

### With Checkbox Selection

```dart
Tree(
  nodes: categoryTree,
  showCheckbox: true,
  selectable: true,
  expandAll: false,
  onNodeTap: handleCategorySelected,
)
```

## Common Patterns

### Use Cases

| Pattern | Configuration |
|---------|---------------|
| File explorer | Basic tree with expand/collapse |
| Category selector | `showCheckbox: true`, `selectable: true` |
| Org chart | Read-only tree, `expandAll: true` |
| Permission tree | Checkbox multi-select |

### API Consistency

- Both Flutter and Web share the same parameters: `nodes`, `onNodeTap`, `onExpand`, `showCheckbox`, `selectable`, and `expandAll`.
- TreeNode structure is identical across platforms.

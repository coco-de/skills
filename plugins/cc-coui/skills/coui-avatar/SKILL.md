---
name: coui-avatar
description: Activate when creating avatar images, user profile icons, initials displays, placeholder avatars, avatar badges, or avatar groups in CoUI Flutter or Web using Avatar, AvatarBadge, AvatarGroup.
---

# CoUI Avatar

## Overview

The Avatar component displays user profile images, initials, or placeholder icons. Both Flutter and Web platforms provide `Avatar`, `AvatarGroup`, and a shared `Avatar.getInitials` helper. Flutter additionally supports `AvatarBadge` for status indicators.

## Flutter (coui_flutter)

### Import

```dart
import 'package:coui_flutter/coui_flutter.dart';
```

### Basic Usage

#### With Image

```dart
Avatar(
  provider: NetworkImage('https://example.com/avatar.jpg'),
  initials: Avatar.getInitials('John Doe'),
  backgroundColor: Colors.blue,
)
```

#### With Initials

```dart
Avatar(initials: Avatar.getInitials('Jane Smith'))
// Displays "JS"

Avatar(initials: 'AB')
```

#### With Icon

```dart
Avatar(child: const Icon(Icons.person))
```

### Key Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `provider` | `ImageProvider?` | Image source |
| `initials` | `String?` | Fallback initials (e.g., "JS") |
| `child` | `Widget?` | Custom widget (icon) |
| `backgroundColor` | `Color?` | Background color |

### AvatarGroup

Display multiple avatars stacked together:

```dart
AvatarGroup(
  children: [
    Avatar(initials: 'JD'),
    Avatar(initials: 'AS'),
    Avatar(initials: 'MK'),
  ],
)
```

### AvatarBadge

Add a status indicator to an avatar:

```dart
Avatar(
  provider: NetworkImage(user.photoUrl),
  initials: Avatar.getInitials(user.name),
  badge: AvatarBadge(
    color: Colors.green, // online status
  ),
)
```

### Profile Header Pattern

```dart
Row(
  children: [
    Avatar(
      provider: NetworkImage(user.photoUrl),
      initials: Avatar.getInitials(user.name),
    ),
    Gap.h(12),
    Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(user.name).bold,
        Text(user.email).small.base200,
      ],
    ),
  ],
)
```

### Contact List Pattern

```dart
ListView.builder(
  itemCount: contacts.length,
  itemBuilder: (context, index) {
    final contact = contacts[index];
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        children: [
          Avatar(
            initials: Avatar.getInitials(contact.name),
            backgroundColor: contact.color,
          ),
          Gap.h(12),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(contact.name).bold,
                Text(contact.role).small.base200,
              ],
            ),
          ),
        ],
      ),
    );
  },
)
```

## Web (coui_web)

### Import

```dart
import 'package:coui_web/coui_web.dart';
```

### Basic Usage

```dart
// With image
Avatar(src: 'https://example.com/photo.jpg')

// With initials fallback
Avatar(fallback: 'JD')

// Named constructors
Avatar.network('https://example.com/photo.jpg', alt: 'User')
Avatar.initials('JD')
Avatar.placeholder()
```

### Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `src` | `String?` | `null` | Image source URL |
| `fallback` | `String?` | `null` | Fallback text (initials) |
| `alt` | `String?` | `null` | Alt text for image |
| `size` | `AvatarSize` | `AvatarSize.md` | Size preset |
| `ring` | `bool` | `false` | Show ring border |

### Sizes

```dart
Avatar.initials('XS', size: AvatarSize.xs)  // 24px
Avatar.initials('SM', size: AvatarSize.sm)  // 32px
Avatar.initials('MD', size: AvatarSize.md)  // 40px (default)
Avatar.initials('LG', size: AvatarSize.lg)  // 48px
Avatar.initials('XL', size: AvatarSize.xl)  // 64px
```

### With Ring

```dart
Avatar.network(
  'https://example.com/photo.jpg',
  ring: true,
)
```

Adds `ring-2 ring-primary ring-offset-2 ring-offset-base-100` classes.

### Fallback Logic

1. If `src` is provided: renders `<img>` element
2. If `fallback` is provided (no src): renders text in a centered div
3. If neither: renders empty placeholder div

### AvatarGroup

Display overlapping avatars:

```dart
AvatarGroup(
  children: [
    Avatar.network('https://example.com/user1.jpg'),
    Avatar.network('https://example.com/user2.jpg'),
    Avatar.network('https://example.com/user3.jpg'),
  ],
)
```

#### AvatarGroup Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `children` | `List<Avatar>` | required | Avatar components |
| `direction` | `AvatarGroupDirection` | `toLeft` | Stacking direction |
| `max` | `int?` | `null` | Max visible (shows +N) |

#### Stacking Direction

```dart
AvatarGroup.toLeft(children: [...])   // Default left overlap
AvatarGroup.toRight(children: [...])  // Right overlap
```

#### Max Visible

```dart
AvatarGroup(
  max: 3,
  children: [
    Avatar.initials('A'),
    Avatar.initials('B'),
    Avatar.initials('C'),
    Avatar.initials('D'),
    Avatar.initials('E'),
  ],
)
// Shows A, B, C, +2
```

### Complete Web Example

```dart
div(
  [
    // User profile
    div(
      [
        Avatar.network(
          'https://example.com/photo.jpg',
          alt: 'John Doe',
          size: AvatarSize.lg,
          ring: true,
        ),
        div(
          [
            span(
              [Component.text('John Doe')],
              classes: 'font-medium',
            ),
            span(
              [Component.text('john@example.com')],
              classes: 'text-sm text-muted-foreground',
            ),
          ],
          classes: 'flex flex-col',
        ),
      ],
      classes: 'flex items-center gap-3',
    ),
    // Team members
    AvatarGroup(
      max: 4,
      children: teamMembers
          .map((m) => Avatar.initials(Avatar.getInitials(m.name)))
          .toList(),
    ),
  ],
  classes: 'space-y-4',
)
```

## Common Patterns

### Avatar.getInitials

Both platforms share the same static helper to extract initials from a name:

```dart
Avatar.getInitials('John Doe')     // 'JD'
Avatar.getInitials('Jane')         // 'J'
Avatar.getInitials('John M. Doe')  // 'JD'
Avatar.getInitials('Bob Smith')    // 'BS'
```

### API Differences Summary

| Feature | Flutter | Web |
|---------|---------|-----|
| Image source | `provider: NetworkImage(url)` | `src: url` or `Avatar.network(url)` |
| Initials | `initials: 'JD'` | `fallback: 'JD'` or `Avatar.initials('JD')` |
| Placeholder | `child: Icon(Icons.person)` | `Avatar.placeholder()` |
| Badge/Status | `badge: AvatarBadge(color: ...)` | Not available |
| Size presets | Not available | `size: AvatarSize.md` |
| Ring border | Not available | `ring: true` |
| Group max | Not available | `max: 3` |
| Group direction | Not available | `direction: AvatarGroupDirection.toLeft` |

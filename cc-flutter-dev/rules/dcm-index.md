---
paths:
  - "**/*.dart"
---

# DCM Rules Quick Reference

Essential Dart Code Metrics rules for all Dart code in this project.
Reference: https://dcm.dev/docs/rules/

## Severity Levels

| Level | Action | CI Impact |
|-------|--------|-----------|
| **error** | Must fix before commit | Blocks CI |
| **warning** | Should fix | May block CI |
| **style** | Recommended | Informational |

## Critical Rules (Must-Follow)

### Correctness

#### avoid-collection-methods-with-unrelated-types
Collection methods should not receive unrelated types.
```dart
// Bad
final list = <String>['a', 'b'];
list.contains(1); // int vs String

// Good
list.contains('c');
```

#### avoid-recursive-calls
Functions should not call themselves recursively without termination.

#### no-empty-block
Empty blocks should not exist (except in catch).
```dart
// Bad
if (condition) {}

// Good
if (condition) {
  doSomething();
}
```

#### avoid-duplicate-exports
Files should not export the same URI multiple times.

### Memory Leak Prevention

#### dispose-class-fields
Disposable fields must be disposed in class dispose methods.
```dart
// Bad
class MyWidget extends StatefulWidget {
  final _controller = TextEditingController();
  // Missing dispose
}

// Good
@override
void dispose() {
  _controller.dispose();
  super.dispose();
}
```

#### avoid-unassigned-stream-subscriptions
Stream subscriptions must be assigned to variables for cancellation.
```dart
// Bad
stream.listen((data) => print(data));

// Good
final subscription = stream.listen((data) => print(data));
// Later: subscription.cancel();
```

### Async Safety

#### avoid-async-call-in-sync-function
Async functions should not be invoked in non-async blocks without handling.

#### avoid-uncaught-future-errors
Future errors in try/catch might not be caught properly.
```dart
// Bad
try {
  someFuture; // Not awaited
} catch (e) {}

// Good
try {
  await someFuture;
} catch (e) {}
```

### Null Safety

#### avoid-non-null-assertion
Avoid using `!` operator on potentially null values.
```dart
// Bad
final name = user?.name!;

// Good
final name = user?.name ?? 'Unknown';
```

### Code Quality

#### avoid-dynamic
Avoid using `dynamic` type declarations.
```dart
// Bad
dynamic value = getData();

// Good
final Object value = getData();
// Or: final String value = getData() as String;
```

#### avoid-late-keyword
Minimize late keyword usage when possible.

#### prefer-correct-identifier-length
Identifiers should have appropriate length (min 3 characters).
```dart
// Bad
final e = items.first;

// Good
final item = items.first;
```

## Performance Rules

#### avoid-border-all (Flutter)
Use `Border.fromBorderSide` instead of `Border.all`.

#### prefer-const-border-radius (Flutter)
Use const `BorderRadius.all` instead of `BorderRadius.circular`.

#### avoid-incorrect-image-opacity (Flutter)
Image should not be wrapped in Opacity widget.

## Project Exceptions

Some rules have `severity: style` in this project. See `project-config.md` for details.

### Common Exceptions
| Rule | Reason |
|------|--------|
| `avoid-dynamic` | JSON processing requires `Map<String, dynamic>` |
| `avoid-default-tostring` | Logging with `$failure` pattern |
| `avoid-nullable-interpolation` | Debug logging allows nullable |
| `avoid-returning-widgets` | Simple reusable widget functions |

## Quick Commands

```bash
# Run DCM analysis
dcm analyze .

# Run with fix suggestions
dcm analyze --fix .

# Check specific rules
dcm analyze --rule-ids=avoid-dynamic .
```

## Related Files

- [BLoC Rules](./dcm-bloc.md) - BLoC/Cubit specific rules
- [Flutter Rules](./dcm-flutter.md) - Widget specific rules
- [Project Config](./project-config.md) - Project settings

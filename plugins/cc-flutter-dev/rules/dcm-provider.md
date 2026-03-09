# Provider DCM Rules

8 rules specific to Provider package usage.
Reference: https://dcm.dev/docs/rules/provider/

## Critical Rules

### avoid-instantiating-in-value-provider
**Severity**: error

Provider.value should NOT create new instances.

```dart
// Bad - Creates new instance
Provider.value(
  value: MyService(), // Wrong!
  child: child,
)

// Good - Use existing instance
final myService = MyService();
Provider.value(
  value: myService,
  child: child,
)

// Or use regular Provider
Provider(
  create: (_) => MyService(),
  child: child,
)
```

### avoid-read-inside-build
**Severity**: error

read() should NOT be used in build method.

```dart
// Bad
@override
Widget build(BuildContext context) {
  final value = context.read<MyService>().value; // Wrong!
  return Text(value);
}

// Good - Use watch for reactive updates
@override
Widget build(BuildContext context) {
  final value = context.watch<MyService>().value;
  return Text(value);
}

// Good - Use read in callbacks
ElevatedButton(
  onPressed: () {
    context.read<MyService>().doSomething();
  },
  child: Text('Submit'),
)
```

### avoid-watch-outside-build
**Severity**: error

watch/select should NOT be used outside build.

```dart
// Bad
void _handleTap(BuildContext context) {
  final value = context.watch<MyService>().value; // Wrong!
}

// Good
void _handleTap(BuildContext context) {
  final value = context.read<MyService>().value;
}
```

## Memory Management

### dispose-providers
**Severity**: warning

Provided disposable classes should have dispose called.

```dart
// Bad - Resource leak
Provider(
  create: (_) => StreamController(),
  // Missing dispose
  child: child,
)

// Good
Provider(
  create: (_) => StreamController(),
  dispose: (_, controller) => controller.close(),
  child: child,
)
```

## Code Quality

### prefer-multi-provider
**Severity**: style

Use MultiProvider instead of nesting.

```dart
// Bad - Deep nesting
Provider<ServiceA>(
  create: (_) => ServiceA(),
  child: Provider<ServiceB>(
    create: (_) => ServiceB(),
    child: Provider<ServiceC>(
      create: (_) => ServiceC(),
      child: MyApp(),
    ),
  ),
)

// Good - Flat structure
MultiProvider(
  providers: [
    Provider<ServiceA>(create: (_) => ServiceA()),
    Provider<ServiceB>(create: (_) => ServiceB()),
    Provider<ServiceC>(create: (_) => ServiceC()),
  ],
  child: MyApp(),
)
```

### prefer-provider-extensions
**Severity**: style

Use context.read/watch instead of Provider.of.

```dart
// Bad
final service = Provider.of<MyService>(context);
final serviceNoListen = Provider.of<MyService>(context, listen: false);

// Good
final service = context.watch<MyService>();
final serviceNoListen = context.read<MyService>();
```

### prefer-nullable-provider-types
**Severity**: style

Provider watch/read types should be nullable when appropriate.

```dart
// Be careful with non-nullable types
final user = context.watch<User>(); // Throws if not found

// Safer with nullable
final user = context.watch<User?>(); // Returns null if not found
```

### prefer-immutable-selector-value
**Severity**: warning

Selector should not return mutable values.

```dart
// Bad - Returns mutable list
Selector<MyModel, List<Item>>(
  selector: (_, model) => model.items, // Mutable
  builder: (_, items, __) => ListView(...),
)

// Good - Return immutable or use Selector0
Selector<MyModel, List<Item>>(
  selector: (_, model) => List.unmodifiable(model.items),
  builder: (_, items, __) => ListView(...),
)
```

## Quick Reference

| Rule | Severity | Key Point |
|------|----------|-----------|
| avoid-instantiating-in-value-provider | error | Don't create in .value |
| avoid-read-inside-build | error | Use watch in build |
| avoid-watch-outside-build | error | Use read in callbacks |
| dispose-providers | warning | Dispose resources |
| prefer-multi-provider | style | Flatten nesting |
| prefer-provider-extensions | style | Use context.read/watch |

## read vs watch Summary

| Method | Usage | Reactive |
|--------|-------|----------|
| `context.watch<T>()` | In build method | Yes |
| `context.read<T>()` | In callbacks, initState | No |
| `context.select<T, R>()` | In build, specific field | Yes |

```dart
@override
Widget build(BuildContext context) {
  // Rebuilds when any UserModel change
  final user = context.watch<UserModel>();

  // Rebuilds only when name changes
  final name = context.select<UserModel, String>((u) => u.name);

  return Column(
    children: [
      Text(name),
      ElevatedButton(
        onPressed: () {
          // Use read in callbacks
          context.read<UserModel>().updateName('New');
        },
        child: Text('Update'),
      ),
    ],
  );
}
```

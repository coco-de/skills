---
paths:
  - "**/*_bloc.dart"
  - "**/*_cubit.dart"
  - "**/bloc/**/*.dart"
  - "**/cubit/**/*.dart"
---

# BLoC/Cubit DCM Rules

22 rules specific to BLoC pattern implementation.
Reference: https://dcm.dev/docs/rules/bloc/

## Critical Rules (Must-Follow)

### check-is-not-closed-after-async-gap
**Severity**: error

Async handlers MUST check `isClosed` before emitting after await.

```dart
// Bad - May emit after bloc is disposed
Future<void> _onLoad(LoadEvent event, Emitter<State> emit) async {
  emit(const Loading());
  final result = await repository.fetchData();
  emit(Loaded(result)); // Dangerous!
}

// Good - Check isClosed after await
Future<void> _onLoad(LoadEvent event, Emitter<State> emit) async {
  emit(const Loading());
  final result = await repository.fetchData();
  if (isClosed) return; // Must check!
  emit(Loaded(result));
}
```

### avoid-passing-build-context-to-blocs
**Severity**: error

Bloc events and Cubit methods should NOT accept BuildContext.

```dart
// Bad
class MyBloc extends Bloc<MyEvent, MyState> {
  void doSomething(BuildContext context) { ... }
}

// Good - Pass data, not context
class MyBloc extends Bloc<MyEvent, MyState> {
  void doSomething(String userId) { ... }
}
```

### avoid-bloc-public-fields
**Severity**: style (relaxed in this project)

Bloc/Cubit should not have public non-state fields.

```dart
// Bad
class MyBloc extends Bloc<MyEvent, MyState> {
  String publicField = ''; // Avoid
}

// Good - Use state or private fields
class MyBloc extends Bloc<MyEvent, MyState> {
  String _privateField = '';
}
```

### avoid-bloc-public-methods
**Severity**: warning

Bloc should not have non-overridden public methods.

```dart
// Bad
class MyBloc extends Bloc<MyEvent, MyState> {
  void customMethod() { ... } // Use events instead
}

// Good - Use events
class MyBloc extends Bloc<MyEvent, MyState> {
  on<CustomEvent>(_onCustom);
}
```

## State Rules

### emit-new-bloc-state-instances
**Severity**: error

emit() should receive NEW state instances, not modified existing ones.

```dart
// Bad
void _onUpdate(UpdateEvent event, Emitter<State> emit) {
  state.items.add(event.item); // Mutating existing state!
  emit(state);
}

// Good - Create new instance
void _onUpdate(UpdateEvent event, Emitter<State> emit) {
  emit(state.copyWith(
    items: [...state.items, event.item],
  ));
}
```

### prefer-immutable-bloc-state
**Severity**: warning

Bloc state should have @immutable annotation.

```dart
// Good
@immutable
sealed class MyState {
  const MyState();
}
```

### prefer-sealed-bloc-state
**Severity**: warning

Bloc state should be sealed or final class.

```dart
// Good
sealed class MyState {
  const MyState();
}

final class Loading extends MyState {
  const Loading();
}
```

## Event Rules

### handle-bloc-event-subclasses
**Severity**: error

Bloc should handle ALL event subclasses.

```dart
// Bad - Missing handler for DeleteEvent
class MyBloc extends Bloc<MyEvent, MyState> {
  MyBloc() : super(Initial()) {
    on<LoadEvent>(_onLoad);
    // Missing: on<DeleteEvent>(_onDelete);
  }
}
```

### prefer-immutable-bloc-events
**Severity**: warning

Bloc events should have @immutable annotation.

### prefer-sealed-bloc-events
**Severity**: warning

Bloc events should be sealed classes.

```dart
// Good
@immutable
sealed class MyEvent {
  const MyEvent();
}

final class LoadEvent extends MyEvent {
  const LoadEvent({required this.id});
  final int id;
}
```

### prefer-bloc-event-suffix
**Severity**: style

Bloc event names should match pattern (e.g., end with Event).

### prefer-bloc-state-suffix
**Severity**: style

Bloc state names should match pattern (e.g., end with State).

## Provider Rules

### avoid-existing-instances-in-bloc-provider
**Severity**: error

BlocProvider should NOT return existing instances.

```dart
// Bad
BlocProvider.value(
  value: existingBloc, // Risky lifecycle
  child: child,
)

// Good - Create in provider
BlocProvider(
  create: (_) => MyBloc(),
  child: child,
)
```

### avoid-instantiating-in-bloc-value-provider
**Severity**: error

BlocProvider.value should NOT create new instances.

```dart
// Bad
BlocProvider.value(
  value: MyBloc(), // Wrong! Use regular BlocProvider
  child: child,
)
```

### prefer-bloc-extensions
**Severity**: style

Use context.read/watch instead of BlocProvider.of.

```dart
// Bad
final bloc = BlocProvider.of<MyBloc>(context);

// Good
final bloc = context.read<MyBloc>();
```

### prefer-correct-bloc-provider
**Severity**: warning

Bloc should use BlocProvider, not Provider.

### prefer-multi-bloc-provider
**Severity**: style

Use MultiBlocProvider for nested providers.

```dart
// Bad
BlocProvider(
  create: (_) => BlocA(),
  child: BlocProvider(
    create: (_) => BlocB(),
    child: child,
  ),
)

// Good
MultiBlocProvider(
  providers: [
    BlocProvider(create: (_) => BlocA()),
    BlocProvider(create: (_) => BlocB()),
  ],
  child: child,
)
```

## Other Rules

### avoid-cubits
**Severity**: none (disabled in this project)

Cubit usage can be avoided in favor of Bloc. We allow Cubits.

### avoid-duplicate-bloc-event-handlers
**Severity**: error

Bloc should not have duplicate event handlers.

### avoid-passing-bloc-to-bloc
**Severity**: warning

Bloc should not depend on other Blocs directly.

```dart
// Bad
class MyBloc extends Bloc<MyEvent, MyState> {
  MyBloc(this.otherBloc); // Direct dependency
  final OtherBloc otherBloc;
}

// Good - Use events or shared repository
```

### avoid-empty-build-when
**Severity**: warning

BlocBuilder/BlocConsumer should specify buildWhen.

```dart
// Bad
BlocBuilder<MyBloc, MyState>(
  builder: (context, state) => Widget(),
)

// Good
BlocBuilder<MyBloc, MyState>(
  buildWhen: (prev, curr) => prev.status != curr.status,
  builder: (context, state) => Widget(),
)
```

### avoid-returning-value-from-cubit-methods
**Severity**: style

Cubit methods should not return values.

```dart
// Bad
class MyCubit extends Cubit<int> {
  int increment() {
    emit(state + 1);
    return state; // Avoid returning
  }
}

// Good
void increment() => emit(state + 1);
```

## Quick Reference

| Rule | Severity | Key Point |
|------|----------|-----------|
| check-is-not-closed-after-async-gap | error | Check `isClosed` after await |
| emit-new-bloc-state-instances | error | Never mutate existing state |
| handle-bloc-event-subclasses | error | Handle all event types |
| avoid-passing-build-context-to-blocs | error | No BuildContext in Bloc |
| prefer-sealed-bloc-state | warning | Use sealed classes |
| prefer-sealed-bloc-events | warning | Use sealed classes |

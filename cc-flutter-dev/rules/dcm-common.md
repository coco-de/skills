# Common DCM Rules

331 common rules for Dart code quality.
This document covers the most important rules.
Reference: https://dcm.dev/docs/rules/common/

## Correctness Rules

### avoid-collection-methods-with-unrelated-types
**Severity**: error

Collection methods should not receive unrelated types.

```dart
// Bad
final list = <String>['a', 'b'];
list.contains(1);       // int vs String
list.remove(1.5);       // double vs String

// Good
list.contains('c');
```

### avoid-duplicate-exports
**Severity**: error

Files should not export same URI multiple times.

```dart
// Bad
export 'utils.dart';
export 'utils.dart' show helper;  // Duplicate

// Good
export 'utils.dart' show helper;
```

### avoid-recursive-calls
**Severity**: error

Functions should not call themselves without proper termination.

```dart
// Bad - Infinite recursion
int factorial(int n) => n * factorial(n - 1);

// Good - Has base case
int factorial(int n) => n <= 1 ? 1 : n * factorial(n - 1);
```

### no-empty-block
**Severity**: error

Empty blocks should not exist except in catch.

```dart
// Bad
if (condition) {}
while (running) {}

// Good
if (condition) {
  handleCondition();
}
```

### avoid-equal-expressions
**Severity**: error

Binary expressions should not have identical operands.

```dart
// Bad
if (a == a) {}           // Always true
final x = value - value; // Always 0

// Good
if (a == b) {}
```

### avoid-shadowing
**Severity**: warning

Declarations should not shadow others with same name.

```dart
// Bad
String name = 'outer';
void process(String name) {  // Shadows outer
  print(name);
}

// Good
String _name = 'outer';
void process(String name) {
  print(name);
}
```

## Null Safety Rules

### avoid-non-null-assertion
**Severity**: warning

Avoid using `!` operator.

```dart
// Bad
final name = user?.name!;

// Good
final name = user?.name ?? 'Unknown';
// Or
if (user != null) {
  final name = user.name;
}
```

### avoid-nullable-tostring
**Severity**: style

ToString should not be called on nullable values.

```dart
// Bad
final text = nullableValue?.toString();

// Good
final text = nullableValue?.toString() ?? '';
```

### avoid-late-final-reassignment
**Severity**: error

Late final variables should not be assigned multiple times.

```dart
// Bad
late final String name;
name = 'first';
name = 'second';  // Error at runtime

// Good
late final String name;
name = 'only assignment';
```

## Maintainability Rules

### avoid-high-cyclomatic-complexity
**Severity**: warning

Cyclomatic complexity should not exceed threshold (10).

```dart
// Bad - Too many branches
void process(int value) {
  if (value > 10) {
    if (value > 20) {
      if (value > 30) {
        // Deep nesting
      }
    }
  }
}

// Good - Extract to methods
void process(int value) {
  if (value > 30) return _handleLarge(value);
  if (value > 20) return _handleMedium(value);
  if (value > 10) return _handleSmall(value);
}
```

### avoid-long-functions
**Severity**: warning

Functions should not exceed configured line count.

### avoid-long-parameter-list
**Severity**: warning

Parameter lists should not be excessively long (max 4).

```dart
// Bad
void createUser(
  String name, String email, String phone,
  String address, String city, String country,
) {}

// Good - Use object
void createUser(CreateUserParams params) {}

class CreateUserParams {
  final String name;
  final String email;
  // ...
}
```

### prefer-correct-identifier-length
**Severity**: warning

Identifiers should have appropriate length (min 3 chars).

```dart
// Bad
final e = items.first;
items.map((x) => x.value);

// Good
final item = items.first;
items.map((element) => element.value);
```

## Async Rules

### avoid-async-call-in-sync-function
**Severity**: warning

Async functions should not be invoked in non-async blocks without handling.

```dart
// Bad
void doWork() {
  fetchData();  // Future ignored
}

// Good
Future<void> doWork() async {
  await fetchData();
}
// Or
void doWork() {
  fetchData().then(handleResult);
}
```

### avoid-uncaught-future-errors
**Severity**: warning

Future errors in try/catch might not be caught.

```dart
// Bad
try {
  someFuture;  // Not awaited, errors won't be caught
} catch (e) {}

// Good
try {
  await someFuture;
} catch (e) {}
```

### prefer-async-await
**Severity**: style

Use async/await instead of .then() for Futures.

```dart
// Okay but harder to read
void loadData() {
  fetchData()
    .then((data) => processData(data))
    .then((result) => saveResult(result));
}

// Better
Future<void> loadData() async {
  final data = await fetchData();
  final result = await processData(data);
  await saveResult(result);
}
```

## Type Safety Rules

### avoid-dynamic
**Severity**: style (relaxed in project)

Dynamic type should not be used.

```dart
// Bad
dynamic value = getData();
value.anyMethod();  // No type checking

// Good
final Object value = getData();
if (value is String) {
  value.substring(0, 5);
}
```

### avoid-inferrable-type-arguments
**Severity**: style

Inferrable type arguments should be removed.

```dart
// Bad
final list = <String>['a', 'b'];  // Inferrable

// Good
final list = ['a', 'b'];

// Exception: BlocProvider needs explicit type
BlocProvider<MyBloc>(create: (_) => MyBloc())
```

### avoid-unnecessary-type-casts
**Severity**: style

Unnecessary as operator usages should be removed.

```dart
// Bad
final String name = value as String;  // Already String

// Good
final name = value;  // Type inferred
```

## Control Flow Rules

### avoid-nested-conditional-expressions
**Severity**: warning (max level: 2)

Conditional expression nesting should be limited.

```dart
// Bad
final result = a ? (b ? 'x' : (c ? 'y' : 'z')) : 'default';

// Good
String getResult() {
  if (a) {
    return b ? 'x' : (c ? 'y' : 'z');
  }
  return 'default';
}
```

### prefer-early-return
**Severity**: style

If statements should use early return when possible.

```dart
// Bad
void process(User? user) {
  if (user != null) {
    // Many lines of code
  }
}

// Good
void process(User? user) {
  if (user == null) return;
  // Many lines of code
}
```

### prefer-switch-expression
**Severity**: style

Convert switch statements to switch expressions when possible.

```dart
// Okay
String getText(Status status) {
  switch (status) {
    case Status.active:
      return 'Active';
    case Status.inactive:
      return 'Inactive';
  }
}

// Better
String getText(Status status) => switch (status) {
  Status.active => 'Active',
  Status.inactive => 'Inactive',
};
```

## Collections Rules

### avoid-unsafe-collection-methods
**Severity**: style (relaxed in project)

Unsafe collection methods like first/last should be handled.

```dart
// Bad - Throws on empty list
final first = list.first;

// Good
final first = list.firstOrNull;
// Or
if (list.isNotEmpty) {
  final first = list.first;
}
```

### prefer-iterable-of
**Severity**: style

Use List.of() instead of List.from().

```dart
// Bad - Loses type info
final copy = List<String>.from(original);

// Good
final copy = List<String>.of(original);
```

## Code Style Rules

### prefer-trailing-comma
**Severity**: style

Collection literals should have trailing commas.

```dart
// Bad
final list = [
  'item1',
  'item2'
];

// Good
final list = [
  'item1',
  'item2',  // Trailing comma
];
```

### double-literal-format
**Severity**: style

Double literals should begin with 0. and not end with trailing 0.

```dart
// Bad
final value = .5;
final other = 1.50;

// Good
final value = 0.5;
final other = 1.5;
```

### prefer-conditional-expressions
**Severity**: style

Use conditional expressions for if/else assignments.

```dart
// Bad
String result;
if (condition) {
  result = 'yes';
} else {
  result = 'no';
}

// Good
final result = condition ? 'yes' : 'no';
```

## Quick Reference

| Category | Key Rules |
|----------|-----------|
| Correctness | avoid-recursive-calls, no-empty-block, avoid-equal-expressions |
| Null Safety | avoid-non-null-assertion, avoid-late-final-reassignment |
| Async | avoid-async-call-in-sync-function, avoid-uncaught-future-errors |
| Types | avoid-dynamic, avoid-inferrable-type-arguments |
| Control Flow | prefer-early-return, prefer-switch-expression |
| Collections | avoid-unsafe-collection-methods, prefer-iterable-of |

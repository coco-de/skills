---
paths:
  - "**/*_page.dart"
  - "**/*_widget.dart"
  - "**/*_view.dart"
  - "**/*_screen.dart"
  - "**/widget/**/*.dart"
  - "**/page/**/*.dart"
  - "**/presentation/**/*.dart"
---

# Flutter Widget DCM Rules

57 rules specific to Flutter widget development.
Reference: https://dcm.dev/docs/rules/flutter/

## Memory Leak Prevention (Critical)

### always-remove-listener
**Severity**: error

Event listeners MUST be removed in dispose.

```dart
// Bad
@override
void initState() {
  super.initState();
  scrollController.addListener(_onScroll);
}
// Missing removeListener in dispose!

// Good
@override
void initState() {
  super.initState();
  scrollController.addListener(_onScroll);
}

@override
void dispose() {
  scrollController.removeListener(_onScroll);
  super.dispose();
}
```

### dispose-fields
**Severity**: error

Widget state fields MUST be disposed.

```dart
// Bad
class _MyWidgetState extends State<MyWidget> {
  final _controller = TextEditingController();
  // Missing dispose!
}

// Good
class _MyWidgetState extends State<MyWidget> {
  final _controller = TextEditingController();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }
}
```

### avoid-undisposed-instances
**Severity**: warning

Disposable instances should be assigned to variables.

```dart
// Bad - Cannot dispose anonymous controller
TextField(controller: TextEditingController())

// Good
final _controller = TextEditingController();
TextField(controller: _controller)
```

## State Management

### avoid-unnecessary-setstate
**Severity**: error

setState should NOT be called in initState or build.

```dart
// Bad
@override
void initState() {
  super.initState();
  setState(() { _value = 0; }); // Wrong!
}

// Good
@override
void initState() {
  super.initState();
  _value = 0; // Direct assignment
}
```

### use-setstate-synchronously
**Severity**: error

setState should NOT be called after await.

```dart
// Bad
Future<void> _loadData() async {
  final data = await fetchData();
  setState(() { _data = data; }); // May fail if unmounted
}

// Good
Future<void> _loadData() async {
  final data = await fetchData();
  if (!mounted) return;
  setState(() { _data = data; });
}
```

### avoid-empty-setstate
**Severity**: warning

setState callbacks should not be empty.

```dart
// Bad
setState(() {});

// Good
setState(() { _counter++; });
```

### avoid-state-constructors
**Severity**: error

State should not have non-empty constructors.

### avoid-stateless-widget-initialized-fields
**Severity**: warning

StatelessWidget should not have initialized fields.

```dart
// Bad
class MyWidget extends StatelessWidget {
  final items = <String>[]; // Initialized mutable field
}

// Good
class MyWidget extends StatelessWidget {
  const MyWidget({required this.items});
  final List<String> items;
}
```

## Performance Rules

### avoid-returning-widgets
**Severity**: style (relaxed in this project)

Methods should not return Widget or subclasses.

```dart
// Bad
Widget _buildHeader() => Text('Header');

// Good - Extract to separate widget
class _Header extends StatelessWidget {
  @override
  Widget build(BuildContext context) => Text('Header');
}
```

### avoid-unnecessary-stateful-widgets
**Severity**: style

StatefulWidget should convert to StatelessWidget if no state.

### avoid-shrink-wrap-in-lists
**Severity**: warning

ListView with shrinkWrap should not be in Column/Row.

```dart
// Bad - Performance issue
Column(
  children: [
    ListView(shrinkWrap: true, children: items),
  ],
)

// Good
Expanded(
  child: ListView(children: items),
)
```

### avoid-incorrect-image-opacity
**Severity**: warning

Image should NOT be wrapped in Opacity widget.

```dart
// Bad - Creates new layer
Opacity(
  opacity: 0.5,
  child: Image.asset('image.png'),
)

// Good
Image.asset(
  'image.png',
  opacity: AlwaysStoppedAnimation(0.5),
)
```

### avoid-border-all
**Severity**: style

Use Border.fromBorderSide instead of Border.all.

```dart
// Okay but less efficient
Border.all(color: Colors.black)

// Better
Border.fromBorderSide(BorderSide(color: Colors.black))
```

### prefer-const-border-radius
**Severity**: style

Use const BorderRadius.all instead of BorderRadius.circular.

```dart
// Okay
BorderRadius.circular(8)

// Better
const BorderRadius.all(Radius.circular(8))
```

### pass-existing-future-to-future-builder
**Severity**: error

Don't create new futures for FutureBuilder.

```dart
// Bad - Creates new future on every build
FutureBuilder(
  future: fetchData(), // New future each build!
  builder: (context, snapshot) => ...,
)

// Good
final _future = fetchData();
FutureBuilder(
  future: _future,
  builder: (context, snapshot) => ...,
)
```

### pass-existing-stream-to-stream-builder
**Severity**: error

Don't create new streams for StreamBuilder.

## Widget Structure

### avoid-single-child-column-or-row
**Severity**: warning

Column/Row should not have single children.

```dart
// Bad
Column(children: [Text('Hello')])

// Good - Use just the child or Align
Text('Hello')
// or
Align(alignment: Alignment.topLeft, child: Text('Hello'))
```

### avoid-expanded-as-spacer
**Severity**: style

Use Spacer instead of Expanded with empty widget.

```dart
// Bad
Expanded(child: SizedBox())

// Good
const Spacer()
```

### prefer-single-widget-per-file
**Severity**: style (with ignore-private-widgets)

Files should contain one public widget.

### avoid-recursive-widget-calls
**Severity**: error

Widgets should not recursively use themselves.

### avoid-flexible-outside-flex
**Severity**: error

Flexible should not be used outside Flex widgets.

## Widget Preferences

### prefer-sized-box-square
**Severity**: style

Use SizedBox.square when height/width match.

```dart
// Okay
SizedBox(width: 50, height: 50)

// Better
SizedBox.square(dimension: 50)
```

### prefer-text-rich
**Severity**: style

Use Text.rich instead of RichText for accessibility.

### prefer-using-list-view
**Severity**: warning

Use ListView instead of Column with SingleChildScrollView.

### prefer-extracting-callbacks
**Severity**: style

Inline callbacks should be extracted.

```dart
// Bad
ElevatedButton(
  onPressed: () {
    // Long callback code
  },
  child: Text('Submit'),
)

// Good
void _onSubmit() {
  // Callback code
}

ElevatedButton(
  onPressed: _onSubmit,
  child: Text('Submit'),
)
```

## Context Usage

### avoid-inherited-widget-in-initstate
**Severity**: error

dependOnInheritedWidgetOfExactType should NOT be called from initState.

```dart
// Bad
@override
void initState() {
  super.initState();
  final theme = Theme.of(context); // Wrong!
}

// Good
@override
void didChangeDependencies() {
  super.didChangeDependencies();
  final theme = Theme.of(context);
}
```

### avoid-late-context
**Severity**: error

context should NOT be used in late field initializers.

### use-closest-build-context
**Severity**: style (relaxed in this project)

Use closest BuildContext available.

### prefer-dedicated-media-query-methods
**Severity**: warning

Use dedicated methods instead of MediaQuery.of.

```dart
// Bad - Rebuilds on any MediaQuery change
final size = MediaQuery.of(context).size;

// Good - Only rebuilds when size changes
final size = MediaQuery.sizeOf(context);
```

## Lifecycle

### proper-super-calls
**Severity**: error

Super calls should be in correct order.

```dart
// Bad
@override
void initState() {
  _initialize(); // Super should come first
  super.initState();
}

// Good
@override
void initState() {
  super.initState();
  _initialize();
}

// For dispose, super.dispose() should be last
@override
void dispose() {
  _controller.dispose();
  super.dispose(); // Last
}
```

## Quick Reference

| Rule | Severity | Key Point |
|------|----------|-----------|
| always-remove-listener | error | Remove listeners in dispose |
| dispose-fields | error | Dispose all controllers |
| use-setstate-synchronously | error | Check mounted after await |
| avoid-unnecessary-setstate | error | No setState in initState/build |
| proper-super-calls | error | Correct super call order |
| pass-existing-future-to-future-builder | error | Don't create futures in build |
| avoid-inherited-widget-in-initstate | error | No Theme.of in initState |

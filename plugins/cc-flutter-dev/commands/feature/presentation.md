---
name: feature:presentation
description: "Clean Architecture Presentation Layer 생성 (BLoC, Page, Widget, 테스트, Widgetbook)"
invoke: /feature:presentation
aliases: ["/presentation", "/presentation:create"]
category: petmedi-workflow
complexity: standard
mcp-servers: [serena, context7, magic]
---

# /feature:presentation

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/feature:presentation` patterns.

## Triggers

- 새로운 Feature의 Presentation Layer가 필요할 때
- BLoC, Page, Widget, Route 생성이 필요할 때
- `/feature:create` 오케스트레이션의 Step 5에서 호출될 때

## Context Trigger Pattern

```
/feature:presentation {feature_name} {entity_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `community`, `chat` |
| `entity_name` | ✅ | Entity명 (PascalCase) | `Post`, `Message` |
| `--location` | ❌ | 위치 | `application`, `common`, `console` (기본: `application`) |
| `--pages` | ❌ | 생성할 페이지 | `"list, detail, create"` |

## Behavioral Flow

### 1. 기존 패턴 분석

```
Serena MCP를 사용하여 기존 Presentation Layer 패턴 분석:
- feature/application/community/lib/src/presentation/bloc/post_list/post_list_bloc.dart
- feature/application/community/lib/src/presentation/bloc/post_list/post_list_event.dart
- feature/application/community/lib/src/presentation/bloc/post_list/post_list_state.dart
```

### 2. BLoC Event 생성 (sealed class + private 구현)

```dart
part of '{feature}_list_bloc.dart';

/// {Feature} 목록 이벤트
@immutable
sealed class {Feature}ListEvent {
  const {Feature}ListEvent();

  // Factory constructors (Public API)
  const factory {Feature}ListEvent.loadRequested() = _LoadRequested;
  const factory {Feature}ListEvent.refreshRequested() = _RefreshRequested;
  const factory {Feature}ListEvent.categoryChanged({
    {Entity}Category? category,
  }) = _CategoryChanged;
}

// Private implementation classes
@immutable
final class _LoadRequested extends {Feature}ListEvent {
  const _LoadRequested();
}

@immutable
final class _RefreshRequested extends {Feature}ListEvent {
  const _RefreshRequested();
}

@immutable
final class _CategoryChanged extends {Feature}ListEvent {
  const _CategoryChanged({this.category});
  final {Entity}Category? category;
}
```

### 3. BLoC State 생성

```dart
part of '{feature}_list_bloc.dart';

/// {Feature} 목록 상태
@immutable
sealed class {Feature}ListState {
  const {Feature}ListState({
    required this.{entity}s,
    required this.currentSort,
    this.currentCategory,
  });

  final List<{Entity}> {entity}s;
  final {Entity}Category? currentCategory;
  final {Entity}SortType currentSort;
}

@immutable
final class {Feature}ListInitial extends {Feature}ListState {
  const {Feature}ListInitial()
      : super({entity}s: const [], currentSort: {Entity}SortType.latest);
}

@immutable
final class {Feature}ListLoading extends {Feature}ListState { ... }

@immutable
final class {Feature}ListLoaded extends {Feature}ListState {
  // ... hasMore, total 추가
  // copyWith 메서드 포함
}

@immutable
final class {Feature}ListError extends {Feature}ListState {
  // ... message 추가
}
```

### 4. BLoC 클래스 생성 (UseCase 직접 생성)

```dart
import 'package:dependencies/dependencies.dart';

part '{feature}_list_event.dart';
part '{feature}_list_state.dart';

/// {Feature} 목록 BLoC
class {Feature}ListBloc extends Bloc<{Feature}ListEvent, {Feature}ListState> {
  {Feature}ListBloc() : super(const {Feature}ListInitial()) {
    on<_LoadRequested>(_onLoadRequested);
    on<_RefreshRequested>(_onRefreshRequested);
  }

  Future<void> _onLoadRequested(
    _LoadRequested event,
    Emitter<{Feature}ListState> emit,
  ) async {
    emit({Feature}ListLoading(...));

    // ✅ UseCase 직접 생성 및 호출
    final result = await const Get{Entity}sUsecase().call(
      Get{Entity}sParams(
        limit: _pageSize,
        offset: _currentOffset,
        category: state.currentCategory,
      ),
    );

    result.fold(
      (failure) {
        if (!isClosed) {  // ✅ BLoC 종료 체크
          emit({Feature}ListError(message: failure.message ?? '오류'));
        }
      },
      ({entity}ListResult) {
        if (!isClosed) {
          emit({Feature}ListLoaded(...));
        }
      },
    );
  }
}
```

### 5. BLoC Test 생성

```dart
void main() {
  late MockI{Feature}Repository mockRepository;

  setUpAll(registerFallbackValues);

  setUp(() {
    mockRepository = MockI{Feature}Repository();
    registerTestLazySingleton<I{Feature}Repository>(mockRepository);
  });

  tearDown(() {
    verifyNoMoreInteractions(mockRepository);
    getIt.reset();
  });

  blocTest<{Feature}ListBloc, {Feature}ListState>(
    '로드 성공 시 {Feature}ListLoaded 상태',
    build: {Feature}ListBloc.new,  // ✅ 기본 생성자
    setUp: () {
      when(() => mockRepository.get{Entity}s(...))
        .thenAnswer((_) async => Right(testResult));
    },
    act: (bloc) => bloc.add(const {Feature}ListEvent.loadRequested()),
    expect: () => [
      isA<{Feature}ListLoading>(),
      isA<{Feature}ListLoaded>(),
    ],
  );
}
```

### 6. Page 생성 (BlocProvider 래핑)

```dart
class {Feature}Page extends StatelessWidget {
  const {Feature}Page({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (context) =>
          {Feature}ListBloc()..add(const {Feature}ListEvent.loadRequested()),
      child: const {Feature}View(),
    );
  }
}

class {Feature}View extends StatelessWidget {
  const {Feature}View({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('{Feature}')),
      body: BlocBuilder<{Feature}ListBloc, {Feature}ListState>(
        builder: (context, state) {
          return switch (state) {
            {Feature}ListInitial() => const SizedBox.shrink(),
            {Feature}ListLoading() => const Center(child: CircularProgressIndicator()),
            {Feature}ListLoaded(:final {entity}s) => ListView.builder(...),
            {Feature}ListError(:final message) => Center(child: Text('오류: $message')),
          };
        },
      ),
    );
  }
}
```

### 7. Widget 생성 (super.key 마지막)

```dart
class {Entity}Card extends StatelessWidget {
  const {Entity}Card({
    required this.{entity},
    this.onTap,
    super.key,  // ✅ 항상 마지막
  });

  final {Entity} {entity};
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) { ... }
}
```

### 8. Widget Test 생성

```dart
testWidgets('{엔티티} 목록 표시', (tester) async {
  when(() => mockRepository.get{Entity}s(...))
    .thenAnswer((_) async => Right(testResult));

  await tester.pumpWidget(const MaterialApp(home: {Feature}Page()));
  await tester.pumpAndSettle();

  expect(find.byType({Entity}Card), findsNWidgets(2));
});
```

### 9. Route 생성

```dart
@TypedGoRoute<{Feature}Route>(path: '/{feature}')
class {Feature}Route extends GoRouteData with ${Feature}Route {
  const {Feature}Route();

  static RouteBase get base => ${feature}Route;

  @override
  MaterialPage<void> buildPage(BuildContext context, GoRouterState state) {
    return const MaterialPage<void>(child: {Feature}Page());
  }
}

abstract class {Feature}RouteName {
  static const String path = '/{feature}';
}
```

### 10. Widgetbook UseCase 생성

```dart
@widgetbook.UseCase(name: 'Default', type: {Entity}Card)
Widget build{Entity}CardUseCase(BuildContext context) {
  return {Entity}Card(
    {entity}: const {Entity}(id: 1, title: '테스트', ...),
  );
}
```

### 11. BDD 테스트 연동 (선택)

**`/bdd:generate` 명령어로 별도 생성:**

```bash
# BDD 테스트 생성
/bdd:generate {feature_name} --location {location}
```

생성되는 BDD 파일:
```
feature/{location}/{feature_name}/test/src/bdd/
├── {feature}_list.feature
├── {feature}_detail.feature
├── {feature}_form.feature
├── step/
│   └── {feature}_steps.dart
└── hooks/
    └── hooks.dart
```

**BDD 시나리오 예시:**

```gherkin
Feature: {feature} 목록
  사용자로서
  {feature} 목록을 보고 싶습니다

  @smoke
  Scenario: 목록 로딩 성공
    Given 앱이 실행 중입니다
    When {feature} 페이지로 이동합니다
    Then {feature} 목록이 보입니다
```

## Output Files

```
feature/{location}/{feature_name}/lib/src/presentation/
├── bloc/{feature}_list/
│   ├── {feature}_list_bloc.dart
│   ├── {feature}_list_event.dart
│   └── {feature}_list_state.dart
├── page/
│   └── {feature}_page.dart
├── widget/
│   └── {entity}_card.dart
└── route/
    └── {feature}_route.dart

feature/{location}/{feature_name}/test/
├── presentation/
│   ├── bloc/{feature}_list_bloc_test.dart
│   └── page/{feature}_page_test.dart
└── src/bdd/                               # BDD 테스트 (선택)
    ├── {feature}_list.feature
    ├── {feature}_detail.feature
    ├── {feature}_form.feature
    ├── step/{feature}_steps.dart
    └── hooks/hooks.dart

app/petmedi_widgetbook/lib/src/{feature_name}/
└── {entity}_card_use_case.dart
```

## MCP Integration

- **Serena**: 기존 Presentation Layer 패턴 분석
- **Context7**: BLoC, GoRouter 문서 참조
- **Magic (21st.dev)**: UI 컴포넌트 생성, 접근성 검사

## 참조 에이전트

상세 구현 규칙은 `~/.claude/commands/agents/presentation-layer-agent.md` 참조

## 핵심 규칙 요약

### ✅ BLoC 패턴

```dart
// Event: sealed class + factory + private implementation
sealed class {Feature}ListEvent {
  const factory {Feature}ListEvent.loadRequested() = _LoadRequested;
}

final class _LoadRequested extends {Feature}ListEvent {
  const _LoadRequested();
}

// BLoC: UseCase 직접 생성
class {Feature}ListBloc extends Bloc<...> {
  {Feature}ListBloc() : super(...);  // 기본 생성자

  Future<void> _onLoadRequested(...) async {
    final result = await const Get{Entity}sUsecase().call(params);  // ✅ 직접 생성
    if (!isClosed) { emit(...); }  // ✅ 종료 체크
  }
}
```

### ❌ 금지 패턴

```dart
// ❌ UseCase 생성자 주입 금지
// {Feature}ListBloc(this._get{Entity}sUseCase);

// ❌ Key? key 패턴 금지
// const {Entity}Card({Key? key}) : super(key: key);
```

### Widget super.key 위치

```dart
const {Entity}Card({
  required this.{entity},  // required 먼저
  this.onTap,              // optional 다음
  super.key,               // ✅ super.key 마지막
});
```

# BLoC 패턴

> **참조 위치**: `.claude/references/patterns/bloc-patterns.md`

BLoC(Business Logic Component)은 Flutter의 상태 관리 패턴입니다.

---

## State 패턴 비교

| 패턴 | 장점 | 단점 | 권장 상황 |
|------|------|------|----------|
| **Freezed Union** | copyWith, equality 자동 생성, 패턴 매칭 | 코드 생성 필요 | 명확한 상태 분리 (권장) |
| **Sealed Class** | 코드 생성 없음, Dart 3.0+ 네이티브 | 수동 구현 필요 | 코드 생성 회피 시 |
| **Single State** | 복잡한 화면, 여러 상태 조합 | 상태 분리 덜 명확 | 페이지네이션, 필터링 등 |

---

## State 정의

### 옵션 A: Freezed Union State ✅ 권장

```dart
// {feature}_state.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_state.freezed.dart';

@freezed
class UserState with _$UserState {
  const factory UserState.initial() = UserInitial;
  const factory UserState.loading() = UserLoading;
  const factory UserState.loaded({
    required User user,
  }) = UserLoaded;
  const factory UserState.error({
    required Failure failure,
  }) = UserError;
}
```

### 옵션 B: Sealed Class (Dart 3.0+)

```dart
// {feature}_state.dart
sealed class UserState {
  const UserState();
}

final class UserInitial extends UserState {
  const UserInitial();
}

final class UserLoading extends UserState {
  const UserLoading();
}

final class UserLoaded extends UserState {
  const UserLoaded({required this.user});
  final User user;
}

final class UserError extends UserState {
  const UserError({required this.failure});
  final Failure failure;
}
```

### 옵션 C: Single State (복잡한 화면)

```dart
@freezed
class HomeState with _$HomeState {
  const factory HomeState({
    @Default(LoadingStatus.initial) LoadingStatus status,
    @Default([]) List<Item> items,
    Failure? failure,
    @Default(false) bool isRefreshing,
    @Default(false) bool hasMore,
    @Default(0) int page,
  }) = _HomeState;

  const HomeState._();

  bool get isInitial => status == LoadingStatus.initial;
  bool get isLoading => status == LoadingStatus.loading;
  bool get isLoaded => status == LoadingStatus.loaded;
  bool get hasError => failure != null;
}

enum LoadingStatus { initial, loading, loaded, error }
```

---

## Event 정의

### 옵션 A: Freezed

```dart
// {feature}_event.dart
import 'package:freezed_annotation/freezed_annotation.dart';

part 'user_event.freezed.dart';

@freezed
class UserEvent with _$UserEvent {
  const factory UserEvent.load({required int userId}) = UserLoad;
  const factory UserEvent.refresh() = UserRefresh;
  const factory UserEvent.update({required UpdateUserParams params}) = UserUpdate;
  const factory UserEvent.delete() = UserDelete;
}
```

### 옵션 B: Sealed Class

```dart
// {feature}_event.dart
sealed class UserEvent {
  const UserEvent();
}

final class UserLoad extends UserEvent {
  const UserLoad({required this.userId});
  final int userId;
}

final class UserRefresh extends UserEvent {
  const UserRefresh();
}

final class UserUpdate extends UserEvent {
  const UserUpdate({required this.params});
  final UpdateUserParams params;
}
```

---

## UseCase 통합 패턴

BLoC에서 UseCase를 사용하는 두 가지 패턴입니다.

### 패턴 A: 직접 인스턴스화 (Direct Instantiation)

```dart
// BLoC에서 UseCase를 직접 생성하여 호출
class UserBloc extends Bloc<UserEvent, UserState> {
  UserBloc() : super(const UserInitial()) {
    on<UserLoad>(_onLoad);
  }

  Future<void> _onLoad(UserLoad event, Emitter<UserState> emit) async {
    emit(const UserLoading());

    final result = await const GetUserUseCase().call(
      GetUserParams(id: event.userId),
    );

    if (isClosed) return;

    result.fold(
      (failure) => emit(UserError(failure: failure)),
      (user) => emit(UserLoaded(user: user)),
    );
  }
}
```

### 패턴 B: DI 디커플링 (Optional Constructor Injection) ✅ 테스트 용이

테스트 시 mock UseCase를 직접 주입할 수 있어, GetIt 모킹 없이 순수 단위테스트가 가능합니다.

```dart
class UserBloc extends Bloc<UserEvent, UserState> {
  UserBloc({
    GetUserUseCase? getUserUseCase,       // Optional: 테스트 시 mock 주입
    UpdateUserUseCase? updateUserUseCase,
  }) : _getUserUseCase = getUserUseCase ?? const GetUserUseCase(),
       _updateUserUseCase = updateUserUseCase ?? const UpdateUserUseCase(),
       super(const UserInitial()) {
    on<UserLoad>(_onLoad);
    on<UserUpdate>(_onUpdate);
  }

  final GetUserUseCase _getUserUseCase;
  final UpdateUserUseCase _updateUserUseCase;

  Future<void> _onLoad(UserLoad event, Emitter<UserState> emit) async {
    emit(const UserLoading());

    final result = await _getUserUseCase(
      GetUserParams(id: event.userId),
    );

    if (isClosed) return;

    result.fold(
      (failure) => emit(UserError(failure: failure)),
      (user) => emit(UserLoaded(user: user)),
    );
  }
}
```

**UseCase 8개 이상일 때: Bundle 패턴**

```dart
class DashboardUseCases {
  const DashboardUseCases({
    GetStatsUseCase? getStats,
    GetChartDataUseCase? getChartData,
    GetRecentItemsUseCase? getRecentItems,
    // ... 8+ UseCases
  }) : getStats = getStats ?? const GetStatsUseCase(),
       getChartData = getChartData ?? const GetChartDataUseCase(),
       getRecentItems = getRecentItems ?? const GetRecentItemsUseCase();

  final GetStatsUseCase getStats;
  final GetChartDataUseCase getChartData;
  final GetRecentItemsUseCase getRecentItems;
}

class DashboardBloc extends Bloc<DashboardEvent, DashboardState> {
  DashboardBloc({DashboardUseCases? useCases})
      : _useCases = useCases ?? const DashboardUseCases(),
        super(const DashboardState()) {
    on<_Load>(_onLoad);
  }

  final DashboardUseCases _useCases;
}
```

### 테스트 비교

| 항목 | 직접 인스턴스화 | DI 디커플링 |
|------|----------------|------------|
| Mock 대상 | GetIt에 Mock Repository 등록 | Mock UseCase를 생성자에 주입 |
| 격리 수준 | Repository 레벨 | UseCase 레벨 (더 정밀) |
| 설정 코드 | `getIt.registerSingleton(...)` | `UserBloc(getUserUseCase: mockUseCase)` |
| tearDown | `getIt.reset()` 필수 | 불필요 |
| 병렬 테스트 | GetIt 전역 상태로 주의 필요 | 완전 격리, 안전 |

---

## Stream 연동 (SWR/Cache-First)

### 패턴 A: emit.forEach + restartable() ✅ 권장

`emit.forEach`를 사용하면 수동 `StreamSubscription` 관리가 불필요합니다.
`restartable()` 트랜스포머로 파라미터 변경 시 이전 스트림이 자동 취소됩니다.

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';

class HomeBloc extends Bloc<HomeEvent, HomeState> {
  HomeBloc({
    GetItemsStreamUseCase? getItemsStream,
  }) : _getItemsStream = getItemsStream ?? const GetItemsStreamUseCase(),
       super(const HomeState()) {
    on<HomeLoad>(
      _onLoad,
      transformer: restartable(),  // 새 이벤트 시 이전 스트림 자동 취소
    );
  }

  final GetItemsStreamUseCase _getItemsStream;

  Future<void> _onLoad(HomeLoad event, Emitter<HomeState> emit) async {
    // 캐시가 없을 때만 로딩 상태 표시
    if (state.items.isEmpty) {
      emit(state.copyWith(status: LoadingStatus.loading));
    }

    // emit.forEach가 스트림을 구독하고 자동으로 정리
    await emit.forEach<Either<Failure, List<Item>>>(
      _getItemsStream(GetItemsParams(categoryId: event.categoryId)),
      onData: (result) => result.fold(
        (failure) => state.copyWith(
          status: LoadingStatus.error,
          failure: failure,
        ),
        (items) => state.copyWith(
          status: LoadingStatus.loaded,
          items: items,
          lastUpdated: DateTime.now(),
        ),
      ),
    );
  }
  // close() 오버라이드 불필요! emit.forEach가 자동 정리
}
```

#### restartable() 동작 원리

```
1. add(HomeLoad(categoryId: 1))  → 스트림A 구독 시작 (캐시 → 서버 순차 yield)
2. add(HomeLoad(categoryId: 2))  → restartable()가 핸들러1 취소 → 스트림A 해제
                                 → 핸들러2 시작 → 스트림B 구독 시작
```

| 트랜스포머 | 동작 | 사용 시점 |
|-----------|------|----------|
| **`restartable()`** | 이전 핸들러 취소, 새 핸들러 시작 | **파라미터 변경 시 (권장)** |
| `droppable()` | 이전 핸들러 완료까지 새 이벤트 무시 | 중복 호출 방지 |
| `sequential()` | 순차 처리 (큐) | 순서 보장 필요 시 |
| `concurrent()` | 병렬 처리 | 독립적인 이벤트 |

### 패턴 B: 수동 StreamSubscription (레거시)

`emit.forEach`를 사용할 수 없는 특수한 경우에만 사용합니다.

```dart
class HomeBloc extends Bloc<HomeEvent, HomeState> {
  HomeBloc() : super(const HomeState()) {
    on<HomeLoad>(_onLoad);
    on<_HomeItemsUpdated>(_onUpdated);
  }

  StreamSubscription<Either<Failure, List<Item>>>? _subscription;

  Future<void> _onLoad(HomeLoad event, Emitter<HomeState> emit) async {
    emit(state.copyWith(status: LoadingStatus.loading));

    await _subscription?.cancel();
    _subscription = const GetItemsStreamUseCase().call(
      GetItemsParams(categoryId: event.categoryId),
    ).listen(
      (result) => add(_HomeItemsUpdated(result)),
      onError: (error) => add(_HomeError(error)),
    );
  }

  @override
  Future<void> close() {
    _subscription?.cancel();  // 수동 정리 필수!
    return super.close();
  }
}
```

---

## UI 통합

### BlocProvider

```dart
@RoutePage()
class UserPage extends StatelessWidget {
  const UserPage({@PathParam('id') required this.userId, super.key});

  final int userId;

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => UserBloc()
        ..add(UserLoad(userId: userId)),
      child: const UserView(),
    );
  }
}
```

### BlocBuilder

```dart
BlocBuilder<UserBloc, UserState>(
  buildWhen: (previous, current) => previous != current,
  builder: (context, state) {
    return switch (state) {
      UserInitial() => const SizedBox.shrink(),
      UserLoading() => const LoadingIndicator(),
      UserLoaded(:final user) => UserContent(user: user),
      UserError(:final failure) => ErrorView(failure: failure),
    };
  },
)
```

### BlocSelector

```dart
// 특정 필드만 구독
BlocSelector<HomeBloc, HomeState, List<Item>>(
  selector: (state) => state.items,
  builder: (context, items) => ItemList(items: items),
)
```

### BlocListener

```dart
BlocListener<UserBloc, UserState>(
  listenWhen: (previous, current) =>
    previous is! UserError && current is UserError,
  listener: (context, state) {
    if (state is UserError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.failure.message)),
      );
    }
  },
  child: const UserView(),
)
```

---

## Cubit (단순한 경우)

```dart
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
  void reset() => emit(0);
}
```

---

## 테스트

### DI 디커플링 패턴 테스트 ✅ 권장

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';

class MockGetUserUseCase extends Mock implements GetUserUseCase {}

void main() {
  late MockGetUserUseCase mockGetUser;

  setUp(() {
    mockGetUser = MockGetUserUseCase();
  });

  blocTest<UserBloc, UserState>(
    'emits [loading, loaded] when load succeeds',
    setUp: () {
      when(() => mockGetUser(any()))
          .thenAnswer((_) async => right(testUser));
    },
    build: () => UserBloc(getUserUseCase: mockGetUser),  // mock 주입
    act: (bloc) => bloc.add(const UserLoad(userId: 1)),
    expect: () => [
      const UserLoading(),
      UserLoaded(user: testUser),
    ],
  );
}
```

### Stream (emit.forEach) 테스트

```dart
class MockGetItemsStreamUseCase extends Mock implements GetItemsStreamUseCase {}

blocTest<HomeBloc, HomeState>(
  'emits cached then fresh data via SWR stream',
  setUp: () {
    when(() => mockGetItemsStream(any())).thenAnswer(
      (_) => Stream.fromIterable([
        right(cachedItems),   // 캐시 데이터
        right(freshItems),    // 서버 데이터
      ]),
    );
  },
  build: () => HomeBloc(getItemsStream: mockGetItemsStream),
  act: (bloc) => bloc.add(const HomeLoad(categoryId: 1)),
  expect: () => [
    HomeState(status: LoadingStatus.loading),
    HomeState(status: LoadingStatus.loaded, items: cachedItems),
    HomeState(status: LoadingStatus.loaded, items: freshItems),
  ],
);
```

### 직접 인스턴스화 테스트 (GetIt 모킹)

```dart
class MockUserRepository extends Mock implements IUserRepository {}

void main() {
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    getIt.registerSingleton<IUserRepository>(mockRepository);
  });

  tearDown(() {
    getIt.reset();
  });

  blocTest<UserBloc, UserState>(
    'emits [loading, loaded] when load succeeds',
    setUp: () {
      when(() => mockRepository.getUser(any()))
          .thenAnswer((_) async => right(testUser));
    },
    build: UserBloc.new,
    act: (bloc) => bloc.add(const UserLoad(userId: 1)),
    expect: () => [
      const UserLoading(),
      UserLoaded(user: testUser),
    ],
  );
}
```

---

## 선택 가이드

```
상태 분리 명확? ─Yes→ Freezed Union (권장)
               └No→ 코드생성 회피? ─Yes→ Sealed Class
                                  └No→ Single State

UseCase 주입? ─테스트 중요→ DI 디커플링 (Optional Constructor Injection)
             └단순한 경우→ 직접 인스턴스화

Stream 연동? ─Yes→ emit.forEach + restartable() (권장)
            └특수한 경우→ 수동 StreamSubscription
```

---

## 체크리스트

- [ ] State 정의 (Freezed union / sealed class / single)
- [ ] Event 정의 (Freezed / sealed class)
- [ ] BLoC 구현 (UseCase 통합 패턴 선택)
- [ ] UseCase 호출 패턴 적용 (직접 인스턴스화 또는 DI 디커플링)
- [ ] `isClosed` 체크 (await 후 필수)
- [ ] Stream 연동 시 `emit.forEach` + `restartable()` 사용
- [ ] buildWhen/listenWhen 최적화
- [ ] 테스트 작성 (mock UseCase 주입 또는 GetIt 모킹)

---

## 참조하는 에이전트

- `/feature:bloc` - BLoC 상태 관리
- `/feature:presentation` - Presentation Layer 생성
- `/inspector:bloc` - BLoC 런타임 디버깅

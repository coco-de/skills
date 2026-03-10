# UseCase 패턴

> **참조 위치**: `.claude/references/patterns/usecase-patterns.md`

UseCase는 비즈니스 로직을 캡슐화하는 Clean Architecture의 핵심 컴포넌트입니다.

---

## 패턴 비교

| 패턴 | 장점 | 단점 | 권장 |
|------|------|------|------|
| **직접 인스턴스화** | DI 설정 단순화, BLoC 코드 간결 | 테스트 시 GetIt 모킹 필요 | 단순한 경우 |
| **DI 디커플링** | Mock 주입 간편, GetIt 의존 제거 | 생성자 파라미터 증가 | ✅ **테스트 중요 시 권장** |

---

## Future UseCase (단건 요청)

### UseCase 정의

```dart
// domain/usecase/get_user_usecase.dart
class GetUserUseCase {
  const GetUserUseCase({IUserRepository? repository})
      : _repository = repository;

  final IUserRepository? _repository;

  // 프로덕션: GetIt에서 가져옴, 테스트: 생성자 주입
  IUserRepository get _repo => _repository ?? getIt<IUserRepository>();

  Future<Either<Failure, User>> call(GetUserParams params) async {
    return _repo.getUser(params.id);
  }
}

class GetUserParams {
  const GetUserParams({required this.id});
  final int id;
}
```

### BLoC에서 사용 (DI 디커플링)

```dart
class UserBloc extends Bloc<UserEvent, UserState> {
  UserBloc({
    GetUserUseCase? getUserUseCase,
  }) : _getUserUseCase = getUserUseCase ?? const GetUserUseCase(),
       super(const UserInitial()) {
    on<UserLoad>(_onLoad);
  }

  final GetUserUseCase _getUserUseCase;

  Future<void> _onLoad(UserLoad event, Emitter<UserState> emit) async {
    emit(const UserLoading());

    final result = await _getUserUseCase(
      GetUserParams(id: event.userId),
    );

    if (isClosed) return; // await 후 체크 필수!

    result.fold(
      (failure) => emit(UserError(failure: failure)),
      (user) => emit(UserLoaded(user: user)),
    );
  }
}
```

### 테스트

```dart
class MockGetUserUseCase extends Mock implements GetUserUseCase {}

blocTest<UserBloc, UserState>(
  'emits [loading, loaded] when load succeeds',
  setUp: () {
    when(() => mockGetUser(any()))
        .thenAnswer((_) async => right(testUser));
  },
  build: () => UserBloc(getUserUseCase: mockGetUser),
  act: (bloc) => bloc.add(const UserLoad(userId: 1)),
  expect: () => [
    const UserLoading(),
    UserLoaded(user: testUser),
  ],
);
```

---

## Stream UseCase (SWR/Cache-First)

캐시 데이터와 서버 데이터를 순차적으로 방출하는 Stream 기반 UseCase입니다.

### StreamUseCase 인터페이스

```dart
/// Stream 기반 UseCase (SWR 패턴용)
abstract class StreamUseCase<T, Params, Repo> {
  Repo get repo;
  Stream<Either<Failure, T>> call(Params param);
}
```

### StreamUseCase 구현

```dart
class GetItemsStreamUseCase
    implements StreamUseCase<List<Item>, GetItemsParams, IItemRepository> {
  const GetItemsStreamUseCase({IItemRepository? repository})
      : _repository = repository;

  final IItemRepository? _repository;

  @override
  IItemRepository get repo => _repository ?? getIt<IItemRepository>();

  @override
  Stream<Either<Failure, List<Item>>> call(GetItemsParams params) {
    return repo.getItemsWithCache(categoryId: params.categoryId);
  }
}
```

### BLoC에서 사용: emit.forEach + restartable()

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';

class ItemBloc extends Bloc<ItemEvent, ItemState> {
  ItemBloc({
    GetItemsStreamUseCase? getItemsStream,
  }) : _getItemsStream = getItemsStream ?? const GetItemsStreamUseCase(),
       super(const ItemState()) {
    on<_Load>(
      _onLoad,
      transformer: restartable(),  // 파라미터 변경 시 이전 스트림 자동 취소
    );
  }

  final GetItemsStreamUseCase _getItemsStream;

  Future<void> _onLoad(_Load event, Emitter<ItemState> emit) async {
    if (state.items.isEmpty) {
      emit(state.copyWith(status: LoadingStatus.loading));
    }

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
}
```

#### restartable() 동작 원리

```
1. add(_Load(categoryId: 1))  → 스트림A 구독 (캐시 → 서버 순차 yield)
2. add(_Load(categoryId: 2))  → restartable()가 핸들러1 취소 → 스트림A 해제
                               → 핸들러2 시작 → 스트림B 구독
```

`emit.forEach`는 내부적으로 `stream.listen()`을 호출하며, `restartable()`가 핸들러를 취소하면 구독도 자동 정리됩니다. `close()` 오버라이드가 불필요합니다.

### Repository SWR Stream 구현

```dart
@override
Stream<Either<Failure, List<Item>>> getItemsWithCache({
  required int categoryId,
}) async* {
  // 1. 캐시 데이터 즉시 yield
  final cached = await _itemDao.getByCategoryId(categoryId);
  if (cached != null && cached.isNotEmpty) {
    yield right(cached.map((e) => e.toDomain()).toList());
  }

  // 2. 서버 데이터 fetch → yield
  try {
    final remote = await _client.item.getItems(categoryId: categoryId);
    await _itemDao.upsertAll(remote.map((e) => e.toLocal()).toList());
    yield right(remote);
  } on Exception catch (error, stackTrace) {
    if (cached == null || cached.isEmpty) {
      yield left(ItemFailure(message: error.toString()));
    }
    // 캐시가 있었으면 에러 무시 (이미 캐시 데이터 표시됨)
    Log.e('서버 갱신 실패', error: error, stackTrace: stackTrace);
  }
}
```

### Stream 테스트

```dart
class MockGetItemsStreamUseCase extends Mock implements GetItemsStreamUseCase {}

blocTest<ItemBloc, ItemState>(
  'emits cached then fresh data via SWR stream',
  setUp: () {
    when(() => mockGetItemsStream(any())).thenAnswer(
      (_) => Stream.fromIterable([
        right(cachedItems),
        right(freshItems),
      ]),
    );
  },
  build: () => ItemBloc(getItemsStream: mockGetItemsStream),
  act: (bloc) => bloc.add(const ItemEvent.load(categoryId: 1)),
  expect: () => [
    ItemState(status: LoadingStatus.loading),
    ItemState(status: LoadingStatus.loaded, items: cachedItems),
    ItemState(status: LoadingStatus.loaded, items: freshItems),
  ],
);
```

---

## UseCase Bundle (8개 이상)

생성자 파라미터가 많아지면 Bundle 클래스로 그룹화합니다.

```dart
class DashboardUseCases {
  const DashboardUseCases({
    GetStatsUseCase? getStats,
    GetChartDataUseCase? getChartData,
    GetRecentItemsUseCase? getRecentItems,
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

---

## 선택 가이드

```
데이터 흐름?
├── 단건 요청 → Future UseCase
└── 캐시+서버 순차 → Stream UseCase + emit.forEach + restartable()

UseCase 주입?
├── 테스트 중요 → DI 디커플링 (Optional Constructor Injection)
└── 단순한 경우 → 직접 인스턴스화

UseCase 개수?
├── 1~7개 → 개별 생성자 파라미터
└── 8개+ → UseCase Bundle 패턴
```

---

## 참조하는 에이전트

- `/feature:domain` - Domain Layer 생성
- `/feature:bloc` - BLoC 상태 관리
- `/feature:presentation` - Presentation Layer 생성

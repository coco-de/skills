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

## BLoC 구현

> ⚠️ **중요**: BLoC에 `@injectable` 사용 금지! Provider를 통해 의존성 주입 및 접근 관리

```dart
// {feature}_bloc.dart
import 'package:flutter_bloc/flutter_bloc.dart';

// ❌ 금지: @injectable 사용
// ❌ 금지: 생성자를 통한 UseCase 주입

class UserBloc extends Bloc<UserEvent, UserState> {
  UserBloc() : super(const UserInitial()) {
    on<UserLoad>(_onLoad);
    on<UserRefresh>(_onRefresh);
  }

  Future<void> _onLoad(UserLoad event, Emitter<UserState> emit) async {
    emit(const UserLoading());

    // ✅ UseCase 직접 인스턴스화하여 호출
    final result = await GetUserUseCase().call(
      GetUserParams(id: event.userId),
    );

    if (isClosed) return; // await 후 체크 필수!

    result.fold(
      (failure) => emit(UserError(failure: failure)),
      (user) => emit(UserLoaded(user: user)),
    );
  }

  Future<void> _onRefresh(UserRefresh event, Emitter<UserState> emit) async {
    final currentState = state;
    if (currentState is! UserLoaded) return;

    // ✅ UseCase 직접 인스턴스화하여 호출
    final result = await GetUserUseCase().call(
      GetUserParams(id: currentState.user.id),
    );

    if (isClosed) return;

    result.fold(
      (failure) => emit(UserError(failure: failure)),
      (user) => emit(UserLoaded(user: user)),
    );
  }
}
```

---

## Stream 연동 (SWR/Cache-First)

```dart
class HomeBloc extends Bloc<HomeEvent, HomeState> {
  HomeBloc() : super(const HomeState()) {
    on<HomeLoad>(_onLoad);
  }

  StreamSubscription<SWRResult<List<Item>>>? _subscription;

  Future<void> _onLoad(HomeLoad event, Emitter<HomeState> emit) async {
    emit(state.copyWith(status: LoadingStatus.loading));

    await _subscription?.cancel();
    // ✅ UseCase 직접 인스턴스화하여 호출
    _subscription = GetItemsStreamUseCase().call(NoParams()).listen(
      (result) => add(HomeItemsUpdated(result)),
      onError: (error) => add(HomeError(error)),
    );
  }

  @override
  Future<void> close() {
    _subscription?.cancel();
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
      // ✅ BLoC 직접 생성 (getIt 사용 금지)
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
// ❌ @injectable 사용 금지
class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() => emit(state + 1);
  void decrement() => emit(state - 1);
  void reset() => emit(0);
}
```

---

## 선택 가이드

```
상태 분리 명확? ─Yes→ Freezed Union (권장)
               └No→ 코드생성 회피? ─Yes→ Sealed Class
                                  └No→ Single State
```

---

## 체크리스트

- [ ] State 정의 (Freezed union / sealed class / single)
- [ ] Event 정의 (Freezed / sealed class)
- [ ] BLoC 구현 (`@injectable` 사용 금지!)
- [ ] UseCase 직접 인스턴스화 (`UseCase().call()` 패턴)
- [ ] `isClosed` 체크 (await 후 필수)
- [ ] BlocProvider로 BLoC 직접 생성 (getIt 사용 금지)
- [ ] buildWhen/listenWhen 최적화
- [ ] 메모리 관리 (close 시 StreamSubscription 정리)
- [ ] 테스트 작성

---

## 참조하는 에이전트

- `/feature:bloc` - BLoC 상태 관리
- `/feature:presentation` - Presentation Layer 생성
- `/inspector:bloc` - BLoC 런타임 디버깅

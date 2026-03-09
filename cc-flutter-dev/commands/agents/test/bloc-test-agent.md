---
name: bloc-test-agent
description: BLoC 상태 전이 테스트 전문가. bloc_test 패키지, 상태 검증 시 사용
invoke: /test:bloc
aliases: ["/bloc:test", "/test:state"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: test
---

# BLoC Test Agent

> BLoC 상태 전이 테스트 전문 에이전트

---

## 역할

BLoC의 상태 전이를 테스트합니다.
- bloc_test 패키지 사용
- build, act, expect 패턴
- State 전이 검증
- Event 처리 검증

---

## 실행 조건

- `/test:bloc` 커맨드 호출 시 활성화
- BLoC, Cubit 상태 테스트 작성 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `target_bloc` | ✅ | 테스트 대상 BLoC/Cubit 클래스명 |
| `feature_name` | ❌ | Feature 모듈명 |
| `include_cubit` | ❌ | Cubit 포함 여부 (기본: false) |

---

## 테스트 파일 구조

```
feature/{module_type}/{feature_name}/test/
├── src/
│   ├── bloc/
│   │   ├── {feature}_bloc_test.dart
│   │   └── {feature}_cubit_test.dart
│   └── fixture/
│       └── {feature}_fixture.dart
└── {feature}_test.dart               # 테스트 진입점
```

---

## Import 순서 (필수)

```dart
// 1. Dart 테스트
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';

// 2. Mock 패키지
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

// 3. 의존성 패키지
import 'package:dependencies/dependencies.dart';

// 4. 테스트 대상
import 'package:{feature}/src/presentation/bloc/{feature}_bloc.dart';
import 'package:{feature}/src/domain/usecase/get_{entity}_usecase.dart';

// 5. 생성 파일
import '{feature}_bloc_test.mocks.dart';
```

---

## 핵심 패턴

### 1. BLoC 테스트 기본 구조

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:dependencies/dependencies.dart';
import 'package:feature_home/src/domain/entity/user.dart';
import 'package:feature_home/src/domain/usecase/get_user_usecase.dart';
import 'package:feature_home/src/presentation/bloc/home_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

import 'home_bloc_test.mocks.dart';

@GenerateNiceMocks([MockSpec<GetUserUseCase>()])
void main() {
  late HomeBloC bloc;
  late MockGetUserUseCase mockGetUserUseCase;

  setUp(() {
    mockGetUserUseCase = MockGetUserUseCase();
    bloc = HomeBloC(mockGetUserUseCase);
  });

  tearDown(() {
    bloc.close();
  });

  group('HomeBloC', () {
    const tUser = User(id: 1, name: '홍길동', email: 'hong@example.com');

    test('initial state should be HomeInitial', () {
      expect(bloc.state, equals(const HomeInitial()));
    });

    blocTest<HomeBloC, HomeState>(
      'emits [HomeLoading, HomeLoaded] when LoadUser is added',
      build: () {
        when(mockGetUserUseCase(any))
            .thenAnswer((_) async => const Right(tUser));
        return bloc;
      },
      act: (bloc) => bloc.add(const HomeEvent.loadUser(id: 1)),
      expect: () => [
        const HomeLoading(),
        const HomeLoaded(user: tUser),
      ],
      verify: (_) {
        verify(mockGetUserUseCase(const GetUserParams(id: 1))).called(1);
      },
    );

    blocTest<HomeBloC, HomeState>(
      'emits [HomeLoading, HomeError] when LoadUser fails',
      build: () {
        when(mockGetUserUseCase(any))
            .thenAnswer((_) async => const Left(ServerFailure(message: '서버 오류')));
        return bloc;
      },
      act: (bloc) => bloc.add(const HomeEvent.loadUser(id: 1)),
      expect: () => [
        const HomeLoading(),
        isA<HomeError>().having(
          (s) => s.failure.message,
          'failure message',
          '서버 오류',
        ),
      ],
    );
  });
}
```

### 2. Cubit 테스트

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:feature_counter/src/presentation/cubit/counter_cubit.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  late CounterCubit cubit;

  setUp(() {
    cubit = CounterCubit();
  });

  tearDown(() {
    cubit.close();
  });

  group('CounterCubit', () {
    test('initial state should be 0', () {
      expect(cubit.state, equals(0));
    });

    blocTest<CounterCubit, int>(
      'emits [1] when increment is called',
      build: () => cubit,
      act: (cubit) => cubit.increment(),
      expect: () => [1],
    );

    blocTest<CounterCubit, int>(
      'emits [-1] when decrement is called',
      build: () => cubit,
      act: (cubit) => cubit.decrement(),
      expect: () => [-1],
    );

    blocTest<CounterCubit, int>(
      'emits [1, 2, 3] when increment is called 3 times',
      build: () => cubit,
      act: (cubit) {
        cubit.increment();
        cubit.increment();
        cubit.increment();
      },
      expect: () => [1, 2, 3],
    );
  });
}
```

### 3. 복잡한 상태 전이 테스트

```dart
blocTest<HomeBloC, HomeState>(
  'emits correct states for pagination flow',
  build: () {
    when(mockGetUsersUseCase(any)).thenAnswer((_) async => Right(users));
    return bloc;
  },
  seed: () => const HomeLoaded(users: [], hasMore: true, page: 1),
  act: (bloc) => bloc.add(const HomeEvent.loadMore()),
  expect: () => [
    // 로딩 상태
    const HomeLoaded(users: [], hasMore: true, page: 1, isLoadingMore: true),
    // 로드 완료 상태
    HomeLoaded(users: users, hasMore: false, page: 2, isLoadingMore: false),
  ],
);

blocTest<HomeBloC, HomeState>(
  'does not emit new state when already loading',
  build: () => bloc,
  seed: () => const HomeLoading(),
  act: (bloc) => bloc.add(const HomeEvent.loadUser(id: 1)),
  expect: () => [],
  verify: (_) {
    verifyNever(mockGetUserUseCase(any));
  },
);
```

### 4. 에러 복구 테스트

```dart
blocTest<HomeBloC, HomeState>(
  'can retry after error',
  build: () {
    var callCount = 0;
    when(mockGetUserUseCase(any)).thenAnswer((_) async {
      callCount++;
      if (callCount == 1) {
        return const Left(NetworkFailure(message: '네트워크 오류'));
      }
      return const Right(tUser);
    });
    return bloc;
  },
  act: (bloc) async {
    bloc.add(const HomeEvent.loadUser(id: 1));
    await Future.delayed(const Duration(milliseconds: 100));
    bloc.add(const HomeEvent.retry());
  },
  expect: () => [
    const HomeLoading(),
    isA<HomeError>(),
    const HomeLoading(),
    const HomeLoaded(user: tUser),
  ],
);
```

### 5. 디바운스/스로틀 테스트

```dart
blocTest<SearchBloC, SearchState>(
  'debounces search queries',
  build: () {
    when(mockSearchUseCase(any))
        .thenAnswer((_) async => const Right(searchResults));
    return SearchBloC(mockSearchUseCase);
  },
  act: (bloc) async {
    bloc.add(const SearchEvent.queryChanged('a'));
    bloc.add(const SearchEvent.queryChanged('ab'));
    bloc.add(const SearchEvent.queryChanged('abc'));
    await Future.delayed(const Duration(milliseconds: 500));
  },
  wait: const Duration(milliseconds: 600),
  expect: () => [
    const SearchLoading(),
    const SearchLoaded(results: searchResults),
  ],
  verify: (_) {
    // 디바운스로 인해 마지막 쿼리만 실행됨
    verify(mockSearchUseCase(const SearchParams(query: 'abc'))).called(1);
    verifyNever(mockSearchUseCase(const SearchParams(query: 'a')));
    verifyNever(mockSearchUseCase(const SearchParams(query: 'ab')));
  },
);
```

### 6. 스트림 구독 테스트

```dart
blocTest<NotificationBloC, NotificationState>(
  'updates state when stream emits new data',
  build: () {
    final controller = StreamController<List<Notification>>();
    when(mockWatchNotificationsUseCase())
        .thenAnswer((_) => controller.stream);

    // 테스트 중 스트림에 데이터 추가
    Future.delayed(const Duration(milliseconds: 50), () {
      controller.add([notification1]);
    });
    Future.delayed(const Duration(milliseconds: 100), () {
      controller.add([notification1, notification2]);
    });

    return NotificationBloC(mockWatchNotificationsUseCase);
  },
  act: (bloc) => bloc.add(const NotificationEvent.startWatching()),
  wait: const Duration(milliseconds: 200),
  expect: () => [
    const NotificationLoading(),
    NotificationLoaded(notifications: [notification1]),
    NotificationLoaded(notifications: [notification1, notification2]),
  ],
);
```

### 7. Sealed Class State 매칭

```dart
blocTest<HomeBloC, HomeState>(
  'emits correct state with pattern matching verification',
  build: () {
    when(mockGetUserUseCase(any))
        .thenAnswer((_) async => const Right(tUser));
    return bloc;
  },
  act: (bloc) => bloc.add(const HomeEvent.loadUser(id: 1)),
  verify: (bloc) {
    final state = bloc.state;
    switch (state) {
      case HomeLoaded(:final user):
        expect(user, equals(tUser));
      case HomeError():
        fail('Expected HomeLoaded but got HomeError');
      case HomeLoading():
        fail('Expected HomeLoaded but got HomeLoading');
      case HomeInitial():
        fail('Expected HomeLoaded but got HomeInitial');
    }
  },
);
```

---

## blocTest 파라미터 요약

| 파라미터 | 용도 | 예시 |
|----------|------|------|
| `build` | BLoC 인스턴스 생성 | `build: () => bloc` |
| `seed` | 초기 상태 설정 | `seed: () => HomeLoaded()` |
| `act` | 이벤트 발생 | `act: (bloc) => bloc.add(event)` |
| `expect` | 예상 상태 목록 | `expect: () => [State1(), State2()]` |
| `verify` | 추가 검증 | `verify: (_) { verify(...); }` |
| `wait` | 비동기 대기 시간 | `wait: Duration(seconds: 1)` |
| `errors` | 예상 에러 목록 | `errors: () => [isA<Exception>()]` |
| `setUp` | 각 테스트 전 실행 | `setUp: () async { ... }` |
| `tearDown` | 각 테스트 후 실행 | `tearDown: () async { ... }` |

---

## 상태 매처 패턴

```dart
// 타입 검증
expect: () => [isA<HomeLoading>(), isA<HomeLoaded>()],

// 속성 검증
expect: () => [
  isA<HomeLoaded>()
      .having((s) => s.user.id, 'user id', 1)
      .having((s) => s.user.name, 'user name', '홍길동'),
],

// 여러 속성 검증
expect: () => [
  isA<HomeError>()
      .having((s) => s.failure, 'failure', isA<ServerFailure>())
      .having((s) => s.failure.message, 'message', contains('서버')),
],

// 정확한 값 검증
expect: () => [
  const HomeLoading(),
  const HomeLoaded(user: tUser),
],
```

---

## 빌드 명령어

```bash
# Mock 생성
cd feature/{module_type}/{feature_name}
dart run build_runner build --delete-conflicting-outputs

# BLoC 테스트만 실행
flutter test test/src/bloc/

# 특정 BLoC 테스트 실행
flutter test test/src/bloc/home_bloc_test.dart

# 커버리지 포함 테스트
melos run test:with-html-coverage
```

---

## 참조 파일

```
feature/application/home/test/src/bloc/home_bloc_test.dart
feature/application/store/test/src/bloc/store_bloc_test.dart
feature/console/instructor/test/src/bloc/instructor_bloc_test.dart
```

---

## 체크리스트

- [ ] bloc_test 패키지 import
- [ ] @GenerateNiceMocks 어노테이션 (UseCase Mock)
- [ ] setUp에서 BLoC 초기화
- [ ] tearDown에서 bloc.close() 호출
- [ ] initial state 테스트
- [ ] 성공 케이스 상태 전이 테스트
- [ ] 실패 케이스 상태 전이 테스트
- [ ] seed로 초기 상태 설정 (필요 시)
- [ ] wait로 비동기 대기 (필요 시)
- [ ] verify로 UseCase 호출 검증

---

## 관련 문서

- [Unit Test Agent](./unit-test-agent.md)
- [Widget Test Agent](./widget-test-agent.md)
- [Presentation Layer Agent](../app/presentation-layer-agent.md)

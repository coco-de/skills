---
name: unit-test-agent
description: UseCase, Repository 단위 테스트 전문가. Mockito 패턴, Either 결과 검증 시 사용
invoke: /test:unit
aliases: ["/unit:create", "/test:usecase"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
skills: test
---

# Unit Test Agent

> UseCase, Repository 단위 테스트 전문 에이전트

---

## 역할

UseCase와 Repository의 단위 테스트를 생성합니다.
- @GenerateNiceMocks 어노테이션 사용
- Mockito 패턴 (when, verify, verifyNoMoreInteractions)
- Either 결과 검증
- setUp/tearDown 패턴

---

## 실행 조건

- `/test:unit` 커맨드 호출 시 활성화
- UseCase, Repository 테스트 작성 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `target_class` | ✅ | 테스트 대상 클래스명 |
| `target_type` | ❌ | `usecase`, `repository` (기본: `usecase`) |
| `feature_name` | ❌ | Feature 모듈명 |

---

## 테스트 파일 구조

```
feature/{module_type}/{feature_name}/test/
├── src/
│   ├── unit/
│   │   ├── usecase/
│   │   │   ├── get_{entity}_usecase_test.dart
│   │   │   └── create_{entity}_usecase_test.dart
│   │   └── repository/
│   │       └── {feature}_repository_test.dart
│   └── fixture/
│       └── {feature}_fixture.dart
└── {feature}_test.dart               # 테스트 진입점
```

---

## Import 순서 (필수)

```dart
// 1. Dart 테스트
import 'package:flutter_test/flutter_test.dart';

// 2. Mock 패키지
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

// 3. 의존성 패키지
import 'package:dependencies/dependencies.dart';

// 4. 테스트 대상
import 'package:{feature}/src/domain/usecase/get_{entity}_usecase.dart';
import 'package:{feature}/src/domain/repository/i_{feature}_repository.dart';

// 5. 생성 파일
import 'get_{entity}_usecase_test.mocks.dart';
```

---

## 핵심 패턴

### 1. UseCase 테스트

```dart
import 'package:dependencies/dependencies.dart';
import 'package:feature_home/src/domain/entity/user.dart';
import 'package:feature_home/src/domain/repository/i_home_repository.dart';
import 'package:feature_home/src/domain/usecase/get_user_usecase.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

import 'get_user_usecase_test.mocks.dart';

@GenerateNiceMocks([MockSpec<IHomeRepository>()])
void main() {
  late GetUserUseCase useCase;
  late MockIHomeRepository mockRepository;

  setUp(() {
    mockRepository = MockIHomeRepository();
    useCase = GetUserUseCase(mockRepository);
  });

  tearDown(() {
    reset(mockRepository);
  });

  group('GetUserUseCase', () {
    const tUserId = 1;
    const tUser = User(id: tUserId, name: '홍길동', email: 'hong@example.com');
    final tParams = GetUserParams(id: tUserId);

    test('should return User when repository call is successful', () async {
      // Arrange
      when(mockRepository.getUser(tUserId))
          .thenAnswer((_) async => const Right(tUser));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, const Right<Failure, User>(tUser));
      verify(mockRepository.getUser(tUserId)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return Failure when repository call fails', () async {
      // Arrange
      const tFailure = ServerFailure(message: '서버 오류');
      when(mockRepository.getUser(tUserId))
          .thenAnswer((_) async => const Left(tFailure));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, const Left<Failure, User>(tFailure));
      verify(mockRepository.getUser(tUserId)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should throw when params is invalid', () async {
      // Arrange
      final invalidParams = GetUserParams(id: -1);

      // Act & Assert
      expect(
        () => useCase(invalidParams),
        throwsA(isA<InvalidParamsException>()),
      );
      verifyZeroInteractions(mockRepository);
    });
  });
}
```

### 2. Repository 테스트

```dart
import 'package:dependencies/dependencies.dart';
import 'package:feature_home/src/data/repository/home_repository.dart';
import 'package:feature_home/src/domain/entity/user.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

import 'home_repository_test.mocks.dart';

@GenerateNiceMocks([
  MockSpec<HomeApiClient>(),
  MockSpec<HomeLocalDataSource>(),
])
void main() {
  late HomeRepository repository;
  late MockHomeApiClient mockApiClient;
  late MockHomeLocalDataSource mockLocalDataSource;

  setUp(() {
    mockApiClient = MockHomeApiClient();
    mockLocalDataSource = MockHomeLocalDataSource();
    repository = HomeRepository(
      apiClient: mockApiClient,
      localDataSource: mockLocalDataSource,
    );
  });

  tearDown(() {
    reset(mockApiClient);
    reset(mockLocalDataSource);
  });

  group('HomeRepository.getUser', () {
    const tUserId = 1;
    const tUserDto = UserDto(id: tUserId, name: '홍길동', email: 'hong@example.com');
    const tUser = User(id: tUserId, name: '홍길동', email: 'hong@example.com');

    test('should return User when API call is successful', () async {
      // Arrange
      when(mockApiClient.getUser(tUserId))
          .thenAnswer((_) async => tUserDto);

      // Act
      final result = await repository.getUser(tUserId);

      // Assert
      expect(result, const Right<Failure, User>(tUser));
      verify(mockApiClient.getUser(tUserId)).called(1);
    });

    test('should cache data locally when API call is successful', () async {
      // Arrange
      when(mockApiClient.getUser(tUserId))
          .thenAnswer((_) async => tUserDto);
      when(mockLocalDataSource.cacheUser(any))
          .thenAnswer((_) async {});

      // Act
      await repository.getUser(tUserId);

      // Assert
      verify(mockLocalDataSource.cacheUser(tUserDto)).called(1);
    });

    test('should return cached data when API call fails', () async {
      // Arrange
      when(mockApiClient.getUser(tUserId))
          .thenThrow(Exception('Network error'));
      when(mockLocalDataSource.getCachedUser(tUserId))
          .thenAnswer((_) async => tUserDto);

      // Act
      final result = await repository.getUser(tUserId);

      // Assert
      expect(result, const Right<Failure, User>(tUser));
      verify(mockLocalDataSource.getCachedUser(tUserId)).called(1);
    });

    test('should return Failure when both API and cache fail', () async {
      // Arrange
      when(mockApiClient.getUser(tUserId))
          .thenThrow(Exception('Network error'));
      when(mockLocalDataSource.getCachedUser(tUserId))
          .thenAnswer((_) async => null);

      // Act
      final result = await repository.getUser(tUserId);

      // Assert
      expect(result.isLeft(), true);
      result.fold(
        (failure) => expect(failure, isA<CacheFailure>()),
        (_) => fail('Should return Left'),
      );
    });
  });
}
```

### 3. Fixture 패턴

```dart
/// Home Feature 테스트 Fixture
abstract final class HomeFixture {
  /// 테스트용 User 객체
  static const User user = User(
    id: 1,
    name: '홍길동',
    email: 'hong@example.com',
    createdAt: DateTime(2024, 1, 1),
  );

  /// 테스트용 User 목록
  static const List<User> users = [
    User(id: 1, name: '홍길동', email: 'hong@example.com'),
    User(id: 2, name: '김철수', email: 'kim@example.com'),
    User(id: 3, name: '이영희', email: 'lee@example.com'),
  ];

  /// 테스트용 UserDto
  static const UserDto userDto = UserDto(
    id: 1,
    name: '홍길동',
    email: 'hong@example.com',
  );

  /// 테스트용 Failure
  static const ServerFailure serverFailure = ServerFailure(
    message: '서버 오류가 발생했습니다',
    statusCode: 500,
  );

  /// 테스트용 NetworkFailure
  static const NetworkFailure networkFailure = NetworkFailure(
    message: '네트워크 연결을 확인해주세요',
  );
}
```

### 4. Either 결과 검증 헬퍼

```dart
import 'package:dependencies/dependencies.dart';
import 'package:flutter_test/flutter_test.dart';

/// Either 결과 검증 확장
extension EitherTestExtension<L, R> on Either<L, R> {
  /// Left 값 추출 (테스트용)
  L getLeft() {
    return fold((l) => l, (_) => throw Exception('Expected Left but got Right'));
  }

  /// Right 값 추출 (테스트용)
  R getRight() {
    return fold((_) => throw Exception('Expected Right but got Left'), (r) => r);
  }
}

/// Either 매처
Matcher isRightWith<R>(R expected) {
  return predicate<Either<dynamic, R>>(
    (either) => either.fold((_) => false, (r) => r == expected),
    'is Right with $expected',
  );
}

Matcher isLeftWith<L>(L expected) {
  return predicate<Either<L, dynamic>>(
    (either) => either.fold((l) => l == expected, (_) => false),
    'is Left with $expected',
  );
}

Matcher isLeftOfType<L>() {
  return predicate<Either<L, dynamic>>(
    (either) => either.fold((l) => l is L, (_) => false),
    'is Left of type $L',
  );
}
```

### 5. 비동기 테스트 패턴

```dart
group('async operations', () {
  test('should handle async operation correctly', () async {
    // Arrange
    when(mockRepository.fetchData())
        .thenAnswer((_) async {
          await Future.delayed(const Duration(milliseconds: 100));
          return const Right(data);
        });

    // Act
    final future = useCase();

    // Assert
    await expectLater(future, completes);
    final result = await future;
    expect(result.isRight(), true);
  });

  test('should timeout when operation takes too long', () async {
    // Arrange
    when(mockRepository.fetchData())
        .thenAnswer((_) async {
          await Future.delayed(const Duration(seconds: 10));
          return const Right(data);
        });

    // Act & Assert
    await expectLater(
      useCase().timeout(const Duration(seconds: 1)),
      throwsA(isA<TimeoutException>()),
    );
  });
});
```

---

## Mockito 패턴 요약

| 메서드 | 용도 | 예시 |
|--------|------|------|
| `when(...).thenReturn()` | 동기 반환값 설정 | `when(mock.getValue()).thenReturn(42)` |
| `when(...).thenAnswer()` | 비동기 반환값 설정 | `when(mock.getData()).thenAnswer((_) async => data)` |
| `when(...).thenThrow()` | 예외 발생 설정 | `when(mock.call()).thenThrow(Exception())` |
| `verify(...).called(n)` | 호출 횟수 검증 | `verify(mock.call()).called(1)` |
| `verifyNever(...)` | 미호출 검증 | `verifyNever(mock.call())` |
| `verifyNoMoreInteractions(...)` | 추가 호출 없음 검증 | `verifyNoMoreInteractions(mock)` |
| `verifyZeroInteractions(...)` | 호출 전무 검증 | `verifyZeroInteractions(mock)` |
| `reset(...)` | Mock 상태 초기화 | `reset(mock)` |
| `any` | 모든 값 매칭 | `when(mock.call(any)).thenReturn(true)` |
| `argThat(...)` | 조건부 매칭 | `argThat(isA<String>())` |
| `captureAny` | 인수 캡처 | `verify(mock.call(captureAny))` |

---

## 빌드 명령어

```bash
# Mock 생성
cd feature/{module_type}/{feature_name}
dart run build_runner build --delete-conflicting-outputs

# 테스트 실행
melos run test:select

# 커버리지 포함 테스트
melos run test:with-html-coverage
```

---

## 참조 파일

```
feature/application/store/test/src/unit/usecase/
feature/application/store/test/src/unit/repository/
feature/common/auth/test/src/unit/
```

---

## 체크리스트

- [ ] @GenerateNiceMocks 어노테이션 추가
- [ ] Mock 클래스 생성 (.mocks.dart)
- [ ] setUp/tearDown 패턴 적용
- [ ] group으로 테스트 그룹화
- [ ] Arrange-Act-Assert 패턴 적용
- [ ] 성공/실패 케이스 모두 테스트
- [ ] verify로 호출 검증
- [ ] Either 결과 검증
- [ ] Fixture 활용

---

## 관련 문서

- [BLoC Test Agent](./bloc-test-agent.md)
- [Widget Test Agent](./widget-test-agent.md)
- [Domain Layer Agent](../app/domain-layer-agent.md)

# Serverpod 테스팅 & TDD

withServerpod 기반 통합 테스트와 TDD Red-Green-Refactor 패턴을 다룹니다.

## 트리거

- 서버 테스트 작성
- withServerpod 사용
- TDD 워크플로우
- 인증/권한 테스트

## 기본 테스트

```dart
import 'package:test/test.dart';
import 'test_tools/serverpod_test_tools.dart';

void main() {
  withServerpod('Given Greeting endpoint', (sessionBuilder, endpoints) {
    test('when calling hello then returns greeting', () async {
      final greeting = await endpoints.greeting.hello(sessionBuilder, 'Bob');
      expect(greeting.message, 'Hello Bob');
    });
  });
}
```

**중요**: 생성된 `test_tools/serverpod_test_tools.dart`를 import. `serverpod_test`를 직접 import하지 않음.

## Session Builder

`copyWith`로 수정된 세션 생성, `build()`로 Session 획득:

```dart
var customSession = sessionBuilder.copyWith(...);
var session = sessionBuilder.build(); // DB 작업용
```

## 인증 테스트

```dart
withServerpod('Given AuthEndpoint', (sessionBuilder, endpoints) {
  final userId = '550e8400-e29b-41d4-a716-446655440000';

  group('when authenticated', () {
    var authed = sessionBuilder.copyWith(
      authentication: AuthenticationOverride.authenticationInfo(
        userId, {Scope('user')}),
    );

    test('then hello succeeds', () async {
      final greeting = await endpoints.authExample.hello(authed, 'Michael');
      expect(greeting, 'Hello, Michael!');
    });
  });

  group('when unauthenticated', () {
    var unauthed = sessionBuilder.copyWith(
      authentication: AuthenticationOverride.unauthenticated(),
    );

    test('then hello throws', () async {
      await expectLater(
        endpoints.authExample.hello(unauthed, 'Michael'),
        throwsA(isA<ServerpodUnauthenticatedException>()),
      );
    });
  });
});
```

## DB 시딩

```dart
withServerpod('Given Products endpoint', (sessionBuilder, endpoints) {
  var session = sessionBuilder.build();

  setUp(() async {
    await Product.db.insert(session, [
      Product(name: 'Apple', price: 10),
      Product(name: 'Banana', price: 10),
    ]);
  });

  test('then all returns both products', () async {
    final products = await endpoints.products.all(sessionBuilder);
    expect(products, hasLength(2));
  });
});
```

tearDown 불필요 — 기본적으로 각 테스트가 롤백되는 트랜잭션에서 실행.

## 롤백 동작

| 모드 | 설명 | 사용 케이스 |
|------|------|-----------|
| `afterEach` | 각 테스트 후 롤백 (기본) | 대부분의 테스트 |
| `afterAll` | 그룹 전체 후 롤백 | 시나리오 테스트, 연속 의존 |
| `disabled` | 자동 롤백 없음 | 동시 트랜잭션 테스트 |

```dart
withServerpod(
  'Given concurrent transactions',
  (sessionBuilder, endpoints) {
    tearDownAll(() async {
      var session = sessionBuilder.build();
      await Product.db.deleteWhere(session, where: (_) => Constant.bool(true));
    });

    test('then should commit all', () async {
      await endpoints.products.concurrentTransactionCalls(sessionBuilder);
    });
  },
  rollbackDatabase: RollbackDatabase.disabled,
);
```

## 스트림 테스트

```dart
withServerpod('Given shared stream', (sessionBuilder, endpoints) {
  final user1 = sessionBuilder.copyWith(
    authentication: AuthenticationOverride.authenticationInfo('user-1', {}));
  final user2 = sessionBuilder.copyWith(
    authentication: AuthenticationOverride.authenticationInfo('user-2', {}));

  test('when posting numbers then listener receives them', () async {
    var stream = endpoints.comm.listenForNumbers(user1);
    await flushEventQueue(); // 스트림 등록 대기

    await endpoints.comm.postNumber(user2, 111);
    await endpoints.comm.postNumber(user2, 222);

    await expectLater(stream.take(2), emitsInOrder([111, 222]));
  });
});
```

## TDD Red-Green-Refactor

### 1. Red (실패하는 테스트 먼저)

```dart
test('when creating user with duplicate email then throws', () async {
  await endpoints.user.create(sessionBuilder,
    User(name: 'A', email: 'dup@test.com'));

  await expectLater(
    endpoints.user.create(sessionBuilder,
      User(name: 'B', email: 'dup@test.com')),
    throwsA(isA<DuplicateEmailException>()),
  );
});
```

### 2. Green (최소한의 구현)

```dart
Future<User> create(Session session, User user) async {
  final existing = await User.db.findFirstRow(session,
    where: (t) => t.email.equals(user.email));
  if (existing != null) throw DuplicateEmailException(user.email);
  return await User.db.insertRow(session, user);
}
```

### 3. Refactor (개선)

중복 제거, 헬퍼 추출, 성능 최적화 — 테스트가 계속 통과하는지 확인.

## withServerpod 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `applyMigrations` | `true` | 시작 시 마이그레이션 적용 |
| `enableSessionLogging` | `false` | 세션 로깅 활성화 |
| `rollbackDatabase` | `afterEach` | 롤백 시점 |
| `runMode` | `ServerpodRunMode.test` | 실행 모드 |
| `testGroupTagsOverride` | `['integration']` | 테스트 그룹 태그 |

## 테스트 실행

```bash
docker compose up -d          # DB & Redis 시작
dart test                     # 전체 테스트
dart test -t integration      # 통합 테스트만
dart test -x integration      # 유닛 테스트만
dart test -t integration --concurrency=1  # 순차 실행
```

## 테스트 예외

| 예외 | 설명 |
|------|------|
| `ServerpodUnauthenticatedException` | 인증 없이 호출 |
| `ServerpodInsufficientAccessException` | 권한 부족 |
| `ConnectionClosedException` | 스트림 연결 종료 |
| `InvalidConfigurationException` | 잘못된 설정 (중첩 트랜잭션 등) |

## DB 커넥션 관리

`withServerpod`마다 `sessionBuilder.build()` 호출 시 Serverpod 인스턴스 생성. 동시 테스트가 많으면 커넥션 한도 초과 가능:

```dart
withServerpod('Given example', (sessionBuilder, endpoints) {
  late Session session;
  setUpAll(() { session = sessionBuilder.build(); });
  // ...
});
```

## 프로젝트 구조

```
test/
├── unit/         # 순수 유닛 테스트
└── integration/  # withServerpod 통합 테스트
```

## 체크리스트

- [ ] 엔드포인트는 `endpoints` 파라미터로 호출 (직접 인스턴스화 금지)
- [ ] 인증 테스트: 인증됨/미인증/권한부족 케이스
- [ ] DB 시딩: setUp에서 데이터 삽입
- [ ] 동시 트랜잭션 테스트: `rollbackDatabase: disabled`
- [ ] 스트림 테스트: `flushEventQueue()` 사용

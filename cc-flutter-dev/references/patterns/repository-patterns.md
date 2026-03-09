# Repository 패턴

> **참조 위치**: `.claude/references/patterns/repository-patterns.md`

Repository는 데이터 소스를 추상화하여 Domain Layer에서 데이터 접근을 담당합니다.

---

## 패턴 비교

| 패턴 | 장점 | 단점 | 권장 상황 |
|------|------|------|----------|
| **Mixin 패턴** | 네트워크 로직 분리, 재사용성 | 구조 복잡도 증가 | 여러 데이터소스, 복잡한 API |
| **직접 구현** | 단순하고 명확 | 로직 재사용 어려움 | 단순한 CRUD |

---

## Repository Interface (Domain Layer)

```dart
// domain/repository/i_user_repository.dart
import 'package:dependencies/dependencies.dart';

abstract interface class IUserRepository {
  Future<Either<Failure, User>> getUser(int id);
  Future<Either<Failure, List<User>>> getUsers();
  Future<Either<Failure, User>> createUser(CreateUserParams params);
  Future<Either<Failure, User>> updateUser(UpdateUserParams params);
  Future<Either<Failure, Unit>> deleteUser(int id);

  // SWR 패턴용 Stream
  Stream<SWRResult<User>> getUserAsStream(int id);
}
```

---

## 패턴 A: Mixin 패턴 ✅ 권장

### Repository 구현체

```dart
// data/repository/user_repository.dart
import 'package:dependencies/dependencies.dart';

@LazySingleton(as: IUserRepository)
class UserRepository
    with UserServerpodMixin  // 네트워크 로직 분리
    implements IUserRepository {

  UserRepository(this._serverpodService);

  final ServerpodService _serverpodService;

  @override
  ServerpodClient get client => _serverpodService.client;
}
```

### Serverpod Mixin (네트워크 로직)

```dart
// data/repository/mixins/user_serverpod_mixin.dart
import 'package:serverpod_service/serverpod_service.dart' as serverpod;

mixin UserServerpodMixin implements IUserRepository {
  serverpod.ServerpodClient get client;

  @override
  Future<Either<Failure, User>> getUser(int id) async {
    try {
      final dto = await client.users.getUser(id);
      if (dto == null) {
        return left(NotFoundFailure('User not found: $id'));
      }
      return right(dto.toEntity());
    } on serverpod.ServerpodClientException catch (e, st) {
      return left(ServerFailure(e.message, error: e, stackTrace: st));
    }
  }

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final dtos = await client.users.getUsers();
      return right(dtos.map((dto) => dto.toEntity()).toList());
    } on serverpod.ServerpodClientException catch (e, st) {
      return left(ServerFailure(e.message, error: e, stackTrace: st));
    }
  }

  @override
  Future<Either<Failure, User>> createUser(CreateUserParams params) async {
    try {
      final dto = await client.users.createUser(
        name: params.name,
        email: params.email,
      );
      return right(dto.toEntity());
    } on serverpod.ServerpodClientException catch (e, st) {
      return left(ServerFailure(e.message, error: e, stackTrace: st));
    }
  }
}
```

### 네임스페이스 사용 이유

- Domain Entity와 API DTO 간 이름 충돌 방지 (User, Category 등)
- `serverpod.` 네임스페이스로 명확히 구분하여 Clean Architecture 원칙 유지

---

## 패턴 B: 직접 구현 패턴

```dart
// data/repository/user_repository.dart
import 'package:dependencies/dependencies.dart';

@LazySingleton(as: IUserRepository)
class UserRepository implements IUserRepository {
  UserRepository(this._serverpodService);

  final ServerpodService _serverpodService;

  @override
  Future<Either<Failure, User>> getUser(int id) async {
    try {
      final response = await _serverpodService.client.users.getUser(id);
      if (response == null) {
        return left(NotFoundFailure('User not found: $id'));
      }
      return right(response.toEntity());
    } on Exception catch (e, st) {
      return left(ServerFailure(e.toString(), error: e, stackTrace: st));
    }
  }

  @override
  Future<Either<Failure, List<User>>> getUsers() async {
    try {
      final response = await _serverpodService.client.users.getUsers();
      return right(response.map((dto) => dto.toEntity()).toList());
    } on Exception catch (e, st) {
      return left(ServerFailure(e.toString(), error: e, stackTrace: st));
    }
  }
}
```

---

## 구조

```
data/repository/
├── user_repository.dart          # Repository 구현체
└── mixins/
    └── user_serverpod_mixin.dart # 네트워크 로직 (Mixin 패턴)
```

---

## DTO → Entity 변환

```dart
// data/mapper/user_mapper.dart (또는 extension)
extension UserDtoMapper on serverpod.User {
  User toEntity() {
    return User(
      id: id!,
      name: name,
      email: email,
      avatarUrl: avatarUrl,
      createdAt: createdAt,
    );
  }
}
```

---

## 선택 가이드

```
네트워크 로직 재사용 필요? ─Yes→ Mixin 패턴 (권장)
                         └No→ 여러 데이터소스 조합? ─Yes→ Mixin 패턴
                                                   └No→ Direct Implementation
```

---

## 체크리스트

- [ ] Repository Interface 정의 (Domain Layer)
- [ ] Repository 구현체 생성 (Data Layer)
- [ ] Serverpod Mixin 구현 (Mixin 패턴 선택 시)
- [ ] DTO → Entity 변환 로직 구현
- [ ] Either<Failure, Success> 반환
- [ ] 예외 처리 (try-catch)
- [ ] @LazySingleton 어노테이션

---

## 참조하는 에이전트

- `/feature:data` - Data Layer 생성
- `/feature:domain` - Repository Interface 정의
- `/serverpod:endpoint` - Serverpod Endpoint 연동

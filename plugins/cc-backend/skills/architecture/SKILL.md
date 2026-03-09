# 아키텍처 패턴

Serverpod 백엔드를 위한 Clean Architecture와 Domain-Driven Design 패턴을 다룹니다.

## 트리거

- 백엔드 아키텍처 설계
- 서비스 레이어 구조화
- 도메인 로직 분리
- 레포지토리 패턴 적용

## Serverpod 프로젝트 구조

```
server/lib/src/
├── endpoints/            # 엔드포인트 (Presentation Layer)
│   ├── user_endpoint.dart
│   └── user_console_endpoint.dart
├── services/             # 비즈니스 로직 (Domain Layer)
│   └── user_service.dart
├── repositories/         # 데이터 접근 (Data Layer)
│   └── user_repository.dart
├── models/               # .spy.yaml 모델 정의
│   ├── entities/
│   ├── dto/
│   └── enum/
└── util/                 # 유틸리티
```

## 레이어 책임

### Endpoint (Presentation)

요청 수신, 파라미터 검증, 서비스 호출, 응답 반환:

```dart
class UserEndpoint extends Endpoint {
  Future<User> getUser(Session session, int id) async {
    return await UserService.getById(session, id);
  }

  Future<User> createUser(Session session, UserCreateRequest request) async {
    return await UserService.create(session, request);
  }
}
```

### Service (Domain)

비즈니스 로직, 검증, 트랜잭션 조율:

```dart
class UserService {
  static Future<User> getById(Session session, int id) async {
    final user = await UserRepository.findById(session, id);
    if (user == null) {
      throw AppException(code: 'NOT_FOUND', message: 'User not found: $id');
    }
    return user;
  }

  static Future<User> create(Session session, UserCreateRequest request) async {
    // 비즈니스 규칙 검증
    final existing = await UserRepository.findByEmail(session, request.email);
    if (existing != null) {
      throw AppException(code: 'DUPLICATE', message: 'Email already exists');
    }

    final user = User(
      name: request.name,
      email: request.email,
      createdAt: DateTime.now(),
    );

    return await UserRepository.insert(session, user);
  }
}
```

### Repository (Data)

DB 접근 캡슐화, 쿼리 로직:

```dart
class UserRepository {
  static Future<User?> findById(Session session, int id) async {
    return await User.db.findById(session, id,
      include: User.include(profile: Profile.include()));
  }

  static Future<User?> findByEmail(Session session, String email) async {
    return await User.db.findFirstRow(session,
      where: (t) => t.email.equals(email));
  }

  static Future<User> insert(Session session, User user) async {
    return await User.db.insertRow(session, user);
  }

  static Future<List<User>> findActive(Session session, {
    int limit = 20,
    int offset = 0,
  }) async {
    return await User.db.find(session,
      where: (t) => t.isActive.equals(true),
      orderBy: (t) => t.createdAt,
      orderDescending: true,
      limit: limit,
      offset: offset,
    );
  }
}
```

## App vs Console 엔드포인트 분리

```dart
// App 엔드포인트 — 일반 사용자용
class UserEndpoint extends Endpoint {
  @override
  bool get requireLogin => true;

  Future<User> getMe(Session session) async {
    final userId = await session.auth.authenticatedUserId;
    return await UserService.getById(session, userId!);
  }
}

// Console 엔드포인트 — 관리자용
class UserConsoleEndpoint extends Endpoint {
  @override
  bool get requireLogin => true;

  Future<List<User>> getAllUsers(Session session) async {
    await _requireAdmin(session);
    return await UserRepository.findAll(session);
  }

  Future<void> _requireAdmin(Session session) async {
    final userId = await session.auth.authenticatedUserId;
    final user = await UserRepository.findById(session, userId!);
    if (user?.role != UserRole.admin) {
      throw AppException(code: 'FORBIDDEN', message: 'Admin access required');
    }
  }
}
```

## 트랜잭션 관리

서비스 레이어에서 트랜잭션 조율:

```dart
class OrderService {
  static Future<Order> placeOrder(
    Session session,
    OrderCreateRequest request,
  ) async {
    return await session.transaction((tx) async {
      // 1. 재고 확인 & 차감
      final product = await ProductRepository.findByIdForUpdate(tx, request.productId);
      if (product.stock < request.quantity) {
        throw AppException(code: 'INSUFFICIENT_STOCK', message: 'Stock insufficient');
      }
      await ProductRepository.decreaseStock(tx, product.id!, request.quantity);

      // 2. 주문 생성
      final order = Order(
        userId: request.userId,
        productId: request.productId,
        quantity: request.quantity,
        totalPrice: product.price * request.quantity,
        status: OrderStatus.pending,
        createdAt: DateTime.now(),
      );
      return await OrderRepository.insert(tx, order);
    });
  }
}
```

## 도메인 이벤트 패턴

```dart
class UserService {
  static Future<User> create(Session session, UserCreateRequest request) async {
    final user = await session.transaction((tx) async {
      final created = await UserRepository.insert(tx, User(
        name: request.name,
        email: request.email,
        createdAt: DateTime.now(),
      ));

      // 도메인 이벤트 기록
      await EventRepository.insert(tx, DomainEvent(
        type: 'user.created',
        entityId: created.id!,
        payload: {'email': request.email},
        createdAt: DateTime.now(),
      ));

      return created;
    });

    // 트랜잭션 외부에서 비동기 작업
    await NotificationService.sendWelcomeEmail(session, user.email);

    return user;
  }
}
```

## 모듈 경계

기능별 모듈 분리:

```
server/lib/src/
├── feature/
│   ├── user/
│   │   ├── model/entities/user.spy.yaml
│   │   ├── user_endpoint.dart
│   │   ├── user_service.dart
│   │   └── user_repository.dart
│   ├── order/
│   │   ├── model/entities/order.spy.yaml
│   │   ├── order_endpoint.dart
│   │   ├── order_service.dart
│   │   └── order_repository.dart
│   └── product/
│       └── ...
```

## 의존성 방향

```
Endpoint → Service → Repository → DB (Serverpod ORM)
    ↓         ↓
  DTO      Entity
```

- Endpoint는 Service만 호출 (Repository 직접 호출 금지)
- Service는 다른 Service 호출 가능
- Repository는 다른 Repository 호출 금지 (Service에서 조율)

## 체크리스트

- [ ] 3-Layer 구조 준수 (Endpoint → Service → Repository)
- [ ] 비즈니스 로직은 Service에만 위치
- [ ] Endpoint에 DB 쿼리 직접 작성 금지
- [ ] 트랜잭션은 Service 레이어에서 관리
- [ ] App/Console 엔드포인트 분리
- [ ] 기능별 모듈 디렉토리 구조

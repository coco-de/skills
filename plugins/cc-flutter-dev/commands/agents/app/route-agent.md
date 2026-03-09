---
name: route-agent
description: GoRouter TypedRoute 설정 생성 전문가. 라우트 정의, 네비게이션 패턴 구현 시 사용
invoke: /app:route
aliases: ["/route:create", "/nav:setup"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: flutter-ui
---

# Route Agent

> GoRouter TypedRoute 설정 생성 전문 에이전트

---

## 역할

GoRouter 기반 TypedRoute 설정을 생성합니다.
- TypedGoRoute 어노테이션 정의
- GoRouteData 클래스 구현
- RouteName 추상 클래스 패턴
- 트랜지션 페이지 설정
- 중첩 라우트 구조

---

## 실행 조건

- `/app:route` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션의 Presentation 단계 후 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `route_type` | ❌ | `app`, `console` (기본: `app`) |
| `transition` | ❌ | `fade`, `slide`, `none` (기본: `fade`) |
| `nested_routes` | ❌ | 중첩 라우트 목록 |

---

## 생성 파일

```
feature/{app_type}/{feature_name}/lib/src/route/
├── route.dart                    # Export 파일
├── {feature_name}_route.dart     # 라우트 정의
└── {feature_name}_route.g.dart   # 자동 생성 (build_runner)
```

---

## Import 순서 (필수)

```dart
// 1. Feature 패키지 (페이지 import)
import 'package:{feature_name}/{feature_name}.dart';

// 2. 의존성 패키지
import 'package:dependencies/dependencies.dart';

// 3. Core (트랜지션 페이지)
import 'package:core/core.dart';

// 4. 생성 파일
part '{feature_name}_route.g.dart';
```

---

## 핵심 패턴

### 1. App 라우트 정의 (FadeTransitionPage)

```dart
part '{feature_name}_route.g.dart';

/// {Feature} 화면 라우트 정의
///
/// 앱의 {feature} 화면으로 연결됩니다.
/// 애니메이션 효과로 [FadeTransitionPage]를 사용합니다.
@TypedGoRoute<{Feature}Route>(
  path: {Feature}RouteName.path,
  routes: [
    // 중첩 라우트 정의
    TypedGoRoute<{Feature}DetailRoute>(
      path: {Feature}DetailRoute.path,
    ),
  ],
)
class {Feature}Route extends GoRouteData with ${Feature}Route {
  /// {Feature} 화면 라우트 생성자
  const {Feature}Route({this.initialId});

  /// 초기 ID (선택사항)
  final int? initialId;

  /// {Feature} 화면 라우트 경로
  static const String path = {Feature}RouteName.path;

  static const LocalKey _key = ValueKey(path);

  @override
  FadeTransitionPage buildPage(BuildContext context, GoRouterState state) {
    return FadeTransitionPage(
      key: _key,
      child: {Feature}Page(initialId: initialId),
    );
  }
}
```

### 2. Console 라우트 정의 (NoTransitionPage)

```dart
/// Console {Feature} 화면 라우트 정의
///
/// 어드민 콘솔의 {feature} 화면으로 연결됩니다.
/// 트랜지션 없이 [NoTransitionPage]를 사용합니다.
@TypedGoRoute<Console{Feature}Route>(
  path: Console{Feature}RouteName.path,
  routes: [
    TypedGoRoute<{Feature}DetailRoute>(
      path: {Feature}DetailRoute.path,
    ),
  ],
)
class Console{Feature}Route extends GoRouteData with $Console{Feature}Route {
  /// Console{Feature} 화면 라우트 생성자
  const Console{Feature}Route();

  /// Console{Feature} 기본 경로
  static RouteBase get base => Console{Feature}RouteName.base;

  @override
  Page<void> buildPage(BuildContext context, GoRouterState state) {
    // 🔑 동적 key 생성 (쿼리 변화에 따라 페이지 재생성)
    final query = state.uri.query;
    final pageKey = ValueKey(
      'console_{feature}_list-${query.isNotEmpty ? query : 'noq'}',
    );

    return NoTransitionPage<void>(
      key: pageKey,
      child: const Console{Feature}Page(),
    );
  }
}
```

### 3. RouteName 추상 클래스 패턴

```dart
/// {Feature} 라우트 경로 이름을 정의하는 추상 클래스
///
/// [path]는 '/{feature}'로 설정되어 {feature} 화면의 경로로 사용됩니다.
abstract class {Feature}RouteName {
  /// {Feature} 화면 라우트 베이스
  static RouteBase get base => ${featureCamel}Route;

  /// {Feature} 화면 라우트 경로
  static const String path = '/{feature}';

  /// {Feature} 화면 라우트 이름
  static const String name = '{feature}';
}
```

### 4. 중첩 라우트 정의

```dart
/// {Feature} 상세 화면 라우트 정의
///
/// 실제 경로는 '/{feature}/{id}'가 됩니다.
@immutable
class {Feature}DetailRoute extends GoRouteData with ${Feature}DetailRoute {
  /// {Feature} 상세 화면 라우트 생성자
  const {Feature}DetailRoute({required this.id});

  /// 조회할 {feature}의 ID
  final int id;

  /// {Feature} 상세 화면 라우트 경로
  static const String path = ':id';

  @override
  FadeTransitionPage buildPage(BuildContext context, GoRouterState state) {
    // id와 전체 쿼리 문자열을 포함하여 고유한 키 생성
    final fullPath = state.uri.toString();
    final pageKey = ValueKey('{feature}Detail/$fullPath');

    return FadeTransitionPage(
      key: pageKey,
      child: {Feature}DetailPage(id: id),
    );
  }
}
```

### 5. 쿼리 파라미터 파싱 헬퍼

```dart
/// 쿼리 파라미터에서 정수 값을 파싱하는 헬퍼 함수
int? _parseIntQueryParam(String? value) {
  return value != null ? int.tryParse(value) : null;
}

/// 쿼리 파라미터에서 불리언 값을 파싱하는 헬퍼 함수
bool _parseBoolQueryParam(String? value) {
  return value?.toLowerCase() == 'true';
}
```

### 6. 라우트 상수 정의

```dart
/// 라우트 상수 정의 (private)
abstract class _RouteConstants {
  /// 상세 라우트 식별자
  static const String detail = 'detail';

  /// 편집 라우트 식별자
  static const String edit = 'edit';

  /// 추가 라우트 식별자
  static const String add = 'add';
}
```

---

## 트랜지션 페이지 유형

| 타입 | 클래스 | 사용처 |
|------|--------|--------|
| Fade | `FadeTransitionPage` | App 일반 화면 |
| Slide | `SlideTransitionPage` | 모달, 상세 화면 |
| None | `NoTransitionPage` | Console, 탭 전환 |

---

## 참조 파일

```
feature/application/store/lib/src/route/store_route.dart
feature/console/console_member_list/lib/src/route/console_member_list_route.dart
feature/application/app_router/lib/src/route/app_routes.dart
package/core/lib/src/transition/
```

---

## 체크리스트

- [ ] TypedGoRoute 어노테이션 정의
- [ ] GoRouteData 상속 + mixin 적용
- [ ] RouteName 추상 클래스 정의
- [ ] 적절한 트랜지션 페이지 선택
- [ ] 고유한 ValueKey 생성
- [ ] 쿼리 파라미터 처리
- [ ] KDoc 주석 작성
- [ ] part 지시문으로 .g.dart 연결
- [ ] build_runner 실행 (`melos run build`)

---

## 관련 문서

- [Presentation Layer Agent](./presentation-layer-agent.md)
- [DI Agent](./di-agent.md)

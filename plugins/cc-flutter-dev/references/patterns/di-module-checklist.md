# DI Module 등록 체크리스트

> 새로운 Feature 모듈 추가 시 DI 등록 누락 방지를 위한 가이드

## 문제 사례

**에러**: `GetIt: Object/factory with type IConsoleAnalyticsRepository is not registered inside GetIt`

**원인**: `console_service_locator.dart`에 모듈 미등록

**해결**: `ExternalModule(ConsoleAnalyticsPackageModule)` 추가

## 체크리스트

### 1. Feature 모듈 DI 파일 생성

```
feature/{type}/{feature_name}/lib/src/di/
├── injector.dart              # @microPackageInit
└── injector.module.dart       # build_runner 자동 생성
```

### 2. Repository/UseCase/BLoC 어노테이션

```dart
// Repository
@LazySingleton(as: IConsoleAnalyticsRepository)
class ConsoleAnalyticsRepository implements IConsoleAnalyticsRepository { }

// UseCase
@lazySingleton
class GetDashboardMetricsUseCase { }

// BLoC
@injectable
class AnalyticsBloC extends Bloc<...> { }
```

### 3. Service Locator 등록

**Console 기능** → `package/core/lib/src/di/console_service_locator.dart`

```dart
import 'package:console_analytics/console_analytics.dart';  // import 추가

@InjectableInit(
  externalPackageModulesAfter: [
    // 📊 콘솔 기능 모듈들
    ExternalModule(ConsoleAnalyticsPackageModule),  // 등록 추가
    // ...
  ],
)
```

**App 기능** → `package/core/lib/src/di/app_service_locator.dart`

### 4. 빌드 및 검증

```bash
# DI 설정 재생성
melos run build:select --no-select -- --scope=core

# 또는 전체 빌드
melos run build
```

## 모듈 그룹 순서

| 순서 | 그룹 | 예시 |
|------|------|------|
| 1 | 공통 | `AuthPackageModule`, `LifePackageModule` |
| 2 | 라우터 | `ConsoleRouterPackageModule` |
| 3 | 기능 | `ConsoleAnalyticsPackageModule` (알파벳순) |
| 4 | 설정 | `SettingsPackageModule`, `SignInWithEmailPackageModule` |

## 자주 발생하는 실수

### 실수 1: import 누락

```dart
// ❌ ExternalModule만 추가하고 import 누락
ExternalModule(ConsoleAnalyticsPackageModule),  // 컴파일 에러

// ✅ import도 함께 추가
import 'package:console_analytics/console_analytics.dart';
ExternalModule(ConsoleAnalyticsPackageModule),
```

### 실수 2: 잘못된 Service Locator

```dart
// ❌ Console 기능을 app_service_locator에 등록
// app_service_locator.dart
ExternalModule(ConsoleAnalyticsPackageModule),  // 콘솔 앱에서 사용 불가

// ✅ 올바른 위치에 등록
// console_service_locator.dart
ExternalModule(ConsoleAnalyticsPackageModule),  // 콘솔 앱에서 사용 가능
```

## 관련 커밋

- `84d80f359`: ConsoleAnalyticsPackageModule DI 등록 누락 수정

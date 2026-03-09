---
name: di-agent
description: Dependency Injection 설정 생성 전문가. Injectable 모듈 등록, GetIt 기반 DI 구현 시 사용
invoke: /app:di
aliases: ["/di:create", "/inject:setup"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: bloc
---

# DI Agent

> Dependency Injection 설정 생성 전문 에이전트

---

## 역할

GetIt + Injectable 기반 의존성 주입 설정을 생성합니다.
- @microPackageInit 어노테이션 적용
- Injectable 모듈 등록
- Service Locator 통합
- 외부 패키지 모듈 등록

---

## 실행 조건

- `/app:di` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션의 마지막 단계에서 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `module_type` | ❌ | `app`, `console`, `common` (기본: `app`) |
| `register_to` | ❌ | 등록할 Service Locator (`app`, `console`, `both`) |

---

## 생성 파일

```
feature/{module_type}/{feature_name}/lib/src/di/
├── injector.dart              # DI 설정 파일
└── injector.module.dart       # 자동 생성 (build_runner)
```

---

## Import 순서 (필수)

```dart
// 1. 의존성 패키지
import 'package:dependencies/dependencies.dart';
```

---

## 핵심 패턴

### 1. 기본 Injector 정의

```dart
import 'package:dependencies/dependencies.dart';

/// {Feature} 모듈 인젝터
@microPackageInit
void injector{Feature}Module() {
  assert(
    () {
      // DI 등록 지점
      return true;
    }(),
    '{Feature} module injector noop init (no registrations yet)',
  );
}
```

### 2. Injectable 어노테이션

**Repository 등록:**
```dart
import 'package:dependencies/dependencies.dart';

/// {Feature} Repository 구현
@LazySingleton(as: I{Feature}Repository)
class {Feature}Repository implements I{Feature}Repository {
  /// {Feature}Repository 생성자
  const {Feature}Repository();

  // Repository 구현...
}
```

**UseCase 등록:**
```dart
import 'package:dependencies/dependencies.dart';

/// {Action} UseCase
@lazySingleton
class {Action}UseCase implements UseCase<{Output}, {Params}> {
  /// {Action}UseCase 생성자
  const {Action}UseCase(this._repository);

  final I{Feature}Repository _repository;

  @override
  Future<Either<Failure, {Output}>> call({Params} params) async {
    // UseCase 구현...
  }
}
```

**BLoC 등록:**
```dart
import 'package:dependencies/dependencies.dart';

/// {Feature} BLoC
@injectable
class {Feature}Bloc extends Bloc<{Feature}Event, {Feature}State> {
  /// {Feature}Bloc 생성자
  {Feature}Bloc(this._useCase) : super(const {Feature}Initial()) {
    on<{Feature}Event>(_onEvent);
  }

  final {Action}UseCase _useCase;

  // BLoC 구현...
}
```

### 3. 생성되는 Module 파일 구조

```dart
//@GeneratedMicroModule;{Feature}PackageModule;package:{feature}/src/di/injector.module.dart
// GENERATED CODE - DO NOT MODIFY BY HAND
// ignore_for_file: type=lint
// coverage:ignore-file

import 'dart:async' as _i687;

import 'package:injectable/injectable.dart' as _i526;
import 'package:{feature}/src/data/repository/{feature}_repository.dart' as _i737;
import 'package:{feature}/src/presentation/bloc/{feature}_bloc.dart' as _i166;

class {Feature}PackageModule extends _i526.MicroPackageModule {
  @override
  _i687.FutureOr<void> init(_i526.GetItHelper gh) {
    gh.factory<_i166.{Feature}Bloc>(() => _i166.{Feature}Bloc());
    gh.lazySingleton<I{Feature}Repository>(() => _i737.{Feature}Repository());
  }
}
```

### 4. Service Locator 등록

**App Service Locator (package/core):**
```dart
import 'package:core/src/di/app_service_locator.config.dart' as app_config;
import 'package:dependencies/dependencies.dart';

/// App GetIt instance
final GetIt appGetIt = GetIt.instance;

@InjectableInit(
  asExtension: false,
  externalPackageModulesAfter: [
    // 🔧 공통 모듈들
    ExternalModule(AuthPackageModule),
    ExternalModule(LifePackageModule),

    // 📚 애플리케이션 기능 모듈들
    ExternalModule({Feature}PackageModule),  // ← 새 모듈 추가

    // ⚙️ 설정 및 공통 기능 모듈들
    ExternalModule(SettingsPackageModule),
  ],
)
Future<void> configureAppDependencies(Env env) async {
  await app_config.init(appGetIt, environment: env.name);
  Log.init();
  await AuthInit.init();
}
```

**Console Service Locator:**
```dart
@InjectableInit(
  asExtension: false,
  externalPackageModulesAfter: [
    // 🔧 공통 모듈들
    ExternalModule(AuthPackageModule),
    ExternalModule(LifePackageModule),

    // 🖥️ 콘솔 전용 모듈들
    ExternalModule(Console{Feature}PackageModule),  // ← 새 모듈 추가
  ],
)
Future<void> configureConsoleDependencies(Env env) async {
  await console_config.init(consoleGetIt, environment: env.name);
}
```

---

## Injectable 어노테이션 종류

| 어노테이션 | 용도 | 스코프 |
|-----------|------|--------|
| `@injectable` | 일반 클래스 등록 | Factory (매번 새 인스턴스) |
| `@lazySingleton` | 지연 싱글톤 | 첫 호출 시 생성, 이후 재사용 |
| `@singleton` | 즉시 싱글톤 | 앱 시작 시 즉시 생성 |
| `@LazySingleton(as: Interface)` | 인터페이스 바인딩 | 인터페이스로 등록 |
| `@microPackageInit` | 마이크로 패키지 | 모듈 단위 등록 |

---

## 의존성 주입 패턴

### 생성자 주입 (권장)

```dart
@injectable
class {Feature}Bloc extends Bloc<{Feature}Event, {Feature}State> {
  {Feature}Bloc(
    this._getUseCase,
    this._createUseCase,
  ) : super(const {Feature}Initial());

  final Get{Entity}UseCase _getUseCase;
  final Create{Entity}UseCase _createUseCase;
}
```

### getIt 직접 사용 (Widget에서)

```dart
class {Feature}Page extends StatelessWidget {
  const {Feature}Page({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => getIt<{Feature}Bloc>()
        ..add(const {Feature}Event.load()),
      child: const _{Feature}View(),
    );
  }
}
```

---

## 참조 파일

```
package/core/lib/src/di/app_service_locator.dart
package/core/lib/src/di/console_service_locator.dart
feature/application/my_library/lib/src/di/injector.dart
feature/application/my_library/lib/src/di/injector.module.dart
```

---

## 체크리스트

- [ ] @microPackageInit 어노테이션 적용
- [ ] injector.dart 파일 생성
- [ ] Repository에 @LazySingleton(as:) 적용
- [ ] UseCase에 @lazySingleton 적용
- [ ] BLoC에 @injectable 적용
- [ ] Service Locator에 ExternalModule 등록
- [ ] build_runner 실행 (`melos run build`)
- [ ] 의존성 그래프 확인

---

## 빌드 명령어

```bash
# 전체 빌드
melos run build

# 특정 패키지만 빌드
cd feature/{module_type}/{feature_name}
dart run build_runner build --delete-conflicting-outputs

# 클린 빌드
melos run build:clean && melos run build
```

---

## 관련 문서

- [Route Agent](./route-agent.md)
- [Presentation Layer Agent](./presentation-layer-agent.md)
- [Data Layer Agent](./data-layer-agent.md)

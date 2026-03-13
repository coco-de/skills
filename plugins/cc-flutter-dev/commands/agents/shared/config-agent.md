---
name: config-agent
description: 환경 설정 관리 전문가. Envied 어노테이션, 플레이버 스위칭 패턴 구현 시 사용
invoke: /shared:config
aliases: ["/env:create", "/config:setup"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
---

# Config Agent

> 환경 설정 관리 전문 에이전트

---

## 역할

환경별 설정을 관리하고 생성합니다.
- Envied 어노테이션 기반 환경 변수 관리
- 3개 환경 클래스 (EnvProd, EnvStg, EnvDev)
- EnvConfig 플레이버 스위칭 패턴
- Platform별 분기 처리

---

## 실행 조건

- `/shared:config` 커맨드 호출 시 활성화
- 환경 변수, 설정 파일 작업 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `env_type` | ❌ | `dev`, `stg`, `prod` (기본: `dev`) |
| `variable_name` | ❌ | 추가할 환경 변수명 |
| `is_secret` | ❌ | 난독화 여부 (기본: false) |

---

## 패키지 구조

```
shared/config/
├── lib/
│   ├── config.dart                   # Export 파일
│   └── src/
│       ├── env/
│       │   ├── env_config.dart       # 플레이버 스위칭
│       │   ├── env_prod.dart         # Production 환경
│       │   ├── env_stg.dart          # Staging 환경
│       │   └── env_dev.dart          # Development 환경
│       ├── generated/                # 자동 생성
│       │   ├── env_prod.g.dart
│       │   ├── env_stg.g.dart
│       │   └── env_dev.g.dart
│       └── platform/
│           └── platform_config.dart  # 플랫폼별 분기
└── env/
    ├── .env.dev                      # 개발 환경 변수
    ├── .env.stg                      # 스테이징 환경 변수
    └── .env.prod                     # 프로덕션 환경 변수
```

---

## Import 순서 (필수)

```dart
// 1. Dart 기본
import 'dart:io';

// 2. Envied 패키지
import 'package:envied/envied.dart';

// 3. 생성 파일
part 'env_dev.g.dart';
```

---

## 핵심 패턴

### 1. 환경 클래스 정의 (Envied)

```dart
import 'package:envied/envied.dart';

part 'env_dev.g.dart';

/// 개발 환경 설정
///
/// [Envied]를 사용하여 `.env.dev` 파일의 환경 변수를 로드합니다.
@Envied(path: 'env/.env.dev', useConstantCase: true)
abstract class EnvDev {
  /// API 기본 URL
  @EnviedField(varName: 'API_BASE_URL')
  static const String apiBaseUrl = _EnvDev.apiBaseUrl;

  /// API 키 (난독화)
  @EnviedField(varName: 'API_KEY', obfuscate: true)
  static final String apiKey = _EnvDev.apiKey;

  /// Firebase 프로젝트 ID
  @EnviedField(varName: 'FIREBASE_PROJECT_ID')
  static const String firebaseProjectId = _EnvDev.firebaseProjectId;

  /// 디버그 모드 활성화
  @EnviedField(varName: 'DEBUG_MODE', defaultValue: 'true')
  static const String debugMode = _EnvDev.debugMode;

  /// Serverpod 서버 URL
  @EnviedField(varName: 'SERVERPOD_URL')
  static const String serverpodUrl = _EnvDev.serverpodUrl;

  /// Serverpod 포트
  @EnviedField(varName: 'SERVERPOD_PORT', defaultValue: '8080')
  static const String serverpodPort = _EnvDev.serverpodPort;
}
```

### 2. 환경 클래스 (Staging)

```dart
import 'package:envied/envied.dart';

part 'env_stg.g.dart';

/// 스테이징 환경 설정
@Envied(path: 'env/.env.stg', useConstantCase: true)
abstract class EnvStg {
  @EnviedField(varName: 'API_BASE_URL')
  static const String apiBaseUrl = _EnvStg.apiBaseUrl;

  @EnviedField(varName: 'API_KEY', obfuscate: true)
  static final String apiKey = _EnvStg.apiKey;

  @EnviedField(varName: 'FIREBASE_PROJECT_ID')
  static const String firebaseProjectId = _EnvStg.firebaseProjectId;

  @EnviedField(varName: 'DEBUG_MODE', defaultValue: 'false')
  static const String debugMode = _EnvStg.debugMode;

  @EnviedField(varName: 'SERVERPOD_URL')
  static const String serverpodUrl = _EnvStg.serverpodUrl;

  @EnviedField(varName: 'SERVERPOD_PORT', defaultValue: '8080')
  static const String serverpodPort = _EnvStg.serverpodPort;
}
```

### 3. 환경 클래스 (Production)

```dart
import 'package:envied/envied.dart';

part 'env_prod.g.dart';

/// 프로덕션 환경 설정
@Envied(path: 'env/.env.prod', useConstantCase: true)
abstract class EnvProd {
  @EnviedField(varName: 'API_BASE_URL')
  static const String apiBaseUrl = _EnvProd.apiBaseUrl;

  @EnviedField(varName: 'API_KEY', obfuscate: true)
  static final String apiKey = _EnvProd.apiKey;

  @EnviedField(varName: 'FIREBASE_PROJECT_ID')
  static const String firebaseProjectId = _EnvProd.firebaseProjectId;

  @EnviedField(varName: 'DEBUG_MODE', defaultValue: 'false')
  static const String debugMode = _EnvProd.debugMode;

  @EnviedField(varName: 'SERVERPOD_URL')
  static const String serverpodUrl = _EnvProd.serverpodUrl;

  @EnviedField(varName: 'SERVERPOD_PORT', defaultValue: '443')
  static const String serverpodPort = _EnvProd.serverpodPort;
}
```

### 4. 플레이버 스위칭 패턴

```dart
/// 환경 타입 열거형
enum Flavor {
  /// 개발 환경
  development,

  /// 스테이징 환경
  staging,

  /// 프로덕션 환경
  production,
}

/// 환경 설정 매니저
///
/// 런타임에 현재 환경을 기반으로 설정값을 제공합니다.
abstract final class EnvConfig {
  /// 현재 환경 (빌드 시 --dart-define으로 설정)
  static Flavor get flavor {
    const flavorString = String.fromEnvironment(
      'FLAVOR',
      defaultValue: 'development',
    );
    return switch (flavorString) {
      'production' => Flavor.production,
      'staging' => Flavor.staging,
      _ => Flavor.development,
    };
  }

  /// API 기본 URL
  static String get apiBaseUrl => switch (flavor) {
        Flavor.production => EnvProd.apiBaseUrl,
        Flavor.staging => EnvStg.apiBaseUrl,
        Flavor.development => EnvDev.apiBaseUrl,
      };

  /// API 키
  static String get apiKey => switch (flavor) {
        Flavor.production => EnvProd.apiKey,
        Flavor.staging => EnvStg.apiKey,
        Flavor.development => EnvDev.apiKey,
      };

  /// Firebase 프로젝트 ID
  static String get firebaseProjectId => switch (flavor) {
        Flavor.production => EnvProd.firebaseProjectId,
        Flavor.staging => EnvStg.firebaseProjectId,
        Flavor.development => EnvDev.firebaseProjectId,
      };

  /// 디버그 모드 여부
  static bool get isDebugMode => switch (flavor) {
        Flavor.production => EnvProd.debugMode == 'true',
        Flavor.staging => EnvStg.debugMode == 'true',
        Flavor.development => EnvDev.debugMode == 'true',
      };

  /// Serverpod URL
  static String get serverpodUrl => switch (flavor) {
        Flavor.production => EnvProd.serverpodUrl,
        Flavor.staging => EnvStg.serverpodUrl,
        Flavor.development => EnvDev.serverpodUrl,
      };

  /// Serverpod 포트
  static int get serverpodPort => switch (flavor) {
        Flavor.production => int.parse(EnvProd.serverpodPort),
        Flavor.staging => int.parse(EnvStg.serverpodPort),
        Flavor.development => int.parse(EnvDev.serverpodPort),
      };

  /// 프로덕션 환경 여부
  static bool get isProduction => flavor == Flavor.production;

  /// 개발 환경 여부
  static bool get isDevelopment => flavor == Flavor.development;

  /// 스테이징 환경 여부
  static bool get isStaging => flavor == Flavor.staging;
}
```

### 5. 플랫폼별 분기 처리

```dart
import 'dart:io';

import 'package:flutter/foundation.dart';

/// 플랫폼 설정
abstract final class PlatformConfig {
  /// 현재 플랫폼
  static TargetPlatform get platform {
    if (kIsWeb) return TargetPlatform.android; // 웹은 Android로 취급
    if (Platform.isIOS) return TargetPlatform.iOS;
    if (Platform.isAndroid) return TargetPlatform.android;
    if (Platform.isMacOS) return TargetPlatform.macOS;
    if (Platform.isWindows) return TargetPlatform.windows;
    if (Platform.isLinux) return TargetPlatform.linux;
    return TargetPlatform.android;
  }

  /// iOS 여부
  static bool get isIOS => !kIsWeb && Platform.isIOS;

  /// Android 여부
  static bool get isAndroid => !kIsWeb && Platform.isAndroid;

  /// 웹 여부
  static bool get isWeb => kIsWeb;

  /// 데스크톱 여부
  static bool get isDesktop =>
      !kIsWeb &&
      (Platform.isMacOS || Platform.isWindows || Platform.isLinux);

  /// 모바일 여부
  static bool get isMobile =>
      !kIsWeb && (Platform.isIOS || Platform.isAndroid);
}
```

### 6. .env 파일 형식

```bash
# .env.dev
API_BASE_URL=https://dev-api.example.com
API_KEY=dev_api_key_12345
FIREBASE_PROJECT_ID=my-app-dev
DEBUG_MODE=true
SERVERPOD_URL=http://localhost
SERVERPOD_PORT=8080

# .env.stg
API_BASE_URL=https://stg-api.example.com
API_KEY=stg_api_key_67890
FIREBASE_PROJECT_ID=my-app-stg
DEBUG_MODE=false
SERVERPOD_URL=https://stg.example.com
SERVERPOD_PORT=8080

# .env.prod
API_BASE_URL=https://api.example.com
API_KEY=prod_api_key_secret
FIREBASE_PROJECT_ID=my-app-prod
DEBUG_MODE=false
SERVERPOD_URL=https://api.example.com
SERVERPOD_PORT=443
```

---

## 빌드 명령어

```bash
# 환경 변수 코드 생성
melos run generate:env

# 특정 환경으로 빌드
flutter build apk --dart-define=FLAVOR=production
flutter build ios --dart-define=FLAVOR=staging
flutter run --dart-define=FLAVOR=development

# 클린 빌드
cd shared/config && dart run build_runner build --delete-conflicting-outputs
```

---

## Envied 어노테이션 종류

| 어노테이션 | 용도 | 예시 |
|-----------|------|------|
| `@Envied` | 환경 클래스 정의 | `@Envied(path: 'env/.env.dev')` |
| `@EnviedField` | 환경 변수 필드 | `@EnviedField(varName: 'API_KEY')` |
| `obfuscate: true` | 값 난독화 | API 키, 시크릿에 사용 |
| `defaultValue` | 기본값 설정 | 선택적 변수에 사용 |
| `useConstantCase: true` | 상수 케이스 자동 변환 | `apiBaseUrl` → `API_BASE_URL` |

---

## 참조 파일

```
shared/config/lib/src/env/env_dev.dart
shared/config/lib/src/env/env_stg.dart
shared/config/lib/src/env/env_prod.dart
shared/config/lib/src/env/env_config.dart
shared/config/lib/src/platform/platform_config.dart
```

---

## 체크리스트

- [ ] 3개 환경 클래스 (dev, stg, prod) 정의
- [ ] part 지시문으로 .g.dart 연결
- [ ] 민감 정보 obfuscate: true 적용
- [ ] EnvConfig 플레이버 스위칭 구현
- [ ] .env 파일 .gitignore에 추가
- [ ] build_runner 실행 (`melos run generate:env`)
- [ ] 빌드 시 --dart-define 사용 확인

---

## 관련 문서

- [DI Agent](../app/di-agent.md)
- [Serverpod Endpoint Agent](../backend/serverpod-endpoint-agent.md)

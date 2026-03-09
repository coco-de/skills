# Data Mapper 패턴

OpenAPI Response를 Domain Entity로 변환하는 Mapper 클래스 작성 규칙입니다.

## 디렉토리 구조

```
feature/{app_or_common}/{feature_name}/lib/src/
├── data/
│   ├── mappers/           # Mapper 클래스 위치
│   │   └── {feature}_mapper.dart
│   ├── repository/
│   │   └── mixins/
│   │       └── {feature}_openapi_mixin.dart  # Mapper 사용
│   └── data.dart          # mappers export 포함
└── domain/
```

## 현재 Mapper 파일 목록

| Feature | 파일 경로 | 주요 변환 |
|---------|----------|----------|
| attendance | `feature/application/attendance/.../attendance_mapper.dart` | QR 검증, 출석 기록 |
| classroom | `feature/application/classroom/.../classroom_mapper.dart` | 클래스, 학생, 폴더 정보 |
| homework | `feature/application/homework/.../homework_mapper.dart` | 숙제 목록, 진행률 |
| league | `feature/application/league/.../league_mapper.dart` | 리그, 랭킹 정보 |
| level_test | `feature/application/level_test/.../level_test_mapper.dart` | 레벨테스트, 문제, 결과 |
| notice_board | `feature/application/notice_board/.../notice_board_mapper.dart` | 알림장, 첨부파일 |
| notification | `feature/application/notification/.../notification_mapper.dart` | 푸시 알림 |
| payment | `feature/application/payment/.../payment_mapper.dart` | 결제 정보 |
| report | `feature/application/report/.../report_mapper.dart` | 학습 리포트 |
| review | `feature/application/review/.../review_mapper.dart` | 오답노트 |
| auth | `feature/common/auth/.../auth_mapper.dart` | 인증, 토큰 |
| mypage | `feature/common/mypage/.../mypage_mapper.dart` | 사용자 프로필 |
| settings | `feature/common/settings/.../settings_mapper.dart` | 앱 설정 |

> **참고**: core.dart가 모든 Feature 패키지의 Mapper를 re-export하므로, `import 'package:core/core.dart';`만으로 모든 Mapper 접근 가능

## Mapper 클래스 구조

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';
import 'package:openapi/api.dart';

/// {Feature} API Response를 Domain Entity로 변환하는 Mapper
abstract final class {Feature}Mapper {
  /// {Response}를 {Entity}로 변환
  static {Entity} from{Response}({Response} response) {
    return {Entity}(
      // 필드 매핑
    );
  }

  /// API 오류를 Failure로 변환
  static Failure mapException(Object error, StackTrace stackTrace) {
    Log.e('{Feature} API Error', error: error, stackTrace: stackTrace);
    if (error is DioException) {
      return NetworkFailure(
        error.message ?? 'Network error occurred',
        error: error,
        stackTrace: stackTrace,
      );
    }
    return UnexpectedFailure(
      error.toString(),
      error: error is Exception ? error : null,
      stackTrace: stackTrace,
    );
  }
}
```

## 규칙

### 클래스 선언
- `abstract final class` 사용 (인스턴스화 방지)
- 모든 메서드는 `static`으로 선언

### 네이밍 컨벤션
| 항목 | 패턴 | 예시 |
|------|------|------|
| 파일명 | `{feature}_mapper.dart` | `classroom_mapper.dart` |
| 클래스명 | `{Feature}Mapper` | `ClassroomMapper` |
| 변환 메서드 | `from{ResponseType}()` | `fromClassResponse()` |
| 파싱 메서드 | `parse{EnumType}()` | `parseWithdrawReason()` |
| 에러 매핑 | `mapException()` | 공통 사용 |

### 변환 메서드 작성
```dart
// Good: 명확한 null 처리와 기본값
static ClassroomClassInfo fromClassResponse(ClassResponse response) {
  return ClassroomClassInfo(
    classId: response.classId?.toString() ?? '',
    name: response.name ?? '',
    createdAt: response.createdAt ?? DateTime.now(),
  );
}

// Bad: null 체크 없이 직접 사용
static ClassroomClassInfo fromClassResponse(ClassResponse response) {
  return ClassroomClassInfo(
    classId: response.classId.toString(), // NPE 위험
    name: response.name,
  );
}
```

### 안전한 파싱 패턴

**int.tryParse 사용 (필수)**
```dart
// ✅ Good: int.tryParse로 안전한 파싱
static int parseUserId(String? value) {
  return int.tryParse(value ?? '') ?? 0;
}

// ❌ Bad: int.parse 직접 사용 (예외 발생 위험)
static int parseUserId(String? value) {
  return int.parse(value!); // FormatException 위험
}
```

**parseXXX 메서드로 enum 변환**
```dart
/// String을 WithdrawReason enum으로 변환
static WithdrawReason parseWithdrawReason(String? value) {
  return switch (value) {
    'INCONVENIENT' => WithdrawReason.inconvenient,
    'CONTENT_UNSATISFIED' => WithdrawReason.contentUnsatisfied,
    'COST_BURDEN' => WithdrawReason.costBurden,
    'LOW_FREQUENCY' => WithdrawReason.lowFrequency,
    'OTHER_SERVICE' => WithdrawReason.otherService,
    'ETC' => WithdrawReason.etc,
    _ => WithdrawReason.etc, // 기본값
  };
}
```

## OpenAPI Enum 패턴

OpenAPI 스키마에서 생성된 enum 타입은 `@JsonEnum` 어노테이션을 사용합니다.

### 필수 구현 패턴

`@JsonEnum(valueField: 'json')` 사용 시 **toJson() 메서드를 수동으로 추가**해야 합니다.

```dart
// package/openapi/lib/src/api/models/{enum_name}.dart
@JsonEnum(valueField: 'json')
enum StudentEnrollmentItemType {
  create('CREATE'),
  existing('EXISTING');

  const StudentEnrollmentItemType(this.json);
  final String json;

  // ✅ 필수: toJson() 메서드 (build_runner가 .g.dart에서 호출)
  String toJson() => json;

  // ✅ 권장: fromJson() 팩토리 메서드
  static StudentEnrollmentItemType fromJson(String value) {
    return StudentEnrollmentItemType.values.firstWhere(
      (item) => item.json == value,
      orElse: () => StudentEnrollmentItemType.existing, // 안전한 기본값
    );
  }
}
```

### 에러 발생 시

```
Error: The method 'toJson' isn't defined for the type 'EnumType'.
  'type': instance.type.toJson(),
```

**해결**: 해당 enum 파일에 `String toJson() => json;` 메서드 추가

### 체크리스트

- [ ] `@JsonEnum(valueField: 'json')` 어노테이션 확인
- [ ] `final String json;` 필드 존재
- [ ] `String toJson() => json;` 메서드 추가
- [ ] `static fromJson()` 메서드 추가 (기본값 포함)

### Repository Mixin에서 사용
```dart
import 'package:{feature}/src/data/mappers/{feature}_mapper.dart';

mixin {Feature}OpenApiMixin implements I{Feature}Repository {
  @override
  Future<Either<Failure, {Entity}>> get{Entity}ById(String id) async {
    try {
      final response = await openApiService.{feature}Api.get{Entity}(id: id);
      return Right({Feature}Mapper.from{Response}(response));
    } on Exception catch (error, stackTrace) {
      return Left({Feature}Mapper.mapException(error, stackTrace));
    }
  }
}
```

## Export 설정

`data/data.dart`에 mapper export 추가:
```dart
export 'mappers/{feature}_mapper.dart';
export 'repository/{feature}_repository.dart';
export 'repository/factories/factories.dart';
```

## 보안 규칙 (로깅)

### 민감 정보 로깅 금지

```dart
// ❌ 금지: 민감 정보를 로그에 포함
Log.d('🔐 로그인 시도: userId=$userId');
Log.d('📱 SMS 인증: phoneNumber=$phoneNumber, code=$code');
Log.d('🔄 토큰 갱신: refreshToken=$refreshToken');

// ✅ 권장: 상태만 기록, 민감 정보 제외
Log.d('🔐 로그인 API 호출');
Log.d('📱 SMS 인증번호 확인 API 호출');
Log.d('🔄 토큰 갱신 API 호출');
```

### 민감 정보 목록

| 유형 | 예시 |
|------|------|
| 인증 정보 | password, userPw, pin |
| 토큰 | accessToken, refreshToken, idToken |
| 식별 정보 | userId, loginId (로그 목적으로는 제외) |
| 개인 정보 | phoneNumber, email |
| 인증 코드 | smsCode, verificationCode, authCode |

## DioException 처리

### Import 규칙

```dart
// ✅ 올바른 방법: dependencies 패키지 통해 import
import 'package:dependencies/dependencies.dart';
// DioException, DioExceptionType 사용 가능

// ❌ 금지: dio 패키지 직접 import
import 'package:dio/dio.dart';
```

### 에러 처리 패턴

```dart
} on DioException catch (error, stackTrace) {
  Log.e('❌ API 에러', error: error, stackTrace: stackTrace);
  // HTTP 상태 코드별 분기 (권장)
  if (error.response?.statusCode == 401) {
    return const Left(AuthFailure.tokenExpired);
  }
  return Left(_mapException(error, stackTrace));
} on Exception catch (error, stackTrace) {
  Log.e('❌ API 에러', error: error, stackTrace: stackTrace);
  return Left(_mapException(error, stackTrace));
}
```

### HTTP 상태 코드별 Failure 매핑

| 상태 코드 | Failure 타입 | 설명 | 예시 |
|-----------|--------------|------|------|
| 400 | `ValidationFailure` | 잘못된 요청 | 필수 파라미터 누락 |
| 401 | `AuthFailure.tokenExpired` | 인증 만료 | 토큰 만료/무효 |
| 403 | `AuthFailure.forbidden` | 권한 없음 | 접근 권한 부족 |
| 404 | `NotFoundFailure` | 리소스 없음 | 존재하지 않는 데이터 |
| 409 | `ConflictFailure` | 충돌 | 중복 데이터 |
| 500+ | `ServerFailure` | 서버 오류 | 내부 서버 오류 |

**상태 코드별 분기 예시**
```dart
static Failure mapException(Object error, StackTrace stackTrace) {
  if (error is DioException) {
    final statusCode = error.response?.statusCode;
    return switch (statusCode) {
      400 => ValidationFailure(error.message ?? '잘못된 요청'),
      401 => const AuthFailure.tokenExpired(),
      403 => const AuthFailure.forbidden(),
      404 => NotFoundFailure(error.message ?? '리소스를 찾을 수 없음'),
      409 => ConflictFailure(error.message ?? '데이터 충돌'),
      >= 500 => ServerFailure(error.message ?? '서버 오류'),
      _ => NetworkFailure(error.message ?? 'Network error'),
    };
  }
  return UnexpectedFailure(error.toString(), stackTrace: stackTrace);
}
```

## DI 모듈 트러블슈팅

### Repository 의존성 추가 후 빌드 에러

Repository가 새로운 의존성(예: AuthBloc)을 추가하면, build_runner가 자동 감지하지 못하는 경우가 있습니다.

**에러 메시지**:
```
Error: Too few positional arguments: 2 required, 1 given.
  () => NoticeBoardRepository(gh<OpenApiClient>()),
```

**원인**:
- Repository Mixin을 통한 간접 의존성을 injectable이 감지하지 못함
- build_runner 캐시가 남아있음

**해결 방법**:

1. **build_runner 재실행**:
```bash
cd feature/application/{feature}
dart run build_runner clean
dart run build_runner build --delete-conflicting-outputs
```

2. **DI 모듈 수동 수정** (build_runner가 감지 못할 경우):
```dart
// feature/application/{feature}/lib/src/di/injector.module.dart
gh.lazySingleton<INoticeBoardRepository>(
  () => NoticeBoardRepository(
    gh<OpenApiClient>(),
    gh<AuthBloc>(),  // ← 수동으로 추가
  ),
);
```

**참고**: 생성된 파일(`*.module.dart`)을 수동 수정하면 다음 build_runner 실행 시 덮어쓰기될 수 있습니다. 가능하면 build_runner가 올바르게 감지하도록 Repository 구조를 조정하는 것이 좋습니다.

---

## 체크리스트

### 기본 설정
- [ ] `data/mappers/` 디렉토리에 mapper 파일 생성
- [ ] `abstract final class` 사용
- [ ] 모든 메서드 `static` 선언
- [ ] `data.dart`에 export 추가
- [ ] Repository mixin에서 `{Feature}Mapper` 사용

### 네이밍 패턴
- [ ] `from{Response}()` 변환 메서드 네이밍
- [ ] `parse{EnumType}()` enum 파싱 메서드 네이밍

### 안전한 코드
- [ ] null-safe 필드 매핑 (기본값 제공)
- [ ] `int.tryParse` 사용 (`int.parse` 금지)
- [ ] switch 표현식으로 enum 변환 (기본값 포함)
- [ ] **로그에 민감 정보 없음** (userId, password, token 등)

### 에러 처리
- [ ] `mapException()` 공통 에러 처리 포함
- [ ] HTTP 상태 코드별 적절한 Failure 반환
- [ ] 401 -> AuthFailure.tokenExpired
- [ ] 404 -> NotFoundFailure
- [ ] 500+ -> ServerFailure
- [ ] **Log.e() 호출 시 error, stackTrace 파라미터 모두 포함**

## Private 헬퍼 메서드 패턴

### 네이밍 규칙

| 용도 | 접두사 | 예시 |
|------|--------|------|
| Enum/Status 변환 | `_map*` | `_mapProgressStatus()`, `_mapTemplate()` |
| 필드/데이터 추출 | `_extract*` | `_extractChoices()`, `_extractStimulus()` |
| 조건부 계산 | 없음 | `_calculateAccuracyRate()`, `_validateData()` |

### 사용 예시

```dart
// ✅ CORRECT
static HomeworkAssignmentStatus _mapProgressStatus(ProgressStatus? status) {
  return switch (status) {
    ProgressStatus.notStarted => HomeworkAssignmentStatus.notStarted,
    ProgressStatus.inProgress => HomeworkAssignmentStatus.inProgress,
    ProgressStatus.completed => HomeworkAssignmentStatus.completed,
    _ => HomeworkAssignmentStatus.notStarted,
  };
}

static List<QuizChoice> _extractChoices(ResponseItem item) {
  return item.choices?.map((c) => QuizChoice(
    text: c.text ?? '',
    isCorrect: c.isCorrect ?? false,
  )).toList() ?? [];
}

// ❌ WRONG
static HomeworkAssignmentStatus _progressStatusMapper(...) { }  // 동사 먼저
static List<QuizChoice> _getChoices(...) { }  // _get은 헬퍼 메서드에 부적절
```

## Log.e() 구조화 패턴 (필수)

### 표준 패턴

```dart
// ✅ CORRECT: error와 stackTrace 모두 파라미터로 전달
Log.e('Homework API Error', error: error, stackTrace: stackTrace);
Log.e('❌ API 에러', error: error, stackTrace: stackTrace);

// ❌ WRONG: 문자열 보간 사용 (파싱 불가)
Log.e('API Error: $error', stackTrace: stackTrace);
Log.e('API Error: $error');

// ❌ WRONG: stackTrace 누락
Log.e('API Error', error: error);
```

### 이유

1. **일관성**: 모든 에러 로깅이 동일한 구조
2. **파싱 가능**: 로그 집계 도구가 `error` 필드 파싱 가능
3. **정보 보존**: stackTrace가 구조화된 필드로 저장됨

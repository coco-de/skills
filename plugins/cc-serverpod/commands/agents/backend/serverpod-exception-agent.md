---
name: serverpod-exception-agent
description: Serverpod 예외, 검증, 상수 클래스 생성 전문가. 에러 처리 패턴 구현 시 사용
invoke: /serverpod:exception
aliases: ["/backend:exception", "/api:error"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
skills: serverpod
---

# Serverpod Exception Agent

> Serverpod 백엔드의 예외, 검증, 상수 클래스 생성 전문 에이전트

---

## 역할

Serverpod 백엔드의 예외 처리 시스템을 구현합니다.
- sealed class 기반 예외 정의
- Validator 클래스 패턴
- Constants, ErrorMessages 분리
- ExceptionHandler.safeExecute() 래핑

---

## 실행 조건

- `/serverpod:exception` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션의 Step 1.5에서 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `include_validator` | ❌ | Validator 생성 여부 (기본: true) |
| `include_constants` | ❌ | Constants 생성 여부 (기본: true) |

---

## 생성 파일

```
backend/kobic_server/lib/src/feature/{feature_name}/
├── exception/
│   ├── exception.dart                    # Export 파일
│   ├── {feature_name}_exception.dart     # 예외 클래스
│   └── {feature_name}_error_messages.dart # 에러 메시지
├── validation/
│   ├── validation.dart                   # Export 파일
│   └── {feature_name}_validator.dart     # 검증 클래스
├── constant/
│   ├── constant.dart                     # Export 파일
│   └── {feature_name}_constants.dart     # 상수 클래스
└── helper/
    ├── helper.dart                       # Export 파일
    └── exception_handler.dart            # 예외 핸들러
```

---

## Import 순서 (필수)

```dart
// 1. Dart 기본 라이브러리
import 'dart:core';

// 2. 공용 상수
import 'package:kobic_server/src/common/constants/http_status_constants.dart';

// 3. Feature 내부 상수/메시지
import '../constant/constant.dart';
```

---

## 핵심 패턴

### 1. sealed class 예외 정의

```dart
/// {Feature} 관련 예외의 기본 클래스
sealed class {Feature}Exceptions implements Exception {
  const {Feature}Exceptions(
    this.message,
    this.statusCode, [
    this.stackTrace,
  ]);

  final String message;
  final int statusCode;
  final StackTrace? stackTrace;
}

/// {Feature} 리소스를 찾을 수 없는 경우
final class {Feature}NotFoundException extends {Feature}Exceptions {
  {Feature}NotFoundException(int resourceId)
      : super(
          {Feature}ErrorMessages.notFound('{feature}', resourceId),
          {Feature}Constants.httpNotFound,
        );
}

/// {Feature} 유효성 검증 실패
final class {Feature}ValidationException extends {Feature}Exceptions {
  {Feature}ValidationException(String reason)
      : super(
          reason,
          {Feature}Constants.httpBadRequest,
        );
}

/// {Feature} 파라미터 유효성 검증 실패
final class Invalid{Feature}ParameterException extends {Feature}Exceptions {
  Invalid{Feature}ParameterException(String parameter, String reason)
      : super(
          {Feature}ErrorMessages.invalidParameter(parameter, reason),
          {Feature}Constants.httpBadRequest,
        );
}

/// {Feature} 데이터베이스 작업 실패
final class {Feature}DatabaseOperationException extends {Feature}Exceptions {
  {Feature}DatabaseOperationException(
    String operation,
    String errorMessage, [
    StackTrace? stackTrace,
  ]) : super(
          {Feature}ErrorMessages.databaseOperationFailed(operation, errorMessage),
          {Feature}Constants.httpInternalServerError,
          stackTrace,
        );
}
```

### 2. ErrorMessages 클래스

```dart
/// {Feature} 에러 메시지 정의
class {Feature}ErrorMessages {
  const {Feature}ErrorMessages._();

  /// 리소스를 찾을 수 없음
  static String notFound(String resource, int id) =>
      '$resource(ID: $id)를 찾을 수 없습니다.';

  /// 파라미터 유효성 검증 실패
  static String invalidParameter(String param, String reason) =>
      '$param: $reason';

  /// 데이터베이스 작업 실패
  static String databaseOperationFailed(String operation, String error) =>
      '데이터베이스 작업 실패 ($operation): $error';

  /// 필수 파라미터 누락
  static const String idRequired = 'ID는 필수입니다.';
  static const String idTooSmall = 'ID는 1 이상이어야 합니다.';

  /// 페이징 관련
  static const String limitTooSmall = 'limit은 최소 1 이상이어야 합니다.';
  static const String limitTooLarge = 'limit은 최대 100 이하여야 합니다.';
  static const String offsetNegative = 'offset은 0 이상이어야 합니다.';
}
```

### 3. Constants 클래스

```dart
/// {Feature} 관련 상수
class {Feature}Constants {
  const {Feature}Constants._();

  // ============ HTTP 상태 코드 ============
  static const int httpOk = HttpStatusConstants.ok;                        // 200
  static const int httpCreated = HttpStatusConstants.created;              // 201
  static const int httpBadRequest = HttpStatusConstants.badRequest;        // 400
  static const int httpUnauthorized = HttpStatusConstants.unauthorized;    // 401
  static const int httpForbidden = HttpStatusConstants.forbidden;          // 403
  static const int httpNotFound = HttpStatusConstants.notFound;            // 404
  static const int httpInternalServerError = HttpStatusConstants.internalServerError; // 500

  // ============ 페이징 상수 ============
  static const int defaultPageLimit = 20;
  static const int maxPageLimit = 100;
  static const int minPageLimit = 1;
  static const int defaultOffset = 0;

  // ============ ID 관련 ============
  static const int minValidId = 1;

  // ============ 필드명 (검증용) ============
  static const String fieldId = 'id';
  static const String fieldLimit = 'limit';
  static const String fieldOffset = 'offset';

  // ============ DB 작업명 ============
  static const String dbOperationInsert = '{feature} insert';
  static const String dbOperationUpdate = '{feature} update';
  static const String dbOperationDelete = '{feature} delete';
  static const String dbOperationSelect = '{feature} select';
}
```

### 4. Validator 클래스

```dart
/// {Feature} 입력 검증
class {Feature}Validator {
  const {Feature}Validator._();

  /// ID 검증 (선택적)
  static void validateId(int? id) {
    if (id != null && id < {Feature}Constants.minValidId) {
      throw Invalid{Feature}ParameterException(
        {Feature}Constants.fieldId,
        {Feature}ErrorMessages.idTooSmall,
      );
    }
  }

  /// ID 검증 (필수)
  static void validateRequiredId(int? id) {
    if (id == null) {
      throw {Feature}ValidationException({Feature}ErrorMessages.idRequired);
    }
    validateId(id);
  }

  /// 페이징 파라미터 검증
  static void validatePagingParams(int limit, int offset) {
    if (limit < {Feature}Constants.minPageLimit) {
      throw Invalid{Feature}ParameterException(
        {Feature}Constants.fieldLimit,
        {Feature}ErrorMessages.limitTooSmall,
      );
    }
    if (limit > {Feature}Constants.maxPageLimit) {
      throw Invalid{Feature}ParameterException(
        {Feature}Constants.fieldLimit,
        {Feature}ErrorMessages.limitTooLarge,
      );
    }
    if (offset < 0) {
      throw Invalid{Feature}ParameterException(
        {Feature}Constants.fieldOffset,
        {Feature}ErrorMessages.offsetNegative,
      );
    }
  }

  /// 객체 null 체크
  static void validateNotNull<T>(T? value, String fieldName) {
    if (value == null) {
      throw Invalid{Feature}ParameterException(
        fieldName,
        '$fieldName은(는) 필수입니다.',
      );
    }
  }
}
```

### 5. ExceptionHandler

```dart
/// 예외 처리 핸들러
class ExceptionHandler {
  const ExceptionHandler._();

  /// 안전한 실행 래퍼
  static Future<T> safeExecute<T>(
    Future<T> Function() operation, {
    required String operationName,
  }) async {
    try {
      return await operation();
    } on {Feature}Exceptions {
      rethrow;
    } on Exception catch (error, stackTrace) {
      throw {Feature}DatabaseOperationException(
        operationName,
        error.toString(),
        stackTrace,
      );
    }
  }
}
```

---

## 참조 파일

```
backend/kobic_server/lib/src/feature/banner/exception/banner_exception.dart
backend/kobic_server/lib/src/feature/banner/constant/banner_constants.dart
backend/kobic_server/lib/src/feature/banner/validation/banner_validator.dart
backend/kobic_server/lib/src/common/constants/http_status_constants.dart
```

---

## 체크리스트

- [ ] sealed class 패턴 적용
- [ ] 모든 예외에 statusCode 포함
- [ ] ErrorMessages 메서드/상수 분리
- [ ] Constants에서 HttpStatusConstants 참조
- [ ] Validator에서 검증 실패 시 명확한 메시지
- [ ] ExceptionHandler.safeExecute() 패턴 적용
- [ ] KDoc 주석 작성

---

## 관련 문서

- [Serverpod Endpoint Agent](./serverpod-endpoint-agent.md)
- [Serverpod Model Agent](./serverpod-model-agent.md)

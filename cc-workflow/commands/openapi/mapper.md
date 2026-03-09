---
name: openapi:mapper
description: "OpenAPI Response → Domain Entity Mapper 자동 생성"
invoke: /openapi:mapper
aliases: ["/mapper", "/mapper:create"]
category: good-teacher-workflow
complexity: standard
---

# /openapi:mapper

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/openapi:mapper` patterns.

## Triggers

- OpenAPI Response를 Domain Entity로 변환하는 Mapper가 필요할 때
- 새로운 API 엔드포인트에 대한 매핑 로직이 필요할 때
- `/feature:data` 전에 Mapper를 미리 생성할 때

## Context Trigger Pattern

```
/openapi:mapper {feature_name} {response_type} {entity_type}
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `classroom`, `student` |
| `response_type` | ✅ | OpenAPI Response 타입명 | `ClassResponse`, `StudentResponse` |
| `entity_type` | ✅ | Domain Entity 타입명 | `ClassroomClassInfo`, `StudentInfo` |

## Behavioral Flow

### 1. OpenAPI Response 분석

```bash
# OpenAPI 패키지에서 Response 타입 확인
find package/openapi -name "*.dart" | xargs grep -l "{response_type}"
```

분석 대상:
- Response 필드 목록
- 필드 타입 (nullable 여부)
- 중첩된 객체 타입

### 2. Domain Entity 분석

```bash
# Domain Entity 확인
find feature -path "*/domain/entity/*" -name "*.dart" | xargs grep -l "{entity_type}"
```

분석 대상:
- Entity 필드 목록
- 필드 타입 및 기본값
- 필수/선택 필드

### 3. Mapper 클래스 생성

> 규칙: `.claude/rules/data-mapper.md` 참조

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';
import 'package:openapi/api.dart';

/// {Feature} API Response를 Domain Entity로 변환하는 Mapper
abstract final class {Feature}Mapper {
  /// {Response}Response를 {Entity}로 변환
  static {Entity} from{Response}Response({Response}Response response) {
    return {Entity}(
      // 필수 필드: null-safe 변환
      id: response.id?.toString() ?? '',
      name: response.name ?? '',

      // 날짜 필드
      createdAt: response.createdAt ?? DateTime.now(),

      // 중첩 객체 필드
      teacher: response.teacher != null
          ? fromTeacherResponse(response.teacher!)
          : null,

      // 리스트 필드
      students: response.students
              ?.map(fromStudentResponse)
              .toList() ??
          [],

      // enum 필드
      status: _mapStatus(response.status),
    );
  }

  /// {Response}Response 리스트 변환
  static List<{Entity}> from{Response}ResponseList(
    List<{Response}Response>? responses,
  ) {
    return responses?.map(from{Response}Response).toList() ?? [];
  }

  /// 중첩 객체 변환 (TeacherResponse → TeacherInfo)
  static TeacherInfo fromTeacherResponse(TeacherResponse response) {
    return TeacherInfo(
      id: response.id?.toString() ?? '',
      name: response.name ?? '',
      // ...
    );
  }

  /// enum 변환 헬퍼
  static {Entity}Status _mapStatus({Response}Status? status) {
    return switch (status) {
      {Response}Status.active => {Entity}Status.active,
      {Response}Status.inactive => {Entity}Status.inactive,
      _ => {Entity}Status.unknown,
    };
  }

  /// API 오류를 Failure로 변환
  static Failure mapException(Object error, StackTrace stackTrace) {
    Log.e('API Error: $error', stackTrace: stackTrace);
    if (error is DioException) {
      final statusCode = error.response?.statusCode;
      final message = error.message ?? 'Network error occurred';

      return switch (statusCode) {
        400 => ValidationFailure(message, error: error, stackTrace: stackTrace),
        401 => AuthFailure(message, error: error, stackTrace: stackTrace),
        403 => PermissionFailure(message, error: error, stackTrace: stackTrace),
        404 => NotFoundFailure(message, error: error, stackTrace: stackTrace),
        _ => NetworkFailure(message, error: error, stackTrace: stackTrace),
      };
    }
    return UnexpectedFailure(
      error.toString(),
      error: error is Exception ? error : null,
      stackTrace: stackTrace,
    );
  }
}
```

## Output File

```
feature/{location}/{feature_name}/lib/src/data/mappers/{feature}_mapper.dart
```

## Mapping Rules

### 필드 타입별 변환 패턴

| Response 타입 | Entity 타입 | 변환 패턴 |
|--------------|------------|----------|
| `int?` | `String` | `response.id?.toString() ?? ''` |
| `String?` | `String` | `response.name ?? ''` |
| `DateTime?` | `DateTime` | `response.createdAt ?? DateTime.now()` |
| `List<T>?` | `List<T>` | `responses?.map(fromT).toList() ?? []` |
| `Nested?` | `Entity?` | `response.nested != null ? fromNested(response.nested!) : null` |
| `Enum?` | `Enum` | `_mapEnum(response.status)` |

### Null Safety 원칙

1. **필수 필드**: 기본값 제공
   ```dart
   id: response.id?.toString() ?? '',
   name: response.name ?? '',
   ```

2. **선택 필드**: nullable 유지
   ```dart
   description: response.description,
   avatarUrl: response.avatarUrl,
   ```

3. **리스트 필드**: 빈 리스트 기본값
   ```dart
   items: response.items?.map(fromItem).toList() ?? [],
   ```

4. **날짜 필드**: 현재 시간 또는 nullable
   ```dart
   createdAt: response.createdAt ?? DateTime.now(),
   updatedAt: response.updatedAt,  // nullable 허용 시
   ```

## Examples

### 교실 Mapper 생성

```
/openapi:mapper classroom ClassResponse ClassroomClassInfo
```

생성 결과:
```dart
abstract final class ClassroomMapper {
  static ClassroomClassInfo fromClassResponse(ClassResponse response) {
    return ClassroomClassInfo(
      classId: response.classId?.toString() ?? '',
      name: response.name ?? '',
      description: response.description ?? '',
      teacherId: response.teacherId?.toString() ?? '',
      joinCode: response.joinCode ?? '',
      memberCount: response.memberCount ?? 0,
      createdAt: response.createdAt ?? DateTime.now(),
    );
  }

  static Failure mapException(Object error, StackTrace stackTrace) { ... }
}
```

### 학생 Mapper 생성

```
/openapi:mapper student StudentResponse StudentInfo
```

## Integration with /feature:data

`/openapi:mapper`는 `/feature:data`의 전처리 단계로 사용:

```
1. /openapi:mapper classroom ClassResponse ClassroomClassInfo
   → data/mappers/classroom_mapper.dart 생성

2. /feature:data classroom ClassroomClassInfo
   → Repository, Mixin에서 ClassroomMapper 사용
```

## Checklist

- [ ] OpenAPI Response 타입 분석
- [ ] Domain Entity 타입 분석
- [ ] 필드 매핑 테이블 작성
- [ ] Mapper 클래스 생성 (`abstract final class`)
- [ ] `from{Response}Response()` 메서드 구현
- [ ] `from{Response}ResponseList()` 메서드 구현
- [ ] 중첩 객체 변환 메서드 구현
- [ ] enum 변환 헬퍼 구현
- [ ] `mapException()` 메서드 구현
- [ ] null-safe 필드 매핑 검증
- [ ] data.dart에 export 추가

## 참조 문서

- `.claude/rules/data-mapper.md` - Mapper 패턴 상세 규칙
- `.claude/references/patterns/repository-patterns.md` - Repository 패턴
- `feature/application/classroom/lib/src/data/mappers/classroom_mapper.dart` - 참조 구현

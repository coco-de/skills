---
name: feature:domain
description: "Clean Architecture Domain Layer 생성"
invoke: /feature:domain
aliases: ["/domain", "/domain:create"]
category: petmedi-workflow
complexity: standard
mcp-servers: [serena, context7]
---

# /feature:domain

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/feature:domain` patterns.

## Triggers

- 새로운 Feature의 Domain Layer가 필요할 때
- Entity, Repository Interface, UseCase 생성이 필요할 때
- `/feature:create` 오케스트레이션의 Step 3에서 호출될 때

## Context Trigger Pattern

```
/feature:domain {feature_name} {entity_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `community`, `chat` |
| `entity_name` | ✅ | Entity명 (PascalCase) | `Post`, `Message` |
| `--location` | ❌ | 위치 | `application`, `common`, `console` (기본: `application`) |
| `--usecases` | ❌ | 생성할 UseCase | `"getList, get, create, update, delete"` |

## Behavioral Flow

### 1. 기존 패턴 분석

```
Serena MCP를 사용하여 기존 Domain Layer 패턴 분석:
- feature/application/community/lib/src/domain/entity/post.dart
- feature/application/community/lib/src/domain/repository/i_community_repository.dart
- feature/application/community/lib/src/domain/usecase/get_posts_usecase.dart
```

### 2. Entity 생성

```dart
import 'package:dependencies/dependencies.dart';

/// {엔티티} 한글 설명
class {Entity} extends Equatable {
  /// [{Entity}]를 생성합니다.
  const {Entity}({
    required this.id,
    required this.title,
    required this.authorId,
    required this.createdAt,
    this.updatedAt,
  });

  final int id;
  final String title;
  final int authorId;
  final DateTime createdAt;
  final DateTime? updatedAt;

  @override
  List<Object?> get props => [id, title, authorId, createdAt, updatedAt];
}
```

### 3. Repository Interface 생성

```dart
import 'package:dependencies/dependencies.dart';

/// {Feature} Repository Interface
abstract interface class I{Feature}Repository {
  /// {엔티티} 목록을 조회합니다.
  Future<Either<Failure, {Entity}ListResult>> get{Entity}s({
    required int limit,
    required int offset,
    {Entity}Category? category,
  });

  /// {엔티티} 목록을 Stream으로 조회합니다 (Cache-First).
  Stream<CacheFirstResult<{Entity}ListResult>> get{Entity}sAsStream({...});

  /// {엔티티} 단건 조회
  Future<Either<Failure, {Entity}>> get{Entity}(int {entity}Id);

  /// {엔티티} 생성
  Future<Either<Failure, {Entity}>> create{Entity}({...});

  /// {엔티티} 수정
  Future<Either<Failure, {Entity}>> update{Entity}({...});

  /// {엔티티} 삭제
  Future<Either<Failure, void>> delete{Entity}(int {entity}Id);
}
```

### 4. UseCase 생성 (상수 생성자 + ServiceLocator)

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// {엔티티} 목록 조회 Params
class Get{Entity}sParams {
  const Get{Entity}sParams({
    this.limit = 20,
    this.offset = 0,
    this.category,
  });

  final int limit;
  final int offset;
  final {Entity}Category? category;
}

/// {엔티티} 목록을 조회하는 UseCase
class Get{Entity}sUsecase
    implements UseCase<{Entity}ListResult, Get{Entity}sParams, I{Feature}Repository> {

  /// [Get{Entity}sUsecase]를 생성합니다.
  const Get{Entity}sUsecase();  // ✅ 상수 생성자 (필수)

  @override
  I{Feature}Repository get repo => getIt();  // ✅ ServiceLocator (필수)

  @override
  Future<Either<Failure, {Entity}ListResult>> call(Get{Entity}sParams params) {
    return repo.get{Entity}s(
      limit: params.limit,
      offset: params.offset,
      category: params.category,
    );
  }
}
```

### 5. UseCase 테스트 생성

```dart
void main() {
  late Get{Entity}sUsecase usecase;
  late MockI{Feature}Repository mockRepository;

  setUpAll(registerFallbackValues);

  setUp(() {
    mockRepository = MockI{Feature}Repository();
    registerTestLazySingleton<I{Feature}Repository>(mockRepository);
    usecase = const Get{Entity}sUsecase();
  });

  tearDown(getIt.reset);

  group('Get{Entity}sUsecase', () {
    test('성공 시 Right({Entity}ListResult) 반환', () async {
      // arrange
      when(() => mockRepository.get{Entity}s(...))
        .thenAnswer((_) async => Right(testResult));

      // act
      final result = await usecase(testParams);

      // assert
      expect(result.isRight(), true);
      verify(() => mockRepository.get{Entity}s(...)).called(1);
    });
  });
}
```

## Output Files

```
feature/{location}/{feature_name}/lib/src/domain/
├── entity/
│   ├── {entity}.dart
│   ├── {entity}_list_result.dart
│   └── entity.dart           # export
├── repository/
│   ├── i_{feature}_repository.dart
│   └── repository.dart       # export
├── usecase/
│   ├── get_{entity}s_usecase.dart
│   ├── get_{entity}_usecase.dart
│   ├── create_{entity}_usecase.dart
│   ├── update_{entity}_usecase.dart
│   ├── delete_{entity}_usecase.dart
│   └── usecase.dart          # export
├── failure/
│   └── {feature}_failure_messages.dart
└── exception/
    └── {feature}_exception.dart

feature/{location}/{feature_name}/test/domain/usecase/
├── get_{entity}s_usecase_test.dart
├── get_{entity}_usecase_test.dart
├── create_{entity}_usecase_test.dart
├── update_{entity}_usecase_test.dart
└── delete_{entity}_usecase_test.dart
```

## Post-Generation Commands

```bash
# 코드 생성 (Freezed 등)
melos exec --scope={feature_name} -- "dart run build_runner build --delete-conflicting-outputs"
```

## MCP Integration

- **Serena**: 기존 Domain Layer 패턴 분석, 심볼 검색
- **Context7**: Clean Architecture, Either 패턴 문서 참조

## Examples

### 게시글 Domain 생성

```
/feature:domain community Post --location application
```

### 채팅 메시지 Domain 생성

```
/feature:domain chat Message --location application
  --usecases "getMessages, sendMessage, markAsRead"
```

## 참조 에이전트

상세 구현 규칙은 `~/.claude/commands/agents/domain-layer-agent.md` 참조

## 핵심 규칙 요약

### ✅ 필수 패턴

1. **Entity는 Equatable 상속**
2. **Repository Interface는 `I` prefix**
3. **UseCase는 상수 생성자 사용** (`const GetPostsUsecase()`)
4. **UseCase는 ServiceLocator** (`get repo => getIt()`)
5. **모든 UseCase에 단위 테스트 작성**

### ❌ 금지 패턴

```dart
// ❌ @injectable 어노테이션 금지
// @injectable
// class GetPostsUseCase { ... }

// ❌ 생성자 주입 금지
// GetPostsUseCase(this._repository);

// ❌ 상대 경로 import 금지
// import '../entity/post.dart';
```

### 테스트 패턴

```dart
setUp(() {
  mockRepository = MockI{Feature}Repository();
  registerTestLazySingleton<I{Feature}Repository>(mockRepository);
  usecase = const Get{Entity}sUsecase();  // 상수 생성자
});

tearDown(getIt.reset);  // GetIt 리셋 필수
```

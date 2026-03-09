---
name: feature:data
description: "Clean Architecture Data Layer 생성"
invoke: /feature:data
aliases: ["/data", "/data:create"]
category: petmedi-workflow
complexity: standard
mcp-servers: [serena, context7]
---

# /feature:data

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/feature:data` patterns.

## Triggers

- 새로운 Feature의 Data Layer가 필요할 때
- Repository 구현체, Serverpod Mixin, Cache 전략 구현이 필요할 때
- `/feature:create` 오케스트레이션의 Step 4에서 호출될 때

## Context Trigger Pattern

```
/feature:data {feature_name} {entity_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `community`, `chat` |
| `entity_name` | ✅ | Entity명 (PascalCase) | `Post`, `Message` |
| `--location` | ❌ | 위치 | `application`, `common`, `console` (기본: `application`) |
| `--caching` | ❌ | 캐싱 전략 | `swr`, `cache-first`, `none` (기본: `swr`) |

## Behavioral Flow

### 1. 기존 패턴 분석

```
Serena MCP를 사용하여 기존 Data Layer 패턴 분석:
- feature/application/community/lib/src/data/repository/community_repository.dart
- feature/application/community/lib/src/data/repository/mixins/community_serverpod_mixin.dart
```

### 2. Repository 구현체 생성

```dart
import 'package:dependencies/dependencies.dart';
import 'package:serverpod_service/serverpod_service.dart';

import '../../domain/repository/i_{feature}_repository.dart';
import 'mixins/{feature}_serverpod_mixin.dart';

/// {Feature} Repository 구현체
@LazySingleton(as: I{Feature}Repository)
class {Feature}Repository
    with {Feature}ServerpodMixin
    implements I{Feature}Repository {

  /// [{Feature}Repository]를 생성합니다.
  {Feature}Repository(
    this._serverpodService,
    this._database,
  );

  final ServerpodService _serverpodService;
  final {Feature}Database _database;

  @override
  ServerpodClient get client => _serverpodService.client;

  @override
  {Entity}Dao get {entity}Dao => _database.{entity}Dao;
}
```

### 3. Serverpod Mixin 생성 (네임스페이스 필수!)

```dart
import 'package:dependencies/dependencies.dart';
import 'package:serverpod_service/serverpod_service.dart' as pod;  // ✅ 네임스페이스 필수

import '../../domain/entity/{entity}.dart';
import '../../domain/repository/i_{feature}_repository.dart';

/// {Feature} Serverpod API Mixin
mixin {Feature}ServerpodMixin implements I{Feature}Repository {
  /// Serverpod 클라이언트
  pod.ServerpodClient get client;  // ✅ 네임스페이스 사용

  /// {Entity} DAO
  {Entity}Dao get {entity}Dao;

  @override
  Future<Either<Failure, {Entity}>> create{Entity}({
    required {Entity}Category category,
    required String title,
    required String content,
  }) async {
    try {
      // 1. Domain → Protocol 변환 (네임스페이스 사용)
      final request = pod.{Entity}CreateRequest(
        category: _categoryToProtocol(category),
        title: title,
        content: content,
      );

      // 2. API 호출
      final response = await client.{feature}.create{Entity}(request);

      // 3. Protocol → Entity 변환
      final entity = _map{Entity}FromProtocol(response);

      // 4. 캐시에 저장
      await {entity}Dao.save{Entity}(entity);

      return Right(entity);
    } on Exception catch (error, stackTrace) {
      return left(
        RepositoryFailure(
          'Failed to create {entity}',
          error: error,
          stackTrace: stackTrace,
        ),
      );
    }
  }

  // DTO 변환 헬퍼
  {Entity} _map{Entity}FromProtocol(pod.{Entity} response) {
    return {Entity}(
      id: response.id ?? 0,
      title: response.title,
      category: _categoryFromProtocol(response.category),
      // ...
    );
  }

  // Protocol → Domain 변환
  {Entity}Category _categoryFromProtocol(pod.{Entity}Category category) {
    switch (category) {
      case pod.{Entity}Category.qna:
        return {Entity}Category.qna;
      // ...
    }
  }

  // Domain → Protocol 변환
  pod.{Entity}Category _categoryToProtocol({Entity}Category category) {
    switch (category) {
      case {Entity}Category.qna:
        return pod.{Entity}Category.qna;
      // ...
    }
  }
}
```

### 4. SWR 캐싱 패턴

```dart
@override
Future<Either<Failure, {Entity}ListResult>> get{Entity}s({...}) async {
  try {
    // 1. 캐시 확인
    final cachedData = await {entity}Dao.getAll{Entity}s(limit: limit, offset: offset);

    if (cachedData.isNotEmpty) {
      // 2. 캐시 데이터 즉시 반환
      final entities = cachedData.map((data) => {entity}Dao.dataTo{Entity}(data)).toList();
      final cachedResult = {Entity}ListResult(items: entities, ...);

      // 3. 백그라운드에서 갱신 (SWR)
      unawaited(_refresh{Entity}sInBackground(...));

      return Right(cachedResult);
    }

    // 4. 캐시 없으면 API 호출
    return _fetchAndCache{Entity}s(...);
  } on Exception catch (error, stackTrace) {
    return left(RepositoryFailure(...));
  }
}
```

### 5. Cache-First Stream 패턴

```dart
@override
Stream<CacheFirstResult<{Entity}ListResult>> get{Entity}sAsStream({...}) async* {
  // 1. 캐시 조회
  final cachedData = await {entity}Dao.getAll{Entity}s(...);

  // 2. 캐시가 있으면 즉시 emit
  if (cachedData.isNotEmpty) {
    yield CacheFirstResult(data: cachedResult, fromCache: true, isRefreshing: true);
  }

  // 3. 네트워크에서 최신 데이터
  final result = await get{Entity}s(...);

  // 4. 네트워크 결과 emit
  yield* result.fold(
    (failure) async* { if (cachedData.isEmpty) throw Exception(...); },
    (networkResult) async* {
      yield CacheFirstResult(data: networkResult, fromCache: false, isRefreshing: false);
    },
  );
}
```

## Output Files

```
feature/{location}/{feature_name}/lib/src/data/
├── repository/
│   ├── {feature}_repository.dart
│   ├── mixins/
│   │   └── {feature}_serverpod_mixin.dart
│   └── repository.dart       # export
├── cache/
│   └── {entity}_cache_repository.dart
└── local/
    ├── tables/
    │   └── {entity}_table.dart
    ├── dao/
    │   └── {entity}_dao.dart
    └── {feature}_database.dart
```

## Post-Generation Commands

```bash
# 코드 생성 (Drift, Injectable)
melos exec --scope={feature_name} -- "dart run build_runner build --delete-conflicting-outputs"
```

## MCP Integration

- **Serena**: 기존 Data Layer 패턴 분석, 심볼 검색
- **Context7**: Serverpod, Drift 문서 참조

## Examples

### 게시글 Data Layer 생성

```
/feature:data community Post --location application --caching swr
```

### 채팅 메시지 Data Layer 생성

```
/feature:data chat Message --location application --caching cache-first
```

## 참조 에이전트

상세 구현 규칙은 `~/.claude/commands/agents/data-layer-agent.md` 참조

## 핵심 규칙 요약

### ✅ Critical Import 패턴

```dart
// Repository 구현체
import 'package:dependencies/dependencies.dart';

// Mixin (네임스페이스 필수!)
import 'package:serverpod_service/serverpod_service.dart' as pod;

mixin {Feature}ServerpodMixin implements I{Feature}Repository {
  pod.ServerpodClient get client;  // ✅ 네임스페이스 사용

  // Domain Entity 사용 (네임스페이스 없음)
  {Entity}Category category = {Entity}Category.qna;

  // Serverpod DTO 사용 (네임스페이스 사용)
  pod.{Entity}Category apiCategory = pod.{Entity}Category.qna;
}
```

### 캐싱 전략 선택

| 전략 | 사용 시점 | 특징 |
|------|----------|------|
| **SWR** | 실시간 데이터 | 캐시 즉시 반환 + 백그라운드 갱신 |
| **Cache-First** | 정적 데이터 | 캐시 있으면 네트워크 호출 안 함 |
| **None** | 항상 최신 필요 | 매번 네트워크 호출 |

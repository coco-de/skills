---
name: serverpod:endpoint
description: "Serverpod 엔드포인트 및 서비스 클래스 생성"
category: petmedi-workflow
complexity: standard
mcp-servers: [serena, context7]
---

# /serverpod:endpoint

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/serverpod:endpoint` patterns.

## Triggers

- 새로운 Serverpod API 엔드포인트가 필요할 때
- 백엔드 비즈니스 로직 구현이 필요할 때
- `/feature:create` 오케스트레이션의 Step 2에서 호출될 때

## Context Trigger Pattern

```
/serverpod:endpoint {feature_name} {entity_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `community`, `chat` |
| `entity_name` | ✅ | Entity명 (PascalCase) | `Post`, `Message` |
| `--type` | ❌ | 엔드포인트 타입 | `app`, `console`, `both` (기본: `app`) |
| `--methods` | ❌ | 생성할 메서드 | `"getList, get, create, update, delete"` |

## Behavioral Flow

### 1. 기존 패턴 분석

```
Serena MCP를 사용하여 기존 엔드포인트 패턴 분석:
- backend/petmedi_server/lib/src/feature/community/endpoint/post_endpoint.dart
- backend/petmedi_server/lib/src/feature/community/service/post_service.dart
```

### 2. Import 순서 준수 (필수)

```dart
// 1. Serverpod 프레임워크
import 'package:serverpod/server.dart';

// 2. 생성된 프로토콜 (모델)
import 'package:petmedi_server/src/generated/protocol.dart';

// 3. Feature 내부 서비스
import 'package:petmedi_server/src/feature/{feature}/service/{feature}_service.dart';

// 4. 공통 유틸리티
import 'package:petmedi_server/src/common/authenticated_mixin.dart';
```

### 3. Endpoint 클래스 생성

**App Endpoint** (`{feature}_endpoint.dart`):

```dart
/// {Feature} 엔드포인트
///
/// - 목록 조회, 단건 조회, 생성, 수정, 삭제 기능 제공
/// - 인증된 사용자만 접근 가능
class {Feature}Endpoint extends Endpoint with AuthenticatedMixin {
  /// {엔티티} 목록을 조회합니다.
  Future<{Entity}ListResponse> get{Entity}s(
    Session session, {
    int? limit,
    int? offset,
    {Entity}Category? category,
  }) async {
    return {Feature}Service.get{Entity}s(
      session,
      limit: limit ?? 20,
      offset: offset ?? 0,
      category: category,
    );
  }

  /// {엔티티}를 생성합니다.
  Future<{Entity}> create{Entity}(
    Session session,
    {Entity}CreateRequest request,
  ) async {
    final user = await requireAuthenticatedUser(session);
    return {Feature}Service.create{Entity}(session, request, user.id!);
  }

  // ... 나머지 CRUD 메서드
}
```

**Console Endpoint** (`{feature}_console_endpoint.dart`):

```dart
/// {Feature} 콘솔 엔드포인트 (관리자용)
class {Feature}ConsoleEndpoint extends Endpoint {
  @override
  bool get requireLogin => true;

  @override
  Set<Scope> get requiredScopes => {Scope.admin};

  /// 전체 {엔티티} 목록을 조회합니다 (관리자용).
  Future<List<{Entity}>> getAll{Entity}s(
    Session session, {
    int? limit,
    int? offset,
    bool includeDeleted = false,
  }) async {
    return {Feature}Service.getAll{Entity}sForAdmin(
      session,
      limit: limit,
      offset: offset,
      includeDeleted: includeDeleted,
    );
  }
}
```

### 4. Service 클래스 생성

```dart
/// {Feature} 비즈니스 로직 서비스
class {Feature}Service {
  /// {엔티티} 목록을 조회합니다.
  static Future<{Entity}ListResponse> get{Entity}s(
    Session session, {
    required int limit,
    required int offset,
    {Entity}Category? category,
  }) async {
    try {
      final entities = await {Entity}.db.find(
        session,
        where: (t) {
          var condition = t.isDeleted.equals(false);
          if (category != null) {
            condition = condition & t.category.equals(category);
          }
          return condition;
        },
        orderBy: (t) => t.createdAt,
        orderDescending: true,
        limit: limit,
        offset: offset,
      );

      final total = await {Entity}.db.count(session, where: ...);

      return {Entity}ListResponse(
        items: entities,
        total: total,
        hasMore: offset + entities.length < total,
      );
    } on Exception catch (error, stackTrace) {
      session.log(
        '{Feature} 목록 조회 실패: $error',
        exception: error,
        level: LogLevel.error,
        stackTrace: stackTrace,
      );
      rethrow;
    }
  }

  // ... 나머지 비즈니스 로직
}
```

## Output Files

```
backend/petmedi_server/lib/src/feature/{feature_name}/
├── endpoint/
│   ├── {feature_name}_endpoint.dart       # App 엔드포인트
│   └── {feature_name}_console_endpoint.dart  # Console 엔드포인트 (선택)
├── service/
│   └── {feature_name}_service.dart        # 비즈니스 로직
└── validation/
    └── {feature_name}_validator.dart      # 입력 검증 (선택)
```

## Post-Generation Commands

```bash
# 코드 생성 (엔드포인트 등록)
melos run backend:pod:generate
```

## MCP Integration

- **Serena**: 기존 엔드포인트 패턴 분석, 심볼 검색
- **Context7**: Serverpod 엔드포인트 문서 참조

## Examples

### 게시글 엔드포인트 생성

```
/serverpod:endpoint community Post --type both
```

### 채팅 엔드포인트 생성

```
/serverpod:endpoint chat Message --type app
  --methods "getMessages, sendMessage, markAsRead"
```

### 관리자 대시보드 엔드포인트 생성

```
/serverpod:endpoint dashboard Stats --type console
  --methods "getOverview, getUserStats, getContentStats"
```

## 참조 에이전트

상세 구현 규칙은 `~/.claude/commands/agents/serverpod-endpoint-agent.md` 참조

## 핵심 규칙 요약

1. **Import 순서 준수** (Serverpod → Protocol → Feature → Utils)
2. **AuthenticatedMixin 사용** (인증 필요 메서드)
3. **Console 엔드포인트에 권한 설정** (`requireLogin`, `requiredScopes`)
4. **Service에 비즈니스 로직 분리**
5. **에러 처리 및 로깅** (`session.log`)
6. **소프트 삭제 패턴 적용**

---
name: data-layer-agent
description: Clean Architecture Data Layer 전문가. Repository 구현, 캐싱, Drift DAO 작업 시 사용
invoke: /feature:data
aliases: ["/data:create", "/layer:data"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
skills: feature
---

# Data Layer Agent

> Clean Architecture Data Layer 구현 전문 에이전트

📚 **상세 패턴 참조**:
- [Repository 패턴](../../references/patterns/repository-patterns.md)
- [캐싱 패턴](../../references/patterns/caching-patterns.md)
- [의존성 그래프](../../references/DEPENDENCY_GRAPH.md)

---

## 역할

Repository 구현체, API Mixin (네임스페이스 import), Cache 전략, Local DB를 일관되게 생성합니다.

---

## 실행 조건

- `/feature:data` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션의 Step 4에서 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `location` | ❌ | `application`, `common`, `console` (기본: `application`) |
| `caching` | ❌ | `swr`, `cache-first`, `none` (기본: `swr`) |

---

## 생성 파일

```
feature/{location}/{feature_name}/lib/src/data/
├── repository/
│   ├── {feature}_repository.dart
│   ├── mixins/
│   │   └── {feature}_api_mixin.dart
│   └── repository.dart
├── cache/
│   └── {entity}_cache_repository.dart
└── local/
    ├── tables/
    │   └── {entity}_table.dart
    ├── dao/
    │   └── {entity}_dao.dart
    └── {feature}_database.dart
```

---

## 핵심 패턴 요약

### Repository 구현체
> 📚 상세: [Repository 패턴](../../references/patterns/repository-patterns.md)

- `@LazySingleton(as: IFeatureRepository)` 어노테이션
- Mixin 분리 패턴 권장 (네트워크 로직 재사용)

### API Mixin (네임스페이스 필수!)
```dart
import 'package:serverpod_service/serverpod_service.dart' as serverpod;

mixin FeatureApiMixin implements IFeatureRepository {
  serverpod.ServerpodClient get client;  // ✅ 네임스페이스로 충돌 방지
}
```

### 캐싱 전략 선택
> 📚 상세: [캐싱 패턴](../../references/patterns/caching-patterns.md)

| 패턴 | 선택 기준 |
|------|----------|
| **SWR** | 빈번한 업데이트, 실시간성 |
| **Cache-First** | 네트워크 최소화, 정적 데이터 |

---

## Critical Import 패턴

```dart
// Repository: dependencies만 사용
import 'package:dependencies/dependencies.dart';

// Mixin: 네임스페이스 필수!
import 'package:serverpod_service/serverpod_service.dart' as serverpod;

// Domain Entity (네임스페이스 없음)
PostCategory category = PostCategory.qna;

// API DTO (네임스페이스로 충돌 방지)
serverpod.PostCategory apiCategory = serverpod.PostCategory.qna;
```

---

## 체크리스트

- [ ] Repository: `@LazySingleton(as: Interface)` 어노테이션
- [ ] API Mixin: `as serverpod` 네임스페이스 import
- [ ] 양방향 DTO 변환: `_mapFromDto`, `_categoryToDto`
- [ ] 캐싱 전략: SWR 또는 Cache-First
- [ ] Drift: Table + DAO 생성
- [ ] 반환 타입: `Either<Failure, T>` 일관성

---

## 관련 문서

- [Repository 패턴 상세](../../references/patterns/repository-patterns.md)
- [캐싱 패턴](../../references/patterns/caching-patterns.md)
- [패턴 선택 가이드](../../references/DECISION_MATRIX.md)

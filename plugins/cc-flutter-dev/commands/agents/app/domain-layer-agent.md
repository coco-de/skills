---
name: domain-layer-agent
description: Clean Architecture Domain Layer 전문가. Entity, UseCase, Repository 인터페이스 작업 시 사용
invoke: /feature:domain
aliases: ["/domain:create", "/layer:domain"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
skills: feature
---

# Domain Layer Agent

> Clean Architecture Domain Layer 구현 전문 에이전트

📚 **상세 패턴 참조**:
- [UseCase 패턴](../../references/patterns/usecase-patterns.md)
- [Repository 패턴](../../references/patterns/repository-patterns.md)
- [의존성 그래프](../../references/DEPENDENCY_GRAPH.md)

---

## 역할

Entity, Repository Interface, UseCase, Failure/Exception을 일관되게 생성합니다.

---

## 실행 조건

- `/feature:domain` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션의 Step 3에서 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `location` | ❌ | `application`, `common`, `console` (기본: `application`) |
| `usecases` | ❌ | 생성할 UseCase 목록 (기본: CRUD 전체) |

---

## 생성 파일

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
│   ├── create_{entity}_usecase.dart
│   └── usecase.dart          # export
├── failure/
│   └── {feature}_failure_messages.dart
└── exception/
    └── {feature}_exception.dart
```

---

## 핵심 패턴 요약

### Entity
- `Equatable` 상속, `const` 생성자
- 필드 순서: ID → 필수 → 선택(nullable) → 메타(createdAt 등)

### Repository Interface
- `I` prefix 필수 (`IFeatureRepository`)
- 반환 타입: `Future<Either<Failure, T>>` 또는 `Stream<CacheFirstResult<T>>`

### UseCase 선택
> 📚 상세: [UseCase 패턴](../../references/patterns/usecase-patterns.md)
> ⚠️ **결론**: 항상 **직접 인스턴스화** 패턴 사용

| 패턴 | 권장 |
|------|------|
| **직접 인스턴스화** | ✅ 권장 - BLoC에 @injectable 불필요 |
| **생성자 주입** | ❌ 금지 - BLoC에 @injectable 필요 |

---

## 금지 패턴

```dart
// ❌ 상대 경로 import 금지
import '../domain/entity/user.dart';

// ❌ Repository 직접 호출 (UseCase 우회) 금지
final result = await repository.getUser();

// ❌ 패턴 혼용 금지
// 프로젝트 내 일관성 유지 필수
```

---

## 체크리스트

### 공통 (필수)
- [ ] Entity: Equatable 상속 + const 생성자
- [ ] Repository: `I` prefix + `Either<Failure, T>` 반환
- [ ] UseCase 단위 테스트 작성
- [ ] 패키지 import만 사용

### UseCase 패턴
- ✅ **직접 인스턴스화**: `const` 생성자 + `get repo => getIt()`
- ❌ **생성자 주입 금지**: BLoC에 `@injectable` 사용 불가

---

## 관련 문서

- [UseCase 패턴 상세](../../references/patterns/usecase-patterns.md)
- [Repository 패턴](../../references/patterns/repository-patterns.md)
- [패턴 선택 가이드](../../references/DECISION_MATRIX.md)

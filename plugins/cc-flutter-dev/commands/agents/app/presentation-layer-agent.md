---
name: presentation-layer-agent
description: Clean Architecture Presentation Layer 전문가. BLoC, Page, Widget, Route 작업 시 사용
invoke: /feature:presentation
aliases: ["/presentation:create", "/layer:presentation"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
skills: feature
---

# Presentation Layer Agent

> Clean Architecture Presentation Layer 구현 전문 에이전트

📚 **상세 패턴 참조**:
- [BLoC 패턴](../../references/patterns/bloc-patterns.md)
- [UseCase 패턴](../../references/patterns/usecase-patterns.md)
- [의존성 그래프](../../references/DEPENDENCY_GRAPH.md)

---

## 역할

BLoC (Event sealed class, State), Page/Widget, Route, 테스트, Widgetbook을 일관되게 생성합니다.

---

## 실행 조건

- `/feature:presentation` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션의 Step 5에서 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `location` | ❌ | `application`, `common`, `console` (기본: `application`) |
| `pages` | ❌ | 생성할 페이지 목록 |

---

## 생성 파일

```
feature/{location}/{feature_name}/lib/src/presentation/
├── bloc/
│   └── {feature}_list/
│       ├── {feature}_list_bloc.dart
│       ├── {feature}_list_event.dart
│       └── {feature}_list_state.dart
├── page/
│   └── {feature}_page.dart
├── widget/
│   └── {entity}_card.dart
└── route/
    └── {feature}_route.dart

# 테스트 파일
feature/{location}/{feature_name}/test/presentation/
├── bloc/{feature}_list_bloc_test.dart
└── page/{feature}_page_test.dart
```

---

## 핵심 패턴 요약

### BLoC Event/State
> 📚 상세: [BLoC 패턴](../../references/patterns/bloc-patterns.md)

- **Event**: `sealed class` + factory constructor + private 구현
- **State**: `sealed class` 또는 Freezed union type
- `isClosed` 체크: await 후 emit 전 필수!

### UseCase 통합 패턴 선택
> 📚 상세: [UseCase 패턴](../../references/patterns/usecase-patterns.md)

| 패턴 | 선택 기준 |
|------|----------|
| **직접 인스턴스화** | DI 최소화, 단순 UseCase |
| **생성자 주입** | 테스트 빈번, 복잡한 의존성 |

### Widget 생성 규칙
```dart
const MyWidget({
  required this.data,
  this.onTap,
  super.key,  // ✅ 항상 마지막
});
```

### Route 패턴
```dart
@TypedGoRoute<FeatureRoute>(path: '/feature')
class FeatureRoute extends GoRouteData { ... }
```

---

## 금지 패턴

```dart
// ❌ Key? key 패턴 금지 (super.key 사용)
const MyWidget({Key? key, required this.data}) : super(key: key);

// ❌ 상대 경로 import 금지
import '../domain/entity/user.dart';

// ❌ BLoC에서 Repository 직접 접근 금지 (UseCase 통해서만)
class MyBloc {
  final IRepository _repository;  // UseCase 우회!
}
```

---

## 체크리스트

### 공통 (필수)
- [ ] Event: sealed class + factory + private 구현 패턴
- [ ] State: sealed class 또는 Freezed union
- [ ] BLoC: `if (isClosed) return;` 체크 (await 후 필수)
- [ ] Page: BlocProvider 래핑
- [ ] Widget: `super.key` 마지막 위치
- [ ] Route: @TypedGoRoute 어노테이션
- [ ] package import만 사용 (상대 경로 금지)

### 테스트
- [ ] BLoC Test 작성
- [ ] Widget Test 작성
- [ ] Widgetbook UseCase 작성

### UseCase 패턴별
- **직접 인스턴스화**: `const UseCase().call()` + GetIt 모킹 테스트
- **생성자 주입**: `@injectable` BLoC + Mock UseCase 직접 주입

---

## 관련 문서

- [BLoC 패턴 상세](../../references/patterns/bloc-patterns.md)
- [UseCase 패턴](../../references/patterns/usecase-patterns.md)
- [패턴 선택 가이드](../../references/DECISION_MATRIX.md)
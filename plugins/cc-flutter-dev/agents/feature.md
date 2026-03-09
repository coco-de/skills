---
name: feature
description: Clean Architecture Feature 모듈 생성 전문가
invoke: /feature:create
aliases: ["@feature"]
tools: Read, Edit, Write, Bash, Glob, Grep
model: inherit
---

# Feature Agent

Clean Architecture 기반 Feature 모듈을 생성하는 전문 에이전트입니다.

## 트리거

- `/feature:create` 또는 `@feature`
- 기능, 모듈, feature 키워드
- Clean Architecture, 도메인/데이터/프레젠테이션 레이어

## Feature 구조

```
feature/{category}/{feature_name}/lib/src/
├── di/injection.dart           # DI 설정
├── route/{feature}_route.dart  # 라우트 정의
├── domain/
│   ├── entity/                 # 비즈니스 엔티티
│   ├── repository/             # I{Feature}Repository
│   ├── usecase/                # 유스케이스
│   └── failure/                # 도메인 실패
├── data/
│   ├── repository/             # 리포지토리 구현
│   │   └── mixins/             # Serverpod 믹스인
│   ├── cache/                  # 캐시 전략
│   └── local/                  # Drift 로컬 DB
└── presentation/
    ├── page/                   # 페이지 위젯
    ├── widget/                 # 재사용 위젯
    └── bloc/                   # 상태 관리
```

## 핵심 패턴 레퍼런스

| 레이어 | 패턴 문서 |
|--------|----------|
| **UseCase** | → `references/patterns/usecase-patterns.md` |
| **BLoC** | → `references/patterns/bloc-patterns.md` |
| **Repository** | → `references/patterns/repository-patterns.md` |
| **Caching** | → `references/patterns/caching-patterns.md` |

## 패턴 선택 가이드

→ 상세: `references/DECISION_MATRIX.md`

| 영역 | 권장 패턴 |
|------|----------|
| Entity | Freezed (copyWith, equality 자동) |
| UseCase | 생성자 주입 (테스트 용이) |
| Repository | Mixin 패턴 (로직 재사용) |
| Caching | SWR (실시간) / Cache-First (정적) |

## 워크플로우

→ 상세: `references/DEPENDENCY_GRAPH.md`

```
/feature:create
├─► /serverpod:model → /serverpod:endpoint
├─► /feature:domain (Entity, UseCase)
├─► /feature:data (Repository, Cache)
└─► /feature:presentation (BLoC, Page, Widget)
```

## 체크리스트

- [ ] Entity 정의 (Freezed)
- [ ] Repository Interface (I prefix)
- [ ] UseCase 구현
- [ ] Repository 구현 (Mixin)
- [ ] BLoC 구현
- [ ] Page/Widget 구현
- [ ] Route 설정 & DI 등록
- [ ] 테스트 작성

## 명령어

```bash
# 코드 생성
melos run build

# 테스트
melos exec --scope=feature_{name} -- "flutter test"
```

## 관련 호출

- `/feature:domain` - Domain Layer
- `/feature:data` - Data Layer
- `/feature:presentation` - Presentation Layer
- `/coui:component` - UI 컴포넌트
- `/bdd:generate` - BDD 테스트

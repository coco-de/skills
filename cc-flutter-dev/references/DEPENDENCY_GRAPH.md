# 에이전트 의존성 그래프

> **참조 위치**: `.claude/references/DEPENDENCY_GRAPH.md`

에이전트, 스킬, 커맨드 간의 워크플로우와 의존성을 시각화합니다.

---

## Feature 생성 워크플로우

전체 Feature 모듈 생성 시 에이전트 호출 순서:

```
/feature:create
│
├─► /serverpod:model ──────────► /serverpod:endpoint
│   (모델 정의)                   (API 엔드포인트)
│
├─► /feature:domain
│   │   └─► usecase-patterns.md 참조
│   │
│   ├─ Entity 정의 (Freezed)
│   ├─ Repository Interface (I prefix)
│   ├─ UseCase 구현
│   └─ Failure/Exception 정의
│
├─► /feature:data
│   │   └─► repository-patterns.md, caching-patterns.md 참조
│   │
│   ├─ Repository 구현체
│   ├─ Serverpod Mixin
│   ├─ Cache 전략 (SWR/Cache-First)
│   └─ Drift DAO
│
└─► /feature:presentation
    │   └─► bloc-patterns.md 참조
    │
    ├─ BLoC 구현
    ├─ Page/Widget
    ├─► /coui:component (UI 컴포넌트)
    └─► /bdd:generate (테스트 시나리오)
```

---

## 백엔드 개발 워크플로우

Serverpod 백엔드 개발 시 에이전트 호출 순서:

```
/serverpod:model
│   (모델 .spy.yaml 정의)
│
└─► /serverpod:endpoint
    │   (Endpoint 클래스 생성)
    │
    ├─ CRUD 메서드 구현
    ├─ 인증/권한 처리
    └─ 비즈니스 로직
```

---

## UI 개발 워크플로우

```
/coui:component
│   (단일 컴포넌트)
│
├─► /coui:form ────────► 폼 컴포넌트 생성
│
├─► /coui:screen ──────► 전체 화면 구성
│
└─► /coui:improve ─────► 기존 UI 개선
```

---

## 테스트 워크플로우

```
/bdd:generate
│   (BDD 시나리오 생성)
│
├─ Feature 파일 (.feature)
├─ Step Definition
└─ Widget Test 통합
```

---

## 디버깅 워크플로우

Flutter Inspector 에이전트 계층:

```
Flutter Inspector (Master)
│
├─► /inspector:ui ─────────► Widget Tree, Layout 분석
│
├─► /inspector:bloc ───────► State History, Event 추적
│
├─► /inspector:network ────► HTTP 요청/응답 로그
│
├─► /inspector:auth ───────► Token, Session 상태
│
├─► /inspector:nav ────────► Route Stack, Navigation 이력
│
├─► /inspector:log ────────► 앱 로그, 에러 추적
│
├─► /inspector:form ───────► 폼 상태, 유효성 검사
│
├─► /inspector:config ─────► 환경 설정, Feature Flags
│
└─► /inspector:image ──────► 이미지 캐시, 메모리 사용
```

---

## Figma → 구현 워크플로우

```
/figma:analyze
│   (Figma 프레임 분석)
│
├─► 요구사항 정의 추출
│
├─► /bdd:generate ─────────► BDD 시나리오 생성
│
├─► /zenhub:create-epic ───► ZenHub Epic/Story 생성
│
└─► /feature:create ───────► Feature 모듈 생성
        │
        └─► 전체 워크플로우 연결
```

---

## 패턴 레퍼런스 의존성

각 에이전트가 참조하는 패턴 문서:

```
patterns/
├── usecase-patterns.md
│   └─► /feature:domain, /feature:presentation
│
├── bloc-patterns.md
│   └─► /feature:presentation, /feature:bloc
│
├── repository-patterns.md
│   └─► /feature:data, /serverpod:endpoint
│
└── caching-patterns.md
    └─► /feature:data
```

---

## 호출 방식 매핑

| 레거시 호출 | 통일 호출 | 에이전트 |
|------------|----------|---------|
| `@feature` | `/feature:create` | Feature 전체 생성 |
| `@bloc` | `/feature:bloc` | BLoC 상태 관리 |
| `@serverpod` | `/serverpod:model` | 모델 정의 |
| `@test` | `/bdd:generate` | BDD 테스트 |
| `@flutter-ui` | `/coui:component` | UI 컴포넌트 |

---

## 병렬 실행 가능 작업

동시 실행 가능한 에이전트 조합:

```
┌─────────────────────────────────────────────────┐
│ 병렬 그룹 1: 레이어 독립 작업                      │
├─────────────────────────────────────────────────┤
│  /feature:domain ─┬─ /feature:data              │
│                   └─ /serverpod:model           │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 병렬 그룹 2: UI 컴포넌트                          │
├─────────────────────────────────────────────────┤
│  /coui:component ─┬─ /coui:form                 │
│                   └─ Widget 개별 생성             │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│ 병렬 그룹 3: 테스트 & 문서화                       │
├─────────────────────────────────────────────────┤
│  /bdd:generate ───┬─ /sc:document               │
│                   └─ /zenhub:create-epic        │
└─────────────────────────────────────────────────┘
```

---

## 순차 실행 필수 작업

의존성으로 인해 순차 실행해야 하는 작업:

```
/serverpod:model → /serverpod:endpoint
(모델 먼저 정의 → 엔드포인트에서 사용)

/feature:domain → /feature:data
(Repository Interface 정의 → 구현체 작성)

/feature:data → /feature:presentation
(Repository 완성 → BLoC에서 UseCase 사용)
```

---

## 참조하는 에이전트

- `/feature:*` - Feature 레이어 생성
- `/serverpod:*` - 백엔드 개발
- `/coui:*` - UI 컴포넌트
- `/bdd:generate` - 테스트 생성
- `/figma:analyze` - Figma 분석

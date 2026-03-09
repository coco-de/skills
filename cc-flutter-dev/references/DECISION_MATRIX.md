# 패턴 선택 가이드

> **참조 위치**: `.claude/references/DECISION_MATRIX.md`

상황에 따른 최적의 패턴 선택을 위한 의사결정 가이드입니다.

---

## UseCase 패턴 선택

> ⚠️ **결론**: 항상 **직접 인스턴스화** 패턴 사용

```
UseCase 사용? ─Yes→ 직접 인스턴스화 (UseCase().call())
             └No→ Repository 직접 접근 금지 (UseCase 통해서만!)
```

### 상세 비교

| 기준 | 직접 인스턴스화 | 생성자 주입 |
|------|---------------|-----------|
| **권장** | ✅ **권장** | ❌ 금지 |
| **DI 설정** | 설정 단순화 | @injectable 필요 (금지됨) |
| **테스트** | GetIt 모킹 | BLoC에 @injectable 필요 |

**선택 기준**:
- ✅ 직접 인스턴스화: BLoC에 `@injectable` 불필요, DI 설정 단순화
- ❌ 생성자 주입: BLoC에 `@injectable` 사용 금지

→ 상세: `patterns/usecase-patterns.md`

---

## BLoC State 패턴 선택

```
상태 분리 명확? ─Yes─► Freezed Union (권장)
               │
               └No─► 코드생성 회피? ─Yes─► Sealed Class
                                   │
                                   └No─► Single State
```

### 상세 비교

| 기준 | Freezed Union | Sealed Class | Single State |
|------|--------------|--------------|--------------|
| **코드 생성** | 필요 | 불필요 | 필요 |
| **상태 분리** | ✅ 명확 | ✅ 명확 | ⚠️ 덜 명확 |
| **copyWith** | ✅ 자동 | ⚠️ 수동 | ✅ 자동 |
| **패턴 매칭** | ✅ when/map | ✅ switch | ⚠️ 조건문 |
| **권장 상황** | 일반적 사용 | Dart 3.0+, 코드생성 회피 | 페이지네이션, 필터링 |

**선택 기준**:
- ✅ Freezed Union: Initial/Loading/Loaded/Error 명확한 분리
- ✅ Sealed Class: 코드 생성 없이 타입 안전
- ✅ Single State: 여러 상태 조합 (isLoading + items + hasMore)

→ 상세: `patterns/bloc-patterns.md`

---

## Repository 구현 패턴 선택

```
네트워크 로직 재사용 필요? ─Yes─► Mixin 패턴 (권장)
                         │
                         └No─► 여러 데이터소스 조합? ─Yes─► Mixin 패턴
                                                     │
                                                     └No─► 직접 구현
```

### 상세 비교

| 기준 | Mixin 패턴 | 직접 구현 |
|------|-----------|----------|
| **로직 재사용** | ✅ 용이 | ⚠️ 어려움 |
| **구조 복잡도** | ⚠️ 증가 | ✅ 단순 |
| **테스트** | ✅ Mixin 독립 테스트 | ⚠️ 전체 테스트 |
| **권장 상황** | 복잡한 API, 여러 데이터소스 | 단순 CRUD |

**선택 기준**:
- ✅ Mixin 패턴: API 로직 재사용, 캐싱 레이어 분리, 복잡한 데이터 처리
- ✅ 직접 구현: 단순 CRUD, 빠른 구현, 재사용 필요 없음

→ 상세: `patterns/repository-patterns.md`

---

## 캐싱 전략 선택

```
데이터 자주 변경? ─Yes─► SWR (Stale-While-Revalidate)
                 │
                 └No─► 오프라인 필요? ─Yes─► Cache-First
                                      │
                                      └No─► SWR
```

### 상세 비교

| 기준 | SWR | Cache-First |
|------|-----|-------------|
| **응답 속도** | ✅ 즉시 (캐시) + 갱신 | ✅ 즉시 (캐시) |
| **네트워크 사용** | ⚠️ 매번 호출 | ✅ 캐시 있으면 안 함 |
| **데이터 신선도** | ✅ 최신 | ⚠️ 캐시 만료 전까지 |
| **오프라인 지원** | ⚠️ 캐시 있을 때만 | ✅ 캐시 우선 |

**적합 케이스**:

| SWR | Cache-First |
|-----|-------------|
| 피드, 타임라인 | 사용자 프로필 |
| 채팅 메시지 | 앱 설정 |
| 알림 목록 | 카테고리 목록 |
| 실시간 상태 | 정적 콘텐츠 |

→ 상세: `patterns/caching-patterns.md`

---

## Entity 정의 패턴 선택

```
코드 생성 가능? ─Yes─► Freezed (권장)
              │
              └No─► Dart 3.0+? ─Yes─► Final Class
                              │
                              └No─► 일반 Class
```

### 상세 비교

| 기준 | Freezed | Final Class | 일반 Class |
|------|---------|-------------|-----------|
| **copyWith** | ✅ 자동 | ⚠️ 수동 | ⚠️ 수동 |
| **equality** | ✅ 자동 | ⚠️ 수동 | ⚠️ 수동 |
| **불변성** | ✅ 강제 | ✅ final 강제 | ⚠️ 선택 |
| **JSON 직렬화** | ✅ 자동 | ⚠️ 수동 | ⚠️ 수동 |

---

## UI 컴포넌트 선택

```
기존 컴포넌트 있음? ─Yes─► /coui:improve (개선)
                   │
                   └No─► 폼 컴포넌트? ─Yes─► /coui:form
                                      │
                                      └No─► 전체 화면? ─Yes─► /coui:screen
                                                        │
                                                        └No─► /coui:component
```

---

## 테스트 전략 선택

```
E2E 테스트? ─Yes─► /bdd:generate (BDD 시나리오)
           │
           └No─► BLoC 테스트? ─Yes─► bloc_test 패키지
                              │
                              └No─► 단위 테스트? ─Yes─► mocktail + flutter_test
```

---

## 에이전트 선택 가이드

### Feature 개발

| 상황 | 호출 | 설명 |
|------|------|------|
| 전체 Feature 생성 | `/feature:create` | Domain + Data + Presentation |
| Domain만 필요 | `/feature:domain` | Entity, UseCase, Repository Interface |
| Data만 필요 | `/feature:data` | Repository 구현, Cache, DAO |
| Presentation만 필요 | `/feature:presentation` | BLoC, Page, Widget |
| BLoC만 필요 | `/feature:bloc` | 상태 관리만 |

### 백엔드 개발

| 상황 | 호출 | 설명 |
|------|------|------|
| 새 모델 정의 | `/serverpod:model` | .spy.yaml 파일 생성 |
| Endpoint 생성 | `/serverpod:endpoint` | API 엔드포인트 |

### UI 개발

| 상황 | 호출 | 설명 |
|------|------|------|
| 단일 컴포넌트 | `/coui:component` | 버튼, 카드 등 |
| 폼 생성 | `/coui:form` | 입력 폼 전체 |
| 전체 화면 | `/coui:screen` | 페이지 구성 |
| 기존 UI 개선 | `/coui:improve` | 리팩토링, 스타일 개선 |

---

## 빠른 참조 체크리스트

### 새 Feature 시작 시

- [ ] `/serverpod:model` - 백엔드 모델 정의
- [ ] `/serverpod:endpoint` - API 엔드포인트
- [ ] `/feature:domain` - Entity, UseCase 정의
- [ ] `/feature:data` - Repository 구현
- [ ] `/feature:presentation` - BLoC, UI 구현
- [ ] `/bdd:generate` - 테스트 시나리오

### 패턴 선택 시

- [ ] UseCase → `patterns/usecase-patterns.md`
- [ ] BLoC State → `patterns/bloc-patterns.md`
- [ ] Repository → `patterns/repository-patterns.md`
- [ ] Caching → `patterns/caching-patterns.md`

### 워크플로우 확인 시

- [ ] Feature 생성 → `DEPENDENCY_GRAPH.md`
- [ ] 병렬 실행 → `DEPENDENCY_GRAPH.md#병렬-실행-가능-작업`

---

## 참조하는 에이전트

- 모든 `/feature:*` 에이전트
- `/serverpod:*` 에이전트
- `/coui:*` 에이전트

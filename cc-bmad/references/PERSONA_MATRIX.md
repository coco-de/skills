# Persona Responsibility Matrix

BMAD 프레임워크의 7개 페르소나별 책임 매트릭스입니다.

## 페르소나 × 페이즈 매트릭스

| 페르소나 | Analysis | Planning | Solutioning | Implementation |
|---------|----------|----------|-------------|----------------|
| Analyst | ✅ 주담당 | 지원 | - | - |
| Product Manager | - | ✅ 주담당 | - | - |
| Architect | - | - | ✅ 주담당 | 지원 |
| UX Designer | - | - | ✅ 주담당 | 지원 |
| Flutter Developer | - | - | - | ✅ 주담당 |
| Backend Developer | - | - | - | ✅ 주담당 |
| Scrum Master | - | - | - | ✅ 주담당 |

---

## 페르소나별 책임 상세

> **연결 에이전트 경로 규칙**:
> - `agents/xxx` → `.claude/agents/xxx.md`
> - `commands/agents/xxx` → `.claude/commands/agents/xxx.md`
> - `skills/xxx` → `.claude/skills/xxx/SKILL.md`

### Analyst (분석가)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | 요구사항 분석, **BDD Gherkin AC 정의**, 타당성 검토 |
| **검토 항목** | 요구사항 명확성, 스코프 적절성, **AC Gherkin 형식**, AC 완성도 |
| **산출물** | 분석된 요구사항, **BDD Gherkin AC 목록**, 화면 타입 식별 |
| **연결 에이전트** | `commands/agents/figma-analyzer-agent`, `commands/agents/bdd-scenario-agent` |
| **승인 기준** | 모든 검토 항목 PASS + AC @happy-path, @error-handling 각 1개 이상 |

### Product Manager (PM)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | 이슈 구조화, Story Point 산정, 우선순위 설정 |
| **검토 항목** | Epic/Story 구조, Story Point (1-8), 라벨링, 의존성 |
| **산출물** | 생성된 이슈, 라벨, Estimate, 의존성 관계 |
| **연결 에이전트** | `commands/agents/zenhub-integration-agent`, ZenHub MCP tools |
| **승인 기준** | 이슈 생성 + 모든 검토 항목 PASS |

### Architect (아키텍트)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | 아키텍처 설계, API 설계, 기술 선택 |
| **검토 항목** | Clean Architecture, DI 구조, API 설계, 보안 |
| **산출물** | 아키텍처 승인, 설계 피드백 |
| **연결 에이전트** | `skills/code-review` |
| **승인 기준** | 모든 필수 검토 항목 PASS |

### UX Designer (UX 디자이너)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | UI/UX 검토, 접근성 검토 |
| **검토 항목** | CoUI 준수, 레이아웃, 상호작용, 접근성(권장) |
| **산출물** | UX 승인, 디자인 피드백 |
| **연결 에이전트** | `agents/flutter-ui`, `commands/agents/shared/widgetbook-agent` |
| **승인 기준** | 필수 검토 항목 PASS (접근성은 권장) |

### Flutter Developer (Flutter 개발자)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | UI 구현, BLoC 상태 관리, 테스트 작성 |
| **검토 항목** | BLoC 패턴, **CoUI MCP 활용**, Widget 패턴, 라우팅, 국제화 |
| **산출물** | 완성된 프론트엔드 코드, 테스트 |
| **연결 에이전트** | `commands/agents/feature-orchestrator-agent`, `commands/agents/app/presentation-layer-agent` |
| **MCP 도구** | `mcp__coui-flutter__*` (search, generate, validate) |
| **승인 기준** | 린트 통과, 테스트 통과 |

### Backend Developer (백엔드 개발자)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | OpenAPI 클라이언트 연동, 데이터 매핑, API 통신 |
| **검토 항목** | Mapper 정의, API 에러 처리, Response 변환 |
| **산출물** | Mapper 클래스, Repository Mixin |
| **연결 에이전트** | `commands/agents/app/data-layer-agent` |
| **승인 기준** | 코드 생성 완료, 테스트 통과 |

### Scrum Master (스크럼 마스터)

| 책임 영역 | 상세 |
|----------|------|
| **주 책임** | 워크플로우 관리, 블로커 해결, 상태 동기화 |
| **검토 항목** | 단계 진행, 검증 게이트, Pipeline 상태, 블로커, **재시도 제한 (최대 3회)** |
| **산출물** | 워크플로우 완료, 머지 |
| **연결 에이전트** | `agents/sequential-workflow`, `commands/agents/workflow/issue-state-agent` |
| **승인 기준** | 모든 단계 완료, PR 머지 |

---

## 검토 항목 × 페르소나 매트릭스

### Analysis Phase

| 검토 항목 | Analyst |
|----------|---------|
| 요구사항 명확성 | ✅ 필수 |
| 스코프 적절성 | ✅ 필수 |
| AC 테스트 가능성 | ✅ 필수 |
| 의존성 분석 | ⚠️ 권장 |

### Planning Phase

| 검토 항목 | PM |
|----------|-----|
| Epic/Story 구조 | ✅ 필수 |
| Story Point | ✅ 필수 |
| 라벨링 | ✅ 필수 |
| 의존성 | ✅ 필수 |

### Solutioning Phase

| 검토 항목 | Architect | UX Designer |
|----------|-----------|-------------|
| Clean Architecture | ✅ 필수 | - |
| DI 구조 | ✅ 필수 | - |
| API 설계 | ⚠️ 조건부 | - |
| 보안 | ✅ 필수 | - |
| CoUI 준수 | - | ✅ 필수 |
| 레이아웃 | - | ✅ 필수 |
| 상호작용 | - | ✅ 필수 |
| 접근성 | - | ⚠️ 권장 |

### Implementation Phase

| 검토 항목 | Flutter Dev | Backend Dev | Scrum Master |
|----------|-------------|-------------|--------------|
| BLoC 패턴 | ✅ 필수 | - | - |
| CoUI 사용 | ✅ 필수 | - | - |
| Widget 패턴 | ✅ 필수 | - | - |
| 라우팅 | ✅ 필수 | - | - |
| 국제화 | ✅ 필수 | - | - |
| Mapper 정의 | - | ✅ 필수 | - |
| API 에러 처리 | - | ✅ 필수 | - |
| Response 변환 | - | ✅ 필수 | - |
| DioException 처리 | - | ✅ 필수 | - |
| 단계 진행 | - | - | ✅ 필수 |
| 게이트 검증 | - | - | ✅ 필수 |
| Pipeline 상태 | - | - | ✅ 필수 |
| 블로커 해결 | - | - | ✅ 필수 |

---

## 병렬 실행 가능 조합

### Solutioning Phase (항상 병렬)

```
Architect ──┬──→ 병렬 실행 ──→ 모두 PASS 시 진행
UX Designer ─┘
```

### Implementation Phase (조건부 병렬)

```
조건: Backend와 Frontend가 독립적인 경우

Backend Developer ──┬──→ 병렬 실행 ──→ 모두 완료 시 통합
Flutter Developer ──┘

조건: Backend 의존성이 있는 경우

Backend Developer ──→ 완료 ──→ Flutter Developer
```

---

## 에스컬레이션 경로

| 상황 | 1차 담당 | 2차 담당 | 에스컬레이션 |
|------|---------|---------|-------------|
| 요구사항 불명확 | Analyst | PM | 사용자 확인 |
| 아키텍처 충돌 | Architect | Flutter Dev | 팀 회의 |
| UI/UX 불일치 | UX Designer | Flutter Dev | 디자인 팀 확인 |
| 블로커 발생 | Scrum Master | PM | 관리자 에스컬레이션 |
| **게이트 3회 실패** | 해당 페르소나 | Scrum Master | **원인 분석 → 작업 분할/재정의** |

### 재시도 제한 에스컬레이션 ⚠️

게이트가 3회 연속 실패하면 자동으로 Scrum Master에게 에스컬레이션됩니다:

```
┌─────────────────────────────────────────────────────────────────┐
│  게이트 3회 실패 시 처리 절차                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. Scrum Master가 실패 원인 분석                               │
│  2. 근본 원인 파악:                                              │
│     - 요구사항 자체 문제 → Analyst와 재정의                     │
│     - 기술적 복잡도 → 작업 분할                                 │
│     - 외부 의존성 → 블로커 등록                                 │
│  3. 해결책 적용 후 재시작 (재시도 카운터 리셋)                   │
│                                                                 │
│  설정: bmad.json → feedback.maxRetries: 3                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 관련 문서

- `.claude/personas/` - 각 페르소나 상세 정의
- `.claude/orchestrators/bmad-orchestrator.md` - 오케스트레이터
- `.claude/orchestrators/phase-gates.md` - 게이트 정의

---
name: BMAD Orchestrator
description: BMAD 프레임워크 메인 오케스트레이터
version: 1.0.0
---

# BMAD Orchestrator

BMAD(Breakthrough Method for Agile AI-Driven Development) 프레임워크의 메인 오케스트레이터입니다.
7개 페르소나가 4개 페이즈를 거쳐 검토하고 워크플로우를 진행합니다.

## 아키텍처 개요

```
┌─────────────────────────────────────────────────────────────────┐
│                    BMAD Orchestrator                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐        │
│  │   Analysis   │ → │   Planning   │ → │ Solutioning  │ →      │
│  │    Phase     │   │    Phase     │   │    Phase     │        │
│  ├──────────────┤   ├──────────────┤   ├──────────────┤        │
│  │  🔍 Analyst  │   │  📝 PM       │   │  🏗️ Architect│        │
│  │              │   │              │   │  🎨 UX Desig.│        │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘        │
│         │                  │                  │                 │
│         ▼                  ▼                  ▼                 │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              Implementation Phase                     │      │
│  ├──────────────────────────────────────────────────────┤      │
│  │  🧑‍💻 Flutter Dev  │  🔧 Backend Dev  │  📋 Scrum Master│      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 페이즈 구조

### Phase 1: Analysis (분석)

| 항목 | 내용 |
|------|------|
| 담당 페르소나 | Analyst |
| 목적 | 요구사항 분석, AC 정의, 타당성 검토 |
| 입력 | 작업 내용 (텍스트) |
| 출력 | 분석된 요구사항, AC 목록 |
| 게이트 | 요구사항 명확성, 스코프 적절성, AC 테스트 가능성 |

### Phase 2: Planning (계획)

| 항목 | 내용 |
|------|------|
| 담당 페르소나 | Product Manager |
| 목적 | 이슈 구조화, Story Point 산정, 우선순위 설정 |
| 입력 | Phase 1 출력 |
| 출력 | 생성된 이슈, 라벨, 의존성 |
| 게이트 | Epic/Story 구조, Story Point, 라벨링, 의존성 |

### Phase 3: Solutioning (설계)

| 항목 | 내용 |
|------|------|
| 담당 페르소나 | Architect + UX Designer (병렬) |
| 목적 | 아키텍처 설계, UI/UX 검토 |
| 입력 | Phase 2 출력 |
| 출력 | 설계 문서, UI 가이드라인 |
| 게이트 | Clean Architecture, DI 구조, CoUI 준수, 접근성 |

### Phase 4: Implementation (구현)

| 항목 | 내용 |
|------|------|
| 담당 페르소나 | Flutter Dev + Backend Dev + Scrum Master |
| 목적 | 코드 구현, 테스트, PR 생성, 머지 |
| 입력 | Phase 3 출력 |
| 출력 | 완성된 코드, 테스트, PR |
| 게이트 | 린트 검증, 테스트 통과, 코드 리뷰 |

## 실행 흐름

### 전체 흐름

```
                    ┌─────────────────────┐
                    │   작업 내용 입력     │
                    └──────────┬──────────┘
                               ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 1: ANALYSIS                                               │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ Analyst 검토                                                 │ │
│ │ - 요구사항 명확성 ✅                                         │ │
│ │ - 스코프 적절성 ✅                                           │ │
│ │ - AC 테스트 가능성 ✅                                        │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                          GATE: PASS                             │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 2: PLANNING                                               │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ PM 검토                                                      │ │
│ │ - Epic/Story 구조 ✅                                         │ │
│ │ - Story Point ✅                                             │ │
│ │ - 라벨링 ✅                                                  │ │
│ │ - 의존성 ✅                                                  │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                          GATE: PASS                             │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 3: SOLUTIONING (병렬 실행)                                │
│ ┌─────────────────────────┐ ┌─────────────────────────┐        │
│ │ Architect 검토          │ │ UX Designer 검토        │        │
│ │ - Clean Architecture ✅ │ │ - CoUI 준수 ✅          │        │
│ │ - DI 구조 ✅            │ │ - 레이아웃 ✅           │        │
│ │ - API 설계 ✅           │ │ - 상호작용 ✅           │        │
│ └─────────────────────────┘ └─────────────────────────┘        │
│                          GATE: ALL PASS                         │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ Phase 4: IMPLEMENTATION                                         │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 병렬 작업 (독립적인 경우)                                    │ │
│ │ - Flutter Developer: UI 구현                                 │ │
│ │ - Backend Developer: API 구현                                │ │
│ │ - Scrum Master: 진행 관리                                    │ │
│ └─────────────────────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────────────────────┐ │
│ │ 순차 작업                                                    │ │
│ │ Step 4: 브랜치 생성 → Step 5: In Progress                   │ │
│ │ Step 6: BDD → Step 7: 구현 → Step 8: 테스트                 │ │
│ │ Step 8.5: 린트 검증 → Step 9: PR 생성                       │ │
│ │ Step 10: Review/QA → Step 11: 코드 리뷰                     │ │
│ │ Step 12: 머지 승인                                          │ │
│ └─────────────────────────────────────────────────────────────┘ │
│                          GATE: ALL PASS                         │
└─────────────────────────────┬───────────────────────────────────┘
                              ▼
                    ┌─────────────────────┐
                    │   워크플로우 완료    │
                    └─────────────────────┘
```

## 페이즈 게이트 처리

### 게이트 성공 시

```
Phase {N} Gate: ✅ PASSED

다음 페이즈로 진행합니다.
```

### 게이트 실패 시

```
Phase {N} Gate: ❌ FAILED

거부 사유:
- {사유 1}
- {사유 2}

필요한 조치:
1. {조치 1}
2. {조치 2}

⚠️ 다음 페이즈로 진행할 수 없습니다.
   조치 완료 후 해당 페르소나 재검토가 필요합니다.
```

## 병렬 실행 패턴

### Fan-out 패턴 (Phase 3)

```typescript
// Architect와 UX Designer 병렬 실행
const [architectResult, uxResult] = await Promise.all([
  Task({
    subagent_type: "architect-review",
    prompt: "아키텍처 검토 수행",
  }),
  Task({
    subagent_type: "ux-review",
    prompt: "UX 검토 수행",
  }),
]);

// 모든 결과가 PASS여야 다음 단계 진행
if (architectResult.status === "PASSED" && uxResult.status === "PASSED") {
  proceed();
} else {
  // 실패한 검토에 대한 피드백 루프
  handleFailedReviews([architectResult, uxResult]);
}
```

### 독립 작업 병렬화 (Phase 4)

```typescript
// Backend와 Frontend가 독립적인 경우 병렬 실행
if (isBackendIndependent(task)) {
  const [backendResult, frontendResult] = await Promise.all([
    Task({
      subagent_type: "backend-developer",
      prompt: "API 구현",
    }),
    Task({
      subagent_type: "flutter-developer",
      prompt: "Mock 기반 UI 구현",
    }),
  ]);
}
```

## 상태 관리

### 워크플로우 상태

```typescript
interface BMADState {
  currentPhase: "analysis" | "planning" | "solutioning" | "implementation";
  phases: {
    analysis: PhaseState;
    planning: PhaseState;
    solutioning: PhaseState;
    implementation: PhaseState;
  };
  issue?: IssueInfo;
  branch?: string;
  pr?: PRInfo;
}

interface PhaseState {
  status: "pending" | "in_progress" | "passed" | "failed";
  reviews: ReviewResult[];
  blockers: Blocker[];
}
```

### 상태 전이

```
pending → in_progress → passed
                     ↘ failed → (수정) → in_progress
```

## 명령어 인터페이스

### 전체 워크플로우 시작

```bash
# BMAD 워크플로우 시작
/bmad "작업 내용"

# 기존 workflow와 통합
/workflow --bmad "작업 내용"
```

### 개별 페르소나 검토

```bash
# 특정 페르소나 검토만 실행
/bmad:review --persona analyst "검토 대상"
/bmad:review --persona architect "현재 PR 검토"
```

### 상태 확인

```bash
# 전체 상태 확인
/bmad:status

# 특정 페이즈 상태
/bmad:status --phase solutioning
```

### 게이트 수동 검증

```bash
# 특정 게이트 수동 검증
/bmad:gate --phase analysis
```

## 설정

### settings.json 확장

```json
{
  "bmad": {
    "enabled": true,
    "strictGates": true,
    "parallelExecution": true,
    "phases": {
      "analysis": { "required": true },
      "planning": { "required": true },
      "solutioning": { "required": true },
      "implementation": { "required": true }
    },
    "personas": {
      "analyst": { "enabled": true },
      "product-manager": { "enabled": true },
      "architect": { "enabled": true },
      "flutter-developer": { "enabled": true },
      "backend-developer": { "enabled": true },
      "scrum-master": { "enabled": true },
      "ux-designer": { "enabled": true }
    }
  }
}
```

## 출력 형식

### 진행 상황 표시

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Workflow: "저자 목록 화면 추가"                           ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 1: ANALYSIS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✅         ║
║  ├── 🔍 Analyst 검토                                           ║
║  │   ├── ✅ 요구사항 명확성                                     ║
║  │   ├── ✅ 스코프 적절성                                       ║
║  │   └── ✅ AC 테스트 가능성                                    ║
║  └── 📋 결과: 승인 (AC 3개 확정)                                ║
║                                                                ║
║  Phase 2: PLANNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✅          ║
║  ├── 📝 PM 검토                                                ║
║  │   ├── ✅ Epic/Story 구조                                    ║
║  │   ├── ✅ Story Point: 5                                     ║
║  │   └── ✅ 의존성: 없음                                       ║
║  └── 📋 결과: Issue #1810 생성                                 ║
║                                                                ║
║  Phase 3: SOLUTIONING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🔄         ║
║  ├── 🏗️ Architect 검토 (병렬)                                  ║
║  │   ├── ✅ Clean Architecture                                 ║
║  │   ├── ✅ DI 구조                                            ║
║  │   └── 🔄 API 설계 검토 중...                                 ║
║  └── 🎨 UX Designer 검토 (병렬)                                ║
║      ├── ✅ CoUI 준수                                          ║
║      └── ⏳ 접근성 검토 대기                                    ║
║                                                                ║
║  Phase 4: IMPLEMENTATION ━━━━━━━━━━━━━━━━━━━━━━━━━━ ⏳         ║
║  └── 대기 중 (Phase 3 완료 후 진행)                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## 관련 파일

- `.claude/personas/` - 7개 페르소나 정의
- `.claude/orchestrators/phase-gates.md` - 페이즈 게이트 상세
- `.claude/skills/bmad/SKILL.md` - BMAD 스킬 정의
- `.claude/commands/bmad.md` - BMAD 커맨드 정의

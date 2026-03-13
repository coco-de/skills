---
name: bmad
description: BMAD 프레임워크 기반 워크플로우 실행
language: korean
context: fork
invocationControl: manual
invoke: /bmad
aliases: []
category: workflow
complexity: high
mcp-servers: [zenhub]
---

# BMAD Skill

BMAD(Breakthrough Method for Agile AI-Driven Development) 프레임워크를 사용하여 7개 페르소나가 검토하고 4개 페이즈를 거쳐 워크플로우를 진행합니다.

## Scope and Capabilities

### 핵심 기능

| 기능 | 설명 |
|------|------|
| 페르소나 검토 | 7개 전문 페르소나가 단계별 검토 |
| 페이즈 게이트 | 강제 게이트로 품질 보장 |
| 병렬 실행 | 독립 작업의 Fan-out 패턴 실행 |
| 피드백 루프 | 실패 시 수정 후 재검토 |

### 7개 페르소나

| 페르소나 | 페이즈 | 역할 |
|---------|--------|------|
| Analyst | Analysis | 요구사항 분석, **BDD Gherkin Acceptance Criteria 작성** |
| Product Manager | Planning | 이슈 구조화, Story Point |
| Architect | Solutioning | 아키텍처 설계 검토 |
| UX Designer | Solutioning | UI/UX 검토 |
| Flutter Developer | Implementation | 프론트엔드 구현 |
| Backend Developer | Implementation | 백엔드 구현 |
| Scrum Master | Implementation | 워크플로우 관리 |

### 4개 페이즈

```
Phase 1: Analysis     → 요구사항 분석, BDD Gherkin Acceptance Criteria 작성 ⭐
Phase 2: Planning     → 이슈 생성, Story Point 산정
Phase 3: Solutioning  → 아키텍처/UX 설계 검토 (병렬)
Phase 4: Implementation → 코드 구현, 테스트, PR, 머지
```

### Quick 모드 페이즈 (--quick)

```
Phase 1: Analysis     → 요구사항 분석 (간소화)
Phase 2: Planning     → ⏭️ 스킵 (이슈/브랜치 없음)
Phase 3: Solutioning  → 설계 검토 (간소화)
Phase 4: Implementation → 구현 + 커밋 + PR 생성 + 리뷰 + 개선 + 머지
```

## Quick Start

### 기본 사용

```bash
# BMAD 워크플로우 시작
/bmad "저자 목록 화면 추가"
```

### Quick 모드 (이슈/브랜치 없이 빠른 작업) ⚡

```bash
# 이슈/브랜치 생성 없이 바로 작업 → 커밋 → PR → 리뷰 → 머지
/bmad --quick "인증 토큰 검증 버그 수정"

# 작업 완료 후 PR만 생성하고 머지까지
/bmad --quick --pr-only
```

### 기존 workflow 통합

```bash
# --bmad 옵션으로 활성화
/workflow --bmad "저자 목록 화면 추가"
```

### 개별 페르소나 검토

```bash
# 특정 페르소나 검토만 실행
/bmad:review --persona architect "현재 PR 검토"
/bmad:review --persona analyst "요구사항 검토"
```

### 상태 확인

```bash
# 전체 상태 확인
/bmad:status

# 특정 페이즈 상태
/bmad:status --phase solutioning
```

### 게이트 검증

```bash
# 수동 게이트 검증
/bmad:gate --phase analysis
```

## 실행 흐름

### 전체 워크플로우

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Workflow                                                 ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 1: ANALYSIS                                             ║
║  ├── 🔍 Analyst 검토                                           ║
║  │   ├── 요구사항 분석                                         ║
║  │   ├── BDD Gherkin Acceptance Criteria 작성 ⭐                 ║
║  │   └── 타당성 검토                                           ║
║  └── Gate: 요구사항 명확성, 스코프 적절성, Acceptance Criteria Gherkin 형식     ║
║                                                                ║
║  Phase 2: PLANNING                                             ║
║  ├── 📝 PM 검토                                                ║
║  │   ├── Epic/Story 구조화                                     ║
║  │   ├── Story Point 산정                                      ║
║  │   └── 이슈 생성                                             ║
║  └── Gate: 구조, Point, 라벨링, 의존성                         ║
║                                                                ║
║  Phase 3: SOLUTIONING (병렬)                                   ║
║  ├── 🏗️ Architect 검토                                         ║
║  │   ├── Clean Architecture                                    ║
║  │   ├── DI 구조                                               ║
║  │   └── API 설계                                              ║
║  ├── 🎨 UX Designer 검토                                       ║
║  │   ├── CoUI 준수                                             ║
║  │   ├── 레이아웃                                              ║
║  │   └── 상호작용                                              ║
║  └── Gate: 모든 검토 통과                                      ║
║                                                                ║
║  Phase 4: IMPLEMENTATION                                       ║
║  ├── 🧑‍💻 Flutter Developer                                     ║
║  │   └── UI 구현                                               ║
║  ├── 🔧 Backend Developer                                      ║
║  │   └── API 구현                                              ║
║  ├── 📋 Scrum Master                                           ║
║  │   └── 진행 관리                                             ║
║  └── Gate: 린트, 테스트, 코드 리뷰                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 기존 워크플로우 매핑

| BMAD 페이즈 | 기존 15단계 |
|------------|------------|
| Analysis | Step 1 (작업 분석) |
| Planning | Step 2-3 (이슈 생성, Backlog) |
| Solutioning | Step 4-6 (브랜치, BDD) |
| Implementation | Step 7-12 (구현~머지) |

---

## Quick 모드 상세 (--quick) ⚡

이슈/브랜치 생성 없이 현재 브랜치에서 바로 작업하고, PR 생성부터 머지까지 자동화합니다.

### 실행 흐름

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Quick Mode                                               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 1: ANALYSIS (간소화)                                    ║
║  ├── 🔍 요구사항 분석                                          ║
║  └── Gate: 명확성 확인만                                       ║
║                                                                ║
║  Phase 2: PLANNING ⏭️ SKIP                                     ║
║  ├── 이슈 생성 없음                                            ║
║  └── 브랜치 생성 없음 (현재 브랜치 사용)                       ║
║                                                                ║
║  Phase 3: SOLUTIONING (간소화)                                 ║
║  ├── 🏗️ Architect 검토 (필요시)                                ║
║  └── Gate: 아키텍처 준수 확인                                  ║
║                                                                ║
║  Phase 4: IMPLEMENTATION + PR CYCLE                            ║
║  ├── 🧑‍💻 구현                                                   ║
║  ├── ✅ 린트/분석 통과                                         ║
║  ├── 📝 커밋                                                   ║
║  ├── 🔀 PR 생성                                                ║
║  ├── 🔍 코드 리뷰 (8개 카테고리)                               ║
║  ├── 🔧 리뷰 개선사항 반영                                     ║
║  ├── 📝 개선 커밋                                              ║
║  └── 🎉 머지                                                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### PR 사이클 상세

```
┌─────────────────────────────────────────────────────────────────┐
│  PR Cycle (자동화)                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1️⃣ PR 생성                                                    │
│     └── gh pr create --title "..." --body "..."                │
│                                                                 │
│  2️⃣ 코드 리뷰 (/code-review 스킬 활용)                         │
│     ├── 🏗️ 아키텍처                                            │
│     ├── 🧩 상태 관리                                            │
│     ├── 🔒 보안                                                 │
│     ├── ⚡ 성능                                                  │
│     ├── 🧪 테스트                                               │
│     ├── 📖 가독성                                               │
│     ├── 🌐 국제화                                               │
│     └── ♿ 접근성                                               │
│                                                                 │
│  3️⃣ 개선사항 반영                                              │
│     ├── 🔴 Critical → 필수 수정                                │
│     ├── 🟡 Improvements → 권장 수정                            │
│     └── 🟢 Suggestions → 선택적                                │
│                                                                 │
│  4️⃣ 개선 커밋                                                  │
│     └── git commit -m "fix: 🐛 코드 리뷰 반영"                 │
│                                                                 │
│  5️⃣ 머지                                                       │
│     └── gh pr merge --squash --delete-branch                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 옵션

| 옵션 | 설명 |
|------|------|
| `--quick` | Quick 모드 활성화 |
| `--pr-only` | 이미 커밋된 상태에서 PR 생성부터 시작 |
| `--no-merge` | 리뷰까지만 진행, 머지는 수동 |
| `--skip-review` | 리뷰 없이 바로 머지 (긴급 시) |

### 사용 예시

```bash
# 전체 Quick 워크플로우
/bmad --quick "인증 토큰 검증 버그 수정"

# 커밋 완료 후 PR만 생성하고 리뷰/머지
/bmad --quick --pr-only

# PR 생성 후 리뷰까지만 (머지는 수동)
/bmad --quick --pr-only --no-merge

# 긴급: 리뷰 없이 바로 머지
/bmad --quick --pr-only --skip-review
```

### Quick 모드 vs 일반 모드

| 항목 | 일반 모드 | Quick 모드 |
|------|----------|-----------|
| 이슈 생성 | ✅ ZenHub 이슈 생성 | ❌ 스킵 |
| 브랜치 생성 | ✅ feature/xxx 생성 | ❌ 현재 브랜치 사용 |
| 분석 | ✅ 전체 분석 + BDD Acceptance Criteria | ⚡ 간소화 |
| 설계 검토 | ✅ Architect + UX | ⚡ Architect만 |
| 구현 | ✅ | ✅ |
| 린트/테스트 | ✅ | ✅ |
| 커밋 | ✅ | ✅ |
| PR 생성 | ✅ | ✅ |
| 코드 리뷰 | ✅ | ✅ (자동) |
| 리뷰 반영 | 수동 | ✅ (자동) |
| 머지 | 수동 | ✅ (자동) |

---

## 옵션

### 전체 워크플로우 옵션

```bash
# 특정 게이트만 활성화
/bmad --gates analysis,planning "작업 내용"

# 긴급 모드 (게이트 간소화)
/bmad --emergency "긴급 수정"

# 병렬 실행 비활성화
/bmad --no-parallel "작업 내용"
```

### 페르소나별 옵션

```bash
# Architect만 재검토
/bmad:review --persona architect --retry

# 여러 페르소나 동시 검토
/bmad:review --persona architect,ux-designer "설계 검토"
```

## 페이즈 게이트

### 강제 게이트 정책

모든 게이트는 **강제**입니다:

```
❌ 게이트 실패 시:
   → 다음 페이즈 진행 불가
   → 피드백 반영 후 재검토 필수

✅ 게이트 통과 시:
   → 다음 페이즈 자동 진행
```

### 게이트별 검증 항목

| 게이트 | 필수 검증 항목 |
|--------|---------------|
| Analysis | 요구사항 명확성, 스코프 적절성, **Acceptance Criteria BDD Gherkin 형식**, Acceptance Criteria 완성도(happy-path + error-handling) |
| Planning | Epic/Story 구조, Story Point (1-8), 라벨링, 의존성 |
| Solutioning | Clean Architecture, DI, API 설계, CoUI 준수, 레이아웃, 상호작용 |
| Implementation | 브랜치 규칙, 린트 통과, 테스트 통과, 코드 리뷰 완료 |

## 피드백 루프

### 게이트 실패 시

```
╔════════════════════════════════════════════════════════════════╗
║  Phase 3 Gate: ❌ FAILED                                       ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  거부 사유:                                                    ║
║  - Architect: BLoC이 Repository를 직접 접근                    ║
║                                                                ║
║  필요한 조치:                                                  ║
║  1. GetBooksUseCase 생성                                       ║
║  2. BLoC에서 UseCase 의존성으로 변경                           ║
║                                                                ║
║  ⚠️ 조치 완료 후 재검토 필요:                                  ║
║     /bmad:review --persona architect --retry                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 재검토 요청

```bash
# 특정 페르소나 재검토
/bmad:review --persona architect --retry

# 전체 페이즈 재검토
/bmad:gate --phase solutioning --retry
```

## 병렬 실행

### Solutioning Phase (병렬)

Architect와 UX Designer가 동시에 검토합니다:

```typescript
// 💡 개념 설명용 의사 코드 (실제로는 Claude Task 도구 병렬 호출로 구현)
const [architectResult, uxResult] = await Promise.all([
  reviewArchitect(input),
  reviewUXDesigner(input),
]);
```

### Implementation Phase (조건부 병렬)

Backend와 Frontend가 독립적인 경우 병렬 실행:

```typescript
// 💡 개념 설명용 의사 코드 (실제로는 Claude Task 도구로 순차/병렬 실행 결정)
if (isIndependent(backend, frontend)) {
  await Promise.all([
    implementBackend(input),
    implementFrontend(input),  // Mock 기반
  ]);
} else {
  await implementBackend(input);
  await implementFrontend(input);  // 실제 API 사용
}
```

## 결과 형식

### 진행 상황

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Workflow: "저자 목록 화면 추가"                           ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 1: ANALYSIS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✅         ║
║  Phase 2: PLANNING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✅          ║
║  Phase 3: SOLUTIONING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 🔄         ║
║  Phase 4: IMPLEMENTATION ━━━━━━━━━━━━━━━━━━━━━━━━━━ ⏳         ║
║                                                                ║
║  현재: Architect 검토 중 (UX Designer 완료)                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 완료

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Workflow Complete: "저자 목록 화면 추가"                  ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Phase 1: ANALYSIS - 승인                                   ║
║  ✅ Phase 2: PLANNING - Issue #1810 생성                       ║
║  ✅ Phase 3: SOLUTIONING - 설계 승인                           ║
║  ✅ Phase 4: IMPLEMENTATION - PR #1815 머지됨                  ║
║                                                                ║
║  📊 Summary:                                                   ║
║     - 검토 통과: 7/7 페르소나                                  ║
║     - 게이트 통과: 4/4 페이즈                                  ║
║     - 재시도: 1회 (Architect)                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## 관련 커맨드

- `/bmad` - 전체 BMAD 워크플로우
- `/bmad:review` - 페르소나별 검토
- `/bmad:status` - 상태 확인
- `/bmad:gate` - 게이트 검증
- `/workflow --bmad` - 기존 workflow와 통합

## 긴급 모드 (Emergency)

프로덕션 장애 등 긴급 상황에서 게이트를 간소화할 수 있습니다.

### 승인 절차

```
1. /bmad --emergency "긴급 수정 내용" 실행
2. Claude가 AskUserQuestion으로 승인 요청:
   ┌─────────────────────────────────────────────────────────────┐
   │  ⚠️ 긴급 모드 승인 요청                                     │
   │                                                             │
   │  긴급 모드는 Analysis, Planning 게이트를 건너뜁니다.        │
   │  Implementation 게이트(린트, 테스트)는 여전히 필수입니다.   │
   │                                                             │
   │  승인하시겠습니까?                                          │
   │  [예, 승인합니다] [아니오, 일반 모드로 진행]               │
   └─────────────────────────────────────────────────────────────┘
3. 승인 시: 간소화된 워크플로우 진행
4. 거부 시: 일반 BMAD 워크플로우로 전환
5. 완료 후: 48시간 내 사후 리뷰 필수 (Architect + PM)
```

### 긴급 모드 제약

| 항목 | 우회 가능 | 필수 |
|------|----------|------|
| Analysis Gate | ✅ | ❌ |
| Planning Gate | ✅ | ❌ |
| Solutioning Gate | ⚠️ 간소화 | ❌ |
| Implementation Gate | ❌ | ✅ (린트, 테스트 필수) |
| 사후 리뷰 | - | ✅ (48시간 내) |

---

## Additional Resources

> 📚 상세 정보는 **REFERENCE.md**를 참조하세요.

| 문서 | 내용 |
|------|------|
| `.claude/skills/bmad/REFERENCE.md` | 페르소나 상세, 게이트 상세, MCP 도구, 설정 옵션 |
| `.claude/config/bmad.json` | BMAD 설정 파일 |
| `.claude/orchestrators/bmad-orchestrator.md` | 오케스트레이터 상세 |
| `.claude/orchestrators/phase-gates.md` | 게이트 정의 |
| `.claude/personas/` | 페르소나 정의 (7개 파일) |
| `.claude/references/PERSONA_MATRIX.md` | 페르소나 책임 매트릭스 |

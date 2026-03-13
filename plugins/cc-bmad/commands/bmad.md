---
name: bmad
description: "BMAD 프레임워크 기반 워크플로우 실행"
invoke: /bmad
aliases: []
category: workflow
complexity: high
mcp-servers: [zenhub]
---

# /bmad

> BMAD(Breakthrough Method for Agile AI-Driven Development) 프레임워크를 사용하여 7개 페르소나가 검토하고 워크플로우를 진행합니다.

---

## 필수 실행 프로토콜

> **중요**: BMAD 워크플로우는 4개 페이즈의 강제 게이트를 통과해야 합니다.

### 페이즈 실행 순서

```
Phase 1: ANALYSIS     → Analyst 검토
Phase 2: PLANNING     → PM 검토
Phase 3: SOLUTIONING  → Architect + UX Designer 검토 (병렬)
Phase 4: IMPLEMENTATION → Flutter/Backend Dev + Scrum Master
```

### 각 페이즈별 실행

#### Phase 1: Analysis

```typescript
// 💡 개념 설명용 의사 코드 (실제로는 Claude가 Analyst 페르소나로 검토 수행)
const analysisResult = await analyzeRequirements({
  input: workContent,
  checks: ["requirementClarity", "scopeAppropriateness", "acTestability"],
});

if (!analysisResult.pass) {
  // 피드백 제공 및 재검토 요청
  return requestRevision(analysisResult.feedback);
}
```

#### Phase 2: Planning

```typescript
// 💡 실제 MCP 도구 호출 예시 (Claude가 PM 페르소나로 실행)
const issue = await mcp__zenhub__createGitHubIssue({
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3",
  title: `${type}(${scope}): ${gitmoji} ${description}`,
  body: generateIssueBody(analysisResult),
  issueTypeId: issueTypeId,
  labels: [type, scope],
});

await mcp__zenhub__setIssueEstimate({
  issueId: issue.id,
  estimate: storyPoint,
});

await mcp__zenhub__moveIssueToPipeline({
  issueId: issue.graphqlId,
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODE",  // Product Backlog
});
```

#### Phase 3: Solutioning (병렬)

```typescript
// 💡 개념 설명용 의사 코드 (실제로는 Claude Task 도구 병렬 호출)
const [architectResult, uxResult] = await Promise.all([
  Task({
    subagent_type: "architect-review",
    prompt: `아키텍처 검토: ${issue.title}`,
  }),
  Task({
    subagent_type: "ux-designer-review",
    prompt: `UX 검토: ${issue.title}`,
  }),
]);

// 모든 검토 통과 필요
if (!architectResult.pass || !uxResult.pass) {
  return requestRevision(combineFeedback(architectResult, uxResult));
}
```

#### Phase 4: Implementation

```bash
# 기존 workflow Step 4-12 실행
# 브랜치 생성
git checkout development && git pull origin development
git checkout -b feature/issue-${issue.number}-${slug}

# In Progress 이동
mcp__zenhub__moveIssueToPipeline(...)

# 구현, 테스트, 린트, PR, 리뷰, 머지
# (기존 workflow 흐름과 동일)
```

---

## Triggers

- 새로운 기능/버그/리팩토링 작업 시작 시
- 페르소나별 검토가 필요한 복잡한 작업 시
- 품질 게이트가 필요한 중요 작업 시

## 사용법

### 기본 사용

```bash
# BMAD 워크플로우 시작
/bmad "저자 목록 화면 추가"
```

### 기존 workflow와 통합

```bash
# --bmad 옵션으로 활성화
/workflow --bmad "저자 목록 화면 추가"
```

### 특정 게이트만 활성화

```bash
# Analysis와 Planning 게이트만
/bmad --gates analysis,planning "간단한 작업"
```

### 긴급 모드

```bash
# 게이트 간소화 (사용자 승인 필요)
/bmad --emergency "프로덕션 긴급 수정"
```

**긴급 모드 승인 절차**:

```typescript
// Claude가 AskUserQuestion 도구로 명시적 승인 요청
AskUserQuestion({
  questions: [{
    header: "Emergency",
    question: "긴급 모드를 활성화하시겠습니까? 이는 Analysis/Planning 게이트를 간소화합니다.",
    options: [
      { label: "예, 승인합니다", description: "긴급 모드 활성화 (48시간 내 사후 리뷰 필수)" },
      { label: "아니오", description: "일반 모드로 진행" }
    ],
    multiSelect: false
  }]
});
```

1. **승인 요청**: Claude가 `AskUserQuestion` 도구로 명시적 승인 요청
2. **사용자 선택**: "예, 승인합니다" 선택 시에만 진행
3. **게이트 간소화**: Analysis, Planning 게이트 간소화 (완전 스킵 아님)
4. **필수 게이트**: Implementation 게이트는 항상 필수 (린트, 테스트)
5. **사후 리뷰**: 완료 후 48시간 내 사후 리뷰 필수 (`BMAD_020` 에러 코드 참조)

---

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `작업 내용` | ✅ | 작업에 대한 설명 | `"저자 목록 화면 추가"` |

---

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--gates` | 모든 게이트 | 특정 게이트만 활성화 |
| `--emergency` | false | 긴급 모드 (게이트 간소화) |
| `--no-parallel` | false | 병렬 실행 비활성화 |
| `--skip-persona` | - | 특정 페르소나 스킵 |

---

## 출력 형식

### 진행 상황

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Workflow: "저자 목록 화면 추가"                           ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 1: ANALYSIS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ✅         ║
║  ├── 🔍 Analyst 검토                                           ║
║  │   ├── ✅ 요구사항 명확성                                     ║
║  │   ├── ✅ 스코프 적절성                                       ║
║  │   └── ✅ Acceptance Criteria 테스트 가능성                    ║
║  └── 📋 결과: 승인 (Acceptance Criteria 3개 확정)               ║
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
║  │   └── 🔄 검토 중...                                         ║
║  └── 🎨 UX Designer 검토 (병렬)                                ║
║      └── ✅ 완료                                                ║
║                                                                ║
║  Phase 4: IMPLEMENTATION ━━━━━━━━━━━━━━━━━━━━━━━━━━ ⏳         ║
║  └── 대기 중                                                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 게이트 실패 시 (에러 코드 포함)

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Gate Failed: BMAD_003                                    ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 3: SOLUTIONING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ ❌         ║
║  ├── 🏗️ Architect 검토: ❌ FAILED                              ║
║  │   ├── ❌ DI 구조: BLoC이 Repository를 직접 접근              ║
║  │   ├── 📋 필요 조치: UseCase 생성 후 의존성 변경              ║
║  │   └── 🔄 재시도: 1/3                                        ║
║  └── 🎨 UX Designer 검토: ✅ PASSED                            ║
║                                                                ║
║  💡 해결: 피드백 반영 후 `/bmad:review --persona architect`    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 완료

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Workflow Complete: "저자 목록 화면 추가"                  ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 Issue: #1810 - 저자 목록 화면 추가                         ║
║  🔀 PR: #1815                                                  ║
║  🌿 Branch: feature/1810-author-list (deleted)                 ║
║                                                                ║
║  ✅ 페르소나 검토: 7/7 통과                                     ║
║  ✅ 게이트 통과: 4/4 페이즈                                     ║
║  ✅ 테스트: 25/25 통과                                         ║
║                                                                ║
║  🏁 Final State: CLOSED                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 자가 검증 체크리스트

| 페이즈 | 게이트 | 완료 |
|--------|--------|------|
| Analysis | 요구사항 명확성 | ⬜ |
| Analysis | 스코프 적절성 | ⬜ |
| Analysis | Acceptance Criteria 테스트 가능성 | ⬜ |
| Planning | Epic/Story 구조 | ⬜ |
| Planning | Story Point (1-8) | ⬜ |
| Planning | 라벨링 | ⬜ |
| Planning | 의존성 | ⬜ |
| Solutioning | Clean Architecture | ⬜ |
| Solutioning | DI 구조 | ⬜ |
| Solutioning | CoUI 준수 | ⬜ |
| Implementation | 브랜치 규칙 | ⬜ |
| Implementation | 린트 통과 | ⬜ |
| Implementation | 테스트 통과 | ⬜ |
| Implementation | 코드 리뷰 | ⬜ |

---

## 관련 커맨드

- `/bmad:review` - 페르소나별 검토
- `/bmad:status` - 상태 확인
- `/bmad:gate` - 게이트 검증
- `/workflow` - 기존 워크플로우 (BMAD 없이)
- `/workflow --bmad` - BMAD 통합 워크플로우

## 관련 문서

- `.claude/orchestrators/bmad-orchestrator.md` - 오케스트레이터
- `.claude/orchestrators/phase-gates.md` - 게이트 정의
- `.claude/personas/` - 페르소나 정의
- `.claude/skills/bmad/SKILL.md` - 스킬 상세

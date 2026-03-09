# BMAD Reference

BMAD 프레임워크의 상세 참조 문서입니다.

## 페르소나 상세

### Analyst (분석가)

**파일**: `.claude/personas/analyst.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Analysis |
| 역할 | 요구사항 분석, AC 정의, 타당성 검토 |
| 검토 항목 | 요구사항 명확성, 스코프 적절성, AC 테스트 가능성 |
| 연결 에이전트 | figma-analyzer-agent, bdd-scenario-agent |

### Product Manager (PM)

**파일**: `.claude/personas/product-manager.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Planning |
| 역할 | 이슈 구조화, Story Point 산정, 우선순위 설정 |
| 검토 항목 | Epic/Story 구조, Story Point (1-8), 라벨링, 의존성 |
| 연결 에이전트 | zenhub-integration-agent |

### Architect (아키텍트)

**파일**: `.claude/personas/architect.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Solutioning |
| 역할 | 아키텍처 설계, API 설계, 기술 선택 |
| 검토 항목 | Clean Architecture, DI 구조, API 설계, 보안 |
| 연결 에이전트 | code-review |

### UX Designer (UX 디자이너)

**파일**: `.claude/personas/ux-designer.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Solutioning |
| 역할 | UI/UX 검토, 접근성 검토 |
| 검토 항목 | CoUI 준수, 레이아웃, 상호작용, 접근성 |
| 연결 에이전트 | flutter-ui, widgetbook-agent |

### Flutter Developer (Flutter 개발자)

**파일**: `.claude/personas/flutter-developer.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Implementation |
| 역할 | UI 구현, BLoC 상태 관리, 테스트 작성 |
| 검토 항목 | BLoC 패턴, CoUI 사용, Widget 패턴, 라우팅, 국제화 |
| 연결 에이전트 | feature-orchestrator-agent, presentation-layer-agent |

### Backend Developer (백엔드 개발자)

**파일**: `.claude/personas/backend-developer.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Implementation |
| 역할 | OpenAPI 클라이언트 연동, 데이터 매핑 |
| 검토 항목 | Mapper 정의, API 통신, 에러 처리 |
| 연결 에이전트 | data-layer-agent |

### Scrum Master (스크럼 마스터)

**파일**: `.claude/personas/scrum-master.md`

| 항목 | 내용 |
|------|------|
| 페이즈 | Implementation |
| 역할 | 워크플로우 관리, 블로커 해결, 상태 동기화 |
| 검토 항목 | 단계 진행, 검증 게이트, Pipeline 상태, 블로커 |
| 연결 에이전트 | sequential-workflow, issue-state-agent |

---

## 게이트 상세

### Analysis Gate

```yaml
gate: analysis
persona: analyst
required_checks:
  - requirement_clarity:
      description: "요구사항이 구체적이고 측정 가능한가?"
      failure_action: "요구사항 재정의"
  - scope_appropriateness:
      description: "단일 이슈로 적절한 크기인가?"
      failure_action: "분할 또는 조정"
  - ac_testability:
      description: "AC가 자동 테스트 가능한가?"
      failure_action: "AC 수정"
```

### Planning Gate

```yaml
gate: planning
persona: product-manager
required_checks:
  - epic_story_structure:
      description: "적절한 계층 구조인가?"
      failure_action: "구조 재설계"
  - story_point:
      description: "1-8 SP 범위인가?"
      failure_action: "재산정 또는 분할"
      threshold:
        min: 1
        max: 8
        split_required: 13
  - labeling:
      description: "Type, Scope 라벨이 있는가?"
      required_labels: ["type", "scope"]
      failure_action: "라벨 추가"
  - dependencies:
      description: "블로커가 해결 가능한가?"
      failure_action: "의존성 해결"
```

### Solutioning Gate

```yaml
gate: solutioning
personas: [architect, ux-designer]
execution: parallel
required_checks:
  architect:
    - clean_architecture:
        description: "레이어 분리가 올바른가?"
        layers: [presentation, domain, data]
    - di_structure:
        description: "Injectable 등록이 완전한가?"
    - api_design:
        description: "네이밍/에러처리가 표준인가?"
        condition: "backend 변경 시"
    - security:
        description: "인증/인가가 적절한가?"
  ux_designer:
    - coui_compliance:
        description: "표준 컴포넌트 사용인가?"
    - layout:
        description: "일관된 간격/정렬인가?"
    - interaction:
        description: "로딩/에러/빈 상태 처리인가?"
    - accessibility:
        description: "WCAG 2.1 AA 기준인가?"
        required: false  # 권장
```

### Implementation Gate

```yaml
gate: implementation
personas: [flutter-developer, backend-developer, scrum-master]
sub_gates:
  - step_4_branch:
      description: "feature 브랜치인가?"
      pattern: "^(feature|fix|refactor|chore)/[0-9]+"
      blocked_branches: [development, main]
  - step_8_5_lint:
      description: "dart/dcm analyze 통과?"
      commands:
        - "dart format"
        - "dcm format"
        - "dart fix --apply"
        - "dart analyze --no-fatal-infos"
        - "dcm analyze --no-fatal-style"
  - step_9_pr:
      description: "PR 생성 조건 충족?"
      checks:
        - branch_format
        - issue_linked
        - commits_exist
        - lint_passed
```

---

## MCP 도구 참조

### ZenHub 도구

```javascript
// 이슈 생성
mcp__zenhub__createGitHubIssue({
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3",
  title: "{type}({scope}): {gitmoji} {한글 설명}",
  body: "## 요약\n{내용}",
  issueTypeId: "{issue_type_id}",
  labels: ["{type}", "{scope}"],
})

// Pipeline 이동
mcp__zenhub__moveIssueToPipeline({
  issueId: "{issue.graphqlId}",
  pipelineId: "{pipeline_id}",
})

// Story Point 설정
mcp__zenhub__setIssueEstimate({
  issueId: "{issue_id}",
  estimate: 5,
})

// 의존성 설정
mcp__zenhub__createBlockage({
  blockedIssueId: "{blocked_id}",
  blockingIssueId: "{blocking_id}",
})
```

### Pipeline ID 참조

```yaml
pipelines:
  icebox: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODA"
  product_backlog: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODE"
  sprint_backlog: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODI"
  in_progress: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODM"
  review_qa: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODQ"
  done: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODU"
```

---

## 설정 옵션

### 설정 파일 위치

BMAD 설정은 별도의 설정 파일에서 관리됩니다:

- **설정 파일**: `.claude/config/bmad.json`
- **스키마 파일**: `.claude/config/bmad-schema.json`

> ⚠️ Claude Code의 `settings.json`은 스키마 검증으로 커스텀 필드를 허용하지 않습니다.
> BMAD 설정은 반드시 `.claude/config/bmad.json`을 사용하세요.

### bmad.json 설정 예시

```json
{
  "version": "1.0.0",
  "enabled": true,
  "defaultMode": "optional",
  "gates": {
    "analysis": { "enabled": true, "mandatory": true },
    "planning": { "enabled": true, "mandatory": true },
    "solutioning": {
      "enabled": true,
      "mandatory": true,
      "parallelPersonas": ["architect", "ux-designer"]
    },
    "implementation": { "enabled": true, "mandatory": true }
  },
  "personas": {
    "analyst": { "enabled": true, "phase": "analysis" },
    "product-manager": { "enabled": true, "phase": "planning" },
    "architect": { "enabled": true, "phase": "solutioning" },
    "ux-designer": { "enabled": true, "phase": "solutioning" },
    "flutter-developer": { "enabled": true, "phase": "implementation" },
    "backend-developer": { "enabled": true, "phase": "implementation" },
    "scrum-master": { "enabled": true, "phase": "implementation" }
  },
  "emergency": {
    "allowBypass": true,
    "requireApproval": true
  },
  "parallelExecution": {
    "enabled": true,
    "maxConcurrency": 2
  }
}
```

### 옵션 설명

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `enabled` | `true` | BMAD 프레임워크 활성화 |
| `defaultMode` | `optional` | 기본 모드 (`optional`, `mandatory`, `disabled`) |
| `gates.{phase}.enabled` | `true` | 해당 게이트 활성화 |
| `gates.{phase}.mandatory` | `true` | 해당 게이트 필수 여부 |
| `gates.solutioning.parallelPersonas` | `["architect", "ux-designer"]` | 병렬 실행 페르소나 |
| `personas.{persona}.enabled` | `true` | 해당 페르소나 활성화 |
| `personas.{persona}.phase` | 해당 페이즈 | 페르소나가 담당하는 페이즈 |
| `personas.{persona}.linkedAgents` | 연결 에이전트 | 페르소나와 연결된 에이전트 목록 |
| `emergency.allowBypass` | `true` | 긴급 모드 게이트 우회 허용 |
| `emergency.requireApproval` | `true` | 긴급 모드 관리자 승인 필요 |
| `parallelExecution.enabled` | `true` | 병렬 실행 활성화 |
| `parallelExecution.maxConcurrency` | `2` | 최대 동시 실행 수 |
| `feedback.maxRetries` | `3` | 최대 재시도 횟수 |
| `feedback.autoFix.enabled` | `true` | 자동 수정 활성화 |

---

## Quick 모드 설정

### bmad.json Quick 모드 설정

```json
{
  "quickMode": {
    "enabled": true,
    "skipPhases": ["planning"],
    "simplifyPhases": ["analysis", "solutioning"],
    "prCycle": {
      "autoCreate": true,
      "autoReview": true,
      "autoFix": true,
      "autoMerge": true,
      "mergeMethod": "squash",
      "deleteSourceBranch": true
    },
    "review": {
      "categories": [
        "architecture",
        "state-management",
        "security",
        "performance",
        "testing",
        "readability",
        "i18n",
        "accessibility"
      ],
      "autoFixSeverity": ["critical", "improvements"],
      "skipSeverity": ["suggestions"]
    }
  }
}
```

### Quick 모드 옵션 상세

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `quickMode.enabled` | `true` | Quick 모드 활성화 |
| `quickMode.skipPhases` | `["planning"]` | 스킵할 페이즈 |
| `quickMode.simplifyPhases` | `["analysis", "solutioning"]` | 간소화할 페이즈 |
| `prCycle.autoCreate` | `true` | PR 자동 생성 |
| `prCycle.autoReview` | `true` | 코드 리뷰 자동 실행 |
| `prCycle.autoFix` | `true` | 리뷰 개선사항 자동 반영 |
| `prCycle.autoMerge` | `true` | 자동 머지 |
| `prCycle.mergeMethod` | `"squash"` | 머지 방식 (squash/merge/rebase) |
| `prCycle.deleteSourceBranch` | `true` | 머지 후 소스 브랜치 삭제 |
| `review.autoFixSeverity` | `["critical", "improvements"]` | 자동 수정할 심각도 |
| `review.skipSeverity` | `["suggestions"]` | 자동 수정 스킵할 심각도 |

---

## 에러 코드

| 코드 | 설명 | 해결 방법 |
|------|------|----------|
| `BMAD_001` | Analysis Gate 실패 | 요구사항 명확화 후 재검토 |
| `BMAD_002` | Planning Gate 실패 | 이슈 구조 수정 후 재검토 |
| `BMAD_003` | Solutioning Gate 실패 | 설계 수정 후 재검토 |
| `BMAD_004` | Implementation Gate 실패 | 코드 수정 후 재검토 |
| `BMAD_010` | 페르소나 비활성화 | 설정에서 페르소나 활성화 |
| `BMAD_011` | 병렬 실행 실패 | 순차 실행으로 전환 |
| `BMAD_020` | 긴급 모드 남용 | 관리자 승인 필요 |
| `BMAD_030` | Quick 모드 PR 생성 실패 | 브랜치/커밋 상태 확인 |
| `BMAD_031` | Quick 모드 리뷰 실패 | 코드 품질 개선 필요 |
| `BMAD_032` | Quick 모드 머지 실패 | 충돌 해결 필요 |

---

## 모범 사례

### Do (권장)

- ✅ 작업 시작 전 AC를 명확히 정의
- ✅ Story Point는 팀 합의에 따라 산정
- ✅ 병렬 가능한 작업은 병렬로 실행
- ✅ 게이트 실패 피드백을 꼼꼼히 확인
- ✅ 재검토 전 모든 피드백 반영

### Don't (금지)

- ❌ 게이트 강제 우회 시도
- ❌ 긴급 모드 남용
- ❌ 페르소나 검토 건너뛰기
- ❌ 피드백 무시하고 재검토 요청
- ❌ development/main 직접 커밋

---

## 관련 문서

- `.claude/config/bmad.json` - BMAD 설정 파일
- `.claude/config/bmad-schema.json` - BMAD 설정 스키마
- `.claude/orchestrators/bmad-orchestrator.md` - 오케스트레이터
- `.claude/orchestrators/phase-gates.md` - 게이트 정의
- `.claude/personas/` - 페르소나 정의
- `.claude/skills/workflow/SKILL.md` - 기존 워크플로우
- `.claude/references/PERSONA_MATRIX.md` - 페르소나 책임 매트릭스

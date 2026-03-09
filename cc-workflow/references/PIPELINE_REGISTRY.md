# ZenHub Pipeline Registry

> ZenHub 파이프라인 ID 중앙 관리 레지스트리

---

## Good Teacher Workspace Pipelines

| Pipeline | GraphQL ID | 용도 |
|----------|------------|------|
| **New Issues** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyNzk` | 신규 이슈 |
| **Icebox** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODA` | 보류/미결정 |
| **Product Backlog** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODE` | 제품 백로그 |
| **Sprint Backlog** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODI` | 스프린트 백로그 |
| **In Progress** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODM` | 작업 중 |
| **Review/QA** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODQ` | 리뷰/QA |
| **Done** | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODU` | 완료 |

---

## Repository IDs

| Repository | GraphQL ID | 용도 |
|------------|------------|------|
| **good-teacher (GitHub)** | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3` | GitHub 이슈 생성 |
| **Unibook (ZenHub)** | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx` | ZenHub 전용 이슈 |

---

## Issue Type IDs

| Type | GraphQL ID | 용도 |
|------|------------|------|
| **Epic** | 조회 필요 | 대규모 기능 |
| **Story** | 조회 필요 | 사용자 스토리 |
| **Feature** | 조회 필요 | 기능 구현 |
| **Bug** | 조회 필요 | 버그 수정 |
| **Task** | 조회 필요 | 일반 작업 |

> Issue Type ID는 `mcp__zenhub__getIssueTypes({ repositoryId })` 로 조회하세요.

---

## 워크플로우별 파이프라인 전환

### 이슈 처리 워크플로우

```
New Issues → Product Backlog → Sprint Backlog → In Progress → Review/QA → Done
```

| 단계 | 트리거 | Pipeline |
|------|--------|----------|
| 이슈 생성 | 자동 | New Issues |
| 백로그 등록 | 트리아지 후 | Product Backlog |
| 스프린트 할당 | 스프린트 계획 | Sprint Backlog |
| **작업 시작** | 브랜치 생성 시 | **In Progress** |
| **리뷰 요청** | PR 생성 후 | **Review/QA** |
| **완료** | PR 머지 후 | **Done** |

### MCP 호출 예시

```javascript
// 작업 시작 시 (In Progress로 이동)
mcp__zenhub__moveIssueToPipeline({
  issueId: "{issue.graphqlId}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODM"
})

// PR 생성 후 (Review/QA로 이동)
mcp__zenhub__moveIssueToPipeline({
  issueId: "{issue.graphqlId}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODQ"
})

// PR 머지 후 (Done으로 이동)
mcp__zenhub__moveIssueToPipeline({
  issueId: "{issue.graphqlId}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODU"
})
```

---

## GitHub 이슈 생성 예시

```javascript
mcp__zenhub__createGitHubIssue({
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3",
  title: "feat(scope): 기능 제목",
  body: "## Summary\n...\n\n## Acceptance Criteria\n- [ ] ...",
  issueTypeId: "{issue_type_id}",
  labels: ["feature"],
})
```

---

## 참조하는 스킬/에이전트

이 레지스트리의 ID를 참조하는 파일들:

| 파일 | 용도 |
|------|------|
| `.claude/commands/workflow.md` | 전체 워크플로우 |
| `.claude/commands/workflow/issue-processor.md` | 이슈 순차 처리 |
| `.claude/commands/workflow/issue-cycle.md` | 단일 이슈 처리 |
| `.claude/commands/zenhub/sequential.md` | Epic 순차 처리 |
| `.claude/commands/agents/workflow/issue-state-agent.md` | 이슈 상태 관리 |
| `.claude/commands/agents/issue-processor-agent.md` | 이슈 처리 에이전트 |

---

## 주의사항

1. **ID 변경 시**: 이 파일만 수정하면 모든 스킬에서 참조 가능
2. **환경별 차이**: Production/Staging 동일 ID 사용
3. **ID 조회**: `mcp__zenhub__getWorkspacePipelinesAndRepositories()` 로 확인 가능

---

## 업데이트 이력

| 날짜 | 변경 내용 |
|------|----------|
| 2026-01-20 | 초기 생성 - 워크플로우 스킬 개선 PR #2014 |

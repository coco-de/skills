---
name: zenhub:workflow
description: "ZenHub PR 연결 및 파이프라인 상태 관리"
category: petmedi-workflow
complexity: simple
mcp-servers: [zenhub]
---

# /zenhub:workflow

> ZenHub 이슈와 PR 연결, 파이프라인 상태 관리를 위한 워크플로우 명령어

## Triggers

- PR 생성 후 이슈 연결이 필요할 때
- 파이프라인 상태 업데이트가 필요할 때
- 작업 진행 상태 변경 시

## Context Trigger Pattern

```bash
/zenhub:workflow {action} [--options]
```

## Actions

| Action | 설명 | 예시 |
|--------|------|------|
| `link-pr` | PR을 이슈에 연결 | `/zenhub:workflow link-pr --pr 1627 --issue 1413` |
| `move` | 이슈를 파이프라인으로 이동 | `/zenhub:workflow move --issue 1413 --to "Review/QA"` |
| `status` | 이슈/PR 상태 확인 | `/zenhub:workflow status --issue 1413` |

## Pipeline 목록

| Pipeline | ID | 용도 |
|----------|----|----|
| New Issues | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDM` | 검토/추정 대기 |
| Icebox | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDU` | 낮은 우선순위 |
| Product Backlog | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDY` | 검토/추정 완료 |
| Sprint Backlog | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDc` | Sprint 작업 대기 |
| In Progress | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDg` | 작업 중 |
| Review/QA | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk` | 코드 리뷰/QA |
| Done | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NTA` | 완료 |

## Workflow Patterns

### 1. 작업 시작 시

```bash
# 이슈를 In Progress로 이동
/zenhub:workflow move --issue {issue_number} --to "In Progress"
```

### 2. PR 생성 후

```bash
# PR 본문에 "Closes #{issue_number}" 포함 (GitHub 자동 연결)
# 이슈를 Review/QA로 이동
/zenhub:workflow move --issue {issue_number} --to "Review/QA"
```

### 3. 머지 후

```bash
# PR 본문의 "Closes #" 키워드로 자동 종료
# 필요시 수동으로 Done 이동
/zenhub:workflow move --issue {issue_number} --to "Done"
```

## PR 연결 Best Practices

### GitHub 자동 연결 키워드

PR 본문에 다음 키워드를 포함하면 GitHub에서 자동 연결:

```markdown
## 관련 이슈
- Closes #1413
- Fixes #1413
- Resolves #1413
```

### ZenHub 연결 제한사항

- PR은 ZenHub에서 이슈의 자식으로 설정 불가
- GitHub의 "Closes #" 키워드 활용 권장
- ZenHub에서는 파이프라인 이동으로 상태 관리

## MCP 도구 사용

### 이슈 검색

```javascript
mcp__zenhub__searchLatestIssues({ query: "1413" })
```

### 파이프라인 이동

```javascript
mcp__zenhub__moveIssueToPipeline({
  issueId: "Z2lkOi8vcmFwdG9yL0lzc3VlLzM4NTIyMjU2Mw",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk"
})
```

### 워크스페이스 정보 조회

```javascript
mcp__zenhub__getWorkspacePipelinesAndRepositories()
```

## Repository IDs

| Repository | ID |
|------------|-----|
| kobic (GitHub) | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTM0MjA0` |
| Unibook (ZenHub) | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx` |

## Issue Type IDs

이슈 생성/수정 시 `issueTypeId` 파라미터에 사용:

| Type | ID | Level | 용도 |
|------|-----|-------|------|
| Initiative | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3NzU` | 1 | 최상위 |
| Project | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3NzY` | 2 | 프로젝트 |
| **Epic** | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzc` | 3 | Epic |
| Bug | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzg` | 4 | 버그 |
| **Feature** | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3ODA` | 4 | Story |
| Task | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzk` | 4 | 작업 |
| **Sub-task** | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3ODE` | 5 | 하위작업 |

## Organization

| 항목 | 값 |
|------|-----|
| Organization ID | `Z2lkOi8vcmFwdG9yL1plbmh1Yk9yZ2FuaXphdGlvbi8xNTM3NzQ` |
| Organization Name | Cocode Inc. |

## 핵심 규칙

1. **PR 생성 시**: 본문에 `Closes #{issue}` 포함
2. **작업 시작**: In Progress로 이동
3. **리뷰 요청**: Review/QA로 이동
4. **머지 후**: Done으로 자동/수동 이동
5. **Epic 구조**: Epic > Story > Sub-task 계층 유지

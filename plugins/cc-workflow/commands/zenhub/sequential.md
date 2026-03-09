---
name: zenhub:sequential
description: "Epic 하위 이슈 순차 자동 처리 워크플로우"
category: petmedi-workflow
complexity: complex
mcp-servers: [zenhub]
---

# /zenhub:sequential

> Epic 하위 이슈들을 순차적으로 자동 처리하는 워크플로우

## Triggers

- Epic 단위 작업 시작 시
- 여러 이슈를 연속적으로 처리해야 할 때
- Sprint 내 이슈 일괄 처리 시

## 사용법

```bash
/zenhub:sequential {epic_number}
```

## 처리 사이클

```
┌──────────────────────────────────────────────────────────────┐
│  1. 다음 이슈 선택                                            │
│     └─ Epic 하위 이슈 중 New Issues 상태인 첫 번째 선택        │
│     └─ 우선순위: P2 > P3, 번호순                              │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  2. 작업 시작                                                 │
│     └─ moveIssueToPipeline → "In Progress"                   │
│     └─ git checkout -b feature/{issue}-{slug}                │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  3. 구현 작업                                                 │
│     └─ 이슈 요구사항 분석 (Acceptance Criteria)               │
│     └─ 코드 구현                                              │
│     └─ 테스트 작성 (필요시)                                   │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  4. PR 생성                                                   │
│     └─ git commit & push                                     │
│     └─ gh pr create --body "Closes #{issue}"                 │
│     └─ moveIssueToPipeline → "Review/QA"                     │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  5. 코드 리뷰 대응                                            │
│     └─ 리뷰 피드백 확인                                       │
│     └─ 수정 커밋 & 푸시                                       │
└──────────────────────┬───────────────────────────────────────┘
                       ↓
┌──────────────────────────────────────────────────────────────┐
│  6. 완료 & 다음 이슈                                          │
│     └─ PR 머지 시 자동 이슈 클로즈 (Closes # 키워드)          │
│     └─ git checkout development && git pull                  │
│     └─ Step 1로 돌아가기                                     │
└──────────────────────────────────────────────────────────────┘
```

## Pipeline IDs (Quick Reference)

| Pipeline | ID |
|----------|-----|
| New Issues | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDM` |
| In Progress | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDg` |
| Review/QA | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk` |
| Done | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NTA` |

## MCP 도구 사용

### 이슈 검색

```javascript
// Epic 하위 이슈 검색
mcp__zenhub__searchLatestIssues({ query: "SALES-001" })
```

### 파이프라인 이동

```javascript
// In Progress로 이동
mcp__zenhub__moveIssueToPipeline({
  issueId: "{issue_graphql_id}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDg"
})

// Review/QA로 이동
mcp__zenhub__moveIssueToPipeline({
  issueId: "{issue_graphql_id}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk"
})
```

## 브랜치 네이밍

```bash
feature/{issue_number}-{short-slug}

# 예시
feature/1415-sales-kpi-summary
feature/1418-sales-period-filter
```

## 커밋 메시지 형식

```
feat(console): ✨ {한글 설명} (#{issue_number})

{상세 설명}

Closes #{issue_number}
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## PR 본문 형식

```markdown
## Summary
- {변경 사항 요약 1}
- {변경 사항 요약 2}

## Related Issue
Closes #{issue_number}

## Test Plan
- [ ] {테스트 항목 1}
- [ ] {테스트 항목 2}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## 작업 순서 결정 기준

1. **Story 순서**: Story 번호 오름차순
2. **Priority 순서**: P2 (높음) > P3 (보통)
3. **Issue 번호 순서**: 작은 번호부터

## 중단 조건

- 코드 리뷰에서 major 이슈 발견 시
- 빌드 실패 시
- 테스트 실패 시
- 사용자가 명시적으로 중단 요청 시

## 관련 명령어

- `/zenhub:workflow` - 단일 이슈 워크플로우
- `/console:feature` - 콘솔 기능 패턴
- `/feature:create` - Feature 모듈 생성

---
name: workflow:issue-processor
description: "ZenHub 이슈 순차 처리 자동화"
category: petmedi-workflow
mcp-servers: [zenhub, sequential]
---

# /workflow:issue-processor

Epic/Story의 하위 이슈들을 순차적으로 처리합니다.

## 사용법
```
/workflow:issue-processor {epic_number}
```

## 워크플로우

### Per-Issue Cycle:
1. **시작**: Pipeline → "In Progress"로 이동
2. **구현**: 코드 작성 및 테스트
3. **리뷰**: Pipeline → "Review/QA"로 이동, PR 생성
4. **완료**: 코드 리뷰 반영 후 이슈 Close
5. **반복**: 다음 이슈로 이동

### MCP 호출 순서:
- `getWorkspacePipelinesAndRepositories` - 파이프라인 ID 조회
- `searchLatestIssues` - Epic 하위 이슈 조회
- `moveIssueToPipeline` - 파이프라인 이동
- `gh pr create` - PR 생성 및 이슈 연결
- `updateIssue` - 이슈 상태 업데이트

## Pipeline IDs (Unibook Workspace)

| Pipeline | ID |
|----------|-----|
| New Issues | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDM` |
| In Progress | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDg` |
| Review/QA | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk` |
| ~~Done~~ | ~~`Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NTA`~~ (사용하지 않음) |

## 이슈 처리 플로우

```
┌─────────────────────────────────────────────────────────┐
│  Issue Processing Flow                                  │
├─────────────────────────────────────────────────────────┤
│  1. Pipeline: New Issues → In Progress                  │
│  2. Branch: feature/issue-{number}-{short-desc}         │
│  3. Implement & Commit                                  │
│  4. Pipeline: In Progress → Review/QA                   │
│  5. Create PR (Closes #{number})                        │
│  6. Code Review & Fix                                   │
│  7. Squash Merge PR                                     │
│  8. Close Issue                                         │
│  9. Next Issue...                                       │
└─────────────────────────────────────────────────────────┘
```

## PR 생성 템플릿

```bash
gh pr create --title "{issue.title}" --body "$(cat <<'EOF'
## Summary
- {변경사항 요약}

## Related Issue
- Closes #{issue.number}

## Test Plan
- [ ] BDD 시나리오 검증
- [ ] 수동 테스트 완료

🤖 Generated with [Claude Code](https://claude.ai/claude-code)
EOF
)"
```

## 검증 체크리스트

- [ ] BDD 시나리오 vs 실제 구현 비교
- [ ] 코드 컨벤션 준수
- [ ] 테스트 작성 (필요시)
- [ ] Hot reload 후 UI 검증
- [ ] 에러 로그 확인

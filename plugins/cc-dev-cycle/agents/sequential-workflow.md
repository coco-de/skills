---
name: sequential-workflow
description: Epic 하위 이슈 순차 자동 처리 에이전트. 멈추지 않고 이슈 단위로 반복 처리
invoke: /zenhub:sequential
aliases: ["@sequential-workflow"]
tools: Read, Edit, Write, Bash, Glob, Grep, Task
mcp-servers: [zenhub]
model: inherit
---

# Sequential Workflow Agent

Epic 하위 이슈를 순차적으로 자동 처리하는 워크플로우 에이전트입니다.

## 트리거

- `/zenhub:sequential {epic_number}` 또는 `@sequential-workflow`
- Epic 단위 대량 작업 처리
- Sprint 이슈 일괄 처리

## 워크플로우 사이클

### Phase 1: 이슈 선택
```
1. Epic 하위 Story/Subtask 조회
2. New Issues 파이프라인에 있는 이슈 필터링
3. 우선순위 및 번호 순 정렬
4. 첫 번째 이슈 선택
```

### Phase 2: 작업 시작
```
1. 이슈를 "In Progress" 파이프라인으로 이동
2. 브랜치 생성: feature/{issue}-{slug}
3. 이슈 요구사항 분석 (title, body, acceptance criteria)
```

### Phase 3: 구현
```
1. 기존 코드베이스 분석
2. 요구사항에 맞는 코드 구현
3. 테스트 작성 (필요시)
4. 빌드 및 분석 통과 확인
```

### Phase 4: PR 생성
```
1. 변경사항 커밋 (Closes #{issue} 포함)
2. 브랜치 푸시
3. PR 생성 (gh pr create)
4. 이슈를 "Review/QA" 파이프라인으로 이동
```

### Phase 5: 코드 리뷰 대응
```
1. 리뷰 피드백 확인
2. 필요시 수정 커밋
3. 승인 대기
```

### Phase 6: 완료 및 다음 이슈
```
1. PR 머지 (자동 이슈 클로즈)
2. development 브랜치로 복귀
3. 최신 코드 pull
4. Phase 1으로 돌아가기
```

## ZenHub MCP 활용

### 이슈 검색
```javascript
// Epic 관련 이슈 검색
mcp__zenhub__searchLatestIssues({ query: "SALES-001" })

// 파이프라인별 이슈 조회
mcp__zenhub__getIssuesInPipeline({
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDM",
  repositoryIds: ["Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTM0MjA0"]
})
```

### 파이프라인 이동
```javascript
// In Progress
mcp__zenhub__moveIssueToPipeline({
  issueId: "{graphql_id}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDg"
})

// Review/QA
mcp__zenhub__moveIssueToPipeline({
  issueId: "{graphql_id}",
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk"
})
```

## Pipeline IDs

| Pipeline | ID | 용도 |
|----------|-----|------|
| New Issues | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDM` | 대기 중 |
| In Progress | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDg` | 작업 중 |
| Review/QA | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NDk` | 리뷰 중 |
| ~~Done~~ | ~~`Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0Mzk2NTA`~~ | 사용하지 않음 (머지 시 자동 Close) |

## Repository IDs

| Repository | ID |
|------------|-----|
| kobic (GitHub) | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTM0MjA0` |
| Unibook (ZenHub) | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx` |

## 브랜치 전략

```bash
# 이슈 작업 브랜치 생성
git checkout development
git pull origin development
git checkout -b feature/{issue_number}-{short-slug}

# 예시
git checkout -b feature/1415-sales-kpi-summary
```

## 커밋 규칙

```bash
# 한글 커밋 메시지 + Gitmoji
feat(console): ✨ 매출 KPI 요약 카드 구현 (#1415)

- 총 결제액 표시
- 총 판매량 표시
- 전월 대비 증감률 표시

Closes #1415
Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
```

## PR 생성 규칙

```bash
gh pr create \
  --base development \
  --title "feat(console): ✨ 매출 KPI 요약 카드 구현 (#1415)" \
  --body "$(cat <<'EOF'
## Summary
- 매출 KPI 요약 카드 컴포넌트 구현
- 총 결제액, 판매량 표시
- 전월 대비 증감률 계산

## Related Issue
Closes #1415

## Test Plan
- [ ] KPI 카드 렌더링 확인
- [ ] 데이터 바인딩 확인
- [ ] 증감률 계산 검증

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

## 중단 조건

워크플로우가 자동으로 중단되는 경우:

1. **빌드 실패**: `melos run analyze` 또는 `flutter build` 실패
2. **테스트 실패**: 단위 테스트 또는 위젯 테스트 실패
3. **코드 리뷰 이슈**: Major 수정 요청 발생
4. **사용자 요청**: 명시적 중단 요청

## 에러 복구

### 빌드 실패 시
```bash
# 에러 분석
melos run analyze 2>&1 | head -50

# 일반적인 수정
melos run format
melos run build
```

### 머지 충돌 시
```bash
git fetch origin development
git rebase origin/development
# 충돌 해결 후
git rebase --continue
```

## 체크리스트

각 이슈 처리 시 확인사항:

- [ ] 이슈 요구사항 파악
- [ ] 브랜치 생성
- [ ] 코드 구현
- [ ] 빌드/분석 통과
- [ ] 커밋 생성 (Closes # 포함)
- [ ] PR 생성
- [ ] 파이프라인 이동 (In Progress → Review/QA)
- [ ] 리뷰 피드백 대응
- [ ] 다음 이슈로 전환

## 관련 에이전트

- `@console-feature` - 콘솔 기능 패턴
- `@bloc` - BLoC 상태 관리
- `@flutter-ui` - UI 컴포넌트 구현
- `@test` - 테스트 작성

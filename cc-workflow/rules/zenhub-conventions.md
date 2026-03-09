# ZenHub 컨벤션

ZenHub를 사용한 이슈 관리 규칙입니다.

## 이슈 생성 규칙

### GitHub 이슈 사용 (필수)

**모든 이슈는 GitHub 이슈로 생성합니다** (ZenHub 이슈 사용 금지)

```javascript
// ✅ CORRECT: GitHub 이슈 생성
mcp__zenhub__createGitHubIssue({
  title: "[Epic] 기능 개발",
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3", // good-teacher
  issueTypeId: "...",
})

// ❌ WRONG: ZenHub 이슈 생성 (사용 금지)
mcp__zenhub__createZenhubIssue({...})
```

**이유**:
- GitHub 이슈는 파이프라인 이동 가능
- 타임라인 설정 정상 작동
- GitHub PR과 자동 연결
- 검색 및 필터링 용이

---

## Repository ID

| Repository | ID | 용도 |
|------------|-----|------|
| good-teacher (GitHub) | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3` | 모든 이슈 생성 |
| Good Teacher (ZenHub) | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NjcxNTM0` | 사용 금지 |

---

## Issue Type ID

| Type | ID | Level | 용도 |
|------|-----|-------|------|
| Initiative | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMDQ3MDQ` | 1 | 대규모 전략적 목표 |
| Project | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMDQ1NzM` | 2 | 프로젝트 단위 |
| Epic | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMDQ1ODg` | 3 | 대규모 기능 묶음 |
| Bug | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMTAyNzM` | 4 | 버그 수정 |
| Feature | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMDY1NDg` | 4 | 기능/Story |
| Task | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMTAyNzI` | 4 | 작업 |
| Sub-task | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMTAyNzQ` | 5 | 하위 작업 |

---

## Pipeline ID

| Pipeline | ID | 용도 |
|----------|-----|------|
| New Issues | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyNzk` | 새 이슈 (기본) |
| Icebox | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODA` | 보류 |
| Product Backlog | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODE` | 제품 백로그 |
| Sprint Backlog | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODI` | 스프린트 백로그 |
| In Progress | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODM` | 진행 중 |
| Review/QA | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODQ` | 리뷰/QA |
| Done | `Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODU` | 완료 |

---

## Organization ID

| Organization | ID |
|--------------|-----|
| Cocode Inc. | `Z2lkOi8vcmFwdG9yL1plbmh1Yk9yZ2FuaXphdGlvbi8xNTM3NzQ` |

---

## 이슈 생성 예시

### Epic 생성

```javascript
// 1. Epic 생성 (GitHub 이슈)
const epic = await mcp__zenhub__createGitHubIssue({
  title: "[Epic] 기능명",
  body: "Epic 설명...",
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3",
  issueTypeId: "Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMDQ1ODg", // Epic
});

// 2. 타임라인 설정
await mcp__zenhub__setDatesForIssue({
  issueId: epic.id,
  startDate: "2026-01-27",
  endDate: "2026-02-17",
  zenhubOrganizationId: "Z2lkOi8vcmFwdG9yL1plbmh1Yk9yZ2FuaXphdGlvbi8xNTM3NzQ",
});

// 3. 파이프라인 이동
await mcp__zenhub__moveIssueToPipeline({
  issueId: epic.id,
  pipelineId: "Z2lkOi8vcmFwdG9yL1BpcGVsaW5lLzM0OTkyODE", // Product Backlog
});
```

### Story 생성

```javascript
// Story 생성 (Epic 하위)
const story = await mcp__zenhub__createGitHubIssue({
  title: "[Story] 기능명",
  body: "Story 설명...",
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NzA5MTE3",
  issueTypeId: "Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8zMDY1NDg", // Feature
  parentIssueId: epic.id, // Epic과 연결
});

// Story Point 설정
await mcp__zenhub__setIssueEstimate({
  issueId: story.id,
  estimate: 5,
});
```

---

## 이슈 제목 컨벤션

| Type | 접두사 | 예시 |
|------|--------|------|
| Epic | `[Epic]` | `[Epic] API 연동 및 SWR 캐싱 전략 적용` |
| Story | `[Story]` | `[Story] classroom API 연동` |
| Bug | `fix:` | `fix: 로그인 토큰 갱신 오류` |
| Feature | `feat:` | `feat: 사용자 프로필 페이지 추가` |
| Task | `chore:` | `chore: 의존성 업데이트` |

---

## 참고 사항

1. **ZenHub 이슈 vs GitHub 이슈**
   - ZenHub 이슈: 파이프라인 이동/타임라인 설정 불가
   - GitHub 이슈: 모든 ZenHub 기능 정상 작동

2. **부모-자식 관계**
   - `parentIssueId` 파라미터로 생성 시 연결
   - 또는 `setParentForIssues`로 나중에 연결

3. **검색**
   - `searchLatestIssues`: GitHub 이슈만 검색됨
   - ZenHub 이슈는 검색 불가

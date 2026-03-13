# /workflow:bug-cycle

> 버그 수정 전체 사이클 자동화 (이슈 생성 → 브랜치 → 수정 → PR)

## 개요

이 워크플로우는 버그 이슈의 전체 수정 사이클을 자동화합니다:
1. 버그 리포트 생성 (옵션)
2. 브랜치 생성
3. 버그 수정 작업
4. PR 생성 및 머지

---

## 사용법

```bash
# 기존 버그 이슈로 시작
/workflow:bug-cycle {issue_number}

# 새 버그 리포트부터 시작
/workflow:bug-cycle --new [이미지_경로] "버그 설명"
```

### 파라미터

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `issue_number` | ✅* | 기존 버그 이슈 번호 |
| `--new` | ✅* | 새 버그 리포트 생성 모드 |
| `--no-merge` | ❌ | PR 생성까지만 (머지 제외) |
| `--skip-tests` | ❌ | 테스트 스킵 (긴급 핫픽스용) |
| `--base` | ❌ | 베이스 브랜치 (기본: development) |

*`issue_number` 또는 `--new` 중 하나 필수

### 옵션 예시

```bash
# PR까지만 (머지 제외)
/workflow:bug-cycle 123 --no-merge

# 테스트 스킵 (긴급)
/workflow:bug-cycle 123 --skip-tests

# 베이스 브랜치 변경
/workflow:bug-cycle 123 --base main

# 새 버그 + 이미지 분석
/workflow:bug-cycle --new /tmp/screenshot.png "앱 크래시 발생"
```

---

## 실행 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                    /workflow:bug-cycle                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: 버그 리포트 생성 (--new 옵션 시)                        │
│  ├── /bug-report 호출 (이미지 분석)                              │
│  ├── ZenHub 이슈 생성                                           │
│  └── 결과: issue_number 획득                                    │
│                                                                 │
│  Step 2: 이슈 정보 조회                                          │
│  ├── mcp__zenhub__searchLatestIssues                           │
│  ├── 이슈 타입, 제목, 본문 추출                                  │
│  └── 버그 원인 분석                                              │
│                                                                 │
│  Step 3: 브랜치 생성                                             │
│  ├── fix/{number}-{slug} 형식                                   │
│  ├── issue-state-agent → "In Progress"                         │
│  └── development 브랜치 기반                                    │
│                                                                 │
│  Step 4: 버그 수정 작업                                          │
│  ├── 이슈 본문 분석 → 원인 파악                                  │
│  ├── 관련 코드 탐색                                              │
│  ├── 코드 수정                                                   │
│  └── 증분 커밋 생성                                              │
│                                                                 │
│  Step 5: 테스트 실행                                             │
│  ├── 관련 테스트 실행                                            │
│  ├── 실패 시 자동 수정 시도                                      │
│  └── 테스트 추가 (필요시)                                        │
│                                                                 │
│  Step 6: PR 생성                                                 │
│  ├── gh pr create                                               │
│  ├── issue-state-agent → "Review"                              │
│  └── 이슈 자동 연결 (Closes #{number})                          │
│                                                                 │
│  Step 7: 머지 (--no-merge 없을 시)                               │
│  ├── 리뷰 대기                                                   │
│  ├── 스쿼시 머지                                                 │
│  └── GitHub "Closes #" 키워드로 이슈 자동 Close                  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 상세 구현

### Step 1: 버그 리포트 생성 (옵션)

`--new` 옵션이 주어진 경우:

```typescript
// /bug-report 스킬 호출
const bugReport = await Skill({
  skill: "bug-report",
  args: `${imagePath} "${description}"`
});

// 생성된 이슈 번호 추출
const issueNumber = bugReport.issue_number;
```

### Step 2: 이슈 정보 조회

```typescript
// 이슈 정보 조회
const issueResult = await mcp__zenhub__searchLatestIssues({
  query: issue_number.toString()
});

const issue = issueResult.find(i => i.number === issue_number);

// 버그 정보 추출
const bugInfo = {
  id: issue.id,
  number: issue.number,
  title: issue.title,
  body: issue.body,           // 재현 단계, 예상/실제 결과 포함
  severity: extractSeverity(issue.labels),
  area: extractArea(issue.labels),
};
```

### Step 3: 브랜치 생성

```typescript
// 브랜치명 생성: fix/{number}-{slug}
const slug = createSlug(bugInfo.title);
const branchName = `fix/${bugInfo.number}-${slug}`;

// 브랜치 생성
await Bash(`git checkout -b ${branchName} origin/development`);

// Pipeline 이동: In Progress
await mcp__zenhub__moveIssueToPipeline({
  issueId: bugInfo.id,
  pipelineId: inProgressPipelineId
});
```

### Step 4: 버그 수정 작업

```typescript
// 버그 원인 분석
// 1. 이슈 본문에서 재현 단계 파악
// 2. 관련 코드 탐색 (Grep, Glob)
// 3. 원인 추론

// 코드 수정
// - 관련 파일 수정
// - 증분 커밋 생성

await Bash(`git commit -m "fix(${scope}): 🐛 ${bugInfo.title}"`);
```

### Step 5: 테스트 실행

```typescript
// 관련 테스트 실행
await Bash(`melos run test:select -- --name "${relatedTestPattern}"`);

// 실패 시 자동 수정 시도
if (testFailed) {
  // 테스트 코드 수정
  // 재실행
}

// 필요시 테스트 추가
if (needsNewTest) {
  // 버그 재발 방지 테스트 작성
}
```

### Step 6: PR 생성

```typescript
// PR 생성
const prTitle = `fix(${scope}): 🐛 ${bugInfo.title}`;
const prBody = `
## Summary
- ${bugInfo.title} 버그 수정

## Changes
- ${changesSummary}

## Test Plan
- [ ] 재현 단계 확인
- [ ] 테스트 통과

Closes #${bugInfo.number}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
`;

await Bash(`gh pr create --title "${prTitle}" --body "${prBody}"`);

// Pipeline 이동: Review
await mcp__zenhub__moveIssueToPipeline({
  issueId: bugInfo.id,
  pipelineId: reviewPipelineId
});
```

### Step 7: 머지

```typescript
// 스쿼시 머지 → GitHub "Closes #" 키워드로 이슈 자동 Close
// Done 파이프라인 이동 불필요 (머지 = 완료)
await Bash(`gh pr merge --squash --delete-branch`);
```

---

## 출력 형식

### 성공 시

```
╔════════════════════════════════════════════════════════════════╗
║  Bug Cycle Complete: #123                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🐛 Bug: [Bug] 로그인: 소셜 로그인 버튼 미동작                  ║
║  🌿 Branch: fix/123-social-login-button                        ║
║                                                                ║
║  📝 Commits:                                                   ║
║    1. fix(auth): 🐛 소셜 로그인 버튼 클릭 핸들러 수정           ║
║    2. test(auth): ✅ 소셜 로그인 버튼 테스트 추가               ║
║                                                                ║
║  ✅ Tests:                                                     ║
║    - Unit: 5/5 passed                                          ║
║    - Widget: 3/3 passed                                        ║
║                                                                ║
║  🔀 PR: #456                                                   ║
║    - URL: https://github.com/coco-de/kobic/pull/456            ║
║    - Status: Merged ✅                                         ║
║                                                                ║
║  📊 Duration: 8m 15s                                           ║
║  🏁 Final State: CLOSED (by merge)                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 실패 시

```
╔════════════════════════════════════════════════════════════════╗
║  Bug Cycle Failed: #123                                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ❌ Failed at: Step 4 (버그 수정 작업)                          ║
║                                                                ║
║  Error Details:                                                ║
║    - 원인 파악 실패: 추가 정보 필요                             ║
║    - 관련 코드를 찾을 수 없음                                   ║
║                                                                ║
║  Current State:                                                ║
║    - Branch: fix/123-social-login (exists)                     ║
║    - Commits: 0                                                ║
║    - Pipeline: In Progress                                     ║
║    - PR: Not created                                           ║
║                                                                ║
║  Recovery Options:                                             ║
║    1. 이슈에 추가 정보 요청                                     ║
║    2. 수동으로 원인 분석 후 재시도                               ║
║    3. /workflow:bug-cycle 123 --skip-tests                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## TodoWrite 통합

### 진행 추적

```typescript
TodoWrite([
  { content: "버그 리포트 생성", status: "completed", activeForm: "버그 리포트 생성 완료" },
  { content: "이슈 정보 조회", status: "in_progress", activeForm: "이슈 정보 조회 중" },
  { content: "브랜치 생성", status: "pending", activeForm: "브랜치 생성 대기" },
  { content: "버그 수정 작업", status: "pending", activeForm: "버그 수정 대기" },
  { content: "테스트 실행", status: "pending", activeForm: "테스트 실행 대기" },
  { content: "PR 생성", status: "pending", activeForm: "PR 생성 대기" },
  { content: "머지 및 클로즈", status: "pending", activeForm: "머지 대기" },
]);
```

---

## 에러 처리

### 단계별 복구 전략

| 실패 단계 | 상태 | 복구 방법 |
|---------|------|----------|
| 버그 리포트 | 변경 없음 | `/bug-report` 재시도 |
| 브랜치 생성 | 이슈 존재 | 재시도 |
| 버그 수정 | 브랜치 존재 | 수동 수정 후 재시도 |
| 테스트 | 코드 수정됨 | 수동 테스트 수정 또는 `--skip-tests` |
| PR 생성 | 코드 완성 | `gh pr create` 수동 실행 |
| 머지 | PR 존재 | CI 통과 대기 후 재시도 |

---

## 핵심 규칙

1. **버그 이슈 타입 확인**: Bug 타입 이슈만 처리
2. **브랜치 명명**: `fix/{number}-{slug}` 형식 준수
3. **커밋 메시지**: `fix({scope}): 🐛 {description}` 형식
4. **테스트 필수**: 버그 재발 방지 테스트 추가 권장
5. **이슈 연결**: PR에 `Closes #{number}` 포함
6. **상태 추적**: 모든 단계에서 Pipeline 상태 업데이트

---

## 관련 명령

- `/bug-report`: 버그 리포트 생성
- `/workflow:issue-cycle`: 일반 이슈 사이클
- `/zenhub:workflow`: ZenHub 파이프라인 관리

## 관련 에이전트

- `issue-state-agent`: 이슈 상태 관리
- `implementation-agent`: 코드 구현
- `test-runner-agent`: 테스트 실행
- `pr-lifecycle-agent`: PR 관리

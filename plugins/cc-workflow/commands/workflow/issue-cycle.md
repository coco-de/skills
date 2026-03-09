# /workflow:issue-cycle

> 단일 이슈의 전체 개발 사이클 실행

## 개요

이 스킬은 단일 ZenHub/GitHub 이슈에 대해 브랜치 생성부터 머지까지 전체 개발 사이클을 자동화합니다.

---

## 사용법

```bash
/workflow:issue-cycle {issue_number}
```

### 파라미터

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `issue_number` | ✅ | GitHub 이슈 번호 |

### 옵션

```bash
/workflow:issue-cycle 25 --no-merge      # 머지 없이 PR까지만
/workflow:issue-cycle 25 --skip-tests    # 테스트 스킵 (긴급 핫픽스용)
/workflow:issue-cycle 25 --base main     # 베이스 브랜치 변경
/workflow:issue-cycle 25 --bdd           # BDD 시나리오 강제 생성
/workflow:issue-cycle 25 --skip-bdd      # BDD 시나리오 스킵
/workflow:issue-cycle 25 --skip-review   # 코드 리뷰 스킵 (긴급 핫픽스용)
```

---

## 실행 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│                    /workflow:issue-cycle                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: 이슈 정보 조회                                           │
│  ├── mcp__zenhub__searchLatestIssues                            │
│  ├── 이슈 타입, 제목, 본문 추출                                     │
│  ├── 화면 타입 감지 (목록/상세/폼)                                  │
│  └── 부모/자식 관계 확인                                           │
│                                                                 │
│  Step 2: 브랜치 생성                                              │
│  ├── Task(subagent_type: "issue-branch-agent")                  │
│  ├── issue-state-agent → "In Progress" 이동                      │
│  └── 결과: feature/{number}-{slug}                               │
│                                                                 │
│  Step 3: BDD 시나리오 작성 (화면 기능 시) ← NEW                     │
│  ├── Task(subagent_type: "bdd-scenario-agent")                  │
│  ├── Gherkin Feature 파일 생성                                    │
│  ├── Step Definition 생성                                        │
│  └── 커밋: "test({scope}): ✅ BDD 시나리오 작성"                    │
│                                                                 │
│  Step 4: 구현 작업                                                │
│  ├── Task(subagent_type: "implementation-agent")                │
│  ├── 이슈 내용 분석 → 레이어 에이전트 위임                            │
│  └── 증분 커밋 생성                                                │
│                                                                 │
│  Step 5: 테스트 실행                                              │
│  ├── Task(subagent_type: "test-runner-agent")                   │
│  ├── Unit → BLoC → BDD 순차 실행                                  │
│  └── 실패 시 자동 수정 시도 (최대 3회)                               │
│                                                                 │
│  Step 6: PR 생성                                                  │
│  ├── gh pr create                                                │
│  ├── Closes #{issue_number} 자동 포함                             │
│  └── issue-state-agent → "Review/QA" 이동                        │
│                                                                 │
│  Step 7: 코드 리뷰 진행 ← NEW                                      │
│  ├── /code-review 자동 실행                                       │
│  ├── 리뷰 피드백 자동 반영 (format, analyze --fix)                  │
│  ├── /checklist:feature-complete 실행                            │
│  └── 재검토 필요 시 반복                                            │
│                                                                 │
│  Step 8: 머지 승인 대기                                            │
│  ├── 최종 상태 요약 표시                                            │
│  ├── 사용자 승인 요청 (AskUserQuestion)                            │
│  ├── 승인 시 스쿼시 머지 실행                                       │
│  └── issue-state-agent → "Done" + 이슈 클로즈                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 화면 타입 자동 감지

이슈 제목/본문에서 화면 키워드를 감지하여 BDD 시나리오 작성 여부를 결정합니다:

| 패턴 | 화면 타입 | BDD |
|------|----------|-----|
| "목록", "리스트", "list", "조회" | List | ✅ 생성 |
| "상세", "detail", "보기" | Detail | ✅ 생성 |
| "추가", "생성", "등록", "form" | Form | ✅ 생성 |
| "수정", "편집", "edit" | Form | ✅ 생성 |
| "리팩토링", "개선", "최적화" | - | ❌ 스킵 |
| "설정", "환경", "빌드" | - | ❌ 스킵 |

---

## 상세 구현

### Step 1: 이슈 정보 조회

```typescript
// 이슈 정보 조회
const issueResult = await mcp__zenhub__searchLatestIssues({
  query: issue_number.toString()
});

const issue = issueResult.find(i => i.number === issue_number);

// 추출할 정보
const issueInfo = {
  id: issue.id,                    // GraphQL ID
  number: issue.number,            // GitHub 번호
  title: issue.title,              // 이슈 제목
  body: issue.body,                // 이슈 본문 (AC 포함)
  type: issue.issueType?.name,     // Feature, Task, Bug, Sub-task
  pipeline: issue.pipelineIssue?.pipeline?.name,
  parentIssue: issue.parentIssue,  // 부모 이슈 정보
  labels: issue.labels,            // 라벨 목록
};
```

### Step 2: 브랜치 생성

```typescript
// 브랜치 에이전트 호출
const branchResult = await Task({
  subagent_type: "issue-branch-agent",
  prompt: `
    issue_number: ${issueInfo.number}
    issue_title: ${issueInfo.title}
    issue_type: ${issueInfo.type}
    base_branch: development

    이 이슈를 위한 브랜치를 생성해주세요.
  `
});

// Pipeline 이동: In Progress
await Task({
  subagent_type: "issue-state-agent",
  prompt: `
    issue_number: ${issueInfo.number}
    action: move_pipeline
    target_pipeline: "In Progress"
  `
});
```

### Step 3: BDD 시나리오 작성 (화면 기능 시)

```typescript
// 화면 타입 감지
const screenKeywords = {
  list: ["목록", "리스트", "list", "조회", "검색"],
  detail: ["상세", "detail", "보기"],
  form: ["추가", "생성", "수정", "편집", "form", "등록"],
};

const screenType = detectScreenType(issueInfo.title + issueInfo.body);
const requiresBdd = screenType !== null && !options.skipBdd;

if (requiresBdd || options.bdd) {
  // BDD 시나리오 에이전트 호출
  await Task({
    subagent_type: "bdd-scenario-agent",
    prompt: `
      feature_name: ${extractFeatureName(issueInfo)}
      entity_name: ${extractEntityName(issueInfo)}
      screen_type: ${screenType || "list"}

      화면 타입에 맞는 BDD 시나리오를 생성해주세요.
    `
  });

  // 커밋
  const scope = extractScope(issueInfo);
  await Bash(`
    git add .
    git commit -m "test(${scope}): ✅ BDD 시나리오 작성

    - ${screenType} 화면 시나리오 추가
    - Step Definition 생성

    Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
  `);
}
```

### Step 4: 구현 작업

```typescript
// 구현 에이전트 호출
const implResult = await Task({
  subagent_type: "implementation-agent",
  prompt: `
    issue_number: ${issueInfo.number}
    issue_body: ${issueInfo.body}
    issue_type: ${issueInfo.type}
    issue_title: ${issueInfo.title}

    이슈 내용을 분석하고 구현해주세요.
    완료된 작업마다 커밋을 생성해주세요.
  `
});

// 커밋 결과 확인
console.log(`생성된 커밋: ${implResult.commits.length}개`);
console.log(`변경된 파일: ${implResult.files_changed.length}개`);
```

### Step 4: 테스트 실행

```typescript
// Feature명 추출 (이슈 제목 또는 스코프에서)
const featureName = extractFeatureName(issueInfo);

// 테스트 에이전트 호출
const testResult = await Task({
  subagent_type: "test-runner-agent",
  prompt: `
    feature_name: ${featureName}
    test_types: ["unit", "bloc", "bdd"]
    auto_fix: true

    모든 테스트를 실행하고 결과를 보고해주세요.
  `
});

// 테스트 실패 시 처리
if (!testResult.success) {
  // 자동 수정 불가능한 실패가 있는 경우
  if (testResult.failures.some(f => !f.fixable)) {
    throw new Error(`테스트 실패: ${testResult.failures.length}개`);
  }
}
```

### Step 6: PR 생성

```typescript
// PR 생성
const gitmoji = getGitmoji(issueInfo.type);
const scope = extractScope(issueInfo);

await Bash(`
  gh pr create --title "${gitmoji} ${scope}: ${issueInfo.title}" \
    --body "$(cat <<'EOF'
## Summary
- ${issueInfo.title}

## Test Plan
- [ ] 단위 테스트 통과
- [ ] BLoC 테스트 통과
${requiresBdd ? '- [ ] BDD 시나리오 통과' : ''}

Closes #${issueInfo.number}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
`);

// Pipeline 이동: Review/QA
await mcp__zenhub__moveIssueToPipeline({
  issueId: issueInfo.id,
  pipelineId: reviewQaPipelineId,
});
```

### Step 7: 코드 리뷰 진행

```typescript
if (!options.skipReview) {
  // /code-review 자동 실행
  await Skill({ skill: "code-review" });

  // 자동 반영 가능한 피드백 적용
  await Bash(`melos run format`);
  await Bash(`melos run analyze --fix`);

  // 수정 사항 있으면 커밋
  const hasChanges = await Bash(`git status --porcelain`);
  if (hasChanges.stdout.trim()) {
    await Bash(`
      git add .
      git commit -m "style(${scope}): 🎨 코드 리뷰 피드백 반영

      - 포맷팅 적용
      - 린트 경고 수정

      Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
    `);
    await Bash(`git push`);
  }

  // /checklist:feature-complete 실행
  await Skill({ skill: "checklist:feature-complete" });
}
```

### Step 8: 머지 승인 대기

```typescript
// 최종 상태 요약 표시
console.log(`
╔════════════════════════════════════════════════════════════════╗
║  Ready for Merge                                               ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 Issue: #${issueInfo.number} - ${issueInfo.title}           ║
║  🔀 PR: #${prNumber}                                           ║
║  🌿 Branch: ${branchResult.branch_name}                        ║
║                                                                ║
║  ✅ Tests: ${testResult.summary.passed}/${testResult.summary.total} passed
║  ✅ Review: All issues resolved                                ║
║  ✅ Checklist: Passed                                          ║
║                                                                ║
║  🔒 Merge blocked until user approval                         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
`);

// 사용자 승인 요청
const approval = await AskUserQuestion({
  questions: [{
    header: "머지",
    question: "PR을 머지하시겠습니까?",
    options: [
      { label: "머지 승인", description: "스쿼시 머지 후 이슈 클로즈" },
      { label: "수정 필요", description: "Step 4로 돌아가서 수정" },
      { label: "취소", description: "현재 상태 유지" },
    ],
    multiSelect: false,
  }],
});

if (approval === "머지 승인") {
  // 스쿼시 머지
  await Bash(`gh pr merge --squash --delete-branch`);

  // Pipeline 이동: Done
  await mcp__zenhub__moveIssueToPipeline({
    issueId: issueInfo.id,
    pipelineId: donePipelineId,
  });

  // 이슈 클로즈
  await mcp__zenhub__updateIssue({
    issueId: issueInfo.id,
    state: "CLOSED",
  });

  // 부모 이슈 자동 확인
  if (issueInfo.parentIssue) {
    console.log(`부모 이슈 #${issueInfo.parentIssue.number} 확인 중...`);
    // issue-state-agent가 자동으로 부모 이슈 처리
  }
}
```

---

## 출력 형식

### 성공 시

```
╔════════════════════════════════════════════════════════════════╗
║  Issue Cycle Complete: #25                                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 Issue: feat(community): ✨ 게시글 목록 화면 구현              ║
║  🌿 Branch: feature/25-community-list                          ║
║                                                                ║
║  📝 Commits:                                                   ║
║    1. feat(community): ✨ domain layer 구현                     ║
║    2. feat(community): ✨ data layer 구현                       ║
║    3. feat(community): ✨ presentation layer 구현               ║
║                                                                ║
║  ✅ Tests:                                                     ║
║    - Unit: 12/12 passed                                        ║
║    - BLoC: 8/8 passed                                          ║
║    - BDD: 5/5 scenarios passed                                 ║
║                                                                ║
║  🔀 PR: #42                                                    ║
║    - URL: https://github.com/owner/repo/pull/42                ║
║    - Reviews: 2 comments (auto-resolved)                       ║
║    - Status: Merged ✅                                         ║
║                                                                ║
║  📊 Duration: 15m 32s                                          ║
║  🏁 Final State: CLOSED                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 실패 시

```
╔════════════════════════════════════════════════════════════════╗
║  Issue Cycle Failed: #25                                       ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ❌ Failed at: Step 4 (테스트 실행)                              ║
║                                                                ║
║  Error Details:                                                ║
║    - Test: post_list_bloc_test.dart                            ║
║    - Reason: Expected PostLoaded but got PostError             ║
║    - Fixable: No (logic error)                                 ║
║                                                                ║
║  Current State:                                                ║
║    - Branch: feature/25-community-list (exists)                ║
║    - Commits: 3 committed                                      ║
║    - Pipeline: In Progress                                     ║
║    - PR: Not created                                           ║
║                                                                ║
║  Recovery Options:                                             ║
║    1. Fix the test manually and re-run                         ║
║    2. /workflow:issue-cycle 25 --skip-tests                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 에러 처리

### 단계별 복구 전략

| 실패 단계 | 상태 | 복구 방법 |
|---------|------|----------|
| 브랜치 생성 | 변경 없음 | 재시도 |
| 구현 작업 | 브랜치 존재, 일부 커밋 | 이어서 작업 |
| 테스트 | 코드 완성, 테스트 실패 | 수동 수정 후 재시도 |
| PR 생성 | 코드 완성 | PR 수동 생성 또는 재시도 |
| 머지 | PR 존재, CI 대기 | CI 통과 대기 후 재시도 |
| 이슈 클로즈 | PR 머지됨 | 수동 클로즈 |

### 자동 복구 시도

```typescript
// 최대 재시도 횟수
const MAX_RETRIES = 3;

async function executeWithRetry(step, retries = MAX_RETRIES) {
  for (let i = 0; i < retries; i++) {
    try {
      return await step();
    } catch (error) {
      if (i === retries - 1) throw error;
      console.log(`재시도 ${i + 1}/${retries}...`);
      await sleep(5000); // 5초 대기
    }
  }
}
```

---

## TodoWrite 통합

### 진행 추적

```typescript
// 시작 시
TodoWrite([
  { content: "이슈 정보 조회", status: "in_progress", activeForm: "이슈 정보 조회 중" },
  { content: "브랜치 생성", status: "pending", activeForm: "브랜치 생성 대기" },
  { content: "구현 작업", status: "pending", activeForm: "구현 작업 대기" },
  { content: "테스트 실행", status: "pending", activeForm: "테스트 실행 대기" },
  { content: "PR 생성 및 머지", status: "pending", activeForm: "PR 생성 대기" },
  { content: "이슈 클로즈", status: "pending", activeForm: "이슈 클로즈 대기" },
]);

// 각 단계 완료 시 즉시 업데이트
// "completed"로 마킹하고 다음 단계를 "in_progress"로 변경
```

---

## 핵심 규칙

1. **순차 실행**: 각 단계는 이전 단계 성공 후에만 진행
2. **상태 추적**: 모든 단계에서 현재 상태를 기록
3. **실패 허용**: 실패 시 현재 상태 보존하고 명확한 복구 가이드 제공
4. **이슈 연결**: 모든 커밋과 PR에 이슈 번호 참조
5. **자동 정리**: 성공 시 브랜치 자동 삭제 (머지 후)
6. **부모 체크**: 이슈 클로즈 시 부모 이슈 자동 확인

---

## 검증 게이트 (필수)

### 브랜치 검증 (Step 2 시작 전)

```bash
# 현재 브랜치 확인
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# development/main에서 직접 작업 시작 금지
if [[ $BRANCH == "development" || $BRANCH == "main" ]]; then
  echo "❌ development/main에서 직접 작업할 수 없습니다"
  echo ""
  echo "   /workflow:issue-cycle은 Step 2에서 브랜치를 생성합니다."
  echo "   현재 development 브랜치에 있다면 정상입니다."
  echo ""
  # Step 2가 브랜치를 생성하므로 계속 진행
fi
```

### PR 생성 전 검증 (Step 6 전)

```bash
# 1. 브랜치 형식 검증
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ ! $BRANCH =~ ^(feature|fix|refactor|chore)/[0-9]+ ]]; then
  echo "❌ 브랜치 형식 오류: $BRANCH"
  echo "   올바른 형식: feature/{issue_number}-description"
  echo ""
  echo "   Step 2에서 브랜치가 생성되지 않았습니다."
  echo "   /workflow:issue-cycle을 다시 실행해주세요."
  exit 1
fi

# 2. development/main 직접 커밋 방지
if [[ $BRANCH == "development" || $BRANCH == "main" ]]; then
  echo "❌ development/main에 직접 PR을 생성할 수 없습니다"
  exit 1
fi

# 3. 커밋 존재 확인
COMMITS=$(git rev-list --count origin/development..HEAD)
if [[ $COMMITS -eq 0 ]]; then
  echo "❌ 커밋이 없습니다."
  echo "   Step 4 (구현 작업)을 먼저 완료해주세요."
  exit 1
fi

# 4. Pre-push 검증
echo "🔍 Pre-push 검증 중..."
melos run format || { echo "❌ 포맷 오류"; exit 1; }
melos run analyze || { echo "❌ 분석 오류"; exit 1; }
echo "✅ Pre-push 검증 통과"
```

---

## TodoWrite 통합 (필수)

### 초기화 (Step 1 시작 시)

```typescript
TodoWrite([
  { content: "Step 1: 이슈 정보 조회", status: "in_progress", activeForm: "이슈 조회 중" },
  { content: "Step 2: 브랜치 생성", status: "pending", activeForm: "브랜치 생성 대기" },
  { content: "Step 3: BDD 시나리오", status: "pending", activeForm: "BDD 작성 대기" },
  { content: "Step 4: 구현 작업", status: "pending", activeForm: "구현 대기" },
  { content: "Step 5: 테스트 실행", status: "pending", activeForm: "테스트 대기" },
  { content: "Step 5.5: Pre-push 검증", status: "pending", activeForm: "검증 대기" },
  { content: "Step 6: PR 생성", status: "pending", activeForm: "PR 생성 대기" },
  { content: "Step 7: 코드 리뷰", status: "pending", activeForm: "리뷰 대기" },
  { content: "Step 8: 머지 승인", status: "pending", activeForm: "머지 대기" },
]);
```

### 단계 완료 시 즉시 업데이트

```typescript
// 각 단계 완료 즉시 TodoWrite 호출
// 예: Step 2 완료 후
TodoWrite([
  { content: "Step 1: 이슈 정보 조회", status: "completed", activeForm: "이슈 조회 완료" },
  { content: "Step 2: 브랜치 생성", status: "completed", activeForm: "브랜치 생성 완료" },
  { content: "Step 3: BDD 시나리오", status: "in_progress", activeForm: "BDD 작성 중" },
  // ... 나머지 pending 유지
]);
```

### 상태 추적 규칙

| 규칙 | 설명 |
|------|------|
| **in_progress 1개만** | 동시에 in_progress 상태는 1개만 허용 |
| **즉시 업데이트** | 단계 완료 즉시 completed로 변경 |
| **스킵 표시** | 해당 없는 단계(BDD 등)는 content에 "(스킵)" 추가 |
| **실패 시 유지** | 실패한 단계는 in_progress 유지, 오류 메시지 출력 |

---

## 관련 에이전트

- `issue-branch-agent`: 브랜치 생성
- `bdd-scenario-agent`: BDD 시나리오 생성 (화면 기능 시)
- `implementation-agent`: 코드 구현
- `test-runner-agent`: 테스트 실행 (BDD 포함)
- `pr-lifecycle-agent`: PR 관리
- `issue-state-agent`: 이슈 상태 관리

## 관련 스킬

- `/workflow`: 작업 내용으로 전체 사이클 시작
- `/workflow:bug-cycle`: 버그 수정 전용 사이클
- `/workflow:parallel-issues`: 여러 이슈 병렬 처리
- `/workflow:sprint`: Epic 전체 오케스트레이션
- `/code-review`: 코드 리뷰 실행
- `/checklist:feature-complete`: 완료 체크리스트
- `/bdd:generate`: BDD 시나리오 생성

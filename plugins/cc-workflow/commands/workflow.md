---
name: workflow
description: "이슈 생성부터 머지까지 전체 개발 사이클 자동화"
invoke: /workflow
aliases: ["/wf"]
category: petmedi-development
complexity: high
mcp-servers: [zenhub]
---

# /workflow

> 작업 내용으로 이슈 생성부터 머지 승인까지 전체 개발 사이클 자동화

## Triggers

- 새로운 기능/버그/리팩토링 작업 시작 시
- 작업 내용만으로 전체 사이클 실행 필요 시
- 이슈 생성 → 구현 → PR → 리뷰 → 머지 일괄 처리 시

## 사용법

### 기본 사용

```bash
# 작업 내용으로 전체 사이클 시작
/workflow "저자 목록 화면 추가"
```

### 기존 이슈로 시작 (Step 4부터)

```bash
/workflow 1810
# 또는
/workflow:issue-cycle 1810
```

---

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `작업 내용` | ✅* | 작업에 대한 설명 | `"저자 목록 화면 추가"` |
| `issue_number` | ✅* | 기존 이슈 번호 | `1810` |

*작업 내용 또는 이슈 번호 중 하나 필수

---

## 옵션

### 자동 결정 옵션 (기본값)

옵션 미지정 시 자동으로 결정됩니다:

| 옵션 | 기본값 | 자동 결정 규칙 |
|------|--------|---------------|
| `--type` | 자동 추론 | 키워드 분석: "추가/생성"→feat, "수정/고치기"→fix, "개선"→refactor |
| `--scope` | 자동 추론 | 작업 내용에서 Entity/Feature명 추출, 불명확 시 질문 |
| `--point` | 자동 산정 | 복잡도 분석: 단일파일(1), 여러파일(3), 여러레이어(5), BDD포함(8) |
| `--bdd` | 화면 감지 시 | 목록/상세/폼 키워드 감지 → 자동 BDD 시나리오 작성 |

### 명시 옵션

```bash
# 타입 명시
/workflow --type feat "저자 목록 화면 추가"

# 스코프 명시
/workflow --scope console-author "저자 목록 화면 추가"

# Point 명시
/workflow --point 5 "저자 목록 화면 추가"

# Sprint 할당
/workflow --sprint current "저자 목록 화면 추가"

# PR까지만 (머지 대기 없이)
/workflow --no-merge "저자 목록 화면 추가"

# 리뷰 스킵 (긴급 핫픽스)
/workflow --skip-review "긴급 수정"

# BDD 시나리오 강제 (화면 아닌 기능에도)
/workflow --bdd "API 클라이언트 리팩토링"

# BDD 시나리오 스킵 (화면 기능이어도)
/workflow --skip-bdd "간단한 목록 수정"

# 테스트 스킵 (긴급)
/workflow --skip-tests "긴급 수정"
```

---

## 실행 흐름 (13단계)

### 단계별 전제조건 및 검증

| Step | 단계 | 전제조건 | 검증 |
|------|------|---------|------|
| 1 | 작업 내용 분석 | 없음 | - |
| 2 | ZenHub 이슈 생성 | Step 1 완료 | issue.id 존재 |
| 3 | Product Backlog 이동 | Step 2 완료 | pipeline 확인 |
| 4 | 브랜치 생성 | Step 2,3 완료 | branch 존재 |
| 5 | In Progress 이동 | Step 4 완료 | pipeline 확인 |
| 6 | BDD 시나리오 작성 | Step 5 완료, 화면 기능 | .feature 파일 존재 |
| 7 | 구현 작업 | Step 5 완료 | 커밋 존재 |
| 7.5 | Backend 코드 생성 | Step 7 완료, Backend 변경 시 | 생성 성공 |
| 8 | 테스트 작성/실행 | Step 7 완료 | 테스트 통과 |
| **8.5** | **Pre-push 검증** | Step 8 완료 | format, analyze 통과 |
| 9 | PR 생성 | Step 8.5 완료 | PR URL 존재 |
| 10 | Review/QA 이동 | Step 9 완료 | pipeline 확인 |
| 11 | 코드 리뷰 진행 | Step 10 완료 | 리뷰 완료 |
| 12 | 머지 승인 대기 | Step 11 완료 | 사용자 승인 |

```
┌─────────────────────────────────────────────────────────────────┐
│                    /workflow "작업 내용"                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Step 1: 작업 내용 분석                                          │
│  ├── 작업 유형 추론 (feat/fix/chore/refactor)                    │
│  ├── 스코프 추출 (feature명)                                     │
│  ├── 화면 타입 감지 (목록/상세/폼)                                │
│  └── 예상 복잡도 산정 (Story Point)                              │
│                                                                 │
│  Step 2: ZenHub 이슈 생성                                        │
│  ├── mcp__zenhub__createGitHubIssue                             │
│  ├── 이슈 타입 자동 설정 (Feature/Task/Bug)                      │
│  ├── 라벨 자동 지정                                              │
│  └── Estimate 설정                                              │
│                                                                 │
│  Step 3: Product Backlog 이동                                   │
│  ├── mcp__zenhub__moveIssueToPipeline                           │
│  └── Pipeline: Product Backlog                                  │
│                                                                 │
│  Step 4: 브랜치 생성 ⚠️ 필수                                     │
│  ├── issue-branch-agent 호출                                    │
│  ├── {type}/{number}-{slug} 형식                                │
│  ├── development 브랜치 기반                                    │
│  └── ⚠️ development/main에 직접 커밋 금지                        │
│                                                                 │
│  Step 5: In Progress 이동                                       │
│  ├── issue-state-agent 호출                                     │
│  └── Pipeline: In Progress                                      │
│                                                                 │
│  Step 6: BDD 시나리오 작성 (화면 기능 시)                          │
│  ├── bdd-scenario-agent 호출                                    │
│  ├── Gherkin Feature 파일 생성                                   │
│  ├── Step Definition 생성                                       │
│  └── 커밋: "test({scope}): ✅ BDD 시나리오 작성"                  │
│                                                                 │
│  Step 7: 구현 작업                                               │
│  ├── 이슈 내용 기반 구현                                         │
│  └── 증분 커밋 생성                                              │
│                                                                 │
│  Step 7.5: Backend 코드 생성 (Backend 변경 시) ⚠️                │
│  ├── melos run backend:pod:generate                             │
│  └── 커밋: "chore(backend): 🔧 코드 생성"                        │
│                                                                 │
│  Step 8: 테스트 작성 및 검증 (필수 게이트) ⚠️                      │
│  ├── [프론트엔드 테스트 - 필수]                                    │
│  │   ├── UseCase 단위 테스트 (unit-test-agent)                   │
│  │   └── BLoC 단위 테스트 (bloc-test-agent)                      │
│  ├── [백엔드 테스트 - Backend 변경 시 필수]                        │
│  │   ├── 엔드포인트 단위 테스트 (serverpod-test-agent)            │
│  │   ├── 서비스 로직 단위 테스트 (serverpod-test-agent)           │
│  │   └── 엔드포인트 통합 테스트 (serverpod-test-agent)            │
│  ├── BDD Widget 테스트 (화면 기능 시)                             │
│  ├── test-runner-agent 호출 (require_tests: true)              │
│  ├── ⚠️ 모든 테스트 통과 필수 (게이트 실패 시 PR 생성 차단)        │
│  └── 커밋: "test({scope}): ✅ 테스트 작성"                        │
│                                                                 │
│  Step 8.5: Pre-push 검증 ⚠️ 필수                                 │
│  ├── melos run format                                           │
│  ├── melos run analyze                                          │
│  ├── dcm analyze .                                              │
│  └── 검증 실패 시 Step 9 진행 불가                                │
│                                                                 │
│  Step 9: PR 생성 (검증 게이트 통과 후)                            │
│  ├── ⚠️ 브랜치 형식 검증 필수                                    │
│  ├── gh pr create                                               │
│  ├── Closes #{issue_number} 자동 포함                           │
│  └── ZenHub PR 연결                                             │
│                                                                 │
│  Step 10: Review/QA 이동                                        │
│  ├── mcp__zenhub__moveIssueToPipeline                           │
│  └── Pipeline: Review/QA                                        │
│                                                                 │
│  Step 11: 코드 리뷰 진행                                         │
│  ├── /code-review 자동 실행                                      │
│  ├── 리뷰 피드백 자동 반영                                        │
│  ├── 재검토 필요 시 반복                                         │
│  └── /checklist:feature-complete 실행                           │
│                                                                 │
│  Step 12: 머지 승인 대기                                         │
│  ├── 사용자 승인 요청                                            │
│  ├── 승인 시 스쿼시 머지                                         │
│  └── GitHub "Closes #" 키워드로 이슈 자동 Close                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 검증 게이트 (필수)

### Step 4 브랜치 검증 (필수)

**development/main 브랜치에서 직접 커밋 금지**:

```bash
# 현재 브랜치 확인
BRANCH=$(git rev-parse --abbrev-ref HEAD)

# development/main 체크
if [[ $BRANCH == "development" || $BRANCH == "main" ]]; then
  echo "❌ development/main에 직접 커밋할 수 없습니다"
  echo "   /workflow 스킬은 반드시 feature 브랜치에서 작업합니다"
  echo ""
  echo "   올바른 사용법:"
  echo "   1. /workflow \"작업 내용\" - 이슈 생성부터 시작"
  echo "   2. /workflow:issue-cycle {number} - 기존 이슈로 시작"
  exit 1
fi
```

### Step 9 PR 생성 전 검증 (필수)

다음 조건을 **모두** 만족해야 PR 생성 가능:

1. **브랜치 형식 검증**
   ```bash
   BRANCH=$(git rev-parse --abbrev-ref HEAD)
   if [[ ! $BRANCH =~ ^(feature|fix|refactor|chore)/[0-9]+ ]]; then
     echo "❌ 브랜치 형식 오류: $BRANCH"
     echo "   올바른 형식: feature/30-description"
     exit 1
   fi
   ```

2. **이슈 연결 검증**
   - 브랜치명에서 이슈 번호 추출 가능
   - ZenHub 이슈가 In Progress 상태

3. **커밋 검증**
   ```bash
   COMMITS=$(git rev-list --count origin/development..HEAD)
   if [[ $COMMITS -eq 0 ]]; then
     echo "❌ 커밋이 없습니다. Step 7을 먼저 완료해주세요"
     exit 1
   fi
   ```

4. **Pre-push 검증** (Step 8.5)
   ```bash
   melos run format || exit 1
   melos run analyze || exit 1
   dcm analyze . || exit 1
   ```

### 단계 건너뛰기 방지

**원칙**: 각 단계는 **이전 단계 완료 후**에만 진행 가능

```typescript
// 단계 전제조건 검증
async function validateStepPrerequisites(stepNumber: number) {
  const todos = await getTodoList();

  // 이전 단계들이 모두 completed인지 확인
  for (let i = 1; i < stepNumber; i++) {
    const step = todos.find(t => t.content.startsWith(`Step ${i}`));
    if (step?.status !== "completed" && step?.status !== "skipped") {
      throw new Error(`
        ❌ Step ${i}이(가) 완료되지 않았습니다.
        현재 상태: ${step?.status || 'unknown'}

        먼저 Step ${i}을(를) 완료해주세요.
      `);
    }
  }
}
```

---

## 세부 구현

### Step 1: 작업 내용 분석

```typescript
// 키워드 기반 타입 자동 추론
const typeKeywords = {
  feat: ["추가", "구현", "생성", "만들기", "화면"],
  fix: ["수정", "고치기", "버그", "에러", "문제"],
  refactor: ["개선", "리팩토링", "정리", "최적화"],
  chore: ["설정", "빌드", "환경", "배포"],
  docs: ["문서", "README", "주석"],
  test: ["테스트", "test", "검증"],
};

// 화면 타입 감지
const screenKeywords = {
  list: ["목록", "리스트", "list", "조회", "검색"],
  detail: ["상세", "detail", "보기"],
  form: ["추가", "생성", "수정", "편집", "form", "등록"],
};

const analysis = {
  type: inferType(workContent),      // feat/fix/refactor...
  scope: extractScope(workContent),  // feature명
  screenType: detectScreen(workContent), // list/detail/form/null
  point: estimatePoint(workContent), // 1/3/5/8
  requiresBdd: screenType !== null,  // 화면 기능이면 true
};
```

### Step 2: ZenHub 이슈 생성

```typescript
// 이슈 타입 매핑
const issueTypeMap = {
  feat: "Feature",
  fix: "Bug",
  refactor: "Task",
  chore: "Task",
  docs: "Task",
  test: "Task",
};

// GitHub 이슈 생성
const issue = await mcp__zenhub__createGitHubIssue({
  repositoryId: githubRepoId,
  title: `${gitmoji} ${analysis.scope}: ${workContent}`,
  body: generateIssueBody(workContent, analysis),
  issueTypeId: getIssueTypeId(issueTypeMap[analysis.type]),
  labels: generateLabels(analysis),
});

// Estimate 설정
await mcp__zenhub__setIssueEstimate({
  issueId: issue.id,
  estimate: analysis.point,
});
```

### Step 3-5: Pipeline 이동 & 브랜치 생성

```typescript
// Product Backlog 이동
await mcp__zenhub__moveIssueToPipeline({
  issueId: issue.id,
  pipelineId: productBacklogPipelineId,
});

// 브랜치 생성
await Task({
  subagent_type: "issue-branch-agent",
  prompt: `이슈 #${issue.number} 브랜치 생성`,
});

// In Progress 이동
await mcp__zenhub__moveIssueToPipeline({
  issueId: issue.id,
  pipelineId: inProgressPipelineId,
});
```

### Step 6: BDD 시나리오 작성 (화면 기능 시)

```typescript
if (analysis.requiresBdd && !options.skipBdd) {
  await Task({
    subagent_type: "bdd-scenario-agent",
    prompt: `
      feature_name: ${analysis.scope}
      screen_type: ${analysis.screenType}

      화면 타입에 맞는 BDD 시나리오를 생성해주세요.
    `,
  });

  // 커밋
  await Bash(`
    git add .
    git commit -m "test(${analysis.scope}): ✅ BDD 시나리오 작성

    - ${analysis.screenType} 화면 시나리오 추가
    - Step Definition 생성

    Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
  `);
}
```

### Step 7-8: 구현 및 테스트

```typescript
// 구현 작업
await Task({
  subagent_type: "implementation-agent",
  prompt: `이슈 #${issue.number} 구현`,
});

// Backend 변경 감지
const hasBackendChanges = detectBackendChanges(issue);

// 테스트 작성 및 검증 (필수 게이트) ⚠️
if (!options.skipTests) {
  const testTypes = ["unit", "bloc"];
  if (analysis.requiresBdd) testTypes.push("bdd");
  if (hasBackendChanges) testTypes.push("backend_unit", "backend_integration");

  await Task({
    subagent_type: "test-runner-agent",
    prompt: `
      feature_name: ${analysis.scope}
      test_types: ${JSON.stringify(testTypes)}
      auto_fix: true
      require_tests: true
    `,
  });

  // ⚠️ 테스트 실패 시 PR 생성 차단
} else {
  // --skip-tests 사용 시 사용자 확인 필수
  const confirm = await AskUserQuestion({
    questions: [{
      header: "테스트 스킵 확인",
      question: "테스트를 스킵하면 검증 없이 PR이 생성됩니다. 계속하시겠습니까?",
      options: [
        { label: "스킵 확인", description: "테스트 없이 진행 (긴급 핫픽스용)" },
        { label: "테스트 실행", description: "테스트를 실행합니다" },
      ],
    }],
  });
}
```

### Step 9-10: PR 생성 & Review/QA 이동

```typescript
// PR 생성
await Bash(`
  gh pr create --title "${gitmoji} ${analysis.scope}: ${workContent}" \
    --body "$(cat <<'EOF'
## Summary
- ${workContent}

## Test Plan
- [ ] UseCase 단위 테스트 통과
- [ ] BLoC 단위 테스트 통과
${hasBackendChanges ? '- [ ] 백엔드 엔드포인트 단위 테스트 통과' : ''}
${hasBackendChanges ? '- [ ] 백엔드 서비스 로직 단위 테스트 통과' : ''}
${hasBackendChanges ? '- [ ] 백엔드 엔드포인트 통합 테스트 통과' : ''}
${analysis.requiresBdd ? '- [ ] BDD 시나리오 통과' : ''}

Closes #${issue.number}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
`);

// Review/QA 이동
await mcp__zenhub__moveIssueToPipeline({
  issueId: issue.id,
  pipelineId: reviewQaPipelineId,
});
```

### Step 11: 코드 리뷰 진행

```typescript
if (!options.skipReview) {
  // /code-review 실행
  await Skill({ skill: "code-review" });

  // 피드백 반영 (자동 가능한 것만)
  await Bash(`melos run format`);
  await Bash(`melos run analyze --fix`);

  // /checklist:feature-complete 실행
  await Skill({ skill: "checklist:feature-complete" });
}
```

### Step 12: 머지 승인 대기

```typescript
// 최종 상태 요약
displayMergeSummary(issue, pr, testResults, reviewResults);

// 사용자 승인 요청
const approval = await AskUserQuestion({
  questions: [{
    header: "머지",
    question: "PR을 머지하시겠습니까?",
    options: [
      { label: "머지 승인", description: "스쿼시 머지 후 이슈 클로즈" },
      { label: "수정 필요", description: "Step 7로 돌아가서 수정" },
      { label: "취소", description: "현재 상태 유지" },
    ],
    multiSelect: false,
  }],
});

if (approval === "머지 승인") {
  // 스쿼시 머지 → GitHub "Closes #" 키워드로 이슈 자동 Close
  // Done 파이프라인 이동 불필요 (머지 = 완료)
  await Bash(`gh pr merge --squash --delete-branch`);
}
```

---

## 출력 형식

### 진행 상황 표시

```
╔════════════════════════════════════════════════════════════════╗
║  /workflow Progress                                            ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  [████████░░░░░░░░░░░░] 50% - Step 6/12                       ║
║                                                                ║
║  ✅ Step 1: 작업 내용 분석 완료 (화면 기능 감지: List)          ║
║  ✅ Step 2: 이슈 #1810 생성 완료                                ║
║  ✅ Step 3: Product Backlog 이동                               ║
║  ✅ Step 4: 브랜치 생성 완료                                   ║
║  ✅ Step 5: In Progress 이동                                   ║
║  🔄 Step 6: BDD 시나리오 작성 중...                            ║
║  ⏳ Step 7: 구현 작업 대기                                     ║
║  ⏳ Step 8: 테스트 작성/실행 대기                               ║
║  ⏳ Step 9: PR 생성 대기                                       ║
║  ⏳ Step 10: Review/QA 이동 대기                               ║
║  ⏳ Step 11: 코드 리뷰 대기                                    ║
║  ⏳ Step 12: 머지 승인 대기                                    ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 완료 시

```
╔════════════════════════════════════════════════════════════════╗
║  Workflow Complete: #1810                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 Issue: #1810 - 저자 목록 화면 추가                          ║
║  🔀 PR: #1815                                                  ║
║  🌿 Branch: feature/1810-author-list (deleted)                 ║
║                                                                ║
║  📝 Changes:                                                   ║
║    - 12 files changed                                         ║
║    - +520 / -30 lines                                         ║
║                                                                ║
║  ✅ Tests: 35/35 passed                                        ║
║    - UseCase Unit: 10/10                                      ║
║    - BLoC Unit: 8/8                                           ║
║    - Backend Unit: 6/6 (endpoint: 3, service: 3)              ║
║    - Backend Integration: 4/4                                 ║
║    - BDD: 7/7 scenarios                                       ║
║                                                                ║
║  ✅ Review: All issues resolved                                ║
║  ✅ Checklist: 11/11 passed                                   ║
║  ✅ CI: All checks passed                                      ║
║                                                                ║
║  📊 Duration: 22m 15s                                          ║
║  🏁 Final State: CLOSED (by merge)                             ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## TodoWrite 통합 (필수)

**규칙**: 각 단계 시작/완료 시 **즉시** TodoWrite 업데이트

### 초기화 (Step 1 시작 시)

```typescript
TodoWrite([
  { content: "Step 1: 작업 내용 분석", status: "in_progress", activeForm: "작업 내용 분석 중" },
  { content: "Step 2: ZenHub 이슈 생성", status: "pending", activeForm: "이슈 생성 대기" },
  { content: "Step 3: Product Backlog 이동", status: "pending", activeForm: "Pipeline 이동 대기" },
  { content: "Step 4: 브랜치 생성", status: "pending", activeForm: "브랜치 생성 대기" },
  { content: "Step 5: In Progress 이동", status: "pending", activeForm: "Pipeline 이동 대기" },
  { content: "Step 6: BDD 시나리오", status: "pending", activeForm: "BDD 작성 대기" },
  { content: "Step 7: 구현 작업", status: "pending", activeForm: "구현 대기" },
  { content: "Step 7.5: Backend 코드 생성", status: "pending", activeForm: "Backend 생성 대기" },
  { content: "Step 8: 테스트 작성 및 검증 (필수 게이트)", status: "pending", activeForm: "테스트 대기" },
  { content: "Step 8.5: Pre-push 검증", status: "pending", activeForm: "검증 대기" },
  { content: "Step 9: PR 생성", status: "pending", activeForm: "PR 생성 대기" },
  { content: "Step 10-12: 리뷰/머지", status: "pending", activeForm: "리뷰 대기" },
]);
```

### 단계 완료 시 즉시 업데이트

```typescript
// Step 4 완료 후 예시
TodoWrite([
  { content: "Step 1: 작업 내용 분석", status: "completed", activeForm: "작업 분석 완료" },
  { content: "Step 2: ZenHub 이슈 생성", status: "completed", activeForm: "이슈 생성 완료" },
  { content: "Step 3: Product Backlog 이동", status: "completed", activeForm: "Pipeline 이동 완료" },
  { content: "Step 4: 브랜치 생성", status: "completed", activeForm: "브랜치 생성 완료" },
  { content: "Step 5: In Progress 이동", status: "in_progress", activeForm: "Pipeline 이동 중" },
  // ... 나머지 pending 유지
]);
```

### 상태 추적 규칙

| 규칙 | 설명 |
|------|------|
| **in_progress 1개만** | 동시에 in_progress 상태는 1개만 허용 |
| **즉시 업데이트** | 단계 완료 즉시 completed로 변경 |
| **스킵 표시** | 해당 없는 단계는 content에 "(스킵)" 추가 |
| **실패 시 유지** | 실패한 단계는 in_progress 유지 |

---

## 자동 추론 상세

### 타입 추론 예시

```bash
/workflow "저자 목록 화면 추가"
→ 키워드 "추가", "화면" 감지 → feat

/workflow "로그인 버그 수정"
→ 키워드 "버그", "수정" 감지 → fix

/workflow "API 응답 캐싱 개선"
→ 키워드 "개선" 감지 → refactor
```

### 화면 타입 감지 예시

```bash
/workflow "저자 목록 화면 추가"
→ 키워드 "목록" 감지 → List → BDD 자동 생성

/workflow "도서 상세 화면 구현"
→ 키워드 "상세" 감지 → Detail → BDD 자동 생성

/workflow "저자 등록 폼 추가"
→ 키워드 "등록" 감지 → Form → BDD 자동 생성

/workflow "API 응답 캐싱 추가"
→ 화면 키워드 없음 → BDD 스킵
```

---

## 에러 처리

### 단계별 복구 전략

| 실패 단계 | 상태 | 복구 방법 |
|---------|------|----------|
| 이슈 생성 | 변경 없음 | 재시도 |
| 브랜치 생성 | 이슈 존재 | 재시도 |
| BDD 시나리오 | 브랜치 존재 | `--skip-bdd` 또는 수동 작성 |
| 구현 작업 | 브랜치 존재 | 이어서 작업 |
| 테스트 | 코드 완성 | `--skip-tests` 또는 수동 수정 |
| PR 생성 | 코드 완성 | `gh pr create` 수동 실행 |
| 코드 리뷰 | PR 존재 | `--skip-review` 또는 수동 반영 |
| 머지 | PR 존재 | CI 통과 대기 후 수동 머지 |

---

## 관련 커맨드

- `/workflow:issue-cycle {number}` - 기존 이슈로 사이클 진행
- `/workflow:bug-cycle` - 버그 수정 전용 사이클
- `/bug-report` - 버그 리포트 생성
- `/code-review` - 코드 리뷰 실행
- `/checklist:feature-complete` - 완료 체크리스트

## 관련 에이전트

- `issue-branch-agent` - 브랜치 생성
- `issue-state-agent` - 이슈 상태 관리
- `bdd-scenario-agent` - BDD 시나리오 생성
- `implementation-agent` - 코드 구현
- `test-runner-agent` - 테스트 실행
- `pr-lifecycle-agent` - PR 관리

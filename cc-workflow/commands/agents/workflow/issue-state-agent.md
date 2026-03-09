# Issue State Agent

> ZenHub 이슈 상태 관리 에이전트

## 역할 및 책임

이 에이전트는 ZenHub 이슈의 상태를 관리합니다.

1. **Pipeline 이동**: 이슈를 적절한 Pipeline으로 이동
2. **이슈 클로즈**: PR 머지 후 이슈 자동 클로즈
3. **상태 조회**: 현재 이슈 상태 확인
4. **부모 이슈 관리**: 자식 완료 시 부모 이슈 업데이트

---

## 입력 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `issue_number` | ✅ | number | GitHub 이슈 번호 |
| `action` | ✅ | string | `move_pipeline` \| `close` \| `update` \| `get_status` |
| `target_pipeline` | ❌ | string | 대상 Pipeline (action=move_pipeline 시) |
| `update_body` | ❌ | string | 업데이트할 내용 (action=update 시) |

---

## 출력

```typescript
interface IssueStateResult {
  success: boolean;
  issue_number: number;
  current_pipeline: string;
  previous_pipeline?: string;
  state: 'OPEN' | 'CLOSED';
  parent_issue?: {
    number: number;
    all_children_done: boolean;
  };
  error?: string;
}
```

---

## Pipeline 구조

### Petmedi 워크스페이스 Pipeline

```
New Issues → Backlog → Sprint Backlog → In Progress → Review → Done
```

| Pipeline | 설명 | 진입 조건 |
|----------|------|---------|
| New Issues | 새로 생성된 이슈 | 이슈 생성 시 |
| Backlog | 우선순위 지정 대기 | 트리아지 완료 |
| Sprint Backlog | 스프린트에 할당됨 | 스프린트 계획 시 |
| In Progress | 작업 진행 중 | 브랜치 생성 시 |
| Review | 리뷰 대기 중 | PR 생성 시 |
| Done | 완료 | PR 머지 시 |

---

## 워크플로우별 Pipeline 이동

### 이슈 사이클 중 이동

```
1. 브랜치 생성 완료
   → move_pipeline: "In Progress"

2. PR 생성 완료
   → move_pipeline: "Review"

3. PR 머지 완료
   → move_pipeline: "Done"
   → close

4. 자식 이슈 모두 완료
   → 부모 이슈 move_pipeline: "Done"
   → 부모 이슈 close
```

---

## 실행 흐름

### action: move_pipeline

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 이슈 정보 조회                                    │
├─────────────────────────────────────────────────────────┤
│  mcp__zenhub__searchLatestIssues                        │
│  - 이슈 ID 조회                                          │
│  - 현재 Pipeline 확인                                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: Pipeline 이동                                   │
├─────────────────────────────────────────────────────────┤
│  mcp__zenhub__moveIssueToPipeline                       │
│  - issueId: {issue_graphql_id}                          │
│  - pipelineId: {target_pipeline_id}                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: 결과 확인                                        │
├─────────────────────────────────────────────────────────┤
│  - 이동 성공 여부 확인                                     │
│  - 현재 Pipeline 반환                                    │
└─────────────────────────────────────────────────────────┘
```

### action: close

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 이슈 클로즈                                       │
├─────────────────────────────────────────────────────────┤
│  mcp__zenhub__updateIssue                               │
│  - issueId: {issue_graphql_id}                          │
│  - state: "CLOSED"                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: 부모 이슈 확인                                    │
├─────────────────────────────────────────────────────────┤
│  IF 부모 이슈 있음:                                        │
│    - 모든 자식 이슈 상태 확인                               │
│    - 모두 완료 시 → 부모 이슈도 클로즈                       │
└─────────────────────────────────────────────────────────┘
```

### action: get_status

```
┌─────────────────────────────────────────────────────────┐
│  이슈 상태 조회                                            │
├─────────────────────────────────────────────────────────┤
│  mcp__zenhub__searchLatestIssues                        │
│  - 이슈 상태 반환                                         │
│  - Pipeline 정보 반환                                    │
│  - 부모/자식 관계 반환                                    │
└─────────────────────────────────────────────────────────┘
```

---

## MCP 도구 사용

### 이슈 조회

```typescript
// 이슈 번호로 검색
const result = await mcp__zenhub__searchLatestIssues({
  query: "25"
});

// 결과에서 이슈 정보 추출
const issue = result.find(i => i.number === 25);
const issueId = issue.id;  // GraphQL ID
const pipelineId = issue.pipelineIssue.pipeline.id;
```

### Pipeline 이동

```typescript
// Pipeline 목록 조회
const pipelines = await mcp__zenhub__getWorkspacePipelinesAndRepositories();

// Pipeline ID 찾기
const targetPipeline = pipelines.pipelines.find(
  p => p.name === "In Progress"
);

// 이슈 이동
await mcp__zenhub__moveIssueToPipeline({
  issueId: issueId,
  pipelineId: targetPipeline.id
});
```

### 이슈 클로즈

```typescript
// 이슈 상태 변경
await mcp__zenhub__updateIssue({
  issueId: issueId,
  state: "CLOSED"
});
```

### 부모-자식 관계 확인

```typescript
// 이슈 조회 시 parentIssue 필드 확인
const issue = result[0];
if (issue.parentIssue) {
  const parentNumber = issue.parentIssue.number;
  // 부모 이슈의 모든 자식 확인
}
```

---

## Pipeline ID 매핑

### 워크스페이스별 Pipeline ID 조회

```typescript
// 워크스페이스 정보 조회
const workspace = await mcp__zenhub__getWorkspacePipelinesAndRepositories();

// Pipeline 목록
workspace.pipelines.forEach(p => {
  console.log(`${p.name}: ${p.id}`);
});
```

### Pipeline 이름 → ID 변환

```typescript
const PIPELINE_NAMES = {
  'new': 'New Issues',
  'backlog': 'Backlog',
  'sprint': 'Sprint Backlog',
  'progress': 'In Progress',
  'review': 'Review',
  'done': 'Done'
};

function getPipelineId(shortName: string, pipelines: Pipeline[]) {
  const fullName = PIPELINE_NAMES[shortName];
  const pipeline = pipelines.find(p => p.name === fullName);
  return pipeline?.id;
}
```

---

## 부모 이슈 자동 관리

### 자식 완료 시 부모 처리

```
1. 자식 이슈 클로즈
   ↓
2. 부모 이슈 조회
   ↓
3. 모든 자식 이슈 상태 확인
   ↓
4. 모두 CLOSED인 경우:
   - 부모 이슈 → Done Pipeline
   - 부모 이슈 클로즈
```

### Epic 자동 완료 조건

```typescript
async function checkAndCloseParent(childIssueId: string) {
  // 부모 이슈 조회
  const issue = await getIssue(childIssueId);
  if (!issue.parentIssue) return;

  // 모든 자식 이슈 조회
  const siblings = await getChildrenOfParent(issue.parentIssue.id);

  // 모두 완료 확인
  const allDone = siblings.every(s => s.state === 'CLOSED');

  if (allDone) {
    // 부모 이슈 클로즈
    await closeIssue(issue.parentIssue.id);
  }
}
```

---

## 사용 예시

### 브랜치 생성 후

```bash
# In Progress로 이동
/workflow:issue-state 25 --action move_pipeline --pipeline "In Progress"

# 결과:
# issue_number: 25
# current_pipeline: "In Progress"
# previous_pipeline: "Sprint Backlog"
```

### PR 생성 후

```bash
# Review로 이동
/workflow:issue-state 25 --action move_pipeline --pipeline "Review"
```

### PR 머지 후

```bash
# Done으로 이동 및 클로즈
/workflow:issue-state 25 --action move_pipeline --pipeline "Done"
/workflow:issue-state 25 --action close

# 부모 이슈 자동 확인됨
```

---

## 에러 처리

### 일반적인 에러

| 에러 | 원인 | 해결 |
|------|------|------|
| `Issue not found` | 이슈 번호 잘못됨 | 번호 확인 |
| `Pipeline not found` | Pipeline 이름 잘못됨 | 이름 확인 |
| `Already in pipeline` | 이미 해당 Pipeline | 스킵 |
| `Cannot close` | 권한 없음 | 수동 처리 필요 |

### 복구 전략

```
1. 에러 로그 기록
2. 현재 상태 반환
3. 실패 보고 (success: false)
```

---

## 핵심 규칙

1. **상태 추적**: 모든 이동 전후 상태 기록
2. **부모 자동 관리**: 자식 완료 시 부모 자동 확인
3. **멱등성**: 같은 Pipeline으로 이동 시 안전하게 스킵
4. **에러 허용**: 실패 시에도 워크플로우 계속
5. **로그 상세**: 모든 상태 변경 상세 로그

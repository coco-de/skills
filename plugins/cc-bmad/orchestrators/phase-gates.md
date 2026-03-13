---
name: Phase Gates
description: BMAD 페이즈 게이트 정의 및 검증 규칙
version: 1.0.0
---

# Phase Gates (페이즈 게이트)

각 페이즈를 통과하기 위한 필수 조건과 검증 규칙을 정의합니다.
**모든 게이트는 강제**이며, 실패 시 다음 페이즈로 진행할 수 없습니다.

## 게이트 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│  강제 게이트 흐름                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Analysis Gate ──┬─→ ✅ PASS → Planning Gate                   │
│                  └─→ ❌ FAIL → 피드백 루프 (수정 후 재검토)      │
│                                                                 │
│  Planning Gate ──┬─→ ✅ PASS → Solutioning Gate                │
│                  └─→ ❌ FAIL → 피드백 루프 (수정 후 재검토)      │
│                                                                 │
│  Solutioning Gate ──┬─→ ✅ PASS → Implementation               │
│                     └─→ ❌ FAIL → 피드백 루프 (수정 후 재검토)   │
│                                                                 │
│  Implementation Gate ──┬─→ ✅ PASS → 완료                       │
│                        └─→ ❌ FAIL → 피드백 루프                 │
│                                                                 │
│  ⚠️ 게이트 실패 시 다음 페이즈 진행 불가                        │
│  ⚠️ 피드백 반영 후 해당 페르소나 재검토 필수                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Gate 1: Analysis Gate

### 검증 주체
- **Analyst** 페르소나

### 필수 조건

| 조건 | 검증 방법 | 실패 시 |
|------|----------|---------|
| 요구사항 명확성 | 구체적이고 측정 가능한가? | 요구사항 재정의 필요 |
| 스코프 적절성 | 단일 이슈로 적절한 크기인가? | 분할 또는 조정 필요 |
| **Acceptance Criteria BDD Gherkin 형식** | **모든 Acceptance Criteria가 Given-When-Then 형식인가?** | **Gherkin 형식으로 재작성** |
| Acceptance Criteria 완성도 | happy-path + error-handling 각 1개 이상인가? | 시나리오 추가 필요 |

### 검증 로직

```typescript
interface AnalysisGateResult {
  pass: boolean;
  checks: {
    requirementClarity: CheckResult;
    scopeAppropriateness: CheckResult;
    acGherkinFormat: CheckResult;   // BDD Gherkin 형식 필수
    acCompleteness: CheckResult;    // happy-path + error-handling
  };
  acceptanceCriteria: GherkinFeature;  // Gherkin 형식 Acceptance Criteria
  feedback?: string;
}

interface GherkinFeature {
  feature: string;
  scenarios: GherkinScenario[];
}

interface GherkinScenario {
  tag: '@happy-path' | '@error-handling' | '@edge-case';
  name: string;
  given: string[];
  when: string[];
  then: string[];
}

function validateAnalysisGate(analysis: AnalysisOutput): AnalysisGateResult {
  const checks = {
    requirementClarity: checkRequirementClarity(analysis),
    scopeAppropriateness: checkScopeAppropriateness(analysis),
    acGherkinFormat: checkACGherkinFormat(analysis),  // Given-When-Then 형식 검증
    acCompleteness: checkACCompleteness(analysis),    // 태그별 시나리오 존재 검증
  };

  const pass = Object.values(checks).every(c => c.status === "pass");

  return {
    pass,
    checks,
    acceptanceCriteria: analysis.acceptanceCriteria,
    feedback: pass ? undefined : generateFeedback(checks),
  };
}

// BDD Gherkin 형식 검증
function checkACGherkinFormat(analysis: AnalysisOutput): CheckResult {
  const scenarios = analysis.acceptanceCriteria.scenarios;
  const allValid = scenarios.every(s =>
    s.given.length > 0 && s.when.length > 0 && s.then.length > 0
  );
  return {
    status: allValid ? 'pass' : 'fail',
    message: allValid
      ? '모든 AC가 Given-When-Then 형식으로 작성됨'
      : 'AC가 Gherkin 형식이 아님. Given-When-Then으로 재작성 필요',
  };
}

// Acceptance Criteria 완성도 검증
function checkACCompleteness(analysis: AnalysisOutput): CheckResult {
  const scenarios = analysis.acceptanceCriteria.scenarios;
  const hasHappyPath = scenarios.some(s => s.tag === '@happy-path');
  const hasErrorHandling = scenarios.some(s => s.tag === '@error-handling');

  const pass = hasHappyPath && hasErrorHandling;
  return {
    status: pass ? 'pass' : 'fail',
    message: pass
      ? `@happy-path: ${scenarios.filter(s => s.tag === '@happy-path').length}개, @error-handling: ${scenarios.filter(s => s.tag === '@error-handling').length}개`
      : `필수 시나리오 누락: ${!hasHappyPath ? '@happy-path ' : ''}${!hasErrorHandling ? '@error-handling' : ''}`,
  };
}
```

### 출력 형식

```
╔════════════════════════════════════════════════════════════════╗
║  Analysis Gate: {PASS | FAIL}                                  ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ 요구사항 명확성: PASS                                       ║
║     - 기능 요구사항 3개 식별                                    ║
║     - 성공 조건 명확                                           ║
║                                                                ║
║  ✅ 스코프 적절성: PASS                                         ║
║     - 예상 복잡도: 중간 (3-5 SP)                               ║
║     - 단일 이슈로 적절                                         ║
║                                                                ║
║  ✅ Acceptance Criteria BDD Gherkin 형식: PASS                   ║
║     - 모든 AC가 Given-When-Then 형식으로 작성됨                 ║
║                                                                ║
║  ✅ Acceptance Criteria 완성도: PASS                             ║
║     - @happy-path: 2개                                         ║
║     - @error-handling: 1개                                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

📋 Acceptance Criteria (BDD Gherkin):

Feature: 저자 목록 화면

  @happy-path
  Scenario: 저자 목록 페이지네이션 표시
    Given 저자 목록 화면에 있다
    When 화면을 로드한다
    Then 페이지당 20명의 저자가 표시된다
    And 페이지네이션이 표시된다

  @happy-path
  Scenario: 저자 이름으로 검색
    Given 저자 "김철수"가 등록되어 있다
    When 검색창에 "김철수"를 입력한다
    Then 검색 결과에 "김철수"가 포함된다

  @error-handling
  Scenario: 검색 결과 없음
    Given 저자 목록이 존재한다
    When 존재하지 않는 이름을 검색한다
    Then "검색 결과가 없습니다" 메시지가 표시된다
```

---

## Gate 2: Planning Gate

### 검증 주체
- **Product Manager** 페르소나

### 필수 조건

| 조건 | 검증 방법 | 실패 시 |
|------|----------|---------|
| Epic/Story 구조 | 적절한 계층 구조인가? | 구조 재설계 필요 |
| Story Point | 1-8 SP 범위인가? | 재산정 또는 분할 필요 |
| 라벨링 | Type, Scope 라벨이 있는가? | 라벨 추가 필요 |
| 의존성 | 블로커가 해결 가능한가? | 의존성 해결 필요 |

### 검증 로직

```typescript
interface PlanningGateResult {
  pass: boolean;
  checks: {
    epicStoryStructure: CheckResult;
    storyPoint: CheckResult;
    labeling: CheckResult;
    dependencies: CheckResult;
  };
  issue: IssueInfo;
  feedback?: string;
}

function validatePlanningGate(planning: PlanningOutput): PlanningGateResult {
  const checks = {
    epicStoryStructure: checkEpicStoryStructure(planning),
    storyPoint: checkStoryPoint(planning),  // 1-8 범위
    labeling: checkLabeling(planning),  // Type, Scope 필수
    dependencies: checkDependencies(planning),  // 블로커 없거나 해결 가능
  };

  const pass = Object.values(checks).every(c => c.status === "pass");

  return {
    pass,
    checks,
    issue: planning.issue,
    feedback: pass ? undefined : generateFeedback(checks),
  };
}
```

### Story Point 규칙

| Point | 조건 | 분할 필요 |
|-------|------|----------|
| 1 | 단일 파일, 명확한 변경 | ❌ |
| 2-3 | 여러 파일, 테스트 포함 | ❌ |
| 5 | 여러 레이어, BDD 포함 | ❌ |
| 8 | 전체 Feature + 테스트 | ❌ |
| 13+ | 너무 큼 | ✅ 분할 필요 |

---

## Gate 3: Solutioning Gate

### 검증 주체
- **Architect** + **UX Designer** (병렬)

### 필수 조건

#### Architect 검토

| 조건 | 검증 방법 | 실패 시 |
|------|----------|---------|
| Clean Architecture | 레이어 분리가 올바른가? | 아키텍처 수정 |
| DI 구조 | Injectable 등록이 완전한가? | DI 수정 |
| API 설계 | 네이밍/에러처리가 표준인가? | API 수정 |
| 보안 | 인증/인가가 적절한가? | 보안 수정 |

#### UX Designer 검토

| 조건 | 검증 방법 | 실패 시 |
|------|----------|---------|
| CoUI 준수 | 표준 컴포넌트 사용인가? | UI 수정 |
| 레이아웃 | 일관된 간격/정렬인가? | 레이아웃 수정 |
| 상호작용 | 로딩/에러/빈 상태 처리인가? | UX 수정 |
| 접근성 | WCAG 2.1 AA 기준인가? | 접근성 개선 (권장) |

### 병렬 검증 로직

```typescript
interface SolutioningGateResult {
  pass: boolean;
  architectReview: ArchitectReviewResult;
  uxReview: UXReviewResult;
  feedback?: string;
}

async function validateSolutioningGate(
  solutioning: SolutioningOutput
): Promise<SolutioningGateResult> {
  // 병렬 실행
  const [architectReview, uxReview] = await Promise.all([
    validateArchitectReview(solutioning),
    validateUXReview(solutioning),
  ]);

  // 모든 검토가 통과해야 함
  const pass = architectReview.pass && uxReview.pass;

  return {
    pass,
    architectReview,
    uxReview,
    feedback: pass ? undefined : combineFeedback(architectReview, uxReview),
  };
}
```

### 부분 실패 처리

```
┌─────────────────────────────────────────────────────────────────┐
│  Solutioning Gate 부분 실패 시                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Case 1: Architect만 실패                                       │
│  → UX 검토 결과 유지, Architect 피드백 반영 후 재검토           │
│                                                                 │
│  Case 2: UX만 실패                                              │
│  → Architect 결과 유지, UX 피드백 반영 후 재검토                │
│                                                                 │
│  Case 3: 둘 다 실패                                             │
│  → 모든 피드백 반영 후 둘 다 재검토                             │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Gate 4: Implementation Gate

### 검증 주체
- **Flutter Developer** + **Backend Developer** + **Scrum Master**

### 필수 조건

| 조건 | 검증 방법 | 실패 시 |
|------|----------|---------|
| 브랜치 규칙 | feature 브랜치인가? | 브랜치 재생성 |
| 코드 품질 | dart/dcm analyze 통과? | 린트 수정 |
| 테스트 | 모든 테스트 통과? | 테스트 수정 |
| 코드 리뷰 | 리뷰 피드백 반영? | 피드백 반영 |

### 세부 게이트

#### Step 4 Gate: 브랜치 검증

```bash
# 브랜치 형식 검증
BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ ! $BRANCH =~ ^(feature|fix|refactor|chore)/[0-9]+ ]]; then
  echo "❌ 브랜치 형식 오류"
  exit 1
fi

# development/main 직접 커밋 금지
if [[ $BRANCH == "development" || $BRANCH == "main" ]]; then
  echo "❌ development/main에 직접 커밋 금지"
  exit 1
fi
```

#### Step 8.5 Gate: Pre-push 린트 검증

```bash
# 변경 파일 추출 (생성 파일 제외)
CHANGED_FILES=$(git diff --name-only origin/development...HEAD -- '*.dart' | \
  grep -v -E '\.(g|freezed|gr|config|module)\.dart$')

# dart + dcm 포맷팅
echo "$CHANGED_FILES" | xargs dart format
echo "$CHANGED_FILES" | xargs dcm format

# dart fix
dart fix --apply

# 분석 검증
echo "$CHANGED_FILES" | xargs dart analyze --no-fatal-infos
echo "$CHANGED_FILES" | xargs dcm analyze --no-fatal-style
```

#### Step 9 Gate: PR 생성 전 검증

```typescript
interface PRCreationGate {
  branchFormat: boolean;    // feature/번호-설명 형식
  issueLinked: boolean;     // 이슈 번호 추출 가능
  commitsExist: boolean;    // 1개 이상 커밋 존재
  lintPassed: boolean;      // Step 8.5 통과
}
```

---

## 긴급 상황 처리

### Emergency 모드

```bash
# 긴급 핫픽스 (관리자 승인 필요)
/workflow --bmad --emergency "프로덕션 장애 긴급 수정"
```

Emergency 모드에서는:
- Analysis, Planning, Solutioning 게이트 간소화
- 코드 리뷰는 사후 검토로 전환
- 머지 후 반드시 정상 리뷰 진행

### 게이트 우회 금지

```
⚠️ 경고: 게이트 우회는 Emergency 모드에서만 허용됩니다.

일반 모드에서 게이트 우회 시도 시:
1. 경고 메시지 표시
2. 진행 차단
3. 담당 페르소나에게 에스컬레이션
```

---

## 피드백 루프

### 재시도 제한 ⚠️

**최대 재시도 횟수: 3회** (무한 루프 방지)

```
┌─────────────────────────────────────────────────────────────────┐
│  재시도 제한 정책                                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  시도 1 → 실패 → 피드백 제공 → 수정                              │
│  시도 2 → 실패 → 피드백 제공 → 수정                              │
│  시도 3 → 실패 → ⛔ 에스컬레이션                                 │
│                                                                 │
│  3회 실패 시:                                                    │
│  1. Scrum Master에게 에스컬레이션                               │
│  2. 원인 분석 및 근본 문제 해결 필요                             │
│  3. 필요 시 요구사항 재정의 또는 작업 분할                       │
│                                                                 │
│  설정: bmad.json → feedback.maxRetries: 3                       │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 실패 시 처리 흐름

```
게이트 실패 (시도 N < 3)
    ↓
피드백 생성
    ↓
수정 사항 안내
    ↓
사용자 수정 작업
    ↓
재검토 요청
    ↓
해당 페르소나 재검토
    ↓
게이트 재평가

게이트 실패 (시도 N = 3)
    ↓
⛔ 에스컬레이션
    ↓
Scrum Master 개입
    ↓
원인 분석 → 작업 분할 또는 재정의
```

### 재검토 요청

```bash
# 특정 페르소나 재검토
/bmad:review --persona architect --retry

# 특정 게이트 재검증
/bmad:gate --phase solutioning --retry
```

---

## 메트릭스 수집

### 게이트 통과율

```typescript
interface GateMetrics {
  phase: string;
  totalAttempts: number;
  passedFirstTime: number;
  passedAfterRetry: number;
  averageRetries: number;
  commonFailureReasons: string[];
}
```

### 모니터링 대시보드

```
╔════════════════════════════════════════════════════════════════╗
║  Gate Metrics (최근 30일)                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Analysis Gate:     92% 첫 시도 통과                           ║
║  Planning Gate:     88% 첫 시도 통과                           ║
║  Solutioning Gate:  75% 첫 시도 통과                           ║
║  Implementation:    85% 첫 시도 통과                           ║
║                                                                ║
║  주요 실패 사유:                                               ║
║  1. Clean Architecture 위반 (25%)                              ║
║  2. 린트 오류 (20%)                                            ║
║  3. Acceptance Criteria 불명확 (15%)                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 관련 파일

- `.claude/orchestrators/bmad-orchestrator.md` - 메인 오케스트레이터
- `.claude/personas/` - 각 페르소나의 검토 기준
- `.claude/skills/workflow/SKILL.md` - 기존 워크플로우 통합

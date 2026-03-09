---
name: session:wrap
description: "세션 종료 시 .claude/ 문서 자동 업데이트"
invoke: /session:wrap
aliases: ["/wrap", "/sw"]
category: petmedi-automation
complexity: medium
---

# /session:wrap

> 세션 진행 중 학습한 내용을 `.claude/` 디렉토리 문서에 자동 반영

## Triggers

- 세션 종료 직전
- 중요한 패턴/규칙 발견 후
- 새로운 자동화 가능 작업 발견 시
- 문서 업데이트가 필요할 때

## 사용법

```bash
# 전체 세션 분석 및 문서 업데이트
/session:wrap

# 특정 영역만 업데이트
/session:wrap --scope rules      # 규칙만 업데이트
/session:wrap --scope commands   # 커맨드만 업데이트
/session:wrap --scope agents     # 에이전트만 업데이트

# 드라이런 (변경사항 미리보기) - 권장
/session:wrap --dry-run
```

> **권장**: 처음 사용 시 `--dry-run` 옵션으로 변경사항을 먼저 확인하세요.
> 실제 파일 수정 전에 어떤 내용이 추가/수정되는지 미리 검토할 수 있습니다.

---

## 실행 흐름 (2 Phase)

```
┌─────────────────────────────────────────────────────────────────┐
│                    /session:wrap                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│  ║ Phase 1: 병렬 분석 (4 Agents)                              ║   │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌────────────┐│
│  │ doc-updater │ │ automation  │ │ learning    │ │ followup   ││
│  │   Agent     │ │   -scout    │ │ -extractor  │ │ -suggester ││
│  └──────┬──────┘ └──────┬──────┘ └──────┬──────┘ └─────┬──────┘│
│         │               │               │              │        │
│         ▼               ▼               ▼              ▼        │
│  ┌────────────────────────────────────────────────────────────┐│
│  │                   분석 결과 수집                            ││
│  └────────────────────────────────────────────────────────────┘│
│                                                                 │
│  ═══════════════════════════════════════════════════════════   │
│  ║ Phase 2: 순차 처리 (1 Agent)                              ║   │
│  ═══════════════════════════════════════════════════════════   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │             duplicate-checker Agent                      │   │
│  │    - 중복 콘텐츠 검사                                     │   │
│  │    - 충돌 해결                                           │   │
│  │    - 최종 문서 정리                                      │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                  결과 요약 출력                           │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: 병렬 분석 에이전트

### 1. doc-updater Agent

CLAUDE.md 및 관련 문서를 세션 내용 기반으로 업데이트

**분석 대상**:
- 새로 발견된 코딩 컨벤션
- 추가된 프로젝트 설정
- 변경된 아키텍처 패턴
- 새로운 의존성/패키지

**출력**:
```yaml
updates:
  - file: CLAUDE.md
    section: "## Architecture and Structure"
    action: append
    content: "새로운 아키텍처 패턴 설명..."
  - file: .claude/rules/naming.md
    section: "### 네이밍 규칙"
    action: update
    content: "업데이트된 네이밍 규칙..."
```

### 2. automation-scout Agent

새로운 자동화 가능 패턴 탐지

**분석 대상**:
- 반복적으로 수행된 작업
- 수동으로 처리한 패턴화 가능 작업
- 새로운 스킬로 만들 수 있는 작업

**출력**:
```yaml
automatable_patterns:
  - pattern: "BLoC 이벤트 추가 시 State도 함께 추가"
    frequency: 3
    suggestion: "bloc-event-state-pair 스킬 생성 권장"
  - pattern: "테스트 파일 생성 후 항상 같은 import 추가"
    frequency: 5
    suggestion: "test-template 스킬에 auto-import 추가"
```

### 3. learning-extractor Agent

세션에서 학습한 규칙/패턴 추출

**분석 대상**:
- 수정된 코드 패턴
- 해결된 에러와 해결책
- 사용자 피드백으로 학습한 선호도
- 프로젝트 특화 규칙

**출력**:
```yaml
learnings:
  - type: rule
    category: "코드 스타일"
    content: "dot shorthand 적극 사용 (.start, .center 등)"
    evidence: "사용자가 불필요한 전체 타입명 사용 지적"
  - type: pattern
    category: "BLoC"
    content: "await 후 isClosed 체크 필수"
    evidence: "린트 에러로 여러 번 수정"
```

### 4. followup-suggester Agent

후속 작업 제안

**분석 대상**:
- 완료되지 않은 TODO
- 언급된 개선 사항
- 발견된 기술 부채
- 다음 세션에서 할 작업

**출력**:
```yaml
followups:
  - priority: high
    task: "console_author_management 테스트 커버리지 80% 달성"
    reason: "현재 45% - 주요 기능 테스트 누락"
  - priority: medium
    task: "저자 검색 API 최적화"
    reason: "100건 이상 시 2초 이상 소요"
```

---

## Phase 2: 순차 처리 에이전트

### 5. duplicate-checker Agent

중복 콘텐츠 검사 및 정리

**처리 내용**:
- Phase 1 결과 중복 검사
- 기존 문서와의 충돌 해결
- 일관성 검증
- 최종 변경사항 적용

**출력**:
```yaml
deduplication_result:
  removed_duplicates: 2
  merged_entries: 1
  conflicts_resolved: 0
  final_changes:
    - file: CLAUDE.md
      lines_added: 15
      lines_removed: 3
    - file: .claude/rules/bloc-patterns.md
      lines_added: 8
      lines_removed: 0
```

---

## 세부 구현

### 메인 실행 로직

```typescript
async function sessionWrap(options: WrapOptions) {
  // Phase 1: 병렬 분석
  const [docUpdates, automations, learnings, followups] = await Promise.all([
    Task({
      subagent_type: "session-doc-updater",
      prompt: "세션 대화 내용을 분석하여 문서 업데이트 제안",
    }),
    Task({
      subagent_type: "session-automation-scout",
      prompt: "자동화 가능한 패턴 탐지",
    }),
    Task({
      subagent_type: "session-learning-extractor",
      prompt: "학습된 규칙/패턴 추출",
    }),
    Task({
      subagent_type: "session-followup-suggester",
      prompt: "후속 작업 제안",
    }),
  ]);

  // Phase 2: 순차 처리
  const finalResult = await Task({
    subagent_type: "session-duplicate-checker",
    prompt: `
      다음 Phase 1 결과를 검토하고 중복/충돌을 해결하세요:

      ## Doc Updates
      ${JSON.stringify(docUpdates)}

      ## Automations
      ${JSON.stringify(automations)}

      ## Learnings
      ${JSON.stringify(learnings)}

      ## Followups
      ${JSON.stringify(followups)}
    `,
  });

  // 결과 출력
  displayWrapSummary(finalResult);
}
```

---

## 출력 형식

### 진행 상황

```
╔════════════════════════════════════════════════════════════════╗
║  /session:wrap Progress                                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Phase 1: 병렬 분석 [████████████░░░░] 75%                    ║
║                                                                ║
║  ✅ doc-updater: 3개 문서 업데이트 제안                        ║
║  ✅ automation-scout: 2개 자동화 패턴 발견                     ║
║  🔄 learning-extractor: 분석 중...                            ║
║  ⏳ followup-suggester: 대기 중                               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 완료 시

```
╔════════════════════════════════════════════════════════════════╗
║  Session Wrap Complete                                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📝 문서 업데이트                                              ║
║  ├── CLAUDE.md: +15 lines (코딩 컨벤션 추가)                  ║
║  ├── .claude/rules/bloc-patterns.md: +8 lines                 ║
║  └── .claude/commands/session/wrap.md: 신규 생성              ║
║                                                                ║
║  🤖 자동화 제안                                                ║
║  ├── bloc-event-state-pair 스킬 생성 권장                     ║
║  └── test-template auto-import 추가 권장                      ║
║                                                                ║
║  📚 학습 내용                                                  ║
║  ├── [규칙] dot shorthand 적극 사용                           ║
║  ├── [규칙] await 후 isClosed 체크 필수                       ║
║  └── [패턴] ZenHub issueTypeId 필수 지정                      ║
║                                                                ║
║  📋 후속 작업                                                  ║
║  ├── [높음] 테스트 커버리지 80% 달성                          ║
║  └── [중간] 저자 검색 API 최적화                              ║
║                                                                ║
║  🔄 중복 제거: 2건                                            ║
║  ⚠️ 충돌 해결: 0건                                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 대상 파일

### 분석 대상

| 경로 | 설명 |
|------|------|
| `CLAUDE.md` | 프로젝트 메인 가이드 |
| `.claude/rules/**/*.md` | 코딩 규칙 |
| `.claude/commands/**/*.md` | 스킬/에이전트 정의 |
| `.claude/settings.local.json` | 로컬 설정 |

### 출력 대상

| 경로 | 설명 |
|------|------|
| `CLAUDE.md` | 컨벤션, 아키텍처 업데이트 |
| `.claude/rules/` | 새 규칙 파일 생성 |
| `.claude/commands/` | 새 스킬/에이전트 생성 |
| `.claude/session-logs/` | 세션 요약 저장 (선택) |

---

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--scope` | all | 분석 범위 (all/rules/commands/agents) |
| `--dry-run` | false | 변경사항 미리보기만 |
| `--auto-commit` | false | 변경사항 자동 커밋 |
| `--skip-duplicates` | false | 중복 검사 스킵 |

---

## 관련 에이전트

- `session-doc-updater` - 문서 업데이트 분석
- `session-automation-scout` - 자동화 패턴 탐지
- `session-learning-extractor` - 학습 내용 추출
- `session-followup-suggester` - 후속 작업 제안
- `session-duplicate-checker` - 중복 검사 및 정리

---

## 컨텍스트 전달

하위 에이전트가 세션 대화 내용에 접근하는 방법:

### 자동 컨텍스트 (기본)

Claude Code의 Task tool은 `general-purpose` 에이전트에 현재 대화 컨텍스트를 자동 전달합니다.
하위 에이전트는 이전 대화 내용을 참조하여 분석을 수행합니다.

```typescript
// 에이전트 호출 시 컨텍스트 자동 포함
Task({
  subagent_type: "Explore",  // general-purpose 계열
  prompt: "세션에서 학습한 규칙 추출",
  // 이전 대화 내용이 자동으로 에이전트에 전달됨
});
```

### 명시적 컨텍스트 전달

특정 정보를 명시적으로 전달해야 하는 경우:

```typescript
Task({
  subagent_type: "session-learning-extractor",
  prompt: `
    ## 분석 대상 세션 정보

    ### 수정된 파일
    - ${modifiedFiles.join('\n- ')}

    ### 사용자 피드백
    - ${userFeedbacks.join('\n- ')}

    ### 발생한 에러
    - ${errors.join('\n- ')}

    위 정보를 기반으로 학습된 규칙/패턴을 추출하세요.
  `,
});
```

### 컨텍스트 제한사항

| 항목 | 접근 가능 | 비고 |
|------|----------|------|
| 현재 세션 대화 | O | 자동 전달 |
| 이전 세션 대화 | X | 세션 간 격리 |
| 파일 시스템 | O | Read, Glob, Grep 도구 |
| Git 히스토리 | O | Bash 도구 통해 |

---

## 핵심 규칙

1. **비파괴적 업데이트**: 기존 내용 삭제보다 추가/수정 우선
2. **근거 기반**: 모든 변경에 세션 내 근거 명시
3. **일관성 유지**: 기존 문서 스타일과 일관성 유지
4. **중복 방지**: 같은 내용 중복 추가 방지
5. **사용자 확인**: 중요 변경은 사용자 확인 후 적용

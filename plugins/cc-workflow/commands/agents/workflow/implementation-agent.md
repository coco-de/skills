# Implementation Agent

> 이슈 내용 기반 코드 작업 및 커밋 에이전트

## 역할 및 책임

이 에이전트는 ZenHub/GitHub 이슈의 내용을 분석하여 코드를 구현하고 커밋합니다.

1. **이슈 분석**: Acceptance Criteria 및 요구사항 파싱
2. **서브에이전트 호출**: 적절한 레이어 에이전트 위임
3. **증분 커밋**: 작업 단위별 커밋 생성
4. **진행 추적**: TodoWrite로 작업 진행 추적

---

## 입력 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `issue_number` | ✅ | number | GitHub 이슈 번호 |
| `issue_body` | ✅ | string | 이슈 상세 내용 |
| `issue_type` | ✅ | string | `Feature` \| `Task` \| `Bug` \| `Sub-task` |
| `issue_title` | ✅ | string | 이슈 제목 |
| `feature_name` | ❌ | string | Feature 모듈명 (자동 추출 가능) |

---

## 출력

```typescript
interface ImplementationResult {
  success: boolean;
  commits: Commit[];
  files_changed: string[];
  tests_created: string[];
  error?: string;
}

interface Commit {
  hash: string;
  message: string;
  files: string[];
}
```

---

## 이슈 분석 패턴

### Acceptance Criteria 파싱

이슈 본문에서 Acceptance Criteria 섹션을 추출합니다:

```markdown
## ✅ 인수 기준 (Acceptance Criteria)

### AC1: 목록 로딩
```gherkin
Given 앱이 실행됨
When 커뮤니티 페이지로 이동
Then 게시글 목록이 표시됨
```

### AC2: 새로고침
...
```

### 기술 작업 파싱

```markdown
## 🛠️ 기술 작업

### Backend
- [ ] Serverpod endpoint 구현
- [ ] DTO 정의

### Domain
- [ ] Entity 정의
- [ ] Repository Interface 정의
- [ ] UseCase 구현

### Data
- [ ] Repository 구현
- [ ] Serverpod Mixin 구현

### Presentation
- [ ] BLoC 구현
- [ ] Page 위젯 구현
```

---

## 실행 흐름

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 이슈 내용 분석                                    │
├─────────────────────────────────────────────────────────┤
│  - issue_type 확인 (Feature/Task/Bug/Sub-task)          │
│  - Acceptance Criteria 추출                               │
│  - 기술 작업 목록 추출                                     │
│  - feature_name 추출/확인                                 │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: 작업 계획 수립 (TodoWrite)                        │
├─────────────────────────────────────────────────────────┤
│  - 필요한 작업 항목 리스트화                                │
│  - 서브에이전트 호출 순서 결정                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: 서브에이전트 위임 (이슈 타입별)                      │
├─────────────────────────────────────────────────────────┤
│  Feature Story:                                         │
│    → domain-layer-agent → data-layer-agent              │
│    → presentation-layer-agent                           │
│                                                         │
│  Backend Task:                                          │
│    → serverpod-model-agent → serverpod-endpoint-agent   │
│                                                         │
│  Bug:                                                   │
│    → 직접 수정 + 테스트 추가                               │
│                                                         │
│  Sub-task:                                              │
│    → 해당 레이어 에이전트만 호출                            │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: 증분 커밋                                        │
├─────────────────────────────────────────────────────────┤
│  각 서브에이전트 완료 시:                                   │
│  $ git add -A                                           │
│  $ git commit -m "{type}({scope}): {gitmoji} {msg}"     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 5: 테스트 생성 및 실행                                │
├─────────────────────────────────────────────────────────┤
│  - UseCase 테스트 생성                                    │
│  - BLoC 테스트 생성                                       │
│  - Widget 테스트 생성 (BDD)                               │
│  $ melos run test --scope={feature_name}                │
└─────────────────────────────────────────────────────────┘
```

---

## 이슈 타입별 처리

### Feature Story

전체 레이어 구현이 필요한 화면 단위 이슈

```
호출 순서:
0. (Backend 변경 필요 시) Backend 구현
   → serverpod-model-agent (Entity, DTO, Enum)
   → serverpod-endpoint-agent (Endpoint, Service)
   → $ melos run backend:pod:generate [필수]
   → 커밋: feat(backend): ✨ {feature} 백엔드 구현

1. domain-layer-agent (Entity, Repository Interface, UseCase)
   → 커밋: feat({feature}): ✨ domain layer 구현

2. data-layer-agent (Repository 구현체, Mixin)
   → 커밋: feat({feature}): ✨ data layer 구현

3. presentation-layer-agent (BLoC, Page, Widget)
   → 커밋: feat({feature}): ✨ presentation layer 구현
```

⚠️ **Backend 변경 감지**: 이슈에 Backend/Serverpod/API 관련 작업이 포함된 경우,
반드시 Step 0에서 Backend 구현 및 `backend:pod:generate`를 먼저 실행합니다.

### Backend Task

Serverpod 백엔드만 구현하는 이슈

```
호출 순서:
1. serverpod-model-agent (Entity, DTO, Enum)
   → 커밋: feat(backend): ✨ {feature} 모델 생성

2. serverpod-endpoint-agent (Endpoint, Service)
   → 커밋: feat(backend): ✨ {feature} 엔드포인트 구현

3. [필수] Backend 코드 생성
   $ melos run backend:pod:generate
   → 커밋: chore(backend): 🔧 코드 생성

4. (Entity 변경 시) 마이그레이션 생성/적용
   $ melos run backend:pod:create-migration
   $ melos run backend:pod:run-migration
```

⚠️ **중요**: Step 3의 `backend:pod:generate`는 **반드시** 실행해야 합니다.
이 단계를 생략하면 kobic_client에 새로운 모델/엔드포인트가 반영되지 않아
프론트엔드에서 빌드 오류가 발생합니다.

### Bug

버그 수정 이슈

```
처리 방식:
1. 문제 분석 (Serena MCP 활용)
2. 코드 수정
   → 커밋: fix({scope}): 🐛 {bug_description}

3. 회귀 테스트 추가
   → 커밋: test({scope}): ✅ {bug} 회귀 테스트 추가
```

### Sub-task

특정 레이어만 구현하는 세부 작업

```
예시:
- "Entity 정의" → domain-layer-agent만 호출
- "BLoC 구현" → presentation-layer-agent (BLoC만)
- "API 연동" → data-layer-agent (Mixin만)
```

---

## 커밋 메시지 규칙

### 형식

```
{type}({scope}): {gitmoji} {한글 설명}

{선택적 본문}

Refs: #{issue_number}
```

### 타입별 Gitmoji

| Type | Gitmoji | 설명 |
|------|---------|------|
| feat | ✨ | 새 기능 |
| fix | 🐛 | 버그 수정 |
| refactor | ♻️ | 리팩토링 |
| test | ✅ | 테스트 |
| docs | 📝 | 문서 |
| chore | 🔧 | 설정/빌드 |
| style | 💄 | UI/스타일 |

### 예시

```bash
# Domain Layer 구현
git commit -m "feat(community): ✨ Post entity 및 UseCase 구현

- PostEntity 정의
- IPostRepository 인터페이스 정의
- GetPostsUseCase 구현
- GetPostUseCase 구현

Refs: #25"
```

---

## 서브에이전트 위임

### 호출 방식

```typescript
// Domain Layer 위임
Task({
  subagent_type: "domain-layer-agent",
  prompt: `
    feature_name: ${feature_name}
    entity_name: ${entity_name}
    usecases: ${usecases.join(', ')}

    이슈 #{issue_number}의 Domain Layer를 구현해주세요.
  `
});

// Data Layer 위임
Task({
  subagent_type: "data-layer-agent",
  prompt: `
    feature_name: ${feature_name}
    entity_name: ${entity_name}
    caching: swr

    이슈 #{issue_number}의 Data Layer를 구현해주세요.
  `
});
```

### 위임 매핑

| 작업 | 에이전트 |
|------|---------|
| Entity, UseCase | domain-layer-agent |
| Repository 구현 | data-layer-agent |
| BLoC, Page, Widget | presentation-layer-agent |
| Serverpod 모델 | serverpod-model-agent |
| Serverpod 엔드포인트 | serverpod-endpoint-agent |
| 테스트 작성 | test-runner-agent 또는 직접 |

---

## 진행 추적

### TodoWrite 활용

```typescript
TodoWrite([
  { content: "이슈 분석", status: "completed" },
  { content: "Domain Layer 구현", status: "in_progress" },
  { content: "Data Layer 구현", status: "pending" },
  { content: "Presentation Layer 구현", status: "pending" },
  { content: "테스트 작성", status: "pending" },
  { content: "최종 검증", status: "pending" }
]);
```

### 상태 업데이트

각 단계 완료 시 즉시 TodoWrite 업데이트

---

## 에러 처리

### 서브에이전트 실패 시

```
1. 에러 로그 기록
2. 부분 완료 상태 저장
3. 다음 시도를 위한 컨텍스트 보존
4. 실패 보고 (success: false)
```

### 테스트 실패 시

```
1. 실패 테스트 분석
2. 자동 수정 시도 (최대 3회)
3. 수정 후 재실행
4. 여전히 실패 시 → 실패 보고
```

---

## 핵심 규칙

1. **증분 커밋**: 각 레이어 완료 시 즉시 커밋
2. **이슈 참조**: 모든 커밋에 이슈 번호 참조
3. **한글 메시지**: 커밋 메시지 한글로 작성
4. **테스트 필수**: 코드 생성 시 테스트도 함께 생성
5. **진행 추적**: TodoWrite로 실시간 상태 업데이트
6. **실패 허용**: 실패 시 스킵하고 로그 기록

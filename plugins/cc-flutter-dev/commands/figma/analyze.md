---
name: figma:analyze
description: "피그마 프레임 분석 후 요구사항 정의, BDD 시나리오 생성, ZenHub 이슈 생성 및 Feature 생성"
category: petmedi-workflow
complexity: complex
mcp-servers: [playwright, sequential, serena, context7, magic, zenhub]
---

# /figma:analyze

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/figma:analyze` patterns.

## Triggers

- 피그마 디자인을 기반으로 Feature를 생성할 때
- UI 디자인에서 요구사항을 추출할 때
- ZenHub Epic/Story를 자동 생성할 때
- BDD 테스트 시나리오를 생성할 때

## Context Trigger Pattern

```bash
/figma:analyze {figma_urls...} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `figma_urls` | ✅ | 피그마 프레임 URL (공백/쉼표 구분) | 여러 URL |
| `--feature-name` | ❌ | Feature명 (자동 추론) | `community` |
| `--entity-name` | ❌ | Entity명 (자동 추론) | `Post` |
| `--create-zenhub` | ❌ | ZenHub Epic/Story 생성 (기본: true) | `true/false` |
| `--generate-bdd` | ❌ | BDD 시나리오 생성 (기본: true) | `true/false` |
| `--zenhub-labels` | ❌ | 추가 ZenHub 라벨 | `"sprint-1,mvp"` |
| `--skip-feature` | ❌ | Feature 코드 생성 건너뛰기 | `true/false` |
| `--auto-create` | ❌ | 분석 후 자동 생성 | `true/false` |
| `--output-dir` | ❌ | 결과물 저장 위치 | `claudedocs/` |

## Behavioral Flow (6 Phases)

### Phase 1: 피그마 프레임 수집

```text
입력된 피그마 URL들을 파싱하고 검증합니다.

지원 URL 형식:
- https://www.figma.com/file/{key}/{name}?node-id={id}
- https://www.figma.com/design/{key}/{name}?node-id={id}
```

**Playwright MCP 사용:**

```javascript
// 각 프레임 캡처
for (const url of figmaUrls) {
  await browser_navigate({ url });
  await browser_snapshot();  // 접근성 트리 캡처
  await browser_take_screenshot({ filename: `frame_${index}.png` });
}
```

**접근 불가 시 대안:**

```markdown
피그마에 직접 접근할 수 없습니다.
다음 중 하나를 선택해 주세요:

1. 스크린샷 파일 경로 제공
2. 화면 설명 직접 입력
3. 피그마 내보내기 이미지 첨부
```

### Phase 2: UI 분석

**Sequential MCP로 체계적 분석:**

각 화면에서 다음을 식별합니다:

```yaml
screen_analysis:
  screen_type: list | detail | form | other

  components:
    - type: AppBar
      elements: [title, search_button, menu]
    - type: ListView
      item_component: Card
      pagination: infinite_scroll
    - type: FAB
      action: navigate_to_create

  data_fields:
    - field: title
      display: text
      editable: true
    - field: thumbnail
      display: image
      editable: true

  user_actions:
    - tap_card: navigate_to_detail
    - tap_fab: navigate_to_create
    - pull_refresh: reload_list
```

### Phase 3: 요구사항 + BDD 시나리오 정의 ⭐ (확장됨)

#### 3.1 요구사항 정의

분석 결과를 구조화된 요구사항으로 변환:

```markdown
# {Feature} 요구사항 명세

## Entity 정의

### {Entity}
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| id | int | ✅ | 고유 식별자 |
| title | String | ✅ | 제목 |
| content | String | ✅ | 내용 |
| category | {Entity}Category | ✅ | 카테고리 |
| imageUrls | List<String>? | ❌ | 이미지 URL 목록 |
| authorId | int | ✅ | 작성자 ID |
| createdAt | DateTime | ✅ | 생성일시 |

### {Entity}Category (Enum)
- general: 일반
- notice: 공지
- event: 이벤트

## 화면 정의

### 1. 목록 화면
- 경로: /{feature}
- 기능: 페이지네이션, 필터, 검색, 정렬
- 컴포넌트: AppBar, FilterBar, ListView, FAB

### 2. 상세 화면
- 경로: /{feature}/{id}
- 기능: 상세 보기, 좋아요, 수정/삭제
- 컴포넌트: SliverAppBar, ContentSection, ActionBar

### 3. 폼 화면
- 경로: /{feature}/create, /{feature}/{id}/edit
- 기능: 생성/수정 폼, 이미지 업로드
- 컴포넌트: Form, ImagePicker, SubmitButton

## API 정의

| 메서드 | 설명 |
|--------|------|
| get{Entity}s | 목록 조회 (페이지네이션) |
| get{Entity} | 단건 조회 |
| create{Entity} | 생성 |
| update{Entity} | 수정 |
| delete{Entity} | 삭제 |
```

#### 3.2 BDD 시나리오 생성 (신규)

**화면 타입별 BDD 시나리오 생성:**

`~/.claude/commands/agents/bdd-scenario-agent.md` 참조

**목록 화면 예시:**

```gherkin
Feature: {feature} 목록
  사용자로서
  {feature} 목록을 보고 싶습니다
  관련 정보를 확인할 수 있도록

  Background:
    Given 앱이 실행 중입니다
    And 로그인되어 있습니다

  @smoke
  Scenario: 목록 로딩 성공
    When {feature} 페이지로 이동합니다
    Then {feature} 목록이 보입니다
    And 최소 1개의 {entity} 카드가 보입니다

  @refresh
  Scenario: 당겨서 새로고침
    Given {feature} 목록 페이지에 있습니다
    When 아래로 당겨서 새로고침합니다
    Then 목록이 갱신됩니다

  @navigation
  Scenario: 카드 탭하여 상세 이동
    Given {feature} 목록 페이지에 있습니다
    When 첫 번째 {entity} 카드를 탭합니다
    Then {entity} 상세 페이지로 이동합니다
```

**출력 파일:**

```
claudedocs/{feature_name}/bdd/
├── scenarios.md              # BDD 시나리오 요약
├── {feature}_list.feature    # 목록 화면 시나리오
├── {feature}_detail.feature  # 상세 화면 시나리오
└── {feature}_form.feature    # 폼 화면 시나리오
```

### Phase 4: ZenHub Epic/Story 생성 ⭐ (신규)

**`--create-zenhub true` (기본값) 시 실행:**

`~/.claude/commands/agents/zenhub-integration-agent.md` 참조

#### 4.1 Epic 생성

```markdown
## Epic 생성

**제목**: [Epic] {feature} 기능 구현

**내용**:
- 비즈니스 가치 설명
- 범위 정의 (포함/제외)
- 기술 노트
- Figma 참조 링크

**라벨**: epic, feature, {feature_name}
```

#### 4.2 Story 생성 (화면 단위)

각 화면에 대해 Story 생성:

```markdown
## Story 목록

| 화면 | 제목 | Point | AC 수 |
|------|------|-------|-------|
| 목록 | [Story] {feature} 목록 화면 | 3 | 8 |
| 상세 | [Story] {feature} 상세 화면 | 3 | 9 |
| 폼 | [Story] {feature} 폼 화면 | 5 | 10 |
```

#### 4.3 Acceptance Criteria 첨부

BDD 시나리오를 Story의 AC로 변환:

```markdown
## 인수 기준 (AC)

### AC1: 목록 로딩 성공
```gherkin
Given 앱이 실행 중입니다
And 로그인되어 있습니다
When {feature} 페이지로 이동합니다
Then {feature} 목록이 보입니다
```
- **Priority**: High
- **Tag**: @smoke
```

**출력 파일:**

```
claudedocs/{feature_name}/zenhub/
├── epic.md                   # Epic 정보
└── stories/
    ├── list_story.md         # 목록 화면 Story
    ├── detail_story.md       # 상세 화면 Story
    └── form_story.md         # 폼 화면 Story
```

### Phase 5: 사용자 확인

```markdown
## 📋 분석 결과 확인

### Entity 필드
| 필드 | 타입 | 필수 |
|------|------|------|
| title | String | ✅ |
| content | String | ✅ |
| category | {Entity}Category | ✅ |
| imageUrls | List<String>? | ❌ |

### 식별된 화면
- 목록 화면 (8개 BDD 시나리오)
- 상세 화면 (9개 BDD 시나리오)
- 폼 화면 (10개 BDD 시나리오)

### ZenHub Issues
- Epic: [Epic] {feature} 기능 구현
- Stories: 3개 (총 11 Point)

### 추천 설정
- 캐싱: SWR
- 엔드포인트: App only

---

**다음 작업을 선택해 주세요:**

1. ✅ Feature 코드 생성 진행
2. ✏️ 요구사항 수정
3. 📝 BDD 시나리오 수정
4. 🎫 ZenHub 이슈만 생성
5. ❌ 취소
```

### Phase 6: Feature + BDD 테스트 생성

**확인 후 실행:**

```bash
/feature:create {feature_name} {entity_name}
  --location application
  --caching swr
  --fields "title:String, content:String, category:{Entity}Category, imageUrls:List<String>?"
  --with-bdd true
```

**BDD 테스트 파일 복사:**

```bash
# claudedocs에서 feature 테스트 디렉토리로 복사
cp claudedocs/{feature}/bdd/*.feature feature/application/{feature}/test/src/bdd/

# Step 정의 생성
/bdd:generate {feature_name}

# BDD 테스트 코드 생성
melos run test:bdd:generate --scope={feature_name}
```

## Output Files

```text
claudedocs/{feature_name}/
├── figma_analysis.md          # 피그마 분석 결과
├── requirements.md            # 요구사항 명세
├── screenshots/               # 캡처된 스크린샷
│   ├── 01_list.png
│   ├── 02_detail.png
│   └── 03_form.png
├── bdd/                       # BDD 시나리오 (신규)
│   ├── scenarios.md
│   ├── {feature}_list.feature
│   ├── {feature}_detail.feature
│   └── {feature}_form.feature
├── zenhub/                    # ZenHub 이슈 (신규)
│   ├── epic.md
│   └── stories/
│       ├── list_story.md
│       ├── detail_story.md
│       └── form_story.md
└── field_mapping.yaml         # 필드 매핑 정보

feature/application/{feature_name}/test/src/bdd/  # BDD 테스트 (신규)
├── {feature}_list.feature
├── {feature}_detail.feature
├── {feature}_form.feature
├── step/
│   └── {feature}_steps.dart
└── hooks/
    └── hooks.dart
```

## MCP Integration

| 단계 | MCP 서버 | 용도 |
|------|----------|------|
| 프레임 수집 | **Playwright** | 피그마 페이지 캡처, 스크린샷 |
| UI 분석 | **Sequential** | 체계적 UI 분석, 컴포넌트 식별 |
| 요구사항 정의 | **Sequential** | 요구사항 구조화 |
| BDD 생성 | **Sequential** | BDD 시나리오 체계화 |
| ZenHub 생성 | **ZenHub** | Epic/Story 생성 |
| Feature 생성 | **Serena, Context7** | 코드 생성, 패턴 참조 |
| UI 컴포넌트 | **Magic** | UI 컴포넌트 생성 |

## Examples

### 기본 사용 (전체 워크플로우)

```bash
/figma:analyze
  "https://www.figma.com/file/abc/App?node-id=1:100"
  "https://www.figma.com/file/abc/App?node-id=1:200"
  "https://www.figma.com/file/abc/App?node-id=1:300"
```

### Feature명 지정 + ZenHub 생성

```bash
/figma:analyze
  "https://www.figma.com/file/abc/App?node-id=1:100"
  --feature-name community
  --entity-name Post
  --zenhub-labels "sprint-1,mvp"
```

### BDD만 생성 (ZenHub 건너뛰기)

```bash
/figma:analyze
  "https://www.figma.com/file/abc/App?node-id=1:100"
  --feature-name community
  --create-zenhub false
  --generate-bdd true
```

### ZenHub만 생성 (Feature 코드 건너뛰기)

```bash
/figma:analyze
  "https://www.figma.com/file/abc/App?node-id=1:100"
  --feature-name community
  --skip-feature true
```

### 스크린샷으로 분석

피그마 접근이 어려운 경우:

```bash
/figma:analyze
  /path/to/list_screen.png
  /path/to/detail_screen.png
  /path/to/form_screen.png
  --feature-name community
```

## 화면 타입별 분석 패턴

### 목록 화면 (List View)

```yaml
indicators:
  - 여러 개의 반복되는 카드/아이템
  - 스크롤 가능한 레이아웃
  - 필터/검색 바
  - FAB (추가 버튼)

extract:
  - 카드 내 필드 (제목, 썸네일, 날짜 등)
  - 필터 옵션 (카테고리, 정렬)
  - 페이지네이션 타입

bdd_scenarios:
  - 목록 로딩 성공
  - 당겨서 새로고침
  - 무한 스크롤
  - 카드 탭 → 상세 이동
  - FAB 탭 → 생성 페이지 이동
  - 필터 적용
  - 빈 목록
  - 로딩 실패
```

### 상세 화면 (Detail View)

```yaml
indicators:
  - 단일 아이템의 전체 정보
  - 큰 이미지/갤러리
  - 액션 버튼 (좋아요, 공유, 수정)
  - 관련 컨텐츠 섹션

extract:
  - 모든 표시 필드
  - 사용자 액션
  - 네비게이션 관계

bdd_scenarios:
  - 상세 정보 표시
  - 좋아요 토글
  - 수정 페이지 이동
  - 삭제 확인
  - 공유하기
  - 뒤로 가기
  - 로딩 실패
```

### 폼 화면 (Form View)

```yaml
indicators:
  - 입력 필드 (TextField, Dropdown 등)
  - 저장/취소 버튼
  - 유효성 검사 메시지

extract:
  - 입력 필드 타입
  - 필수/선택 여부
  - 유효성 규칙

bdd_scenarios:
  - 유효한 폼 제출
  - 필수 필드 누락
  - 글자 수 제한
  - 이미지 첨부/삭제
  - 작성 취소
  - 저장 실패
```

## 참조 에이전트

- **피그마 분석**: `~/.claude/commands/agents/figma-analyzer-agent.md`
- **BDD 시나리오**: `~/.claude/commands/agents/bdd-scenario-agent.md`
- **ZenHub 연동**: `~/.claude/commands/agents/zenhub-integration-agent.md`

## 핵심 규칙

1. **체계적 분석**: Sequential MCP로 단계별 분석
2. **BDD 한글 작성**: Given-When-Then 키워드 + 한글 설명
3. **ZenHub 연동**: Epic → Story 계층 구조
4. **AC 매핑**: BDD 시나리오 = Story AC
5. **사용자 확인**: 생성 전 반드시 확인
6. **문서화**: 분석 결과와 요구사항 문서 생성
7. **점진적 진행**: 불확실한 부분은 질문으로 확인
8. **대안 제공**: 피그마 접근 불가 시 스크린샷 분석

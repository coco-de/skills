---
name: zenhub:create-epic
description: "ZenHub Epic 및 Story 생성 (Feature 요구사항 기반)"
category: petmedi-workflow
complexity: moderate
mcp-servers: [zenhub, sequential]
---

# /zenhub:create-epic

> **Context Framework Note**: 이 명령어는 Feature 요구사항을 기반으로 ZenHub Epic/Story를 생성합니다.

## Triggers

- Feature 요구사항에서 이슈를 생성할 때
- `/figma:analyze` Phase 4에서 호출될 때
- 수동으로 ZenHub 이슈를 생성할 때

## Context Trigger Pattern

```bash
/zenhub:create-epic {feature_name} {entity_name} [--options]
```

## Parameters

### 필수 파라미터

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `feature_name` | Feature명 (snake_case) | `community` |
| `entity_name` | Entity명 (PascalCase) | `Post` |

### 이미지 분석 옵션 (선택)

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `--images` | 분석할 이미지 파일 (쉼표 구분) | `"list.png,detail.png,form.png"` |
| `--images-dir` | 이미지 디렉토리 경로 | `./screenshots/` |
| `--attach-images` | repo에 commit 후 Issue 첨부 (기본: false) | `true/false` |
| `--min-confidence` | 화면 타입 식별 최소 신뢰도 (기본: 70%) | `80` |
| `--skip-analysis` | 이미지 분석 건너뛰기 | `true/false` |
| `--no-cache` | 캐시 무시하고 재분석 | `true/false` |

### 기타 옵션 (선택)

| 파라미터 | 설명 | 예시 |
|---------|------|------|
| `--requirements` | 요구사항 문서 경로 | `claudedocs/community/requirements.md` |
| `--bdd-dir` | BDD 시나리오 디렉토리 | `claudedocs/community/bdd/` |
| `--labels` | 추가 라벨 | `"sprint-1,mvp"` |
| `--screens` | 생성할 화면 | `"list,detail,form"` |
| `--points` | Story Point 설정 | `"3,3,5"` |
| `--sprint` | Sprint 할당 | `"current"` |

## Issue Type IDs (상수)

이슈 생성 시 `issueTypeId` 파라미터에 사용하는 ID 목록입니다.

| Type | ID | Level | 용도 |
|------|-----|-------|------|
| Initiative | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3NzU` | 1 | 최상위 Initiative |
| Project | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3NzY` | 2 | 프로젝트 |
| **Epic** | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzc` | 3 | Epic 생성 시 |
| Bug | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzg` | 4 | 버그 이슈 |
| **Feature** | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3ODA` | 4 | Story/Feature 생성 시 |
| Task | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzk` | 4 | 일반 작업 |
| **Sub-task** | `Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3ODE` | 5 | Sub-task 생성 시 |

## Repository IDs

| Repository | ID | 용도 |
|------------|-----|------|
| **Unibook (ZenHub)** | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx` | ZenHub 자체 이슈 |
| **kobic (GitHub)** | `Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTM0MjA0` | GitHub 이슈 |

---

## Behavioral Flow

### Step 0: 이미지 분석 (--images 제공 시)

`--images` 또는 `--images-dir` 파라미터가 제공된 경우 실행됩니다.

#### 0.1 이미지 로드

**지원 포맷**: PNG, JPG, JPEG, WEBP
**권장 크기**: 최대 5MB/파일, 1920x1080 이하 권장

```bash
# 개별 파일 지정
--images "list.png,detail.png,form.png"

# 디렉토리 지정 (지원 포맷 자동 필터링)
--images-dir ./screenshots/
```

#### 0.2 화면 타입 식별

각 이미지를 Claude 멀티모달로 분석하여 식별:

| 이미지 | 화면 타입 | 신뢰도 | 주요 컴포넌트 |
|--------|----------|--------|--------------|
| list.png | 목록 | 95% | AppBar, ListView, FAB |
| detail.png | 상세 | 90% | SliverAppBar, ContentSection |
| form.png | 폼 | 92% | Form, TextField, Button |

**화면 타입 식별 기준:**
- **목록(List)**: 여러 개의 반복되는 카드/아이템, 스크롤 가능한 레이아웃, FAB
- **상세(Detail)**: 단일 아이템의 전체 정보, 큰 이미지/갤러리, 액션 버튼
- **폼(Form)**: 입력 필드 (TextField, Dropdown 등), 저장/취소 버튼

**신뢰도 임계값** (`--min-confidence`, 기본: 70%):
- 신뢰도가 임계값 미만인 화면은 사용자에게 수동 확인 요청
- 예: `--min-confidence 80` 설정 시 80% 미만 신뢰도는 확인 필요

#### 0.3 Entity 필드 추출

이미지 내 UI 요소에서 Entity 필드 추론:

```yaml
entity:
  name: {EntityName}
  fields:
    - name: title
      type: String
      required: true
      ui_component: TextField
      validation:
        max_length: 100
      source_screen: form.png

    - name: content
      type: String
      required: true
      ui_component: TextArea
      validation:
        max_length: 5000
      source_screen: form.png

    - name: category
      type: "{EntityName}Category"
      required: true
      ui_component: Dropdown
      options: [general, notice, event]
      source_screen: form.png

    - name: imageUrls
      type: "List<String>?"
      required: false
      ui_component: ImagePicker
      validation:
        max_count: 5
      source_screen: form.png
```

#### 0.4 BDD 시나리오 생성

화면 타입에 따라 기본 BDD 시나리오 템플릿 적용합니다.

> **언어**: BDD 시나리오는 **한국어**로 생성됩니다 (프로젝트 컨벤션).

**목록 화면:**
- 목록 로딩 성공
- 당겨서 새로고침
- 무한 스크롤
- 카드 탭 → 상세 이동
- 필터 적용
- 빈 목록

**상세 화면:**
- 상세 정보 표시
- 좋아요 토글
- 수정/삭제
- 뒤로 가기

**폼 화면:**
- 유효한 폼 제출
- 필수 필드 누락
- 이미지 첨부
- 작성 취소

#### 0.5 요구사항 문서 생성

분석 결과를 마크다운으로 저장:

**경로**: `claudedocs/{feature_name}/requirements.md`

```markdown
# {Feature} 요구사항 명세

> 이미지 분석으로 자동 생성됨

## Entity 정의

### {Entity}
| 필드 | 타입 | 필수 | 설명 |
|------|------|------|------|
| title | String | ✅ | 제목 |
| content | String | ✅ | 내용 |
...

## 화면 정의

### 1. 목록 화면 (list.png)
- 컴포넌트: AppBar, ListView, FAB
- 액션: 카드 탭 → 상세 이동, FAB 탭 → 생성
...
```

#### 0.6 이미지 저장 및 URL 생성 (--attach-images true 시)

> **기본값**: `--attach-images`는 기본적으로 **비활성화(false)**입니다.
> 이미지를 repo에 commit하려면 명시적으로 `--attach-images true`를 지정해야 합니다.

이미지를 repo에 저장하고 GitHub raw URL 생성:

> ⚠️ **주의**: 현재 브랜치에 직접 push합니다. Protected branch(main/development)인 경우 실패할 수 있습니다.

**사용자 확인 프롬프트:**
```markdown
🖼️ 이미지를 repo에 commit하시겠습니까?

- 대상 파일: list.png, detail.png, form.png
- 저장 경로: claudedocs/{feature}/screenshots/
- 현재 브랜치: {current_branch}

**계속하시겠습니까? (y/N)**
```

```bash
# 1. 이미지를 claudedocs에 복사
cp {input_images} claudedocs/{feature}/screenshots/

# 2. Git에 추가 (현재 브랜치)
git add claudedocs/{feature}/screenshots/
git commit -m "docs: 📸 {feature} 스크린샷 추가"
git push origin HEAD

# 3. GitHub raw URL 생성
# https://raw.githubusercontent.com/{owner}/{repo}/{branch}/claudedocs/{feature}/screenshots/{image}
```

**Protected Branch 대응:**
- Feature 브랜치에서 실행 권장
- Push 실패 시 이미지 URL 없이 진행 (로컬 경로 사용)

#### 0.7 사용자 확인

```markdown
## 📸 이미지 분석 결과

### 식별된 화면
| # | 이미지 | 화면 타입 | 컴포넌트 수 |
|---|--------|----------|-----------|
| 1 | list.png | 목록 | 5 |
| 2 | detail.png | 상세 | 4 |
| 3 | form.png | 폼 | 6 |

### 추출된 Entity 필드
| 필드 | 타입 | 필수 | 출처 |
|------|------|------|------|
| title | String | ✅ | form.png |
| content | String | ✅ | form.png |
| category | Enum | ✅ | form.png |

### 생성할 BDD 시나리오
- 목록: 8개
- 상세: 6개
- 폼: 7개

**분석 결과가 정확합니까? (Y/n)**
```

#### 0.8 에러 처리

| 상황 | 처리 |
|------|------|
| 이미지 파일 없음 | `❌ 파일을 찾을 수 없습니다: {path}` 출력 후 종료 |
| 지원하지 않는 포맷 | PNG, JPG, JPEG, WEBP만 지원. 다른 포맷은 무시하고 경고 표시 |
| Git push 실패 | 이미지 URL 없이 진행, 로컬 경로 사용 (경고 표시) |
| 분석 신뢰도 < 임계값 | 사용자에게 수동 확인 요청: `⚠️ 신뢰도 {n}% - 화면 타입을 확인해주세요` |
| 디렉토리에 이미지 없음 | `⚠️ 디렉토리에 지원하는 이미지가 없습니다: {path}` 출력 후 종료 |
| Entity 필드 추출 실패 | 빈 필드로 진행, 사용자에게 수동 입력 요청 |

---

### Step 1: 요구사항 로드

**우선순위:**
1. Step 0에서 생성된 요구사항 (`--images` 사용 시)
2. `--requirements`로 지정된 파일
3. 기본 경로: `claudedocs/{feature}/requirements.md`

```markdown
## 요구사항 로드

1. claudedocs/{feature}/requirements.md 읽기
2. BDD 시나리오 파일들 읽기 (있는 경우)
3. Entity 필드 정의 추출
4. 화면 정의 추출
```

### Step 2: Epic 생성

**MCP 호출 예시**:
```javascript
mcp__zenhub__createZenhubIssue({
  title: "[Epic] {feature} 기능 구현",
  body: "{epic_body_template}",
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx",  // Unibook
  issueTypeId: "Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3Nzc",       // Epic
  labels: ["epic", "feature", "{feature_name}"]
})
```

```markdown
## Epic 생성 확인

**제목**: [Epic] {feature} 기능 구현

**내용 미리보기**:
---
# Epic: {Feature} 기능 구현

## 📋 개요
{feature_description}

## 💼 비즈니스 가치
**사용자로서**, {capability}을(를) 원합니다.
**그래서** {value}을(를) 얻을 수 있습니다.

## 📊 범위
- ✅ 목록 화면
- ✅ 상세 화면
- ✅ 폼 화면

## 🛠️ 기술 노트
| 항목 | 값 |
|------|-----|
| Entity | `{EntityName}` |
| Backend | Serverpod endpoint |
| Caching | SWR |
---

**라벨**: epic, feature, {feature_name}, petmedi

**생성하시겠습니까? (Y/n)**
```

### Step 3: Story 생성

확인 후 각 화면별 Story 생성:

**MCP 호출 예시** (각 화면별 반복):
```javascript
mcp__zenhub__createZenhubIssue({
  title: "[Story] {feature} {screen} 화면",
  body: "{story_body_template}",
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx",  // Unibook
  issueTypeId: "Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3ODA",       // Feature (Story)
  parentIssueId: "{epic_id}",                                    // Epic과 연결
  labels: ["story", "{feature_name}", "{screen_type}-view"]
})
```

```markdown
## Story 생성

| # | 화면 | 제목 | Point | AC 수 |
|---|------|------|-------|-------|
| 1 | 목록 | [Story] {feature} 목록 화면 | 3 | 8 |
| 2 | 상세 | [Story] {feature} 상세 화면 | 3 | 9 |
| 3 | 폼 | [Story] {feature} 폼 화면 | 5 | 10 |

**총 Story**: 3개
**총 Point**: 11
```

### Step 3.5: Sub-task 생성 (선택)

Story 하위에 세부 작업을 Sub-task로 생성합니다.

**MCP 호출 예시**:
```javascript
mcp__zenhub__createZenhubIssue({
  title: "[{PREFIX}-00X-0Y] {task_description}",
  body: "{subtask_body}",
  repositoryId: "Z2lkOi8vcmFwdG9yL1JlcG9zaXRvcnkvMTM0NTI1MDkx",  // Unibook
  issueTypeId: "Z2lkOi8vcmFwdG9yL0lzc3VlVHlwZS8yOTg3ODE",       // Sub-task
  parentIssueId: "{story_id}",                                   // Story와 연결
  labels: ["subtask", "{feature_name}", "p{priority}"]
})
```

**화면 타입별 자동 생성 Sub-task**:

| 화면 타입 | Sub-task 목록 |
|---------|--------------|
| **목록** | 테이블 컬럼 정의, 검색 기능, 필터 기능, 정렬 기능, 페이지네이션 |
| **상세** | 데이터 표시, 액션 버튼, 수정/삭제 확인 |
| **폼** | 필드 유효성 검사, 폼 제출, 취소 처리, 이미지 업로드 |

**Sub-task 제목 형식**:
- `[{PREFIX}-001-01]` : Story 001의 첫 번째 Sub-task
- `[{PREFIX}-001-02]` : Story 001의 두 번째 Sub-task
- PREFIX는 feature_name 기반 (예: `AUTH`, `INST`, `BOOK`)

### Step 4: Epic-Story 연결

```markdown
## 연결 완료

✅ Epic #{epic_number} 생성 완료
✅ Story #{story_1} 연결됨
✅ Story #{story_2} 연결됨
✅ Story #{story_3} 연결됨

### 생성된 이슈 링크
- Epic: https://github.com/cocode/petmedi/issues/{epic_number}
- 목록: https://github.com/cocode/petmedi/issues/{story_1}
- 상세: https://github.com/cocode/petmedi/issues/{story_2}
- 폼: https://github.com/cocode/petmedi/issues/{story_3}
```

## Output Files

```
claudedocs/{feature_name}/
├── screenshots/              # 이미지 분석 시 저장 (--images 사용 시)
│   ├── list.png
│   ├── detail.png
│   └── form.png
├── image_analysis.md         # 이미지 분석 결과 (--images 사용 시)
├── requirements.md           # 요구사항 (자동 생성 또는 기존 파일)
├── bdd/                      # BDD 시나리오 (자동 생성)
│   ├── {feature}_list.feature
│   ├── {feature}_detail.feature
│   └── {feature}_form.feature
└── zenhub/
    ├── epic.md               # Epic 상세 정보
    └── stories/
        ├── list_story.md     # 목록 Story 정보
        ├── detail_story.md   # 상세 Story 정보
        └── form_story.md     # 폼 Story 정보
```

## Epic 템플릿

```markdown
# Epic: {Feature} 기능 구현

## 📋 개요
{Feature에 대한 간략한 설명}

## 💼 비즈니스 가치
**사용자로서**, {feature_capability}을(를) 원합니다.
**그래서** {business_value}을(를) 얻을 수 있습니다.

## 📊 범위

### 포함
- ✅ {screen_1} 화면
- ✅ {screen_2} 화면
- ✅ {screen_3} 화면

### 제외
- ❌ (필요시 명시)

## 🛠️ 기술 노트
| 항목 | 값 |
|------|-----|
| Entity | `{EntityName}` |
| Backend | Serverpod endpoint |
| Caching | {SWR / Cache-First} |
| Location | `feature/{location}/{feature_name}` |

## 🎨 디자인 스크린샷

> `--images` 사용 시 자동 생성됨

### 목록 화면
![목록 화면](https://raw.githubusercontent.com/{owner}/{repo}/{branch}/claudedocs/{feature}/screenshots/list.png)

### 상세 화면
![상세 화면](https://raw.githubusercontent.com/{owner}/{repo}/{branch}/claudedocs/{feature}/screenshots/detail.png)

### 폼 화면
![폼 화면](https://raw.githubusercontent.com/{owner}/{repo}/{branch}/claudedocs/{feature}/screenshots/form.png)

> 또는 Figma 링크: {figma_urls}

## 📎 관련 Story
- [ ] #{story_1_number} - 목록 화면
- [ ] #{story_2_number} - 상세 화면
- [ ] #{story_3_number} - 폼 화면

---
> 🤖 Generated by `/zenhub:create-epic`
```

## Story 템플릿

```markdown
# Story: {Screen Name}

## 📋 사용자 스토리
**{user_type}로서**, {screen_capability}을(를) 원합니다.
**그래서** {value}을(를) 얻을 수 있습니다.

## ✅ 인수 기준 (Acceptance Criteria)

### AC1: {scenario_1_name}
```gherkin
Given {precondition_1}
When {action_1}
Then {expected_result_1}
```
- **Priority**: {High/Medium/Low}
- **Tag**: @{tag}

### AC2: {scenario_2_name}
```gherkin
Given {precondition_2}
When {action_2}
Then {expected_result_2}
```
- **Priority**: {High/Medium/Low}
- **Tag**: @{tag}

## 🛠️ 기술 작업

### Backend
- [ ] Serverpod endpoint 구현
- [ ] DTO 정의

### Domain
- [ ] Entity 정의
- [ ] Repository Interface 정의
- [ ] UseCase 구현
- [ ] UseCase 테스트 작성

### Data
- [ ] Repository 구현
- [ ] Serverpod Mixin 구현
- [ ] 캐싱 전략 적용

### Presentation
- [ ] BLoC 구현 (Event/State)
- [ ] Page 위젯 구현
- [ ] Widget 컴포넌트 구현
- [ ] Route 등록
- [ ] BDD 테스트 작성

### Widgetbook
- [ ] Component story 추가

## 🎨 디자인 참조

> `--images` 사용 시 자동 생성됨

![{screen_name}](https://raw.githubusercontent.com/{owner}/{repo}/{branch}/claudedocs/{feature}/screenshots/{screen}.png)

> 또는 Figma 링크: {figma_link}

## 📐 예상 Story Point
{point_value}

---
> 🤖 Generated by `/zenhub:create-epic`
> 📎 Epic: #{epic_number}
```

## MCP Integration

| 작업 | MCP 서버 | 용도 |
|------|----------|------|
| 이슈 생성 | **ZenHub** | Epic/Story 생성 |
| 템플릿 구조화 | **Sequential** | 체계적 이슈 구성 |

## Examples

### 기본 사용

```bash
/zenhub:create-epic community Post
```

### 요구사항 파일 지정

```bash
/zenhub:create-epic community Post \
  --requirements claudedocs/community/requirements.md \
  --bdd-dir claudedocs/community/bdd/
```

### Sprint 및 라벨 지정

```bash
/zenhub:create-epic community Post \
  --labels "sprint-1,mvp" \
  --sprint current
```

### Story Point 커스텀

```bash
/zenhub:create-epic community Post \
  --screens "list,detail,form" \
  --points "5,3,8"
```

### 이미지 파일로 Epic 생성 (신규)

```bash
/zenhub:create-epic community Post \
  --images "list.png,detail.png,form.png"
```

### 이미지 디렉토리로 Epic 생성

```bash
/zenhub:create-epic community Post \
  --images-dir ./screenshots/community/
```

### 이미지 + 추가 옵션

```bash
/zenhub:create-epic community Post \
  --images "list.png,detail.png,form.png" \
  --labels "sprint-1,mvp" \
  --sprint current
```

### 이미지 첨부 없이 분석만

```bash
/zenhub:create-epic community Post \
  --images "list.png,detail.png,form.png" \
  --attach-images false
```

## 참조 에이전트

상세 구현 규칙: `~/.claude/commands/agents/zenhub-integration-agent.md`

## 핵심 규칙

1. **Epic 먼저**: Story 전에 Epic 생성
2. **연결 필수**: 모든 Story는 Epic에 연결
3. **AC 포함**: 각 Story에 BDD 기반 AC 포함
4. **라벨 일관성**: 정해진 라벨 체계 준수
5. **확인 후 생성**: 사용자 확인 후 실제 이슈 생성
6. **문서화**: 생성 결과 claudedocs에 저장
7. **이미지 분석**: `--images` 사용 시 Claude 멀티모달로 상세 분석
8. **이미지 첨부**: `--attach-images true` 시 사용자 확인 후 repo에 commit하여 Issue에 URL 첨부
9. **BDD 언어**: 자동 생성되는 BDD 시나리오는 한국어로 작성

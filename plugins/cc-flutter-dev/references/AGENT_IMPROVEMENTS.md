# Agent Improvement Requirements

> **작성 일시**: 2025-12-17
> **목적**: Community Feature 구현 과정에서 발견된 에이전트 개선 사항

---

## 🎯 개선 필요 에이전트

### 1. `/figma:analyze` 개선

**현재 문제**:
- ❌ 분석만 하고 실제 UI 구현까지 연결되지 않음
- ❌ ZenHub Story에 피그마 프레임 링크가 기록되지 않음

**개선 요구사항**:

#### 1-1. 피그마 프레임 링크 기록

**Story Body에 추가해야 할 내용**:
```markdown
## 🎨 Figma Design

**프레임 링크**:
- [목록 화면](https://www.figma.com/design/QkKRtr51GXgmLdKcKcBqQe/🐶-Petaround?node-id=235-11480)
- [상세 화면](https://www.figma.com/design/...)
- [작성 화면](https://www.figma.com/design/...)
```

**에이전트 동작**:
```
1. 피그마 URL 파싱
2. Story 문서 생성 시 "## 🎨 Figma Design" 섹션 자동 추가
3. 각 화면별 프레임 링크 매핑
```

#### 1-2. 실제 UI 구현 연결

**현재 플로우**:
```
피그마 분석 → 요구사항 문서 → BDD 시나리오 → (끝)
```

**개선된 플로우**:
```
피그마 분석 → 요구사항 문서 → BDD 시나리오 → ZenHub 생성 → UI 구현 → 검증
```

**Phase 추가**:
```
Phase 7: UI 구현 (NEW)
  - /feature:presentation 실행
  - 피그마 스타일 반영
  - 실제 화면 구현

Phase 8: 동작 검증 (NEW)
  - build_runner 실행
  - 테스트 실행
  - 화면 동작 확인
```

---

### 2. ZenHub Issue Body 형식 개선

**현재 문제**:
- ❌ 링크만 제공 (실제 내용 확인 불가)
- ❌ 내용이 길어도 모두 표시 (가독성 저하)

**현재 형식**:
```markdown
## 참조
- [Story 문서](../claudedocs/community/zenhub/stories/list_story.md)
- [BDD Scenarios](../claudedocs/community/bdd/community_list.feature)
```

**개선된 형식** (Details 태그 사용):
```markdown
<details>
<summary>📝 Story 상세 내용 (클릭하여 펼치기)</summary>

## Story 설명
(전체 Story 문서 내용)

</details>

<details>
<summary>✅ Acceptance Criteria (10개)</summary>

### AC1: 목록 로딩 성공
```gherkin
Given the app is running # 앱이 실행됨
...
```

### AC2: 당겨서 새로고침
...

</details>

<details>
<summary>🧪 BDD 테스트 시나리오 (13개)</summary>

```gherkin
Feature: Community 목록 화면
  (전체 BDD Feature 파일 내용)
```

</details>

<details>
<summary>🛠️ 구현 태스크</summary>

### Backend Tasks
- [ ] Post 모델 정의
- [ ] API 구현

### Frontend Tasks
- [ ] Domain Layer
- [ ] Data Layer
- [ ] Presentation Layer

</details>
```

**장점**:
- ✅ Issue 하나로 모든 정보 확인 가능
- ✅ 가독성 향상 (접었다 펼치기)
- ✅ 링크 클릭 없이 바로 확인
- ✅ 오프라인에서도 확인 가능

---

### 3. `/feature:create` 오케스트레이터 개선

**현재 문제**:
- ❌ 기존 feature 존재 시 처리 로직 없음
- ❌ Phase별 실행이 불완전함
- ❌ UI 실제 구현이 누락됨
- ❌ 검증 단계 없음

**개선 요구사항**:

#### 3-1. 기존 Feature 감지

```
1. feature/{location}/{feature_name} 존재 확인
2. 존재하면:
   - 옵션 A: 업데이트 모드
   - 옵션 B: 스킵
   - 옵션 C: 덮어쓰기 (확인 필요)
3. 존재하지 않으면:
   - 전체 생성
```

#### 3-2. Phase별 완전한 실행

**Phase 2: Backend** (현재 OK):
- ✅ Serverpod 모델 생성
- ✅ 엔드포인트 생성
- ✅ 코드 생성
- ✅ 마이그레이션

**Phase 3: Frontend** (개선 필요):
```dart
// 현재: 구조만 생성
/feature:domain → Entity, UseCase, Repository Interface
/feature:data → Repository impl, Mixin
/feature:presentation → BLoC, Page (템플릿만)

// 개선: 실제 동작하는 코드 생성
/feature:domain → (동일)
/feature:data → (동일)
/feature:presentation →
  - BLoC 완전 구현 (Event, State, Logic)
  - Page 완전 구현 (Scaffold, AppBar, Body)
  - Widget 완전 구현 (PostCard with 모든 필드)
  - 피그마 스타일 반영
```

#### 3-3. 실제 UI 구현 보장

**추가해야 할 Step**:
```
Step 7-1: 피그마 분석 정보 로드
  - claudedocs/{feature}/figma_analysis.md 읽기
  - 스타일, 레이아웃 정보 추출

Step 7-2: Widget 실제 구현
  - PostCard: 모든 필드 표시
  - CategoryChip: 스타일 적용
  - SearchBar: 동작 구현

Step 7-3: Page 실제 구현
  - Scaffold 완성
  - BLoC 연결
  - 상태별 UI (Loading, Loaded, Error, Empty)
```

#### 3-4. 검증 단계 추가

**Phase 5: 검증** (강화 필요):
```bash
# 현재
melos run build
melos run test

# 개선
melos run build --scope={feature}
melos run analyze --scope={feature}
melos run test --scope={feature}
melos run test:bdd --scope={feature}  # BDD 테스트 실행
flutter run --target=lib/main_development.dart  # 실제 앱 실행
```

---

## 📋 에이전트 업데이트 체크리스트

### `/figma:analyze` 업데이트

**파일**: `~/.claude/commands/figma/analyze.md` (또는 프로젝트)

**추가 사항**:
- [ ] Phase 6에 "피그마 프레임 링크 Story에 기록" 단계 추가
- [ ] Story 템플릿에 "## 🎨 Figma Design" 섹션 추가
- [ ] URL 파싱 및 매핑 로직

**템플릿**:
```markdown
## 🎨 Figma Design

**프레임 링크**:
- [목록 화면]({figma_url_1})
- [상세 화면]({figma_url_2})
- [작성 화면]({figma_url_3})

**디자인 분석**:
- 컬러: {colors}
- 타이포그래피: {typography}
- 스페이싱: {spacing}
```

---

### ZenHub Issue 템플릿 개선

**파일**: 신규 생성 필요

**Issue Body 템플릿**:
```markdown
# [Story] {title}

> **Story Point**: {point}
> **Sprint**: {sprint}
> **Epic**: #{epic_number}

## 🎨 Figma Design
{figma_links}

<details>
<summary>📝 Story 상세 내용 (클릭하여 펼치기)</summary>

{story_content}

</details>

<details>
<summary>✅ Acceptance Criteria ({ac_count}개)</summary>

{ac_list}

</details>

<details>
<summary>🧪 BDD 테스트 시나리오 ({scenario_count}개)</summary>

```gherkin
{bdd_content}
```

</details>

<details>
<summary>🛠️ 구현 태스크</summary>

{tasks}

</details>

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

### `/feature:create` 오케스트레이터 개선

**파일**: `~/.claude/commands/feature/create.md` (또는 프로젝트)

**추가 Phase**:
```markdown
## Phase 3.5: 피그마 스타일 적용 (NEW)

### Step 3.5-1: 피그마 분석 로드
- claudedocs/{feature}/figma_analysis.md 읽기
- 디자인 토큰 추출 (색상, 폰트, 스페이싱)

### Step 3.5-2: 스타일 적용
- Widget에 피그마 스타일 반영
- 컬러, 타이포그래피, 레이아웃 적용

## Phase 4.5: 실제 동작 구현 (NEW)

### Step 4.5-1: BLoC 로직 완성
- Event handler 실제 구현
- State transition 로직

### Step 4.5-2: Widget 완전 구현
- 모든 필드 표시
- 사용자 인터랙션
- 에러 처리

### Step 4.5-3: Page 완전 구현
- Scaffold 구성
- AppBar, Body, FAB
- 네비게이션 연결
```

**기존 Feature 처리**:
```markdown
## Phase 0: 기존 Feature 확인 (NEW)

### Step 0-1: 존재 여부 확인
```bash
if [ -d "feature/{location}/{feature_name}" ]; then
  echo "Feature already exists"
  # 업데이트 모드
else
  # 전체 생성 모드
fi
```

### Step 0-2: 사용자 확인
- 기존 feature 존재 시:
  - 옵션 1: 업데이트 (필드 추가, UI 개선)
  - 옵션 2: 스킵
  - 옵션 3: 재생성 (기존 백업)
```

---

## 📝 구현 가이드

### Details 태그 생성 함수

```typescript
function createDetailsSection(
  summary: string,
  content: string,
  icon: string = ""
): string {
  return `
<details>
<summary>${icon} ${summary}</summary>

${content}

</details>
`;
}

// 사용 예시
const storyDetails = createDetailsSection(
  "Story 상세 내용 (클릭하여 펼치기)",
  storyContent,
  "📝"
);

const acDetails = createDetailsSection(
  `Acceptance Criteria (${acCount}개)`,
  acContent,
  "✅"
);
```

### Story Body 생성 로직

```typescript
const issueBody = `
# [Story] ${title}

> **Story Point**: ${point}
> **Sprint**: ${sprint}
> **Epic**: #${epicNumber}

## 🎨 Figma Design
${figmaLinks}

${storyDetails}
${acDetails}
${bddDetails}
${tasksDetails}

🤖 Generated with [Claude Code](https://claude.com/claude-code)
`;
```

---

## ✅ 적용 체크리스트

### `/figma:analyze`
- [ ] Story 생성 시 피그마 링크 섹션 추가
- [ ] URL에서 node-id 추출하여 매핑
- [ ] 화면별 프레임 링크 기록

### ZenHub Issue
- [ ] Details 태그 템플릿 작성
- [ ] Story 전체 내용 포함
- [ ] Acceptance Criteria 전체 내용 포함
- [ ] BDD 시나리오 전체 내용 포함
- [ ] 구현 태스크 체크리스트 포함

### `/feature:create`
- [ ] 기존 feature 감지 로직
- [ ] Phase 3.5: 피그마 스타일 적용
- [ ] Phase 4.5: 실제 동작 구현
- [ ] Phase 5: 완전한 검증 (BDD 포함)

---

## 🔧 다음 세션 작업

1. **에이전트 파일 위치 확인**:
   ```bash
   # 전역 설정
   ls ~/.claude/commands/

   # 프로젝트 설정
   ls .claude/commands/
   ```

2. **/figma:analyze 업데이트**:
   - 피그마 링크 기록 로직 추가
   - Story 템플릿 업데이트

3. **ZenHub Issue 템플릿 생성**:
   - Details 태그 활용
   - 전체 내용 포함

4. **/feature:create 강화**:
   - 기존 feature 처리
   - UI 완전 구현
   - 검증 강화

5. **Community UI 실제 구현**:
   - 개선된 에이전트로 재실행
   - 동작하는 목록 화면 완성

---

## 📚 참고 문서

- **Dart Convention**: 디렉토리명 단수 사용 (CLAUDE.md:508-513)
- **BDD 규칙**: 영어 Step + 한글 주석 (.claude/commands/bdd/generate.md)
- **Community 요구사항**: claudedocs/community/requirements.md
- **피그마 분석**: claudedocs/community/figma_analysis.md

---

**문서 버전**: 1.0
**최종 수정일**: 2025-12-17

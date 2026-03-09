# BMAD 튜토리얼

실제 예제를 통해 BMAD 워크플로우를 단계별로 학습합니다.

---

## 튜토리얼 1: 첫 번째 BMAD 워크플로우

### 시나리오

"콘솔 앱에 저자 목록 화면을 추가"하는 작업을 BMAD로 진행합니다.

### Step 1: BMAD 워크플로우 시작

```bash
/bmad "콘솔 저자 목록 화면 추가"
```

### Step 2: Analysis 페이즈 (자동)

**Analyst**가 요구사항을 분석하고 AC를 작성합니다:

```
╔════════════════════════════════════════════════════════════════╗
║  🔍 Analyst Review: APPROVED                                   ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ 요구사항 명확성: PASS                                       ║
║     - 콘솔 앱, 저자 목록 화면                                   ║
║     - 스코프: feature/console 모듈                              ║
║                                                                ║
║  ✅ AC BDD Gherkin 형식: PASS                                   ║
║     - @happy-path: 2개                                         ║
║     - @error-handling: 1개                                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

📋 Acceptance Criteria:

Feature: 콘솔 저자 목록 화면
  As a 출판사 관리자
  I want to 저자 목록을 확인할 수 있다
  So that 저자 정보를 관리할 수 있다

  @happy-path
  Scenario: 저자 목록 조회
    Given 출판사 관리자로 로그인되어 있다
    When 저자 관리 메뉴를 클릭한다
    Then 저자 목록 화면이 표시된다
    And 등록된 저자 목록이 테이블에 표시된다

  @happy-path
  Scenario: 저자 검색
    Given 저자 목록 화면에 있다
    And "홍길동" 저자가 등록되어 있다
    When 검색창에 "홍길동"을 입력한다
    Then 검색 결과에 "홍길동"이 포함된다

  @error-handling
  Scenario: 목록 로딩 실패
    Given 서버 연결이 불안정하다
    When 저자 목록 화면으로 이동한다
    Then "데이터를 불러올 수 없습니다" 메시지가 표시된다
    And 재시도 버튼이 표시된다
```

### Step 3: Planning 페이즈 (자동)

**Product Manager**가 이슈를 생성합니다:

```
╔════════════════════════════════════════════════════════════════╗
║  📝 PM Review: APPROVED                                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 이슈 생성: #1810                                            ║
║     제목: [feat] 콘솔 저자 목록 화면 추가                        ║
║     라벨: feature, console, author                             ║
║     Story Point: 5                                             ║
║                                                                ║
║  📊 복잡도 분석:                                                ║
║     - 화면 타입: List (페이지네이션, 검색)                      ║
║     - 레이어: Presentation + Domain + Data                     ║
║     - 예상 파일: 15-20개                                       ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### Step 4: Solutioning 페이즈 (병렬)

**Architect**와 **UX Designer**가 동시에 검토합니다:

```
╔════════════════════════════════════════════════════════════════╗
║  Phase 3: SOLUTIONING (병렬 실행)                              ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🏗️ Architect 검토: ✅ APPROVED                                ║
║  ├── ✅ Clean Architecture                                     ║
║  │   └── AuthorListBloC → GetAuthorsUseCase → IAuthorRepo     ║
║  ├── ✅ DI 구조                                                ║
║  │   └── Injectable 등록, barrel export 확인                   ║
║  └── ✅ API 설계                                               ║
║      └── 기존 AuthorEndpoint 사용                              ║
║                                                                ║
║  🎨 UX Designer 검토: ✅ APPROVED                              ║
║  ├── ✅ CoUI 준수                                              ║
║  │   └── DataTable, TextField, Button 사용                    ║
║  ├── ✅ 레이아웃                                               ║
║  │   └── 표준 콘솔 레이아웃 (Scaffold + headers)               ║
║  └── ✅ 접근성                                                 ║
║      └── 키보드 네비게이션 지원                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### Step 5: Implementation 페이즈

**Flutter Developer**가 구현을 시작합니다:

```
╔════════════════════════════════════════════════════════════════╗
║  Phase 4: IMPLEMENTATION                                       ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🌿 브랜치 생성: feature/1810-author-list                      ║
║                                                                ║
║  📁 생성된 파일:                                                ║
║  feature/console/console_author/                               ║
║  ├── lib/src/                                                  ║
║  │   ├── data/                                                 ║
║  │   │   └── repository/author_repository_impl.dart            ║
║  │   ├── domain/                                               ║
║  │   │   ├── entity/author.dart                                ║
║  │   │   ├── repository/i_author_repository.dart               ║
║  │   │   └── usecase/get_authors_usecase.dart                  ║
║  │   ├── presentation/                                         ║
║  │   │   ├── bloc/author_list_bloc.dart                        ║
║  │   │   ├── page/author_list_page.dart                        ║
║  │   │   └── widget/author_table.dart                          ║
║  │   ├── di/injector.dart                                      ║
║  │   └── route/route.dart                                      ║
║  └── test/                                                     ║
║      ├── bloc/author_list_bloc_test.dart                       ║
║      └── bdd/author_list_test.dart                             ║
║                                                                ║
║  ✅ melos run analyze: PASS                                    ║
║  ✅ 테스트: 12/12 통과                                         ║
║  ✅ PR #1815 생성                                              ║
║  ✅ 코드 리뷰: APPROVED                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### Step 6: 완료

```
╔════════════════════════════════════════════════════════════════╗
║  🎉 BMAD Workflow Complete                                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Phase 1: ANALYSIS - 승인 (AC 3개 확정)                      ║
║  ✅ Phase 2: PLANNING - Issue #1810 생성                       ║
║  ✅ Phase 3: SOLUTIONING - 설계 승인                           ║
║  ✅ Phase 4: IMPLEMENTATION - PR #1815 머지됨                  ║
║                                                                ║
║  📊 Summary:                                                   ║
║     - 검토 통과: 7/7 페르소나                                  ║
║     - 게이트 통과: 4/4 페이즈                                  ║
║     - 재시도: 0회                                              ║
║     - 총 파일: 18개                                            ║
║                                                                ║
║  🧹 정리 완료:                                                  ║
║     - 브랜치 삭제: feature/1810-author-list                    ║
║     - 이슈 종료: #1810                                         ║
║     - 파이프라인: Done                                         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 튜토리얼 2: 게이트 실패 및 재검토

### 시나리오

Solutioning 페이즈에서 Architect 검토가 실패한 경우를 다룹니다.

### Step 1: 게이트 실패 발생

```
╔════════════════════════════════════════════════════════════════╗
║  Phase 3: SOLUTIONING Gate ❌ FAILED                           ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🏗️ Architect 검토: ❌ REJECTED                                ║
║  ├── ✅ Clean Architecture: PASS                               ║
║  ├── ❌ DI 구조: FAIL                                          ║
║  │   └── injector.module.dart가 barrel에 export되지 않음       ║
║  └── ✅ API 설계: PASS                                         ║
║                                                                ║
║  🎨 UX Designer 검토: ✅ APPROVED                              ║
║                                                                ║
║  ────────────────────────────────────────────────────────────  ║
║  필요한 조치:                                                  ║
║  ────────────────────────────────────────────────────────────  ║
║  1. lib/console_author.dart에 추가:                            ║
║     export 'src/di/injector.module.dart';                     ║
║                                                                ║
║  ⚠️ 조치 완료 후 재검토 필요:                                  ║
║     /bmad:review --persona architect --retry                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### Step 2: 피드백 확인

```bash
# 현재 상태 확인
/bmad:status --phase solutioning
```

출력:
```
Phase: Solutioning
Status: ❌ BLOCKED (Architect 검토 실패)

Architect 피드백:
  - injector.module.dart export 누락
  - 파일: lib/console_author.dart
  - 필요한 줄: export 'src/di/injector.module.dart';

UX Designer: ✅ APPROVED

다음 조치: 피드백 반영 후 /bmad:review --persona architect --retry
```

### Step 3: 코드 수정

```dart
// lib/console_author.dart (수정 전)
library;

export 'src/data/data.dart';
export 'src/di/injector.dart';
// injector.module.dart 누락!
export 'src/domain/domain.dart';
export 'src/presentation/presentation.dart';
export 'src/route/route.dart';
```

```dart
// lib/console_author.dart (수정 후)
library;

export 'src/data/data.dart';
export 'src/di/injector.dart';
export 'src/di/injector.module.dart';  // ✅ 추가
export 'src/domain/domain.dart';
export 'src/presentation/presentation.dart';
export 'src/route/route.dart';
```

### Step 4: 재검토 요청

```bash
/bmad:review --persona architect --retry
```

출력:
```
╔════════════════════════════════════════════════════════════════╗
║  🏗️ Architect Review (재검토): ✅ APPROVED                     ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Clean Architecture: PASS                                    ║
║  ✅ DI 구조: PASS                                               ║
║     └── injector.module.dart export 확인됨 ✓                   ║
║  ✅ API 설계: N/A                                               ║
║                                                                ║
║  Phase 3 Gate: ✅ PASSED                                        ║
║  → Phase 4 (Implementation) 진행                               ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 튜토리얼 3: 긴급 모드 사용

### 시나리오

프로덕션에서 결제 버그가 발생하여 긴급 수정이 필요한 상황입니다.

### Step 1: 긴급 모드 시작

```bash
/bmad --emergency "결제 금액 계산 오류 긴급 수정"
```

### Step 2: 승인 요청

```
╔════════════════════════════════════════════════════════════════╗
║  ⚠️ 긴급 모드 승인 요청                                        ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  긴급 모드는 다음 게이트를 간소화합니다:                        ║
║  - Analysis: 스킵                                              ║
║  - Planning: 스킵                                              ║
║  - Solutioning: 간소화 (핵심 검토만)                           ║
║                                                                ║
║  ⚠️ Implementation 게이트는 여전히 필수입니다:                  ║
║  - melos run analyze 통과                                      ║
║  - 기본 테스트 통과                                            ║
║                                                                ║
║  ⚠️ 완료 후 48시간 내 사후 리뷰가 필요합니다.                   ║
║                                                                ║
║  [예, 승인합니다] [아니오, 일반 모드로 진행]                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

사용자가 "예, 승인합니다" 선택.

### Step 3: 간소화된 워크플로우

```
╔════════════════════════════════════════════════════════════════╗
║  🚨 Emergency Mode: 결제 금액 계산 오류 긴급 수정              ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ⏭️ Phase 1: ANALYSIS - 스킵됨 (긴급 모드)                     ║
║  ⏭️ Phase 2: PLANNING - 스킵됨 (긴급 모드)                     ║
║  🔄 Phase 3: SOLUTIONING - 간소화 검토 중                      ║
║  ⏳ Phase 4: IMPLEMENTATION - 대기                              ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### Step 4: 완료 및 사후 리뷰 알림

```
╔════════════════════════════════════════════════════════════════╗
║  🚨 Emergency Workflow Complete                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ 긴급 수정 완료: PR #1820 머지됨                             ║
║                                                                ║
║  ⚠️ 사후 리뷰 필수:                                            ║
║  - 기한: 48시간 내 (2025-01-26 15:30까지)                      ║
║  - 리뷰어: Architect, Product Manager                          ║
║  - 이슈: #1821 (자동 생성됨)                                   ║
║                                                                ║
║  사후 리뷰 항목:                                                ║
║  - [ ] 수정 사항이 아키텍처에 미치는 영향 검토                  ║
║  - [ ] 추가 테스트 필요 여부 확인                               ║
║  - [ ] 문서화 필요 여부 확인                                    ║
║  - [ ] 재발 방지 조치 계획                                      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 튜토리얼 4: 특정 페르소나 스킵

### 시나리오

백엔드 전용 작업으로 UX Designer 검토가 필요 없는 경우.

### Step 1: 페르소나 스킵 옵션 사용

```bash
/bmad --skip-persona ux-designer "Serverpod 마이그레이션 엔드포인트 추가"
```

### Step 2: Solutioning 페이즈

```
╔════════════════════════════════════════════════════════════════╗
║  Phase 3: SOLUTIONING                                          ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🏗️ Architect 검토: ✅ APPROVED                                ║
║  ├── ✅ Clean Architecture                                     ║
║  ├── ✅ API 설계                                               ║
║  └── ✅ DB 마이그레이션 검토                                   ║
║                                                                ║
║  🎨 UX Designer 검토: ⏭️ 스킵됨 (--skip-persona)               ║
║                                                                ║
║  Phase 3 Gate: ✅ PASSED                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 튜토리얼 5: AC(Acceptance Criteria) 작성 가이드

### BDD Gherkin 형식 필수

Analysis 페이즈에서 Analyst는 모든 AC를 **BDD Gherkin 형식**으로 작성해야 합니다.

### 기본 구조

```gherkin
Feature: {기능명}
  As a {사용자 역할}
  I want to {원하는 기능}
  So that {기대 효과}

  Background:
    Given {공통 전제 조건}

  @happy-path
  Scenario: {정상 케이스}
    Given {전제 조건}
    When {행동}
    Then {검증 가능한 결과}

  @error-handling
  Scenario: {에러 케이스}
    Given {전제 조건}
    When {에러 유발 행동}
    Then {에러 처리 결과}

  @edge-case
  Scenario: {경계값 케이스}
    Given {특수 상황}
    When {행동}
    Then {결과}
```

### 필수 태그

| 태그 | 필수 | 최소 개수 |
|------|------|----------|
| `@happy-path` | ✅ | 1개 이상 |
| `@error-handling` | ✅ | 1개 이상 |
| `@edge-case` | 권장 | - |

### 예시: 폼 화면

```gherkin
Feature: 저자 등록 폼
  As a 출판사 관리자
  I want to 새 저자를 등록할 수 있다
  So that 저자 정보를 관리할 수 있다

  Background:
    Given 출판사 관리자로 로그인되어 있다
    And 저자 등록 화면에 있다

  @happy-path
  Scenario: 유효한 정보로 저자 등록
    Given 모든 필수 필드가 비어있다
    When 이름에 "홍길동"을 입력한다
    And 이메일에 "hong@example.com"을 입력한다
    And 저장 버튼을 클릭한다
    Then 저자가 성공적으로 등록된다
    And 저자 목록 화면으로 이동한다
    And 성공 토스트가 표시된다

  @error-handling
  Scenario: 필수 필드 누락
    Given 이름 필드가 비어있다
    When 저장 버튼을 클릭한다
    Then "이름은 필수입니다" 에러가 표시된다
    And 폼이 제출되지 않는다

  @error-handling
  Scenario: 이메일 형식 오류
    Given 이메일에 "invalid-email"을 입력한다
    When 저장 버튼을 클릭한다
    Then "유효한 이메일을 입력하세요" 에러가 표시된다

  @edge-case
  Scenario: 중복 이메일
    Given 이메일 "hong@example.com"이 이미 등록되어 있다
    When 이메일에 "hong@example.com"을 입력한다
    And 저장 버튼을 클릭한다
    Then "이미 등록된 이메일입니다" 에러가 표시된다
```

### AC 검증 실패 예시

```
╔════════════════════════════════════════════════════════════════╗
║  🔍 Analyst Review: ❌ REJECTED                                 ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ❌ AC BDD Gherkin 형식: FAIL                                   ║
║     - @error-handling 시나리오가 없습니다                       ║
║                                                                ║
║  필요한 조치:                                                   ║
║  1. 에러 처리 시나리오 최소 1개 추가                            ║
║                                                                ║
║  예시:                                                          ║
║  @error-handling                                               ║
║  Scenario: 서버 오류 시 에러 표시                               ║
║    Given 서버 연결이 불안정하다                                 ║
║    When 저장 버튼을 클릭한다                                    ║
║    Then "저장에 실패했습니다" 에러가 표시된다                   ║
║    And 재시도 버튼이 표시된다                                   ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 다음 단계

- [BMAD_GUIDE.md](./BMAD_GUIDE.md) - 전체 가이드
- [BMAD_QUICKREF.md](./BMAD_QUICKREF.md) - 빠른 참조
- [PERSONA_MATRIX.md](../.claude/references/PERSONA_MATRIX.md) - 페르소나 매트릭스

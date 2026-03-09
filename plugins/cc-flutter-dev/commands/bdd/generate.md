---
name: bdd:generate
description: "BDD Feature 파일 및 Step Definition 생성"
invoke: /bdd:generate
aliases: ["/bdd", "/test:bdd:generate"]
category: petmedi-workflow
complexity: moderate
mcp-servers: [sequential, context7, serena]
---

# /bdd:generate

> **Context Framework Note**: 이 명령어는 BDD Feature 파일과 Step Definition을 생성합니다.

## 한글 프로젝트 규칙 요약

| 구분 | 언어 | 비고 |
|-----|-----|------|
| Feature 제목/설명 | 한글 | 자유롭게 작성 |
| Scenario 제목/설명 | 한글 | 자유롭게 작성 |
| Step 패턴 | **영어** | 상단 한글 Usage 주석 필수 |
| Step 파라미터 (UI 텍스트) | `{'한글값'}` | Dart 문자열로 전달 |
| 커스텀 Step 함수 | **영어 camelCase** | Usage 주석에 영문/한글 병기 |

---

## Triggers

- Feature의 BDD 테스트를 생성할 때
- `/figma:analyze` Phase 6에서 호출될 때
- 기존 Feature에 BDD 테스트를 추가할 때

## Context Trigger Pattern

```bash
/bdd:generate {feature_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature명 (snake_case) | `community` |
| `--entity-name` | ❌ | Entity명 (자동 추론) | `Post` |
| `--location` | ❌ | Feature 위치 | `application` |
| `--screens` | ❌ | 화면 타입 | `"list,detail,form"` |
| `--from-claudedocs` | ❌ | claudedocs에서 복사 | `true` |
| `--only-steps` | ❌ | Step 정의만 생성 | `true` |
| `--run-build` | ❌ | 빌드 자동 실행 | `true` |

---

## 프로젝트 구조

```
feature/{location}/{feature_name}/
├── lib/
│   ├── ...
│   └── test_steps/                    # 도메인 특화 스텝 라이브러리
│       ├── common_steps.dart          # Feature 공용 스텝
│       └── {feature}_steps.dart       # Feature 전용 스텝
├── test/
│   ├── features/                      # .feature 파일
│   │   ├── {feature}_list.feature
│   │   ├── {feature}_detail.feature
│   │   └── {feature}_form.feature
│   └── steps/                         # 자동 생성 스텝 (build_runner)
│       └── ...
├── build.yaml
└── pubspec.yaml
```

---

## build.yaml 설정

**권장 구조**: `package/core`에 공통 스텝, 각 feature에서 `externalSteps`로 import

```yaml
targets:
  $default:
    sources:
      include:
        - "pubspec.yaml"
        - $package$
        - lib/$lib$
        - lib/**.dart
        - test/**
    builders:
      # BDD Widget Test - Feature 파일 기반 테스트 생성
      bdd_widget_test|featureBuilder:
        enabled: true
        options:
          # 자동 생성되는 스텝 저장 위치
          stepFolderName: test/steps

          # 외부 공용 스텝 라이브러리
          externalSteps:
            # Core 공통 스텝 (앱 전체 공용)
            - package:core/src/test/bdd/common_steps.dart
            - package:core/src/test/bdd/navigation_steps.dart
            - package:core/src/test/bdd/widget_steps.dart

            # Feature 전용 스텝 (선택사항)
            # - package:{feature}/test_steps/{feature}_steps.dart
```

---

## Step Definition 작성 규칙

### 핵심 규칙

1. **함수명**: 영어 camelCase (예: `iSeeClassListScreen`)
2. **Usage 주석**: 영문 Step 패턴 + 한글 용도 설명
3. **파라미터**: 한글 UI 텍스트는 `{'한글값'}` 형식으로 전달

### Step 정의 템플릿

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// =============================================================================
// Given Steps
// =============================================================================

/// Usage: Given the app is running
/// 용도: 앱을 실행함
Future<void> theAppIsRunning(WidgetTester tester) async {
  await tester.pumpWidget(const MyApp());
  await tester.pumpAndSettle();
}

/// Usage: And user is logged in as {email}
/// 용도: {email} 계정으로 로그인된 상태를 설정
Future<void> userIsLoggedInAs(WidgetTester tester, String email) async {
  // 테스트용 로그인 상태 주입
}

// =============================================================================
// When Steps
// =============================================================================

/// Usage: When I tap {text} text
/// 용도: {text} 텍스트를 탭함
Future<void> iTapText(WidgetTester tester, String text) async {
  await tester.tap(find.text(text));
  await tester.pumpAndSettle();
}

/// Usage: And I tap enroll button
/// 용도: 등록 버튼을 탭함
Future<void> iTapEnrollButton(WidgetTester tester) async {
  await tester.tap(find.widgetWithText(ElevatedButton, '등록'));
  await tester.pumpAndSettle();
}

// =============================================================================
// Then Steps
// =============================================================================

/// Usage: Then I see {text} text
/// 용도: {text} 텍스트가 표시되는지 확인
Future<void> iSeeText(WidgetTester tester, String text) async {
  expect(find.text(text), findsOneWidget);
}

/// Usage: And I see class list screen
/// 용도: 수업 목록 화면이 표시되는지 확인
Future<void> iSeeClassListScreen(WidgetTester tester) async {
  expect(find.byType(ClassListView), findsOneWidget);
}

/// Usage: And I see at least {count} class items
/// 용도: 최소 {count}개의 수업 항목이 표시되는지 확인
Future<void> iSeeAtLeastClassItems(WidgetTester tester, int count) async {
  final items = find.byType(ClassListTile);
  expect(items, findsAtLeast(count));
}
```

---

## Feature 파일 작성법

### 핵심 규칙

1. **Feature/Scenario 제목**: 한글
2. **Step 패턴**: 영어 (패키지가 매칭하는 패턴)으로 작성하고, 반드시 한글 주석을 붙인다.
3. **파라미터**: `{'한글값'}` 형식

### 예시: 목록 화면

```gherkin
Feature: 수업 등록
  학생이 원하는 수업을 검색하고 등록할 수 있는 기능을 테스트한다.
  등록 완료 후 마이페이지에서 등록된 수업을 확인할 수 있어야 한다.

  Background:
    # 앱 실행 및 로그인 상태 설정
    Given the app is running # 앱이 실행됨
    And user is logged in as {'student@school.com'} # 주어진 이메일로 로그인 상태임

  @smoke
  Scenario: 수업 목록 조회
    사용자가 수업 탭을 선택하면 현재 등록 가능한 수업 목록이 표시된다.

    # 수업 탭으로 이동
    When I tap {'수업'} text # '수업' 텍스트를 탭함
    # 수업 목록 화면 확인
    Then I see class list screen # 수업 목록 화면이 표시되는지 확인
    And I see at least {3} class items # 최소 3개의 수업 항목이 표시되는지 확인

  @enrollment @payment
  Scenario: 유료 수업 등록
    사용자가 유료 수업을 선택하고 결제를 완료하면 등록이 완료된다.

    # 수업 선택
    Given I am on class list screen # 수업 목록 화면에 있음
    When I tap {'고급 수학'} text # '고급 수학' 텍스트를 탭함
    # 등록 버튼 클릭
    And I tap enroll button # 등록 버튼을 탭함
    # 결제 진행
    And I complete payment with {'카드'} # '카드' 결제 진행
    # 등록 완료 확인
    Then I see {'등록이 완료되었습니다'} text # '등록이 완료되었습니다' 텍스트가 표시됨
    And class {'고급 수학'} appears in my enrolled list # 내 등록 내역에서 '고급 수학'이 나타남
```

### 예시: 폼 화면

```gherkin
Feature: 숙제 제출
  학생이 숙제를 확인하고 제출할 수 있는 기능을 테스트한다.

  Background:
    Given the app is running # 앱이 실행됨
    And user is logged in as {'student@school.com'} # 주어진 이메일로 로그인 상태임

  @homework @submit
  Scenario: 숙제 파일 제출
    학생이 숙제에 파일을 첨부하고 제출하면 제출 완료 상태가 된다.

    Given I am on class list screen # 수업 목록 화면에 있음
    When I tap {'숙제'} text # '숙제' 텍스트를 탭함
    And I tap first homework item # 첫 번째 숙제 항목을 탭함
    And I attach file {'answer.pdf'} # 'answer.pdf' 파일을 첨부함
    And I tap submit button # 제출 버튼을 탭함
    Then I see {'제출 완료'} text # '제출 완료' 텍스트가 표시됨
    And homework status is {'제출됨'} # 숙제 상태가 '제출됨'임
```

---

## Predefined Steps 활용

bdd_widget_test 패키지 기본 제공 스텝:

```gherkin
# 이미 구현되어 있음 - 커스텀 스텝 불필요
Then I see {'환영합니다'} text # '환영합니다' 텍스트가 표시되는지 확인
And I tap {'확인'} text # '확인' 텍스트를 탭함
And I don't see {'로딩중'} text # '로딩중' 텍스트가 표시되지 않는지 확인
And I see {Icons.check} icon # 체크 아이콘이 표시되는지 확인
And I enter {'test@email.com'} into {'이메일'} input field # '이메일' 입력 칸에 'test@email.com'을 입력함
```

---

## 멀티 패키지 환경 설정

여러 패키지에서 스텝을 공유하려면 `bdd_options.yaml` 사용:

**`bdd_options.yaml`** (프로젝트 루트)

```yaml
include: package:core/bdd_options.yaml
externalSteps:
  - package:core/src/test/bdd/bdd.dart
  - package:{feature}/test_steps/common_steps.dart
```

---

## hooks.dart 설정

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:mocktail/mocktail.dart';

// Mock imports
import '../../mocks/mocks.dart';

/// BDD 테스트 Setup Hook
Future<void> setUp(WidgetTester tester) async {
  // GetIt 초기화
  final getIt = GetIt.instance;
  await getIt.reset();

  // Fallback values 등록
  registerFallbackValues();

  // Mock 객체 등록
  registerMocks(getIt);
}

/// BDD 테스트 TearDown Hook
Future<void> tearDown(WidgetTester tester) async {
  await GetIt.instance.reset();
}

/// Fallback values 등록
void registerFallbackValues() {
  // 필요한 fallback values 등록
  // registerFallbackValue(Fake{Entity}());
}

/// Mock 객체 등록
void registerMocks(GetIt getIt) {
  // Repository mocks
  // getIt.registerLazySingleton<I{Feature}Repository>(
  //   () => Mock{Feature}Repository(),
  // );
}
```

---

## 도메인 스텝 라이브러리 장점

| 장점 | 설명 |
|-----|------|
| 재사용성 | 여러 feature 파일에서 동일한 스텝 공유 |
| 유지보수 | 한 곳에서 스텝 로직 수정 시 전체 반영 |
| 일관성 | 도메인 용어와 테스트 패턴 통일 |
| 멀티 패키지 | `externalSteps`로 패키지 간 공유 가능 |
| 자동 완성 | IDE에서 Usage 주석 기반 힌트 제공 |

---

## MCP Integration

| 작업 | MCP 서버 | 용도 |
|------|----------|------|
| 시나리오 구조화 | **Sequential** | 체계적 시나리오 설계 |
| 패턴 참조 | **Context7** | bdd_widget_test 문서 |
| 코드 생성 | **Serena** | Step 정의 생성 |

---

## Examples

### 기본 사용

```bash
/bdd:generate community
```

### claudedocs에서 복사 + 빌드

```bash
/bdd:generate community \
  --from-claudedocs true \
  --run-build true
```

### Step 정의만 생성

```bash
/bdd:generate community \
  --only-steps true
```

### 특정 화면만 생성

```bash
/bdd:generate community \
  --screens "list,detail"
```

---

## 테스트 실행

```bash
# 코드 생성
dart run build_runner build --delete-conflicting-outputs

# watch 모드 (개발 중 권장)
dart run build_runner watch --delete-conflicting-outputs

# 테스트 실행
flutter test

# 태그 필터링
flutter test --tags enrollment
flutter test --exclude-tags payment

# 특정 feature 파일만 실행
flutter test test/features/class/
```

### melos 명령

```bash
# BDD 테스트 코드 생성
melos run test:bdd:generate --scope={feature_name}

# BDD 테스트 실행
melos run test:bdd --scope={feature_name}

# 전체 실행 (생성 + 테스트)
melos run test:bdd:full --scope={feature_name}
```

---

## 핵심 규칙 요약

1. **Step 패턴은 영어**: `.feature` 파일의 Given/When/Then 뒤는 영어
2. **함수명은 camelCase 영어**: `iSeeClassListScreen`, `iTapEnrollButton`
3. **Usage 주석 필수**: `/// Usage: And I tap enroll button` + `/// 용도: 등록 버튼을 탭함`
4. **한글 파라미터**: `{'한글값'}` 형식으로 전달
5. **공용 스텝 재사용**: `package:core/src/test/bdd/bdd.dart` 활용
6. **externalSteps 활용**: build.yaml에서 외부 스텝 라이브러리 지정
7. **태그 사용**: `@smoke`, `@navigation` 등 분류 태그

---

## 참조 에이전트

상세 구현 규칙: `~/.claude/commands/agents/bdd-scenario-agent.md`

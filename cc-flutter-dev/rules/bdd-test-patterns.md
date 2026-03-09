# BDD 테스트 패턴

이 프로젝트는 BDD(Behavior-Driven Development) 스타일의 테스트를 사용합니다.

## 디렉토리 구조

```
feature/{module}/test/src/bdd/
├── {feature}_test.dart       # 메인 테스트 파일
├── hooks/
│   └── hooks.dart            # 테스트 설정/정리 훅
└── step/
    ├── i_am_on_the_{page}.dart
    ├── i_tap_the_{button}.dart
    ├── the_{element}_should_be_displayed.dart
    └── ...
```

---

## Step 파일 네이밍 규칙

### Given (전제 조건)
- `i_am_on_the_{page}.dart` - 특정 페이지에 있음
- `the_dashboard_has_loaded.dart` - 대시보드가 로드됨
- `the_filter_data_is_available.dart` - 필터 데이터가 사용 가능

### When (행동)
- `i_tap_the_{button}.dart` - 버튼 탭
- `i_select_{option}.dart` - 옵션 선택
- `i_enter_{input}.dart` - 입력값 입력

### Then (결과 검증)
- `the_{element}_should_be_displayed.dart` - 요소가 표시됨
- `the_{value}_should_be_{expected}.dart` - 값이 예상과 일치
- `the_{error}_should_be_displayed.dart` - 에러가 표시됨

---

## Step 함수 패턴

### 동기 함수 (권장)

```dart
import 'package:flutter_test/flutter_test.dart';

/// KPI 카드 섹션이 표시되어야 함
void theKpiCardSectionShouldBeDisplayed(WidgetTester tester) {
  expect(find.byType(SalesKpiSection), findsOneWidget);
}
```

### 비동기 함수 (필요 시)

```dart
import 'package:flutter_test/flutter_test.dart';

/// 버튼을 탭함
Future<void> iTapTheSubmitButton(WidgetTester tester) async {
  await tester.tap(find.text('제출'));
  await tester.pumpAndSettle();
}
```

### 파라미터 미사용 시

```dart
/// 대시보드가 로드됨 (tester 미사용)
void theDashboardHasLoaded(WidgetTester _) {
  // 상태 설정만 수행
}
```

---

## 테스트 파일 구조

```dart
@Tags(['smoke', 'sales_analysis'])
import 'package:flutter_test/flutter_test.dart';

import './step/i_am_on_the_sales_analysis_page.dart';
import './step/the_dashboard_has_loaded.dart';
import './step/i_select_7_days_period.dart';
import './step/the_7_days_period_should_be_selected.dart';

void main() {
  group('''Sales Analysis''', () {
    Future<void> bddSetUp(WidgetTester tester) async {
      await iAmOnTheSalesAnalysisPage(tester);
    }

    testWidgets('''Select 7 days period''', (tester) async {
      await bddSetUp(tester);
      theDashboardHasLoaded(tester);
      await iSelect7DaysPeriod(tester);
      the7DaysPeriodShouldBeSelected(tester);
    }, tags: ['period_selection']);
  });
}
```

---

## Step 파일 생성 체크리스트

1. **파일 생성**: `test/src/bdd/step/{step_name}.dart`
2. **import 추가**: 메인 테스트 파일에 import 추가
3. **함수 구현**: 적절한 검증/행동 로직 구현
4. **테스트 실행**: `flutter test` 또는 `melos run test`

---

## 누락된 Step 파일 오류

```
error • Target of URI doesn't exist: './step/the_kpi_card_section_should_be_displayed.dart'
```

**해결 방법**:
1. 누락된 step 파일 생성
2. 표준 패턴에 맞게 함수 구현
3. 분석 재실행하여 확인

---

## 주의사항

1. **파일명 = 함수명**: 파일명과 함수명이 일치해야 함 (snake_case ↔ camelCase 변환)
2. **import 순서**: 메인 테스트 파일에서 모든 step 파일을 import
3. **async/sync**: 필요한 경우에만 async 사용
4. **tester 파라미터**: 사용하지 않으면 `_`로 명명

---

## 관련 문서

- [CLAUDE.md](../../CLAUDE.md) - 프로젝트 전체 가이드
- [Flutter 테스트 문서](https://docs.flutter.dev/testing)

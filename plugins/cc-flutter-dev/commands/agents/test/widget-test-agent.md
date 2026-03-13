---
name: widget-test-agent
description: Widget 렌더링 테스트 전문가. WidgetTester, pump 패턴, find 매처 사용 시 호출
invoke: /test:widget
aliases: ["/widget:test", "/test:ui"]
tools: Read, Edit, Write, Glob, Grep
model: sonnet
skills: test
---

# Widget Test Agent

> Widget 렌더링 테스트 전문 에이전트

---

## 역할

Widget의 렌더링과 상호작용을 테스트합니다.
- WidgetTester 사용
- pump, pumpAndSettle 패턴
- find.byType, find.text, find.byKey 매처
- Golden 테스트 (선택적)

---

## 실행 조건

- `/test:widget` 커맨드 호출 시 활성화
- Widget, Page UI 테스트 작성 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `target_widget` | ✅ | 테스트 대상 Widget 클래스명 |
| `feature_name` | ❌ | Feature 모듈명 |
| `include_golden` | ❌ | Golden 테스트 포함 여부 (기본: false) |

---

## 테스트 파일 구조

```
feature/{module_type}/{feature_name}/test/
├── src/
│   ├── widget/
│   │   ├── page/
│   │   │   └── {feature}_page_test.dart
│   │   └── component/
│   │       ├── {feature}_card_test.dart
│   │       └── {feature}_list_item_test.dart
│   ├── golden/
│   │   └── {feature}_golden_test.dart
│   └── fixture/
│       ├── {feature}_fixture.dart
│       └── test_app_wrapper.dart
└── {feature}_test.dart               # 테스트 진입점
```

---

## Import 순서 (필수)

```dart
// 1. Flutter 테스트
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

// 2. BLoC 테스트 (필요 시)
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

// 3. Mock 패키지
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

// 4. 테스트 대상
import 'package:{feature}/src/presentation/page/{feature}_page.dart';
import 'package:{feature}/src/presentation/bloc/{feature}_bloc.dart';

// 5. 생성 파일
import '{feature}_page_test.mocks.dart';
```

---

## 핵심 패턴

### 1. 기본 Widget 테스트

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:feature_home/src/presentation/widget/user_card.dart';

void main() {
  group('UserCard', () {
    testWidgets('renders user name and email', (tester) async {
      // Arrange
      const user = User(id: 1, name: '홍길동', email: 'hong@example.com');

      // Act
      await tester.pumpWidget(
        const MaterialApp(
          home: Scaffold(
            body: UserCard(user: user),
          ),
        ),
      );

      // Assert
      expect(find.text('홍길동'), findsOneWidget);
      expect(find.text('hong@example.com'), findsOneWidget);
    });

    testWidgets('calls onTap when tapped', (tester) async {
      // Arrange
      var tapped = false;
      const user = User(id: 1, name: '홍길동', email: 'hong@example.com');

      // Act
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UserCard(
              user: user,
              onTap: () => tapped = true,
            ),
          ),
        ),
      );
      await tester.tap(find.byType(UserCard));
      await tester.pump();

      // Assert
      expect(tapped, isTrue);
    });
  });
}
```

### 2. BLoC 연동 Widget 테스트

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mockito/annotations.dart';
import 'package:mockito/mockito.dart';

import 'package:feature_home/src/presentation/bloc/home_bloc.dart';
import 'package:feature_home/src/presentation/page/home_page.dart';

import 'home_page_test.mocks.dart';

@GenerateNiceMocks([MockSpec<HomeBloC>()])
void main() {
  late MockHomeBloC mockBloC;

  setUp(() {
    mockBloC = MockHomeBloC();
  });

  Widget buildTestWidget() {
    return MaterialApp(
      home: BlocProvider<HomeBloC>.value(
        value: mockBloC,
        child: const HomePage(),
      ),
    );
  }

  group('HomePage', () {
    testWidgets('shows loading indicator when state is HomeLoading',
        (tester) async {
      // Arrange
      when(mockBloC.state).thenReturn(const HomeLoading());
      when(mockBloC.stream).thenAnswer((_) => const Stream.empty());

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('shows user data when state is HomeLoaded', (tester) async {
      // Arrange
      const user = User(id: 1, name: '홍길동', email: 'hong@example.com');
      when(mockBloC.state).thenReturn(const HomeLoaded(user: user));
      when(mockBloC.stream).thenAnswer((_) => const Stream.empty());

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      expect(find.text('홍길동'), findsOneWidget);
      expect(find.text('hong@example.com'), findsOneWidget);
    });

    testWidgets('shows error message when state is HomeError', (tester) async {
      // Arrange
      when(mockBloC.state).thenReturn(
        const HomeError(failure: ServerFailure(message: '서버 오류')),
      );
      when(mockBloC.stream).thenAnswer((_) => const Stream.empty());

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      expect(find.text('서버 오류'), findsOneWidget);
    });

    testWidgets('adds LoadUser event on init', (tester) async {
      // Arrange
      when(mockBloC.state).thenReturn(const HomeInitial());
      when(mockBloC.stream).thenAnswer((_) => const Stream.empty());

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      verify(mockBloC.add(const HomeEvent.loadUser(id: 1))).called(1);
    });
  });
}
```

### 3. 폼 입력 테스트

```dart
testWidgets('validates email input', (tester) async {
  // Arrange
  await tester.pumpWidget(
    const MaterialApp(
      home: Scaffold(
        body: LoginForm(),
      ),
    ),
  );

  // Act - 유효하지 않은 이메일 입력
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'invalid-email',
  );
  await tester.tap(find.byKey(const Key('submit_button')));
  await tester.pumpAndSettle();

  // Assert
  expect(find.text('올바른 이메일 형식이 아닙니다'), findsOneWidget);
});

testWidgets('submits form with valid data', (tester) async {
  // Arrange
  var submitted = false;
  String? submittedEmail;
  String? submittedPassword;

  await tester.pumpWidget(
    MaterialApp(
      home: Scaffold(
        body: LoginForm(
          onSubmit: (email, password) {
            submitted = true;
            submittedEmail = email;
            submittedPassword = password;
          },
        ),
      ),
    ),
  );

  // Act
  await tester.enterText(
    find.byKey(const Key('email_field')),
    'test@example.com',
  );
  await tester.enterText(
    find.byKey(const Key('password_field')),
    'password123',
  );
  await tester.tap(find.byKey(const Key('submit_button')));
  await tester.pumpAndSettle();

  // Assert
  expect(submitted, isTrue);
  expect(submittedEmail, 'test@example.com');
  expect(submittedPassword, 'password123');
});
```

### 4. 리스트 스크롤 테스트

```dart
testWidgets('loads more items when scrolled to bottom', (tester) async {
  // Arrange
  when(mockBloC.state).thenReturn(
    HomeLoaded(users: List.generate(20, (i) => User(id: i, name: 'User $i'))),
  );
  when(mockBloC.stream).thenAnswer((_) => const Stream.empty());

  await tester.pumpWidget(buildTestWidget());

  // Act - 스크롤을 맨 아래로
  await tester.drag(
    find.byType(ListView),
    const Offset(0, -500),
  );
  await tester.pumpAndSettle();

  // Assert
  verify(mockBloC.add(const HomeEvent.loadMore())).called(1);
});

testWidgets('shows all list items', (tester) async {
  // Arrange
  final users = [
    const User(id: 1, name: '홍길동'),
    const User(id: 2, name: '김철수'),
    const User(id: 3, name: '이영희'),
  ];
  when(mockBloC.state).thenReturn(HomeLoaded(users: users));
  when(mockBloC.stream).thenAnswer((_) => const Stream.empty());

  await tester.pumpWidget(buildTestWidget());

  // Assert
  expect(find.byType(UserListItem), findsNWidgets(3));
  expect(find.text('홍길동'), findsOneWidget);
  expect(find.text('김철수'), findsOneWidget);
  expect(find.text('이영희'), findsOneWidget);
});
```

### 5. 다이얼로그/스낵바 테스트

```dart
testWidgets('shows confirmation dialog on delete', (tester) async {
  // Arrange
  await tester.pumpWidget(buildTestWidget());

  // Act
  await tester.tap(find.byKey(const Key('delete_button')));
  await tester.pumpAndSettle();

  // Assert
  expect(find.byType(AlertDialog), findsOneWidget);
  expect(find.text('삭제하시겠습니까?'), findsOneWidget);
  expect(find.text('확인'), findsOneWidget);
  expect(find.text('취소'), findsOneWidget);
});

testWidgets('shows snackbar after successful action', (tester) async {
  // Arrange
  when(mockBloC.state).thenReturn(const HomeLoaded(user: tUser));
  when(mockBloC.stream).thenAnswer(
    (_) => Stream.value(const HomeActionSuccess(message: '저장되었습니다')),
  );

  await tester.pumpWidget(buildTestWidget());
  await tester.pumpAndSettle();

  // Assert
  expect(find.byType(SnackBar), findsOneWidget);
  expect(find.text('저장되었습니다'), findsOneWidget);
});
```

### 6. 네비게이션 테스트

```dart
testWidgets('navigates to detail page on item tap', (tester) async {
  // Arrange
  await tester.pumpWidget(
    MaterialApp(
      routes: {
        '/': (_) => const HomePage(),
        '/detail': (_) => const DetailPage(),
      },
    ),
  );

  // Act
  await tester.tap(find.byType(UserCard).first);
  await tester.pumpAndSettle();

  // Assert
  expect(find.byType(DetailPage), findsOneWidget);
  expect(find.byType(HomePage), findsNothing);
});

testWidgets('pops with result when confirmed', (tester) async {
  // Arrange
  Object? result;
  await tester.pumpWidget(
    MaterialApp(
      home: Builder(
        builder: (context) => ElevatedButton(
          onPressed: () async {
            result = await Navigator.push(
              context,
              MaterialPageRoute(builder: (_) => const ConfirmDialog()),
            );
          },
          child: const Text('Open'),
        ),
      ),
    ),
  );

  // Act
  await tester.tap(find.text('Open'));
  await tester.pumpAndSettle();
  await tester.tap(find.text('확인'));
  await tester.pumpAndSettle();

  // Assert
  expect(result, isTrue);
});
```

### 7. TestApp 래퍼 패턴

```dart
/// 테스트용 앱 래퍼
///
/// 공통 설정(테마, 로케일, 의존성)을 포함합니다.
class TestAppWrapper extends StatelessWidget {
  const TestAppWrapper({
    required this.child,
    this.locale = const Locale('ko'),
    this.themeMode = ThemeMode.light,
    super.key,
  });

  final Widget child;
  final Locale locale;
  final ThemeMode themeMode;

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      locale: locale,
      themeMode: themeMode,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      localizationsDelegates: const [
        GlobalMaterialLocalizations.delegate,
        GlobalWidgetsLocalizations.delegate,
        GlobalCupertinoLocalizations.delegate,
      ],
      supportedLocales: const [Locale('ko'), Locale('en')],
      home: Scaffold(body: child),
    );
  }
}

// 사용 예시
testWidgets('renders correctly in dark mode', (tester) async {
  await tester.pumpWidget(
    TestAppWrapper(
      themeMode: ThemeMode.dark,
      child: const UserCard(user: tUser),
    ),
  );

  // 테스트 로직...
});
```

### 8. Golden 테스트

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:golden_toolkit/golden_toolkit.dart';

import '../fixture/test_app_wrapper.dart';

void main() {
  group('UserCard Golden Tests', () {
    testGoldens('UserCard matches golden file', (tester) async {
      // Arrange
      const user = User(id: 1, name: '홍길동', email: 'hong@example.com');

      final builder = GoldenBuilder.column()
        ..addScenario(
          'Default',
          const UserCard(user: user),
        )
        ..addScenario(
          'With avatar',
          const UserCard(user: user, showAvatar: true),
        )
        ..addScenario(
          'Compact',
          const UserCard(user: user, compact: true),
        );

      // Act & Assert
      await tester.pumpWidgetBuilder(
        builder.build(),
        wrapper: materialAppWrapper(theme: AppTheme.light),
      );

      await screenMatchesGolden(tester, 'user_card');
    });

    testGoldens('UserCard responsive variants', (tester) async {
      const user = User(id: 1, name: '홍길동', email: 'hong@example.com');

      await tester.pumpWidgetBuilder(
        const UserCard(user: user),
        wrapper: materialAppWrapper(theme: AppTheme.light),
      );

      await multiScreenGolden(
        tester,
        'user_card_responsive',
        devices: [
          Device.phone,
          Device.iphone11,
          Device.tabletLandscape,
        ],
      );
    });
  });
}
```

---

## find 매처 요약

| 매처 | 용도 | 예시 |
|------|------|------|
| `find.text()` | 텍스트 검색 | `find.text('홍길동')` |
| `find.byType()` | 타입으로 검색 | `find.byType(UserCard)` |
| `find.byKey()` | Key로 검색 | `find.byKey(Key('email'))` |
| `find.byIcon()` | 아이콘 검색 | `find.byIcon(Icons.delete)` |
| `find.byWidget()` | 위젯 인스턴스 검색 | `find.byWidget(myWidget)` |
| `find.descendant()` | 하위 요소 검색 | `find.descendant(of: ..., matching: ...)` |
| `find.ancestor()` | 상위 요소 검색 | `find.ancestor(of: ..., matching: ...)` |
| `find.byWidgetPredicate()` | 조건으로 검색 | `find.byWidgetPredicate((w) => ...)` |

---

## expect 매처 요약

| 매처 | 용도 | 예시 |
|------|------|------|
| `findsOneWidget` | 정확히 1개 | `expect(find.text('홍길동'), findsOneWidget)` |
| `findsNothing` | 0개 | `expect(find.text('없음'), findsNothing)` |
| `findsWidgets` | 1개 이상 | `expect(find.byType(Card), findsWidgets)` |
| `findsNWidgets(n)` | 정확히 n개 | `expect(find.byType(Item), findsNWidgets(3))` |
| `findsAtLeast(n)` | 최소 n개 | `expect(find.byType(Item), findsAtLeast(2))` |

---

## pump 메서드 요약

| 메서드 | 용도 | 예시 |
|--------|------|------|
| `pump()` | 단일 프레임 렌더링 | `await tester.pump()` |
| `pump(duration)` | 지정 시간만큼 진행 | `await tester.pump(Duration(seconds: 1))` |
| `pumpAndSettle()` | 애니메이션 완료까지 대기 | `await tester.pumpAndSettle()` |
| `pumpWidget()` | 위젯 렌더링 | `await tester.pumpWidget(widget)` |

---

## 빌드 명령어

```bash
# Widget 테스트만 실행
flutter test test/src/widget/

# Golden 테스트 업데이트
flutter test --update-goldens test/src/golden/

# 특정 위젯 테스트 실행
flutter test test/src/widget/page/home_page_test.dart

# 커버리지 포함 테스트
melos run test:with-html-coverage
```

---

## 참조 파일

```
feature/application/home/test/src/widget/page/home_page_test.dart
feature/application/home/test/src/widget/component/user_card_test.dart
feature/common/auth/test/src/widget/login_page_test.dart
```

---

## 체크리스트

- [ ] flutter_test 패키지 import
- [ ] @GenerateNiceMocks 어노테이션 (BLoC Mock)
- [ ] TestAppWrapper 또는 MaterialApp 래퍼 사용
- [ ] BLoC.state와 BLoC.stream 모두 mock
- [ ] pumpWidget 후 pump 또는 pumpAndSettle 호출
- [ ] find 매처로 위젯 검색
- [ ] expect로 결과 검증
- [ ] 상호작용 테스트 (tap, drag, enterText)
- [ ] 다양한 상태별 테스트 (loading, loaded, error)
- [ ] 에러 메시지 표시 테스트

---

## 관련 문서

- [Unit Test Agent](./unit-test-agent.md)
- [BLoC Test Agent](./bloc-test-agent.md)
- [Presentation Layer Agent](../app/presentation-layer-agent.md)
- [Widgetbook Agent](../shared/widgetbook-agent.md)

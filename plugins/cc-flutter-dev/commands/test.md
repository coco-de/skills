---
name: test
description: "단위/위젯/BDD 테스트 작성 가이드"
invoke: /test
aliases: ["/test:unit", "/test:widget", "/test:bloc"]
category: petmedi-development
complexity: moderate
mcp-servers: [serena, context7]
---

# /test

> **Context Framework Note**: 테스트 코드 작성 시 활성화됩니다.

## Triggers

- 새로운 테스트 파일 작성 시
- 테스트 커버리지 개선 시
- TDD/BDD 개발 시

## Context Trigger Pattern

```
/test {type} {target} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `type` | ✅ | 테스트 타입 | `unit`, `widget`, `bloc`, `bdd` |
| `target` | ✅ | 테스트 대상 | `GetUserUseCase`, `HomeBloc`, `LoginPage` |
| `--feature` | ❌ | Feature 모듈 | `auth`, `home` |
| `--coverage` | ❌ | 커버리지 목표 | `80`, `90` (기본: 80) |

## Test Structure

```
feature/{location}/{feature_name}/test/
├── src/
│   ├── domain/
│   │   └── usecase/           # UseCase 단위 테스트
│   ├── data/
│   │   └── repository/        # Repository 테스트 (mocked)
│   └── presentation/
│       ├── bloc/              # BLoC 테스트
│       └── widget/            # Widget 테스트
└── feature/                   # BDD 테스트
    ├── {feature}.feature
    └── step/
```

## UseCase Unit Test

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:dependencies/dependencies.dart';

class MockI{Feature}Repository extends Mock implements I{Feature}Repository {}

void main() {
  late Get{Entity}UseCase useCase;
  late MockI{Feature}Repository mockRepository;

  setUp(() {
    mockRepository = MockI{Feature}Repository();
    useCase = Get{Entity}UseCase(mockRepository);
  });

  group('Get{Entity}UseCase', () {
    final tEntity = {Entity}(id: 1, name: 'Test');
    final tParams = Get{Entity}Params(id: 1);

    test('should return entity when repository succeeds', () async {
      // Arrange
      when(() => mockRepository.get{Entity}(any()))
          .thenAnswer((_) async => Right(tEntity));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, Right(tEntity));
      verify(() => mockRepository.get{Entity}(1)).called(1);
      verifyNoMoreInteractions(mockRepository);
    });

    test('should return failure when repository fails', () async {
      // Arrange
      final tFailure = ServerFailure('Error');
      when(() => mockRepository.get{Entity}(any()))
          .thenAnswer((_) async => Left(tFailure));

      // Act
      final result = await useCase(tParams);

      // Assert
      expect(result, Left(tFailure));
    });
  });
}
```

## BLoC Test

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

class MockGet{Entity}UseCase extends Mock implements Get{Entity}UseCase {}

void main() {
  late {Feature}Bloc bloc;
  late MockGet{Entity}UseCase mockUseCase;

  setUp(() {
    mockUseCase = MockGet{Entity}UseCase();
    bloc = {Feature}Bloc();
  });

  tearDown(() {
    bloc.close();
  });

  group('{Feature}Bloc', () {
    test('initial state is Initial', () {
      expect(bloc.state, const {Feature}State.initial());
    });

    blocTest<{Feature}Bloc, {Feature}State>(
      'emits [Loading, Loaded] when load succeeds',
      build: () => bloc,
      act: (bloc) => bloc.load(),
      expect: () => [
        const {Feature}State.loading(),
        isA<{Feature}State>().having(
          (s) => s.maybeMap(loaded: (l) => l.items, orElse: () => null),
          'items',
          isNotEmpty,
        ),
      ],
    );

    blocTest<{Feature}Bloc, {Feature}State>(
      'emits [Loading, Error] when load fails',
      build: () => bloc,
      act: (bloc) => bloc.load(),
      expect: () => [
        const {Feature}State.loading(),
        isA<{Feature}State>().having(
          (s) => s.maybeMap(error: (e) => e.failure, orElse: () => null),
          'failure',
          isNotNull,
        ),
      ],
    );
  });
}
```

## Widget Test

```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:mocktail/mocktail.dart';

class Mock{Feature}Bloc extends MockBloc<{Feature}Event, {Feature}State>
    implements {Feature}Bloc {}

void main() {
  late Mock{Feature}Bloc mockBloc;

  setUp(() {
    mockBloc = Mock{Feature}Bloc();
  });

  Widget buildTestWidget() {
    return MaterialApp(
      home: BlocProvider<{Feature}Bloc>.value(
        value: mockBloc,
        child: const {Feature}Page(),
      ),
    );
  }

  group('{Feature}Page', () {
    testWidgets('renders loading indicator when loading', (tester) async {
      // Arrange
      when(() => mockBloc.state).thenReturn(const {Feature}State.loading());

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('renders list when loaded', (tester) async {
      // Arrange
      final items = [
        {Entity}(id: 1, name: 'Item 1'),
        {Entity}(id: 2, name: 'Item 2'),
      ];
      when(() => mockBloc.state).thenReturn(
        {Feature}State.loaded(items: items),
      );

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      expect(find.text('Item 1'), findsOneWidget);
      expect(find.text('Item 2'), findsOneWidget);
    });

    testWidgets('shows error message when error', (tester) async {
      // Arrange
      when(() => mockBloc.state).thenReturn(
        {Feature}State.error(ServerFailure('Network error')),
      );

      // Act
      await tester.pumpWidget(buildTestWidget());

      // Assert
      expect(find.text('Network error'), findsOneWidget);
    });
  });
}
```

## BDD Test (.feature)

```gherkin
Feature: {Feature} 목록 조회
  사용자가 {Feature} 목록을 조회할 수 있다.

  Background:
    Given 앱이 실행되어 있다
    And 사용자가 로그인되어 있다

  Scenario: 목록 조회 성공
    Given 서버에 {entity} 데이터가 존재한다
    When 사용자가 {feature} 화면에 진입한다
    Then {entity} 목록이 표시된다

  Scenario: 빈 목록
    Given 서버에 {entity} 데이터가 없다
    When 사용자가 {feature} 화면에 진입한다
    Then 빈 목록 메시지가 표시된다

  Scenario: 네트워크 오류
    Given 네트워크 연결이 끊어져 있다
    When 사용자가 {feature} 화면에 진입한다
    Then 오류 메시지가 표시된다
```

## Test Commands

```bash
# 전체 테스트
melos run test

# Feature별 테스트
melos run test --scope=feature_{feature_name}

# 커버리지 포함
melos run test:with-html-coverage

# BDD 테스트 생성
melos run test:bdd:generate --scope={feature_name}

# BDD 테스트 실행
melos run test:bdd --scope={feature_name}
```

## 핵심 규칙

### 테스트 구조
- Arrange → Act → Assert 패턴
- 하나의 테스트는 하나의 동작만 검증
- 테스트 간 독립성 유지

### Mocking
- `mocktail` 패키지 사용
- Repository/UseCase를 Mock으로 대체
- `registerFallbackValue` 필요 시 설정

### BDD 테스트
- Gherkin 문법 준수
- Step Definition 재사용
- 한글 시나리오 작성

### 커버리지
- 최소 80% 코드 커버리지 목표
- UseCase 100% 테스트 필수
- BLoC 주요 흐름 테스트 필수

## MCP Integration

| 단계 | MCP 서버 | 용도 |
|------|----------|------|
| 패턴 분석 | Context7 | flutter_test, bloc_test 문서 |
| 코드 검색 | Serena | 기존 테스트 패턴 참조 |
| 심볼 분석 | Serena | 테스트 대상 확인 |

## Examples

### UseCase 테스트 생성

```
/test unit GetUserUseCase --feature auth
```

### BLoC 테스트 생성

```
/test bloc HomeBloc --feature home
```

### Widget 테스트 생성

```
/test widget LoginPage --feature auth
```

### BDD 시나리오 생성

```
/test bdd community --coverage 90
```

## 참조

- 상세 구현: `.claude/agents/test.md`
- BDD 생성: `.claude/commands/bdd/generate.md`
- 테스트 예제: `feature/*/test/`

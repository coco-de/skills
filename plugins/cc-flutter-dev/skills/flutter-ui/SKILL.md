---
name: flutter-ui
description: Flutter UI 컴포넌트 및 패턴 구현 가이드. 페이지 구조, 상태 관리, 폼, 로딩, 오버레이 등 12개 Use Case 제공.
language: korean
invocationControl: semiauto
---

# Flutter UI Patterns

Flutter UI 컴포넌트 및 패턴 구현을 위한 마스터 스킬입니다.
12개 핵심 Use Case를 기반으로 일관된 UI 구현을 지원합니다.

## Scope and Capabilities

### 12개 Use Case

| # | Use Case | 설명 | 핵심 키워드 |
|---|----------|------|------------|
| 1 | **Page Structure** | 페이지 기본 구조 | Scaffold, AppBar, BlocProvider |
| 2 | **State Management** | 비동기 상태 관리 | BlocBuilder, BlocConsumer, MultiBlocProvider |
| 3 | **Local State** | 로컬 UI 상태 | HookWidget, useState, useEffect |
| 4 | **Typography** | 텍스트 스타일링 | Text chaining, typography tokens |
| 5 | **Buttons** | 버튼 variants | primary, ghost, card, icon |
| 6 | **Forms** | 폼 입력 및 검증 | Form, FormTextField, validation |
| 7 | **Loading States** | 로딩 및 스켈레톤 | Skeletonizer, loadingOr, emptyOrWhen |
| 8 | **Color System** | 색상 토큰 시스템 | ColorScheme, semantic colors |
| 9 | **Spacing** | 간격 및 레이아웃 | Gap, Spacing constants |
| 10 | **Overlays** | 오버레이 UI | Dialog, BottomSheet, Popover |
| 11 | **Lists** | 리스트 및 페이지네이션 | SliverList, RefreshIndicator, infinite scroll |
| 12 | **Navigation** | 라우팅 | GoRouter, TypedRoute |

## Quick Start

### 사용 방법

```
/flutter-ui [use-case]
```

### 예시

```
/flutter-ui page        # 페이지 구조 가이드
/flutter-ui form        # 폼 구현 가이드
/flutter-ui loading     # 로딩 상태 가이드
```

---

## 핵심 원칙

### Widget 선택 기준

| 상황 | 선택 | 이유 |
|------|------|------|
| 로컬 상태 필요 | `HookWidget` | useState, useEffect 사용 |
| 상태 없음 | `StatelessWidget` | 단순함, 성능 |
| BLoC 연결 | `HookWidget` + `BlocProvider` | 상태 분리 |
| 애니메이션 | `HookWidget` + `useAnimationController` | 자동 dispose |

### Import 규칙

```dart
// ✅ CORRECT: dependencies 패키지 통해 import
import 'package:dependencies/dependencies.dart';

// ❌ WRONG: 직접 import 금지
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:flutter_hooks/flutter_hooks.dart';
```

---

## Quick Reference

### 1. Page Structure

```dart
class MyPage extends HookWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => MyBloc()..add(const MyEvent.started()),
      child: Scaffold(
        headers: [
          AppBar(
            title: Text('페이지 제목'),
            leading: [BackButton()],
          ),
        ],
        child: _Body(),
      ),
    );
  }
}
```

### 2. State Management

```dart
// BlocBuilder - 상태 기반 UI
BlocBuilder<MyBloc, MyState>(
  buildWhen: (prev, curr) => prev.items != curr.items,
  builder: (context, state) => switch (state.status) {
    Status.loading => const LoadingWidget(),
    Status.success => SuccessWidget(data: state.data),
    Status.failure => ErrorWidget(message: state.error),
  },
)

// BlocConsumer - UI + 사이드 이펙트
BlocConsumer<MyBloc, MyState>(
  listener: (context, state) {
    if (state.isSuccess) context.pop();
  },
  builder: (context, state) => MyWidget(state: state),
)
```

### 3. Local State (Hooks)

```dart
class MyWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final isExpanded = useState(false);
    final controller = useTextEditingController();

    useEffect(() {
      // 초기화 로직
      return () { /* cleanup */ };
    }, []);

    return Column(
      children: [
        TextField(controller: controller),
        Switch(
          value: isExpanded.value,
          onChanged: (v) => isExpanded.value = v,
        ),
      ],
    );
  }
}
```

### 4. Typography

```dart
// Text chaining (권장)
Text('제목').lg.bold.baseContent
Text('본문').sm.semiBold.base200
Text('캡션').xs.normal.withOpacity(0.5)

// Typography 직접 접근
final typography = context.theme.typography;
Text('텍스트', style: typography.lg.merge(typography.semiBold))
```

### 5. Buttons

```dart
// Primary (주요 액션)
Button.primary(
  onPressed: onSubmit,
  expanded: true,
  child: Text('확인'),
)

// Ghost (보조 액션)
Button.ghost(
  onPressed: onCancel,
  child: Text('취소'),
)

// Card (카드 형태)
Button.card(
  onPressed: onTap,
  child: CardContent(),
)

// IconButton
IconButton.ghost(
  icon: HeroIcon(HeroIcons.pencilSquare),
  onPressed: onEdit,
)
```

### 6. Forms

```dart
Form(
  child: Column(
    children: [
      FormTextField(
        key: const Key('email'),
        label: Text('이메일'),
        placeholder: '이메일을 입력하세요',
        keyboardType: TextInputType.emailAddress,
        validator: (value) => value.isEmpty ? '필수 입력' : null,
      ),
      const Gap.s4(),
      Button.primary(
        expanded: true,
        enabled: isValid,
        onPressed: onSubmit,
        child: Text('제출'),
      ),
    ],
  ),
)
```

### 7. Loading States

```dart
// Skeletonizer (스켈레톤 로딩)
widget.skeletonizer(enabled: isLoading)

// 조건부 로딩
widget.loadingOr(
  isLoading: isLoading,
  loadingWidget: const CircularProgressIndicator(),
)

// 빈 상태 처리
listWidget.emptyOrWhen(
  condition: () => items.isEmpty,
  emptyWidget: const EmptyStateWidget(),
)
```

### 8. Color System

```dart
final colorScheme = context.theme.colorScheme;

// Semantic colors
colorScheme.primary       // 주요 액션
colorScheme.success       // 성공 상태
colorScheme.error         // 에러 상태
colorScheme.warning       // 경고

// Base colors
colorScheme.base100       // 배경
colorScheme.base200       // 카드 배경
colorScheme.baseContent   // 텍스트

// ❌ 금지
Color(0xFF123456)         // 하드코딩
Colors.blue               // 직접 색상 사용
```

### 9. Spacing

```dart
// Gap 사용
const Gap.s1()   // 4px
const Gap.s2()   // 8px
const Gap.s4()   // 16px
const Gap.s6()   // 24px

// Spacing 상수
EdgeInsets.symmetric(
  horizontal: Spacing.s4,
  vertical: Spacing.s2,
)

// ❌ 금지
SizedBox(height: 16)      // 하드코딩
EdgeInsets.all(16.0)      // 직접 값 사용
```

### 10. Overlays

```dart
// Dialog
showDialog(
  context: context,
  barrierColor: Colors.black.withValues(alpha: 0.2),
  builder: (context) => AlertDialog(
    title: Text('제목'),
    content: Text('내용'),
    actions: [
      Button.ghost(onPressed: () => Navigator.pop(context), child: Text('취소')),
      Button.primary(onPressed: onConfirm, child: Text('확인')),
    ],
  ),
)

// BottomSheet
showModalBottomSheet(
  context: context,
  builder: (context) => SafeArea(
    child: Padding(
      padding: EdgeInsets.all(Spacing.s4),
      child: content,
    ),
  ),
)
```

### 11. Lists

```dart
// RefreshIndicator + ListView
RefreshIndicator(
  onRefresh: () async {
    context.read<MyBloc>().add(const MyEvent.refreshed());
  },
  child: ListView.separated(
    itemCount: items.length,
    separatorBuilder: (_, __) => const Gap.s2(),
    itemBuilder: (context, index) => ItemCard(item: items[index]),
  ),
)

// SliverList (CustomScrollView 내부)
SliverList.separated(
  itemCount: items.length,
  separatorBuilder: (_, __) => const Gap.s2(),
  itemBuilder: (context, index) => ItemCard(item: items[index]),
)
```

### 12. Navigation

```dart
// GoRouter 정의
@TypedGoRoute<MyRoute>(path: '/my-page/:id')
class MyRoute extends GoRouteData {
  const MyRoute({required this.id});
  final String id;

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return MyPage(id: id);
  }
}

// 네비게이션
context.go('/my-page/123');
context.push('/my-page/123');
context.pop();

// TypedRoute 사용
const MyRoute(id: '123').go(context);
```

---

## Do / Don't 요약

| 항목 | ✅ Do | ❌ Don't |
|------|-------|---------|
| Import | `package:dependencies/dependencies.dart` | 직접 패키지 import |
| 색상 | `colorScheme.primary` | `Colors.blue`, `Color(0xFF...)` |
| 간격 | `const Gap.s4()`, `Spacing.s4` | `SizedBox(height: 16)` |
| 텍스트 | `Text('...').lg.bold` | `TextStyle(fontSize: 18)` |
| 상태 | `HookWidget` + `useState` | `StatefulWidget` (복잡한 경우 제외) |
| 비동기 | `BlocBuilder`, `BlocConsumer` | `FutureBuilder`, `StreamBuilder` |
| 생성자 | `const MyWidget({super.key})` | `MyWidget({Key? key}) : super(key: key)` |
| 투명도 | `withValues(alpha: 0.5)` | `withOpacity(0.5)` |

---

## Additional Resources

- [REFERENCE.md](REFERENCE.md) - 각 Use Case 상세 설명
- [TEMPLATES.md](TEMPLATES.md) - 복사 가능한 코드 템플릿
- [coui-flutter.md](../../rules/coui-flutter.md) - CoUI 컴포넌트 규칙

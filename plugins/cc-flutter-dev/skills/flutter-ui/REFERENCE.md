# Flutter UI Patterns - Reference

각 Use Case에 대한 상세 설명, 예시 코드, 주의사항을 제공합니다.

---

## 1. Page Structure

### 개요

모든 페이지는 일관된 구조를 따릅니다.

### 기본 구조

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
            leading: [
              IconButton.ghost(
                icon: HeroIcon(HeroIcons.arrowLeft),
                onPressed: () => context.pop(),
              ),
            ],
            trailing: [
              IconButton.ghost(
                icon: HeroIcon(HeroIcons.cog6Tooth),
                onPressed: onSettings,
              ),
            ],
          ),
        ],
        child: const _Body(),
      ),
    );
  }
}

class _Body extends StatelessWidget {
  const _Body();

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<MyBloc, MyState>(
      builder: (context, state) {
        return Padding(
          padding: EdgeInsets.symmetric(horizontal: Spacing.s4),
          child: Column(
            children: [
              // 컨텐츠
            ],
          ),
        );
      },
    );
  }
}
```

### 패턴 선택 기준

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| HookWidget + BlocProvider | 비동기 데이터 로드 | 상세 페이지, 리스트 |
| HookWidget만 | 로컬 상태만 필요 | 설정 페이지, 폼 |
| StatelessWidget | 상태 없음 | 정적 정보 페이지 |

### 주의사항

```dart
// ✅ CORRECT: BlocProvider는 페이지 레벨에서 생성
class MyPage extends HookWidget {
  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => MyBloc(),
      child: _Body(),
    );
  }
}

// ❌ WRONG: build 메서드 내에서 매번 생성 금지
class MyPage extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final bloc = MyBloc(); // 매번 새로 생성됨!
    return BlocProvider.value(
      value: bloc,
      child: _Body(),
    );
  }
}
```

---

## 2. State Management

### BLoC 패턴 개요

```
User Action → Event → BLoC → State → UI Update
```

### BlocBuilder

상태에 따른 UI 렌더링에 사용합니다.

```dart
BlocBuilder<MyBloc, MyState>(
  // 선택적: 리빌드 조건 지정
  buildWhen: (previous, current) => previous.items != current.items,
  builder: (context, state) {
    // switch expression으로 상태 분기 (권장)
    return switch (state) {
      MyStateInitial() => const SizedBox.shrink(),
      MyStateLoading() => const LoadingIndicator(),
      MyStateSuccess(:final data) => SuccessWidget(data: data),
      MyStateFailure(:final error) => ErrorWidget(message: error),
    };
  },
)
```

### BlocConsumer

UI 렌더링 + 사이드 이펙트가 모두 필요할 때 사용합니다.

```dart
BlocConsumer<AuthBloc, AuthState>(
  listenWhen: (previous, current) => previous.status != current.status,
  listener: (context, state) {
    // 사이드 이펙트: 네비게이션, 스낵바, 다이얼로그
    if (state.isAuthenticated) {
      context.go('/home');
    }
    if (state.hasError) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(state.errorMessage)),
      );
    }
  },
  buildWhen: (previous, current) => previous.formState != current.formState,
  builder: (context, state) {
    return LoginForm(
      isLoading: state.isLoading,
      isValid: state.isValid,
    );
  },
)
```

### BlocListener

사이드 이펙트만 필요할 때 사용합니다.

```dart
BlocListener<PaymentBloc, PaymentState>(
  listenWhen: (previous, current) => current.isCompleted,
  listener: (context, state) {
    showDialog(
      context: context,
      builder: (_) => SuccessDialog(),
    );
  },
  child: PaymentForm(),
)
```

### MultiBlocProvider

여러 BLoC이 필요한 페이지에서 사용합니다.

```dart
MultiBlocProvider(
  providers: [
    BlocProvider(create: (_) => UserBloc()),
    BlocProvider(create: (_) => SettingsBloc()),
    BlocProvider(create: (_) => NotificationBloc()),
  ],
  child: SettingsPage(),
)
```

### 이벤트 발송

```dart
// ✅ CORRECT: context.read 사용
Button.primary(
  onPressed: () {
    context.read<MyBloc>().add(const MyEvent.submitted());
  },
  child: Text('제출'),
)

// ❌ WRONG: context.watch로 이벤트 발송 금지
Button.primary(
  onPressed: () {
    context.watch<MyBloc>().add(...); // 불필요한 리빌드 발생
  },
)
```

---

## 3. Local State (Hooks)

### 기본 Hooks

```dart
class MyWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    // useState - 단순 상태
    final counter = useState(0);
    final isVisible = useState(true);

    // useTextEditingController - 텍스트 입력
    final controller = useTextEditingController();

    // useEffect - 사이드 이펙트
    useEffect(() {
      final subscription = stream.listen((value) {
        counter.value = value;
      });
      return subscription.cancel; // cleanup
    }, []); // 빈 배열 = componentDidMount

    return Column(
      children: [
        Text('Count: ${counter.value}'),
        TextField(controller: controller),
        Switch(
          value: isVisible.value,
          onChanged: (v) => isVisible.value = v,
        ),
      ],
    );
  }
}
```

### 애니메이션 Hooks

```dart
class AnimatedWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final animationController = useAnimationController(
      duration: const Duration(milliseconds: 300),
    );

    final animation = useAnimation(
      CurvedAnimation(
        parent: animationController,
        curve: Curves.easeInOut,
      ),
    );

    return FadeTransition(
      opacity: animation,
      child: Content(),
    );
  }
}
```

### useMemoized

비용이 큰 계산 결과를 캐시합니다.

```dart
final expensiveResult = useMemoized(
  () => computeExpensiveValue(items),
  [items], // 의존성 변경 시 재계산
);
```

### useCallback

콜백 함수를 메모이제이션합니다.

```dart
final onSubmit = useCallback(() {
  context.read<MyBloc>().add(const MyEvent.submitted());
}, []);
```

---

## 4. Typography

### Text Chaining 패턴

이 프로젝트의 표준 텍스트 스타일링 방식입니다.

```dart
// 크기
Text('텍스트').xs    // 12px
Text('텍스트').sm    // 14px
Text('텍스트').md    // 16px (기본)
Text('텍스트').lg    // 18px
Text('텍스트').xl    // 20px

// 굵기
Text('텍스트').normal     // 400
Text('텍스트').medium     // 500
Text('텍스트').semiBold   // 600
Text('텍스트').bold       // 700

// 색상
Text('텍스트').baseContent    // 기본 텍스트
Text('텍스트').base200        // 보조 텍스트
Text('텍스트').primary        // 주요 색상
Text('텍스트').success        // 성공
Text('텍스트').error          // 에러

// 조합
Text('제목').lg.bold.baseContent
Text('부제목').md.semiBold.base200
Text('본문').sm.normal.baseContent
Text('캡션').xs.normal.base200.withOpacity(0.7)
```

### Typography 직접 접근

특수한 경우 typography 객체에 직접 접근합니다.

```dart
final typography = context.theme.typography;

// 스타일 병합
Text(
  '텍스트',
  style: typography.lg.merge(typography.semiBold).copyWith(
    letterSpacing: 0.5,
  ),
)
```

### 주의사항

```dart
// ❌ WRONG: TextStyle 직접 정의 금지
Text(
  '텍스트',
  style: TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.bold,
  ),
)

// ✅ CORRECT: Text chaining 사용
Text('텍스트').lg.bold
```

---

## 5. Buttons

### Button Variants

```dart
// Primary - 주요 액션 (제출, 확인)
Button.primary(
  onPressed: onSubmit,
  expanded: true,        // 전체 너비
  enabled: isValid,      // 활성화 상태
  child: Text('확인'),
)

// Ghost - 보조 액션 (취소, 뒤로)
Button.ghost(
  onPressed: onCancel,
  child: Text('취소'),
)

// Card - 카드 형태 버튼
Button.card(
  style: const ButtonStyle.card().copyWith(
    borderRadius: RadiusScale.kBox,
  ),
  onPressed: onTap,
  child: Column(
    children: [
      Icon(Icons.settings),
      Text('설정'),
    ],
  ),
)

// Outline - 테두리 버튼
Button.outline(
  onPressed: onTap,
  child: Text('자세히 보기'),
)
```

### IconButton

```dart
IconButton.ghost(
  icon: HeroIcon(HeroIcons.pencilSquare),
  onPressed: onEdit,
)

IconButton.primary(
  icon: HeroIcon(HeroIcons.plus),
  onPressed: onAdd,
)
```

### 버튼 크기

```dart
Button.primary(
  style: const ButtonStyle.primary().copyWith(
    size: ButtonSize.small,
  ),
  onPressed: onTap,
  child: Text('작은 버튼'),
)
```

### 주의사항

```dart
// ❌ WRONG: 빈 style 파라미터 금지
Button.ghost(
  style: const ButtonStyle.ghost(
    // 빈 괄호
  ),
  onPressed: onTap,
  child: Text('취소'),
)

// ✅ CORRECT: 기본값 사용 시 style 생략
Button.ghost(
  onPressed: onTap,
  child: Text('취소'),
)
```

---

## 6. Forms

### 기본 Form 구조

```dart
class LoginForm extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final formKey = useMemoized(GlobalKey<FormState>.new);
    final emailController = useTextEditingController();
    final passwordController = useTextEditingController();
    final isValid = useState(false);

    void validate() {
      isValid.value = formKey.currentState?.validate() ?? false;
    }

    return Form(
      key: formKey,
      onChanged: validate,
      child: Column(
        children: [
          FormTextField(
            controller: emailController,
            label: Text('이메일'),
            placeholder: '이메일을 입력하세요',
            keyboardType: TextInputType.emailAddress,
            validator: (value) {
              if (value == null || value.isEmpty) {
                return '이메일을 입력하세요';
              }
              if (!value.contains('@')) {
                return '올바른 이메일 형식이 아닙니다';
              }
              return null;
            },
          ),
          const Gap.s4(),
          FormTextField(
            controller: passwordController,
            label: Text('비밀번호'),
            placeholder: '비밀번호를 입력하세요',
            obscureText: true,
            validator: (value) {
              if (value == null || value.length < 8) {
                return '8자 이상 입력하세요';
              }
              return null;
            },
          ),
          const Gap.s6(),
          Button.primary(
            expanded: true,
            enabled: isValid.value,
            onPressed: () {
              if (formKey.currentState!.validate()) {
                // 제출 로직
              }
            },
            child: Text('로그인'),
          ),
        ],
      ),
    );
  }
}
```

### FormTextField 속성

```dart
FormTextField(
  controller: controller,
  label: Text('라벨'),
  placeholder: '플레이스홀더',
  height: 56,                              // 높이
  keyboardType: TextInputType.text,        // 키보드 타입
  textInputAction: TextInputAction.next,   // 액션 버튼
  autofocus: true,                         // 자동 포커스
  obscureText: false,                      // 비밀번호 숨김
  maxLines: 1,                             // 최대 줄 수
  enabled: true,                           // 활성화 상태
  readOnly: false,                         // 읽기 전용
  validator: (value) => null,              // 검증 함수
  onChanged: (value) {},                   // 변경 콜백
  onSubmitted: (value) {},                 // 제출 콜백
)
```

### 검증 상태 시각화

```dart
enum ValidationState { pending, valid, invalid }

Widget buildValidationIcon(ValidationState state) {
  final colorScheme = context.theme.colorScheme;

  return switch (state) {
    ValidationState.pending => Icon(
        Icons.circle_outlined,
        color: colorScheme.baseContent,
      ),
    ValidationState.valid => Icon(
        Icons.check_circle,
        color: colorScheme.success,
      ),
    ValidationState.invalid => Icon(
        Icons.error,
        color: colorScheme.error,
      ),
  };
}
```

---

## 7. Loading States

### Skeletonizer

위젯을 스켈레톤 로딩 상태로 변환합니다.

```dart
BlocBuilder<MyBloc, MyState>(
  builder: (context, state) {
    return MyCard(
      title: state.title ?? 'Loading Title',
      subtitle: state.subtitle ?? 'Loading Subtitle',
    ).skeletonizer(enabled: state.isLoading);
  },
)
```

### loadingOr Extension

조건부 로딩 위젯을 표시합니다.

```dart
// 기본 사용
ContentWidget().loadingOr(
  isLoading: isLoading,
  loadingWidget: const CircularProgressIndicator(),
)

// Mock 데이터로 스켈레톤
ContentWidget().loadingOrWithMock(
  isLoading: isLoading,
  mockWidget: () => ContentWidget(data: MockData()),
)
```

### emptyOrWhen Extension

빈 상태 처리에 사용합니다.

```dart
ListView.builder(
  itemCount: items.length,
  itemBuilder: (context, index) => ItemCard(item: items[index]),
).emptyOrWhen(
  condition: () => items.isEmpty,
  emptyWidget: const EmptyStateWidget(
    icon: HeroIcon(HeroIcons.inbox),
    title: '항목이 없습니다',
    subtitle: '새 항목을 추가해보세요',
  ),
)
```

### 상태 기반 UI 분기

```dart
BlocBuilder<MyBloc, MyState>(
  builder: (context, state) {
    return switch (state.status) {
      LoadingStatus.initial => const SizedBox.shrink(),
      LoadingStatus.loading => const Center(
          child: CircularProgressIndicator(),
        ),
      LoadingStatus.success => SuccessWidget(data: state.data),
      LoadingStatus.failure => ErrorWidget(
          message: state.errorMessage,
          onRetry: () => context.read<MyBloc>().add(const MyEvent.retried()),
        ),
    };
  },
)
```

---

## 8. Color System

### ColorScheme 접근

```dart
final colorScheme = context.theme.colorScheme;
```

### Semantic Colors

| 토큰 | 용도 | 예시 |
|------|------|------|
| `primary` | 주요 액션, 브랜드 | 버튼, 링크 |
| `primaryContent` | primary 위의 텍스트 | 버튼 텍스트 |
| `success` | 성공 상태 | 완료, 승인 |
| `error` | 에러 상태 | 실패, 오류 |
| `warning` | 경고 상태 | 주의, 알림 |
| `info` | 정보 표시 | 안내, 팁 |

### Base Colors

| 토큰 | 용도 | 예시 |
|------|------|------|
| `base100` | 기본 배경 | 페이지 배경 |
| `base200` | 카드 배경 | 카드, 컨테이너 |
| `base300` | 구분선, 테두리 | 디바이더 |
| `baseContent` | 기본 텍스트 | 제목, 본문 |
| `neutral` | 중립 요소 | 비활성 버튼 |

### 사용 예시

```dart
Container(
  color: colorScheme.base100,
  child: Column(
    children: [
      Container(
        color: colorScheme.base200,
        child: Text('카드 내용').baseContent,
      ),
      Divider(color: colorScheme.base300),
      Container(
        color: colorScheme.success,
        child: Text('성공!').successContent,
      ),
    ],
  ),
)
```

### 투명도 적용

```dart
// ✅ CORRECT: withValues 사용
colorScheme.baseContent.withValues(alpha: 0.5)
Colors.black.withValues(alpha: 0.2)

// ❌ WRONG: withOpacity 사용 (deprecated)
colorScheme.baseContent.withOpacity(0.5)
```

---

## 9. Spacing

### Gap 위젯

```dart
// 상수 Gap
const Gap.s1()   // 4px
const Gap.s2()   // 8px
const Gap.s3()   // 12px
const Gap.s4()   // 16px
const Gap.s5()   // 20px
const Gap.s6()   // 24px
const Gap.s8()   // 32px

// 동적 Gap
Gap(Spacing.s4)
```

### Spacing 상수

```dart
// EdgeInsets에서 사용
EdgeInsets.all(Spacing.s4)
EdgeInsets.symmetric(
  horizontal: Spacing.s4,
  vertical: Spacing.s2,
)
EdgeInsets.only(
  top: Spacing.s4,
  bottom: Spacing.s2,
  left: Spacing.s4,
  right: Spacing.s4,
)
```

### 일관된 간격 사용

```dart
Column(
  children: [
    Header(),
    const Gap.s4(),        // 헤더 아래 16px
    ContentSection(),
    const Gap.s6(),        // 섹션 간 24px
    Footer(),
  ],
)

Padding(
  padding: EdgeInsets.symmetric(
    horizontal: Spacing.s4,  // 좌우 16px
    vertical: Spacing.s2,    // 상하 8px
  ),
  child: Content(),
)
```

---

## 10. Overlays

### Dialog

```dart
Future<bool?> showConfirmDialog(BuildContext context) {
  return showDialog<bool>(
    context: context,
    barrierColor: Colors.black.withValues(alpha: 0.2),
    builder: (context) => AlertDialog(
      title: Text('삭제 확인'),
      content: Text('정말 삭제하시겠습니까?'),
      actions: [
        Button.ghost(
          onPressed: () => Navigator.pop(context, false),
          child: Text('취소'),
        ),
        Button.primary(
          onPressed: () => Navigator.pop(context, true),
          child: Text('삭제'),
        ),
      ],
    ),
  );
}

// 사용
final result = await showConfirmDialog(context);
if (result == true) {
  // 삭제 수행
}
```

### BottomSheet

```dart
void showOptionsSheet(BuildContext context) {
  showModalBottomSheet(
    context: context,
    isScrollControlled: true,  // 높이 조절 가능
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
    ),
    builder: (context) => SafeArea(
      child: Padding(
        padding: EdgeInsets.all(Spacing.s4),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: HeroIcon(HeroIcons.pencil),
              title: Text('편집'),
              onTap: () {
                Navigator.pop(context);
                // 편집 로직
              },
            ),
            ListTile(
              leading: HeroIcon(HeroIcons.trash),
              title: Text('삭제').error,
              onTap: () {
                Navigator.pop(context);
                // 삭제 로직
              },
            ),
          ],
        ),
      ),
    ),
  );
}
```

### Popover

```dart
Popover(
  positions: [PopoverPosition.bottom],
  barrierColor: Colors.transparent,
  builder: (context) => Container(
    padding: EdgeInsets.all(Spacing.s2),
    decoration: BoxDecoration(
      color: colorScheme.base200,
      borderRadius: BorderRadius.circular(8),
      boxShadow: [
        BoxShadow(
          color: Colors.black.withValues(alpha: 0.1),
          blurRadius: 8,
        ),
      ],
    ),
    child: Column(
      mainAxisSize: MainAxisSize.min,
      children: [
        PopoverItem(title: '옵션 1', onTap: onOption1),
        PopoverItem(title: '옵션 2', onTap: onOption2),
      ],
    ),
  ),
  child: IconButton.ghost(
    icon: HeroIcon(HeroIcons.ellipsisVertical),
    onPressed: null, // Popover가 처리
  ),
)
```

---

## 11. Lists

### 기본 ListView

```dart
ListView.separated(
  padding: EdgeInsets.all(Spacing.s4),
  itemCount: items.length,
  separatorBuilder: (_, __) => const Gap.s2(),
  itemBuilder: (context, index) {
    final item = items[index];
    return ItemCard(item: item);
  },
)
```

### RefreshIndicator

```dart
RefreshIndicator(
  onRefresh: () async {
    context.read<MyBloc>().add(const MyEvent.refreshed());
    // BLoC 상태가 업데이트될 때까지 대기
    await context.read<MyBloc>().stream.firstWhere(
      (state) => !state.isRefreshing,
    );
  },
  child: ListView.builder(
    itemCount: items.length,
    itemBuilder: (context, index) => ItemCard(item: items[index]),
  ),
)
```

### CustomScrollView + SliverList

```dart
CustomScrollView(
  slivers: [
    SliverAppBar(
      title: Text('목록'),
      floating: true,
    ),
    SliverPadding(
      padding: EdgeInsets.symmetric(horizontal: Spacing.s4),
      sliver: SliverList.separated(
        itemCount: items.length,
        separatorBuilder: (_, __) => const Gap.s2(),
        itemBuilder: (context, index) => ItemCard(item: items[index]),
      ),
    ),
  ],
)
```

### 무한 스크롤 (Pagination)

```dart
class InfiniteListWidget extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final scrollController = useScrollController();

    useEffect(() {
      void onScroll() {
        if (scrollController.position.pixels >=
            scrollController.position.maxScrollExtent - 200) {
          context.read<MyBloc>().add(const MyEvent.loadMore());
        }
      }

      scrollController.addListener(onScroll);
      return () => scrollController.removeListener(onScroll);
    }, []);

    return BlocBuilder<MyBloc, MyState>(
      builder: (context, state) {
        return ListView.builder(
          controller: scrollController,
          itemCount: state.items.length + (state.hasMore ? 1 : 0),
          itemBuilder: (context, index) {
            if (index >= state.items.length) {
              return const Center(child: CircularProgressIndicator());
            }
            return ItemCard(item: state.items[index]);
          },
        );
      },
    );
  }
}
```

---

## 12. Navigation

### GoRouter 설정

```dart
// route 정의
@TypedGoRoute<HomeRoute>(
  path: '/',
  routes: [
    TypedGoRoute<ProfileRoute>(path: 'profile/:userId'),
    TypedGoRoute<SettingsRoute>(path: 'settings'),
  ],
)
class HomeRoute extends GoRouteData {
  const HomeRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const HomePage();
  }
}

class ProfileRoute extends GoRouteData {
  const ProfileRoute({required this.userId});
  final String userId;

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return ProfilePage(userId: userId);
  }
}
```

### 네비게이션 메서드

```dart
// 페이지 이동 (히스토리 교체)
context.go('/home');

// 페이지 추가 (히스토리 유지)
context.push('/details');

// 뒤로 가기
context.pop();

// 결과와 함께 뒤로 가기
context.pop(result);

// TypedRoute 사용 (타입 안전)
const ProfileRoute(userId: '123').go(context);
const ProfileRoute(userId: '123').push(context);
```

### 네비게이션 결과 받기

```dart
// 이동하는 페이지
Button.primary(
  onPressed: () async {
    final result = await context.push<String>('/select-item');
    if (result != null) {
      // 결과 처리
    }
  },
  child: Text('선택'),
)

// 결과 반환하는 페이지
Button.primary(
  onPressed: () => context.pop(selectedItem),
  child: Text('확인'),
)
```

### 딥 링크 파라미터

```dart
@TypedGoRoute<SearchRoute>(path: '/search')
class SearchRoute extends GoRouteData {
  const SearchRoute({this.query, this.category});

  final String? query;
  final String? category;

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return SearchPage(
      initialQuery: query,
      initialCategory: category,
    );
  }
}

// 쿼리 파라미터와 함께 이동
const SearchRoute(query: 'flutter', category: 'tutorial').go(context);
// → /search?query=flutter&category=tutorial
```

# Flutter UI Patterns - Templates

복사해서 바로 사용할 수 있는 코드 템플릿입니다.
주석으로 커스터마이징 포인트를 표시했습니다.

---

## 1. 기본 페이지 템플릿

### BLoC 페이지

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] 페이지 설명
class MyPage extends HookWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      // [TODO] BLoC 타입 변경
      create: (_) => MyBloc()..add(const MyEvent.started()),
      child: Scaffold(
        headers: [
          AppBar(
            // [TODO] 페이지 제목 변경
            title: Text('페이지 제목'),
            leading: [
              IconButton.ghost(
                icon: HeroIcon(HeroIcons.arrowLeft),
                onPressed: () => context.pop(),
              ),
            ],
            // [TODO] 필요한 경우 trailing 액션 추가
            trailing: const [],
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
    final colorScheme = context.theme.colorScheme;

    return BlocBuilder<MyBloc, MyState>(
      builder: (context, state) {
        // [TODO] 상태에 따른 UI 분기
        return switch (state.status) {
          LoadingStatus.initial || LoadingStatus.loading =>
            const Center(child: CircularProgressIndicator()),
          LoadingStatus.failure => _ErrorView(message: state.errorMessage),
          LoadingStatus.success => _SuccessView(data: state.data),
        };
      },
    );
  }
}

class _SuccessView extends StatelessWidget {
  const _SuccessView({required this.data});

  final MyData data;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.symmetric(horizontal: Spacing.s4),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Gap.s4(),
          // [TODO] 컨텐츠 구현
          Text('컨텐츠').lg.bold.baseContent,
        ],
      ),
    );
  }
}

class _ErrorView extends StatelessWidget {
  const _ErrorView({required this.message});

  final String message;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          HeroIcon(HeroIcons.exclamationCircle, size: 48),
          const Gap.s4(),
          Text(message).md.baseContent,
          const Gap.s4(),
          Button.primary(
            onPressed: () {
              context.read<MyBloc>().add(const MyEvent.retried());
            },
            child: Text('다시 시도'),
          ),
        ],
      ),
    );
  }
}
```

### 심플 페이지 (로컬 상태만)

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] 페이지 설명
class SimplePage extends HookWidget {
  const SimplePage({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = context.theme.colorScheme;
    // [TODO] 로컬 상태 정의
    final selectedIndex = useState(0);
    final isExpanded = useState(false);

    return Scaffold(
      headers: [
        AppBar(
          title: Text('페이지 제목'),
          leading: [
            IconButton.ghost(
              icon: HeroIcon(HeroIcons.arrowLeft),
              onPressed: () => context.pop(),
            ),
          ],
        ),
      ],
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: Spacing.s4),
        child: Column(
          children: [
            const Gap.s4(),
            // [TODO] 컨텐츠 구현
          ],
        ),
      ),
    );
  }
}
```

---

## 2. 폼 페이지 템플릿

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] 폼 페이지 설명
class MyFormPage extends HookWidget {
  const MyFormPage({super.key});

  @override
  Widget build(BuildContext context) {
    final colorScheme = context.theme.colorScheme;
    final formKey = useMemoized(GlobalKey<FormState>.new);

    // [TODO] 컨트롤러 정의
    final nameController = useTextEditingController();
    final emailController = useTextEditingController();

    final isValid = useState(false);
    final isLoading = useState(false);

    void validate() {
      isValid.value = formKey.currentState?.validate() ?? false;
    }

    Future<void> submit() async {
      if (!formKey.currentState!.validate()) return;

      isLoading.value = true;
      try {
        // [TODO] 제출 로직 구현
        await Future<void>.delayed(const Duration(seconds: 1));
        if (context.mounted) {
          context.pop();
        }
      } finally {
        isLoading.value = false;
      }
    }

    return Scaffold(
      headers: [
        AppBar(
          title: Text('폼 제목'),
          leading: [
            IconButton.ghost(
              icon: HeroIcon(HeroIcons.xMark),
              onPressed: () => context.pop(),
            ),
          ],
        ),
      ],
      child: SafeArea(
        child: Padding(
          padding: EdgeInsets.symmetric(horizontal: Spacing.s4),
          child: Form(
            key: formKey,
            onChanged: validate,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Gap.s4(),

                // [TODO] 폼 필드 정의
                FormTextField(
                  controller: nameController,
                  label: Text('이름'),
                  placeholder: '이름을 입력하세요',
                  validator: (value) {
                    if (value == null || value.isEmpty) {
                      return '이름을 입력하세요';
                    }
                    return null;
                  },
                ),

                const Gap.s4(),

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

                const Spacer(),

                // 제출 버튼
                Button.primary(
                  expanded: true,
                  enabled: isValid.value && !isLoading.value,
                  onPressed: submit,
                  child: isLoading.value
                      ? const CircularProgressIndicator()
                      : Text('제출'),
                ),

                const Gap.s4(),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
```

---

## 3. 리스트 페이지 템플릿

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] 리스트 페이지 설명
class MyListPage extends HookWidget {
  const MyListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => MyListBloc()..add(const MyListEvent.started()),
      child: Scaffold(
        headers: [
          AppBar(
            title: Text('목록'),
            trailing: [
              IconButton.ghost(
                icon: HeroIcon(HeroIcons.plus),
                onPressed: () => context.push('/create'),
              ),
            ],
          ),
        ],
        child: const _Body(),
      ),
    );
  }
}

class _Body extends HookWidget {
  const _Body();

  @override
  Widget build(BuildContext context) {
    final scrollController = useScrollController();

    // 무한 스크롤
    useEffect(() {
      void onScroll() {
        if (scrollController.position.pixels >=
            scrollController.position.maxScrollExtent - 200) {
          context.read<MyListBloc>().add(const MyListEvent.loadMore());
        }
      }

      scrollController.addListener(onScroll);
      return () => scrollController.removeListener(onScroll);
    }, []);

    return BlocBuilder<MyListBloc, MyListState>(
      builder: (context, state) {
        if (state.isInitialLoading) {
          return const Center(child: CircularProgressIndicator());
        }

        return RefreshIndicator(
          onRefresh: () async {
            context.read<MyListBloc>().add(const MyListEvent.refreshed());
            await context.read<MyListBloc>().stream.firstWhere(
              (s) => !s.isRefreshing,
            );
          },
          child: ListView.separated(
            controller: scrollController,
            padding: EdgeInsets.all(Spacing.s4),
            itemCount: state.items.length + (state.hasMore ? 1 : 0),
            separatorBuilder: (_, __) => const Gap.s2(),
            itemBuilder: (context, index) {
              if (index >= state.items.length) {
                return const Center(
                  child: Padding(
                    padding: EdgeInsets.all(16),
                    child: CircularProgressIndicator(),
                  ),
                );
              }
              return _ItemCard(item: state.items[index]);
            },
          ).emptyOrWhen(
            condition: () => state.items.isEmpty,
            emptyWidget: const _EmptyView(),
          ),
        );
      },
    );
  }
}

class _ItemCard extends StatelessWidget {
  const _ItemCard({required this.item});

  // [TODO] 아이템 타입 변경
  final MyItem item;

  @override
  Widget build(BuildContext context) {
    final colorScheme = context.theme.colorScheme;

    return Button.card(
      onPressed: () => context.push('/detail/${item.id}'),
      child: Padding(
        padding: EdgeInsets.all(Spacing.s4),
        child: Row(
          children: [
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(item.title).md.semiBold.baseContent,
                  const Gap.s1(),
                  Text(item.subtitle).sm.base200,
                ],
              ),
            ),
            HeroIcon(
              HeroIcons.chevronRight,
              color: colorScheme.base300,
            ),
          ],
        ),
      ),
    );
  }
}

class _EmptyView extends StatelessWidget {
  const _EmptyView();

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          HeroIcon(HeroIcons.inbox, size: 64),
          const Gap.s4(),
          Text('항목이 없습니다').lg.base200,
          const Gap.s2(),
          Text('새 항목을 추가해보세요').sm.base300,
        ],
      ),
    );
  }
}
```

---

## 4. 탭 페이지 템플릿

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] 탭 페이지 설명
class MyTabPage extends HookWidget {
  const MyTabPage({super.key});

  @override
  Widget build(BuildContext context) {
    final selectedTab = useState(0);

    // [TODO] 탭 정의
    final tabs = [
      _TabInfo(title: '첫 번째', icon: HeroIcons.home),
      _TabInfo(title: '두 번째', icon: HeroIcons.user),
      _TabInfo(title: '세 번째', icon: HeroIcons.cog6Tooth),
    ];

    return Scaffold(
      headers: [
        AppBar(
          title: Text('탭 페이지'),
        ),
      ],
      child: Column(
        children: [
          // 탭 바
          TabList(
            selectedIndex: selectedTab.value,
            onSelectedIndexChanged: (index) => selectedTab.value = index,
            tabs: tabs.map((tab) => Tab(label: tab.title)).toList(),
          ),

          // 탭 컨텐츠
          Expanded(
            child: IndexedStack(
              index: selectedTab.value,
              children: const [
                _FirstTabContent(),
                _SecondTabContent(),
                _ThirdTabContent(),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _TabInfo {
  const _TabInfo({required this.title, required this.icon});

  final String title;
  final HeroIcons icon;
}

class _FirstTabContent extends StatelessWidget {
  const _FirstTabContent();

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('첫 번째 탭 컨텐츠'),
    );
  }
}

class _SecondTabContent extends StatelessWidget {
  const _SecondTabContent();

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('두 번째 탭 컨텐츠'),
    );
  }
}

class _ThirdTabContent extends StatelessWidget {
  const _ThirdTabContent();

  @override
  Widget build(BuildContext context) {
    return const Center(
      child: Text('세 번째 탭 컨텐츠'),
    );
  }
}
```

---

## 5. 카드 위젯 템플릿

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] 카드 설명
class MyCard extends StatelessWidget {
  const MyCard({
    required this.title,
    required this.subtitle,
    this.onTap,
    super.key,
  });

  final String title;
  final String subtitle;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    final colorScheme = context.theme.colorScheme;

    return Button.card(
      onPressed: onTap,
      child: Container(
        padding: EdgeInsets.all(Spacing.s4),
        decoration: BoxDecoration(
          color: colorScheme.base200,
          borderRadius: BorderRadius.circular(RadiusScale.kBox),
        ),
        child: Row(
          children: [
            // 아이콘 영역
            Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                color: colorScheme.primary.withValues(alpha: 0.1),
                borderRadius: BorderRadius.circular(RadiusScale.kRound),
              ),
              child: Center(
                child: HeroIcon(
                  HeroIcons.star,
                  color: colorScheme.primary,
                ),
              ),
            ),

            const Gap.s3(),

            // 텍스트 영역
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(title).md.semiBold.baseContent,
                  const Gap.s1(),
                  Text(subtitle).sm.base200,
                ],
              ),
            ),

            // 화살표
            HeroIcon(
              HeroIcons.chevronRight,
              color: colorScheme.base300,
              size: 20,
            ),
          ],
        ),
      ),
    );
  }
}
```

---

## 6. 다이얼로그 템플릿

### 확인 다이얼로그

```dart
/// 확인 다이얼로그 표시
Future<bool> showConfirmDialog(
  BuildContext context, {
  required String title,
  required String message,
  String confirmText = '확인',
  String cancelText = '취소',
  bool isDestructive = false,
}) async {
  final result = await showDialog<bool>(
    context: context,
    barrierColor: Colors.black.withValues(alpha: 0.2),
    builder: (context) => AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        Button.ghost(
          onPressed: () => Navigator.pop(context, false),
          child: Text(cancelText),
        ),
        if (isDestructive)
          Button.primary(
            style: const ButtonStyle.primary().copyWith(
              backgroundColor: context.theme.colorScheme.error,
            ),
            onPressed: () => Navigator.pop(context, true),
            child: Text(confirmText),
          )
        else
          Button.primary(
            onPressed: () => Navigator.pop(context, true),
            child: Text(confirmText),
          ),
      ],
    ),
  );

  return result ?? false;
}

// 사용 예시
void onDeleteTap(BuildContext context) async {
  final confirmed = await showConfirmDialog(
    context,
    title: '삭제 확인',
    message: '정말 삭제하시겠습니까?\n이 작업은 되돌릴 수 없습니다.',
    confirmText: '삭제',
    cancelText: '취소',
    isDestructive: true,
  );

  if (confirmed && context.mounted) {
    context.read<MyBloc>().add(const MyEvent.deleted());
  }
}
```

### 입력 다이얼로그

```dart
/// 입력 다이얼로그 표시
Future<String?> showInputDialog(
  BuildContext context, {
  required String title,
  String? initialValue,
  String? placeholder,
  String confirmText = '확인',
  String cancelText = '취소',
}) async {
  final controller = TextEditingController(text: initialValue);

  final result = await showDialog<String>(
    context: context,
    barrierColor: Colors.black.withValues(alpha: 0.2),
    builder: (context) => AlertDialog(
      title: Text(title),
      content: FormTextField(
        controller: controller,
        placeholder: placeholder,
        autofocus: true,
      ),
      actions: [
        Button.ghost(
          onPressed: () => Navigator.pop(context),
          child: Text(cancelText),
        ),
        Button.primary(
          onPressed: () => Navigator.pop(context, controller.text),
          child: Text(confirmText),
        ),
      ],
    ),
  );

  controller.dispose();
  return result;
}
```

---

## 7. BottomSheet 템플릿

### 옵션 선택 BottomSheet

```dart
/// 옵션 선택 BottomSheet 표시
Future<T?> showOptionsSheet<T>(
  BuildContext context, {
  required String title,
  required List<OptionItem<T>> options,
}) {
  return showModalBottomSheet<T>(
    context: context,
    isScrollControlled: true,
    shape: const RoundedRectangleBorder(
      borderRadius: BorderRadius.vertical(top: Radius.circular(16)),
    ),
    builder: (context) => SafeArea(
      child: Padding(
        padding: EdgeInsets.all(Spacing.s4),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // 핸들
            Center(
              child: Container(
                width: 40,
                height: 4,
                decoration: BoxDecoration(
                  color: context.theme.colorScheme.base300,
                  borderRadius: BorderRadius.circular(2),
                ),
              ),
            ),
            const Gap.s4(),

            // 제목
            Text(title).lg.bold.baseContent,
            const Gap.s4(),

            // 옵션 목록
            ...options.map(
              (option) => ListTile(
                leading: option.icon != null
                    ? HeroIcon(option.icon!)
                    : null,
                title: Text(option.label),
                onTap: () => Navigator.pop(context, option.value),
              ),
            ),

            const Gap.s2(),
          ],
        ),
      ),
    ),
  );
}

class OptionItem<T> {
  const OptionItem({
    required this.label,
    required this.value,
    this.icon,
  });

  final String label;
  final T value;
  final HeroIcons? icon;
}

// 사용 예시
void onSortTap(BuildContext context) async {
  final result = await showOptionsSheet<SortOrder>(
    context,
    title: '정렬 기준',
    options: [
      OptionItem(label: '최신순', value: SortOrder.newest, icon: HeroIcons.arrowDown),
      OptionItem(label: '오래된순', value: SortOrder.oldest, icon: HeroIcons.arrowUp),
      OptionItem(label: '이름순', value: SortOrder.name, icon: HeroIcons.bars3),
    ],
  );

  if (result != null && context.mounted) {
    context.read<MyBloc>().add(MyEvent.sorted(result));
  }
}
```

---

## 8. Route 정의 템플릿

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

part 'my_feature_route.g.dart';

/// [TODO] 라우트 설명
@TypedGoRoute<MyFeatureRoute>(
  path: '/my-feature',
  routes: [
    TypedGoRoute<MyFeatureDetailRoute>(path: ':id'),
    TypedGoRoute<MyFeatureCreateRoute>(path: 'create'),
  ],
)
class MyFeatureRoute extends GoRouteData {
  const MyFeatureRoute();

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return const MyFeaturePage();
  }
}

class MyFeatureDetailRoute extends GoRouteData {
  const MyFeatureDetailRoute({required this.id});

  final String id;

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return MyFeatureDetailPage(id: id);
  }
}

class MyFeatureCreateRoute extends GoRouteData {
  const MyFeatureCreateRoute({this.parentId});

  final String? parentId;

  @override
  Widget build(BuildContext context, GoRouterState state) {
    return MyFeatureCreatePage(parentId: parentId);
  }
}
```

---

## 9. BLoC 이벤트/상태 템플릿

### Event 정의

```dart
import 'package:dependencies/dependencies.dart';

part 'my_event.freezed.dart';

@freezed
sealed class MyEvent with _$MyEvent {
  const factory MyEvent.started() = _Started;
  const factory MyEvent.refreshed() = _Refreshed;
  const factory MyEvent.loadMore() = _LoadMore;
  const factory MyEvent.itemSelected(String id) = _ItemSelected;
  const factory MyEvent.submitted() = _Submitted;
}
```

### State 정의

```dart
import 'package:dependencies/dependencies.dart';

part 'my_state.freezed.dart';

@freezed
abstract class MyState with _$MyState {
  const factory MyState({
    @Default(LoadingStatus.initial) LoadingStatus status,
    @Default([]) List<MyItem> items,
    @Default(false) bool hasMore,
    @Default('') String errorMessage,
    MyItem? selectedItem,
  }) = _MyState;
}

enum LoadingStatus { initial, loading, success, failure }

extension MyStateX on MyState {
  bool get isInitialLoading => status == LoadingStatus.initial || status == LoadingStatus.loading;
  bool get isRefreshing => status == LoadingStatus.loading && items.isNotEmpty;
  bool get hasError => status == LoadingStatus.failure;
}
```

### BLoC 정의

```dart
import 'package:core/core.dart';
import 'package:dependencies/dependencies.dart';

/// [TODO] BLoC 설명
class MyBloc extends Bloc<MyEvent, MyState> {
  /// [MyBloc]를 생성하고 초기 상태를 설정합니다.
  MyBloc() : super(const MyState()) {
    on<_Started>(_onStarted);
    on<_Refreshed>(_onRefreshed);
    on<_LoadMore>(_onLoadMore);
  }

  Future<void> _onStarted(_Started event, Emitter<MyState> emit) async {
    emit(state.copyWith(status: LoadingStatus.loading));

    // [TODO] 데이터 로드 로직 구현
    try {
      final items = await _fetchItems();
      if (isClosed) return;

      emit(state.copyWith(
        status: LoadingStatus.success,
        items: items,
        hasMore: items.length >= 20,
      ));
    } on Exception catch (e) {
      if (isClosed) return;
      emit(state.copyWith(
        status: LoadingStatus.failure,
        errorMessage: e.toString(),
      ));
    }
  }

  Future<void> _onRefreshed(_Refreshed event, Emitter<MyState> emit) async {
    emit(state.copyWith(status: LoadingStatus.loading));

    try {
      final items = await _fetchItems();
      if (isClosed) return;

      emit(state.copyWith(
        status: LoadingStatus.success,
        items: items,
        hasMore: items.length >= 20,
      ));
    } on Exception {
      if (isClosed) return;
      emit(state.copyWith(status: LoadingStatus.failure));
    }
  }

  Future<void> _onLoadMore(_LoadMore event, Emitter<MyState> emit) async {
    if (!state.hasMore || state.status == LoadingStatus.loading) return;

    try {
      final newItems = await _fetchItems(offset: state.items.length);
      if (isClosed) return;

      emit(state.copyWith(
        items: [...state.items, ...newItems],
        hasMore: newItems.length >= 20,
      ));
    } on Exception {
      // 무한 스크롤 실패는 무시
    }
  }

  // [TODO] 실제 데이터 로드 로직으로 교체
  Future<List<MyItem>> _fetchItems({int offset = 0}) async {
    // API 호출 또는 Repository 사용
    return [];
  }
}
```

---

## 사용 방법

1. 적절한 템플릿을 선택합니다.
2. `[TODO]` 주석을 찾아 프로젝트에 맞게 수정합니다.
3. 타입, 이름, 로직을 변경합니다.
4. 필요 없는 부분은 삭제합니다.

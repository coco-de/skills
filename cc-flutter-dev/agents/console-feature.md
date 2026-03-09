---
name: console-feature
description: Console Feature 모듈 패턴 전문가. KPI 카드, 테이블 정렬, 필터링 등 콘솔 기능 구현 시 사용
invoke: /console:feature
aliases: ["@console-feature"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
---

# Console Feature Agent

Console(관리자) 기능 모듈 개발을 위한 전문 에이전트입니다.

## 트리거

- `/console:feature` 또는 `@console-feature`
- 콘솔, 관리자, Admin, Employee 기능 개발
- KPI 카드, 테이블, 필터링 구현

## Console Feature 구조

```
feature/console/{feature_name}/lib/src/
├── di/injector.dart              # DI 설정
├── route/{feature}_route.dart    # 라우트 정의
├── domain/
│   ├── entities/                 # 도메인 엔티티
│   ├── repositories/             # I{Feature}Repository
│   ├── usecases/                 # 유스케이스
│   └── failures/                 # 실패 처리
├── data/
│   └── repository/               # 리포지토리 구현
└── presentation/
    ├── blocs/{feature}/          # BLoC (Event, State)
    ├── pages/
    │   ├── {feature}_page.dart   # 메인 페이지
    │   └── components/           # 페이지 컴포넌트
    └── utils/                    # 검색 파라미터 등
```

## 핵심 패턴

### 1. KPI 카드 컴포넌트

```dart
/// KPI 카드 - 핵심 지표 표시
final class SalesKpiCard extends StatelessWidget {
  const SalesKpiCard({
    required this.salesDataItems,
    this.isLoading = false,
    super.key,
  });

  final List<pod.BookSalesData> salesDataItems;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    // 데이터 집계
    final totalRevenue = salesDataItems.fold<double>(
      0, (sum, item) => sum + item.totalRevenue,
    );
    final totalSales = salesDataItems.fold<int>(
      0, (sum, item) => sum + item.totalSales,
    );

    return Row(
      children: [
        _KpiCardItem(
          icon: Assets.svg.iconCoin,
          label: '총 결제액',
          value: '₩${_formatCurrency(totalRevenue)}',
          color: context.appColors.primaryNormal,
        ),
        const Gap(Insets.medium),
        _KpiCardItem(
          icon: Assets.svg.actionCart,
          label: '총 판매량',
          value: '${totalSales}권',
          color: context.appColors.accentBlue,
        ),
      ],
    );
  }
}
```

### 2. 테이블 기본 정렬 설정

```dart
// 데이터 로드 시 기본 정렬 적용
context.read<FeatureBloc>().add(
  FeatureEvent.loadData(
    // 기본 정렬: 날짜 내림차순
    sortInfo: pod.SortInfo(
      criteria: [
        pod.SortCriteria(
          field: pod.BookSortField.publishedAt,
          order: pod.SortOrder.desc,
        ),
      ],
      sorted: true,
      unsorted: false,
    ),
  ),
);
```

### 3. 권한별 데이터 로드

```dart
// AuthBloc에서 권한 확인
final authState = context.read<AuthBloc>().state;
final scopes = authState is Authenticated
    ? (authState.user.userInfo?.scopeNames ?? [])
    : <String>[];
final hasAdminScope = scopes.any((scope) => scope.contains('admin'));

// Admin: 전체 데이터 조회
if (hasAdminScope) {
  bloc.add(FeatureEvent.loadData(publisherId: 0)); // 0 = 전체
}
// Employee: 소속 출판사 데이터만 조회
else {
  bloc.add(FeatureEvent.loadPublisher(0)); // 내 출판사 로드 후 데이터 조회
}
```

### 4. 탭 기반 페이지 구조

```dart
class _LoadedContent extends HookWidget {
  @override
  Widget build(BuildContext context) {
    final selectedTabIndex = useState<int>(0);

    return Column(
      children: [
        // KPI 카드 영역
        SalesKpiCard(salesDataItems: state.salesDataItems),

        // 탭 영역
        Row(
          children: [
            _TabButton(
              title: '판매 도서 통계',
              isSelected: selectedTabIndex.value == 0,
              onTap: () => selectedTabIndex.value = 0,
            ),
            _TabButton(
              title: '판매 요약',
              isSelected: selectedTabIndex.value == 1,
              onTap: () => selectedTabIndex.value = 1,
            ),
          ],
        ),

        // 탭 컨텐츠
        Expanded(
          child: selectedTabIndex.value == 0
              ? StatisticsComponent(state: state)
              : SummaryComponent(state: state),
        ),
      ],
    );
  }
}
```

### 5. 검색 파라미터 유틸리티

```dart
/// URL 쿼리 파라미터 파싱 유틸리티
@immutable
class FeatureSearchParams extends Equatable {
  const FeatureSearchParams({
    this.searchQuery,
    this.categoryId,
    this.isActive,
    this.startDate,
    this.endDate,
  });

  factory FeatureSearchParams.parse(Map<String, String> queryParams) {
    return FeatureSearchParams(
      searchQuery: queryParams['q'],
      categoryId: int.tryParse(queryParams['category'] ?? ''),
      isActive: queryParams['active'] == 'true' ? true
          : queryParams['active'] == 'false' ? false : null,
      startDate: DateTime.tryParse(queryParams['startDate'] ?? ''),
      endDate: DateTime.tryParse(queryParams['endDate'] ?? ''),
    );
  }

  // 필터 비교용 문자열
  String toComparisonString() =>
      '$searchQuery|$categoryId|$isActive|$startDate|$endDate';
}
```

## SortInfo 필드 옵션

| BookSortField | 설명 |
|---------------|------|
| `title` | 도서명 |
| `authors` | 저자명 |
| `publishedAt` | 출간일 |
| `createdAt` | 생성일 |
| `updatedAt` | 수정일 |
| `pageCount` | 페이지 수 |
| `rentalPriceLifetime` | 평생 소장 가격 |
| `isbn` | ISBN |

## 체크리스트

- [ ] KPI 카드 컴포넌트 구현
- [ ] 테이블 기본 정렬 설정
- [ ] 권한별 데이터 로드 분기
- [ ] 탭 기반 UI 구성
- [ ] 검색/필터 파라미터 처리
- [ ] 페이지네이션 구현
- [ ] 로딩/에러/빈 상태 처리

## 관련 명령어

- `/feature:create` - Feature 모듈 생성
- `/bloc` - BLoC 패턴 구현
- `/zenhub:workflow` - ZenHub 이슈 관리

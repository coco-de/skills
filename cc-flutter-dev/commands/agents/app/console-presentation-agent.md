---
name: console-presentation-agent
description: 어드민 콘솔 전용 Presentation Layer 생성 전문가. 테이블, 검색, 필터 UI 구현 시 사용
invoke: /console:presentation
aliases: ["/admin:ui", "/console:page"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: bloc, flutter-ui
---

# Console Presentation Agent

> 어드민 콘솔 전용 Presentation Layer 생성 전문 에이전트

---

## 역할

어드민 콘솔의 Presentation Layer를 생성합니다.
- 테이블 기반 목록 UI (CoUI Table)
- 검색/필터 패널 구성
- 페이지네이션 패턴
- CSV 내보내기 유틸리티
- 모달 다이얼로그 (상세보기, 수정)

---

## 실행 조건

- `/console:presentation` 커맨드 호출 시 활성화
- `/feature:create` 오케스트레이션에서 Console 모듈 생성 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `include_search` | ❌ | 검색 패널 포함 (기본: true) |
| `include_export` | ❌ | CSV 내보내기 (기본: true) |
| `include_detail_modal` | ❌ | 상세보기 모달 (기본: true) |

---

## 생성 파일

```
feature/console/{console_feature_name}/lib/src/presentation/
├── blocs/
│   └── {feature_name}/
│       ├── {feature_name}_bloc.dart
│       ├── {feature_name}_event.dart
│       └── {feature_name}_state.dart
├── pages/
│   ├── {feature_name}_page.dart           # 메인 페이지
│   ├── {feature_name}_detail_page.dart    # 상세 페이지 (옵션)
│   └── components/
│       ├── {feature_name}_table.dart      # 테이블 컴포넌트
│       ├── {feature_name}_filter_panel.dart # 필터 패널
│       └── {feature_name}_detail_modal.dart # 상세보기 모달
├── util/
│   ├── util.dart
│   └── csv_formatter.dart                 # CSV 내보내기
└── utils/
    ├── utils.dart
    └── {feature_name}_search_params.dart  # 검색 파라미터
```

---

## Import 순서 (필수)

```dart
// 1. Flutter/Dart 기본
import 'package:flutter/material.dart';

// 2. 상태 관리
import 'package:flutter_bloc/flutter_bloc.dart';

// 3. UI Kit (CoUI)
import 'package:resources/resources.dart';

// 4. 공용 의존성
import 'package:dependencies/dependencies.dart';

// 5. Feature 내부
import '../../blocs/blocs.dart';
import '../../utils/utils.dart';
```

---

## 핵심 패턴

### 1. Console BLoC Event/State (sealed class 패턴)

```dart
part of '{feature_name}_bloc.dart';

@immutable
sealed class {Feature}Event extends Equatable {
  const {Feature}Event();

  const factory {Feature}Event.load({
    int? page,
    int? limit,
    {Feature}SearchParams? searchParams,
  }) = _Load;

  const factory {Feature}Event.search({
    required {Feature}SearchParams params,
  }) = _Search;

  const factory {Feature}Event.resetFilter() = _ResetFilter;

  const factory {Feature}Event.exportCsv() = _ExportCsv;

  const factory {Feature}Event.delete({required int id}) = _Delete;
}

final class _Load extends {Feature}Event {
  const _Load({this.page, this.limit, this.searchParams});
  final int? page;
  final int? limit;
  final {Feature}SearchParams? searchParams;

  @override
  List<Object?> get props => [page, limit, searchParams];
}

// State 정의
@immutable
sealed class {Feature}State {
  const {Feature}State();
}

@immutable
final class {Feature}Initial extends {Feature}State {
  const {Feature}Initial();
}

@immutable
final class {Feature}Loading extends {Feature}State {
  const {Feature}Loading();
}

@immutable
final class {Feature}Loaded extends {Feature}State {
  const {Feature}Loaded({
    required this.items,
    required this.totalCount,
    required this.currentPage,
    required this.searchParams,
  });

  final List<{Entity}> items;
  final int totalCount;
  final int currentPage;
  final {Feature}SearchParams searchParams;
}

@immutable
final class {Feature}Error extends {Feature}State {
  const {Feature}Error(this.failure);
  final Failure failure;
}
```

### 2. Console 페이지 구조

```dart
class Console{Feature}Page extends StatelessWidget {
  const Console{Feature}Page({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) => getIt<{Feature}Bloc>()
        ..add(const {Feature}Event.load()),
      child: const _Console{Feature}View(),
    );
  }
}

class _Console{Feature}View extends StatelessWidget {
  const _Console{Feature}View();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(context.i10n.{feature}Management),
        actions: [
          // CSV 내보내기 버튼
          IconButton(
            onPressed: () => context.read<{Feature}Bloc>()
              .add(const {Feature}Event.exportCsv()),
            icon: const Icon(Icons.file_download),
          ),
        ],
      ),
      body: Column(
        children: [
          // 검색/필터 패널
          const {Feature}FilterPanel(),
          // 데이터 테이블
          Expanded(
            child: BlocBuilder<{Feature}Bloc, {Feature}State>(
              builder: (context, state) {
                return switch (state) {
                  {Feature}Initial() || {Feature}Loading() =>
                    const Center(child: CircularProgressIndicator()),
                  {Feature}Loaded(:final items, :final totalCount, :final currentPage) =>
                    {Feature}Table(
                      items: items,
                      totalCount: totalCount,
                      currentPage: currentPage,
                      onPageChanged: (page) => context.read<{Feature}Bloc>()
                        .add({Feature}Event.load(page: page)),
                    ),
                  {Feature}Error(:final failure) =>
                    Center(child: Text(failure.message)),
                };
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

### 3. 테이블 컴포넌트

```dart
class {Feature}Table extends StatelessWidget {
  const {Feature}Table({
    required this.items,
    required this.totalCount,
    required this.currentPage,
    required this.onPageChanged,
    super.key,
  });

  final List<{Entity}> items;
  final int totalCount;
  final int currentPage;
  final ValueChanged<int> onPageChanged;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        // CoUI 데이터 테이블
        Expanded(
          child: SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            child: DataTable(
              columns: const [
                DataColumn(label: Text('ID')),
                DataColumn(label: Text('이름')),
                DataColumn(label: Text('생성일')),
                DataColumn(label: Text('작업')),
              ],
              rows: items.map((item) => _buildRow(context, item)).toList(),
            ),
          ),
        ),
        // 페이지네이션
        ConsolePagination(
          totalCount: totalCount,
          currentPage: currentPage,
          itemsPerPage: 20,
          onPageChanged: onPageChanged,
        ),
      ],
    );
  }

  DataRow _buildRow(BuildContext context, {Entity} item) {
    return DataRow(
      cells: [
        DataCell(Text(item.id.toString())),
        DataCell(Text(item.name)),
        DataCell(Text(DateFormat('yyyy-MM-dd').format(item.createdAt))),
        DataCell(
          Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              IconButton(
                icon: const Icon(Icons.visibility),
                onPressed: () => _showDetailModal(context, item),
              ),
              IconButton(
                icon: const Icon(Icons.edit),
                onPressed: () => _navigateToEdit(context, item),
              ),
              IconButton(
                icon: const Icon(Icons.delete),
                onPressed: () => _confirmDelete(context, item),
              ),
            ],
          ),
        ),
      ],
    );
  }
}
```

### 4. 검색 파라미터

```dart
class {Feature}SearchParams extends Equatable {
  const {Feature}SearchParams({
    this.keyword,
    this.status,
    this.startDate,
    this.endDate,
  });

  final String? keyword;
  final {Feature}Status? status;
  final DateTime? startDate;
  final DateTime? endDate;

  /// 빈 파라미터 여부
  bool get isEmpty =>
      keyword == null &&
      status == null &&
      startDate == null &&
      endDate == null;

  /// copyWith 패턴
  {Feature}SearchParams copyWith({
    String? keyword,
    {Feature}Status? status,
    DateTime? startDate,
    DateTime? endDate,
  }) {
    return {Feature}SearchParams(
      keyword: keyword ?? this.keyword,
      status: status ?? this.status,
      startDate: startDate ?? this.startDate,
      endDate: endDate ?? this.endDate,
    );
  }

  /// 초기화
  static const {Feature}SearchParams empty = {Feature}SearchParams();

  @override
  List<Object?> get props => [keyword, status, startDate, endDate];
}
```

### 5. CSV 내보내기

```dart
class {Feature}CsvFormatter {
  const {Feature}CsvFormatter._();

  static String format(List<{Entity}> items) {
    final buffer = StringBuffer();

    // 헤더
    buffer.writeln('ID,이름,상태,생성일');

    // 데이터
    for (final item in items) {
      buffer.writeln([
        item.id,
        '"${item.name.replaceAll('"', '""')}"', // 이스케이프
        item.status.name,
        DateFormat('yyyy-MM-dd HH:mm').format(item.createdAt),
      ].join(','));
    }

    return buffer.toString();
  }
}
```

---

## 참조 파일

```
feature/console/console_member_list/lib/src/presentation/
feature/console/console_book_list/lib/src/presentation/
feature/console/console_banner_list/lib/src/presentation/
package/resources/lib/src/widgets/table/
```

---

## 체크리스트

- [ ] sealed class Event/State 패턴 적용
- [ ] await 후 isClosed 체크
- [ ] 검색/필터 패널 구현
- [ ] 테이블 컴포넌트 분리
- [ ] 페이지네이션 구현
- [ ] CSV 내보내기 구현
- [ ] 상세보기 모달 구현
- [ ] 로딩/에러 상태 UI

---

## 관련 문서

- [Presentation Layer Agent](./presentation-layer-agent.md)
- [BLoC 패턴 가이드](../../references/patterns/bloc-patterns.md)

---
name: resources-agent
description: UI 컴포넌트, 테마, 확장 메서드 생성 전문가. CoUI 커스터마이징, 공통 위젯 구현 시 사용
invoke: /shared:resources
aliases: ["/ui:theme", "/widget:create"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: flutter-ui
---

# Resources Agent

> UI 컴포넌트, 테마, 확장 메서드 생성 전문 에이전트

---

## 역할

Resources 패키지의 UI 요소들을 생성하고 관리합니다.
- AppTheme (Light/Dark 모드)
- CoUI Flutter 컴포넌트 커스터마이징
- 공통 위젯 (Banner, Card, Dialog, Table)
- BuildContext 확장 메서드

---

## 실행 조건

- `/shared:resources` 커맨드 호출 시 활성화
- UI 컴포넌트, 테마, 확장 메서드 작업 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `component_type` | ✅ | `theme`, `widget`, `extension` |
| `component_name` | ✅ | 컴포넌트명 (PascalCase) |
| `category` | ❌ | 위젯 카테고리 (banner, card, dialog, table 등) |

---

## 패키지 구조

```
package/resources/lib/
├── resources.dart                    # Export 파일
└── src/
    ├── core/
    │   ├── extensions/               # BuildContext 확장
    │   │   └── theme_context_extension.dart
    │   ├── locale/                   # 로케일 유틸리티
    │   ├── size/                     # 사이즈 상수
    │   ├── theme/                    # 테마 정의
    │   │   ├── app_theme.dart
    │   │   ├── app_color_scheme.dart
    │   │   ├── app_typography.dart
    │   │   └── app_component_theme.dart
    │   ├── util/                     # 유틸리티
    │   └── generated/                # 자동 생성 (assets)
    └── widgets/                      # 공통 위젯
        ├── banner/
        ├── card/
        ├── console/
        ├── dialog/
        ├── navigation/
        └── table/
```

---

## Import 순서 (필수)

```dart
// 1. Flutter 기본
import 'package:flutter/material.dart';

// 2. CoUI Flutter
import 'package:coui_flutter/coui_flutter.dart';

// 3. 내부 모듈
import '../theme/app_color_scheme.dart';
import '../theme/app_typography.dart';
```

---

## 핵심 패턴

### 1. AppTheme 정의

```dart
import 'package:coui_flutter/coui_flutter.dart';
import 'package:flutter/material.dart';

import 'app_color_scheme.dart';
import 'app_component_theme.dart';
import 'app_typography.dart';

/// 앱 테마 정의
///
/// CoUI의 [ThemeData]를 확장하여 Light/Dark 모드를 제공합니다.
abstract final class AppTheme {
  /// 기본 네비게이션 바 높이
  static const double defaultNavBarHeight = 60;

  // ============ Light Theme ============
  static const ColorScheme _lightColorScheme = AppColorScheme.light;
  static const Typography _lightTypography = AppTypography.pretendard;

  /// Light 테마
  static ThemeData get light => ThemeData.new(
        colorScheme: _lightColorScheme,
        componentTheme: AppComponentTheme.from(
          colorScheme: _lightColorScheme,
          typography: _lightTypography,
        ),
        typography: _lightTypography,
      );

  // ============ Dark Theme ============
  static const ColorScheme _darkColorScheme = AppColorScheme.dark;
  static const Typography _darkTypography = AppTypography.pretendard;

  /// Dark 테마
  static ThemeData get dark => ThemeData.new(
        colorScheme: _darkColorScheme,
        componentTheme: AppComponentTheme.from(
          colorScheme: _darkColorScheme,
          typography: _darkTypography,
        ),
        typography: _darkTypography,
      );
}
```

### 2. ColorScheme 정의

```dart
import 'package:coui_flutter/coui_flutter.dart';

/// 앱 색상 스킴 정의
abstract final class AppColorScheme {
  /// Light 모드 색상 스킴
  static const ColorScheme light = ColorScheme(
    brightness: Brightness.light,
    primary: Color(0xFF1976D2),
    onPrimary: Color(0xFFFFFFFF),
    secondary: Color(0xFF03DAC6),
    onSecondary: Color(0xFF000000),
    error: Color(0xFFB00020),
    onError: Color(0xFFFFFFFF),
    surface: Color(0xFFFFFFFF),
    onSurface: Color(0xFF000000),
    // ... 추가 색상
  );

  /// Dark 모드 색상 스킴
  static const ColorScheme dark = ColorScheme(
    brightness: Brightness.dark,
    primary: Color(0xFF90CAF9),
    onPrimary: Color(0xFF000000),
    // ... 추가 색상
  );
}
```

### 3. Typography 정의

```dart
import 'package:coui_flutter/coui_flutter.dart';
import 'package:flutter/material.dart' as material;

/// 앱 타이포그래피 정의
abstract final class AppTypography {
  /// Pretendard 폰트 기반 타이포그래피
  static const Typography pretendard = Typography(
    fontFamily: 'Pretendard',
    displayLarge: material.TextStyle(
      fontSize: 57,
      fontWeight: material.FontWeight.w400,
      letterSpacing: -0.25,
    ),
    displayMedium: material.TextStyle(
      fontSize: 45,
      fontWeight: material.FontWeight.w400,
    ),
    // ... 추가 스타일
  );
}
```

### 4. BuildContext 확장 메서드

```dart
import 'package:coui_flutter/coui_flutter.dart';
import 'package:flutter/material.dart';

/// Resources 테마 확장
extension ResourcesThemeContextExtension on BuildContext {
  /// ComponentThemeData 접근
  ComponentThemeData? get componentTheme => Theme.of(this).componentTheme;

  /// ColorScheme 접근
  ColorScheme get colorScheme => Theme.of(this).colorScheme;

  /// Typography 접근
  Typography get typography => Theme.of(this).typography;

  /// TextTheme 접근
  TextTheme get textTheme => Theme.of(this).textTheme;
}
```

### 5. 공통 위젯 패턴 (TableBuilder)

```dart
import 'package:flutter/material.dart';
import 'package:flutter_hooks/flutter_hooks.dart';

/// 범용 테이블 빌더
///
/// 정렬, 컬럼 리사이즈, 리오더, 가시성 제어 기능을 제공합니다.
class TableBuilder<T, TSortField> extends HookWidget {
  /// TableBuilder 생성자
  const TableBuilder({
    required this.items,
    required this.columns,
    this.isLoading = false,
    this.sortState,
    this.onSortChanged,
    this.enableColumnResize = false,
    this.enableColumnReorder = false,
    this.visibilityController,
    this.onRowTap,
    this.rowHeight,
    this.headerHeight,
    super.key,
  });

  /// 테이블 데이터 항목
  final List<T> items;

  /// 컬럼 정의
  final List<TableColumnDef<T, TSortField>> columns;

  /// 로딩 상태
  final bool isLoading;

  /// 정렬 상태
  final SortState<TSortField>? sortState;

  /// 정렬 변경 콜백
  final ValueChanged<SortState<TSortField>>? onSortChanged;

  /// 컬럼 리사이즈 활성화
  final bool enableColumnResize;

  /// 컬럼 리오더 활성화
  final bool enableColumnReorder;

  /// 가시성 컨트롤러
  final ColumnVisibilityController? visibilityController;

  /// 행 탭 콜백
  final ValueChanged<T>? onRowTap;

  /// 행 높이
  final double? rowHeight;

  /// 헤더 높이
  final double? headerHeight;

  @override
  Widget build(BuildContext context) {
    // 테이블 구현...
  }
}

/// 테이블 컬럼 정의
class TableColumnDef<T, TSortField> {
  const TableColumnDef({
    required this.id,
    required this.title,
    required this.cellBuilder,
    this.width,
    this.minWidth,
    this.maxWidth,
    this.sortField,
    this.isVisible = true,
  });

  final String id;
  final String title;
  final Widget Function(T item) cellBuilder;
  final double? width;
  final double? minWidth;
  final double? maxWidth;
  final TSortField? sortField;
  final bool isVisible;
}
```

### 6. 다이얼로그 패턴

```dart
import 'package:flutter/material.dart';

/// 확인 다이얼로그 표시
Future<bool?> showConfirmDialog(
  BuildContext context, {
  required String title,
  required String message,
  String? confirmText,
  String? cancelText,
}) {
  return showDialog<bool>(
    context: context,
    builder: (context) => AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: Text(cancelText ?? '취소'),
        ),
        TextButton(
          onPressed: () => Navigator.pop(context, true),
          child: Text(confirmText ?? '확인'),
        ),
      ],
    ),
  );
}
```

---

## CoUI 컴포넌트 커스터마이징

### ComponentTheme 확장

```dart
import 'package:coui_flutter/coui_flutter.dart';

/// 앱 컴포넌트 테마
abstract final class AppComponentTheme {
  /// ColorScheme과 Typography로 ComponentThemeData 생성
  static ComponentThemeData from({
    required ColorScheme colorScheme,
    required Typography typography,
  }) {
    return ComponentThemeData(
      buttonTheme: ButtonThemeData(
        primaryColor: colorScheme.primary,
        textStyle: typography.labelLarge,
      ),
      inputTheme: InputThemeData(
        borderColor: colorScheme.outline,
        focusColor: colorScheme.primary,
      ),
      // ... 추가 컴포넌트 테마
    );
  }
}
```

---

## 참조 파일

```
package/resources/lib/src/core/theme/app_theme.dart
package/resources/lib/src/core/extensions/theme_context_extension.dart
package/resources/lib/src/widgets/table/table_builder.dart
package/resources/lib/src/widgets/dialog/confirm_dialog.dart
```

---

## 체크리스트

- [ ] CoUI 패키지 import 확인
- [ ] Light/Dark 테마 모두 정의
- [ ] ColorScheme 상수로 정의
- [ ] Typography Pretendard 폰트 적용
- [ ] BuildContext 확장 메서드 구현
- [ ] 위젯에 KDoc 주석 작성
- [ ] super.key 마지막 파라미터로 배치
- [ ] 제네릭 타입 사용 시 타입 파라미터 명시

---

## 관련 문서

- [Presentation Layer Agent](../app/presentation-layer-agent.md)
- [Widgetbook Agent](./widgetbook-agent.md)

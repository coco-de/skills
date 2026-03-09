---
name: widgetbook-agent
description: Widgetbook 컴포넌트 전시 전문가. UseCase 작성, 컴포넌트 카탈로그 구성 시 사용
invoke: /shared:widgetbook
aliases: ["/widgetbook:add", "/catalog:create"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: flutter-ui
---

# Widgetbook Agent

> Widgetbook 컴포넌트 전시 전문 에이전트

---

## 역할

Widgetbook을 사용한 컴포넌트 카탈로그를 관리합니다.
- @UseCase 어노테이션 기반 컴포넌트 전시
- Addon 구성 (Viewport, Theme, Slang)
- Component, Feature, Foundation 구조
- Mock 객체 설정

---

## 실행 조건

- `/shared:widgetbook` 커맨드 호출 시 활성화
- 컴포넌트 카탈로그, UseCase 작성 시 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `component_name` | ✅ | 컴포넌트명 (PascalCase) |
| `category` | ❌ | `component`, `feature`, `foundation` (기본: `component`) |
| `path` | ❌ | Widgetbook 내 경로 |

---

## 패키지 구조

```
app/kobic_widgetbook/
├── lib/
│   ├── main.dart                     # 앱 진입점
│   ├── main.directories.g.dart       # 자동 생성
│   ├── add_on/                       # 커스텀 Addon
│   │   ├── add_on.dart
│   │   ├── slang_addon.dart
│   │   ├── view_ports.dart
│   │   └── widgetbook_group.dart
│   ├── component/                    # UI 컴포넌트
│   │   ├── component.dart
│   │   ├── widget_book_button.dart
│   │   ├── widget_book_input.dart
│   │   └── widget_book_card.dart
│   ├── feature/                      # Feature 컴포넌트
│   │   ├── feature.dart
│   │   ├── widget_book_home.dart
│   │   └── widget_book_profile.dart
│   └── foundation/                   # 기초 요소
│       ├── foundation.dart
│       ├── widget_book_colors.dart
│       └── widget_book_typography.dart
└── pubspec.yaml
```

---

## Import 순서 (필수)

```dart
// 1. Flutter 기본
import 'package:flutter/material.dart' as material;

// 2. Widgetbook 패키지
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';

// 3. UI Kit (CoUI)
import 'package:coui_flutter/coui_flutter.dart';

// 4. 내부 모듈
import 'add_on/add_on.dart';
import 'main.directories.g.dart';
```

---

## 핵심 패턴

### 1. 메인 앱 설정

```dart
import 'package:flutter/material.dart' as material;
import 'package:i10n/i10n.dart';
import 'package:resources/resources.dart';
import 'package:widgetbook/widgetbook.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';

import 'add_on/add_on.dart';
import 'main.directories.g.dart';

/// Widgetbook 앱 진입점
@App()
class WidgetbookApp extends material.StatelessWidget {
  /// WidgetbookApp 생성자
  const WidgetbookApp({super.key});

  @override
  material.Widget build(material.BuildContext context) {
    return Widgetbook.material(
      // 초기 라우트
      initialRoute: '/StorePage',

      // 자동 생성된 디렉토리
      directories: directories,

      // Addon 구성
      addons: [
        // 뷰포트 선택
        ViewportAddon(Viewports.all),

        // 위젯 인스펙터
        InspectorAddon(),

        // 다국어 지원
        SlangAddon(
          locales: AppLocaleUtils.supportedLocales,
          localeNames: {
            const material.Locale('en'): 'English',
            const material.Locale('ko'): '한국어',
            const material.Locale('ja'): '日本語',
            // ... 추가 로케일
          },
        ),

        // 테마 선택
        MaterialThemeAddon(
          themes: [
            WidgetbookTheme(
              name: 'Light',
              data: AppTheme.light,
            ),
            WidgetbookTheme(
              name: 'Dark',
              data: AppTheme.dark,
            ),
          ],
        ),

        // 정렬 옵션
        AlignmentAddon(initialAlignment: material.Alignment.topLeft),

        // 텍스트 스케일
        TextScaleAddon(initialScale: 1),

        // SafeArea 래퍼
        BuilderAddon(
          name: 'SafeArea',
          builder: (context, child) => material.SafeArea(child: child),
        ),
      ],
    );
  }
}

/// 앱 메인 함수
void main() {
  material.runApp(const WidgetbookApp());
}
```

### 2. UseCase 어노테이션 패턴

```dart
import 'package:coui_flutter/coui_flutter.dart';
import 'package:flutter/material.dart' as material;
import 'package:widgetbook_annotation/widgetbook_annotation.dart';

import 'add_on/widgetbook_group.dart';

/// Button 컴포넌트 UseCase
@UseCase(
  name: 'Button',
  type: Button,
  path: '[Component]',
)
material.Widget buildWidgetbookButtonUseCase(material.BuildContext context) {
  return WidgetbookGroup(
    label: 'Unibook Button',
    children: [
      // Primary Button
      WidgetbookButton(
        label: 'Primary Button',
        button: Button.primary(
          label: 'Primary',
          onPressed: () {},
        ),
      ),

      // Secondary Button
      WidgetbookButton(
        label: 'Secondary Button',
        button: Button.secondary(
          label: 'Secondary',
          onPressed: () {},
        ),
      ),

      // Outlined Button
      WidgetbookButton(
        label: 'Outlined Button',
        button: Button.outlined(
          label: 'Outlined',
          onPressed: () {},
        ),
      ),

      // Disabled Button
      WidgetbookButton(
        label: 'Disabled Button',
        button: Button.primary(
          label: 'Disabled',
          onPressed: null,
        ),
      ),

      // Loading Button
      WidgetbookButton(
        label: 'Loading Button',
        button: Button.primary(
          label: 'Loading',
          isLoading: true,
          onPressed: () {},
        ),
      ),
    ],
  );
}
```

### 3. WidgetbookGroup 헬퍼

```dart
import 'package:flutter/material.dart' as material;

/// Widgetbook 그룹 컨테이너
class WidgetbookGroup extends material.StatelessWidget {
  /// WidgetbookGroup 생성자
  const WidgetbookGroup({
    required this.label,
    required this.children,
    super.key,
  });

  /// 그룹 라벨
  final String label;

  /// 자식 위젯들
  final List<material.Widget> children;

  @override
  material.Widget build(material.BuildContext context) {
    return material.SingleChildScrollView(
      padding: const material.EdgeInsets.all(16),
      child: material.Column(
        crossAxisAlignment: material.CrossAxisAlignment.start,
        children: [
          material.Text(
            label,
            style: const material.TextStyle(
              fontSize: 24,
              fontWeight: material.FontWeight.bold,
            ),
          ),
          const material.SizedBox(height: 16),
          ...children.map((child) => material.Padding(
                padding: const material.EdgeInsets.only(bottom: 16),
                child: child,
              )),
        ],
      ),
    );
  }
}

/// Widgetbook 버튼 항목
class WidgetbookButton extends material.StatelessWidget {
  /// WidgetbookButton 생성자
  const WidgetbookButton({
    required this.label,
    required this.button,
    super.key,
  });

  /// 버튼 라벨
  final String label;

  /// 버튼 위젯
  final material.Widget button;

  @override
  material.Widget build(material.BuildContext context) {
    return material.Column(
      crossAxisAlignment: material.CrossAxisAlignment.start,
      children: [
        material.Text(
          label,
          style: const material.TextStyle(
            fontSize: 14,
            color: material.Colors.grey,
          ),
        ),
        const material.SizedBox(height: 8),
        button,
      ],
    );
  }
}
```

### 4. Slang Addon

```dart
import 'package:flutter/material.dart' as material;
import 'package:i10n/i10n.dart';
import 'package:widgetbook/widgetbook.dart';

/// Slang 다국어 Addon
class SlangAddon extends WidgetbookAddon<material.Locale> {
  /// SlangAddon 생성자
  SlangAddon({
    required this.locales,
    required this.localeNames,
    material.Locale? initialLocale,
  }) : super(
          name: 'Locale',
          initialSetting: initialLocale ?? locales.first,
        );

  /// 지원 로케일 목록
  final List<material.Locale> locales;

  /// 로케일별 표시 이름
  final Map<material.Locale, String> localeNames;

  @override
  List<Field> get fields => [
        ListField<material.Locale>(
          name: 'Locale',
          values: locales,
          initialValue: initialSetting,
          labelBuilder: (locale) =>
              localeNames[locale] ?? locale.languageCode,
        ),
      ];

  @override
  material.Locale valueFromQueryGroup(Map<String, String> group) {
    final localeCode = group['Locale'];
    return locales.firstWhere(
      (locale) => locale.languageCode == localeCode,
      orElse: () => locales.first,
    );
  }

  @override
  material.Widget buildUseCase(
    material.BuildContext context,
    material.Widget child,
    material.Locale setting,
  ) {
    return TranslationProvider(
      child: material.Builder(
        builder: (context) {
          // 로케일 변경
          LocaleSettings.setLocale(
            AppLocale.values.firstWhere(
              (l) => l.languageCode == setting.languageCode,
              orElse: () => AppLocale.en,
            ),
          );
          return child;
        },
      ),
    );
  }
}
```

### 5. Viewports 정의

```dart
import 'package:widgetbook/widgetbook.dart';

/// 뷰포트 정의
abstract final class Viewports {
  /// 모든 뷰포트
  static const List<Device> all = [
    // 모바일
    Device.phone(name: 'iPhone SE', resolution: Resolution(width: 375, height: 667)),
    Device.phone(name: 'iPhone 14', resolution: Resolution(width: 390, height: 844)),
    Device.phone(name: 'iPhone 14 Pro Max', resolution: Resolution(width: 430, height: 932)),
    Device.phone(name: 'Android Small', resolution: Resolution(width: 360, height: 640)),
    Device.phone(name: 'Android Large', resolution: Resolution(width: 412, height: 915)),

    // 태블릿
    Device.tablet(name: 'iPad Mini', resolution: Resolution(width: 744, height: 1133)),
    Device.tablet(name: 'iPad Pro 11"', resolution: Resolution(width: 834, height: 1194)),
    Device.tablet(name: 'iPad Pro 12.9"', resolution: Resolution(width: 1024, height: 1366)),

    // 데스크톱
    Device.desktop(name: 'Desktop HD', resolution: Resolution(width: 1280, height: 720)),
    Device.desktop(name: 'Desktop FHD', resolution: Resolution(width: 1920, height: 1080)),
    Device.desktop(name: 'Desktop 4K', resolution: Resolution(width: 3840, height: 2160)),
  ];

  /// 모바일 뷰포트만
  static const List<Device> mobile = [
    Device.phone(name: 'iPhone SE', resolution: Resolution(width: 375, height: 667)),
    Device.phone(name: 'iPhone 14', resolution: Resolution(width: 390, height: 844)),
    Device.phone(name: 'Android', resolution: Resolution(width: 412, height: 915)),
  ];

  /// 태블릿 뷰포트만
  static const List<Device> tablet = [
    Device.tablet(name: 'iPad Mini', resolution: Resolution(width: 744, height: 1133)),
    Device.tablet(name: 'iPad Pro', resolution: Resolution(width: 1024, height: 1366)),
  ];
}
```

### 6. Feature UseCase 예시

```dart
import 'package:feature_home/feature_home.dart';
import 'package:flutter/material.dart' as material;
import 'package:flutter_bloc/flutter_bloc.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';

/// Home 페이지 UseCase
@UseCase(
  name: 'HomePage',
  type: HomePage,
  path: '[Feature]/Home',
)
material.Widget buildWidgetbookHomePageUseCase(material.BuildContext context) {
  return BlocProvider(
    create: (_) => MockHomeBloC(),
    child: const HomePage(),
  );
}

/// Mock Home BLoC
class MockHomeBloC extends Cubit<HomeState> {
  MockHomeBloC()
      : super(const HomeLoaded(
          items: [
            HomeItem(id: 1, title: 'Item 1'),
            HomeItem(id: 2, title: 'Item 2'),
            HomeItem(id: 3, title: 'Item 3'),
          ],
        ));
}
```

### 7. Foundation UseCase 예시

```dart
import 'package:flutter/material.dart' as material;
import 'package:resources/resources.dart';
import 'package:widgetbook_annotation/widgetbook_annotation.dart';

/// Colors UseCase
@UseCase(
  name: 'Colors',
  type: material.ColorScheme,
  path: '[Foundation]',
)
material.Widget buildWidgetbookColorsUseCase(material.BuildContext context) {
  final colorScheme = material.Theme.of(context).colorScheme;

  return material.SingleChildScrollView(
    padding: const material.EdgeInsets.all(16),
    child: material.Column(
      crossAxisAlignment: material.CrossAxisAlignment.start,
      children: [
        _ColorTile(name: 'Primary', color: colorScheme.primary),
        _ColorTile(name: 'On Primary', color: colorScheme.onPrimary),
        _ColorTile(name: 'Secondary', color: colorScheme.secondary),
        _ColorTile(name: 'On Secondary', color: colorScheme.onSecondary),
        _ColorTile(name: 'Surface', color: colorScheme.surface),
        _ColorTile(name: 'On Surface', color: colorScheme.onSurface),
        _ColorTile(name: 'Error', color: colorScheme.error),
        _ColorTile(name: 'On Error', color: colorScheme.onError),
      ],
    ),
  );
}

class _ColorTile extends material.StatelessWidget {
  const _ColorTile({required this.name, required this.color});

  final String name;
  final material.Color color;

  @override
  material.Widget build(material.BuildContext context) {
    return material.Padding(
      padding: const material.EdgeInsets.only(bottom: 8),
      child: material.Row(
        children: [
          material.Container(
            width: 48,
            height: 48,
            decoration: material.BoxDecoration(
              color: color,
              borderRadius: material.BorderRadius.circular(8),
              border: material.Border.all(color: material.Colors.grey),
            ),
          ),
          const material.SizedBox(width: 16),
          material.Text(name),
        ],
      ),
    );
  }
}
```

---

## 빌드 명령어

```bash
# Widgetbook 실행
flutter run -t lib/main.dart -d chrome

# 코드 생성
cd app/kobic_widgetbook && dart run build_runner build --delete-conflicting-outputs

# 웹 빌드
flutter build web -t lib/main.dart
```

---

## 참조 파일

```
app/kobic_widgetbook/lib/main.dart
app/kobic_widgetbook/lib/add_on/slang_addon.dart
app/kobic_widgetbook/lib/add_on/view_ports.dart
app/kobic_widgetbook/lib/component/widget_book_button.dart
```

---

## 체크리스트

- [ ] @App() 어노테이션 적용
- [ ] @UseCase 어노테이션 작성
- [ ] path 경로 일관성 유지 ([Component], [Feature], [Foundation])
- [ ] Addon 구성 (Viewport, Theme, Slang)
- [ ] Mock 객체 설정 (BLoC, Repository)
- [ ] build_runner 실행
- [ ] 다양한 뷰포트에서 테스트

---

## 관련 문서

- [Resources Agent](./resources-agent.md)
- [Presentation Layer Agent](../app/presentation-layer-agent.md)

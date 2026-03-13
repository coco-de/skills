---
name: jaspr-patterns
description: Jaspr 웹 개발 패턴
---

# Jaspr Web Development Patterns (Jaspr 웹 개발 패턴)

## 트리거
- Jaspr Web 페이지나 컴포넌트를 새로 구현할 때
- SSR/SSG 설정을 구성할 때
- Jaspr 라우팅을 추가하거나 수정할 때
- CoUI 웹 컴포넌트(`coui_web`)를 Jaspr 프로젝트에서 활용할 때
- jaspr_content 기반 문서/콘텐츠 사이트를 구축할 때

## 동작
1. Jaspr 컴포넌트 구조를 설계한다
   - `StatelessComponent` 또는 `StatefulComponent` 선택
   - `build()` 메서드에서 HTML 요소 트리 구성 (`div`, `span`, `p`, `h1` 등)
   - `classes` 파라미터로 CoUI/Tailwind CSS 클래스 적용
   - `Styles(raw: {'key': 'value'})` 문법으로 인라인 스타일 적용
2. jaspr_router를 활용한 라우팅을 구성한다
   - `Router` + `ShellRoute` + `Route` 계층 구조
   - `state.path`로 현재 경로 감지, 활성 메뉴 표시
3. jaspr_content를 활용한 콘텐츠 사이트를 구성한다
   - `ContentApp.custom()` + `FilesystemLoader` + `MarkdownParser`
   - `PageConfig.all(components: [Callout()])` 커스텀 컴포넌트 등록
   - 마크다운 frontmatter (title, description, layout) 지원
4. CoUI 웹 컴포넌트를 통합한다
   - `coui_web` 패키지: Button, Badge, Alert, Card, Select, Toggle 등
   - CoUI 시맨틱 클래스 활용: `btn-primary`, `badge-accent`, `alert-success`

## Jaspr 핵심 패턴

### 컴포넌트 기본 구조
```dart
import 'package:jaspr/jaspr.dart';
import 'package:jaspr/dom.dart'; // div, span, p, h1, link, script 등

class MyPage extends StatelessComponent {
  const MyPage({super.key});

  @override
  Component build(BuildContext context) {
    return div([
      h1([text('Title')], classes: 'text-3xl font-bold'),
      p([text('Description')], classes: 'text-base-content/70 mt-2'),
    ], classes: 'p-6 max-w-6xl mx-auto');
  }
}
```

### 인라인 스타일
```dart
// Styles(raw: {...}) 문법 사용 (Styles.raw()는 없음!)
div([], styles: Styles(raw: {
  'font-size': '16px',
  'background-color': 'var(--primary)',
}));
```

### jaspr_content 문서 사이트
```dart
ContentApp.custom(
  loaders: [FilesystemLoader('content')],
  eagerlyLoadAllPages: true,
  configResolver: PageConfig.all(
    parsers: [MarkdownParser()],
    layouts: [EmptyLayout()],
    components: [Callout()], // Info/Warning/Success/Error 콜아웃
  ),
  routerBuilder: (contentRoutes) {
    final guideRoutes = contentRoutes.expand((r) => r).toList();
    return MyApp(guideRoutes: guideRoutes);
  },
);
```

### jaspr_router 라우팅
```dart
Router(routes: [
  ShellRoute(
    builder: (context, state, child) => Layout(currentPath: state.path, child: child),
    routes: [
      Route(path: '/', builder: (context, state) => const HomePage()),
      Route(path: '/about', builder: (context, state) => const AboutPage()),
      ...guideRoutes, // jaspr_content 마크다운 라우트
    ],
  ),
]);
```

### CoUI 컴포넌트 클래스
```dart
// 버튼
div([], classes: 'btn btn-primary btn-sm')
// 카드
div([], classes: 'card bg-base-200 shadow-md')
// 배지
span([], classes: 'badge badge-accent badge-lg')
// 테이블
Component.element(tag: 'table', classes: 'table table-zebra', children: [...])
```

## 출력
- Jaspr 컴포넌트 코드 (Dart)
- jaspr_router 라우팅 설정 코드
- jaspr_content 문서 사이트 설정
- CoUI 스타일이 적용된 HTML 구조

## 참고
- Jaspr는 Dart 기반 웹 프레임워크로, Flutter와 동일 언어를 사용하여 `coui_core` 토큰을 공유한다
- Jaspr의 컴포넌트 모델은 Flutter와 유사하지만 HTML 요소를 직접 렌더링한다
- `coui_web` 컴포넌트는 CoUI CSS 클래스를 Dart에서 타입 세이프하게 래핑한다
- `Document()` 위젯으로 `<head>` 설정 (CSS, 폰트, 스크립트 등)
- `Style(styles: [...])` 컴포넌트로 인라인 `<style>` 태그 생성
- `css('selector').styles(raw: {...})`로 CSS 규칙 정의
- Serverpod와의 통신은 생성된 클라이언트 코드를 통해 처리한다
- Domain 레이어의 Entity와 UseCase는 Flutter와 Jaspr 간 공유 가능하다

# Design System (CoUI 디자인 시스템)

## 트리거
- 새로운 디자인 토큰(색상, 타이포그래피, 간격)을 정의하거나 수정할 때
- DaisyUI 테마를 커스터마이징할 때
- CoUI 컴포넌트의 테마를 설정하거나 변경할 때
- 디자인 시스템 문서를 생성하거나 업데이트할 때

## 동작
1. 프로젝트의 기존 CoUI 디자인 토큰 파일을 분석한다
2. DaisyUI 테마 설정 파일(`tailwind.config.js` 또는 `theme.dart`)을 확인한다
3. 요청된 변경 사항에 따라 디자인 토큰을 생성하거나 수정한다
   - 색상 토큰: primary, secondary, accent, neutral 등 시맨틱 색상 정의
   - 타이포그래피 토큰: 폰트 패밀리, 크기, 두께, 줄 높이 정의
   - 간격 토큰: padding, margin, gap 등 일관된 간격 체계 정의
4. Flutter 측 `ThemeData`와 Jaspr Web 측 DaisyUI 테마 간 일관성을 검증한다
5. CoUI 컴포넌트에 테마가 올바르게 적용되는지 확인한다

## 출력
- 업데이트된 디자인 토큰 정의 파일 (Dart 상수 또는 JSON)
- DaisyUI 테마 설정 파일
- Flutter `ThemeData` 확장 코드
- 토큰 변경 사항 요약 및 영향 범위 분석

## 참고
- CoUI는 CoCode 팀의 자체 컴포넌트 라이브러리로, Flutter와 Jaspr Web 양쪽에서 사용된다
- DaisyUI 테마는 Jaspr Web 측에서 Tailwind CSS 기반으로 적용된다
- Flutter 측 테마는 `ThemeData`와 `ThemeExtension`을 활용하여 CoUI 토큰과 매핑한다
- 디자인 토큰 변경 시 Flutter와 Web 양쪽의 일관성을 반드시 유지해야 한다
- BLoC 패턴에서 테마 전환(다크 모드 등)은 `ThemeCubit`으로 관리한다

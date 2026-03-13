# cc-uiux-design

Cocode 팀을 위한 UI/UX 디자인 플러그인입니다.

## 개요

`coui_core` 디자인 토큰 시스템을 기반으로 3개 디자인 시스템(CoUI, M3 Expressive, Liquid Glass)을 지원하는 테마 관리 및 디자인 리뷰를 제공합니다.

## 스킬 목록

### design-system
- `CoreThemeData` 기반 테마 설정 및 커스터마이징
- `CoreColorScheme` 36개 색상 토큰 관리 (CoUI 20 + M3E 12 + LG 4)
- `CoreTypographyScale` 30개 텍스트 스타일 (15 baseline + 15 emphasized)
- `Spacing` 34단계, `CoreRadiusScale` 10단계, `CoreDuration` 12개 타이밍
- `CoreSpringConfig` 5개 모션 프리셋, `CoreSurfaceToken` 3종 표면 렌더링

### design-review
- `coui_core` 디자인 토큰 준수 여부 자동 검증
- Flutter(`coui_flutter`) / Web(`coui_web`) 간 API 일관성 검토
- 하드코딩된 값 탐지 및 토큰 대체 제안

## 기술 스택

- **토큰**: coui_core (디자인 토큰, 컨트랙트, 공유 로직)
- **Flutter**: coui_flutter (Flutter 위젯 구현)
- **Web**: coui_web (Jaspr + Tailwind CSS 구현)
- **테마**: CoUI 35+ 빌트인 테마, M3 Expressive, Liquid Glass
- **패턴**: BLoC 패턴, Clean Architecture

---
name: design-system
description: CoUI 디자인 시스템 토큰 및 테마
---

# Design System (CoUI 디자인 시스템)

## 트리거
- 새로운 디자인 토큰(색상, 타이포그래피, 간격, 모션)을 정의하거나 수정할 때
- DaisyUI 테마를 커스터마이징할 때
- CoUI 컴포넌트의 테마를 설정하거나 변경할 때
- 디자인 시스템 문서를 생성하거나 업데이트할 때
- 3개 디자인 시스템(DaisyUI, M3 Expressive, Liquid Glass) 간 전환 또는 비교할 때

## 동작
1. `coui_core` 패키지의 기존 디자인 토큰 파일을 분석한다
2. `CoreThemeData`를 기반으로 테마 설정을 확인한다
3. 요청된 변경 사항에 따라 디자인 토큰을 생성하거나 수정한다
4. Flutter 측 `coui_flutter`와 Jaspr Web 측 `coui_web` 간 일관성을 검증한다
5. CoUI 컴포넌트에 테마가 올바르게 적용되는지 확인한다

## coui_core 디자인 토큰 레퍼런스

### CoreThemeData (테마 최상위 객체)

```dart
import 'package:coui_core/coui_core.dart';

final theme = CoreThemeData(
  colorScheme: CoreColorScheme(...),   // 필수 — 36개 색상 토큰
  brightness: CoreBrightness.light,    // 필수 — light | dark
  designSystem: DesignSystem.daisyUI,  // 필수 — daisyUI | m3Expressive | liquidGlass
  typography: CoreTypographyScale.material3, // 선택 — 30개 텍스트 스타일
  cornerStyle: CornerStyle.rounded,    // 선택 — rounded | squircle | glassRounded
  defaultMotion: CoreSpringConfig.standard,  // 선택 — 애니메이션 기본값
  defaultSurface: CoreSurfaceToken.flat(),   // 선택 — 표면 렌더링
  textScaling: 1.0,    // 선택 — 전역 텍스트 스케일
  sizeScaling: 1.0,    // 선택 — 전역 사이즈 스케일
  radiusScaling: 1.0,  // 선택 — 전역 라디우스 스케일
);
```

### CoreColorScheme (36개 색상 토큰)

**DaisyUI Core (20개, 필수)**:
- `primary`, `primaryContent`
- `secondary`, `secondaryContent`
- `accent`, `accentContent`
- `neutral`, `neutralContent`
- `base100`, `base200`, `base300`, `baseContent`
- `info`, `infoContent`
- `success`, `successContent`
- `warning`, `warningContent`
- `error`, `errorContent`

**M3 Expressive Extended (12개, nullable)**:
- `tertiary`, `tertiaryContent`
- `surfaceContainerLowest`, `surfaceContainerLow`, `surfaceContainer`, `surfaceContainerHigh`, `surfaceContainerHighest`
- `outline`, `outlineVariant`
- `inverseSurface`, `inverseOnSurface`, `inversePrimary`

**Liquid Glass (4개, nullable)**:
- `glassTint`, `glassHighlight`, `glassShadow`, `glassIllumination`

```dart
final scheme = CoreColorScheme(
  primary: CoreColor.fromHex('#570DF8'),
  primaryContent: CoreColor.fromHex('#FFFFFF'),
  // ... 20개 필수 토큰
);

// 또는 Map에서 생성
final scheme = CoreColorScheme.fromMap(colorMap);
```

### CoreTypographyScale (30개 텍스트 스타일)

**Baseline (15개)**: displayLarge/Medium/Small, headlineLarge/Medium/Small, titleLarge/Medium/Small, bodyLarge/Medium/Small, labelLarge/Medium/Small

**Emphasized (15개)**: 각 baseline에 `Emphasized` 접미사 (더 무거운 font-weight)

```dart
final typography = CoreTypographyScale.material3;
final headline = typography.headlineLarge;
// → CoreTextStyle(fontSize: 32, lineHeight: 1.25, fontWeight: 400)
final scaled = typography.scale(0.875); // 전체 스케일
```

### Spacing (34개 값)

```dart
// Spacing.s0 (0) ~ Spacing.s96 (384)
// 주요: s1(4), s2(8), s3(12), s4(16), s6(24), s8(32), s12(48), s16(64)
```

### CoreRadiusScale (10단계 + 4 시맨틱 별칭)

```dart
// 스케일: none(0), extraExtraSmall(2), extraSmall(4), small(8), medium(12),
//         large(16), extraLarge(20), extraExtraLarge(28), extraExtraExtraLarge(32), full(9999)
// 시맨틱: box(16), field(4), selector(8), badge(9999)
```

### CoreComponentSize

```dart
enum CoreComponentSize { xs, sm, md, lg, xl }
```

### CoreDuration (12개 타이밍 값)

```dart
// instant(0ms), ultraShort(50ms), xs(100ms), short(150ms),
// normal(200ms), medium(300ms), long(400ms), xl(500ms)
// 시맨틱: pageTransition, modal(250ms), tooltipDelay, toast(3000ms)
```

### CoreSpringConfig (5개 프리셋)

```dart
// gentle(damping:0.8, stiffness:200), standard(0.7, 300),
// bouncy(0.5, 400), snappy(0.9, 500), stiff(1.0, 600)
```

### CoreMotionToken (sealed class)

```dart
// CssTransitionMotion — CSS transition 기반 (durationMs + easing)
// SpringMotion — 스프링 물리 기반 (dampingRatio + stiffness)
// GlassPhysicsMotion — Liquid Glass 물리 (spring + specularResponse)
```

### CoreSurfaceToken (표면 렌더링)

```dart
CoreSurfaceToken.flat()                          // 평면
CoreSurfaceToken.tonalElevation(elevation: 2)    // M3 tonal elevation (0-5)
CoreSurfaceToken.glass(opacity: 0.3, blur: 20, material: CoreGlassMaterial(...)) // 유리
```

### DesignSystem enum

```dart
enum DesignSystem { daisyUI, m3Expressive, liquidGlass }
```

| 차원 | DaisyUI | M3 Expressive | Liquid Glass |
|------|---------|---------------|--------------|
| 색상 | 20 시맨틱 토큰 | +12 surface/outline | +4 glass 토큰 |
| 모양 | rounded | squircle | glassRounded |
| 모션 | CSS transition | Spring physics | Glass physics |
| 표면 | flat | tonalElevation | glass |

## 출력
- `CoreThemeData` 기반 테마 설정 코드
- `CoreColorScheme` 정의 (DaisyUI/M3E/LG 레이어)
- DaisyUI `@plugin` CSS 테마 설정
- Flutter/Web 크로스 플랫폼 일관성 검증 결과

## 참고
- CoUI는 `coui_core` (토큰+컨트랙트), `coui_flutter` (Flutter 구현), `coui_web` (Jaspr Web 구현) 3개 패키지로 구성된다
- `coui_core`의 디자인 토큰은 플랫폼 무관하게 공유되는 순수 Dart 객체이다
- DaisyUI 테마는 Jaspr Web 측에서 `@plugin "daisyui"` CSS로 적용되며 35+ 빌트인 테마를 제공한다
- Flutter 측 테마는 `CoreThemeData`에서 직접 토큰을 읽어 위젯에 적용한다
- `CoreColorScheme.fromMap()`과 `toMap()`으로 JSON 직렬화/역직렬화가 가능하다
- `CoreThemeData.copyWith()`로 다크 모드 등 테마 변형을 생성한다

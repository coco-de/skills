---
name: design-review
description: 디자인 리뷰 체크리스트 및 프로세스
---

# Design Review (디자인 리뷰)

## 트리거
- UI 관련 코드 변경에 대한 리뷰가 요청될 때
- CoUI 컴포넌트 사용의 일관성을 검증할 때
- 새로운 화면이나 위젯이 추가될 때
- 디자인 토큰 준수 여부를 확인할 때

## 동작
1. 변경된 UI 코드에서 사용된 CoUI 컴포넌트를 식별한다
2. 하드코딩된 값이 있는지 검사한다:
   - 색상: `Color(0xFF...)` 대신 `CoreColorScheme` 토큰 사용 여부
   - 간격: 매직 넘버 대신 `Spacing.s4` 등 토큰 사용 여부
   - 라디우스: 직접 값 대신 `CoreRadiusScale.medium` 등 사용 여부
   - 타이포: 인라인 스타일 대신 `CoreTypographyScale` 참조 여부
   - 모션: 직접 Duration 대신 `CoreDuration.normal` 등 사용 여부
3. `CoreThemeData` 기반 테마 접근 패턴이 올바른지 확인한다
4. 컴포넌트 사용 패턴이 CoUI 가이드라인과 일치하는지 검증한다
5. `coui_flutter`와 `coui_web` 간 동일 컴포넌트의 API 일관성을 점검한다
6. 발견된 문제점과 개선 제안을 정리한다

## 검증 체크리스트

### 토큰 준수
- [ ] 색상은 `CoreColorScheme` 프로퍼티로 참조 (primary, secondary, accent, ...)
- [ ] 간격은 `Spacing` 상수 사용 (s0~s96)
- [ ] 라디우스는 `CoreRadiusScale` 사용 (none~full, box/field/selector/badge)
- [ ] 사이즈는 `CoreComponentSize` enum 사용 (xs/sm/md/lg/xl)
- [ ] 모션은 `CoreDuration` 또는 `CoreSpringConfig` 사용
- [ ] 타이포는 `CoreTypographyScale` 스타일 참조

### 컴포넌트 일관성
- [ ] Flutter: `coui_flutter` 위젯 사용 (Button, TextField, Select 등)
- [ ] Web: `coui_web` 컴포넌트 사용 (Button, Input, Select 등)
- [ ] 양 플랫폼에서 동일 컨트랙트(`coui_core` abstract interface) 준수
- [ ] 컴포넌트 인자 순서: DCM `arguments-ordering` 규칙 준수

### 디자인 시스템
- [ ] `DesignSystem` enum에 맞는 토큰 레이어 사용 (CoUI/M3E/LG)
- [ ] 다크 모드 대응: `CoreBrightness` 기반 분기
- [ ] `CornerStyle` 일관성 (rounded/squircle/glassRounded)

## 출력
- 디자인 일관성 검토 결과 보고서
- 하드코딩된 값 목록 및 토큰 대체 제안
- CoUI 가이드라인 위반 항목 및 수정 방법
- Flutter/Jaspr Web 간 불일치 항목

## 참고
- CoUI 표준에 정의된 컴포넌트만 사용해야 하며, 커스텀 위젯은 CoUI 확장으로 등록한다
- 색상은 반드시 `CoreColorScheme` 시맨틱 토큰을 사용하고 `Color(0xFF...)` 직접 사용을 지양한다
- DCM `no-magic-number` 규칙: 허용값(0, 1, 2, -1, 0.0, 1.0) 외 숫자는 상수로 추출한다
- Clean Architecture의 Presentation 레이어에서만 UI 컴포넌트를 참조한다
- BLoC의 State에서 UI 관련 로직을 분리하여 뷰는 순수 렌더링에 집중한다

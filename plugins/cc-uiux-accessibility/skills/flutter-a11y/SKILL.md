---
name: flutter-a11y
description: Flutter 접근성 구현 가이드
---

# Flutter Accessibility (Flutter 접근성)

## 트리거
- Flutter 위젯에 접근성 속성을 추가하거나 개선할 때
- 스크린 리더(TalkBack, VoiceOver) 지원을 구현할 때
- 명암비(contrast ratio)를 검증할 때
- CoUI 컴포넌트의 접근성 준수 여부를 점검할 때

## 동작
1. 대상 위젯 트리에서 `Semantics` 위젯 사용 현황을 분석한다
2. 인터랙티브 요소(버튼, 입력 필드 등)에 적절한 시맨틱 레이블이 있는지 확인한다
3. `ExcludeSemantics`, `MergeSemantics` 사용이 적절한지 검증한다
4. 이미지에 `semanticLabel`이 제공되는지 확인한다
5. CoUI 컴포넌트가 기본 접근성 속성을 올바르게 노출하는지 점검한다
6. 충분한 터치 타겟 크기(최소 48x48dp)를 확인한다
7. 명암비가 WCAG AA 기준(일반 텍스트 4.5:1, 큰 텍스트 3:1)을 충족하는지 검증한다

## 출력
- 접근성 개선이 필요한 위젯 목록
- `Semantics` 위젯 추가/수정 코드 제안
- 명암비 검증 결과
- 스크린 리더 테스트 가이드

## 참고
- Flutter의 `Semantics` 위젯은 네이티브 접근성 API(iOS: UIAccessibility, Android: AccessibilityNodeInfo)와 매핑된다
- CoUI 컴포넌트는 기본적으로 접근성 속성을 포함하도록 설계되어야 한다
- BLoC State 변경 시 접근성 알림(`SemanticsService.announce`)을 적절히 트리거한다
- Clean Architecture에서 접근성 관련 유틸리티는 Presentation 레이어의 공통 모듈에 위치한다

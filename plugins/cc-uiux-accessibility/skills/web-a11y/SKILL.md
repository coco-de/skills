---
name: web-a11y
description: Jaspr 웹 접근성 구현 가이드
---

# Jaspr Web Accessibility (Jaspr 웹 접근성)

## 트리거
- Jaspr Web 컴포넌트에 ARIA 속성을 추가할 때
- 키보드 네비게이션을 구현하거나 개선할 때
- WCAG 2.1 준수 여부를 검증할 때
- CoUI 웹 컴포넌트의 접근성을 점검할 때

## 동작
1. Jaspr 컴포넌트에서 생성되는 HTML 요소의 ARIA 속성을 분석한다
2. 인터랙티브 요소에 `role`, `aria-label`, `aria-describedby` 등이 적절히 설정되었는지 확인한다
3. 키보드 네비게이션 흐름(Tab 순서, 포커스 관리)을 검증한다
4. 동적 콘텐츠 변경 시 `aria-live` 영역이 올바르게 설정되었는지 확인한다
5. 폼 요소에 연관된 `label`이 있는지 점검한다
6. 색상 의존 정보 전달이 없는지 확인한다 (색각 이상 사용자 고려)
7. WCAG 2.1 AA 수준의 전체 체크리스트를 적용한다

## 출력
- ARIA 속성 추가/수정 코드 제안
- 키보드 네비게이션 개선 사항
- WCAG 2.1 준수 검증 결과 보고서
- 접근성 위반 항목 및 우선순위별 수정 가이드

## 참고
- Jaspr Web은 Dart로 작성된 서버 사이드 렌더링 프레임워크로, HTML/CSS 출력에 직접 ARIA 속성을 삽입한다
- CoUI 웹 컴포넌트는 독립적인 디자인 시스템이며, 기본 접근성 속성을 포함해야 한다
- Jaspr의 `DomComponent`에서 `attributes` 맵을 통해 ARIA 속성을 설정한다
- 서버 사이드 렌더링 특성상 초기 HTML에 접근성 속성이 포함되어 SEO와 접근성 모두에 유리하다

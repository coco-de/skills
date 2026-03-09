# Responsive & Adaptive Design (반응형/적응형 디자인)

## 트리거
- 다양한 화면 크기에 대응하는 레이아웃을 설계할 때
- 모바일/태블릿/데스크톱/웹 간 적응형 UI를 구현할 때
- 브레이크포인트를 정의하거나 수정할 때
- 플랫폼별 UI 차이를 처리할 때

## 동작
1. CoUI 브레이크포인트 시스템을 기반으로 레이아웃 전략을 수립한다
   - 모바일: < 600dp
   - 태블릿: 600dp ~ 1024dp
   - 데스크톱/웹: > 1024dp
2. Flutter에서 `LayoutBuilder`, `MediaQuery`를 활용한 반응형 레이아웃을 구성한다
3. 플랫폼 감지(`Platform`, `kIsWeb`)를 통해 적응형 UI를 분기한다
4. Jaspr Web에서는 DaisyUI/Tailwind 반응형 유틸리티를 활용한다
5. CoUI 컴포넌트의 반응형 변형(variant)을 적용한다

## 출력
- 반응형 레이아웃 코드 (Flutter `LayoutBuilder` 기반)
- 적응형 위젯 선택 로직
- Jaspr Web 반응형 스타일 코드
- 브레이크포인트 정의 상수

## 참고
- CoUI는 자체 브레이크포인트 시스템(`CoBreakpoint`)을 제공하며, Flutter와 Jaspr Web 모두에서 사용한다
- Flutter에서는 `CoResponsiveBuilder` 위젯으로 브레이크포인트별 UI를 분기한다
- Jaspr Web에서는 Tailwind의 `sm:`, `md:`, `lg:` 접두사를 CoUI 래퍼를 통해 사용한다
- 적응형 디자인 시 네비게이션 패턴이 플랫폼에 따라 변경된다 (모바일: BottomNav, 데스크톱: SideNav)
- BLoC에서 화면 크기 변경은 `LayoutCubit`으로 관리하여 상태를 중앙 집중화한다

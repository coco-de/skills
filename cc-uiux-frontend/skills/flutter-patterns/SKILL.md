# Flutter Development Patterns (Flutter 개발 패턴)

## 트리거
- 새로운 Flutter 화면이나 기능을 구현할 때
- BLoC 패턴 기반 상태 관리를 설계할 때
- Clean Architecture 레이어 구조를 적용할 때
- CoUI 컴포넌트를 Flutter 프로젝트에 통합할 때

## 동작
1. Clean Architecture 레이어 구조에 따라 파일 구조를 설계한다
   - Domain: Entity, UseCase, Repository Interface
   - Data: Repository Implementation, DataSource, Model
   - Presentation: BLoC, Page, Widget
2. BLoC 패턴에 맞춰 상태 관리 코드를 생성한다
   - Event 정의: 사용자 액션 및 시스템 이벤트
   - State 정의: 로딩, 성공, 실패 등 상태 모델링
   - BLoC 로직: Event를 받아 State를 emit
3. CoUI 컴포넌트를 활용하여 UI를 구성한다
   - CoUI 위젯 선택 및 속성 설정
   - 디자인 토큰 기반 스타일링
4. 의존성 주입(DI) 설정을 확인한다 (get_it, injectable 등)

## 출력
- Clean Architecture 기반 파일/폴더 구조
- BLoC (Event, State, Bloc) 코드
- CoUI 컴포넌트를 사용한 UI 코드
- 의존성 주입 등록 코드

## 참고
- CoCode 프로젝트는 feature-first 폴더 구조를 사용한다 (`lib/features/{feature_name}/`)
- BLoC에서 비즈니스 로직은 UseCase를 통해 호출하며, BLoC이 직접 Repository를 참조하지 않는다
- CoUI 컴포넌트는 `CoButton`, `CoCard`, `CoTextField` 등 `Co` 접두사를 사용한다
- Serverpod 클라이언트와의 통신은 Data 레이어의 DataSource에서 처리한다
- Freezed 패키지를 활용하여 불변 State 클래스를 생성한다

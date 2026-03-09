# Jaspr Web Development Patterns (Jaspr 웹 개발 패턴)

## 트리거
- Jaspr Web 페이지나 컴포넌트를 새로 구현할 때
- SSR(서버 사이드 렌더링) 설정을 구성할 때
- Jaspr 라우팅을 추가하거나 수정할 때
- CoUI 웹 컴포넌트를 Jaspr 프로젝트에서 활용할 때

## 동작
1. Jaspr 컴포넌트 구조를 설계한다
   - `StatelessComponent` 또는 `StatefulComponent` 선택
   - `build()` 메서드에서 HTML 요소 트리 구성
2. SSR 설정을 확인하고 구성한다
   - 서버 사이드에서 초기 데이터를 로드하는 패턴 적용
   - SEO를 위한 메타 태그 및 구조화된 데이터 설정
3. 라우팅을 구성한다
   - 페이지별 라우트 정의
   - 동적 라우트 파라미터 처리
   - 네비게이션 가드 설정
4. CoUI 웹 컴포넌트를 통합한다
   - DaisyUI 기반 스타일링 적용
   - CoUI 디자인 토큰과 매핑

## 출력
- Jaspr 컴포넌트 코드 (Dart)
- 라우팅 설정 코드
- SSR 데이터 로딩 패턴 코드
- DaisyUI/CoUI 스타일이 적용된 HTML 구조

## 참고
- Jaspr는 Dart로 작성된 웹 프레임워크로, Flutter와 동일한 언어를 사용하여 코드 공유가 가능하다
- Jaspr의 컴포넌트 모델은 Flutter와 유사하지만 HTML 요소를 직접 렌더링한다
- CoUI 웹 컴포넌트는 DaisyUI CSS 클래스를 Dart에서 타입 세이프하게 사용할 수 있게 래핑한다
- Serverpod와의 통신은 생성된 클라이언트 코드를 통해 처리한다
- Domain 레이어의 Entity와 UseCase는 Flutter와 Jaspr 간 공유할 수 있다

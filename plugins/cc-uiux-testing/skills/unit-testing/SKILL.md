# Dart Unit Testing (Dart 단위 테스트)

## 트리거
- 새로운 비즈니스 로직이나 유틸리티 함수에 대한 테스트를 작성할 때
- BLoC의 이벤트-상태 변환 로직을 테스트할 때
- UseCase나 Repository의 단위 테스트가 필요할 때
- 모킹(Mocking) 전략을 설계할 때

## 동작
1. 테스트 대상 클래스와 메서드를 분석한다
2. 테스트 파일 구조를 설정한다
   - `test/` 디렉토리에 소스 구조를 미러링
   - `_test.dart` 접미사 규칙 적용
3. 모킹 전략을 수립한다
   - Mocktail을 사용하여 의존성을 모킹
   - Repository, DataSource, 외부 서비스 모킹
4. BLoC 테스트를 작성한다
   - `bloc_test` 패키지의 `blocTest()` 활용
   - Event 입력에 대한 State 시퀀스 검증
   - `setUp`에서 모킹된 의존성 주입
5. 테스트 케이스를 구조화한다
   - `group()`으로 관련 테스트 그룹화
   - `setUp()`, `tearDown()`으로 테스트 환경 관리
   - Edge case와 에러 케이스 포함

## 출력
- Dart 단위 테스트 코드 (`*_test.dart`)
- Mock 클래스 정의
- BLoC 테스트 코드 (`blocTest()` 활용)
- 테스트 커버리지 보고서 가이드

## 참고
- Cocode 프로젝트는 Mocktail을 기본 모킹 라이브러리로 사용한다 (Mockito 대비 코드 생성 불필요)
- BLoC 테스트 시 `bloc_test` 패키지의 `blocTest()`를 사용하여 `act`, `expect`, `verify`를 선언적으로 작성한다
- Clean Architecture 덕분에 각 레이어를 독립적으로 테스트할 수 있다 (UseCase는 Repository 모킹, BLoC은 UseCase 모킹)
- Freezed로 생성된 State/Event 클래스는 `==` 연산자가 자동 구현되어 테스트 비교가 용이하다
- Serverpod 생성 코드(클라이언트)도 모킹하여 서버 의존 없이 테스트한다

# Integration Testing (통합 테스트)

## 트리거
- End-to-End 사용자 시나리오를 테스트할 때
- Flutter 앱과 Serverpod 서버 간 통합을 검증할 때
- 여러 화면에 걸친 워크플로우를 테스트할 때
- 배포 전 전체 시스템 동작을 확인할 때

## 동작
1. Flutter 통합 테스트를 설정한다
   - `integration_test/` 디렉토리에 테스트 파일 생성
   - `IntegrationTestWidgetsFlutterBinding.ensureInitialized()` 호출
   - 실제 또는 테스트 Serverpod 서버 연결 설정
2. 사용자 시나리오를 구현한다
   - 로그인 -> 화면 이동 -> 데이터 CRUD 등 실제 사용 흐름 시뮬레이션
   - `tester.tap()`, `tester.enterText()` 등으로 인터랙션 수행
   - `tester.pumpAndSettle()`로 비동기 작업 완료 대기
3. Serverpod 통합 테스트를 작성한다
   - `withServerpod()` 헬퍼를 활용한 서버 측 테스트
   - 테스트 전용 데이터베이스 환경 설정
   - 엔드포인트 호출 및 응답 검증
   - 트랜잭션 롤백으로 테스트 격리 보장
4. 테스트 데이터를 관리한다
   - Fixture/Factory 패턴으로 테스트 데이터 생성
   - 테스트 간 데이터 격리

## 출력
- Flutter 통합 테스트 코드 (`integration_test/`)
- Serverpod 통합 테스트 코드
- 테스트 데이터 Fixture/Factory
- CI에서 실행 가능한 테스트 스크립트

## 참고
- Flutter 통합 테스트는 실제 디바이스나 에뮬레이터에서 실행되며, CI에서는 Chrome(Web) 또는 에뮬레이터를 사용한다
- Serverpod의 `withServerpod()` 테스트 유틸리티는 테스트용 Session을 자동 생성한다
- 통합 테스트에서는 모킹을 최소화하고 실제 Serverpod 서버와 PostgreSQL을 사용한다
- Clean Architecture의 모든 레이어를 관통하는 테스트로, 레이어 간 통합이 올바른지 검증한다

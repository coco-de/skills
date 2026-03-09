# Monitoring (모니터링)

## 트리거
- 앱 크래시 리포팅을 설정할 때
- Serverpod 서버 헬스 체크를 구성할 때
- 로그 수집 및 분석 파이프라인을 구축할 때
- 알림 규칙을 정의할 때

## 동작
1. Flutter 앱 크래시 리포팅을 설정한다
   - Firebase Crashlytics 또는 Sentry 연동
   - BLoC에서 발생하는 에러를 자동 보고하도록 `BlocObserver` 설정
   - 사용자 컨텍스트(로그인 상태, 화면 등) 첨부
2. Serverpod 서버 모니터링을 구성한다
   - 헬스 체크 엔드포인트 구현 (`/health`)
   - API 응답 시간 메트릭 수집
   - 데이터베이스 연결 풀 상태 모니터링
   - 에러율 및 요청 처리량 추적
3. 로그 집계를 설정한다
   - Serverpod 로깅 설정 (`log` 레벨 관리)
   - 구조화된 로그 포맷(JSON) 적용
   - 로그 수집 서비스 연동 (CloudWatch, Datadog 등)
4. 알림 및 대응 프로세스를 정의한다
   - 에러율 임계값 초과 시 알림
   - 서버 다운 감지 및 자동 복구
   - 인시던트 대응 프로세스

## 출력
- 크래시 리포팅 설정 코드
- 서버 헬스 체크 엔드포인트 코드
- 로그 수집 설정 파일
- 알림 규칙 정의서

## 참고
- Serverpod는 내장 로깅 시스템을 제공하며, `session.log()`를 통해 요청별 로그를 기록한다
- Flutter에서 `FlutterError.onError`와 `PlatformDispatcher.instance.onError`를 설정하여 전역 에러를 캡처한다
- BLoC 에러는 `addError()`를 통해 전파되며, `BlocObserver.onError`에서 중앙 처리한다
- Clean Architecture에서 로깅은 Infrastructure 레이어의 공통 서비스로 제공한다
- Jaspr Web 모니터링은 브라우저 Performance API와 Core Web Vitals 메트릭을 활용한다

# Performance Testing (성능 테스트)

## 트리거
- Flutter 앱의 프레임 렌더링 성능을 분석할 때
- 화면 전환이나 애니메이션이 느려질 때
- Serverpod API 응답 시간을 측정할 때
- 메모리 누수가 의심될 때

## 동작
1. Flutter DevTools를 활용한 프로파일링을 수행한다
   - Timeline 뷰에서 프레임 렌더링 시간 분석
   - CPU Profiler로 핫스팟 함수 식별
   - Memory 뷰에서 메모리 사용량 및 누수 탐지
2. 프레임 분석을 수행한다
   - 60fps/120fps 타겟 기준으로 jank 프레임 식별
   - `PerformanceOverlay`를 활용한 실시간 프레임 모니터링
   - 빌드/레이아웃/페인트 단계별 소요 시간 분석
3. 위젯 리빌드 최적화를 분석한다
   - `const` 생성자 활용 여부 확인
   - BLoC `buildWhen` 조건 최적화
   - `RepaintBoundary` 활용 검토
4. Serverpod API 성능을 측정한다
   - 엔드포인트 응답 시간 벤치마크
   - 데이터베이스 쿼리 실행 계획 분석
   - 동시 요청 처리 성능 테스트

## 출력
- 성능 프로파일링 결과 보고서
- Jank 프레임 목록 및 원인 분석
- 최적화 권고 사항 (위젯 리빌드, 쿼리 튜닝 등)
- 성능 벤치마크 스크립트

## 참고
- Flutter의 프로파일 모드(`--profile`)에서 성능을 측정해야 정확한 결과를 얻을 수 있다
- BLoC 패턴에서 불필요한 State emit을 방지하면 위젯 리빌드를 최소화할 수 있다
- CoUI 컴포넌트의 `const` 생성자 지원 여부를 확인하고, 가능한 `const`로 인스턴스화한다
- Serverpod의 데이터베이스 쿼리는 `EXPLAIN ANALYZE`로 실행 계획을 확인하여 인덱스 활용을 검증한다
- 대량 리스트 렌더링 시 `ListView.builder`와 CoUI의 가상 스크롤 컴포넌트를 사용한다

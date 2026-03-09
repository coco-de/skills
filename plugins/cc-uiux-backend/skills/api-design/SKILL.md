# Serverpod API Design (Serverpod API 설계)

## 트리거
- 새로운 Serverpod 엔드포인트를 설계할 때
- 직렬화 가능한 모델 클래스를 정의할 때
- 인증/인가 로직을 구현할 때
- API 버저닝이나 구조 변경이 필요할 때

## 동작
1. Serverpod 엔드포인트 클래스를 설계한다
   - `Endpoint` 클래스 상속 및 메서드 정의
   - `Session` 객체를 통한 컨텍스트 접근
   - 적절한 반환 타입 설정
2. 직렬화 모델을 정의한다
   - `protocol/*.yaml` 파일에 모델 스키마 작성
   - `serverpod generate` 명령으로 코드 생성
   - 클라이언트/서버 간 공유 모델 관리
3. 인증을 구현한다
   - Serverpod Auth 모듈 설정
   - `session.authenticated` 검증
   - 역할 기반 접근 제어(RBAC) 적용
4. 에러 처리 패턴을 적용한다
   - `SerializableException` 활용
   - 클라이언트 측 에러 핸들링

## 출력
- Serverpod 엔드포인트 코드
- Protocol YAML 모델 정의
- 인증/인가 미들웨어 코드
- 생성된 클라이언트 코드 가이드

## 참고
- Serverpod는 Dart 풀스택 프레임워크로, 클라이언트 코드를 자동 생성한다
- `protocol/*.yaml`에 정의된 모델은 서버와 클라이언트(Flutter, Jaspr) 양쪽에서 공유된다
- Clean Architecture에서 Serverpod 엔드포인트는 Infrastructure 레이어에 위치하며, UseCase를 호출한다
- Serverpod의 `Session` 객체는 요청 컨텍스트, 인증 정보, 데이터베이스 접근을 제공한다
- BLoC에서 Serverpod 클라이언트 호출은 Repository 구현체를 통해 수행한다

# Serverpod Database Design (Serverpod 데이터베이스 설계)

## 트리거
- 새로운 데이터베이스 테이블을 설계할 때
- 테이블 간 관계(Relations)를 정의할 때
- 마이그레이션을 생성하거나 적용할 때
- 쿼리 최적화가 필요할 때

## 동작
1. Serverpod 프로토콜 YAML에서 모델과 테이블을 정의한다
   - 필드 타입, nullable, 기본값 설정
   - `table` 키워드로 데이터베이스 매핑 선언
   - 인덱스 정의
2. 테이블 간 관계를 설정한다
   - 1:1, 1:N, N:M 관계 정의
   - `relation` 키워드 활용
   - 외래 키 및 참조 무결성 설정
3. 마이그레이션을 관리한다
   - `serverpod create-migration` 명령 실행
   - 마이그레이션 파일 검토 및 수정
   - 롤백 전략 수립
4. 쿼리 패턴을 구현한다
   - Serverpod의 타입 세이프 쿼리 빌더 활용
   - 트랜잭션 처리
   - 페이지네이션 구현

## 출력
- Protocol YAML 모델 정의 (테이블 매핑 포함)
- 마이그레이션 SQL 파일
- Repository 구현체의 쿼리 코드
- 인덱스 및 성능 최적화 제안

## 참고
- Serverpod는 PostgreSQL을 기본 데이터베이스로 사용한다
- 모델 정의는 `protocol/*.yaml`에서 관리하며, `serverpod generate`로 Dart 코드와 SQL을 자동 생성한다
- Clean Architecture에서 데이터베이스 접근은 Data 레이어의 Repository 구현체에서만 수행한다
- Serverpod의 `Session.db`를 통해 데이터베이스에 접근하며, 타입 세이프한 쿼리를 지원한다
- 대량 데이터 처리 시 Serverpod의 스트리밍 쿼리와 배치 처리를 활용한다

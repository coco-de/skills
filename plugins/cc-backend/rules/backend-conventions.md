---
name: backend-conventions
description: Serverpod 백엔드 코딩 컨벤션
globs: ["**/server/lib/src/**/*.dart", "**/*.spy.yaml"]
---

# 백엔드 코딩 컨벤션

## 레이어 구조

- Endpoint → Service → Repository → DB
- Endpoint에 비즈니스 로직 금지
- Endpoint에 DB 쿼리 직접 작성 금지
- Repository 간 직접 호출 금지 (Service에서 조율)

## 엔드포인트 규칙

- App 엔드포인트와 Console 엔드포인트 분리
- 인증 필요 시 `requireLogin => true`
- 메서드명: `get`, `list`, `create`, `update`, `delete` 접두사

## 모델 규칙

- Entity에 `createdAt: DateTime`, `updatedAt: DateTime?` 필수
- 모든 필드에 한글 주석(`###`) 추가
- 외래키에 인덱스 필수
- DTO는 Entity와 분리 (`_create_request`, `_update_request`, `_list_response`)

## 트랜잭션 규칙

- 트랜잭션 내에서 `tx` 사용 (`session` 아님)
- 다중 DB 작업은 반드시 트랜잭션으로 감싸기
- 트랜잭션 관리는 Service 레이어에서만

## 캐싱 규칙

- 반드시 `lifetime` 설정
- 엔티티 수정 시 관련 캐시 무효화
- 다중 서버 환경에서 `global` 캐시 사용

## 테스팅 규칙

- 엔드포인트는 `endpoints` 파라미터로 호출
- 인증 테스트: 인증됨/미인증/권한부족 3가지 케이스
- 동시 트랜잭션 테스트: `rollbackDatabase: disabled`

## 로깅 규칙

- 민감 데이터 로깅 금지
- InternalSession은 반드시 close
- 세션 종료 후 세션 사용 금지

## 코드 생성

- `.spy.yaml` 수정 후 반드시 `serverpod generate`
- Entity 변경 후 반드시 `serverpod create-migration`
- 마이그레이션 적용 후 커밋

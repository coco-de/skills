---
name: api-security
description: Serverpod API 보안 구현
---

# Serverpod API Security (Serverpod API 보안)

## 트리거
- Serverpod 엔드포인트의 보안을 설계하거나 검토할 때
- 인증/인가 체계를 구현할 때
- 입력 검증 로직을 추가할 때
- Rate Limiting을 설정할 때

## 동작
1. 인증(Authentication)을 구현한다
   - Serverpod Auth 모듈 설정 (이메일, 소셜 로그인 등)
   - JWT 또는 세션 기반 인증 흐름 구성
   - `session.authenticated`를 통한 인증 상태 검증
   - 토큰 갱신(Refresh Token) 메커니즘 구현
2. 인가(Authorization)를 구현한다
   - 역할 기반 접근 제어(RBAC) 설계
   - 엔드포인트별 권한 검사 로직
   - 리소스 소유권 검증 (자신의 데이터만 접근)
3. 입력 검증을 적용한다
   - 모든 엔드포인트 파라미터의 타입/범위/포맷 검증
   - SQL 인젝션 방지 (Serverpod ORM의 파라미터 바인딩 활용)
   - XSS 방지를 위한 출력 이스케이핑
4. Rate Limiting을 설정한다
   - IP 기반/사용자 기반 요청 제한
   - 로그인 시도 횟수 제한
   - API 사용량 모니터링

## 출력
- 인증/인가 구현 코드
- 입력 검증 유틸리티 코드
- Rate Limiting 설정
- API 보안 체크리스트 결과

## 참고
- Serverpod의 엔드포인트 메서드에서 `session.authenticated`가 null이면 인증되지 않은 요청이다
- Serverpod Auth 모듈은 Google, Apple, Firebase 등 다양한 인증 제공자를 지원한다
- Clean Architecture에서 인증/인가 로직은 Domain 레이어의 UseCase에서 처리하고, Serverpod 엔드포인트는 이를 호출한다
- CORS 설정은 Jaspr Web 클라이언트와의 통신을 위해 적절히 구성해야 한다
- 민감한 데이터(비밀번호 해시, 토큰 등)는 로그에 기록하지 않도록 주의한다

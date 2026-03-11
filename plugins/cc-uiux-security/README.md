# cc-uiux-security

Cocode 팀을 위한 보안 플러그인입니다.

## 개요

Serverpod API 보안과 Flutter 앱 보안을 포괄하는 보안 가이드라인을 제공합니다. OWASP 모바일/웹 Top 10 기반의 보안 감사를 지원합니다.

## 스킬 목록

### api-security
- Serverpod 인증/인가 구현
- 입력 검증 및 속도 제한(Rate Limiting)

### app-security
- Flutter 보안 저장소(Secure Storage)
- 인증서 피닝(Certificate Pinning)
- 코드 난독화(Obfuscation)

### security-audit
- OWASP 모바일 Top 10 점검
- OWASP 웹 Top 10 점검
- 의존성 취약점 스캔

## 기술 스택

- **서버**: Serverpod 보안 모듈
- **앱**: Flutter Secure Storage, SSL Pinning
- **감사**: OWASP 표준, Dependency Scanner
- **인증**: Serverpod Auth 모듈

---
name: app-security
description: Flutter 앱 보안 구현
---

# Flutter App Security (Flutter 앱 보안)

## 트리거
- Flutter 앱의 보안을 설계하거나 강화할 때
- 민감 데이터의 안전한 저장이 필요할 때
- 네트워크 통신 보안(Certificate Pinning)을 구현할 때
- 앱 코드 난독화를 설정할 때

## 동작
1. 보안 저장소(Secure Storage)를 구현한다
   - `flutter_secure_storage` 패키지를 활용하여 민감 데이터 저장
   - 인증 토큰, API 키 등의 안전한 저장/조회/삭제
   - iOS Keychain / Android Keystore 활용 확인
2. Certificate Pinning을 설정한다
   - HTTPS 통신 시 서버 인증서 핀 설정
   - Serverpod 클라이언트의 HTTP 클라이언트 커스터마이징
   - 인증서 만료 시 업데이트 전략 수립
3. 코드 난독화를 적용한다
   - `flutter build --obfuscate --split-debug-info` 설정
   - ProGuard/R8 규칙 구성 (Android)
   - 디버그 심볼 보관 및 크래시 리포트 역난독화
4. 앱 무결성을 검증한다
   - 탈옥/루팅 감지
   - 앱 패키지 변조 감지
   - 디버거 연결 감지

## 출력
- Secure Storage 래퍼 클래스 코드
- Certificate Pinning 설정 코드
- 난독화 빌드 스크립트
- 보안 점검 체크리스트 결과

## 참고
- BLoC에서 인증 상태 관리 시 토큰을 State에 직접 포함하지 않고 Secure Storage를 통해 접근한다
- Clean Architecture에서 보안 관련 유틸리티는 Infrastructure 레이어의 Security 모듈에 위치한다
- Serverpod 클라이언트와의 통신은 기본적으로 HTTPS를 사용하며, 추가로 Certificate Pinning을 적용한다
- 릴리스 빌드에서는 반드시 난독화를 활성화하고, `assert`와 `debugPrint`가 제거되었는지 확인한다
- 딥링크/유니버설 링크의 URL 스킴을 검증하여 피싱 공격을 방지한다

---
name: deployment
description: Flutter Web/App + Serverpod 배포 전략
---

# Deployment Strategies (배포 전략)

## 트리거
- Flutter Web/App을 배포할 때
- Serverpod 서버를 스테이징/프로덕션에 배포할 때
- 배포 전략(Blue-Green, Canary 등)을 수립할 때
- 롤백 절차를 준비할 때

## 동작
1. Flutter 앱 배포를 준비한다
   - Android: APK/AAB 빌드 및 Google Play Console 업로드
   - iOS: IPA 빌드 및 App Store Connect 업로드
   - Web: `flutter build web` 후 정적 파일 배포
   - 버전 번호 및 빌드 번호 관리
2. Jaspr Web 배포를 구성한다
   - Jaspr 빌드 및 정적 자산 생성
   - CDN 또는 호스팅 서버에 배포
   - SSR 서버 배포 (필요 시)
3. Serverpod 서버를 배포한다
   - Docker 컨테이너 빌드 및 배포
   - 데이터베이스 마이그레이션 실행
   - 환경 변수 및 시크릿 설정
   - 헬스 체크 엔드포인트 검증
4. 배포 전략을 적용한다
   - Blue-Green 배포: 무중단 전환
   - Canary 배포: 점진적 트래픽 이동
   - 롤백 절차 및 핫픽스 프로세스

## 출력
- 빌드 아티팩트 (APK, IPA, Web 빌드, Docker 이미지)
- 배포 스크립트 및 설정 파일
- 환경별 배포 가이드
- 롤백 절차서

## 참고
- Cocode 프로젝트는 환경(dev, staging, prod)별로 Serverpod 설정 파일(`config/`)을 분리하여 관리한다
- Flutter 앱 배포 시 `--dart-define`으로 환경별 설정을 주입한다
- Serverpod 마이그레이션은 서버 시작 시 자동 실행하거나 별도 스크립트로 수동 실행할 수 있다
- 프로덕션 배포 전 스테이징 환경에서 충분한 검증을 거친다
- 앱 스토어 심사 기간을 고려하여 서버 API의 하위 호환성을 유지한다

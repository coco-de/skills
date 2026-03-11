# CI/CD Pipeline (CI/CD 파이프라인)

## 트리거
- GitHub Actions 워크플로우를 새로 생성하거나 수정할 때
- Flutter 빌드 파이프라인을 구성할 때
- Serverpod 배포 자동화를 설정할 때
- 테스트/린트/코드 품질 게이트를 설정할 때

## 동작
1. GitHub Actions 워크플로우 YAML을 설계한다
   - PR 트리거: 린트, 테스트, 빌드 검증
   - main 브랜치 머지 트리거: 스테이징/프로덕션 배포
2. Flutter 빌드 파이프라인을 구성한다
   - `flutter analyze` 및 `dart format --set-exit-if-changed` 실행
   - 단위/위젯/통합 테스트 실행
   - Web, Android, iOS 빌드 아티팩트 생성
3. Jaspr Web 빌드 파이프라인을 구성한다
   - Jaspr 빌드 및 정적 자산 생성
   - 배포 대상 서버로 전송
4. Serverpod 배포 파이프라인을 구성한다
   - 서버 코드 빌드 및 테스트
   - Docker 이미지 빌드 (필요 시)
   - 마이그레이션 실행 및 서버 배포
5. 시크릿 및 환경 변수를 관리한다

## 출력
- GitHub Actions 워크플로우 YAML 파일 (`.github/workflows/`)
- 빌드/배포 스크립트
- 환경 변수 및 시크릿 설정 가이드
- 파이프라인 실행 결과 알림 설정

## 참고
- Cocode 프로젝트는 모노레포 구조로, Flutter 앱/Jaspr Web/Serverpod 서버가 하나의 저장소에 존재한다
- `serverpod generate`는 CI에서도 실행하여 생성 코드의 최신 상태를 검증한다
- Flutter 빌드 캐시(`pub cache`, 빌드 아티팩트)를 GitHub Actions 캐시로 관리하여 빌드 시간을 단축한다
- 프로덕션 배포 전 스테이징 환경에서 자동 E2E 테스트를 실행한다

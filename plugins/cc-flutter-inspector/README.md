# cc-flutter-inspector

Flutter Inspector 디버깅 플러그인 (Master + 9 전문 Inspectors)

## 구조

### Master Inspector

모든 전문 Inspector를 조율하는 마스터 인스펙터입니다. 문제 유형을 분석하고 적절한 전문 Inspector에게 위임합니다.

### 9 전문 Inspectors

- `auth` - 인증/인가 디버깅
- `bloc` - BLoC 상태 관리 디버깅
- `config` - 설정/환경 디버깅
- `form` - 폼 유효성 검사 디버깅
- `image` - 이미지 로딩/렌더링 디버깅
- `log` - 로그 분석 디버깅
- `nav` - 네비게이션/라우팅 디버깅
- `network` - 네트워크 요청/응답 디버깅
- `ui` - UI 레이아웃/렌더링 디버깅

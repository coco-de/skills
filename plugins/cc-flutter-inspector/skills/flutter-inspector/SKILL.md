---
name: flutter-inspector
description: Flutter 앱 런타임 디버깅 및 상태 검사. 앱 에러, BLoC 상태, 네비게이션, 네트워크 요청, 폼 유효성, 이미지 캐시 등 런타임 문제 해결 시 사용. flutter-inspector MCP 서버를 통해 실행 중인 앱과 직접 통신.
---

# Flutter Inspector

Flutter 앱 런타임 디버깅을 위한 마스터 인스펙터입니다. MCP toolkit을 통해 실행 중인 앱과 직접 통신하여 상태를 검사하고 문제를 진단합니다.

## Scope and Capabilities

### 지원하는 디버깅 영역

| 영역 | 인스펙터 | 주요 기능 |
|------|----------|-----------|
| 네비게이션 | nav | GoRouter 스택, 딥링크, 리다이렉트 |
| 상태 관리 | bloc | BLoC/Cubit 상태 추적, 이벤트 히스토리 |
| 인증 | auth | 토큰 상태, 세션, 자동 로그인 |
| 네트워크 | network | HTTP 요청/응답, 에러, 성능 |
| 로그 | log | 앱 로그 검색, 필터링, 분석 |
| UI | ui | 위젯 트리, 오버플로우, 레이아웃 |
| 설정 | config | 환경 변수, 피처 플래그 |
| 폼 | form | 폼 상태, 유효성 검사 |
| 이미지 | image | 캐시 통계, 메모리 분석 |

### MCP 연결 요구사항

Flutter 앱은 다음 플래그로 실행되어야 합니다:
```bash
flutter run --enable-vm-service \
  --host-vmservice-port=8182 \
  --dds-port=8181 \
  --disable-service-auth-codes
```

## Quick Start

### 1. 앱 연결 확인
```
listClientToolsAndResources
```

### 2. 에러 확인
```
runClientResource resourceUri="visual://localhost/app/errors/latest"
```

### 3. 스크린샷 캡처
```
runClientResource resourceUri="visual://localhost/view/screenshots"
```

## 문제 유형별 진단 플로우

### 앱 크래시
```
1. runClientResource → 에러 로그 확인
2. /inspector/bloc → 마지막 상태 확인
3. /inspector/log → 크래시 직전 로그 추적
```

### 화면 이동 안 됨
```
1. /inspector/nav → 현재 라우트 스택
2. /inspector/auth → 인증 상태 확인 (가드)
3. /inspector/bloc → 네비게이션 관련 BLoC 상태
```

### API 호출 실패
```
1. /inspector/network → 요청/응답 로그
2. /inspector/auth → 토큰 만료 확인
3. /inspector/config → API URL 설정 확인
```

### UI 렌더링 문제
```
1. /inspector/ui → 오버플로우 검사
2. /inspector/bloc → 상태 확인
3. hot_reload_flutter → 변경사항 적용
```

### 폼 제출 실패
```
1. /inspector/form → 폼 상태 확인
2. 유효성 검사 에러 확인
3. 필드 값 검증
```

### 메모리 문제
```
1. /inspector/image → 캐시 사용량 확인
2. 오버사이즈 이미지 식별
3. 캐시 정리 권고
```

## Sub-Inspectors

### /inspector/nav
GoRouter 네비게이션 디버깅
- 현재 라우트 스택 확인
- 딥링크 테스트
- 리다이렉트 추적

### /inspector/bloc
BLoC/Cubit 상태 관리 디버깅
- 등록된 BLoC 목록
- 상태 스냅샷
- 이벤트 히스토리

### /inspector/auth
인증 상태 디버깅
- 토큰 상태 확인
- 세션 정보
- 자동 로그인 상태

### /inspector/network
HTTP 네트워크 디버깅
- 요청/응답 로그
- 에러 필터링
- 성능 통계

### /inspector/log
앱 로그 관리
- 최근 로그 조회
- 레벨별 필터링
- 키워드 검색

### /inspector/ui
위젯 트리 검사
- 트리 구조 분석
- 오버플로우 탐지
- 화면 정보

### /inspector/config
설정 및 피처 플래그
- 환경 설정 조회
- 피처 플래그 상태
- 환경 정보

### /inspector/form
폼 상태 디버깅
- 폼 목록 조회
- 필드 상태 확인
- 유효성 검사 실행

### /inspector/image
이미지 캐시 분석
- 캐시 통계
- 메모리 사용량
- 오버사이즈 경고

## Hot Reload Workflow

```
1. 코드 수정
2. hot_reload_flutter → UI 즉시 반영
3. /inspector/* → 상태 변화 확인
4. 반복
```

## Additional Resources

- [REFERENCE.md](REFERENCE.md) - MCP 도구 상세 API 및 트러블슈팅
- [TEMPLATES.md](TEMPLATES.md) - 커스텀 인스펙터 도구 등록 템플릿

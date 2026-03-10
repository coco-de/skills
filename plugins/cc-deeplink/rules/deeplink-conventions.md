---
name: deeplink-conventions
description: 딥링크 설정 컨벤션 및 보안 규칙
globs: ["**/.well-known/*", "**/well_known_route*", "**/AndroidManifest.xml", "**/*.entitlements", "**/deep_link*", "**/deeplink*", "**/env_config*", "**/invite_link*", "**/coupon_link*"]
---

# 딥링크 컨벤션

## AASA (iOS Universal Links)

### 필수 규칙

- AASA는 `/.well-known/apple-app-site-association`에서 서빙
- Content-Type: `application/json` 필수
- HTTPS 직접 서빙 (리다이렉트 금지)
- 서버 전용 경로는 반드시 `NOT` prefix로 제외

### 제외 대상 경로

```json
"paths": [
  "NOT /auth/*",
  "NOT /internal/*",
  "NOT /api/*",
  "*"
]
```

| 경로 | 이유 |
|------|------|
| `/auth/*` | OAuth 콜백 (서버 토큰 교환 필요) |
| `/internal/*` | 서버 간 내부 통신 |
| `/api/*` | REST API 엔드포인트 |

### 새 서버 경로 추가 시

앱이 아닌 서버에서 처리해야 하는 새 경로를 추가할 때:
1. 동적 AASA (`well_known_route.dart`)에 NOT 규칙 추가
2. 정적 AASA 폴백 파일에도 동일하게 추가
3. 두 파일의 paths가 항상 동기화되어야 함

## assetlinks.json (Android App Links)

### 필수 규칙

- `/.well-known/assetlinks.json`에서 서빙
- 릴리즈 + 디버그 SHA-256 지문 모두 포함
- 경로 제어는 `AndroidManifest.xml`에서 (assetlinks.json 아님)

### 경로 제외 불필요

Android는 `intent-filter`에 포함할 경로만 명시하므로, 서버 콜백 경로는 자동으로 제외됩니다.

## 동적 + 정적 동기화

| 파일 | 용도 | 수정 시 |
|------|------|--------|
| `well_known_route.dart` | 동적 AASA (환경별 Bundle ID) | 서버 코드 수정 |
| `web/.well-known/apple-app-site-association` | 정적 폴백 | 파일 수정 |

**두 파일의 paths 설정은 반드시 동일해야 합니다.**

## URL 생성 규칙

### 중앙 설정 사용 (필수)

딥링크 URL 생성 시 **반드시** 중앙 설정(`EnvConfig.deeplinkBaseUrl`)을 사용합니다.

```dart
// ✅ CORRECT: 중앙 설정 사용
final url = '${EnvConfig.deeplinkBaseUrl}/store/book/$bookId';

// ❌ WRONG: 도메인 직접 조합
final url = 'https://$scheme.$domain/store/book/$bookId';

// ❌ WRONG: 하드코딩 도메인
final url = 'https://unibook.laputa.im/store/book/$bookId';
```

### 도메인 추출

```dart
// ✅ CORRECT: URI 파싱으로 도메인 추출
final domain = Uri.parse(EnvConfig.deeplinkBaseUrl).host;

// ❌ WRONG: 문자열 조합 (구분자 누락 위험)
final domain = '${EnvConfig.deepLinkScheme}${EnvConfig.domain}';
```

## 도메인 마이그레이션 규칙

### 하위 호환 필수

도메인 변경 시 기존 도메인을 즉시 제거하지 않습니다.

| 설정 | 새 도메인 | 기존 도메인 |
|------|----------|-----------|
| iOS entitlements | 추가 | **유지** |
| Android intent-filter | 추가 | **유지** |
| URL 생성 코드 | 새 도메인 사용 | - |

### 전수 조사 대상

도메인 변경 시 아래 영역을 모두 검색합니다:

- 공유 링크 생성 (채팅 초대, 도서 공유)
- 쿠폰/프로모션 딥링크
- 관리자 콘솔 URL 생성
- 푸시 알림 페이로드
- 테스트 코드 assertion
- 주석/문서의 예시 URL

## 보안 규칙

- AASA/assetlinks.json에 내부 전용 경로 노출 금지
- SHA-256 지문은 릴리즈 키만 포함 (디버그 키는 개발 환경 전용)
- 프로덕션 AASA에 개발 Bundle ID 포함 금지

---
name: deeplink-conventions
description: 딥링크 설정 컨벤션 및 보안 규칙
globs: ["**/.well-known/*", "**/well_known_route*", "**/AndroidManifest.xml", "**/*.entitlements"]
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

## 보안 규칙

- AASA/assetlinks.json에 내부 전용 경로 노출 금지
- SHA-256 지문은 릴리즈 키만 포함 (디버그 키는 개발 환경 전용)
- 프로덕션 AASA에 개발 Bundle ID 포함 금지

# cc-deeplink

Deep Link, Universal Links, App Links 설정 및 관리 플러그인

> iOS Universal Links (AASA), Android App Links (assetlinks.json), GoRouter 딥링크 연동을 다룹니다.

## Skills

| 스킬 | 설명 |
|------|------|
| `universal-links` | iOS Universal Links 설정 (AASA, Entitlements, Xcode) |
| `app-links` | Android App Links 설정 (assetlinks.json, AndroidManifest, intent-filter) |
| `aasa-management` | AASA 동적/정적 서빙 및 경로 제어 (NOT prefix, 서버 콜백 제외) |

## Rules

| 규칙 | 설명 |
|------|------|
| `deeplink-conventions` | 딥링크 설정 컨벤션 및 보안 규칙 |

## 주요 사용 사례

- Universal Links / App Links 초기 설정
- AASA paths에서 서버 전용 경로 제외 (OAuth 콜백 등)
- 신규 딥링크 경로 추가
- 딥링크 디버깅 및 검증

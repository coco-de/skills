# iOS Universal Links 설정

Apple Universal Links를 설정하여 웹 URL을 앱에서 직접 열 수 있도록 합니다.

## 트리거

- Universal Links 초기 설정
- 새로운 앱 번들 ID 추가
- Associated Domains 설정
- AASA 파일 생성/수정

## AASA (Apple App Site Association) 구조

### 기본 구조

```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "{TEAM_ID}.{BUNDLE_ID}",
        "paths": ["*"]
      }
    ]
  },
  "webcredentials": {
    "apps": [
      "{TEAM_ID}.{BUNDLE_ID}"
    ]
  }
}
```

### 다중 앱 지원

```json
{
  "applinks": {
    "details": [
      {
        "appID": "TEAM_ID.com.example.app",
        "paths": ["NOT /auth/*", "NOT /api/*", "*"]
      },
      {
        "appID": "TEAM_ID.com.example.console",
        "paths": ["NOT /auth/*", "NOT /api/*", "*"]
      }
    ]
  }
}
```

### paths 규칙

| 패턴 | 설명 | 예시 |
|------|------|------|
| `*` | 모든 경로 매칭 | 모든 URL을 앱으로 |
| `/path/*` | 특정 경로 하위 매칭 | `/books/*` |
| `NOT /path/*` | 특정 경로 제외 | `NOT /auth/*` |
| `?` | 단일 문자 와일드카드 | `/book/?` |

**평가 순서**: NOT 규칙이 먼저 평가되고, 이후 매칭 규칙이 적용됩니다.

## Xcode 설정

### Associated Domains Capability

1. Xcode → Target → Signing & Capabilities
2. "+ Capability" → "Associated Domains"
3. 도메인 추가:

```
applinks:yourdomain.com
webcredentials:yourdomain.com
```

### Entitlements 파일

```xml
<!-- Runner.entitlements -->
<key>com.apple.developer.associated-domains</key>
<array>
  <string>applinks:yourdomain.com</string>
  <string>webcredentials:yourdomain.com</string>
</array>
```

## Flutter 연동 (GoRouter)

```dart
GoRouter(
  routes: [...],
  // Universal Links는 GoRouter가 자동 처리
  // initialLocation, redirect 등에서 딥링크 경로 처리
)
```

## 검증

```bash
# AASA 파일 확인
curl -s https://yourdomain.com/.well-known/apple-app-site-association | jq .

# Apple CDN 캐시 확인 (Apple이 AASA를 캐시함)
curl -s https://app-site-association.cdn-apple.com/a/v1/yourdomain.com | jq .
```

### 디버깅

- iOS Settings → Developer → Associated Domains → Diagnostics
- Xcode Console에서 `swcd` 프로세스 로그 확인
- Apple CDN은 24시간 캐시 → 변경 후 즉시 반영 안 될 수 있음

## 체크리스트

- [ ] AASA 파일이 `/.well-known/apple-app-site-association`에서 서빙됨
- [ ] Content-Type: `application/json`
- [ ] HTTPS 필수 (리다이렉트 없이 직접 서빙)
- [ ] Team ID + Bundle ID 정확히 설정
- [ ] Xcode Associated Domains 추가
- [ ] 서버 전용 경로 NOT prefix로 제외 (OAuth 콜백 등)

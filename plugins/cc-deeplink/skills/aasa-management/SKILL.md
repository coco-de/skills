# AASA 동적/정적 서빙 및 경로 제어

서버에서 AASA(Apple App Site Association)를 동적으로 생성하고, 특정 경로를 Universal Links에서 제외하는 방법을 다룹니다.

## 트리거

- AASA에서 특정 경로 제외 (OAuth 콜백 등)
- 동적 AASA 서빙 설정
- 멀티 도메인/앱 AASA 관리
- Universal Links 디버깅

## 경로 제외 패턴

### 문제 상황

OAuth 로그인(네이버, 카카오 등) 시 서버 콜백 URL(`/auth/naver/callback`)이 AASA `"paths": ["*"]` 설정에 의해 iOS Universal Links로 매칭되면, **서버가 토큰 교환을 완료하기 전에 앱이 열립니다**.

```
1. 사용자 → 네이버 로그인 페이지
2. 네이버 → 서버 /auth/naver/callback (토큰 교환 필요)
3. ❌ iOS가 /auth/naver/callback을 앱으로 리다이렉트
4. 서버 토큰 교환 미완료 → 로그인 실패
```

### 해결: NOT prefix

```json
{
  "applinks": {
    "details": [
      {
        "appID": "TEAM_ID.BUNDLE_ID",
        "paths": [
          "NOT /auth/*",
          "NOT /internal/*",
          "NOT /api/*",
          "*"
        ]
      }
    ]
  }
}
```

### 제외 대상 경로

| 경로 | 이유 |
|------|------|
| `/auth/*` | OAuth 콜백 (네이버, 카카오, Google 등) |
| `/internal/*` | 서버 간 통신 (Lambda 콜백, 웹훅 등) |
| `/api/*` | REST API 엔드포인트 |
| `/webhooks/*` | 외부 서비스 웹훅 (결제, 알림 등) |
| `/health` | 헬스체크 엔드포인트 |

### 평가 순서

Apple AASA paths 평가 규칙:
1. **NOT 규칙이 먼저 평가** → 매칭되면 Universal Link에서 제외
2. **포함 규칙 평가** → `*`, `/books/*` 등
3. 첫 번째 매칭 규칙이 적용됨

## 동적 AASA 서빙 (Serverpod)

### WellKnownRoute 패턴

```dart
class WellKnownRoute extends Route {
  Map<String, dynamic> _appleAppSiteAssociation() {
    return {
      'applinks': {
        'apps': <String>[],
        'details': [
          {
            'appID': '\${EnvConfig.appleTeamId}.\${EnvConfig.packageName}',
            'paths': [
              'NOT /auth/*',
              'NOT /internal/*',
              'NOT /api/*',
              '*',
            ],
          },
        ],
      },
      'webcredentials': {
        'apps': [
          '\${EnvConfig.appleTeamId}.\${EnvConfig.packageName}',
        ],
      },
    };
  }

  @override
  FutureOr<Result> handleCall(Session session, Request request) {
    if (request.url.path == '/.well-known/apple-app-site-association') {
      final body = jsonEncode(_appleAppSiteAssociation());
      return Response.ok(
        body: Body.fromString(body, mimeType: .json),
        headers: Headers.build((headers) {
          headers[HttpHeaders.cacheControlHeader] = ['max-age=31536000'];
        }),
      );
    }
    return Response.notFound();
  }
}
```

### 동적 vs 정적 AASA

| 방식 | 장점 | 단점 |
|------|------|------|
| **동적** (서버 코드) | 환경별 Bundle ID 자동 적용, 코드 관리 | 서버 의존 |
| **정적** (파일) | 서버 다운 시에도 서빙 가능 | 환경별 수동 관리 |

**권장**: 동적 AASA를 기본으로 사용하고, 정적 파일을 폴백으로 유지합니다.

### 정적 AASA 폴백

```
web/.well-known/apple-app-site-association
```

모든 환경(dev/stg/prod)의 Bundle ID를 포함:

```json
{
  "applinks": {
    "details": [
      {
        "appIDs": [
          "TEAM_ID.com.example.app.dev",
          "TEAM_ID.com.example.app.stg",
          "TEAM_ID.com.example.app"
        ],
        "paths": [
          "NOT /auth/*",
          "NOT /internal/*",
          "NOT /api/*",
          "*"
        ]
      }
    ]
  }
}
```

## Android assetlinks.json과의 차이

| 항목 | iOS AASA | Android assetlinks.json |
|------|----------|------------------------|
| 경로 제어 위치 | **서버** (AASA paths) | **앱** (AndroidManifest intent-filter) |
| 제외 방법 | `NOT /path/*` | intent-filter에 포함 경로만 지정 |
| 설정 변경 | 서버 배포 필요 | 앱 업데이트 필요 |

→ **Android에서는 assetlinks.json 수정 불필요** (도메인 수준 검증만 담당)

## 검증

```bash
# 동적 AASA 확인
curl -s https://yourdomain.com/.well-known/apple-app-site-association | jq .

# NOT 규칙 동작 확인: /auth/ 경로가 앱으로 열리지 않아야 함
# iOS Safari에서 https://yourdomain.com/auth/naver/callback 접근
# → 앱이 열리지 않고 웹에서 처리되어야 정상

# Apple CDN 캐시 확인 (최대 24시간 지연)
curl -s https://app-site-association.cdn-apple.com/a/v1/yourdomain.com | jq .
```

## 트러블슈팅

### Universal Links가 동작하지 않을 때

1. AASA Content-Type이 `application/json`인지 확인
2. HTTPS 리다이렉트 없이 직접 서빙되는지 확인
3. Apple CDN 캐시 (24시간) 대기
4. iOS 설정 → Developer → Associated Domains 진단

### OAuth 콜백이 앱으로 열릴 때

1. AASA paths에 `NOT /auth/*` 추가
2. 서버 재배포
3. Apple CDN 캐시 갱신 대기 (또는 앱 재설치)
4. Safari에서 콜백 URL 직접 접근하여 웹에서 처리되는지 확인

## 체크리스트

- [ ] 서버 전용 경로에 NOT prefix 적용
- [ ] 동적 AASA와 정적 AASA 폴백 모두 동일한 paths 설정
- [ ] 새 OAuth 프로바이더 추가 시 `/auth/*` 패턴으로 자동 커버 확인
- [ ] 배포 후 `curl`로 AASA 응답 검증
- [ ] Apple CDN 캐시 갱신 후 iOS 기기에서 테스트

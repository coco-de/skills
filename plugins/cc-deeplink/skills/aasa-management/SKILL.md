---
name: aasa-management
description: AASA 동적/정적 서빙 및 경로 제어
---

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

## Firebase Hosting AASA 가로채기

### 문제: Firebase Hosting이 AASA를 자동 생성

Firebase Hosting을 리버스 프록시/CDN으로 사용하는 경우, `.well-known/apple-app-site-association` 요청이 **백엔드 서버에 도달하지 않습니다**.

```
iOS 기기 → DNS → Firebase Hosting CDN → 백엔드 서버 (Serverpod 등)
                       ↑
                 여기서 AASA 가로챔
```

Firebase는 프로젝트에 iOS 앱이 등록되어 있으면 **자동으로 AASA를 생성**하여 반환합니다. 이 자동 생성 AASA에는 Firebase 내부 경로(`/__/auth/*`, `/_/*`)만 NOT prefix로 제외되고, 커스텀 NOT 규칙(예: `NOT /auth/*`)은 **포함되지 않습니다**.

### 결과

- 백엔드 서버의 `WellKnownRoute`가 아무리 올바르게 설정되어 있어도, Firebase가 먼저 응답
- OAuth 콜백(`/auth/naver/callback` 등)이 Universal Link로 매칭되어 앱이 열림
- 서버 토큰 교환 미완료 → 로그인 실패

### 해결: 커스텀 정적 AASA 파일 배포

Firebase Hosting의 `public` 디렉토리에 정적 AASA 파일을 배포하면, Firebase 자동 생성 AASA보다 **높은 우선순위**로 서빙됩니다.

```
우선순위:
1순위: public 디렉토리의 정적 파일 ← 커스텀 AASA
2순위: Firebase 자동 생성 AASA
3순위: rewrites 규칙 (백엔드 프록시)
```

#### 1단계: 정적 AASA 파일 생성

```
web/.well-known/apple-app-site-association
```

```json
{
  "applinks": {
    "apps": [],
    "details": [
      {
        "appID": "TEAM_ID.BUNDLE_ID",
        "paths": [
          "NOT /auth/*",
          "NOT /internal/*",
          "NOT /api/*",
          "NOT /__/auth/action/",
          "NOT /__/auth/handler/",
          "NOT /_/*",
          "/*"
        ]
      }
    ]
  }
}
```

> **중요**: Firebase 기본 NOT 규칙(`/__/auth/*`, `/_/*`)도 함께 포함해야 합니다.

#### 2단계: firebase.json 설정

```json
{
  "hosting": {
    "public": "build/web",
    "ignore": ["firebase.json", "**/node_modules/**"],
    "headers": [
      {
        "source": "/.well-known/apple-app-site-association",
        "headers": [
          { "key": "Content-Type", "value": "application/json" }
        ]
      }
    ]
  }
}
```

**주의사항**:
- `ignore` 배열에서 `"**/.*"` 제거 필수 (`.well-known` 디렉토리가 무시되지 않도록)
- Content-Type 헤더 명시 (Firebase가 자동 감지하지 못할 수 있음)

#### 3단계: 빌드 스크립트에서 .well-known 복사

`flutter build web` 후 `.well-known` 디렉토리가 빌드 출력에 포함되지 않으므로, 수동 복사가 필요합니다.

```bash
# deploy_web.sh 또는 CI 스크립트
flutter build web --release

# .well-known 디렉토리 복사
if [ -d "web/.well-known" ]; then
  cp -r "web/.well-known" "build/web/.well-known"
fi

# Firebase 배포
firebase deploy --only hosting
```

#### 4단계: 배포 후 검증

```bash
# Firebase Hosting이 커스텀 AASA를 서빙하는지 확인
curl -s https://yourdomain.com/.well-known/apple-app-site-association | jq .

# NOT /auth/* 규칙 포함 여부 확인
curl -s https://yourdomain.com/.well-known/apple-app-site-association | jq '.applinks.details[0].paths'
```

### 동적 AASA와 정적 AASA 동기화

Firebase Hosting 환경에서는 **두 곳의 AASA가 모두 동기화**되어야 합니다:

| 파일 | 서빙 도메인 | 용도 |
|------|-----------|------|
| `web/.well-known/apple-app-site-association` | Firebase Hosting 도메인 (예: `www.example.com`) | Firebase가 가로채는 AASA 대체 |
| `well_known_route.dart` (동적) | 백엔드 직접 접근 도메인 (예: `api.example.com`) | 백엔드 서버가 직접 서빙 |

**두 파일의 `paths` 설정은 반드시 동일해야 합니다.**

## 트러블슈팅

### Universal Links가 동작하지 않을 때

1. AASA Content-Type이 `application/json`인지 확인
2. HTTPS 리다이렉트 없이 직접 서빙되는지 확인
3. Apple CDN 캐시 (24시간) 대기
4. iOS 설정 → Developer → Associated Domains 진단

### OAuth 콜백이 앱으로 열릴 때

1. AASA paths에 `NOT /auth/*` 추가
2. **Firebase Hosting 사용 시**: 커스텀 정적 AASA 파일 배포 (서버 배포만으로는 부족)
3. 서버 재배포 + Firebase Hosting 재배포
4. Apple CDN 캐시 갱신 대기 (또는 앱 재설치)
5. Safari에서 콜백 URL 직접 접근하여 웹에서 처리되는지 확인

### Firebase Hosting 배포 후에도 AASA가 안 바뀔 때

1. `firebase.json`의 `ignore`에서 `"**/.*"` 제거했는지 확인
2. 빌드 스크립트에서 `web/.well-known` → `build/web/.well-known` 복사 확인
3. Firebase CDN 캐시 (15분) 대기
4. `curl -H "Cache-Control: no-cache"` 로 캐시 우회 확인

## 체크리스트

- [ ] 서버 전용 경로에 NOT prefix 적용
- [ ] 동적 AASA와 정적 AASA 폴백 모두 동일한 paths 설정
- [ ] 새 OAuth 프로바이더 추가 시 `/auth/*` 패턴으로 자동 커버 확인
- [ ] **Firebase Hosting 사용 시**: 커스텀 정적 AASA 파일 배포
- [ ] **Firebase Hosting 사용 시**: `firebase.json`에서 `**/.*` ignore 제거
- [ ] **Firebase Hosting 사용 시**: 빌드 스크립트에 `.well-known` 복사 추가
- [ ] 배포 후 `curl`로 AASA 응답 검증
- [ ] Apple CDN 캐시 갱신 후 iOS 기기에서 테스트

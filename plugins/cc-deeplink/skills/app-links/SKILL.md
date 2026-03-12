---
name: app-links
description: Android App Links (assetlinks.json) 설정
---

# Android App Links 설정

Android App Links를 설정하여 웹 URL을 앱에서 직접 열 수 있도록 합니다.

## 트리거

- App Links 초기 설정
- 새로운 패키지명 추가
- SHA-256 인증서 지문 업데이트
- intent-filter 설정

## assetlinks.json 구조

### 기본 구조

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.example.app",
      "sha256_cert_fingerprints": [
        "AA:BB:CC:..."
      ]
    }
  }
]
```

### 다중 앱 지원

```json
[
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.example.app",
      "sha256_cert_fingerprints": ["AA:BB:CC:..."]
    }
  },
  {
    "relation": ["delegate_permission/common.handle_all_urls"],
    "target": {
      "namespace": "android_app",
      "package_name": "com.example.console",
      "sha256_cert_fingerprints": ["AA:BB:CC:..."]
    }
  }
]
```

## iOS와의 차이점

| 항목 | iOS (Universal Links) | Android (App Links) |
|------|----------------------|---------------------|
| 설정 파일 | `apple-app-site-association` | `assetlinks.json` |
| 경로 제어 | AASA `paths` 필드 | `AndroidManifest.xml` intent-filter |
| 서버 역할 | 도메인 + 경로 매칭 | **도메인 검증만** |
| 경로 필터링 | 서버(AASA)에서 제어 | 앱(Manifest)에서 제어 |

**핵심 차이**: Android는 `assetlinks.json`의 `handle_all_urls`가 도메인 수준 검증만 담당합니다.
경로 필터링은 `AndroidManifest.xml`의 `intent-filter`에서 제어합니다.

## AndroidManifest.xml 설정

```xml
<activity android:name=".MainActivity">
  <!-- App Links (verified) -->
  <intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https"
          android:host="yourdomain.com"
          android:pathPattern="/books/.*" />
  </intent-filter>
</activity>
```

### 특정 경로만 앱으로 열기

```xml
<!-- 도서 상세만 앱으로 -->
<data android:pathPattern="/books/.*" />

<!-- 프로필 페이지만 앱으로 -->
<data android:pathPrefix="/profile" />
```

### 서버 콜백 경로 제외

Android는 intent-filter에 **포함할 경로만 지정**하므로, `/auth/*` 같은 서버 콜백은 자동으로 제외됩니다.

### 멀티 도메인 지원 (마이그레이션 시)

도메인 변경 시 **기존 intent-filter를 유지**하고 새 도메인용 intent-filter를 추가합니다.

```xml
<!-- 새 도메인 -->
<intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="@string/www_host" />
</intent-filter>

<!-- 기존 도메인 (하위 호환) -->
<intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="https" android:host="@string/old_host" />
</intent-filter>
```

**Flavor별 strings.xml**에서 호스트명을 관리합니다:

```xml
<!-- values/strings.xml (production) -->
<string name="www_host">www.example.com</string>

<!-- values-staging/strings.xml -->
<string name="www_host">stg.example.com</string>
```

> `assetlinks.json`은 도메인 독립적이므로 수정 불필요. 단, 새 도메인에서도 서빙되어야 합니다.

## SHA-256 인증서 지문 확인

```bash
# 디버그 키
keytool -list -v -keystore ~/.android/debug.keystore -alias androiddebugkey -storepass android

# 릴리즈 키
keytool -list -v -keystore release.keystore -alias release_alias

# Google Play Console에서 확인
# Setup → App signing → SHA-256 certificate fingerprint
```

## 검증

```bash
# assetlinks.json 확인
curl -s https://yourdomain.com/.well-known/assetlinks.json | jq .

# Google 검증 도구
# https://developers.google.com/digital-asset-links/tools/generator
```

### adb 디버깅

```bash
# App Links 상태 확인
adb shell pm get-app-links com.example.app

# 딥링크 테스트
adb shell am start -a android.intent.action.VIEW \
  -d "https://yourdomain.com/books/123" com.example.app
```

## 체크리스트

- [ ] `assetlinks.json`이 `/.well-known/assetlinks.json`에서 서빙됨
- [ ] Content-Type: `application/json`
- [ ] HTTPS 필수
- [ ] 릴리즈 + 디버그 SHA-256 지문 모두 포함
- [ ] `AndroidManifest.xml`에 `android:autoVerify="true"` 설정
- [ ] intent-filter에 필요한 경로만 포함 (서버 콜백 자동 제외)
- [ ] 멀티 도메인 시: 새 도메인 intent-filter 추가 + 기존 유지
- [ ] 멀티 도메인 시: 모든 flavor의 strings.xml에 호스트 추가
- [ ] 멀티 도메인 시: 새 도메인에서 assetlinks.json 서빙 확인

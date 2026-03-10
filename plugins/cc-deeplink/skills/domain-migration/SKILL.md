# 딥링크 도메인 마이그레이션

딥링크/유니버셜 링크 도메인을 변경할 때 필요한 전체 작업 범위와 하위 호환 전략을 다룹니다.

## 트리거

- 딥링크 도메인 변경 (예: `old.example.com` → `www.example.com`)
- 멀티 도메인 지원 추가
- 레거시 하드코딩 도메인 제거
- URL 생성 로직 중앙화

## 마이그레이션 체크리스트

도메인 마이그레이션 시 변경이 필요한 영역 전체 목록입니다.

### 1. 중앙 설정 변경

딥링크 베이스 URL을 환경 설정에서 **한 곳에서만** 관리합니다.

```dart
// env_config.dart - 환경별 딥링크 베이스 URL
static String get deeplinkBaseUrl => switch (Flavor.flavor) {
  .DEVELOPMENT || null => webBaseUrl,
  .STAGING => 'https://stg.example.com',
  .PRODUCTION => 'https://www.example.com',  // 새 도메인
};
```

**핵심 원칙**: 모든 URL 생성은 `EnvConfig.deeplinkBaseUrl`을 사용합니다. 하드코딩 도메인을 직접 조합하지 않습니다.

### 2. iOS 설정 (Universal Links)

#### Entitlements 파일

새 도메인을 추가하되, **기존 도메인을 제거하지 않습니다** (하위 호환).

```xml
<!-- Runner.entitlements -->
<key>com.apple.developer.associated-domains</key>
<array>
  <!-- 새 도메인 (우선) -->
  <string>applinks:www.example.com</string>
  <string>webcredentials:www.example.com</string>
  <string>applinks:example.com</string>
  <string>webcredentials:example.com</string>
  <!-- 기존 도메인 (하위 호환) -->
  <string>applinks:old.example.com</string>
  <string>webcredentials:old.example.com</string>
</array>
```

> **모든 앱 타겟**에 동일하게 적용 (메인 앱, 콘솔 앱 등)

#### AASA 서빙

새 도메인(`www.example.com`)에서도 `.well-known/apple-app-site-association`이 서빙되어야 합니다.

- 기존 서버가 새 도메인을 서빙한다면 추가 작업 불필요
- DNS/CDN 설정이 다르다면 새 도메인에서도 AASA 접근 가능하도록 설정

### 3. Android 설정 (App Links)

#### AndroidManifest.xml

새 도메인용 intent-filter를 **추가**합니다. 기존 intent-filter는 유지합니다.

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

#### strings.xml (Flavor별)

```xml
<!-- values/strings.xml (production) -->
<string name="www_host">www.example.com</string>

<!-- values-staging/strings.xml -->
<string name="www_host">stg.example.com</string>

<!-- values-development/strings.xml -->
<string name="www_host">dev.example.com</string>
```

#### assetlinks.json

`assetlinks.json`은 **도메인 독립적**(domain-agnostic)입니다. 패키지명과 SHA-256 지문만 포함하므로 도메인 변경 시 수정 불필요. 단, 새 도메인에서도 서빙되어야 합니다.

### 4. 앱 내 도메인 추출 로직

도메인을 직접 조합하지 말고, 중앙 설정에서 파싱합니다.

```dart
// ❌ WRONG: 도메인을 직접 조합
static String getCurrentDomain() {
  final scheme = EnvConfig.deepLinkScheme;
  final domain = EnvConfig.domain;
  return '$scheme.$domain';
}

// ✅ CORRECT: deeplinkBaseUrl에서 파싱
static String getCurrentDomain() {
  final uri = Uri.parse(EnvConfig.deeplinkBaseUrl);
  return uri.host;
}
```

### 5. 하위 호환 도메인 목록

앱이 수신할 수 있는 모든 도메인을 지원합니다.

```dart
static List<String> supportedDomains() => [
  getCurrentDomain(),              // 새 도메인 (www.example.com)
  '${EnvConfig.scheme}.old.com',   // 기존 도메인 (하위 호환)
  'example.com',                   // naked 도메인
  'localhost',                     // 로컬 개발
  '127.0.0.1',                     // 로컬 개발
];
```

### 6. URL 생성 코드 전수 조사

프로젝트 전체에서 딥링크 URL을 생성하는 코드를 검색합니다.

```bash
# 하드코딩 도메인 검색
grep -r "old\.example\.com" --include="*.dart" --include="*.xml" --include="*.json"

# 레거시 도메인 패턴 검색
grep -r "laputa\.im\|legacy\.domain" --include="*.dart"

# URL 조합 패턴 검색 (scheme + domain 조합)
grep -r "deepLinkScheme.*domain\|scheme.*\.domain" --include="*.dart"
```

**주요 검색 대상:**

| 영역 | 검색 키워드 | 예시 |
|------|-----------|------|
| 공유 링크 생성 | `share`, `invite`, `link` | 채팅 초대, 도서 공유 |
| 쿠폰 딥링크 | `coupon`, `couponCode` | 쿠폰 구매 링크 |
| 관리자 콘솔 | `console`, `admin`, `webBaseUrl` | 도서 등록, 견본 도서 |
| 알림 링크 | `notification`, `push`, `payload` | 푸시 알림 딥링크 |
| 테스트 코드 | `test`, `expect` | URL assertion |
| 주석/문서 | `//`, `///`, `README` | 예시 URL |

### 7. 인프라 확인

| 확인 항목 | 설명 |
|----------|------|
| DNS | 새 도메인이 올바른 서버를 가리키는지 |
| HTTPS 인증서 | 새 도메인의 SSL 인증서 유효한지 |
| `.well-known` 서빙 | 새 도메인에서 AASA/assetlinks.json 접근 가능한지 |
| CDN/Proxy | 리버스 프록시가 `.well-known` 경로를 올바르게 전달하는지 |
| Firebase Hosting | 정적 사이트가 새 도메인에서 서빙되는지 |

```bash
# 새 도메인에서 .well-known 파일 접근 확인
curl -sI https://www.example.com/.well-known/apple-app-site-association
curl -sI https://www.example.com/.well-known/assetlinks.json

# Apple CDN 캐시 확인
curl -s https://app-site-association.cdn-apple.com/a/v1/www.example.com | jq .
```

## 일반적인 실수

### 도메인 조합 시 구분자 누락

```dart
// ❌ BUG: 점(.) 누락 → "unibookunibook.co.kr"
final domain = '${EnvConfig.deepLinkScheme}${EnvConfig.domain}';

// ✅ CORRECT: deeplinkBaseUrl 사용
final domain = Uri.parse(EnvConfig.deeplinkBaseUrl).host;
```

### 레거시 도메인 하드코딩 방치

```dart
// ❌ 레거시 코드가 다른 파일에 남아있는 경우
final url = 'https://$scheme.laputa.im/store/book/$bookId';

// ✅ 중앙 설정 사용
final url = '${EnvConfig.deeplinkBaseUrl}/store/book/$bookId';
```

### 테스트/주석에서 URL 미갱신

테스트 assertion과 주석의 예시 URL도 함께 업데이트해야 합니다.

```dart
// ❌ 테스트에서 옛 도메인 사용
expect(url, 'https://old.example.com/store/book/123');

// ✅ 새 도메인으로 업데이트
expect(url, 'https://www.example.com/store/book/123');
```

## 마이그레이션 순서

```
1. 중앙 설정(EnvConfig) 변경
2. iOS entitlements에 새 도메인 추가
3. Android intent-filter + strings.xml 추가
4. 앱 내 도메인 추출 로직 수정
5. URL 생성 코드 전수 조사 및 수정
6. 테스트/주석 URL 업데이트
7. 인프라 확인 (.well-known 서빙)
8. 배포 후 검증 (iOS Safari, Android adb)
```

## 롤백 전략

문제 발생 시 기존 도메인으로 빠르게 복구할 수 있습니다.

1. `EnvConfig.deeplinkBaseUrl`만 이전 값으로 복원
2. iOS/Android 네이티브 설정은 **그대로 유지** (양쪽 도메인 모두 지원하므로)
3. 핫픽스 배포

## 체크리스트

- [ ] `EnvConfig.deeplinkBaseUrl` 변경
- [ ] iOS `Runner.entitlements`에 새 도메인 추가 (모든 앱 타겟)
- [ ] Android `AndroidManifest.xml`에 새 intent-filter 추가
- [ ] Android `strings.xml` (dev/stg/prod) 새 호스트 추가
- [ ] 앱 내 도메인 추출을 `Uri.parse(deeplinkBaseUrl).host` 방식으로 통일
- [ ] URL 생성 코드 전수 조사 (하드코딩, 레거시 도메인)
- [ ] 테스트 코드의 URL assertion 업데이트
- [ ] 주석/문서의 예시 URL 업데이트
- [ ] 기존 도메인 하위 호환 유지 (entitlements, intent-filter에 보존)
- [ ] 새 도메인에서 `.well-known` 파일 서빙 확인
- [ ] Apple CDN 캐시 갱신 확인
- [ ] 실기기에서 Universal Links / App Links 동작 검증

# HTTP 로깅 규칙

HTTP 요청/응답 로깅을 위한 TalkerDioLogger 설정 및 보안 가이드입니다.

## HttpModule 인터셉터 순서

`package/openapi_service/lib/src/http/http_module.dart`의 인터셉터 체인:

| 순서 | 인터셉터 | 역할 |
|------|----------|------|
| 1 | DioCacheInterceptor | 응답 캐싱 (HiveStore/MemStore) |
| 2 | Setting interceptors | 커스텀 설정 인터셉터 |
| 3 | AuthInterceptor | 인증 토큰 주입 |
| 4 | RateLimitInterceptor | 요청 속도 제한 |
| 5 | **TalkerDioLogger** | HTTP 로깅 (디버그 모드만) |
| 6 | RetryInterceptor | 실패 시 재시도 |

## TalkerDioLogger 설정

### 기본 설정

```dart
import 'package:flutter/foundation.dart' show kDebugMode;
import 'package:talker_dio_logger/talker_dio_logger.dart';

// 디버그 모드에서만 활성화
if (kDebugMode) {
  dio.interceptors.add(
    TalkerDioLogger(
      settings: const TalkerDioLoggerSettings(
        printRequestHeaders: true,
        printResponseHeaders: true,
      ),
    ),
  );
}
```

### 설정 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `printRequestHeaders` | false | 요청 헤더 출력 |
| `printResponseHeaders` | false | 응답 헤더 출력 |
| `printResponseMessage` | true | 응답 메시지 출력 |
| `printRequestData` | true | 요청 바디 출력 |
| `printResponseData` | true | 응답 바디 출력 |

### 확장 설정 (필요 시)

```dart
TalkerDioLogger(
  settings: TalkerDioLoggerSettings(
    printRequestHeaders: true,
    printResponseHeaders: true,
    // 에러만 출력
    printErrorData: true,
    printErrorHeaders: true,
    printErrorMessage: true,
    // 요청/응답 데이터 필터링
    requestFilter: (options) => !options.path.contains('/health'),
    responseFilter: (response) => response.statusCode != 200,
  ),
)
```

## 보안 규칙

### 민감 정보 로깅 금지

```dart
// ❌ 금지: 민감 정보를 로그에 포함
Log.d('🔐 로그인: userId=$userId, password=$password');
Log.d('🔄 토큰: accessToken=$accessToken');

// ✅ 권장: 상태만 기록
Log.d('🔐 로그인 API 호출');
Log.d('🔄 토큰 갱신 완료');
```

### 민감 정보 목록

| 유형 | 예시 | 로깅 |
|------|------|------|
| 인증 정보 | password, pin, userPw | ❌ 금지 |
| 토큰 | accessToken, refreshToken, idToken | ❌ 금지 |
| 식별 정보 | userId, loginId (디버깅 목적 외) | ⚠️ 주의 |
| 개인 정보 | phoneNumber, email, address | ❌ 금지 |
| 인증 코드 | smsCode, verificationCode | ❌ 금지 |

## kDebugMode 패턴

### 올바른 사용

```dart
import 'package:flutter/foundation.dart' show kDebugMode;

// ✅ 컴파일 타임 상수로 프로덕션 코드에서 제거됨
if (kDebugMode) {
  // 디버그 전용 코드
}
```

### 주의사항

```dart
// ❌ 금지: 런타임 체크 (프로덕션에 코드 포함됨)
final isDebug = !const bool.fromEnvironment('dart.vm.product');
if (isDebug) { ... }

// ✅ 권장: kDebugMode 사용
if (kDebugMode) { ... }
```

## 체크리스트

### 로거 추가 시

- [ ] `kDebugMode` 조건 내에 로거 추가
- [ ] 프로덕션 빌드에서 로깅 비활성화 확인
- [ ] 민감 정보 로깅 여부 검토

### PR 리뷰 시

- [ ] 새로운 로그에 민감 정보 없음
- [ ] `kDebugMode` 조건부 로깅 사용
- [ ] 불필요한 상세 로깅 없음

## Mapper와 Repository Mixin의 로깅 스타일

### 로그 메시지 계층

| 계층 | 패턴 | 예시 |
|------|------|------|
| **Mapper** | 구조화된 로깅만 | `Log.e('msg', error: e, stackTrace: st)` |
| **Repository 시작** | 고정 메시지 | `Log.d('📝 API 호출')` |
| **Repository 성공** | 결과 포함 | `Log.d('✅ 완료: ${count}개')` |
| **Repository 에러** | 구조화된 로깅 | `Log.e('msg', error: e, stackTrace: st)` |

### 구조화된 로깅 패턴 (필수)

```dart
// ✅ CORRECT: error 파라미터 포함
Log.e('❌ Homework API Error', error: error, stackTrace: stackTrace);

// ❌ WRONG: error 파라미터 누락
Log.e('❌ Homework API Error: $error');
Log.e('❌ Homework API Error');

// ❌ WRONG: stackTrace 누락
Log.e('❌ Homework API Error', error: error);
```

### 이유

1. **일관성**: 모든 에러 로깅이 동일한 구조
2. **파싱**: 로그 집계 도구(Stack Driver 등)가 `error` 필드 파싱 가능
3. **정보 보존**: stackTrace가 구조화된 필드로 저장됨

## 관련 문서

- [data-mapper.md](./data-mapper.md) - DioException 처리 패턴
- [CLAUDE.md](../../CLAUDE.md) - HTTP 디버깅 섹션

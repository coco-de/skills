# Serverpod 로깅

session.log 기반 로깅, 보존 정책, Serverpod Insights를 다룹니다.

## 트리거

- 로깅 추가, 디버깅
- 로그 보존 정책 설정
- 로그 레벨 관리

## 기본 사용

```dart
session.log('Operation completed');

session.log('Something went wrong',
  level: LogLevel.warning,
  exception: e,
  stackTrace: stackTrace);
```

엔드포인트에서 잡히지 않은 예외는 `serverpod_session_log`에 실패로 기록.

## 저장 위치

| 저장소 | 테이블 | 조건 |
|--------|--------|------|
| DB | `serverpod_log`, `serverpod_query_log`, `serverpod_session_log` | persistent 활성화 시 |
| Console | stdout | console 활성화 시 |

기본: DB 설정 시 persistent ON + console OFF. DB 없으면 persistent OFF + console ON.

## 설정

`sessionLogs:` 또는 환경 변수:

| 설정 | 환경 변수 | 기본값 |
|------|----------|--------|
| persistentEnabled | `SERVERPOD_SESSION_PERSISTENT_LOG_ENABLED` | true (DB 있을 때) |
| consoleEnabled | `SERVERPOD_SESSION_CONSOLE_LOG_ENABLED` | false (DB 있을 때) |
| consoleLogFormat | `SERVERPOD_SESSION_CONSOLE_LOG_FORMAT` | text |
| cleanupInterval | `SERVERPOD_SESSION_LOG_CLEANUP_INTERVAL` | 24h |
| retentionPeriod | `SERVERPOD_SESSION_LOG_RETENTION_PERIOD` | 90d |
| retentionCount | `SERVERPOD_SESSION_LOG_RETENTION_COUNT` | - |

## 세션 타입별 생명주기

| 타입 | 생성 시점 | 종료 시점 |
|------|----------|----------|
| MethodCallSession | 엔드포인트 메서드 호출 | 요청 완료 |
| WebCallSession | 웹 서버 라우트 | 요청 완료 |
| MethodStreamSession | 스트림 메서드 | 스트림 종료 |
| StreamingSession | WebSocket 연결 | 연결 종료 |
| FutureCallSession | Future Call | 태스크 완료 |
| InternalSession | 수동 생성 | `session.close()` 호출 |

## InternalSession (수동 세션)

반드시 `finally`에서 close:

```dart
var session = await Serverpod.instance.createSession();
try {
  await doWork(session);
} finally {
  await session.close();
}
```

닫지 않으면 메모리 누수 + 로그 미저장.

## Cleanup Callback

```dart
session.addWillCloseListener((session) async {
  // 세션 종료 직전 실행
});
```

## 주의: 세션 캡처 금지

```dart
// BAD — 엔드포인트 반환 후 세션 이미 종료됨
Timer(Duration(seconds: 5), () => user.updateLastSeen(session));

// GOOD — FutureCall 또는 새 InternalSession 사용
session.serverpod.futureCalls.callWithDelay(...);
```

## 체크리스트

- [ ] 민감 데이터 로깅 금지
- [ ] retentionPeriod 설정 (로그 테이블 무한 증가 방지)
- [ ] InternalSession은 반드시 close
- [ ] 세션 종료 후 세션 사용 금지

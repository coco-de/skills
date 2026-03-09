# ClickHouse API Reference

serverpod-clickhouse 패키지의 상세 API 레퍼런스입니다.

## ClickHouseService

### 초기화

```dart
// Serverpod에서 초기화 (passwords.yaml 사용)
await ClickHouseService.initialize(pod);

// 수동 초기화 (테스트용)
await ClickHouseService.initializeWithConfig(
  ClickHouseConfig.cloud(
    host: 'xxx.clickhouse.cloud',
    database: 'analytics',
    username: 'default',
    password: 'xxx',
  ),
);
```

### 인스턴스 접근

```dart
final service = ClickHouseService.instance;

// 사용 가능한 컴포넌트
service.client    // ClickHouseClient - HTTP 클라이언트
service.tracker   // EventTracker - 이벤트 추적
service.analytics // AnalyticsQueryBuilder - 분석 쿼리
service.schema    // SchemaManager - 스키마 관리
service.sync      // SyncUtility - 동기화 유틸리티
```

---

## AnalyticsQueryBuilder

### 기본 메트릭

#### dau() - 일별 활성 사용자

```dart
Future<ClickHouseResult> dau({
  DateTime? date,  // 기준 날짜 (기본: 오늘)
  int days = 30,   // 조회 기간
})

// 사용
final result = await analytics.dau(days: 30);
// 결과: [{date: '2025-01-01', dau: 150}, ...]
```

#### wau() - 주별 활성 사용자

```dart
Future<ClickHouseResult> wau({int weeks = 12})

// 결과: [{week: '2025-01-06', wau: 850}, ...]
```

#### mau() - 월별 활성 사용자

```dart
Future<ClickHouseResult> mau({int months = 12})

// 결과: [{month: '2025-01-01', mau: 3200}, ...]
```

### 퍼널 분석

#### funnel() - 단계별 전환 분석

```dart
Future<FunnelResult> funnel({
  required List<String> steps,  // 이벤트 단계 목록
  int days = 7,                 // 분석 기간
  Duration? windowDuration,     // 전환 시간 윈도우 (기본: 1일)
})

// 사용
final result = await analytics.funnel(
  steps: ['sign_up_started', 'email_entered', 'sign_up_completed'],
  days: 7,
);

// 결과
print(result.overallConversionRate);  // 전체 전환율
print(result.stepResults[0].users);    // 1단계 사용자 수
print(result.stepResults[0].dropoffRate); // 이탈율
```

### 리텐션 분석

#### cohortRetention() - 코호트 리텐션

```dart
Future<ClickHouseResult> cohortRetention({
  required String cohortEvent,   // 코호트 정의 이벤트
  String returnEvent = 'app_opened',  // 복귀 이벤트
  int weeks = 8,                 // 분석 기간 (주)
})

// 결과: [{cohort_week, week_number, users}, ...]
```

#### nDayRetention() - N일 리텐션

```dart
Future<ClickHouseResult> nDayRetention({
  required String cohortEvent,
  String returnEvent = 'app_opened',
  List<int> days = const [1, 7, 30],  // D1, D7, D30
  int lookbackDays = 60,
})

// 결과: [{cohort_date, cohort_size, day_1_retained, day_7_retained, day_30_retained}, ...]
```

### 매출 분석

#### dailyRevenue() - 일별 매출

```dart
Future<ClickHouseResult> dailyRevenue({
  String revenueTable = 'orders',
  int days = 30,
})

// 결과: [{date, revenue, order_count, unique_customers}, ...]
```

#### arpu() - 사용자당 평균 매출

```dart
Future<ClickHouseResult> arpu({
  String revenueTable = 'orders',
  int months = 6,
})

// 결과: [{month, arpu, total_revenue, paying_users}, ...]
```

### 경로 분석

#### navigationPaths() - 화면 이동 경로

```dart
Future<ClickHouseResult> navigationPaths({
  int days = 7,
  int minCount = 10,      // 최소 이동 횟수
  String? flowName,       // 특정 플로우 필터
})

// 결과: [{from_screen, to_screen, transitions, unique_users}, ...]
```

#### dropOffPoints() - 이탈 지점

```dart
Future<ClickHouseResult> dropOffPoints({
  String? flowName,
  int days = 7,
  int limit = 20,
})

// 결과: [{flow_name, abandoned_at, step_index, abandon_count}, ...]
```

#### userJourney() - 사용자 여정

```dart
Future<ClickHouseResult> userJourney({
  required String userId,
  int days = 7,
  String? sessionId,
})

// 결과: [{session_id, timestamp, event_name, from_screen, to_screen}, ...]
```

### 커스텀 쿼리

```dart
Future<ClickHouseResult> custom(
  String sql, {
  Map<String, dynamic>? params,
})

// 사용
final result = await analytics.custom('''
  SELECT
    toDate(created_at) as date,
    count() as count
  FROM kobic_analytics.payment_book_order
  WHERE created_at >= now() - INTERVAL {days} DAY
  GROUP BY date
''', params: {'days': 30});
```

---

## EventTracker

### 이벤트 전송

```dart
Future<void> track(
  String eventName, {
  String? userId,
  String? sessionId,
  Map<String, dynamic>? properties,
  Map<String, dynamic>? context,
})

// 사용
await tracker.track(
  'button_click',
  userId: 'user_123',
  sessionId: 'session_456',
  properties: {
    'button': 'purchase',
    'book_id': '789',
    'price': 15000,
  },
  context: {
    'device': 'mobile',
    'os': 'iOS',
    'app_version': '1.0.0',
  },
);
```

### 배치 전송

```dart
// 버퍼에 쌓인 이벤트 즉시 전송
await tracker.flush();

// 서버 종료 시 (모든 이벤트 전송 후 정리)
await tracker.shutdown();
```

### 설정

```dart
EventTrackerConfig(
  batchSize: 100,           // 배치 크기
  flushInterval: Duration(seconds: 30),  // 자동 플러시 간격
  maxRetries: 3,            // 재시도 횟수
)
```

---

## ClickHouseClient

### 직접 쿼리

```dart
Future<ClickHouseResult> query(
  String sql, {
  Map<String, dynamic>? params,
})

// 사용
final result = await client.query(
  'SELECT * FROM events WHERE user_id = {user_id}',
  params: {'user_id': 'user_123'},
);
```

### 연결 테스트

```dart
Future<bool> ping()

// 사용
final connected = await client.ping();
```

### 배치 삽입

```dart
Future<void> insert(
  String table,
  List<Map<String, dynamic>> rows,
)

// 사용
await client.insert('events', [
  {'event_name': 'click', 'user_id': 'u1', 'timestamp': DateTime.now()},
  {'event_name': 'view', 'user_id': 'u2', 'timestamp': DateTime.now()},
]);
```

---

## ClickHouseResult

### 속성

```dart
class ClickHouseResult {
  final List<Map<String, dynamic>> rows;  // 결과 행
  final int rowsRead;      // 읽은 행 수
  final int bytesRead;     // 읽은 바이트
  final Duration elapsed;  // 쿼리 소요 시간
}
```

### 사용

```dart
final result = await analytics.dau(days: 7);

// 결과 접근
for (final row in result.rows) {
  print('${row['date']}: ${row['dau']} users');
}

// 메타데이터
print('Query took: ${result.elapsed.inMilliseconds}ms');
print('Rows read: ${result.rowsRead}');
```

---

## 파라미터 바인딩

### 지원 타입

| 타입 | 예시 |
|------|------|
| String | `{user_id}` → `'user_123'` |
| int | `{days}` → `30` |
| List<String> | `{ids}` → `('a', 'b', 'c')` |
| DateTime | `{date}` → `'2025-01-14'` |

### 예시

```dart
await client.query('''
  SELECT * FROM events
  WHERE user_id IN ({user_ids})
    AND timestamp >= {start_date}
    AND event_name = {event}
''', params: {
  'user_ids': ['user_1', 'user_2', 'user_3'],
  'start_date': DateTime(2025, 1, 1),
  'event': 'purchase',
});
```

---

## 에러 처리

```dart
try {
  final result = await analytics.dau(days: 30);
} on ClickHouseException catch (e) {
  print('ClickHouse error: ${e.message}');
  print('Query: ${e.query}');
} catch (e) {
  print('Unexpected error: $e');
}
```

---

## 성능 최적화

### 배치 쿼리 (대용량 데이터)

```dart
// WHERE + IN 패턴 (JOIN 대비 99% 메모리 절감)
final results = await analytics.batchQuery(
  ids: largeUserList,
  batchSize: 1000,
  sql: 'SELECT * FROM events WHERE user_id IN ({ids})',
);

// 결과 병합
final merged = analytics.mergeResults(results);
```

### argMax 활용 (FINAL 회피)

```dart
// ReplacingMergeTree에서 최신 상태 조회
final latest = await analytics.latestUserState(
  stateTable: 'user_states',
  userIds: ['u1', 'u2'],
  selectColumns: ['status', 'last_login'],
  versionColumn: 'updated_at',
);
```

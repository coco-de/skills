# ClickHouse Query Templates

kobic 프로젝트를 위한 분석 쿼리 템플릿입니다.

## 도서 분석

### 일별 도서 판매 현황

```sql
SELECT
    toDate(created_at) as date,
    count() as order_count,
    sum(total_amount) as revenue,
    uniqExact(user_id) as unique_buyers
FROM kobic_analytics.payment_book_order
WHERE created_at >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date DESC
```

### 베스트셀러 TOP 10

```sql
SELECT
    b.id as book_id,
    b.title as book_title,
    count(o.id) as sales_count,
    sum(o.total_amount) as total_revenue
FROM kobic_analytics.payment_book_order o
JOIN kobic_analytics.book_book b ON o.book_id = b.id
WHERE o.created_at >= now() - INTERVAL 30 DAY
GROUP BY b.id, b.title
ORDER BY sales_count DESC
LIMIT 10
```

### 출판사별 매출

```sql
SELECT
    p.name as publisher_name,
    count(o.id) as order_count,
    sum(o.total_amount) as revenue
FROM kobic_analytics.payment_book_order o
JOIN kobic_analytics.book_book b ON o.book_id = b.id
JOIN kobic_analytics.book_publisher p ON b.publisher_id = p.id
WHERE o.created_at >= now() - INTERVAL 30 DAY
GROUP BY p.id, p.name
ORDER BY revenue DESC
```

---

## 사용자 분석

### DAU/WAU/MAU

```sql
-- DAU
SELECT
    toDate(created_at) as date,
    uniqExact(user_id) as dau
FROM kobic_analytics.book_reading_progress
WHERE created_at >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date;

-- WAU
SELECT
    toStartOfWeek(created_at) as week,
    uniqExact(user_id) as wau
FROM kobic_analytics.book_reading_progress
WHERE created_at >= now() - INTERVAL 12 WEEK
GROUP BY week
ORDER BY week;

-- MAU
SELECT
    toStartOfMonth(created_at) as month,
    uniqExact(user_id) as mau
FROM kobic_analytics.book_reading_progress
WHERE created_at >= now() - INTERVAL 12 MONTH
GROUP BY month
ORDER BY month;
```

### 신규 가입자 추이

```sql
SELECT
    toDate(created) as date,
    count() as new_users
FROM kobic_analytics.serverpod_user_info
WHERE created >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date
```

### 사용자 코호트 분석

```sql
WITH first_purchase AS (
    SELECT
        user_id,
        toStartOfMonth(min(created_at)) as cohort_month
    FROM kobic_analytics.payment_book_order
    GROUP BY user_id
)
SELECT
    cohort_month,
    count() as cohort_size
FROM first_purchase
GROUP BY cohort_month
ORDER BY cohort_month
```

---

## 읽기 행동 분석

### 일별 읽기 활동

```sql
SELECT
    toDate(updated_at) as date,
    count() as reading_sessions,
    uniqExact(user_id) as active_readers,
    uniqExact(book_id) as books_read
FROM kobic_analytics.book_reading_progress
WHERE updated_at >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date DESC
```

### 인기 도서 (읽기 기준)

```sql
SELECT
    b.id as book_id,
    b.title as book_title,
    count(rp.id) as read_count,
    uniqExact(rp.user_id) as unique_readers,
    avg(rp.progress_percentage) as avg_progress
FROM kobic_analytics.book_reading_progress rp
JOIN kobic_analytics.book_book b ON rp.book_id = b.id
WHERE rp.updated_at >= now() - INTERVAL 7 DAY
GROUP BY b.id, b.title
ORDER BY unique_readers DESC
LIMIT 20
```

### 완독률 분석

```sql
SELECT
    b.title as book_title,
    count() as total_readers,
    countIf(rp.progress_percentage >= 100) as completed_readers,
    round(completed_readers * 100.0 / total_readers, 2) as completion_rate
FROM kobic_analytics.book_reading_progress rp
JOIN kobic_analytics.book_book b ON rp.book_id = b.id
WHERE rp.updated_at >= now() - INTERVAL 30 DAY
GROUP BY b.id, b.title
HAVING total_readers >= 10
ORDER BY completion_rate DESC
```

### 읽기 시간대 분석

```sql
SELECT
    toHour(updated_at) as hour,
    count() as reading_count,
    uniqExact(user_id) as unique_users
FROM kobic_analytics.book_reading_progress
WHERE updated_at >= now() - INTERVAL 7 DAY
GROUP BY hour
ORDER BY hour
```

---

## 필기 활동 분석

### 일별 필기 활동

```sql
SELECT
    toDate(created_at) as date,
    count() as scribble_count,
    uniqExact(user_id) as active_users,
    uniqExact(book_id) as books_with_scribbles
FROM kobic_analytics.scribble_activity
WHERE created_at >= now() - INTERVAL 30 DAY
GROUP BY date
ORDER BY date DESC
```

### 필기 유형별 분석

```sql
SELECT
    activity_type,
    count() as count,
    uniqExact(user_id) as unique_users
FROM kobic_analytics.scribble_activity
WHERE created_at >= now() - INTERVAL 7 DAY
GROUP BY activity_type
ORDER BY count DESC
```

### 필기 많은 도서 TOP 10

```sql
SELECT
    b.title as book_title,
    count(s.id) as scribble_count,
    uniqExact(s.user_id) as unique_users
FROM kobic_analytics.scribble_activity s
JOIN kobic_analytics.book_book b ON s.book_id = b.id
WHERE s.created_at >= now() - INTERVAL 30 DAY
GROUP BY b.id, b.title
ORDER BY scribble_count DESC
LIMIT 10
```

---

## 결제 분석

### 결제 수단별 현황

```sql
SELECT
    payment_method,
    count() as transaction_count,
    sum(amount) as total_amount,
    avg(amount) as avg_amount
FROM kobic_analytics.payment_wallet_transaction
WHERE created_at >= now() - INTERVAL 30 DAY
GROUP BY payment_method
ORDER BY total_amount DESC
```

### 쿠폰 사용 현황

```sql
SELECT
    c.code as coupon_code,
    c.discount_type,
    count(uc.id) as usage_count,
    sum(uc.discount_amount) as total_discount
FROM kobic_analytics.payment_user_coupon uc
JOIN kobic_analytics.payment_coupon c ON uc.coupon_id = c.id
WHERE uc.used_at >= now() - INTERVAL 30 DAY
GROUP BY c.id, c.code, c.discount_type
ORDER BY usage_count DESC
```

### ARPU (사용자당 평균 매출)

```sql
SELECT
    toStartOfMonth(created_at) as month,
    sum(total_amount) as total_revenue,
    uniqExact(user_id) as paying_users,
    round(total_revenue / paying_users, 2) as arpu
FROM kobic_analytics.payment_book_order
WHERE created_at >= now() - INTERVAL 6 MONTH
GROUP BY month
ORDER BY month
```

---

## 알림 분석

### 알림 발송 현황

```sql
SELECT
    toDate(created_at) as date,
    notification_type,
    count() as sent_count
FROM kobic_analytics.notification_send
WHERE created_at >= now() - INTERVAL 7 DAY
GROUP BY date, notification_type
ORDER BY date DESC, sent_count DESC
```

### 알림 효과 분석 (클릭률)

```sql
SELECT
    ns.notification_type,
    count(ns.id) as sent,
    count(nr.id) as received,
    countIf(nr.clicked = true) as clicked,
    round(clicked * 100.0 / sent, 2) as click_rate
FROM kobic_analytics.notification_send ns
LEFT JOIN kobic_analytics.notification_receive nr ON ns.id = nr.notification_id
WHERE ns.created_at >= now() - INTERVAL 7 DAY
GROUP BY ns.notification_type
ORDER BY click_rate DESC
```

---

## 퍼널 분석

### 가입 퍼널

```sql
WITH funnel AS (
    SELECT
        user_id,
        minIf(created_at, event_name = 'sign_up_started') as step1,
        minIf(created_at, event_name = 'email_verified') as step2,
        minIf(created_at, event_name = 'profile_completed') as step3,
        minIf(created_at, event_name = 'first_book_view') as step4
    FROM events
    WHERE created_at >= now() - INTERVAL 7 DAY
    GROUP BY user_id
)
SELECT
    count() as total_users,
    countIf(step1 IS NOT NULL) as started,
    countIf(step2 IS NOT NULL) as email_verified,
    countIf(step3 IS NOT NULL) as profile_completed,
    countIf(step4 IS NOT NULL) as first_book_view
FROM funnel
```

### 구매 퍼널

```sql
WITH purchase_funnel AS (
    SELECT
        user_id,
        minIf(created_at, event_name = 'book_detail_view') as view,
        minIf(created_at, event_name = 'add_to_cart') as cart,
        minIf(created_at, event_name = 'checkout_started') as checkout,
        minIf(created_at, event_name = 'purchase_completed') as purchase
    FROM events
    WHERE created_at >= now() - INTERVAL 7 DAY
    GROUP BY user_id
)
SELECT
    countIf(view IS NOT NULL) as viewed,
    countIf(cart IS NOT NULL) as added_to_cart,
    countIf(checkout IS NOT NULL) as started_checkout,
    countIf(purchase IS NOT NULL) as purchased,
    round(purchased * 100.0 / viewed, 2) as conversion_rate
FROM purchase_funnel
```

---

## 리텐션 분석

### 주간 리텐션

```sql
WITH first_activity AS (
    SELECT
        user_id,
        toStartOfWeek(min(created_at)) as cohort_week
    FROM kobic_analytics.book_reading_progress
    GROUP BY user_id
),
weekly_activity AS (
    SELECT
        user_id,
        toStartOfWeek(created_at) as activity_week
    FROM kobic_analytics.book_reading_progress
    GROUP BY user_id, activity_week
)
SELECT
    fa.cohort_week,
    dateDiff('week', fa.cohort_week, wa.activity_week) as week_number,
    uniqExact(fa.user_id) as users
FROM first_activity fa
JOIN weekly_activity wa ON fa.user_id = wa.user_id
WHERE wa.activity_week >= fa.cohort_week
    AND fa.cohort_week >= now() - INTERVAL 8 WEEK
GROUP BY fa.cohort_week, week_number
ORDER BY fa.cohort_week, week_number
```

---

## Dart 코드 예시

### 커스텀 쿼리 실행

```dart
import 'package:serverpod_clickhouse/serverpod_clickhouse.dart';

Future<List<Map<String, dynamic>>> getTopBooks({int days = 30}) async {
  final service = ClickHouseService.instance;

  final result = await service.analytics.custom('''
    SELECT
        b.id as book_id,
        b.title,
        count(o.id) as sales_count,
        sum(o.total_amount) as revenue
    FROM kobic_analytics.payment_book_order o
    JOIN kobic_analytics.book_book b ON o.book_id = b.id
    WHERE o.created_at >= now() - INTERVAL {days} DAY
    GROUP BY b.id, b.title
    ORDER BY sales_count DESC
    LIMIT 10
  ''', params: {'days': days});

  return result.rows;
}
```

### 대시보드 데이터 조회

```dart
Future<DashboardData> getDashboardData() async {
  final service = ClickHouseService.instance;

  // 병렬 쿼리 실행
  final results = await Future.wait([
    service.analytics.dau(days: 7),
    service.analytics.dailyRevenue(revenueTable: 'payment_book_order', days: 7),
    service.analytics.custom('SELECT count() as total FROM kobic_analytics.user'),
  ]);

  return DashboardData(
    dau: results[0].rows,
    revenue: results[1].rows,
    totalUsers: results[2].rows.first['total'] as int,
  );
}
```

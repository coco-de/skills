---
name: clickhouse
description: serverpod-clickhouse 패키지를 활용한 BI 분석 구축. DAU/MAU, 퍼널, 리텐션, 매출 분석 및 CDC 연동 지원.
---

# ClickHouse BI

serverpod-clickhouse 패키지를 활용한 BI 분석 구축 마스터 스킬입니다.

## Scope and Capabilities

### 지원 기능

| 기능 | 설명 | 명령어 |
|------|------|--------|
| CDC 설정 | PostgreSQL → ClickHouse 실시간 동기화 | `/clickhouse cdc` |
| 분석 쿼리 | DAU, 퍼널, 리텐션 등 분석 | `/clickhouse query` |
| 이벤트 추적 | 사용자 행동 이벤트 전송 | `/clickhouse event` |
| 스키마 관리 | 테이블 생성 및 마이그레이션 | `/clickhouse schema` |

### 아키텍처

```
┌─────────────────┐     CDC      ┌──────────────────┐
│  PostgreSQL     │ ──────────▶  │  ClickHouse      │
│  (RDS)          │  ClickPipes  │  Cloud           │
│  - OLTP         │              │  - OLAP 분석     │
└─────────────────┘              └────────┬─────────┘
                                          │
┌─────────────────┐                       │
│  Serverpod      │ ◀─────────────────────┘
│  Server         │   분석 API
└─────────────────┘
```

## Quick Start

### 1. 서버 초기화

```dart
// server.dart
import 'package:serverpod_clickhouse/serverpod_clickhouse.dart' as clickhouse;

Future<void> run(List<String> args) async {
  final pod = Serverpod(args, Protocol(), Endpoints());

  // ClickHouse 초기화
  await clickhouse.ClickHouseService.initialize(pod);

  await pod.start();
}
```

### 2. 분석 쿼리 사용

```dart
// Endpoint에서 사용
final service = clickhouse.ClickHouseService.instance;

// DAU 조회
final dau = await service.analytics.dau(days: 30);

// 퍼널 분석
final funnel = await service.analytics.funnel(
  steps: ['sign_up_started', 'email_entered', 'sign_up_completed'],
  days: 7,
);

// 커스텀 쿼리
final result = await service.analytics.custom('''
  SELECT
    toDate(created_at) as date,
    count() as orders,
    sum(total_amount) as revenue
  FROM kobic_analytics.payment_book_order
  GROUP BY date
  ORDER BY date DESC
  LIMIT 30
''');
```

### 3. 이벤트 추적

```dart
// 이벤트 전송
await service.tracker.track(
  'button_click',
  userId: 'user_123',
  properties: {'button': 'purchase', 'book_id': '456'},
);

// 배치 전송 (자동)
await service.tracker.flush();
```

## 환경 설정

### passwords.yaml

```yaml
staging:
  clickhouse_host: "xxx.ap-northeast-2.aws.clickhouse.cloud"
  clickhouse_port: "8443"
  clickhouse_database: "kobic_analytics"
  clickhouse_user: "default"
  clickhouse_password: "your-password"

production:
  clickhouse_host: "xxx.ap-northeast-2.aws.clickhouse.cloud"
  clickhouse_port: "8443"
  clickhouse_database: "kobic_analytics"
  clickhouse_user: "default"
  clickhouse_password: "your-password"
```

## CDC 테이블 (현재 동기화 중)

| 테이블 | 용도 | 데이터 |
|--------|------|--------|
| `user` | 사용자 정보 | 마스터 |
| `book_book` | 도서 정보 | 마스터 |
| `book_publisher` | 출판사 | 마스터 |
| `author` | 저자 | 마스터 |
| `book_category` | 카테고리 | 마스터 |
| `book_reading_progress` | 읽기 진행률 | 행동 분석 |
| `payment_book_order` | 주문 | 매출 분석 |
| `payment_wallet_transaction` | 결제 | 결제 분석 |
| `payment_user_wallet` | 지갑 | 결제 분석 |
| `payment_coupon` | 쿠폰 | 프로모션 |
| `payment_user_coupon` | 사용자 쿠폰 | 프로모션 |
| `notification_send` | 알림 발송 | 푸시 분석 |
| `notification_receive` | 알림 수신 | 푸시 분석 |
| `serverpod_user_info` | 인증 정보 | 마스터 |
| `scribble_activity` | 필기 활동 | 행동 분석 |

## 핵심 분석 쿼리

### DAU/WAU/MAU

```dart
final dau = await service.analytics.dau(days: 30);
final wau = await service.analytics.wau(weeks: 12);
final mau = await service.analytics.mau(months: 12);
```

### 퍼널 분석

```dart
final funnel = await service.analytics.funnel(
  steps: [
    'book_view',
    'add_to_cart',
    'checkout_started',
    'purchase_completed',
  ],
  days: 7,
);
print('전환율: ${funnel.overallConversionRate * 100}%');
```

### 리텐션 분석

```dart
final retention = await service.analytics.cohortRetention(
  cohortEvent: 'sign_up_completed',
  returnEvent: 'app_opened',
  weeks: 8,
);
```

### 매출 분석

```dart
final revenue = await service.analytics.dailyRevenue(
  revenueTable: 'payment_book_order',
  days: 30,
);
```

## 명령어

### CDC 테이블 추가

```bash
# PostgreSQL에서
GRANT SELECT ON public.{table_name} TO clickpipes_user;
ALTER PUBLICATION kobic_analytics_pub ADD TABLE public.{table_name};

# ClickPipes UI에서 테이블 추가
```

### 연결 테스트

```bash
curl --user 'default:{password}' \
  --data-binary 'SELECT count() FROM kobic_analytics.{table}' \
  https://{host}:8443
```

## OpenAPI (ClickPipes 자동화)

ClickHouse Cloud OpenAPI를 사용하여 ClickPipes CDC를 프로그래매틱하게 관리할 수 있습니다.

### 인증

```bash
# API Key 생성: ClickHouse Cloud Console → Organization → API Keys
KEY_ID="your-key-id"
KEY_SECRET="your-key-secret"

# HTTP Basic Auth 사용
curl --user "${KEY_ID}:${KEY_SECRET}" \
  "https://api.clickhouse.cloud/v1/organizations"
```

### 주요 엔드포인트

| 작업 | Method | Endpoint |
|------|--------|----------|
| 조직 목록 | GET | `/v1/organizations` |
| 서비스 목록 | GET | `/v1/organizations/{orgId}/services` |
| ClickPipe 목록 | GET | `/v1/organizations/{orgId}/services/{serviceId}/clickpipes` |
| ClickPipe 생성 | POST | `/v1/organizations/{orgId}/services/{serviceId}/clickpipes` |
| ClickPipe 삭제 | DELETE | `/v1/organizations/{orgId}/services/{serviceId}/clickpipes/{pipeId}` |

### ClickPipe 생성 예시 (PostgreSQL CDC)

```bash
curl --user "${KEY_ID}:${KEY_SECRET}" \
  -X POST \
  -H "Content-Type: application/json" \
  "https://api.clickhouse.cloud/v1/organizations/${ORG_ID}/services/${SERVICE_ID}/clickpipes" \
  -d '{
    "name": "my-cdc-pipe",
    "source": {
      "postgres": {
        "host": "your-rds-host.amazonaws.com",
        "port": 5432,
        "database": "your_database",
        "credentials": {
          "username": "clickpipes_user",
          "password": "your_password"
        },
        "settings": {
          "syncIntervalSeconds": 60,
          "publicationName": "your_publication",
          "replicationMode": "cdc",
          "allowNullableColumns": true
        },
        "tableMappings": [
          {
            "sourceSchemaName": "public",
            "sourceTable": "users",
            "targetTable": "users",
            "tableEngine": "ReplacingMergeTree"
          }
        ]
      }
    },
    "destination": {
      "database": "analytics"
    }
  }'
```

### kobic 환경 정보

```bash
# Staging
ORG_ID="4824fced-f81b-4ce0-999c-dedda1640510"
SERVICE_ID="cf625fee-d709-420f-8088-6308de4cd908"  # kobic-analytics-staging

# Production
SERVICE_ID="4c0db2e2-48fb-4e33-8509-c33babff3600"  # kobic_analytics
```

### 주의사항

- PostgreSQL CDC ClickPipe 수정 시 먼저 삭제 후 재생성 필요
- 기존 테이블이 있으면 충돌 발생 → 테이블 먼저 DROP 필요
- Terraform 지원은 2025년 후반 예정 (현재 Kafka만 지원)

## Additional Resources

- [REFERENCE.md](REFERENCE.md) - 상세 API 레퍼런스
- [TEMPLATES.md](TEMPLATES.md) - 분석 쿼리 템플릿
- [CDC Setup Guide](https://github.com/coco-de/serverpod-clickhouse/blob/main/docs/CDC_SETUP_GUIDE.md) - CDC 설정 가이드
- [BI Events Guide](https://github.com/coco-de/serverpod-clickhouse/blob/main/docs/BI_EVENTS_GUIDE.md) - 이벤트 추적 가이드

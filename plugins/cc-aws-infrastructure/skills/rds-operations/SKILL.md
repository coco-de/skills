---
name: rds-operations
description: RDS 장애 대응 및 운영 관리
---

# RDS 장애 대응 및 운영

RDS PostgreSQL 장애 진단, 스토리지 확장, replication slot 관리를 다룹니다.

## 트리거

- 서버 502/503 에러 (앱에서 "서버 점검 중")
- RDS 인스턴스 상태 이상 (storage-full, modifying 등)
- 데이터베이스 성능 저하
- Replication slot WAL 누적

> 인프라 장애 디버깅 순서는 `rules/aws-operations.md` 참조

## RDS Storage-Full 대응

### 진단

```bash
# 1. RDS 인스턴스 상태 확인
aws rds describe-db-instances \
  --db-instance-identifier kobic-<env> \
  --query 'DBInstances[0].{Status:DBInstanceStatus,Storage:AllocatedStorage,MaxStorage:MaxAllocatedStorage}'

# 2. FreeStorageSpace 메트릭 (최근 1시간)
aws cloudwatch get-metric-statistics \
  --namespace AWS/RDS \
  --metric-name FreeStorageSpace \
  --dimensions Name=DBInstanceIdentifier,Value=kobic-<env> \
  --start-time $(date -u -v-1H +%Y-%m-%dT%H:%M:%S) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%S) \
  --period 300 --statistics Minimum \
  --output table

# 3. DB 접속 후 테이블별 용량 확인
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as total_size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
LIMIT 20;
```

### 긴급 스토리지 확장

```bash
# 즉시 적용, 다운타임 없음
aws rds modify-db-instance \
  --db-instance-identifier kobic-<env> \
  --allocated-storage <new_size_gb> \
  --max-allocated-storage <new_max_gb> \
  --apply-immediately
```

**주의사항**:
- RDS 스토리지 확장은 **축소 불가** (한번 늘리면 줄일 수 없음)
- 확장 후 **6시간 쿨다운** (추가 확장 불가)
- `storage-optimization` 상태에서도 DB는 정상 사용 가능

### Terraform Drift 처리

긴급 확장 후 Terraform 코드와 실제 인프라가 불일치합니다:

```hcl
# config.auto.tfvars 업데이트 필요
db_configs = {
  "staging" = {
    allocated_storage       = 200  # 긴급 확장 반영
    max_allocated_storage   = 500  # 긴급 확장 반영
    # ...
  }
}
```

## Replication Slot 관리

CDC(Change Data Capture) replication slot이 WAL을 누적하여 스토리지를 소비합니다.

```sql
-- Replication slot 상태 확인
SELECT slot_name, slot_type, active,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) as retained_wal
FROM pg_replication_slots;

-- 비활성 slot 삭제 (ClickHouse ClickPipe 등)
SELECT pg_drop_replication_slot('slot_name_here');
```

## RDS 인스턴스 사양

### 현재 설정 (Graviton2 ARM64)

| 환경 | Instance Class | vCPU | Memory | Storage | Max Storage | Multi-AZ |
|------|---------------|------|--------|---------|------------|----------|
| Production | db.t4g.small | 2 | 2GB | 20GB | 200GB | ✅ |
| Staging | db.t4g.small | 2 | 2GB | 20GB | 100GB | ❌ |
| Development | db.t4g.micro | 2 | 1GB | 20GB | 50GB | ❌ |

> CloudWatch 알람 현황은 `rules/aws-operations.md` 참조

## 체크리스트

### Storage-Full 대응
- [ ] `aws rds describe-db-instances` 상태 확인
- [ ] CloudWatch FreeStorageSpace 메트릭 확인
- [ ] 테이블별 용량 분석 (pg_total_relation_size)
- [ ] Replication slot retained WAL 확인
- [ ] 긴급 스토리지 확장 실행
- [ ] Terraform config.auto.tfvars 업데이트 (별도 PR)

### 정기 모니터링
- [ ] 월 1회 스토리지 사용률 확인
- [ ] Replication slot WAL 크기 확인
- [ ] CloudWatch 알람 alarm_actions 연결 확인

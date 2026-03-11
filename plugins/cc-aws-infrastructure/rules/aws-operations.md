# AWS 인프라 운영 규칙

AWS 인프라 장애 대응 및 운영 규칙입니다.

## 인프라 디버깅 순서

장애 발생 시 아래 순서로 확인합니다 (**RDS가 가장 흔한 원인**):

```
1. RDS 상태 확인 (storage-full이 가장 빈번)
2. EC2/ASG 인스턴스 상태 확인
3. Target Group 헬스체크 확인
4. ALB 접근 로그 확인
5. CodeDeploy 배포 상태 확인
6. CloudWatch 로그 확인
```

## 빠른 상태 확인 명령어

```bash
# RDS 상태
aws rds describe-db-instances \
  --query 'DBInstances[*].{ID:DBInstanceIdentifier,Status:DBInstanceStatus,Storage:AllocatedStorage}' \
  --output table

# ASG 인스턴스 상태
aws autoscaling describe-auto-scaling-groups \
  --query 'AutoScalingGroups[?contains(AutoScalingGroupName,`kobic`)].{Name:AutoScalingGroupName,Desired:DesiredCapacity,Instances:Instances[*].{ID:InstanceId,Health:HealthStatus}}' \
  --output json

# Target Group 헬스
aws elbv2 describe-target-health \
  --target-group-arn <target-group-arn> \
  --output table

# 최근 배포 상태
aws deploy list-deployments \
  --application-name kobic-app \
  --deployment-group-name kobic-<env>-dg \
  --max-items 3 \
  --query 'deployments'
```

## RDS Storage-Full 대응

### 증상

- 서버 502/503 에러 (앱에서 "서버 점검 중")
- RDS 인스턴스 상태: `storage-full`
- CloudWatch `FreeStorageSpace` 메트릭이 0에 도달

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
- RDS 스토리지 확장은 **축소 불가**
- 확장 후 **6시간 쿨다운**
- `storage-optimization` 상태에서도 DB 정상 사용 가능
- 긴급 확장 후 Terraform `config.auto.tfvars` 업데이트 필요 (drift 방지)

### Replication Slot 관리

CDC replication slot이 WAL을 누적하여 스토리지를 소비합니다.

```sql
-- slot 상태 확인
SELECT slot_name, slot_type, active,
       pg_size_pretty(pg_wal_lsn_diff(pg_current_wal_lsn(), restart_lsn)) as retained_wal
FROM pg_replication_slots;

-- 비활성 slot 삭제
SELECT pg_drop_replication_slot('slot_name_here');
```

## CodeDeploy ASG 누적 문제

### 증상

- 배포 시 CodeDeploy가 삭제된 ASG에 배포 시도 → 실패

### 해결

```bash
# CodeDeploy Deployment Group의 ASG 목록 확인
aws deploy get-deployment-group \
  --application-name kobic-app \
  --deployment-group-name kobic-<env>-dg \
  --query 'deploymentGroupInfo.autoScalingGroups[].name'

# 올바른 ASG만 포함하도록 업데이트
aws deploy update-deployment-group \
  --application-name kobic-app \
  --current-deployment-group-name kobic-<env>-dg \
  --auto-scaling-groups "kobic-<env>-asg"
```

## Docker 기반 배포 워크플로우

```
GitHub Actions → Docker Build → ECR Push → CodeDeploy → ASG Instance (Docker Compose)
```

| 환경 | 코드 반영 브랜치 | 배포 방법 |
|------|-----------------|----------|
| **Staging** | `development` | GitHub Actions workflow_dispatch |
| **Production** | `main` | `main` 브랜치 push 시 자동 배포 |

## CloudWatch 알람 현황

| 알람 | 임계값 | 상태 |
|------|--------|------|
| `database-high-cpu` | 80% | ⚠️ alarm_actions 빈 배열 |
| `database-high-connections` | 50 | 설정 없음 |
| FreeStorageSpace | 미설정 | ❌ **추가 필요** |

## ElastiCache Redis 주의사항

- Transit Encryption이 비활성화된 상태에서는 AUTH 활성화 불가
- Serverpod는 Redis 활성화 시 `SERVERPOD_PASSWORD_redis` 환경 변수 필수
- `SERVERPOD_PASSWORD_redis=""` 설정으로 서버 시작 가능 (AUTH 없이 동작)
- 인증은 Redis 없이도 DB 기반으로 정상 동작

## 체크리스트

### 장애 대응

- [ ] RDS 인스턴스 상태 확인 (`describe-db-instances`)
- [ ] CloudWatch FreeStorageSpace 메트릭 확인
- [ ] Replication slot retained WAL 확인
- [ ] ASG/Target Group 헬스체크 확인
- [ ] CodeDeploy 배포 상태 확인

### Terraform Drift 방지

- [ ] 긴급 AWS CLI 변경 후 `config.auto.tfvars` 업데이트
- [ ] `terraform plan`으로 drift 확인
- [ ] 별도 PR로 코드 업데이트

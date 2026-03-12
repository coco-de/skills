---
name: terraform-apply
description: Terraform Apply 실행 및 인프라 변경 적용
---

# Terraform Apply 실행

Terraform apply를 `-target` 옵션으로 안전하게 실행하여 인프라 변경을 적용합니다.

## 트리거

- DNS 레코드 추가/수정 적용
- 인프라 설정 변경 반영
- 새 환경 리소스 프로비저닝

## 사전 조건

1. **Lambda ZIP placeholder** 생성 완료 (terraform-plan 스킬 참조)
2. **terraform init** 성공
3. **terraform plan** 실행하여 변경사항 확인 완료

## Apply 패턴

### -target 옵션으로 안전한 적용

```bash
# ⚠️ 항상 -target으로 범위를 제한하여 적용
terraform apply -auto-approve \
  -target='module.production_env[0].aws_route53_record.deeplink' \
  -target='module.production_env[0].aws_route53_record.deeplink_secondary' \
  -target='module.staging_env[0].aws_route53_record.deeplink' \
  -target='module.staging_env[0].aws_route53_record.deeplink_secondary'
```

### 모듈명 참조

| 용도 | 모듈명 | count 조건 |
|------|--------|-----------|
| Production 환경 | `module.production_env[0]` | `enable_production_server` |
| Staging 환경 | `module.staging_env[0]` | `enable_staging_server` |
| Development 환경 | `module.development_env[0]` | `enable_development_server` |
| Push (Production) | `module.message_production[0]` | `enable_push_notifications && is_production_enabled` |
| Push (Staging) | `module.message_staging[0]` | `enable_push_notifications && is_staging_enabled` |
| PDF (Production) | `module.pdf_processing_production[0]` | `enable_pdf_processing && is_production_enabled` |
| Batch (Production) | `module.batch_processing_production[0]` | `enable_batch_processing && is_production_enabled` |

### "No changes" 결과 해석

Terraform이 "No changes"를 반환하는 경우:

| 원인 | 진단 방법 |
|------|----------|
| 이미 적용됨 | `terraform state list \| grep <resource>` |
| count = 0 | 변수 조건 확인 (enable_route53, enable_primary_dns 등) |
| 잘못된 모듈명 | main.tf의 `module "..."` 블록명 확인 |
| State에 없음 | `aws` CLI로 실제 리소스 존재 여부 확인 |

## Apply 후 검증

### DNS 레코드 검증

```bash
# DNS 전파 확인
dig <domain> CNAME +short

# Route53 직접 확인
aws route53 list-resource-record-sets \
  --hosted-zone-id <zone-id> \
  --query "ResourceRecordSets[?contains(Name, '<keyword>')]"
```

### RDS 상태 확인

```bash
aws rds describe-db-instances \
  --query 'DBInstances[*].{ID:DBInstanceIdentifier,Status:DBInstanceStatus}'
```

### State 확인

```bash
# 적용된 리소스 확인
terraform state list | grep <keyword>

# 특정 리소스 상세
terraform state show 'module.production_env[0].aws_route53_record.deeplink[0]'
```

## 주의사항

- **-target 없이 apply 금지**: Lambda ZIP placeholder로 인해 Lambda 리소스가 업데이트될 수 있음
- **production workspace에서 주의**: 실수로 리소스 삭제 방지를 위해 항상 plan 먼저 실행
- **State 원격 저장**: S3 backend (`kobic-tfstate-bucket`)에 자동 저장, DynamoDB로 락 관리

## 체크리스트

- [ ] `terraform plan` 결과 확인 (destroy 없는지)
- [ ] `-target` 옵션으로 범위 제한
- [ ] apply 후 실제 리소스 생성 확인 (AWS CLI 또는 dig)
- [ ] State에 리소스 기록 확인

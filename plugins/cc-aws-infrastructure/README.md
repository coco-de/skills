# cc-aws-infrastructure

AWS 인프라 관리 및 Terraform 운영 플러그인

> Serverpod 백엔드의 AWS 인프라를 Terraform으로 관리합니다. VPC, ALB, ASG, RDS, Redis, Lambda, Route53, CloudFront, CodeDeploy 등 전체 스택을 다룹니다.

## Skills

| 스킬 | 설명 |
|------|------|
| `terraform-plan` | Terraform plan 실행 및 변경사항 분석 (Lambda ZIP placeholder 자동 처리) |
| `terraform-apply` | Terraform apply 실행 (-target 옵션으로 안전한 부분 적용) |
| `dns-management` | Route53 DNS 레코드 관리 (CNAME, A record, multi-domain) |
| `rds-operations` | RDS 장애 대응 (storage-full, 스토리지 확장, replication slot 정리) |
| `lambda-management` | Lambda 함수 관리 (ZIP 빌드, 배포, Step Functions 연동) |

## Rules

| 규칙 | 설명 |
|------|------|
| `terraform-conventions` | Terraform 코드 컨벤션 및 모듈 구조 규칙 |
| `aws-operations` | AWS 인프라 운영 및 장애 대응 규칙 |

## 아키텍처 개요

```
┌─ Shared (1회 생성) ──────────────────────────────┐
│  VPC (4 public + 4 private subnets, Multi-AZ)    │
│  ALB (HTTPS termination, multi-domain)           │
│  Security Groups (5개)                            │
│  IAM Roles, CodeDeploy App, ECR                  │
└──────────────────────────────────────────────────┘
        │
┌─ Per-Environment (production, staging, dev) ─────┐
│  EC2 ASG + Launch Template (Serverpod Docker)    │
│  RDS PostgreSQL (t4g, Multi-AZ optional)         │
│  ElastiCache Redis (t4g, Redis 7.0)              │
│  S3 Buckets + CloudFront CDN                     │
│  Route53 DNS (primary + secondary domain)        │
│  CodeDeploy Deployment Group                     │
└──────────────────────────────────────────────────┘
        │
┌─ Optional Services (feature-toggled) ────────────┐
│  Push Notifications (SQS → Lambda → SNS/FCM)    │
│  PDF Processing (S3 → Step Functions → Lambda)   │
│  Batch Processing (SQS → Lambda → DB)            │
└──────────────────────────────────────────────────┘
```

## 주요 사용 사례

- Terraform plan/apply로 인프라 변경 적용
- Route53 DNS 레코드 추가/수정 (딥링크, Firebase Hosting 등)
- RDS storage-full 장애 대응 및 스토리지 확장
- Lambda 함수 배포 및 환경 변수 관리
- CloudFront 캐시 무효화
- CodeDeploy 배포 상태 확인 및 ASG 정리

# Terraform 코드 컨벤션

## 모듈 구조

```
terraform/
├── main.tf              # 모듈 조합 및 오케스트레이션
├── variables.tf         # Map-based 변수 (환경별)
├── config.auto.tfvars   # 실제 값 설정
├── outputs.tf           # 출력 변수
├── backend.tf           # S3 + DynamoDB 원격 상태
├── moved.tf             # 상태 마이그레이션
└── modules/
    ├── shared/          # 1회 생성 (VPC, ALB, IAM, SG)
    ├── environment/     # 환경별 (EC2, RDS, Redis, S3, DNS)
    ├── message/         # Push 알림 (SQS, SNS, Lambda)
    ├── pdf_processing/  # PDF 처리 (Step Functions, Lambda)
    └── batch_processing/ # 배치 처리 (SQS, Lambda)
```

## 변수 설계 패턴

### Map-based 변수 (환경별 설정)

```hcl
# ✅ CORRECT: Map으로 환경별 설정
variable "instance_types" {
  type = map(string)
  default = {
    "production"  = "t4g.medium"
    "staging"     = "t4g.small"
    "development" = "t4g.small"
  }
}

# ❌ WRONG: 환경별 별도 변수
variable "production_instance_type" { ... }
variable "staging_instance_type" { ... }
```

### 모듈에 변수 전달 (lookup 패턴)

```hcl
# ✅ CORRECT: lookup으로 안전한 접근
deeplink_subdomain = lookup(var.deeplink_config, "production", null) != null ? var.deeplink_config["production"]["subdomain"] : ""

# ❌ WRONG: 직접 접근 (키 없으면 에러)
deeplink_subdomain = var.deeplink_config["production"]["subdomain"]
```

### Feature Toggle 패턴

```hcl
# 환경 활성화
locals {
  is_production_enabled  = var.enable_production_server
  is_staging_enabled     = var.enable_staging_server
  is_development_enabled = var.enable_development_server
}

# 모듈 count 조건
module "production_env" {
  count = local.is_production_enabled ? 1 : 0
  # ...
}

# 서비스 + 환경 조합 조건
module "message_production" {
  count = var.enable_push_notifications && local.is_production_enabled ? 1 : 0
  # ...
}
```

## Route53 리소스 패턴

### count 조건 규칙

| 레코드 유형 | count 조건 |
|-----------|-----------|
| Primary CNAME | `enable_route53 && enable_primary_dns && subdomain != ""` |
| Secondary CNAME | `enable_route53 && secondary_domain != null && subdomain != ""` |
| Top domain A | `enable_route53 && enable_primary_dns && enable_top_domain_alias && length(ips) > 0` |
| Production-only | 추가로 `local.is_production` 조건 |

### 서브도메인 네이밍

```hcl
# ✅ CORRECT: Production은 prefix 없이, 나머지는 suffix
name = local.is_production ? "console" : "console-${local.env_short_suffix}"

# env_short_suffix: "stg" or "dev"
```

## Lambda ZIP 경로 규칙

### path.module 기준 상대 경로

```hcl
# 모듈 내부에서 Lambda ZIP 참조
locals {
  lambda_base_path = "${path.module}/../../../lambda/python"
  router_zip_path  = "${local.lambda_base_path}/pdf_router/build/pdf-router.zip"
}
```

**⚠️ 주의**: `path.module`은 모듈 .tf 파일 위치 기준이므로:
- `modules/pdf_processing/../../../` = `deploy/aws/`
- `terraform/` 실행 디렉토리가 아님

### fileexists() 가드 패턴

```hcl
# ✅ CORRECT: fileexists()로 가드
locals {
  zip_exists = fileexists(local.zip_path)
}

resource "aws_lambda_function" "example" {
  count            = local.zip_exists ? 1 : 0
  source_code_hash = local.zip_exists ? filebase64sha256(local.zip_path) : null
}

# ❌ WRONG: 가드 없이 직접 호출 (파일 없으면 plan 실패)
resource "aws_lambda_function" "example" {
  source_code_hash = filebase64sha256(local.zip_path)
}
```

## State 관리

### Remote Backend

```hcl
backend "s3" {
  bucket         = "kobic-tfstate-bucket"
  key            = "terraform.tfstate"
  region         = "ap-northeast-2"
  dynamodb_table = "kobic-tfstate-lock"
  encrypt        = true
}
```

### Workspace 사용

```bash
# Workspace 목록
terraform workspace list

# Workspace 전환
terraform workspace select production
```

> 이 프로젝트는 workspace + enable_*_server 플래그 조합으로 환경을 관리합니다.

## 태그 규칙

```hcl
tags = {
  Project     = var.project_name
  Environment = var.environment
  ManagedBy   = "terraform"
}
```

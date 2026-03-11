# Route53 DNS 레코드 관리

Route53 DNS 레코드를 Terraform으로 관리합니다. Multi-domain 지원 (primary + secondary domain).

## 트리거

- 새 서브도메인 추가 (딥링크, Firebase Hosting 등)
- DNS 레코드 수정/삭제
- 도메인 마이그레이션

## 도메인 구조

### Hosted Zones

| 도메인 | Zone ID | 용도 |
|--------|---------|------|
| unibook.co.kr | `Z0775776240YOL7IYBNYH` | Primary (현재 사용) |
| laputa.im | `Z0911207339KKWN48L9BW` | Secondary (레거시) |

### 인증서 (ACM)

| 용도 | 리전 | 비고 |
|------|------|------|
| ALB용 | ap-northeast-2 | `*.unibook.co.kr` 와일드카드 |
| CloudFront용 | us-east-1 | `*.unibook.co.kr` 와일드카드 (CloudFront 필수) |
| Secondary ALB | ap-northeast-2 | `*.laputa.im` 와일드카드 |
| Secondary CloudFront | us-east-1 | `*.laputa.im` 와일드카드 |

### 서브도메인 패턴

| 서브도메인 | 타겟 | Production | Staging |
|-----------|------|-----------|---------|
| api | ALB | `api.unibook.co.kr` | `api-stg.unibook.co.kr` |
| web | ALB | `web.unibook.co.kr` | `web-stg.unibook.co.kr` |
| insights | ALB | `insights.unibook.co.kr` | `insights-stg.unibook.co.kr` |
| storage | CloudFront | `storage.unibook.co.kr` | `storage-stg.unibook.co.kr` |
| assets | CloudFront | `assets.unibook.co.kr` | `assets-stg.unibook.co.kr` |
| app | Firebase | `app.unibook.co.kr` | `app-stg.unibook.co.kr` |
| console | Firebase | `console.unibook.co.kr` | `console-stg.unibook.co.kr` |
| deeplink | ALB (CNAME) | `deeplink.unibook.co.kr` | `stdeeplink.unibook.co.kr` |

## DNS 레코드 추가 절차

### 1. variables.tf에 Map 변수 추가 (root)

```hcl
variable "new_config" {
  description = "New domain configuration"
  type = map(object({
    subdomain = string
    target    = string
  }))
  default = {}
}
```

### 2. config.auto.tfvars에 값 설정

```hcl
new_config = {
  "production" = {
    "subdomain" = "myapp"
    "target"    = "web.unibook.co.kr"
  }
  "staging" = {
    "subdomain" = "myapp-stg"
    "target"    = "web-stg.unibook.co.kr"
  }
}
```

### 3. environment 모듈 variables.tf에 변수 추가

```hcl
variable "new_subdomain" {
  description = "Subdomain for new service"
  type        = string
  default     = ""
}

variable "new_target" {
  description = "Target for new service"
  type        = string
  default     = ""
}
```

### 4. firebase-dns.tf (또는 새 .tf 파일)에 리소스 추가

```hcl
# Primary domain
resource "aws_route53_record" "new_service" {
  count = var.enable_route53 && var.enable_primary_dns && var.new_subdomain != "" ? 1 : 0

  zone_id         = var.hosted_zone_id
  name            = var.new_subdomain
  type            = "CNAME"
  ttl             = "60"
  records         = [var.new_target]
  allow_overwrite = true
}

# Secondary domain
resource "aws_route53_record" "new_service_secondary" {
  count = var.enable_route53 && var.secondary_domain != null && var.new_subdomain != "" ? 1 : 0

  zone_id         = var.secondary_hosted_zone_id
  name            = var.new_subdomain
  type            = "CNAME"
  ttl             = "60"
  records         = ["${var.new_subdomain}.${var.secondary_domain}"]
  allow_overwrite = true
}
```

### 5. main.tf에서 변수 전달

```hcl
module "production_env" {
  # ...
  new_subdomain = lookup(var.new_config, "production", null) != null ? var.new_config["production"]["subdomain"] : ""
  new_target    = lookup(var.new_config, "production", null) != null ? var.new_config["production"]["target"] : ""
}
```

## count 조건 패턴

### Primary domain DNS

```hcl
count = var.enable_route53 && var.enable_primary_dns && var.<subdomain> != "" ? 1 : 0
```

### Secondary domain DNS

```hcl
count = var.enable_route53 && var.secondary_domain != null && var.<subdomain> != "" ? 1 : 0
```

### Production-only 리소스 (Top domain alias 등)

```hcl
count = var.enable_route53 && var.enable_primary_dns && var.enable_top_domain_alias && <condition> ? 1 : 0
```

## 검증

```bash
# CNAME 레코드 확인
dig <subdomain>.unibook.co.kr CNAME +short

# A 레코드 확인
dig <subdomain>.unibook.co.kr A +short

# Route53 직접 조회
aws route53 list-resource-record-sets \
  --hosted-zone-id <hosted-zone-id> \
  --query "ResourceRecordSets[?contains(Name, '<keyword>')]" \
  --output table
```

## 체크리스트

- [ ] root variables.tf에 Map 변수 추가
- [ ] config.auto.tfvars에 환경별 값 설정
- [ ] environment module variables.tf에 변수 추가
- [ ] Route53 리소스 정의 (primary + secondary)
- [ ] main.tf에서 각 환경 모듈에 변수 전달 (lookup 패턴)
- [ ] terraform plan으로 변경 확인
- [ ] terraform apply -target으로 적용
- [ ] dig 또는 AWS CLI로 DNS 전파 확인

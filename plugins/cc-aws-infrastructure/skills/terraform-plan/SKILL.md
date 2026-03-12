---
name: terraform-plan
description: Terraform Plan 실행 및 변경사항 분석
---

# Terraform Plan 실행 및 분석

Terraform plan을 실행하여 인프라 변경사항을 미리 확인합니다. Lambda ZIP 파일 누락 문제를 자동으로 해결합니다.

## 트리거

- Terraform 코드 변경 후 plan 확인
- 인프라 변경 영향도 분석
- `-target` 옵션으로 특정 리소스만 plan

## Lambda ZIP Placeholder 자동 처리

### 문제

`filebase64sha256()` 함수는 `-target` 옵션과 관계없이 **모든 리소스의 표현식을 평가**합니다.
Lambda ZIP 파일은 CI에서만 빌드되므로 로컬에서 plan 실행 시 파일 누락 에러가 발생합니다.

### 해결

모듈 내부의 `${path.module}/../../../lambda/` 경로를 분석하여 올바른 위치에 placeholder ZIP을 생성합니다.

```bash
# 모듈 기준 상대 경로 해석
# modules/pdf_processing/../../../lambda/python/ → deploy/aws/lambda/python/
# terraform 실행 디렉토리 기준이 아닌 모듈 파일 기준으로 해석됨
```

> Placeholder ZIP 생성 스크립트는 `lambda-management/SKILL.md`의 "로컬 Placeholder 생성" 참조

### ZIP 파일 경로 매핑

| 모듈 | 경로 (모듈 기준) | 실제 경로 (deploy/aws/ 기준) |
|------|-----------------|---------------------------|
| pdf_processing | `${path.module}/../../../lambda/python/pdf_router/build/pdf-router.zip` | `lambda/python/pdf_router/build/pdf-router.zip` |
| pdf_processing | `${path.module}/../../../lambda/python/pdf_processor/build/pdf-processor.zip` | `lambda/python/pdf_processor/build/pdf-processor.zip` |
| pdf_processing | `${path.module}/../../../lambda/python/pdf_page_processor/build/pdf-page-processor.zip` | `lambda/python/pdf_page_processor/build/pdf-page-processor.zip` |
| pdf_processing | `${path.module}/../../../lambda/python/pdf_aggregator/build/pdf-aggregator.zip` | `lambda/python/pdf_aggregator/build/pdf-aggregator.zip` |
| pdf_processing | `${path.module}/../../../lambda/python/pdf_prepare_batches/build/pdf-prepare-batches.zip` | `lambda/python/pdf_prepare_batches/build/pdf-prepare-batches.zip` |
| pdf_processing | `${path.module}/../../../lambda/python/layers/pymupdf/build/x86_64/pymupdf-layer.zip` | `lambda/python/layers/pymupdf/build/x86_64/pymupdf-layer.zip` |
| batch_processing | `${path.module}/../../../lambda/python/book_batch_processor/build/book-batch-processor.zip` | `lambda/python/book_batch_processor/build/book-batch-processor.zip` |
| message | `abspath(var.push_forwarder_lambda_path)` | `lambda/dart/sqs_to_sns/build/x86_64/sqs_to_sns.zip` |
| message | `abspath(var.fcm_topic_manager_lambda_path)` | `lambda/go/fcm_topic_manager/build/x86_64/fcm_topic_manager.zip` |

### fileexists() 체크 여부

| 모듈 | fileexists() | 비고 |
|------|-------------|------|
| message | ✅ | 파일 없으면 `source_code_hash = null` |
| batch_processing | ✅ | `batch_processor_zip_exists` 로컬 변수 |
| pdf_processing | ❌ (lambda.tf에서 직접 호출) | **무조건 파일 필요** |

## Plan 실행 패턴

### 특정 리소스만 Plan

```bash
# 모듈명 확인 (main.tf의 module 블록 이름)
# production_env, staging_env, development_env (NOT production, staging 등)

terraform plan \
  -target='module.production_env[0].aws_route53_record.deeplink' \
  -target='module.staging_env[0].aws_route53_record.deeplink'
```

### Workspace 전환

```bash
# 현재 workspace 확인
terraform workspace list

# workspace 전환 (production, staging, default)
terraform workspace select production
```

> **주의**: 이 프로젝트는 workspace + `enable_*_server` 플래그 조합으로 환경을 관리합니다. 각 workspace 내에서 feature flag로 환경별 리소스를 조건부 생성합니다.

## 체크리스트

- [ ] Lambda ZIP placeholder 생성 (deploy/aws/lambda/ 하위)
- [ ] `terraform init` 성공 확인
- [ ] `-target` 옵션으로 영향 범위 제한
- [ ] plan 결과에서 `destroy` 리소스 없는지 확인
- [ ] 변경 예정 리소스 수 확인

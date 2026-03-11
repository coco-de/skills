# Lambda 함수 관리

Lambda 함수 배포, 환경 변수 관리, Step Functions 연동을 다룹니다.

## 트리거

- Lambda 함수 배포/업데이트
- 환경 변수 변경
- Lambda ZIP 빌드
- Step Functions 워크플로우 관리

## Lambda 함수 목록

### Push Notifications (Dart Runtime)

| 함수 | 런타임 | 메모리 | 타임아웃 | 용도 |
|------|--------|--------|---------|------|
| push-forwarder | provided.al2 (Dart) | 256MB | 60s | SQS → SNS/FCM 전달 |

### FCM Topic Manager (Go Runtime)

| 함수 | 런타임 | 메모리 | 타임아웃 | 용도 |
|------|--------|--------|---------|------|
| fcm-topic-manager | provided.al2 (Go) | 256MB | 30s | FCM 토픽 구독 관리 |

### PDF Processing (Python Runtime)

| 함수 | 런타임 | 용도 |
|------|--------|------|
| pdf-router | python3.11 | PDF 처리 라우팅 (Step Functions 진입점) |
| pdf-processor | python3.11 | PDF 페이지 처리 (PyMuPDF) |
| pdf-page-processor | python3.11 | 개별 페이지 처리 |
| pdf-aggregator | python3.11 | 결과 집계 |
| pdf-prepare-batches | python3.11 | 배치 준비 |

### Batch Processing (Python Runtime)

| 함수 | 런타임 | 용도 |
|------|--------|------|
| book-batch-processor | python3.11 | CSV 도서 일괄 업로드 처리 |

## Lambda ZIP 빌드

Lambda ZIP 파일은 **CI 파이프라인에서만 빌드**됩니다. 로컬에서는 placeholder ZIP을 사용합니다.

### ZIP 파일 위치 (CI 빌드 후)

```
deploy/aws/lambda/
├── dart/sqs_to_sns/build/x86_64/sqs_to_sns.zip
├── go/fcm_topic_manager/build/x86_64/fcm_topic_manager.zip
└── python/
    ├── pdf_router/build/pdf-router.zip
    ├── pdf_processor/build/pdf-processor.zip
    ├── pdf_page_processor/build/pdf-page-processor.zip
    ├── pdf_aggregator/build/pdf-aggregator.zip
    ├── pdf_prepare_batches/build/pdf-prepare-batches.zip
    ├── book_batch_processor/build/book-batch-processor.zip
    └── layers/pymupdf/build/x86_64/pymupdf-layer.zip
```

### 로컬 Placeholder 생성

```bash
cd deploy/aws/
for zip_file in \
  lambda/python/pdf_router/build/pdf-router.zip \
  lambda/python/pdf_processor/build/pdf-processor.zip \
  lambda/python/pdf_page_processor/build/pdf-page-processor.zip \
  lambda/python/pdf_aggregator/build/pdf-aggregator.zip \
  lambda/python/pdf_prepare_batches/build/pdf-prepare-batches.zip \
  lambda/python/book_batch_processor/build/book-batch-processor.zip \
  lambda/python/layers/pymupdf/build/x86_64/pymupdf-layer.zip \
  lambda/dart/sqs_to_sns/build/x86_64/sqs_to_sns.zip \
  lambda/go/fcm_topic_manager/build/x86_64/fcm_topic_manager.zip; do
  mkdir -p "$(dirname "$zip_file")"
  echo "placeholder" > /tmp/_placeholder && zip -j "$zip_file" /tmp/_placeholder 2>/dev/null
done
```

## Terraform 모듈 구조

### Message 모듈 (Push + FCM)

```
modules/message/
├── main.tf              # Locals, zip path resolution
├── sqs.tf               # SQS queue + DLQ
├── sns.tf               # SNS topic (FCM/APNS)
├── lambda-push-forwarder.tf    # Dart Lambda
├── lambda-fcm-topic-manager.tf # Go Lambda + API Gateway
├── iam.tf               # Lambda execution roles
├── monitoring.tf        # CloudWatch alarms
├── variables.tf
└── outputs.tf
```

### PDF Processing 모듈

```
modules/pdf_processing/
├── main.tf              # Locals, Lambda Layer (PyMuPDF)
├── lambda.tf            # 5 Lambda functions
├── step-functions.tf    # Step Functions state machine
├── iam.tf               # Lambda execution roles
├── variables.tf
└── outputs.tf
```

## Feature Toggle

Lambda 모듈은 feature flag로 활성화/비활성화:

```hcl
# config.auto.tfvars
enable_push_notifications = true
enable_fcm_topic_manager  = true
enable_pdf_processing     = true
enable_batch_processing   = true
```

## 체크리스트

- [ ] Lambda ZIP 파일 경로 확인 (모듈 기준 상대 경로)
- [ ] fileexists() 체크 여부 확인 (pdf_processing은 미체크)
- [ ] 환경 변수 설정 확인 (Firebase service account 등)
- [ ] IAM 역할 권한 확인
- [ ] CloudWatch 로그 그룹 생성 확인
- [ ] DLQ 설정 확인 (실패 메시지 처리)

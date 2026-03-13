---
title: 백엔드 & 인프라
description: Serverpod 기초/심화, API·DB 설계, AWS 인프라, ClickHouse BI 분석 플러그인
---

# 백엔드 & 인프라

## cc-serverpod

**Serverpod 기초** — 모델·엔드포인트 생성, 마이그레이션을 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 1개 (serverpod) |
| Commands | 3개 (endpoint, model, merge-migrations) |

### 주요 커맨드

```
/serverpod:endpoint          # Endpoint 생성
/serverpod:model             # .spy.yaml 모델 파일 생성
/serverpod:merge-migrations  # Migration 병합
```

### 설치

```
claude plugins install coco-de/skills/plugins/cc-serverpod
```

> [상세 페이지 보기 →](/plugins/cc-serverpod/)

---

## cc-backend

**Serverpod 백엔드 심화** — ORM, 인증, 캐싱, 테스팅, API 설계, 아키텍처 패턴을 다룹니다. cc-serverpod가 모델/엔드포인트/마이그레이션 생성을 담당한다면, cc-backend는 심화 패턴과 아키텍처를 제공합니다.

| 항목 | 내용 |
|------|------|
| Skills | 7개 (database, auth, caching, testing, logging, api-design, architecture) |
| Agents | 2개 (backend-architect, tdd-orchestrator) |
| Rules | 1개 (backend-conventions) |

### 스킬 상세

| 스킬 | 설명 |
|------|------|
| database | Serverpod ORM 심화 — 필터, 관계, 트랜잭션, Row 잠금 |
| auth | 인증 모듈 — IDP, JWT, 서버사이드 세션, Flutter UI |
| caching | 캐싱 — Local, Redis, CacheMissHandler |
| testing | 테스팅 & TDD — withServerpod, 롤백, 스트림 |
| logging | 로깅 & 세션 생명주기 |
| api-design | API 설계 원칙 — REST, 페이지네이션, 에러 처리 |
| architecture | 아키텍처 패턴 — Clean Architecture, DDD for Serverpod |

### 설치

```
claude plugins install coco-de/skills/plugins/cc-backend
```

> [상세 페이지 보기 →](/plugins/cc-backend/)

---

## cc-uiux-backend

**Serverpod API·DB 설계 템플릿** — Serverpod 전용 API 및 데이터베이스 설계를 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 2개 (api-design, database-design) |

### 설치

```
claude plugins install coco-de/skills/plugins/cc-uiux-backend
```

> [상세 페이지 보기 →](/plugins/cc-uiux-backend/)

---

## cc-aws-infrastructure

**AWS 인프라 관리** — Terraform, Route53, RDS, Lambda, CloudFront, CodeDeploy를 활용한 Serverpod 백엔드 인프라 운영을 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 5개 (terraform-plan, terraform-apply, dns-management, rds-operations, lambda-management) |

### 주요 커맨드

```
/terraform:plan              # Terraform Plan 실행
/terraform:apply             # Terraform Apply 실행
/dns:manage                  # Route53 DNS 관리
/rds:operate                 # RDS 운영
/lambda:manage               # Lambda 관리
```

### 설치

```
claude plugins install coco-de/skills/plugins/cc-aws-infrastructure
```

> [상세 페이지 보기 →](/plugins/cc-aws-infrastructure/)

---

## cc-clickhouse

**ClickHouse BI 분석** — 쿼리 작성, 테이블 설계, 분석 대시보드를 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 1개 (clickhouse) |
| 기능 | 쿼리 작성, 테이블 설계, 분석 대시보드 |

### 설치

```
claude plugins install coco-de/skills/plugins/cc-clickhouse
```

> [상세 페이지 보기 →](/plugins/cc-clickhouse/)

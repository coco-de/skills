---
title: 백엔드 & 분석
description: Serverpod 백엔드 및 ClickHouse BI 분석 플러그인
---

# 백엔드 & 분석

## cc-serverpod

**Serverpod 백엔드** — Dart 기반 서버 프레임워크 Serverpod의 Model, Endpoint, Migration을 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 1개 (serverpod) |
| Commands | 3개 (endpoint, model, merge-migrations) |

### 주요 커맨드

```bash
/serverpod:endpoint          # Endpoint 생성
/serverpod:model             # .spy.yaml 모델 파일 생성
/serverpod:merge-migrations  # Migration 병합
```

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-serverpod
```

---

## cc-clickhouse

**ClickHouse BI 분석** — 쿼리 작성, 테이블 설계, 분석 대시보드를 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 1개 (clickhouse) |
| 기능 | 쿼리 작성, 테이블 설계, 분석 대시보드 |

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-clickhouse
```

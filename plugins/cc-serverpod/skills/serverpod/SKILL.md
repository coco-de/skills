---
name: serverpod
description: Serverpod 모델·엔드포인트 생성 및 마이그레이션
---

# Serverpod Skills

Serverpod 백엔드 관련 스킬 모음입니다.

## 스킬 목록

| 스킬 | 설명 |
|------|------|
| `/serverpod:merge-migrations` | 여러 마이그레이션을 하나로 병합 |
| `/serverpod:model` | Serverpod 모델 생성 |
| `/serverpod:endpoint` | Serverpod 엔드포인트 생성 |

## Quick Start

```bash
# 프로덕션 마이그레이션 기준으로 병합
/serverpod:merge-migrations --base 20251223123500000

# 특정 범위 마이그레이션 병합
/serverpod:merge-migrations --from 20251229134213396 --to 20260113023207235
```

## 관련 명령어

```bash
# 마이그레이션 생성
melos run backend:pod:create-migration

# 마이그레이션 적용
melos run backend:pod:run-migration

# 코드 생성
melos run backend:pod:generate
```

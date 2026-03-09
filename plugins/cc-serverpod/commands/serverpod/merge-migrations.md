---
name: serverpod:merge-migrations
description: "여러 마이그레이션을 하나로 병합 (프로덕션 배포 전 정리용)"
category: serverpod
complexity: moderate
mcp-servers: []
---

# /serverpod:merge-migrations

> **Context Framework Note**: 프로덕션 배포 전 개발 중 생성된 여러 마이그레이션을 하나로 병합합니다.

## Triggers

- 프로덕션 배포 전 마이그레이션 정리 시
- 개발 중 생성된 여러 마이그레이션을 하나로 합칠 때
- 마이그레이션 히스토리 정리 시

## Context Trigger Pattern

```bash
/serverpod:merge-migrations --base {production_migration} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `--base` | ✅ | 프로덕션 기준 마이그레이션 ID (이 ID는 보존됨) | `20251223123500000` |
| `--from` | ❌ | 병합 시작 마이그레이션 (미지정 시 base 다음 자동 탐지) | `20251229134213396` |
| `--to` | ❌ | 병합 종료 마이그레이션 (미지정 시 최신 자동 탐지) | `20260113023207235` |
| `--name` | ❌ | 병합된 마이그레이션 이름 | `consolidated_dev` |
| `--dry-run` | ❌ | 실제 변경 없이 미리보기만 | `true/false` |

> **Note**: `--base`는 항상 필수입니다. 프로덕션에 적용된 마이그레이션 ID를 지정하여 해당 마이그레이션 이후의 개발 마이그레이션만 병합합니다.

## Behavioral Flow

### Step 1: 마이그레이션 분석

```markdown
## 마이그레이션 분석

**프로덕션 기준**: {base_migration}
**병합 대상**: {count}개

| # | 마이그레이션 ID | 생성일 | 변경 테이블 |
|---|----------------|--------|------------|
| 1 | 20251229134213396 | 2025-12-29 | coupon |
| 2 | 20260112140301453 | 2026-01-12 | author |
| 3 | 20260113023207235 | 2026-01-13 | author |

**영향 테이블**: coupon, author
```

### Step 2: SQL 병합

```markdown
## SQL 병합 미리보기

### 병합 전 (개별 마이그레이션)

```sql
-- Migration 1: 20251229134213396
ALTER TABLE "coupon" ADD COLUMN "new_field" text;

-- Migration 2: 20260112140301453
ALTER TABLE "author" ADD COLUMN "memo" text;

-- Migration 3: 20260113023207235
ALTER TABLE "author" ADD COLUMN "extra" text;
```

### 병합 후 (단일 마이그레이션)

```sql
-- Migration: {new_migration_id}
BEGIN;

ALTER TABLE "coupon" ADD COLUMN "new_field" text;
ALTER TABLE "author" ADD COLUMN "memo" text;
ALTER TABLE "author" ADD COLUMN "extra" text;

-- MIGRATION VERSION FOR kobic
INSERT INTO "serverpod_migrations" ("module", "version", "timestamp")
    VALUES ('kobic', '{new_migration_id}', now())
    ON CONFLICT ("module")
    DO UPDATE SET "version" = '{new_migration_id}', "timestamp" = now();

COMMIT;
```
```

### Step 3: 사용자 확인

```markdown
## 병합 확인

⚠️ **주의사항**:
- 이 작업은 기존 마이그레이션 파일을 삭제합니다
- 로컬 개발 DB에서만 실행하세요
- 프로덕션 DB에는 기존 마이그레이션이 적용되어 있어야 합니다

**병합을 진행하시겠습니까? (Y/n)**
```

### Step 4: 병합 실행

```bash
# 1. 기존 마이그레이션 백업
mkdir -p migrations_backup
for dir in migrations/{from} migrations/{middle} migrations/{to}; do
  cp -r "$dir" migrations_backup/
done

# 2. 기존 마이그레이션 삭제
rm -rf migrations/{from}
rm -rf migrations/{middle}
rm -rf migrations/{to}

# 3. 새 마이그레이션 생성
serverpod create-migration --experimental-features=all

# 4. migration_registry.txt 업데이트
# 기존 마이그레이션 ID 제거, 새 ID 추가
```

### Step 5: 검증

```markdown
## 병합 완료

✅ 기존 마이그레이션 백업: `migrations_backup/`
✅ 새 마이그레이션 생성: `{new_migration_id}`
✅ migration_registry.txt 업데이트

### 다음 단계

1. **로컬 DB 리셋** (선택):
   ```bash
   # 로컬 DB를 처음부터 다시 생성
   melos run backend:pod:run-migration
   ```

2. **변경사항 커밋**:
   ```bash
   git add backend/kobic_server/migrations/
   git commit -m "chore(migration): 🗃️ 마이그레이션 병합 ({from}~{to} → {new_id})"
   ```

### 백업 위치
기존 마이그레이션은 `migrations_backup/`에 보관됨
```

## Output Files

```
backend/kobic_server/
├── migrations/
│   ├── {base_migration}/           # 프로덕션 (유지)
│   ├── {new_migration}/            # 새로 생성된 병합 마이그레이션
│   │   ├── definition.json
│   │   ├── definition.sql
│   │   ├── definition_project.json
│   │   ├── migration.json
│   │   └── migration.sql
│   └── migration_registry.txt      # 업데이트됨
├── migrations_backup/              # 백업 (삭제 가능)
│   ├── {old_migration_1}/
│   ├── {old_migration_2}/
│   └── ...
```

## 수동 병합 가이드 (스크립트 대신)

스킬이 자동 실행되지 않는 경우, 다음 단계를 수동으로 진행:

### 1. 현재 상태 확인

```bash
# migration_registry.txt 확인
cat backend/kobic_server/migrations/migration_registry.txt

# 프로덕션 이후 마이그레이션 확인
ls -la backend/kobic_server/migrations/ | grep "2026"
```

### 2. 기존 마이그레이션 백업 및 삭제

```bash
cd backend/kobic_server

# 백업
mkdir -p migrations_backup
mv migrations/20251229134213396 migrations_backup/
mv migrations/20260112140301453 migrations_backup/
mv migrations/20260113023207235 migrations_backup/

# migration_registry.txt에서 해당 라인 삭제
# 수동으로 편집하여 삭제할 마이그레이션 ID 제거
```

### 3. 새 마이그레이션 생성

```bash
# 코드 생성 (현재 모델 기준)
melos run backend:pod:generate

# 새 마이그레이션 생성
melos run backend:pod:create-migration
```

### 4. 검증

```bash
# 새 마이그레이션 확인
ls -la backend/kobic_server/migrations/ | tail -5

# migration_registry.txt 확인
tail backend/kobic_server/migrations/migration_registry.txt
```

## Examples

### 기본 사용 (프로덕션 기준)

`--base` 이후의 모든 마이그레이션을 자동 탐지하여 병합:

```bash
/serverpod:merge-migrations --base 20251223123500000
```

### 범위 지정

`--base` 기준으로 특정 범위만 병합 (base 이후 ~ to까지):

```bash
/serverpod:merge-migrations \
  --base 20251223123500000 \
  --from 20251229134213396 \
  --to 20260113023207235
```

### Dry-run (미리보기)

실제 변경 없이 병합될 내용만 확인:

```bash
/serverpod:merge-migrations --base 20251223123500000 --dry-run
```

## 핵심 규칙

1. **프로덕션 기준**: 프로덕션에 적용된 마이그레이션은 건드리지 않음
2. **백업 필수**: 삭제 전 반드시 백업
3. **로컬 전용**: 프로덕션 DB에서는 절대 실행 금지
4. **순서 유지**: 마이그레이션 순서는 타임스탬프로 자동 관리
5. **검증 필수**: 병합 후 `melos run backend:pod:generate`로 검증

## 주의사항

⚠️ **프로덕션 DB 주의**:
- 프로덕션 DB에는 기존 마이그레이션이 이미 적용되어 있음
- 병합된 마이그레이션은 새로운 환경에서만 사용
- 기존 프로덕션은 영향 없음 (serverpod_migrations 테이블 참조)

⚠️ **팀 협업 시**:
- 다른 개발자와 마이그레이션 충돌 가능
- 병합 전 팀원들과 조율 필요
- PR 머지 전 migration_registry.txt 충돌 확인

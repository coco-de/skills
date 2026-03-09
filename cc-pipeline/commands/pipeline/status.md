---
name: pipeline:status
description: "파이프라인 현황 조회"
invoke: /pipeline:status
category: pipeline
complexity: simple
---

# /pipeline:status

> 현재 프로젝트의 파이프라인 진행 상태를 조회합니다.

## Triggers

- 파이프라인 진행 상황을 확인하고 싶을 때
- 다음 스테이지를 확인할 때

## 사용법

```bash
# 현재 프로젝트 상태
/pipeline:status

# 특정 프로젝트 상태
/pipeline:status community

# 모든 프로젝트 목록
/pipeline:status --all
```

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `slug` | 아니오 | 프로젝트 슬러그 | `community` |

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--all` | `false` | 모든 프로젝트 목록 조회 |
| `--detail` | `false` | 산출물, 게이트 상세 표시 |

## 실행 흐름

1. `.pipeline/` 디렉토리에서 상태 파일(들) 조회
2. YAML 파싱하여 상태 정보 추출
3. 시각적 대시보드 출력

## 출력 형식

### 단일 프로젝트

```
📊 Pipeline: 커뮤니티 기능 (community)
   Level: 3 | Created: 2025-01-15

   ✅ Discovery    ──→  ✅ Planning    ──→  🔄 Design
   ──→  ⏳ Epic       ──→  ⏳ Development ──→  ⏳ Launch

   현재: Design (Solutioning Gate 진행 중)
   산출물: docs/discovery-community.md, docs/prd-community.md
   다음: /project:epic
```

### 상태 아이콘

| 아이콘 | 상태 |
|--------|------|
| ⏳ | pending |
| 🔄 | in-progress |
| ✅ | completed |
| ⏭️ | skipped |
| ❌ | failed |

### 모든 프로젝트 (--all)

```
📊 Pipeline Status

   community     [████████░░░░] Stage 3/6 (Design)
   auth-system   [████████████] Complete
   admin-panel   [██░░░░░░░░░░] Stage 1/6 (Discovery)
```

### 상세 모드 (--detail)

각 스테이지별:
- 시작/완료 시간
- 산출물 목록 (파일 존재 여부)
- 게이트 통과 여부 및 체크 항목
- 스킵 사유 (해당 시)

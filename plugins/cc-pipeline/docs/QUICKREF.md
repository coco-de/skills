# Quick Reference — cc-pipeline

## 커맨드 요약

| 커맨드 | 설명 |
|--------|------|
| `/project "설명"` | 전체 파이프라인 실행 |
| `/project:discover "설명"` | Stage 1: Discovery |
| `/project:plan` | Stage 2: Planning |
| `/project:design` | Stage 3: Design |
| `/project:epic` | Stage 4: Epic Creation |
| `/project:develop --epic N` | Stage 5: Development (Epic) |
| `/project:develop --issue N` | Stage 5: Development (단일 이슈) |
| `/project:launch` | Stage 6: Launch |
| `/pipeline:status` | 파이프라인 상태 조회 |

## 주요 옵션

```bash
# 전체 파이프라인
/project --level 3 "설명"           # 레벨 지정
/project --from design "설명"       # 특정 스테이지부터
/project --to epic "설명"           # 특정 스테이지까지

# Discovery
/project:discover --depth deep      # 심층 탐색
/project:discover --focus user      # 사용자 리서치 집중

# Planning
/project:plan --doc both            # PRD + Tech Spec 모두
/project:plan --bdd false           # BDD 스킵

# Design
/project:design --focus architecture # 아키텍처만

# Epic
/project:epic --sprint current      # 현재 스프린트 할당

# Development
/project:develop --epic 42          # Epic 전체
/project:develop --issue 1810       # 단일 이슈

# Status
/pipeline:status --all              # 전체 프로젝트
/pipeline:status --detail           # 상세 정보
```

## BMAD 레벨 & 스킵

| Level | 이름 | 스킵 스테이지 |
|-------|------|---------------|
| 0 | Hotfix | Discovery, Design, Epic, Launch |
| 1 | Minor | Discovery, Launch |
| 2 | Feature | 없음 |
| 3 | Major | 없음 |
| 4 | New Project | 없음 (Discovery 심층) |

## 게이트

| 게이트 | 위치 | 핵심 체크 |
|--------|------|-----------|
| Analysis | Planning → Design | 요구사항, 범위, Acceptance Criteria |
| Solutioning | Design → Epic | 아키텍처, UX |
| Planning | Epic → Development | Story 구조, 포인트 |
| Implementation | Development (Story별) | 린트, 테스트, 리뷰 |

## 산출물 경로

```
docs/discovery-{slug}.md        # Discovery
docs/prd-{slug}.md              # Planning (PRD)
docs/tech-spec-{slug}.md        # Planning (Tech Spec)
docs/bdd-{slug}.md              # Planning (BDD)
docs/architecture-{slug}.md     # Design
docs/ux-spec-{slug}.md          # Design
docs/gtm-{slug}.md              # Launch
docs/analytics-plan-{slug}.md   # Launch
.pipeline/{slug}.yaml           # 상태 파일
```

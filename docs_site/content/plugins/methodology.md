---
title: 방법론 & 워크플로우
description: BMAD 방법론, 개발 워크플로우, 코드 품질 관리 플러그인
---

# 방법론 & 워크플로우

## cc-bmad

**BMAD 방법론** (Business Method Agile Delivery) — 제품 개발 전 과정을 체계적으로 관리하는 방법론입니다.

| 항목 | 내용 |
|------|------|
| Skills | 10개 (bmad-master, analyst, architect, developer, pm, scrum-master 등) |
| Commands | 18개 |
| Personas | 7개 (analyst, architect, backend-developer, flutter-developer, pm 등) |
| Orchestrators | 2개 (bmad-orchestrator, phase-gates) |

### 주요 커맨드

```bash
/bmad:prd                    # PRD 작성
/bmad:architecture           # 아키텍처 설계
/bmad:tech-spec              # 기술 스펙 작성
/bmad:sprint-planning        # 스프린트 계획
/bmad:brainstorm             # 브레인스토밍
/bmad:create-story           # 스토리 생성
/bmad:dev-story              # 개발 스토리
```

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-bmad
```

---

## cc-workflow

**개발 워크플로우** — Issue Cycle, Bug Cycle, Session 관리, ZenHub 연동을 포함합니다.

| 항목 | 내용 |
|------|------|
| Skills | 2개 (workflow, session) |
| Agents | 2개 (sequential-workflow, mcp-debug) |
| Commands | workflow/\*, session/\*, zenhub/\*, openapi/\* |

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-workflow
```

---

## cc-code-quality

**코드 품질** — 코드리뷰, 체크리스트, 버그리포트를 체계화합니다.

| 항목 | 내용 |
|------|------|
| Skills | 3개 (code-review, checklist, bug-report) |
| Commands | 3개 |

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-code-quality
```

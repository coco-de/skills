---
title: 방법론 & 워크플로우
description: BMAD 방법론, 개발 사이클 자동화, 코드 품질, 파이프라인 오케스트레이터 플러그인
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

```
/bmad:prd                    # PRD 작성
/bmad:architecture           # 아키텍처 설계
/bmad:tech-spec              # 기술 스펙 작성
/bmad:sprint-planning        # 스프린트 계획
/bmad:brainstorm             # 브레인스토밍
/bmad:create-story           # 스토리 생성
/bmad:dev-story              # 개발 스토리
```

### 설치

```
claude plugins install coco-de/skills/plugins/cc-bmad
```

> [상세 페이지 보기 →](/plugins/cc-bmad/)

---

## cc-dev-cycle

**개발 사이클** — Issue Cycle, Bug Cycle, Session 관리, ZenHub 연동을 포함합니다.

| 항목 | 내용 |
|------|------|
| Skills | 2개 (workflow, session) |
| Agents | 2개 (sequential-workflow, mcp-debug) |
| Commands | workflow/*, session/*, zenhub/*, openapi/* |

### 설치

```
claude plugins install cc-dev-cycle@cocode-skills
```

> [상세 페이지 보기 →](/plugins/cc-dev-cycle/)

---

## cc-code-quality

**코드 품질** — 코드리뷰, 체크리스트, 버그리포트를 체계화합니다.

| 항목 | 내용 |
|------|------|
| Skills | 3개 (code-review, checklist, bug-report) |
| Commands | 3개 |

### 설치

```
claude plugins install coco-de/skills/plugins/cc-code-quality
```

> [상세 페이지 보기 →](/plugins/cc-code-quality/)

---

## cc-pipeline

**통합 프로젝트 파이프라인 오케스트레이터** — Discovery에서 Launch까지 6단계 프로젝트 라이프사이클을 관리합니다.

| 단계 | 커맨드 | 설명 |
|------|--------|------|
| 1. Discovery | `/project:discover` | 시장 조사, 사용자 리서치, 문제 정의 |
| 2. Planning | `/project:plan` | PRD 작성, 기술 요구사항, 로드맵 |
| 3. Design | `/project:design` | 아키텍처 설계, UI/UX 디자인 |
| 4. Epic | `/project:epic` | 에픽/스토리 분해, 스프린트 계획 |
| 5. Development | `/project:develop` | 구현, 코드리뷰, 테스트 |
| 6. Launch | `/project:launch` | 배포, 모니터링, 릴리스 |

### 설치

```
claude plugins install coco-de/skills/plugins/cc-pipeline
```

> [상세 페이지 보기 →](/plugins/cc-pipeline/)

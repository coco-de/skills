---
title: Methodology & Workflow
description: BMAD methodology, development workflow, and code quality plugins
---

# Methodology & Workflow

## cc-bmad

**BMAD Methodology** (Business Method Agile Delivery) — Systematically manages the entire product development lifecycle.

| Item | Count |
|------|-------|
| Skills | 10 (bmad-master, analyst, architect, developer, pm, scrum-master, etc.) |
| Commands | 18 |
| Personas | 7 (analyst, architect, backend-developer, flutter-developer, pm, etc.) |
| Orchestrators | 2 (bmad-orchestrator, phase-gates) |

### Key Commands

```bash
/bmad:prd                    # Write PRD
/bmad:architecture           # Architecture design
/bmad:tech-spec              # Technical specification
/bmad:sprint-planning        # Sprint planning
/bmad:brainstorm             # Brainstorming
/bmad:create-story           # Create story
/bmad:dev-story              # Development story
```

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-bmad
```

---

## cc-workflow

**Development Workflow** — Includes Issue Cycle, Bug Cycle, Session management, and ZenHub integration.

| Item | Count |
|------|-------|
| Skills | 2 (workflow, session) |
| Agents | 2 (sequential-workflow, mcp-debug) |
| Commands | workflow/*, session/*, zenhub/*, openapi/* |

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-workflow
```

---

## cc-code-quality

**Code Quality** — Systematizes code review, checklists, and bug reports.

| Item | Count |
|------|-------|
| Skills | 3 (code-review, checklist, bug-report) |
| Commands | 3 |

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-code-quality
```

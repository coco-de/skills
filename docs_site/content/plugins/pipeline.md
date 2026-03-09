---
title: Pipeline
description: Integrated project pipeline orchestrator — 6 stages from Discovery to Launch
---

# Pipeline

## cc-pipeline

**Integrated Project Pipeline Orchestrator** — Manages the 6-stage project lifecycle from Discovery to Launch.

### 6-Stage Pipeline

| Stage | Command | Description |
|-------|---------|-------------|
| 1. Discovery | `/project:discover` | Market research, user research, problem definition |
| 2. Planning | `/project:plan` | PRD, technical requirements, roadmap |
| 3. Design | `/project:design` | Architecture design, UI/UX design |
| 4. Epic | `/project:epic` | Epic/story breakdown, sprint planning |
| 5. Development | `/project:develop` | Implementation, code review, testing |
| 6. Launch | `/project:launch` | Deployment, monitoring, release |

### Pipeline Status

```bash
/pipeline:status             # Check current pipeline status
```

### Integrated Plugins

cc-pipeline orchestrates other plugins:

- **cc-bmad** — Methodology, gates, personas
- **cc-pm-discovery** — User research
- **cc-pm-strategy** — Product strategy
- **cc-pm-analytics** — Data analytics
- **cc-pm-gtm** — Go-to-Market
- **cc-workflow** — Workflow automation

### Artifacts

Pipeline artifacts are stored at:

```
project/
├── docs/
└── .pipeline/
    └── {slug}.yaml          # Pipeline state file
```

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-pipeline
```

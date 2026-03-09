---
title: Getting Started
description: Installation and setup guide for Cocode Skills
---

# Getting Started

## Installation

### Full Repository

Install all plugins at once:

```bash
claude plugins install coco-de/skills
```

### Individual Plugins

Install only the plugins you need:

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-bmad
claude plugins install coco-de/skills/plugins/cc-coui
claude plugins install coco-de/skills/plugins/cc-pipeline
```

## Project Setup

Maintain these items in each project's `.claude/` directory:

```
.claude/
├── settings.json
├── settings.local.json
├── rules/
│   └── project-config.md
├── plans/
├── hooks/
└── docs/
```

## Validation

Verify plugin structure:

```bash
python3 validate_plugins.py       # basic
python3 validate_plugins.py -v    # verbose
```

## Recommended Combinations

### Flutter App Development

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-coui
claude plugins install coco-de/skills/plugins/cc-i18n
claude plugins install coco-de/skills/plugins/cc-flutter-inspector
```

### Full-Stack Development

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-serverpod
claude plugins install coco-de/skills/plugins/cc-backend
claude plugins install coco-de/skills/plugins/cc-coui
claude plugins install coco-de/skills/plugins/cc-workflow
```

### PM + Development

```bash
claude plugins install coco-de/skills/plugins/cc-pipeline
claude plugins install coco-de/skills/plugins/cc-bmad
claude plugins install coco-de/skills/plugins/cc-pm-discovery
claude plugins install coco-de/skills/plugins/cc-pm-strategy
```

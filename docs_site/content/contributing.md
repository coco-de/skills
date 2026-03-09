---
title: Contributing
description: How to contribute to Cocode Skills plugins
---

# Contributing

## Plugin Structure

Each plugin lives under `plugins/` with the `cc-` prefix:

```
plugins/cc-<name>/
├── .claude-plugin/
│   └── plugin.json          # Required: plugin metadata
├── README.md                # Required: plugin description
├── skills/                  # SKILL.md, REFERENCE.md, TEMPLATES.md
├── commands/                # Slash commands (.md)
├── agents/                  # Agent definitions (.md)
├── rules/                   # Rules (.md)
└── references/              # Reference documents
```

## plugin.json Format

```json
{
  "name": "cc-<name>",
  "version": "1.0.0",
  "description": "Plugin description",
  "skills": ["skills/"],
  "commands": ["commands/"],
  "agents": ["agents/"],
  "rules": ["rules/"]
}
```

## File Formats

### Skill Files

- `SKILL.md` — Skill definition (triggers, behavior, output)
- `REFERENCE.md` — Reference docs (patterns, API, rules)
- `TEMPLATES.md` — Code/document templates

### Command Files

Each `.md` file defines one slash command. File path becomes the command name:

```
commands/workflow/issue-cycle.md → /workflow:issue-cycle
```

## Contribution Guidelines

1. **New plugin** — `cc-` prefix required, include `plugin.json`
2. **Modify existing** — Work within the plugin directory
3. **Validate** — Run `python3 validate_plugins.py`
4. **PR rules** — Separate commits per changed plugin

<Warning>
  New plugins must also be registered in marketplace.json.
</Warning>

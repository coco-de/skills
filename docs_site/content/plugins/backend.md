---
title: Backend & Analytics
description: Serverpod backend, advanced backend patterns, and ClickHouse BI analytics plugins
---

# Backend & Analytics

## cc-serverpod

**Serverpod Backend** — Supports Model, Endpoint, and Migration generation for the Dart-based Serverpod framework.

| Item | Count |
|------|-------|
| Skills | 1 (serverpod) |
| Commands | 3 (endpoint, model, merge-migrations) |

### Key Commands

```bash
/serverpod:endpoint          # Generate endpoint
/serverpod:model             # Generate .spy.yaml model
/serverpod:merge-migrations  # Merge migrations
```

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-serverpod
```

---

## cc-backend

**Advanced Serverpod Backend** — Deep patterns for ORM, Auth, Caching, Testing, API Design, and Architecture. Complements cc-serverpod with architectural guidance.

| Item | Count |
|------|-------|
| Skills | 7 (database, auth, caching, testing, logging, api-design, architecture) |
| Agents | 2 (backend-architect, tdd-orchestrator) |
| Rules | 1 (backend-conventions) |

### Skills Overview

| Skill | Description |
|-------|-------------|
| database | Serverpod ORM deep dive — filters, relations, transactions, row locking |
| auth | Auth module — IDP, JWT, server-side sessions, Flutter UI |
| caching | Caching — Local, Redis, CacheMissHandler |
| testing | Testing & TDD — withServerpod, rollback, streams |
| logging | Logging & session lifecycle |
| api-design | API design principles — REST, pagination, error handling |
| architecture | Architecture patterns — Clean Architecture, DDD for Serverpod |

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-backend
```

---

## cc-clickhouse

**ClickHouse BI Analytics** — Supports query writing, table design, and analytics dashboards.

| Item | Count |
|------|-------|
| Skills | 1 (clickhouse) |

### Install

```bash
claude plugins install coco-de/skills/plugins/cc-clickhouse
```

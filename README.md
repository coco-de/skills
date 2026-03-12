<p align="center">
  <img src="https://raw.githubusercontent.com/coco-de/skills/main/docs_site/web/images/logo.svg" alt="Cocode Skills" width="120" />
</p>

<h1 align="center">Cocode Skills</h1>

<p align="center">
  Dart 풀스택 개발을 위한 Claude Code 스킬, 에이전트, 커맨드 모음
</p>

<p align="center">
  <a href="https://github.com/coco-de/skills/stargazers"><img src="https://img.shields.io/github/stars/coco-de/skills?style=flat&color=6366f1" alt="Stars" /></a>
  <a href="https://github.com/coco-de/skills/blob/main/LICENSE"><img src="https://img.shields.io/github/license/coco-de/skills?style=flat&color=6366f1" alt="License" /></a>
  <a href="https://github.com/coco-de/skills/commits/main"><img src="https://img.shields.io/github/last-commit/coco-de/skills?style=flat&color=6366f1" alt="Last Commit" /></a>
  <img src="https://img.shields.io/badge/Dart-Flutter-02569B?style=flat&logo=dart" alt="Dart & Flutter" />
  <img src="https://img.shields.io/badge/Claude-Code-6366f1?style=flat" alt="Claude Code" />
</p>

---

## What's Included

```
coco-de/skills
├── 24 Plugins
├── 22 Agents
├── 100 Commands
└── 87 Skills
```

Flutter + Serverpod + CoUI 기반의 Dart 풀스택 프로젝트를 위한 Claude Code 플러그인 컬렉션입니다. 방법론, 개발, 테스트, 배포까지 전체 개발 라이프사이클을 커버합니다.

---

## Quick Start

### 전체 설치

```bash
claude plugins install coco-de/skills
```

### 개별 플러그인 설치

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-coui
claude plugins install coco-de/skills/plugins/cc-serverpod
```

### 추천 조합

| 용도 | 플러그인 |
|------|---------|
| Flutter 앱 개발 | `cc-flutter-dev` + `cc-coui` + `cc-i18n` |
| 풀스택 개발 | `cc-flutter-dev` + `cc-serverpod` + `cc-coui` |
| PM 워크플로우 | `cc-bmad` + `cc-pm-discovery` + `cc-pm-strategy` + `cc-pm-gtm` |
| UI/UX 전문 | `cc-uiux-design` + `cc-uiux-frontend` + `cc-uiux-accessibility` |
| 전체 파이프라인 | `cc-pipeline` (기존 플러그인 오케스트레이션) |

---

## 플러그인 카테고리

### 방법론 & 워크플로우

| 플러그인 | 설명 | Skills | Commands | Agents |
|---------|------|--------|----------|--------|
| `cc-bmad` | BMAD 방법론 (10 skills, 18 commands) | 11 | 22 | — |
| `cc-workflow` | 개발 워크플로우 (Issue/Bug Cycle, Session, ZenHub) | 2 | 7 | 2 |
| `cc-code-quality` | 코드리뷰, 체크리스트, 버그리포트 | 3 | 3 | — |
| `cc-pipeline` | 6단계 파이프라인 오케스트레이터 | 1 | 3 | — |

### Flutter & 프론트엔드

| 플러그인 | 설명 | Skills | Commands | Agents |
|---------|------|--------|----------|--------|
| `cc-coui` | CoUI 컴포넌트 라이브러리 (26개 컴포넌트) | 26 | — | — |
| `cc-flutter-dev` | Flutter 개발 핵심 (UI 패턴, Feature 생성, BLoC, 테스트) | 2 | 7 | 6 |
| `cc-flutter-inspector` | Flutter Inspector 디버깅 (Master + 9 전문) | 1 | 2 | 10 |
| `cc-i18n` | 국제화 (Slang 기반) | 1 | 1 | 1 |
| `cc-deeplink` | Deep Link & Universal Links (AASA, GoRouter, 도메인 마이그레이션) | 4 | — | — |
| `cc-uiux-frontend` | 프론트엔드 패턴 가이드 (Clean Architecture, Jaspr Web, 반응형) | 3 | — | — |

### 백엔드 & 인프라

| 플러그인 | 설명 | Skills | Commands | Agents |
|---------|------|--------|----------|--------|
| `cc-serverpod` | Serverpod 기초 — 모델·엔드포인트 생성, 마이그레이션 | 1 | 2 | 1 |
| `cc-backend` | Serverpod 심화 패턴 (ORM, Auth, Caching, TDD, API Design) | 7 | — | 2 |
| `cc-uiux-backend` | Serverpod API·DB 설계 템플릿 | 2 | — | — |
| `cc-aws-infrastructure` | AWS 인프라 관리 (Terraform, Route53, RDS, Lambda, CloudFront) | 5 | — | — |

### PM (Product Management)

| 플러그인 | 설명 | Skills | Commands | Agents |
|---------|------|--------|----------|--------|
| `cc-pm-discovery` | 제품 발견 (인터뷰, 실험, 가정 테스트) | 3 | — | — |
| `cc-pm-strategy` | 제품 전략 (비전, 비즈니스 모델) | 3 | — | — |
| `cc-pm-analytics` | 데이터 분석 (SQL, 코호트, A/B 테스트) | 3 | — | — |
| `cc-pm-gtm` | Go-to-Market | 3 | — | — |

### 품질 & 운영

| 플러그인 | 설명 | Skills | Commands | Agents |
|---------|------|--------|----------|--------|
| `cc-uiux-design` | UI/UX 디자인 (CoUI 토큰, DaisyUI 테마) | 2 | — | — |
| `cc-uiux-accessibility` | 접근성 (Flutter + Jaspr Web) | 2 | — | — |
| `cc-uiux-testing` | 테스팅 (Dart/Flutter) | 4 | — | — |
| `cc-uiux-security` | 보안 (API + 앱) | 3 | — | — |
| `cc-uiux-devops` | DevOps (배포 파이프라인) | 3 | — | — |

### 분석

| 플러그인 | 설명 | Skills | Commands | Agents |
|---------|------|--------|----------|--------|
| `cc-clickhouse` | ClickHouse BI 분석 | 1 | — | — |

---

## 기술 스택

| 영역 | 기술 |
|------|------|
| **Frontend** | Flutter (Mobile/Desktop) + Jaspr (Web) |
| **Backend** | Serverpod |
| **UI Library** | CoUI (크로스플랫폼 컴포넌트) |
| **Architecture** | Clean Architecture + BLoC 패턴 |
| **Infrastructure** | AWS (Terraform, Route53, RDS, Lambda) |
| **BI/Analytics** | ClickHouse |
| **Methodology** | BMAD |

---

## Repository Structure

```
skills/
├── plugins/
│   ├── cc-bmad/           # BMAD 방법론
│   ├── cc-clickhouse/     # ClickHouse BI
│   ├── cc-code-quality/   # 코드 품질
│   ├── cc-coui/           # CoUI 컴포넌트
│   ├── cc-flutter-dev/    # Flutter 개발
│   ├── cc-flutter-inspector/ # Flutter 디버깅
│   ├── cc-i18n/           # 국제화
│   ├── cc-deeplink/       # Deep Link & Universal Links
│   ├── cc-pipeline/       # 파이프라인 오케스트레이터
│   ├── cc-pm-*/           # PM 플러그인 (4개)
│   ├── cc-serverpod/      # Serverpod 백엔드
│   ├── cc-backend/        # Serverpod 백엔드 심화
│   ├── cc-aws-infrastructure/ # AWS 인프라 관리
│   ├── cc-uiux-*/         # UI/UX 플러그인 (7개)
│   └── cc-workflow/       # 워크플로우
├── docs_site/             # 문서 사이트 (Jaspr)
└── validate_plugins.py    # 플러그인 검증 스크립트
```

---

## 프로젝트 로컬 유지 항목

각 프로젝트의 `.claude/`에 유지해야 할 항목:

- `settings.json`, `settings.local.json`
- `rules/project-config.md` (프로젝트별 구조/설정)
- 프로젝트 고유 rules
- `plans/`, `hooks/`, `docs/`

---

## 검증

```bash
python3 validate_plugins.py
```

---

## Documentation

📖 **문서 사이트**: [skills.cocode.im](https://skills.cocode.im/)

---

## Contributing

1. Fork → Branch → PR
2. `python3 validate_plugins.py` 검증 통과 필수
3. 플러그인 구조: `plugins/<name>/{skills,commands,agents}/`

## License

[MIT](LICENSE)

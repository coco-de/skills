---
title: 시작하기
description: Cocode Skills 설치 및 설정 가이드
---

# 시작하기

## 설치

### 전체 레포지토리 설치

모든 플러그인을 한 번에 설치합니다:

```bash
claude plugins install coco-de/skills
```

### 개별 플러그인 설치

필요한 플러그인만 선택적으로 설치할 수 있습니다:

```bash
# Flutter 개발 핵심
claude plugins install coco-de/skills/plugins/cc-flutter-dev

# BMAD 방법론
claude plugins install coco-de/skills/plugins/cc-bmad

# CoUI 컴포넌트
claude plugins install coco-de/skills/plugins/cc-coui

# 프로젝트 파이프라인
claude plugins install coco-de/skills/plugins/cc-pipeline
```

## 프로젝트 설정

각 프로젝트의 `.claude/` 디렉토리에 다음 항목을 유지해야 합니다:

```
.claude/
├── settings.json
├── settings.local.json
├── rules/
│   └── project-config.md      # 프로젝트별 구조/설정
├── plans/
├── hooks/
└── docs/
```

### project-config.md 예시

```markdown
# 프로젝트 설정
- 프로젝트명: MyApp
- 아키텍처: Clean Architecture + BLoC
- UI 라이브러리: CoUI
- 백엔드: Serverpod
```

## 검증

플러그인 구조가 올바른지 검증하려면:

```bash
python3 validate_plugins.py       # 기본 검증
python3 validate_plugins.py -v    # 상세 출력
```

## 추천 설치 조합

### Flutter 앱 개발

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-coui
claude plugins install coco-de/skills/plugins/cc-i18n
claude plugins install coco-de/skills/plugins/cc-flutter-inspector
```

### 풀스택 개발

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-serverpod
claude plugins install coco-de/skills/plugins/cc-coui
claude plugins install coco-de/skills/plugins/cc-workflow
```

### PM + 개발 통합

```bash
claude plugins install coco-de/skills/plugins/cc-pipeline
claude plugins install coco-de/skills/plugins/cc-bmad
claude plugins install coco-de/skills/plugins/cc-pm-discovery
claude plugins install coco-de/skills/plugins/cc-pm-strategy
```

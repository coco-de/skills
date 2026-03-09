---
title: 시작하기
description: Cocode Skills 설치 및 설정 가이드
---

# 시작하기

## 사전 준비

이 레포지토리는 **Private**입니다. 설치 전에 GitHub 접근 권한이 설정되어 있어야 합니다.

### 1. GitHub 접근 권한 확인

`coco-de/skills` 레포지토리에 대한 읽기 권한이 필요합니다. 팀 관리자에게 초대를 요청하세요.

### 2. GitHub CLI 인증 (권장)

Claude Code는 내부적으로 `gh` CLI를 사용하여 플러그인을 설치합니다. 인증되어 있지 않다면 먼저 설정합니다:

```bash
# GitHub CLI 설치 (macOS)
brew install gh

# 인증 — 브라우저에서 로그인
gh auth login

# 인증 확인
gh auth status
```

<Warning>
  `gh auth login` 시 **HTTPS** 프로토콜을 선택하고, 인증 방식은 **Login with a web browser**를 권장합니다.
</Warning>

### 3. 접근 권한 테스트

```bash
# Private 레포 접근 가능 여부 확인
gh repo view coco-de/skills --json name
```

정상이면 `{"name":"skills"}`가 출력됩니다. 권한 오류가 발생하면 팀 관리자에게 문의하세요.

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

### 설치 확인

```bash
# 설치된 플러그인 목록 확인
claude plugins list
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
claude plugins install coco-de/skills/plugins/cc-backend
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

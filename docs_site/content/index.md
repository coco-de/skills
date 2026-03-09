---
title: Cocode Skills
description: Cocode 팀 통합 스킬 레포지토리 — Dart 풀스택 개발을 위한 Claude Code 플러그인 모음
---

# Cocode Skills

Cocode 팀 통합 스킬 레포지토리입니다. **Dart 풀스택** 개발 환경에 최적화된 **22개 플러그인**을 제공합니다.

## 기술 스택

| 영역 | 기술 |
|------|------|
| **Frontend** | Flutter (Mobile/Desktop) + Jaspr (Web) |
| **Backend** | Serverpod |
| **UI Library** | CoUI (크로스플랫폼 컴포넌트) |
| **Architecture** | Clean Architecture + BLoC 패턴 |

## 플러그인 카테고리

| 카테고리 | 플러그인 수 | 설명 |
|----------|:---------:|------|
| [방법론 & 워크플로우](/plugins/methodology) | 3 | BMAD, 워크플로우, 코드 품질 |
| [제품 관리](/plugins/product-management) | 4 | Discovery, Strategy, Analytics, GTM |
| [Flutter 개발](/plugins/flutter) | 4 | CoUI, 핵심 개발, Inspector, i18n |
| [백엔드 & 분석](/plugins/backend) | 3 | Serverpod, 백엔드 심화, ClickHouse |
| [UI/UX 엔지니어링](/plugins/uiux) | 7 | 디자인, 접근성, 프론트엔드, 백엔드, 테스팅, DevOps, 보안 |
| [파이프라인](/plugins/pipeline) | 1 | 통합 오케스트레이터 |

## 빠른 시작

<Warning>
  Private 레포입니다. 설치 전에 `gh auth login`으로 GitHub 인증이 필요합니다.
</Warning>

전체 설치:

```bash
# GitHub CLI 인증 (최초 1회)
gh auth login

# 전체 플러그인 설치
claude plugins install coco-de/skills
```

개별 플러그인 설치:

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
claude plugins install coco-de/skills/plugins/cc-bmad
```

<Info>
  자세한 설치 방법은 [시작하기](/getting-started) 페이지를 참고하세요.
</Info>

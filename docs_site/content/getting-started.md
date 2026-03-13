---
title: 시작하기
description: Skills 설치 및 설정 가이드
---

# 시작하기

## Claude Code 플러그인이란?

Claude Code 플러그인은 **Skills**, **Rules**, **Agents**, **Commands**로 구성된 확장 패키지입니다. 플러그인을 설치하면 Claude Code가 팀의 개발 컨벤션, 아키텍처 패턴, 워크플로우를 자동으로 따릅니다.

| 구성 요소 | 설명 | 예시 |
|-----------|------|------|
| **Skills** | 슬래시 커맨드로 호출하는 전문 기능 | `/flutter-ui`, `/code-review` |
| **Rules** | 항상 적용되는 코딩 규칙 | 네이밍 컨벤션, 아키텍처 규칙 |
| **Agents** | 복잡한 작업을 자율적으로 수행하는 에이전트 | `backend-architect`, `tdd-orchestrator` |
| **Commands** | 특정 작업을 실행하는 명령어 | `/prd`, `/sprint-planning` |

### 플러그인 구조

```
plugins/cc-flutter-dev/
├── .claude-plugin/
│   └── plugin.json          # 플러그인 메타데이터
├── skills/                   # 슬래시 커맨드로 호출 가능한 스킬
│   ├── flutter-ui/
│   │   └── SKILL.md
│   └── workflow/
│       └── SKILL.md
├── agents/                   # 자동 활성화되는 에이전트
│   └── feature-agent.md
└── rules/                    # 항상 적용되는 규칙
    └── conventions.md
```

## 사전 준비

이 레포지토리는 **Private**입니다. 설치 전에 GitHub 접근 권한이 설정되어 있어야 합니다.

### 1. Claude Code 설치 확인

Claude Code가 설치되어 있어야 합니다. 터미널에서 확인:

```
claude --version
```

설치되어 있지 않다면 [Claude Code 공식 문서](https://docs.anthropic.com/en/docs/claude-code)를 참고하세요.

### 2. GitHub 접근 권한 확인

`coco-de/skills` 레포지토리에 대한 읽기 권한이 필요합니다. 팀 관리자에게 초대를 요청하세요.

### 3. GitHub CLI 인증 (권장)

Claude Code는 내부적으로 `gh` CLI를 사용하여 플러그인을 설치합니다. 인증되어 있지 않다면 먼저 설정합니다:

```
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

### 4. 접근 권한 테스트

```
# Private 레포 접근 가능 여부 확인
gh repo view coco-de/skills --json name
```

정상이면 `{"name":"skills"}`가 출력됩니다. 권한 오류가 발생하면 팀 관리자에게 문의하세요.

## 설치

### Step 1: 마켓플레이스 등록

먼저 `coco-de/skills` 레포지토리를 마켓플레이스로 등록합니다:

```
claude plugins marketplace add coco-de/skills
```

<Info>
  마켓플레이스는 한 번만 등록하면 됩니다. 등록 후 `claude plugins marketplace list`로 확인할 수 있습니다.
</Info>

### Step 2: 플러그인 설치

마켓플레이스 등록 후 개별 플러그인을 설치합니다:

```
# 개별 플러그인 설치 (플러그인명@마켓플레이스명)
claude plugins install cc-flutter-dev@cocode-skills
claude plugins install cc-bmad@cocode-skills
claude plugins install cc-coui@cocode-skills
claude plugins install cc-pipeline@cocode-skills
claude plugins install cc-workflow@cocode-skills
```

<Warning>
  `claude plugins install coco-de/skills` 형태는 지원되지 않습니다. 반드시 `플러그인명@마켓플레이스명` 형식을 사용하세요.
</Warning>

### 설치 확인

```
# 설치된 플러그인 목록 확인
claude plugins list
```

설치가 성공하면 플러그인 이름과 버전이 표시됩니다:

```
cc-flutter-dev@cocode-skills  1.0.0  Flutter 개발 핵심 (UI 패턴, Feature 생성, BLoC, 테스트)
cc-bmad@cocode-skills         1.0.0  BMAD 방법론 (Business Method Agile Delivery)
cc-coui@cocode-skills         2.0.0  CoUI 컴포넌트 라이브러리 (85개 크로스플랫폼 컴포넌트)
...
```

## 설치 후 사용법

### 스킬 사용하기

설치된 플러그인의 스킬은 **슬래시 커맨드(`/`)로 호출**합니다. Claude Code 대화 중에 입력하세요:

```
# Flutter UI 패턴 스킬 호출
> /flutter-ui 로그인 페이지 만들어줘

# 코드 리뷰 스킬 호출
> /code-review

# BMAD PRD 작성
> /prd
```

<Info>
  사용 가능한 스킬 목록은 Claude Code에서 `/`를 입력하면 자동완성으로 확인할 수 있습니다.
</Info>

### 에이전트 활용

에이전트는 관련 작업 시 **자동으로 활성화**됩니다. 별도 호출 없이 Claude Code가 적절한 에이전트를 선택합니다.

```
# 백엔드 작업 시 backend-architect 에이전트 자동 활성화
> Serverpod에 새 엔드포인트 추가해줘

# TDD 작업 시 tdd-orchestrator 에이전트 자동 활성화
> 이 기능에 대한 테스트부터 작성해줘
```

### 룰 적용

룰은 **항상 자동 적용**됩니다. 설치만 하면 Claude Code가 해당 규칙을 따릅니다.

```
# cc-flutter-dev의 rules가 적용되어 Clean Architecture 컨벤션을 자동으로 따름
> 새 Feature 만들어줘
```

## 플러그인 관리

### 업데이트

```
# 마켓플레이스 카탈로그 갱신 (원격 저장소에서 최신 정보 가져오기)
claude plugins marketplace update cocode-skills

# 개별 플러그인 업데이트
claude plugins update cc-workflow@cocode-skills

# 업데이트 후 Claude Code 재시작 필요
```

<Warning>
  플러그인의 `plugin.json` 버전이 변경되어야 업데이트가 감지됩니다. 버전이 동일하면 "already at the latest version"으로 표시됩니다.
</Warning>

### 삭제

```
# 개별 플러그인 삭제
claude plugins uninstall cc-flutter-dev

# 마켓플레이스 제거
claude plugins marketplace remove cocode-skills
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

```
# 프로젝트 설정
- 프로젝트명: MyApp
- 아키텍처: Clean Architecture + BLoC
- UI 라이브러리: CoUI
- 백엔드: Serverpod
```

## 추천 설치 조합

### Flutter 앱 개발

```
claude plugins install cc-flutter-dev@cocode-skills
claude plugins install cc-coui@cocode-skills
claude plugins install cc-i18n@cocode-skills
claude plugins install cc-flutter-inspector@cocode-skills
```

### 풀스택 개발

```
claude plugins install cc-flutter-dev@cocode-skills
claude plugins install cc-serverpod@cocode-skills
claude plugins install cc-backend@cocode-skills
claude plugins install cc-coui@cocode-skills
claude plugins install cc-dev-cycle@cocode-skills
```

### PM + 개발 통합

```
claude plugins install cc-pipeline@cocode-skills
claude plugins install cc-bmad@cocode-skills
claude plugins install cc-pm-discovery@cocode-skills
claude plugins install cc-pm-strategy@cocode-skills
```

### UI/UX 전문

```
claude plugins install cc-uiux-design@cocode-skills
claude plugins install cc-uiux-frontend@cocode-skills
claude plugins install cc-uiux-accessibility@cocode-skills
claude plugins install cc-uiux-testing@cocode-skills
```

## 트러블슈팅

### `gh auth` 오류

```
# 인증 상태 확인
gh auth status

# 재인증
gh auth login
```

### 플러그인이 인식되지 않을 때

1. Claude Code를 재시작합니다
2. 설치 상태를 확인합니다:

```
claude plugins list
```

3. 재설치합니다:

```
claude plugins marketplace update cocode-skills
claude plugins update cc-flutter-dev@cocode-skills
```

### 슬래시 커맨드가 나타나지 않을 때

- 플러그인이 설치되었는지 `claude plugins list`로 확인
- Claude Code 세션을 새로 시작 (`/clear` 또는 터미널 재시작)
- 해당 플러그인에 skills 디렉토리가 있는지 확인

### 권한 오류

```
# GitHub 토큰 권한 확인
gh auth status

# repo 접근 테스트
gh repo view coco-de/skills --json name
```

Private 레포 접근이 안 되면 팀 관리자에게 Organization 초대를 요청하세요.

## 검증

플러그인 구조가 올바른지 검증하려면:

```
python3 validate_plugins.py       # 기본 검증
python3 validate_plugins.py -v    # 상세 출력
```

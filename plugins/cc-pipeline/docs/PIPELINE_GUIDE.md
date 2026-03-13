# Pipeline Guide — 전체 워크플로우 가이드

## 개요

cc-pipeline은 Cocode 팀의 프로젝트 라이프사이클을 6단계 파이프라인으로 관리하는 오케스트레이션 플러그인입니다. 기존 플러그인(cc-bmad, cc-pm-*, cc-workflow)을 수정하지 않고 위에서 조율합니다.

## 파이프라인 흐름

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Discovery  │───▶│  Planning   │───▶│   Design    │
│   (분석)    │    │   (기획)    │    │   (설계)    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                   │
                    Analysis Gate      Solutioning Gate
                          │                   │
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Launch    │◀───│ Development │◀───│Epic Creation│
│   (출시)    │    │   (개발)    │    │   (생성)    │
└─────────────┘    └─────────────┘    └─────────────┘
                          │                   │
                   Implementation       Planning Gate
                       Gate
```

## 시작하기

### 신규 프로젝트

```bash
/project "프로젝트 설명"
```

이 명령은:
1. 프로젝트 슬러그 생성
2. BMAD 레벨 자동 판단
3. 6단계를 순차 실행 (스킵 가능 스테이지 자동 판단)

### 개별 스테이지 진입

각 스테이지를 독립적으로 실행할 수 있습니다:

```bash
/project:discover "기능 설명"
/project:plan
/project:design
/project:epic
/project:develop --epic 42
/project:launch
```

이전 스테이지의 산출물이 있으면 자동 참조됩니다.

## BMAD 레벨별 가이드

### Level 0: Hotfix (단순 버그 수정)

```
Planning → Development
```

Discovery, Design, Epic Creation, Launch를 스킵합니다.

### Level 1: Minor Feature (소규모 기능 추가)

```
Planning → Design → Epic Creation → Development
```

Discovery, Launch를 스킵합니다.

### Level 2-3: Feature / Major Feature

```
Discovery → Planning → Design → Epic Creation → Development → Launch
```

전체 파이프라인을 실행합니다.

### Level 4: New Project

```
Discovery (심층) → Planning → Design → Epic Creation → Development → Launch
```

Discovery를 심층 모드로 실행합니다.

## 게이트

각 게이트는 BMAD 프레임워크의 품질 체크포인트입니다.

### Analysis Gate (Planning → Design)

- 요구사항 명확성
- 범위 적절성
- Acceptance Criteria 테스트 가능성

### Solutioning Gate (Design → Epic Creation)

- Architect: Clean Architecture, DI, API, 보안
- UX Designer: CoUI, 레이아웃, 인터랙션, 접근성

### Planning Gate (Epic Creation → Development)

- Epic/Story 구조
- 스토리 포인트
- 라벨링
- 의존성

### Implementation Gate (Development, 각 Story별)

- 린트 통과
- 테스트 통과
- 코드 리뷰 통과
- 브랜치 네이밍 규칙

## 상태 관리

파이프라인 상태는 `.pipeline/{slug}.yaml`에 저장됩니다.

```bash
# 상태 확인
/pipeline:status

# 특정 프로젝트
/pipeline:status community

# 전체 프로젝트 목록
/pipeline:status --all
```

## 산출물 관리

모든 산출물은 프로젝트의 `docs/` 디렉토리에 저장됩니다:

| 스테이지 | 산출물 |
|----------|--------|
| Discovery | `docs/discovery-{slug}.md` |
| Planning | `docs/prd-{slug}.md`, `docs/tech-spec-{slug}.md`, `docs/bdd-{slug}.md` |
| Design | `docs/architecture-{slug}.md`, `docs/ux-spec-{slug}.md` |
| Epic Creation | ZenHub Epic + Stories (이슈 번호) |
| Development | 구현 코드 + PR |
| Launch | `docs/gtm-{slug}.md`, `docs/analytics-plan-{slug}.md` |

## 중단 및 재개

파이프라인은 언제든 중단하고 재개할 수 있습니다:

```bash
# 중단 후 상태 확인
/pipeline:status community

# Design 스테이지부터 재개
/project --from design "커뮤니티 기능"
```

상태 파일에 마지막 위치가 기록되므로, 이전 산출물을 자동으로 참조합니다.

## 의존 플러그인

| 플러그인 | 사용 스테이지 | 역할 |
|----------|---------------|------|
| cc-bmad | 1-5 | 방법론, 게이트, 페르소나 |
| cc-pm-discovery | 1 | 사용자 리서치 |
| cc-pm-strategy | 1-2 | 제품 전략 |
| cc-pm-gtm | 6 | Go-to-Market |
| cc-pm-analytics | 6 | 데이터 분석 |
| cc-workflow | 4-5 | 개발 워크플로우 |

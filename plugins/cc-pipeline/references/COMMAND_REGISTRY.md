# Command Registry — 전체 커맨드 레지스트리

cc-pipeline이 오케스트레이션하는 모든 소스 플러그인의 커맨드/스킬 목록입니다.

## cc-pipeline 커맨드

| 커맨드 | 파일 | 설명 |
|--------|------|------|
| `/project` | `commands/project.md` | 전체 파이프라인 실행 |
| `/project:discover` | `commands/project/discover.md` | Stage 1: Discovery |
| `/project:plan` | `commands/project/plan.md` | Stage 2: Planning |
| `/project:design` | `commands/project/design.md` | Stage 3: Design |
| `/project:epic` | `commands/project/epic.md` | Stage 4: Epic Creation |
| `/project:develop` | `commands/project/develop.md` | Stage 5: Development |
| `/project:launch` | `commands/project/launch.md` | Stage 6: Launch |
| `/pipeline:status` | `commands/pipeline/status.md` | 파이프라인 상태 조회 |

## 소스 플러그인별 커맨드/스킬

### cc-bmad (방법론)

| 유형 | 이름 | 사용 스테이지 | 역할 |
|------|------|---------------|------|
| 커맨드 | `/bmad:research` | Discovery | 시장/기술 리서치 |
| 커맨드 | `/bmad:brainstorm` | Discovery | 아이디에이션 |
| 커맨드 | `/bmad:product-brief` | Planning | 제품 브리프 |
| 커맨드 | `/bmad:prd` | Planning | PRD 작성 |
| 커맨드 | `/bmad:tech-spec` | Planning | 기술 사양 |
| 커맨드 | `/bmad:architecture` | Design | 아키텍처 설계 |
| 커맨드 | `/bmad:create-ux-design` | Design | UX 설계 |
| 커맨드 | `/bmad:create-story` | Epic Creation | 스토리 작성 |
| 커맨드 | `/bmad:sprint-planning` | Epic Creation | 스프린트 계획 |
| 커맨드 | `/bmad:dev-story` | Development | 스토리 구현 |
| 페르소나 | Analyst | Planning | 요구사항 분석, BDD AC |
| 페르소나 | Architect | Design | 아키텍처 리뷰 |
| 페르소나 | UX Designer | Design | UX 리뷰 |
| 페르소나 | PM | Epic Creation | 스토리 포인트, 라벨링 |
| 페르소나 | Flutter Dev | Development | Flutter 구현 리뷰 |
| 페르소나 | Backend Dev | Development | Backend 구현 리뷰 |

### cc-pm-discovery (제품 발견)

| 유형 | 이름 | 사용 스테이지 | 역할 |
|------|------|---------------|------|
| 스킬 | user-interview | Discovery | 사용자 인터뷰 |
| 스킬 | assumption-testing | Discovery | 가정 검증 |
| 스킬 | experiment-design | Discovery | 실험 설계 |

### cc-pm-strategy (제품 전략)

| 유형 | 이름 | 사용 스테이지 | 역할 |
|------|------|---------------|------|
| 스킬 | competitive-analysis | Discovery | 경쟁 분석 |
| 스킬 | product-vision | Discovery | 비전 수립 |
| 스킬 | business-model | Planning | 비즈니스 모델 |

### cc-workflow (개발 워크플로우)

| 유형 | 이름 | 사용 스테이지 | 역할 |
|------|------|---------------|------|
| 커맨드 | `/zenhub:create-epic` | Epic Creation | Epic/Story 생성 |
| 커맨드 | `/workflow` | Development | 13단계 개발 사이클 |

### cc-pm-gtm (Go-to-Market)

| 유형 | 이름 | 사용 스테이지 | 역할 |
|------|------|---------------|------|
| 스킬 | gtm-motion | Launch | GTM 전략 |
| 스킬 | icp-definition | Launch | ICP 정의 |
| 스킬 | messaging-framework | Launch | 메시징 프레임워크 |

### cc-pm-analytics (데이터 분석)

| 유형 | 이름 | 사용 스테이지 | 역할 |
|------|------|---------------|------|
| 스킬 | ab-testing | Launch | A/B 테스트 설계 |
| 스킬 | cohort-analysis | Launch | 코호트 분석 |

## 스테이지별 의존성 요약

| 스테이지 | 필수 플러그인 | 선택 플러그인 |
|----------|---------------|---------------|
| Discovery | cc-pm-discovery | cc-pm-strategy, cc-bmad |
| Planning | cc-bmad | cc-pm-strategy |
| Design | cc-bmad | — |
| Epic Creation | cc-workflow, cc-bmad | — |
| Development | cc-workflow | cc-bmad |
| Launch | cc-pm-gtm | cc-pm-analytics |

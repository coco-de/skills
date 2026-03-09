# cc-pipeline

통합 프로젝트 파이프라인 오케스트레이터. 분석부터 출시까지 6단계 파이프라인을 하나의 진입점으로 제공합니다.

## 개요

cc-bmad, cc-pm-*, cc-workflow 등 기존 플러그인을 **병합하지 않고 오케스트레이션**하여 전체 프로젝트 라이프사이클을 관리합니다.

## 6-Stage Pipeline

| Stage | 이름 | 커맨드 | 설명 |
|-------|------|--------|------|
| 1 | Discovery | `/project:discover` | 사용자 리서치, 경쟁 분석, 아이디에이션 |
| 2 | Planning | `/project:plan` | 제품 브리프, PRD, 기술 사양 |
| 3 | Design | `/project:design` | 아키텍처, UX 설계 |
| 4 | Epic Creation | `/project:epic` | ZenHub Epic/Story 생성 |
| 5 | Development | `/project:develop` | 13단계 개발 사이클 |
| 6 | Launch | `/project:launch` | GTM, 메시징, 분석 |

## 사용법

```bash
# 전체 파이프라인 실행
/project "커뮤니티 기능 개발"

# 개별 스테이지
/project:discover "커뮤니티 기능"
/project:plan
/project:design
/project:epic
/project:develop --epic 42
/project:launch

# 현황 조회
/pipeline:status
```

## 의존 플러그인

- `cc-bmad` — 방법론, 게이트, 페르소나
- `cc-pm-discovery` — 사용자 리서치
- `cc-pm-strategy` — 제품 전략
- `cc-pm-gtm` — Go-to-Market
- `cc-pm-analytics` — 데이터 분석
- `cc-workflow` — 개발 워크플로우 자동화

## 산출물

각 스테이지의 산출물은 프로젝트 `docs/` 디렉토리에 저장됩니다:

- `docs/discovery-{slug}.md`
- `docs/prd-{slug}.md` / `docs/tech-spec-{slug}.md`
- `docs/architecture-{slug}.md` / `docs/ux-spec-{slug}.md`
- ZenHub Epic + Stories
- 구현 코드 + PR
- `docs/gtm-{slug}.md`

파이프라인 상태는 `.pipeline/{slug}.yaml`에 추적됩니다.

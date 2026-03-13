---
name: pipeline
description: 프로젝트 파이프라인 오케스트레이션 (Discovery → Launch 6단계)
---

# Pipeline Orchestrator (프로젝트 파이프라인 오케스트레이터)

## 트리거
- "프로젝트 시작", "새 프로젝트", "전체 파이프라인" 키워드가 언급될 때
- `/project` 커맨드가 호출될 때
- 분석→기획→설계→개발→출시 전체 흐름이 필요할 때
- 기존 플러그인들을 연결하는 오케스트레이션이 필요할 때

## 동작

### 1. 프로젝트 초기화
- 프로젝트 슬러그 생성 (kebab-case)
- `.pipeline/{slug}.yaml` 상태 파일 생성
- BMAD 프로젝트 레벨 판단 (Level 0-4)

### 2. 스테이지 실행 흐름

```
Discovery → Planning → Design → Epic Creation → Development → Launch
    │           │          │           │              │           │
    ▼           ▼          ▼           ▼              ▼           ▼
cc-pm-*     cc-bmad    cc-bmad    cc-workflow     cc-workflow  cc-pm-gtm
cc-bmad     cc-pm-*               cc-bmad         cc-bmad      cc-pm-analytics
```

### 3. 각 스테이지 실행 시
1. **이전 산출물 확인**: 이전 스테이지 산출물이 존재하는지 검증
2. **스킵 조건 평가**: 프로젝트 레벨/유형에 따라 스킵 가능 여부 판단
3. **소스 플러그인 위임**: 해당 스테이지의 스킬/커맨드를 순서대로 호출
4. **게이트 검증**: BMAD 게이트 통과 여부 확인
5. **산출물 저장**: 결과물을 `docs/` 디렉토리에 저장
6. **상태 업데이트**: `.pipeline/{slug}.yaml` 갱신

### 4. 스테이지 간 데이터 전달
- 이전 스테이지의 산출물 경로를 다음 스테이지에 자동 전달
- Discovery → Planning: 리서치 결과, 비전
- Planning → Design: PRD, 기술 사양, BDD Acceptance Criteria
- Design → Epic: 아키텍처, UX 스펙
- Epic → Development: Epic/Story 이슈 번호
- Development → Launch: 배포된 기능 목록

### 5. 스킵 규칙
- **Discovery 스킵**: BMAD Level 0-1 (기존 제품의 소규모 기능 추가)
- **Launch 스킵**: 내부 기능, 소규모 개선, 인프라 변경
- **사용자 확인**: 스킵 시 항상 사용자에게 확인

### 6. 상태 파일 형식 (.pipeline/{slug}.yaml)

```yaml
project:
  name: "커뮤니티 기능"
  slug: community
  level: 3
  created: 2025-01-15T10:00:00Z
  updated: 2025-01-16T14:30:00Z

stages:
  discovery:
    status: completed        # pending | in-progress | completed | skipped
    started: 2025-01-15T10:00:00Z
    completed: 2025-01-15T12:00:00Z
    artifacts:
      - docs/discovery-community.md
    skip_reason: null

  planning:
    status: in-progress
    started: 2025-01-15T14:00:00Z
    gate: analysis           # 현재 게이트
    artifacts: []

  design:
    status: pending
  epic:
    status: pending
  development:
    status: pending
  launch:
    status: pending
```

## 출력
- 프로젝트 상태 대시보드 (스테이지별 진행률)
- 각 스테이지의 산출물 (docs/ 디렉토리)
- `.pipeline/{slug}.yaml` 상태 추적 파일
- 스테이지 전환 시 요약 리포트

## 참고
- 기존 플러그인을 **수정하지 않고** 위에서 오케스트레이션
- BMAD 게이트는 품질 체크포인트로 활용 (analysis, planning, solutioning, implementation)
- 페르소나는 각 스테이지의 리뷰어 역할 (Analyst, Architect, PM 등)
- 사용자가 원하면 어떤 스테이지든 독립적으로 실행 가능
- `config/stage-mapping.yaml`에서 스테이지별 소스 커맨드 매핑 관리

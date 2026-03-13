---
name: project:plan
description: "Stage 2: Planning — 제품 브리프, PRD, 기술 사양, BDD Acceptance Criteria"
invoke: /project:plan
category: pipeline
complexity: moderate
---

# /project:plan

> Stage 2: Planning — 제품 브리프, PRD/기술 사양을 작성하고 BMAD Analysis Gate를 통과합니다.

## Triggers

- Discovery 산출물을 기반으로 제품 기획을 진행할 때
- PRD, 기술 사양, BDD 시나리오를 작성해야 할 때

## 사용법

```bash
/project:plan
/project:plan --doc prd "커뮤니티 기능"
/project:plan --doc tech-spec
```

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--doc` | `prd` | 문서 유형 (`prd`, `tech-spec`, `both`) |
| `--bdd` | `true` | BDD Gherkin Acceptance Criteria 포함 여부 |

## 전제 조건

- Discovery 스테이지 완료 또는 스킵됨 (`.pipeline/{slug}.yaml` 확인)
- Discovery 산출물이 있으면 자동 참조

## 실행 흐름

### Phase 1: 제품 브리프

**소스**: cc-bmad

1. **제품 브리프 작성** (/bmad:product-brief)
   - Discovery 산출물 기반 제품 개요
   - 목표, 범위, 제약 조건
   - 성공 기준 정의

### Phase 2: 상세 문서 작성

**소스**: cc-bmad, cc-pm-strategy

2. **PRD 또는 기술 사양** (/bmad:prd 또는 /bmad:tech-spec)
   - 기능 요구사항 상세화
   - 비기능 요구사항 (성능, 보안, 접근성)
   - 사용자 플로우
   - 데이터 모델 초안

3. **비즈니스 모델** (cc-pm-strategy: business-model)
   - 수익 모델 검토
   - 비용 구조 분석
   - 가치 제안 정리

### Phase 3: 요구사항 분석

**소스**: cc-bmad (Analyst 페르소나)

4. **요구사항 분석**
   - 요구사항 명확성 검증
   - 모호성, 충돌 식별
   - 우선순위 매기기

5. **BDD Acceptance Criteria**
   - Gherkin 형식 시나리오 작성
   - Given-When-Then 구조화
   - 엣지 케이스 시나리오 포함

### Phase 4: Analysis Gate

**BMAD Analysis Gate 검증**:
- [ ] 요구사항 명확성 (requirement_clarity)
- [ ] 범위 적절성 (scope_appropriateness)
- [ ] Acceptance Criteria 테스트 가능성 (ac_testability)

게이트 실패 시 피드백을 반영하여 문서를 수정합니다.

## 산출물

```
docs/prd-{slug}.md          # PRD (선택 시)
docs/tech-spec-{slug}.md    # 기술 사양 (선택 시)
docs/bdd-{slug}.md          # BDD 시나리오
```

## 완료 후

- Analysis Gate 통과 확인
- `.pipeline/{slug}.yaml` 상태 업데이트
- 다음 스테이지 `/project:design` 진행 여부 확인

---
name: project:epic
description: "Stage 4: Epic Creation — ZenHub Epic/Story 생성, 스프린트 계획"
invoke: /project:epic
category: pipeline
complexity: moderate
mcp-servers: [zenhub]
---

# /project:epic

> Stage 4: Epic Creation — 설계 산출물을 기반으로 ZenHub Epic과 Story를 생성합니다.

## Triggers

- Design 스테이지 완료 후 개발 이슈를 생성할 때
- 아키텍처/UX 스펙을 실행 가능한 작업 단위로 분할할 때

## 사용법

```bash
/project:epic
/project:epic --sprint current
/project:epic --feature community --entity Post
```

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--sprint` | 없음 | 스프린트 할당 (`current`, `next`, 번호) |
| `--feature` | 슬러그 | Feature 이름 (snake_case) |
| `--entity` | 자동 추론 | Entity 이름 (PascalCase) |

## 전제 조건

- Design 스테이지 완료 (Solutioning Gate 통과)
- Architecture Doc, UX Spec 산출물 존재

## 실행 흐름

### Phase 1: Epic 생성

**소스**: cc-workflow

1. **ZenHub Epic 생성** (/zenhub:create-epic)
   - Architecture Doc 기반 Epic 구조화
   - Feature/Entity 매핑
   - Epic 설명에 설계 산출물 링크

### Phase 2: Story 작성

**소스**: cc-bmad

2. **개별 Story 작성** (/bmad:create-story)
   - UX Spec 기반 화면별 Story
   - Architecture 기반 기술 Story
   - BDD 시나리오를 Acceptance Criteria로 연결
   - 의존성 관계 설정

3. **스프린트 계획** (/bmad:sprint-planning)
   - Story 우선순위 결정
   - 스프린트 할당
   - 용량 계획

### Phase 3: PM 리뷰

**소스**: cc-bmad (PM 페르소나)

4. **Story 품질 검증**
   - 스토리 포인트 산정
   - 라벨링 (type, scope, priority)
   - 의존성 검증
   - Acceptance Criteria 완전성 확인

### Phase 4: Planning Gate

**BMAD Planning Gate 검증**:
- [ ] Epic/Story 구조 (epic_story_structure)
- [ ] 스토리 포인트 (story_point)
- [ ] 라벨링 (labeling)
- [ ] 의존성 (dependencies)

## 산출물

- ZenHub Epic (이슈 번호 기록)
- 연결된 Stories (이슈 번호 목록)
- `.pipeline/{slug}.yaml`에 epic 번호 기록

## 완료 후

- Planning Gate 통과 확인
- Epic/Story 번호를 상태 파일에 기록
- 다음 스테이지 `/project:develop --epic {번호}` 안내

---
name: project:design
description: "Stage 3: Design — 아키텍처 설계, UX 설계, Solutioning Gate"
invoke: /project:design
category: pipeline
complexity: moderate
---

# /project:design

> Stage 3: Design — 아키텍처와 UX를 설계하고 BMAD Solutioning Gate를 통과합니다.

## Triggers

- Planning 산출물(PRD/Tech Spec)을 기반으로 설계를 진행할 때
- 아키텍처와 UX 설계가 필요할 때

## 사용법

```bash
/project:design
/project:design --focus architecture
/project:design --focus ux
```

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--focus` | `both` | 집중 영역 (`architecture`, `ux`, `both`) |

## 전제 조건

- Planning 스테이지 완료 (Analysis Gate 통과)
- PRD/Tech Spec 산출물 존재

## 실행 흐름

### Phase 1: 아키텍처 설계

**소스**: cc-bmad

1. **아키텍처 설계** (/bmad:architecture)
   - 시스템 구조 설계 (Clean Architecture)
   - 레이어 정의 (Presentation, Domain, Data)
   - DI 구조 설계
   - API 설계
   - 데이터 모델 확정
   - 보안 아키텍처

### Phase 2: UX 설계

**소스**: cc-bmad

2. **UX 설계** (/bmad:create-ux-design)
   - 화면 플로우 설계
   - 와이어프레임
   - CoUI 컴포넌트 매핑
   - 인터랙션 패턴
   - 접근성 고려사항

### Phase 3: 병렬 리뷰

**소스**: cc-bmad (Architect + UX Designer 페르소나)

3. **Architect 리뷰**
   - Clean Architecture 준수 여부
   - DI 구조 적절성
   - API 설계 검토
   - 보안 검토

4. **UX Designer 리뷰**
   - CoUI 컴포넌트 적합성
   - 레이아웃 일관성
   - 인터랙션 자연스러움
   - 접근성 검증

### Phase 4: Solutioning Gate

**BMAD Solutioning Gate 검증**:

Architect 체크:
- [ ] Clean Architecture 준수 (clean_architecture)
- [ ] DI 구조 적절 (di_structure)
- [ ] API 설계 (api_design)
- [ ] 보안 (security)

UX Designer 체크:
- [ ] CoUI 준수 (coui_compliance)
- [ ] 레이아웃 (layout)
- [ ] 인터랙션 (interaction)
- [ ] 접근성 (accessibility)

게이트 실패 시 피드백을 반영하여 설계를 수정합니다.

## 산출물

```
docs/architecture-{slug}.md    # 아키텍처 문서
docs/ux-spec-{slug}.md         # UX 사양
```

## 완료 후

- Solutioning Gate 통과 확인
- `.pipeline/{slug}.yaml` 상태 업데이트
- 다음 스테이지 `/project:epic` 진행 여부 확인

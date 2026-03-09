---
name: project:develop
description: "Stage 5: Development — Epic 내 Stories를 순회하며 13단계 개발 사이클 실행"
invoke: /project:develop
category: pipeline
complexity: high
mcp-servers: [zenhub]
---

# /project:develop

> Stage 5: Development — Epic 내 Stories를 순회하며 cc-workflow 13단계 개발 사이클을 실행합니다.

## Triggers

- Epic Creation 완료 후 개발을 시작할 때
- 특정 Epic 또는 Issue의 구현이 필요할 때

## 사용법

```bash
# Epic 전체 개발
/project:develop --epic 42

# 단일 이슈 개발
/project:develop --issue 1810

# 파이프라인 컨텍스트에서 자동
/project:develop
```

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `--epic` | ✅* | Epic 번호 | `42` |
| `--issue` | ✅* | 단일 이슈 번호 | `1810` |

*epic 또는 issue 중 하나 필수. 파이프라인 컨텍스트에서는 자동으로 epic 번호 참조.

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--parallel` | `false` | 독립 Story 병렬 실행 |
| `--skip-review` | `false` | 코드 리뷰 스킵 (긴급) |
| `--skip-tests` | `false` | 테스트 스킵 (긴급) |

## 전제 조건

- Epic Creation 스테이지 완료 (Planning Gate 통과)
- ZenHub Epic 및 Stories 존재

## 실행 흐름

### Epic 모드 (--epic)

1. **Story 목록 조회**
   - ZenHub에서 Epic 내 Story 목록 가져오기
   - 의존성 순서대로 정렬
   - 상태 확인 (이미 완료된 Story 스킵)

2. **Story 순회 실행**
   각 Story에 대해:

   a. **Story 구현 준비** (cc-bmad: /bmad:dev-story)
      - Story 상세 분석
      - 구현 계획 수립
      - 필요 파일/컴포넌트 식별

   b. **13단계 개발 사이클** (cc-workflow: /workflow {issue_number})
      - Step 1: 이슈 분석
      - Step 2: BDD 시나리오 확인
      - Step 3: 구현 계획
      - Step 4: 브랜치 생성
      - Step 5: 구현
      - Step 6: 테스트 작성
      - Step 7: 테스트 실행
      - Step 8: 린트 검사
      - Step 9: PR 생성
      - Step 10: 코드 리뷰
      - Step 11: 리뷰 반영
      - Step 12: 머지
      - Step 13: 정리

   c. **구현 리뷰** (cc-bmad: Flutter/Backend Dev 페르소나)
      - 구현 품질 검증
      - 아키텍처 준수 확인

3. **진행 상황 추적**
   - 각 Story 완료 시 `.pipeline/{slug}.yaml` 업데이트
   - 실패한 Story 기록

### 단일 이슈 모드 (--issue)

- 바로 cc-workflow 13단계 실행
- 파이프라인 상태 업데이트

### Implementation Gate

**BMAD Implementation Gate 검증** (각 Story별):
- [ ] 린트 통과 (dart analyze, dcm analyze)
- [ ] 테스트 통과
- [ ] 코드 리뷰 통과
- [ ] 브랜치 네이밍 규칙 준수

## 산출물

- 구현 코드 (각 Story별 브랜치 → PR → 머지)
- `.pipeline/{slug}.yaml`에 완료된 Story 목록

## 완료 후

- 모든 Story 완료 확인
- Implementation Gate 통과 확인
- `.pipeline/{slug}.yaml` 상태 업데이트
- 다음 스테이지 `/project:launch` 진행 여부 확인

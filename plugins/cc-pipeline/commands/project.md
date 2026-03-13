---
name: project
description: "프로젝트 전체 파이프라인 실행 (Discovery → Launch)"
invoke: /project
category: pipeline
complexity: high
---

# /project

> 프로젝트 설명으로 6단계 전체 파이프라인을 순차 실행합니다.

## Triggers

- 새로운 프로젝트를 처음부터 끝까지 진행할 때
- 전체 라이프사이클 오케스트레이션이 필요할 때

## 사용법

```bash
# 전체 파이프라인
/project "커뮤니티 기능 개발"

# 레벨 지정 (스킵 규칙에 영향)
/project --level 3 "커뮤니티 기능 개발"

# 특정 스테이지부터 시작
/project --from design "커뮤니티 기능 개발"

# 특정 스테이지까지만
/project --to epic "커뮤니티 기능 개발"
```

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `설명` | ✅ | 프로젝트 설명 | `"커뮤니티 기능 개발"` |

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--level` | 자동 판단 | BMAD 프로젝트 레벨 (0-4) |
| `--from` | discovery | 시작 스테이지 |
| `--to` | launch | 종료 스테이지 |
| `--skip` | 없음 | 스킵할 스테이지 (쉼표 구분) |

## 실행 흐름

### Step 1: 프로젝트 초기화

1. 프로젝트 설명에서 슬러그 생성 (kebab-case)
2. BMAD 프로젝트 레벨 자동 판단
   - Level 0: 단순 버그 수정 → Discovery/Launch 스킵
   - Level 1: 소규모 기능 추가 → Discovery 스킵
   - Level 2: 중규모 기능 → 전체 실행
   - Level 3: 대규모 기능/새 모듈 → 전체 실행
   - Level 4: 신규 프로젝트 → 전체 실행 (심층)
3. `.pipeline/{slug}.yaml` 상태 파일 생성
4. `docs/` 디렉토리 확인/생성

### Step 2: Discovery (분석)

**스킵 조건**: Level 0-1

```
→ /project:discover "{설명}"
```

- cc-pm-discovery: 사용자 인터뷰, 가정 검증, 실험 설계
- cc-pm-strategy: 경쟁 분석, 비전 수립
- cc-bmad: /bmad:research, /bmad:brainstorm
- **산출물**: `docs/discovery-{slug}.md`

### Step 3: Planning (기획)

```
→ /project:plan
```

- cc-bmad: /bmad:product-brief, /bmad:prd 또는 /bmad:tech-spec
- cc-pm-strategy: 비즈니스 모델
- cc-bmad Analyst: 요구사항 분석, BDD Acceptance Criteria
- **게이트**: BMAD Analysis Gate
- **산출물**: PRD/Tech Spec + BDD Acceptance Criteria

### Step 4: Design (설계)

```
→ /project:design
```

- cc-bmad: /bmad:architecture, /bmad:create-ux-design
- cc-bmad Architect + UX Designer: 병렬 리뷰
- **게이트**: BMAD Solutioning Gate
- **산출물**: Architecture Doc + UX Spec

### Step 5: Epic Creation (생성)

```
→ /project:epic
```

- cc-dev-cycle: /zenhub:create-epic
- cc-bmad: /bmad:create-story, /bmad:sprint-planning
- cc-bmad PM: 스토리 포인트, 라벨링
- **게이트**: BMAD Planning Gate
- **산출물**: ZenHub Epic + linked Stories

### Step 6: Development (개발)

```
→ /project:develop --epic {epic_number}
```

- Epic 내 Stories 순회, 각각 cc-dev-cycle 13단계 실행
- cc-bmad: /bmad:dev-story
- cc-bmad Flutter/Backend Dev: 구현 리뷰
- **게이트**: BMAD Implementation Gate
- **산출물**: 구현 코드 + PR

### Step 7: Launch (출시)

**스킵 조건**: 내부 기능, 소규모 개선

```
→ /project:launch
```

- cc-pm-gtm: GTM 전략, ICP 정의, 메시징
- cc-pm-analytics: A/B 테스트, 코호트 분석
- **산출물**: `docs/gtm-{slug}.md`

### Step 8: 완료

- 상태 파일 최종 업데이트
- 전체 파이프라인 요약 리포트 출력
- 산출물 목록 정리

## 스테이지 간 전환

각 스테이지 완료 후:
1. 산출물 존재 확인
2. 게이트 통과 확인 (해당 시)
3. 상태 파일 업데이트
4. 다음 스테이지 진입 전 사용자 확인 요청

## 에러 처리

- 게이트 실패 시: 실패 사유 표시, 수정 후 재시도 안내
- 소스 플러그인 미설치 시: 경고 후 해당 스테이지 수동 진행 안내
- 중단 시: 상태 파일에 마지막 위치 기록, 이후 `--from` 옵션으로 재개 가능

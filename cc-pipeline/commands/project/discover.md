---
name: project:discover
description: "Stage 1: Discovery — 사용자 리서치, 경쟁 분석, 아이디에이션"
invoke: /project:discover
category: pipeline
complexity: moderate
---

# /project:discover

> Stage 1: Discovery — 시장 조사, 사용자 리서치, 경쟁 분석, 아이디에이션을 수행합니다.

## Triggers

- 새로운 제품/기능의 초기 탐색 단계
- 시장 기회를 파악하고 검증해야 할 때

## 사용법

```bash
/project:discover "커뮤니티 기능"
/project:discover --depth deep "소셜 커머스 플랫폼"
```

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `설명` | ✅ | 탐색 대상 설명 | `"커뮤니티 기능"` |

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--depth` | `normal` | 탐색 깊이 (`quick`, `normal`, `deep`) |
| `--focus` | 없음 | 집중 영역 (`user`, `market`, `tech`) |

## 스킵 조건

다음 경우 이 스테이지를 건너뛸 수 있습니다:
- BMAD Level 0-1 (기존 제품의 소규모 기능 추가/버그 수정)
- 이미 충분한 리서치 산출물이 존재하는 경우

스킵 시 사용자에게 확인을 요청합니다.

## 실행 흐름

### Phase 1: 사용자 리서치

**소스**: cc-pm-discovery

1. **사용자 인터뷰** (user-interview)
   - 타겟 사용자 페르소나 정의
   - 인터뷰 가이드 작성
   - 핵심 인사이트 정리

2. **가정 검증** (assumption-testing)
   - 핵심 가정 목록화
   - 가정별 검증 방법 설계
   - 리스크 수준 평가

3. **실험 설계** (experiment-design)
   - MVP 실험 설계
   - 성공 메트릭 정의
   - 실험 일정 수립

### Phase 2: 시장 분석

**소스**: cc-pm-strategy

4. **경쟁 분석** (competitive-analysis)
   - 직접/간접 경쟁사 매핑
   - 기능 비교 매트릭스
   - 차별화 포인트 도출

5. **비전 수립** (product-vision)
   - 제품 비전 스테이트먼트
   - 성공 메트릭 (North Star Metric)
   - 장기 로드맵 방향

### Phase 3: 아이디에이션

**소스**: cc-bmad

6. **시장/기술 리서치** (/bmad:research)
   - 기술 트렌드 분석
   - 기술 실현 가능성 평가

7. **아이디에이션** (/bmad:brainstorm)
   - 브레인스토밍 세션
   - 아이디어 우선순위화
   - 초기 솔루션 방향 도출

### Phase 4: 산출물 통합

- 모든 Phase 결과를 `docs/discovery-{slug}.md`로 통합
- 핵심 인사이트 요약
- 다음 스테이지(Planning)로의 권고사항 정리

## 산출물

```
docs/discovery-{slug}.md
```

### 산출물 구조

```markdown
# Discovery: {프로젝트명}

## 사용자 리서치
### 타겟 페르소나
### 핵심 인사이트
### 검증된/미검증 가정

## 시장 분석
### 경쟁 환경
### 차별화 포인트

## 비전
### 비전 스테이트먼트
### North Star Metric

## 아이디에이션
### 솔루션 방향
### 기술 실현 가능성

## 권고사항
### Planning 스테이지 입력 사항
```

## 완료 후

- `.pipeline/{slug}.yaml`의 discovery 상태를 `completed`로 업데이트
- 산출물 경로 기록
- 다음 스테이지 `/project:plan` 진행 여부 확인

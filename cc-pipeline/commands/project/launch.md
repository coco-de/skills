---
name: project:launch
description: "Stage 6: Launch — GTM 전략, ICP 정의, 메시징, A/B 테스트"
invoke: /project:launch
category: pipeline
complexity: moderate
---

# /project:launch

> Stage 6: Launch — Go-to-Market 전략, 메시징, 분석 계획을 수립합니다.

## Triggers

- Development 완료 후 출시 준비가 필요할 때
- GTM 전략, 마케팅 메시지를 수립해야 할 때

## 사용법

```bash
/project:launch
/project:launch --focus gtm
/project:launch --focus analytics
```

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--focus` | `all` | 집중 영역 (`gtm`, `analytics`, `all`) |

## 스킵 조건

다음 경우 이 스테이지를 건너뛸 수 있습니다:
- 내부 기능 (사용자에게 노출되지 않는 기능)
- 소규모 개선 (UI 미세 조정, 버그 수정)
- 인프라 변경

스킵 시 사용자에게 확인을 요청합니다.

## 전제 조건

- Development 스테이지 완료
- 배포 가능한 코드 존재

## 실행 흐름

### Phase 1: GTM 전략

**소스**: cc-pm-gtm

1. **GTM 모션** (gtm-motion)
   - Product-Led vs Sales-Led 결정
   - 채널 전략
   - 런칭 타임라인

2. **ICP 정의** (icp-definition)
   - 이상적 고객 프로필 정의
   - 세그먼트별 특성
   - 초기 타겟 세그먼트

3. **메시징 프레임워크** (messaging-framework)
   - 포지셔닝 스테이트먼트
   - 엘리베이터 피치
   - 채널별 메시지 변형

### Phase 2: 분석 계획

**소스**: cc-pm-analytics

4. **A/B 테스트 설계** (ab-testing)
   - 테스트 가설
   - 변형(Variant) 설계
   - 표본 크기 계산
   - 성공 메트릭

5. **코호트 분석** (cohort-analysis)
   - 코호트 정의
   - 추적 메트릭
   - 분석 쿼리 설계

### Phase 3: 산출물 통합

- GTM 전략 + 분석 계획 통합 문서 작성
- 런칭 체크리스트 생성

## 산출물

```
docs/gtm-{slug}.md             # GTM 전략 문서
docs/analytics-plan-{slug}.md  # 분석 계획
```

## 완료 후

- `.pipeline/{slug}.yaml` 전체 파이프라인 `completed`
- 전체 프로젝트 요약 리포트 출력
- 산출물 목록 정리

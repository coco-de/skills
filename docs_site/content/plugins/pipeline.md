---
title: 파이프라인
description: 통합 프로젝트 파이프라인 오케스트레이터 — Discovery에서 Launch까지 6단계
---

# 파이프라인

## cc-pipeline

**통합 프로젝트 파이프라인 오케스트레이터** — Discovery에서 Launch까지 6단계 프로젝트 라이프사이클을 관리합니다.

### 6단계 파이프라인

| 단계 | 커맨드 | 설명 |
|------|--------|------|
| 1. Discovery | `/project:discover` | 시장 조사, 사용자 리서치, 문제 정의 |
| 2. Planning | `/project:plan` | PRD 작성, 기술 요구사항, 로드맵 |
| 3. Design | `/project:design` | 아키텍처 설계, UI/UX 디자인 |
| 4. Epic | `/project:epic` | 에픽/스토리 분해, 스프린트 계획 |
| 5. Development | `/project:develop` | 구현, 코드리뷰, 테스트 |
| 6. Launch | `/project:launch` | 배포, 모니터링, 릴리스 |

### 파이프라인 상태 확인

```
/pipeline:status             # 현재 파이프라인 상태 확인
```

### 연동 플러그인

cc-pipeline은 다른 플러그인들을 오케스트레이션합니다:

- **cc-bmad** — 방법론, 게이트, 페르소나
- **cc-pm-discovery** — 사용자 리서치
- **cc-pm-strategy** — 제품 전략
- **cc-pm-analytics** — 데이터 분석
- **cc-pm-gtm** — Go-to-Market
- **cc-workflow** — 워크플로우 자동화

### 산출물

파이프라인 산출물은 다음 경로에 저장됩니다:

```
project/
├── docs/                    # 프로젝트 문서
└── .pipeline/
    └── {slug}.yaml          # 파이프라인 상태 파일
```

### 설치

```
claude plugins install coco-de/skills/plugins/cc-pipeline
```

> [상세 페이지 보기 →](/plugins/cc-pipeline/)

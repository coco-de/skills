# BMAD Framework 사용 가이드

BMAD(Breakthrough Method for Agile AI-Driven Development)는 7개 전문 페르소나가 검토하고 4개 페이즈 게이트를 통해 품질을 보장하는 AI 기반 개발 프레임워크입니다.

---

## 목차

1. [빠른 시작](#빠른-시작)
2. [페이즈 개요](#페이즈-개요)
3. [페르소나 소개](#페르소나-소개)
4. [커맨드 레퍼런스](#커맨드-레퍼런스)
5. [워크플로우 예시](#워크플로우-예시)
6. [설정 커스터마이징](#설정-커스터마이징)
7. [문제 해결](#문제-해결)

---

## 빠른 시작

### 기본 사용법

```bash
# BMAD 워크플로우로 새 기능 개발
/bmad "저자 목록 화면 추가"

# 기존 workflow에 BMAD 활성화
/workflow --bmad "저자 목록 화면 추가"
```

### 첫 번째 BMAD 워크플로우

1. **작업 설명 입력**: `/bmad "원하는 기능 설명"`
2. **Analysis 페이즈**: Analyst가 요구사항 분석
3. **Planning 페이즈**: PM이 이슈 생성 및 Story Point 산정
4. **Solutioning 페이즈**: Architect와 UX Designer가 병렬 검토
5. **Implementation 페이즈**: 코드 구현, 테스트, PR 생성
6. **완료**: PR 머지 및 이슈 종료

---

## 페이즈 개요

### 4단계 페이즈 흐름

```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Analysis   │ → │   Planning   │ → │ Solutioning  │ → │Implementation│
│              │    │              │    │   (병렬)     │    │              │
│  • 요구사항   │    │  • 이슈 생성  │    │  • 아키텍처  │    │  • 코드 구현  │
│  • AC 정의   │    │  • SP 산정   │    │  • UX 검토   │    │  • 테스트    │
│  • 타당성    │    │  • 라벨링    │    │              │    │  • PR/머지   │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
       │                  │                   │                   │
       ▼                  ▼                   ▼                   ▼
   [Gate 1]           [Gate 2]            [Gate 3]            [Gate 4]
```

### 페이즈별 상세

| 페이즈 | 담당 페르소나 | 게이트 검증 항목 |
|--------|--------------|-----------------|
| **Analysis** | Analyst | 요구사항 명확성, 스코프 적절성, **AC BDD Gherkin 형식** ⭐ |
| **Planning** | Product Manager | Epic/Story 구조, Story Point (1-8), 라벨링, 의존성 |
| **Solutioning** | Architect + UX Designer (병렬) | Clean Architecture, DI 구조, CoUI 준수, 레이아웃 |
| **Implementation** | Flutter/Backend Developer, Scrum Master | 브랜치 규칙, 린트 통과, 테스트, 코드 리뷰 |

---

## 페르소나 소개

### 7개 전문 페르소나

| 페르소나 | 역할 | 담당 페이즈 |
|---------|------|-----------|
| **Analyst** | 요구사항 분석, **BDD Gherkin AC 작성** ⭐, 타당성 검토 | Analysis |
| **Product Manager** | 이슈 구조화, Story Point 산정, 우선순위 설정 | Planning |
| **Architect** | 아키텍처 설계 검토, API 설계, 보안 검토 | Solutioning |
| **UX Designer** | UI/UX 검토, CoUI 준수, 접근성 검토 | Solutioning |
| **Flutter Developer** | UI 구현, BLoC 상태 관리, 테스트 작성 | Implementation |
| **Backend Developer** | Serverpod 구현, DB 설계, API 개발 | Implementation |
| **Scrum Master** | 워크플로우 관리, 블로커 해결, 상태 동기화 | Implementation |

### 페르소나 정의 파일

각 페르소나의 상세 정의는 `.claude/personas/` 디렉토리에 있습니다:

```
.claude/personas/
├── analyst.md
├── product-manager.md
├── architect.md
├── ux-designer.md
├── flutter-developer.md
├── backend-developer.md
└── scrum-master.md
```

---

## 커맨드 레퍼런스

### 메인 커맨드

#### `/bmad` - 전체 워크플로우 실행

```bash
# 기본 사용
/bmad "저자 목록 화면 추가"

# 특정 게이트만 활성화
/bmad --gates analysis,planning "간단한 작업"

# 긴급 모드 (게이트 간소화, 관리자 승인 필요)
/bmad --emergency "프로덕션 긴급 수정"

# 병렬 실행 비활성화
/bmad --no-parallel "순차 처리 필요"

# 특정 페르소나 스킵
/bmad --skip-persona ux-designer "백엔드 전용 작업"
```

#### `/workflow --bmad` - 기존 워크플로우 통합

```bash
# 기존 workflow에 BMAD 페이즈 게이트 적용
/workflow --bmad "저자 목록 화면 추가"
```

### 보조 커맨드

#### `/bmad:review` - 페르소나별 검토

```bash
# 특정 페르소나 검토 요청
/bmad:review --persona architect "현재 코드 검토"

# 여러 페르소나 동시 검토
/bmad:review --persona architect,ux-designer "설계 검토"

# 재검토 요청 (실패 후)
/bmad:review --persona architect --retry
```

#### `/bmad:status` - 상태 확인

```bash
# 전체 상태 확인
/bmad:status

# 특정 페이즈 상세 확인
/bmad:status --phase solutioning

# 특정 이슈 상태 확인
/bmad:status --issue 1810
```

#### `/bmad:gate` - 게이트 검증

```bash
# 특정 페이즈 게이트 검증
/bmad:gate --phase analysis
/bmad:gate --phase solutioning

# 재검증 요청
/bmad:gate --phase solutioning --retry

# 모든 게이트 상태 확인
/bmad:gate --all
```

### 옵션 요약

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--bmad` | `false` | BMAD 페이즈 게이트 활성화 |
| `--gates` | 모든 게이트 | 특정 게이트만 활성화 |
| `--emergency` | `false` | 긴급 모드 (게이트 간소화) |
| `--skip-persona` | - | 특정 페르소나 스킵 |
| `--no-parallel` | `false` | 병렬 실행 비활성화 |
| `--retry` | `false` | 재검토/재검증 모드 |

---

## 워크플로우 예시

### 예시 1: 새 기능 개발

```bash
# 1. BMAD 워크플로우 시작
/bmad "저자 목록 화면 추가"

# 2. Analysis 결과 확인 (자동 진행)
# - Analyst가 요구사항 분석
# - AC 3개 정의됨
# - Gate 1 통과

# 3. Planning 결과 확인 (자동 진행)
# - PM이 이슈 #1810 생성
# - Story Point: 5
# - Gate 2 통과

# 4. Solutioning 결과 확인 (병렬 실행)
# - Architect: Clean Architecture 검토 ✅
# - UX Designer: CoUI 준수 검토 ✅
# - Gate 3 통과

# 5. Implementation 진행 (자동 진행)
# - 브랜치 생성: feature/1810-author-list
# - 코드 구현
# - 테스트 작성/실행
# - PR #1815 생성
# - 코드 리뷰 완료
# - Gate 4 통과

# 6. 완료
# - PR 머지
# - 이슈 종료
```

### 예시 2: 게이트 실패 및 재검토

```bash
# 1. 워크플로우 진행 중 Solutioning Gate 실패
# 출력:
# ╔════════════════════════════════════════════════════════════════╗
# ║  Solutioning Gate: ❌ FAILED                                   ║
# ╠════════════════════════════════════════════════════════════════╣
# ║  🏗️ Architect 검토: ❌ FAILED                                  ║
# ║  ├── ❌ DI 구조: BLoC이 Repository를 직접 접근                  ║
# ║  └── 필요한 조치: UseCase 생성 후 의존성 변경                   ║
# ╚════════════════════════════════════════════════════════════════╝

# 2. 피드백에 따라 코드 수정
# (UseCase 생성, BLoC 수정)

# 3. 재검토 요청
/bmad:review --persona architect --retry

# 4. 재검토 통과 시 다음 단계 자동 진행
```

### 예시 3: 긴급 수정

```bash
# 긴급 모드로 워크플로우 실행
# (Analysis, Planning 게이트 간소화)
/bmad --emergency "프로덕션 결제 버그 긴급 수정"

# ⚠️ 주의: 긴급 모드는 관리자 승인 필요
# ⚠️ 사후 리뷰 필수
```

---

## 설정 커스터마이징

### 설정 파일 위치

```
.claude/config/bmad.json       # BMAD 설정
.claude/config/bmad-schema.json # 설정 스키마
```

### 주요 설정 항목

```json
{
  "enabled": true,
  "defaultMode": "optional",

  "gates": {
    "analysis": { "enabled": true, "mandatory": true },
    "planning": { "enabled": true, "mandatory": true },
    "solutioning": {
      "enabled": true,
      "mandatory": true,
      "parallelPersonas": ["architect", "ux-designer"]
    },
    "implementation": { "enabled": true, "mandatory": true }
  },

  "personas": {
    "analyst": { "enabled": true },
    "product-manager": { "enabled": true },
    "architect": { "enabled": true },
    "ux-designer": { "enabled": true },
    "flutter-developer": { "enabled": true },
    "backend-developer": { "enabled": true },
    "scrum-master": { "enabled": true }
  },

  "emergency": {
    "allowBypass": true,
    "requireApproval": true
  },

  "parallelExecution": {
    "enabled": true,
    "maxConcurrency": 2
  }
}
```

### 설정 변경 예시

#### 특정 페르소나 비활성화

```json
{
  "personas": {
    "ux-designer": { "enabled": false }
  }
}
```

#### 병렬 실행 비활성화

```json
{
  "parallelExecution": {
    "enabled": false
  }
}
```

---

## 문제 해결

### 자주 묻는 질문

#### Q: 게이트가 계속 실패해요

**A**: 피드백 내용을 확인하고 모든 항목을 수정한 후 재검토를 요청하세요.

```bash
# 피드백 확인
/bmad:status --phase solutioning

# 수정 후 재검토
/bmad:review --persona architect --retry
```

#### Q: 특정 페르소나 검토를 건너뛰고 싶어요

**A**: `--skip-persona` 옵션을 사용하거나 설정에서 비활성화하세요.

```bash
# 커맨드 옵션으로
/bmad --skip-persona ux-designer "백엔드 전용 작업"

# 또는 설정 파일에서
# .claude/config/bmad.json
{
  "personas": {
    "ux-designer": { "enabled": false }
  }
}
```

#### Q: 긴급 상황에서 게이트를 우회하고 싶어요

**A**: `--emergency` 옵션을 사용하세요. 단, 관리자 승인과 사후 리뷰가 필요합니다.

```bash
/bmad --emergency "긴급 수정"
```

### 에러 코드 참조

| 코드 | 설명 | 해결 방법 |
|------|------|----------|
| `BMAD_001` | Analysis Gate 실패 | 요구사항 명확화 후 재검토 |
| `BMAD_002` | Planning Gate 실패 | 이슈 구조 수정 후 재검토 |
| `BMAD_003` | Solutioning Gate 실패 | 설계 수정 후 재검토 |
| `BMAD_004` | Implementation Gate 실패 | 코드 수정 후 재검토 |
| `BMAD_010` | 페르소나 비활성화 | 설정에서 페르소나 활성화 |
| `BMAD_011` | 병렬 실행 실패 | 순차 실행으로 전환 |
| `BMAD_020` | 긴급 모드 남용 | 관리자 승인 필요 |

---

## 관련 문서

### 사용자 가이드

| 문서 | 설명 |
|------|------|
| `BMAD_QUICKREF.md` | 5분 빠른 참조 가이드 |
| `BMAD_TUTORIAL.md` | 단계별 튜토리얼 |

### 개발자 참조

| 문서 | 설명 |
|------|------|
| `.claude/skills/bmad/SKILL.md` | BMAD 스킬 정의 |
| `.claude/skills/bmad/REFERENCE.md` | 상세 참조 |
| `.claude/orchestrators/bmad-orchestrator.md` | 오케스트레이터 |
| `.claude/orchestrators/phase-gates.md` | 게이트 정의 |
| `.claude/references/PERSONA_MATRIX.md` | 페르소나 책임 매트릭스 |
| `.claude/personas/` | 페르소나 정의 디렉토리 (7개 파일) |

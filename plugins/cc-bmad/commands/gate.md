---
name: bmad:gate
description: "BMAD 페이즈 게이트 수동 검증"
invoke: /bmad:gate
aliases: []
category: workflow
complexity: medium
mcp-servers: []
---

# /bmad:gate

> BMAD 페이즈 게이트를 수동으로 검증합니다.

---

## Triggers

- 게이트 상태 수동 확인 시
- 게이트 실패 후 재검증 시
- 특정 게이트 조건 확인 시

## 사용법

### 기본 사용

```bash
# 특정 페이즈 게이트 검증
/bmad:gate --phase analysis
/bmad:gate --phase planning
/bmad:gate --phase solutioning
/bmad:gate --phase implementation
```

### 재검증 요청

```bash
# 피드백 반영 후 재검증
/bmad:gate --phase solutioning --retry
```

### 모든 게이트 확인

```bash
# 전체 게이트 상태 확인
/bmad:gate --all
```

---

## 옵션

| 옵션 | 필수 | 설명 |
|------|------|------|
| `--phase` | ⚠️* | 검증할 페이즈 |
| `--all` | ⚠️* | 모든 게이트 확인 |
| `--retry` | ❌ | 재검증 모드 |
| `--verbose` | ❌ | 상세 결과 출력 |

*`--phase` 또는 `--all` 중 하나 필수

---

## 게이트별 검증 항목

### Analysis Gate

```yaml
checks:
  - requirement_clarity:
      description: "요구사항이 구체적이고 측정 가능한가?"
  - scope_appropriateness:
      description: "단일 이슈로 적절한 크기인가?"
  - ac_testability:
      description: "AC가 자동 테스트 가능한가?"
```

### Planning Gate

```yaml
checks:
  - epic_story_structure:
      description: "적절한 계층 구조인가?"
  - story_point:
      description: "1-8 SP 범위인가?"
      threshold: { min: 1, max: 8, split_required: 13 }
  - labeling:
      description: "Type, Scope 라벨이 있는가?"
  - dependencies:
      description: "블로커가 해결 가능한가?"
```

### Solutioning Gate

```yaml
checks:
  architect:
    - clean_architecture
    - di_structure
    - api_design  # backend 변경 시
    - security
  ux_designer:
    - coui_compliance
    - layout
    - interaction
    - accessibility  # 권장
```

### Implementation Gate

```yaml
sub_gates:
  - step_4_branch:
      pattern: "^(feature|fix|refactor|chore)/[0-9]+"
  - step_8_5_lint:
      commands: ["dart analyze", "dcm analyze"]
  - step_9_pr:
      checks: [branch_format, issue_linked, commits_exist, lint_passed]
```

---

## 출력 형식

### 게이트 통과

```
╔════════════════════════════════════════════════════════════════╗
║  Analysis Gate: ✅ PASSED                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ 요구사항 명확성: PASS                                       ║
║     - 기능 요구사항 3개 식별                                    ║
║     - 성공 조건 명확                                           ║
║                                                                ║
║  ✅ 스코프 적절성: PASS                                         ║
║     - 예상 복잡도: 중간 (3-5 SP)                               ║
║     - 단일 이슈로 적절                                         ║
║                                                                ║
║  ✅ AC 테스트 가능성: PASS                                      ║
║     - AC 3개 정의됨                                            ║
║     - 모두 BDD 시나리오로 변환 가능                            ║
║                                                                ║
║  → Planning 페이즈로 진행 가능                                 ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 게이트 실패

```
╔════════════════════════════════════════════════════════════════╗
║  Solutioning Gate: ❌ FAILED                                   ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🏗️ Architect 검토: ❌ FAILED                                  ║
║  ├── ✅ Clean Architecture                                     ║
║  ├── ❌ DI 구조: injector.module.dart export 누락              ║
║  ├── ✅ API 설계 (N/A)                                         ║
║  └── ✅ 보안                                                   ║
║                                                                ║
║  🎨 UX Designer 검토: ✅ PASSED                                ║
║  ├── ✅ CoUI 준수                                              ║
║  ├── ✅ 레이아웃                                               ║
║  ├── ✅ 상호작용                                               ║
║  └── ⚠️ 접근성 (권장)                                          ║
║                                                                ║
║  게이트 결과: FAILED (Architect 검토 실패)                     ║
║                                                                ║
║  필요한 조치:                                                  ║
║  1. lib/console_author.dart에 export 추가:                     ║
║     export 'src/di/injector.module.dart';                     ║
║                                                                ║
║  재검증 명령:                                                  ║
║  /bmad:gate --phase solutioning --retry                        ║
║                                                                ║
║  ⚠️ Implementation 페이즈로 진행할 수 없습니다.                ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 전체 게이트 상태

```
╔════════════════════════════════════════════════════════════════╗
║  BMAD Gate Status (전체)                                       ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Analysis Gate:       ✅ PASSED                                ║
║  Planning Gate:       ✅ PASSED                                ║
║  Solutioning Gate:    ❌ FAILED (Architect)                    ║
║  Implementation Gate: ⏳ PENDING                               ║
║                                                                ║
║  현재 블로커: Solutioning Gate                                 ║
║  다음 조치: /bmad:gate --phase solutioning --retry            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 강제 게이트 정책

⚠️ **중요**: 모든 게이트는 강제입니다.

```
게이트 실패 시:
├── 다음 페이즈 진행 불가
├── 피드백 제공
└── 재검증 필요

예외:
├── Emergency 모드 (--emergency)
│   └── 관리자 승인 필요
└── 사후 리뷰 필수
```

---

## 관련 커맨드

- `/bmad` - 전체 BMAD 워크플로우
- `/bmad:review` - 페르소나별 검토
- `/bmad:status` - 상태 확인

## 관련 문서

- `.claude/orchestrators/phase-gates.md` - 게이트 상세 정의
- `.claude/personas/` - 페르소나별 검토 기준

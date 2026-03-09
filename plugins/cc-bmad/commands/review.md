---
name: bmad:review
description: "특정 페르소나로 검토 실행"
invoke: /bmad:review
aliases: []
category: workflow
complexity: medium
mcp-servers: [zenhub]
---

# /bmad:review

> 특정 페르소나로 개별 검토를 실행합니다.

---

## Triggers

- 특정 페르소나의 검토만 필요할 때
- 게이트 실패 후 재검토 시
- 부분 검토가 필요할 때

## 사용법

### 기본 사용

```bash
# Architect 검토
/bmad:review --persona architect "현재 PR 검토"

# Analyst 검토
/bmad:review --persona analyst "요구사항 검토"

# UX Designer 검토
/bmad:review --persona ux-designer "UI 검토"
```

### 재검토 요청

```bash
# 피드백 반영 후 재검토
/bmad:review --persona architect --retry
```

### 여러 페르소나 동시 검토

```bash
# Architect와 UX Designer 병렬 검토
/bmad:review --persona architect,ux-designer "설계 검토"
```

---

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `--persona` | ✅ | 검토할 페르소나 | `architect`, `analyst` |
| `검토 대상` | ⚠️ | 검토할 내용 (신규 시 필수) | `"현재 PR 검토"` |

---

## 옵션

| 옵션 | 기본값 | 설명 |
|------|--------|------|
| `--retry` | false | 이전 피드백 기반 재검토 |
| `--verbose` | false | 상세 검토 결과 출력 |

---

## 사용 가능한 페르소나

| 페르소나 | 페이즈 | 검토 항목 |
|---------|--------|----------|
| `analyst` | Analysis | 요구사항, 스코프, AC |
| `product-manager` | Planning | Epic/Story, Point, 라벨 |
| `architect` | Solutioning | Architecture, DI, API |
| `ux-designer` | Solutioning | CoUI, 레이아웃, 상호작용 |
| `flutter-developer` | Implementation | BLoC, Widget, 테스트 |
| `backend-developer` | Implementation | Model, Endpoint, DB |
| `scrum-master` | Implementation | 워크플로우, 블로커 |

---

## 검토 실행 로직

### 단일 페르소나 검토

```typescript
async function runPersonaReview(
  persona: PersonaType,
  input: ReviewInput,
  options: ReviewOptions
): Promise<ReviewResult> {
  // 페르소나 설정 로드
  const personaConfig = loadPersona(persona);

  // 체크리스트 실행
  const checks = await runChecklist(personaConfig.checks, input);

  // 결과 집계
  const pass = checks.every(c => c.status === "pass");

  return {
    persona,
    pass,
    checks,
    feedback: pass ? undefined : generateFeedback(checks),
  };
}
```

### 여러 페르소나 병렬 검토

```typescript
async function runParallelReviews(
  personas: PersonaType[],
  input: ReviewInput
): Promise<ReviewResult[]> {
  return Promise.all(
    personas.map(persona => runPersonaReview(persona, input, {}))
  );
}
```

---

## 출력 형식

### 검토 통과

```
╔════════════════════════════════════════════════════════════════╗
║  🏗️ Architect Review: APPROVED                                 ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Clean Architecture: PASS                                    ║
║     - 레이어 분리 올바름                                       ║
║     - BLoC → UseCase → Repository 흐름 정상                    ║
║                                                                ║
║  ✅ DI 구조: PASS                                               ║
║     - Injectable 등록 완전                                     ║
║     - injector.module.dart export 확인                         ║
║                                                                ║
║  ✅ API 설계: N/A (Backend 변경 없음)                           ║
║                                                                ║
║  ✅ 보안: PASS                                                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 검토 거부

```
╔════════════════════════════════════════════════════════════════╗
║  🏗️ Architect Review: REJECTED                                 ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  ✅ Clean Architecture: PASS                                    ║
║                                                                ║
║  ❌ DI 구조: FAIL                                               ║
║     - injector.module.dart가 barrel에 export되지 않음          ║
║                                                                ║
║  필요한 수정:                                                  ║
║  1. lib/console_author.dart에 추가:                            ║
║     export 'src/di/injector.module.dart';                     ║
║                                                                ║
║  재검토 명령:                                                  ║
║  /bmad:review --persona architect --retry                      ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 재검토 흐름

```
┌─────────────────────────────────────────────────────────────────┐
│  재검토 흐름                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 초기 검토                                                   │
│     /bmad:review --persona architect "검토 대상"               │
│                                                                 │
│  2. 검토 실패 시                                                │
│     → 피드백 확인                                              │
│     → 수정 작업 수행                                           │
│                                                                 │
│  3. 재검토 요청                                                 │
│     /bmad:review --persona architect --retry                   │
│                                                                 │
│  4. 재검토 실행                                                 │
│     → 이전 피드백 항목 중심 검토                               │
│     → 새로운 문제 발견 시 추가 피드백                          │
│                                                                 │
│  5. 통과 시 다음 단계 진행                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 관련 커맨드

- `/bmad` - 전체 BMAD 워크플로우
- `/bmad:status` - 상태 확인
- `/bmad:gate` - 게이트 검증

## 관련 문서

- `.claude/personas/` - 각 페르소나 정의
- `.claude/orchestrators/phase-gates.md` - 게이트 기준

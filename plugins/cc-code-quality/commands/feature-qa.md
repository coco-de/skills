---
name: feature-qa
description: "Feature 단위 QA Health Score 평가 및 baseline 회귀 추적"
invoke: /feature-qa
aliases: ["/qa", "/quality-check"]
category: petmedi-development
complexity: moderate
---

# /feature-qa

> Feature 단위로 5축 QA Health Score를 평가하고, baseline 기반 회귀를 추적합니다.
> gstack `/qa` 패턴 참고: 정량적 품질 점수 + regression baseline 비교

## Triggers

- Feature 구현 완료 후 품질 검증 시
- PR 생성 전 품질 게이트로 사용 시
- 기존 Feature의 품질 회귀 확인 시

## 사용법

```bash
# 기본 사용: Feature 경로로 QA
/feature-qa feature/auth/

# regression 비교 (이전 baseline 대비)
/feature-qa feature/auth/ --regression

# 빠른 검사 (기능 완성도만)
/feature-qa feature/auth/ --quick

# 특정 축만 검사
/feature-qa feature/auth/ --focus ui,a11y
```

## 파라미터

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_path` | ✅ | Feature 모듈 경로 | `feature/auth/` |
| `--regression` | ❌ | 이전 baseline 대비 비교 | |
| `--quick` | ❌ | 빠른 검사 (기능 완성도만) | |
| `--focus` | ❌ | 특정 축 집중 | `ui`, `a11y`, `perf`, `i18n`, `func` |
| `--save-baseline` | ❌ | baseline 저장 (기본: 자동 저장) | |
| `--no-save` | ❌ | baseline 저장 안 함 | |

---

## 5축 평가 체계

### 🧪 기능 완성도 (Functional) — 가중치 30%

| 항목 | 배점 | 검사 방법 |
|------|------|----------|
| Acceptance Criteria 충족 | 30점 | 이슈의 AC와 구현 코드 매핑 |
| 엣지 케이스 처리 | 25점 | null/empty/boundary 처리 확인 |
| 에러 핸들링 | 25점 | try-catch, ErrorState, 사용자 메시지 |
| 테스트 커버리지 | 20점 | UseCase 100%, BLoC 80%+ 기준 |

**검사 항목:**
- [ ] 모든 AC가 구현 코드와 매핑되는가
- [ ] null safety가 적절히 처리되는가
- [ ] 네트워크 에러 시 사용자에게 피드백이 있는가
- [ ] 빈 목록 상태(EmptyState)가 처리되는가
- [ ] 로딩 상태가 표시되는가

### 🎨 UI/UX (Visual) — 가중치 20%

| 항목 | 배점 | 검사 방법 |
|------|------|----------|
| CoUI 컴포넌트 올바른 사용 | 30점 | 컴포넌트 API 준수 확인 |
| 레이아웃 일관성 | 25점 | Gap/Insets 상수 사용, 정렬 |
| 색상 체계 준수 | 25점 | appColors/colorScheme 사용 |
| 타이포그래피 준수 | 20점 | context.textStyles 사용 |

**검사 항목:**
- [ ] CoUI 컴포넌트 API가 올바르게 사용되는가 (features 파라미터 등)
- [ ] Gap/Insets 상수를 사용하는가 (하드코딩된 수치 없음)
- [ ] context.appColors / context.colorScheme으로 색상 접근하는가
- [ ] context.textStyles로 텍스트 스타일 접근하는가
- [ ] ButtonSize.medium 같은 존재하지 않는 API를 사용하지 않는가

### ♿ 접근성 (Accessibility) — 가중치 20%

| 항목 | 배점 | 검사 방법 |
|------|------|----------|
| Semantic Labels | 35점 | 이미지, 아이콘, 버튼에 label 존재 |
| 터치 타겟 크기 | 30점 | 최소 48x48 확인 |
| 색상 대비 | 20점 | WCAG AA 기준 |
| 스크린 리더 순서 | 15점 | 논리적 탭 순서 |

**검사 항목:**
- [ ] Image/Icon에 semanticLabel이 있는가
- [ ] 터치 가능 요소가 최소 48x48인가
- [ ] 텍스트-배경 색상 대비가 4.5:1 이상인가
- [ ] 의미 있는 순서로 위젯이 배치되는가

### ⚡ 성능 (Performance) — 가중치 15%

| 항목 | 배점 | 검사 방법 |
|------|------|----------|
| const 위젯 활용 | 30점 | const 가능한 위젯 확인 |
| BlocBuilder 최적화 | 25점 | buildWhen/listenWhen 사용 |
| 이미지 최적화 | 25점 | cacheWidth/cacheHeight 적용 |
| 리소스 해제 | 20점 | dispose/cancel 확인 |

**검사 항목:**
- [ ] const로 선언 가능한 위젯이 const인가
- [ ] BlocBuilder에 buildWhen이 적용되는가
- [ ] 네트워크 이미지에 cacheWidth/cacheHeight가 있는가
- [ ] Stream subscription이 dispose에서 cancel되는가
- [ ] BLoC의 isClosed 체크가 async 핸들러에 있는가

### 🌐 국제화 (i18n) — 가중치 15%

| 항목 | 배점 | 검사 방법 |
|------|------|----------|
| 번역 키 사용 | 40점 | context.t.* 패턴 사용 |
| 하드코딩 문자열 없음 | 30점 | UI 텍스트 하드코딩 검출 |
| 복수형 처리 | 15점 | plural/ordinal 적용 |
| 동적 값 파라미터화 | 15점 | 문자열 보간 대신 파라미터 |

**검사 항목:**
- [ ] 모든 UI 텍스트가 context.t.*를 사용하는가
- [ ] 하드코딩된 한국어/영어 문자열이 없는가
- [ ] 숫자 포함 텍스트에 복수형이 처리되는가
- [ ] 동적 값이 파라미터로 전달되는가

---

## Health Score 산출

### 점수 계산

```
총점 = Σ(각 축 점수 × 가중치) - (Critical 이슈 수 × 10)

각 축 점수 = Σ(항목별 점수) / 100 × 100
```

### 등급 기준

| 등급 | 점수 범위 | 의미 |
|------|----------|------|
| **A** | 90-100 | 우수 — 프로덕션 준비 완료 |
| **B** | 80-89 | 양호 — 마이너 개선 필요 |
| **C** | 70-79 | 보통 — 개선 권장 |
| **D** | 60-69 | 미흡 — 개선 필수 |
| **F** | 0-59 | 불량 — PR 생성 전 반드시 수정 |

---

## Baseline 저장 및 Regression 비교

### Baseline 저장

QA 실행 시 자동으로 `.qa-baseline/{feature-name}.json`에 저장:

```json
{
  "feature": "auth",
  "date": "2026-03-13T10:30:00Z",
  "grade": "B",
  "totalScore": 85,
  "scores": {
    "functional": { "score": 90, "weight": 0.30, "weighted": 27.0 },
    "visual": { "score": 80, "weight": 0.20, "weighted": 16.0 },
    "accessibility": { "score": 75, "weight": 0.20, "weighted": 15.0 },
    "performance": { "score": 85, "weight": 0.15, "weighted": 12.75 },
    "i18n": { "score": 90, "weight": 0.15, "weighted": 13.5 }
  },
  "criticalIssues": 0,
  "penalty": 0,
  "issues": [
    {
      "axis": "accessibility",
      "severity": "warning",
      "message": "semantic label 누락",
      "file": "lib/src/presentation/widget/author_card.dart",
      "line": 42
    }
  ]
}
```

### Regression 비교

`--regression` 옵션 사용 시 이전 baseline과 비교:

```markdown
## Regression Report: auth

| 축 | 이전 | 현재 | 변화 |
|----|------|------|------|
| 기능 완성도 | 90 | 92 | ✅ +2 |
| UI/UX | 80 | 80 | ➡️ 0 |
| 접근성 | 75 | 70 | ⚠️ -5 |
| 성능 | 85 | 88 | ✅ +3 |
| i18n | 90 | 90 | ➡️ 0 |
| **총점** | **85 (B)** | **84 (B)** | ⚠️ -1 |

### 회귀 항목 (점수 하락)
- ♿ 접근성 -5점: 새로 추가된 ProfileImage에 semanticLabel 누락
```

---

## 출력 형식

```markdown
╔════════════════════════════════════════════════════════════════╗
║  Feature QA Health Score: auth                                ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Grade: B (85/100)                                             ║
║                                                                ║
║  🧪 기능 완성도  ████████████████████░░  90/100 (×0.30 = 27.0) ║
║  🎨 UI/UX       ████████████████░░░░░░  80/100 (×0.20 = 16.0) ║
║  ♿ 접근성       ███████████████░░░░░░░  75/100 (×0.20 = 15.0) ║
║  ⚡ 성능         ████████████████░░░░░░  85/100 (×0.15 = 12.8) ║
║  🌐 i18n        ████████████████████░░  90/100 (×0.15 = 13.5) ║
║                                                                ║
║  Critical: 0건 | Penalty: 0점                                  ║
║  Baseline: 저장됨 (.qa-baseline/auth.json)                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

### Issues Found (5건)

| # | 축 | 심각도 | 이슈 | 파일 |
|---|-----|--------|------|------|
| 1 | ♿ 접근성 | ⚠️ | semantic label 누락 | author_card.dart:42 |
| 2 | ⚡ 성능 | ⚠️ | cacheWidth 미지정 | author_image.dart:15 |
| 3 | 🌐 i18n | 💡 | 하드코딩 문자열 | author_list_page.dart:28 |
| 4 | 🎨 UI/UX | 💡 | Gap 대신 SizedBox 사용 | author_form.dart:55 |
| 5 | 🧪 기능 | 💡 | EmptyState 미처리 | author_list_bloc.dart:30 |
```

---

## Automation

```bash
# 테스트 실행 (커버리지 확인용)
melos run test:with-html-coverage -- --scope="*auth*"

# 정적 분석
melos run analyze -- --scope="*auth*"

# 코드 리뷰 (상세)
/code-review feature/auth/ --gate-mode
```

---

## 관련 커맨드

- `/code-review` - 8카테고리 코드 리뷰
- `/checklist:feature-complete` - Feature 완료 체크리스트
- `/workflow` - 전체 개발 사이클 (Step 8.7에서 자동 호출 가능)

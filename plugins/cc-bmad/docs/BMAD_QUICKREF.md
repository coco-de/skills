# BMAD 빠른 참조 가이드

> 💡 5분 안에 BMAD를 시작할 수 있는 핵심 가이드

---

## 1분 요약

```bash
# 새 기능 개발
/bmad "기능 설명"

# 또는 기존 workflow에 BMAD 적용
/workflow --bmad "기능 설명"
```

BMAD는 **7명의 전문가**가 **4단계**를 거쳐 코드 품질을 검증합니다:

```
Analysis → Planning → Solutioning → Implementation
(분석가)    (PM)      (설계자+UX)    (개발자)
```

---

## 커맨드 치트 시트

### 메인 커맨드

| 커맨드 | 용도 | 예시 |
|--------|------|------|
| `/bmad` | BMAD 워크플로우 시작 | `/bmad "저자 목록 화면"` |
| `/bmad:review` | 특정 페르소나 검토 | `/bmad:review --persona architect` |
| `/bmad:status` | 진행 상태 확인 | `/bmad:status` |
| `/bmad:gate` | 게이트 검증 | `/bmad:gate --phase analysis` |

### 자주 쓰는 옵션

| 옵션 | 설명 | 예시 |
|------|------|------|
| `--gates` | 특정 게이트만 활성화 | `--gates analysis,planning` |
| `--emergency` | 긴급 모드 (게이트 간소화) | `--emergency` |
| `--skip-persona` | 특정 페르소나 스킵 | `--skip-persona ux-designer` |
| `--retry` | 재검토 요청 | `--retry` |

---

## 페이즈별 핵심 체크리스트

### Phase 1: Analysis (분석)

**담당**: Analyst

**통과 조건**:
- [ ] 요구사항이 명확하고 측정 가능한가?
- [ ] AC가 **BDD Gherkin 형식**으로 작성되었는가? ⭐
- [ ] `@happy-path` 시나리오가 최소 1개 있는가?
- [ ] `@error-handling` 시나리오가 최소 1개 있는가?

**Acceptance Criteria 예시** (필수 형식):
```gherkin
Feature: 저자 목록 화면

  @happy-path
  Scenario: 저자 목록 조회
    Given 관리자로 로그인되어 있다
    When 저자 목록 화면으로 이동한다
    Then 저자 목록이 표시된다

  @error-handling
  Scenario: 목록 로딩 실패
    Given 서버 연결이 불안정하다
    When 저자 목록 화면으로 이동한다
    Then 에러 메시지가 표시된다
    And 재시도 버튼이 표시된다
```

### Phase 2: Planning (기획)

**담당**: Product Manager

**통과 조건**:
- [ ] 이슈가 생성되었는가?
- [ ] Story Point가 1-8 사이인가?
- [ ] 적절한 라벨이 지정되었는가?
- [ ] 의존성이 명시되었는가?

### Phase 3: Solutioning (설계)

**담당**: Architect + UX Designer (병렬)

**Architect 체크리스트**:
- [ ] Clean Architecture 준수 (BLoC → UseCase → Repository)
- [ ] DI 구조 적절 (Injectable, GetIt)
- [ ] API 설계 검토 (필요 시)

**UX Designer 체크리스트**:
- [ ] CoUI 컴포넌트 사용
- [ ] 레이아웃 적절성
- [ ] 접근성 고려

### Phase 4: Implementation (구현)

**담당**: Flutter/Backend Developer, Scrum Master

**통과 조건**:
- [ ] 브랜치명 규칙: `feature/{이슈번호}-{slug}`
- [ ] `melos run analyze` 통과
- [ ] 테스트 통과
- [ ] 코드 리뷰 완료

---

## 게이트 실패 대응

### 실패 메시지 확인

```bash
# 상태 확인
/bmad:status

# 특정 페이즈 상세
/bmad:status --phase solutioning
```

### 재검토 요청

```bash
# 피드백 반영 후 재검토
/bmad:review --persona architect --retry

# 또는 게이트 재검증
/bmad:gate --phase solutioning --retry
```

### 흔한 실패 원인

| 게이트 | 흔한 실패 원인 | 해결 방법 |
|--------|---------------|----------|
| Analysis | AC가 Gherkin 형식 아님 | Given-When-Then 형식으로 재작성 |
| Analysis | @happy-path/@error-handling 누락 | 필수 태그 추가 |
| Solutioning | BLoC이 Repository 직접 접근 | UseCase 추가 |
| Solutioning | CoUI 미사용 | Material → CoUI 컴포넌트 변경 |
| Implementation | 린트 실패 | `melos run format && melos run analyze` |

---

## 긴급 모드

프로덕션 장애 등 긴급 상황에서만 사용:

```bash
/bmad --emergency "긴급 수정 내용"
```

**제약사항**:
- 관리자 승인 필요
- Implementation 게이트는 여전히 필수 (린트, 테스트)
- **48시간 내 사후 리뷰 필수**

---

## 설정 파일 위치

| 파일 | 용도 |
|------|------|
| `.claude/config/bmad.json` | BMAD 설정 |
| `.claude/personas/*.md` | 페르소나 정의 (7개) |
| `.claude/orchestrators/phase-gates.md` | 게이트 정의 |

### 페르소나 비활성화

```json
// .claude/config/bmad.json
{
  "personas": {
    "ux-designer": { "enabled": false }
  }
}
```

---

## 관련 문서

| 문서 | 내용 |
|------|------|
| `BMAD_GUIDE.md` | 전체 가이드 |
| `BMAD_TUTORIAL.md` | 단계별 튜토리얼 |
| `.claude/skills/bmad/SKILL.md` | 스킬 정의 |
| `.claude/references/PERSONA_MATRIX.md` | 페르소나 매트릭스 |

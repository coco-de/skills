---
name: workflow
description: 이슈 생성부터 머지까지 전체 개발 사이클 자동화
---

# Workflow

작업 내용으로 이슈 생성부터 머지 승인까지 전체 개발 사이클을 자동화하는 스킬입니다.

## Scope and Capabilities

### 핵심 기능

| 기능 | 설명 |
|------|------|
| 작업 분석 | 키워드 기반 타입/스코프/복잡도 자동 추론 |
| 이슈 생성 | ZenHub/GitHub 이슈 자동 생성 및 라벨링 |
| BDD 시나리오 | 화면 기능 감지 시 Gherkin 시나리오 자동 생성 |
| 테스트 실행 | Unit/BLoC/BDD Widget 테스트 자동 실행 |
| 코드 리뷰 | /code-review 및 /checklist 통합 |
| 머지 승인 | 사용자 승인 후 스쿼시 머지 |

### 13단계 워크플로우

| 단계 | 설명 | 전제조건 |
|------|------|---------|
| 1 | 작업 내용 분석 (타입/스코프/화면타입/포인트) | 없음 |
| 2 | ZenHub 이슈 생성 | Step 1 완료 |
| 3 | Product Backlog 이동 | Step 2 완료 |
| 4 | **브랜치 생성** ⚠️ 필수 | Step 2,3 완료 |
| 5 | In Progress 이동 | Step 4 완료 |
| 6 | BDD 시나리오 작성 (화면 기능 시) | Step 5 완료 |
| 7 | 구현 작업 | Step 5 완료 |
| 7.5 | Backend 코드 생성 (Backend 변경 시) | Step 7 완료 |
| 8 | 테스트 작성/실행 | Step 7 완료 |
| **8.5** | **Pre-push 검증** ⚠️ 필수 | Step 8 완료 |
| 9 | PR 생성 (검증 게이트 통과 후) | Step 8.5 완료 |
| 10 | Review/QA 이동 | Step 9 완료 |
| 11 | 코드 리뷰 진행 | Step 10 완료 |
| 12 | 머지 승인 대기 | Step 11 완료 |

### ⚠️ 단계 건너뛰기 방지

- **각 단계는 이전 단계 완료 후에만 진행 가능**
- development/main 브랜치에서 직접 커밋/PR 생성 금지
- TodoWrite로 상태 추적, 건너뛰기 시 오류 발생

## Quick Start

### 기본 사용

```bash
# 작업 내용으로 전체 사이클 시작
/workflow "저자 목록 화면 추가"
```

### 기존 이슈로 시작

```bash
# 이슈 번호로 시작 (Step 4부터)
/workflow 1810
```

### 옵션 사용

```bash
# 타입 명시
/workflow --type feat "저자 목록 화면 추가"

# 스코프 명시
/workflow --scope console-author "저자 목록 화면 추가"

# BDD 시나리오 스킵
/workflow --skip-bdd "간단한 수정"

# 테스트 스킵 (긴급)
/workflow --skip-tests "긴급 수정"

# 코드 리뷰 스킵 (긴급)
/workflow --skip-review "긴급 핫픽스"
```

## 자동 추론 규칙

### 타입 추론

| 키워드 | 타입 | Gitmoji |
|--------|------|---------|
| 추가, 구현, 생성, 화면 | feat | ✨ |
| 수정, 고치기, 버그, 에러 | fix | 🐛 |
| 개선, 리팩토링, 최적화 | refactor | ♻️ |
| 설정, 빌드, 환경 | chore | 🔧 |

### 화면 타입 감지 (BDD 생성 조건)

| 키워드 | 화면 타입 | BDD |
|--------|----------|-----|
| 목록, 리스트, list, 조회 | List | ✅ |
| 상세, detail, 보기 | Detail | ✅ |
| 추가, 생성, 등록, form | Form | ✅ |
| 수정, 편집, edit | Form | ✅ |

### Story Point 산정

| 복잡도 | Point | 조건 |
|--------|-------|------|
| 간단 | 1 | 단일 파일 |
| 보통 | 3 | 여러 파일 |
| 복잡 | 5 | 여러 레이어 |
| 대형 | 8 | 전체 Feature + BDD |

## 결과 형식

### 완료 시

```
╔════════════════════════════════════════════════════════════════╗
║  Workflow Complete: #1810                                      ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 Issue: #1810 - 저자 목록 화면 추가                          ║
║  🔀 PR: #1815                                                  ║
║  🌿 Branch: feature/1810-author-list (deleted)                 ║
║                                                                ║
║  ✅ Tests: 25/25 passed                                        ║
║  ✅ Review: All issues resolved                                ║
║  ✅ Checklist: 11/11 passed                                   ║
║                                                                ║
║  🏁 Final State: CLOSED                                        ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## Backend 코드 생성 (Step 7.5 & 12.5) ⚠️

### 실행 조건

Backend 관련 파일이 변경되었을 때 **반드시** 실행해야 합니다:

| 파일 패턴 | 의미 |
|----------|------|
| `*.spy.yaml` | 모델/DTO/Enum 정의 변경 |
| `*_endpoint.dart` | 엔드포인트 추가/수정 |
| `*_service.dart` | 서비스 로직 변경 |

### 실행 명령어

```bash
# Backend 코드 생성 (필수)
melos run backend:pod:generate

# 생성된 코드 커밋
git add .
git commit -m "chore(backend): 🔧 코드 생성"
```

### 실행 시점

| 시점 | 설명 |
|------|------|
| Step 7.5 | 구현 완료 후, 테스트 전에 실행 |
| Step 12.5 | PR 머지 후 development 브랜치에서 실행 |

### ⚠️ 생략 시 발생하는 문제

- kobic_client에 새 모델/API가 반영되지 않음
- 프론트엔드에서 새 기능 사용 불가
- **빌드 오류 발생**

## 검증 게이트 (필수)

### Step 4 브랜치 검증

**development/main 브랜치에서 직접 커밋 금지**:
- `/workflow` 스킬은 반드시 feature 브랜치에서 작업
- 브랜치 형식: `{type}/{issue_number}-{slug}`
- 올바른 예: `feature/30-validation-gates`

### Step 9 PR 생성 전 검증

1. **브랜치 형식 검증**: `feature|fix|refactor|chore/번호-설명`
2. **이슈 연결 검증**: 브랜치명에서 이슈 번호 추출 가능
3. **커밋 검증**: development 대비 1개 이상 커밋 존재
4. **Pre-push 검증**: format, analyze 통과

## Pre-push 훅 실패 대응

| 실패 유형 | 해결 방법 |
|----------|----------|
| dart format 실패 | `melos run format` 실행 후 재커밋 |
| flutter analyze 실패 | 분석 오류 수정 |
| dcm analyze 실패 | DCM 규칙 위반 수정 |
| 긴급 시 우회 | `LEFTHOOK=0 git push` (권장하지 않음) |

## 관련 커맨드

- `/workflow:issue-cycle` - 기존 이슈로 사이클 진행
- `/workflow:bug-cycle` - 버그 수정 전용 사이클
- `/code-review` - 코드 리뷰 실행
- `/checklist:feature-complete` - 완료 체크리스트
- `/bdd:generate` - BDD 시나리오 생성

## Additional Resources

- [workflow.md](../../commands/workflow.md) - 상세 커맨드 정의
- [issue-cycle.md](../../commands/workflow/issue-cycle.md) - 이슈 사이클 상세

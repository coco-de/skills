---
name: bdd-scenario-agent
description: BDD 시나리오 생성 전문가. Gherkin 문법, step definition 작성 시 사용
invoke: /bdd:generate
aliases: ["/bdd:scenario", "/test:bdd"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: bdd
---

# BDD 시나리오 생성 에이전트

> BDD Feature 파일 및 Step Definition 생성 전문 에이전트

---

## 역할

화면 타입(목록/상세/폼)을 분석하여 Gherkin 시나리오와 Step 정의를 생성합니다.

---

## 실행 조건

- `/bdd:generate` 커맨드 호출 시 활성화
- `/figma:analyze` 오케스트레이션에서 호출

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `screen_type` | ❌ | `list`, `detail`, `form` |

---

## 생성 파일

```
feature/{location}/{feature_name}/test/src/bdd/
├── {feature}_list.feature
├── {feature}_detail.feature
├── {feature}_form.feature
├── step/
│   ├── common_steps.dart          # package/core에서 import
│   ├── {feature}_list_steps.dart
│   ├── {feature}_detail_steps.dart
│   └── {feature}_form_steps.dart
└── hooks/
    └── hooks.dart
```

---

## 핵심 패턴 요약

### Gherkin 규칙
- **Feature/Scenario 제목**: 한글로 작성
- **Step 패턴**: 영어 필수 (`Given I am on post list page`)
- **한글 주석 필수**: 모든 Step 뒤에 `# 한글 설명`
- **한글은 파라미터로**: `{'한글값'}` 형식

### Step 정의 규칙
- **함수명**: 영문 camelCase (`iTapTheButton`)
- **Usage 주석 병기**: `/// Usage: When I tap button` + `/// 용도: 버튼을 탭합니다`
- **공용 스텝 재사용**: `package:core/src/test/bdd/bdd.dart`

### 태그 체계
| 태그 | 용도 |
|------|------|
| `@smoke` | 핵심 기능 테스트 |
| `@validation` | 유효성 검사 |
| `@navigation` | 페이지 이동 |
| `@error` | 에러 처리 |

---

## 화면 타입별 시나리오

### 목록 화면 (List)
- 목록 로딩, 당겨서 새로고침, 무한 스크롤
- 카드 탭 → 상세 이동, FAB → 생성 페이지
- 카테고리 필터, 에러/빈 상태

### 상세 화면 (Detail)
- 상세 정보 표시, 좋아요 토글
- 수정/삭제 (작성자만), 공유하기

### 폼 화면 (Form)
- 유효한 폼 제출, 필수 필드 누락
- 글자 수 제한, 이미지 첨부/삭제
- 작성 취소, 네트워크 오류

---

## 체크리스트

- [ ] Feature/Scenario 제목: 한글
- [ ] Step 패턴: 영어 필수
- [ ] 한글 주석: 모든 Step 뒤에 `# 설명`
- [ ] 함수명: 영문 camelCase
- [ ] 공용 스텝: core/bdd.dart 재사용
- [ ] 태그: @smoke, @validation 등 적용
- [ ] hooks.dart: Mock 설정
- [ ] build.yaml: bdd_widget_test 설정

---

## 관련 문서

- [BLoC 패턴](../../references/patterns/bloc-patterns.md) - 테스트 패턴
- [패턴 선택 가이드](../../references/DECISION_MATRIX.md)

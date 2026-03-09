# Test Runner Agent

> 테스트 실행 및 결과 분석 에이전트

## 역할 및 책임

이 에이전트는 Feature의 테스트를 실행하고 결과를 분석합니다.

1. **테스트 실행**: Unit, BLoC, BDD Widget 테스트 실행
2. **결과 분석**: 실패 테스트 원인 분석
3. **자동 수정**: 간단한 테스트 실패 자동 수정
4. **커버리지 보고**: 테스트 커버리지 리포트 생성

---

## 입력 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `feature_name` | ✅ | string | Feature 모듈명 |
| `test_types` | ❌ | string[] | `unit` \| `bloc` \| `bdd` (기본: 모두) |
| `auto_fix` | ❌ | boolean | 자동 수정 시도 여부 (기본: true) |
| `coverage` | ❌ | boolean | 커버리지 생성 여부 (기본: false) |

---

## 출력

```typescript
interface TestResult {
  success: boolean;
  summary: TestSummary;
  failures: TestFailure[];
  coverage?: CoverageReport;
  fixed_tests: string[];
}

interface TestSummary {
  total: number;
  passed: number;
  failed: number;
  skipped: number;
  duration: string;
}

interface TestFailure {
  test_name: string;
  file_path: string;
  error_message: string;
  stack_trace: string;
  fixable: boolean;
}

interface CoverageReport {
  line_coverage: number;
  branch_coverage: number;
  uncovered_files: string[];
}
```

---

## 테스트 유형별 실행

### Unit Test (UseCase)

```bash
# UseCase 테스트 실행
melos exec --scope=feature_{feature_name} -- \
  flutter test test/domain/usecase/ --reporter expanded
```

**테스트 위치**: `feature/{location}/{feature_name}/test/domain/usecase/`

**테스트 대상**:
- `get_{entity}s_usecase_test.dart`
- `get_{entity}_usecase_test.dart`
- `create_{entity}_usecase_test.dart`
- `update_{entity}_usecase_test.dart`
- `delete_{entity}_usecase_test.dart`

### BLoC Test

```bash
# BLoC 테스트 실행
melos exec --scope=feature_{feature_name} -- \
  flutter test test/presentation/bloc/ --reporter expanded
```

**테스트 위치**: `feature/{location}/{feature_name}/test/presentation/bloc/`

**테스트 대상**:
- `{feature}_list_bloc_test.dart`
- `{feature}_detail_bloc_test.dart`
- `{feature}_form_bloc_test.dart`

### BDD Widget Test

```bash
# BDD Widget 테스트 실행
melos exec --scope=feature_{feature_name} -- \
  flutter test test/src/bdd/ --reporter expanded
```

**테스트 위치**: `feature/{location}/{feature_name}/test/src/bdd/`

**테스트 대상**:
- `{feature}_list.feature` + steps
- `{feature}_detail.feature` + steps
- `{feature}_form.feature` + steps

---

## 실행 흐름

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 테스트 환경 준비                                  │
├─────────────────────────────────────────────────────────┤
│  $ melos run build                                      │
│  - 코드 생성 완료 확인                                     │
│  - 분석 오류 없음 확인                                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: Unit Test 실행                                  │
├─────────────────────────────────────────────────────────┤
│  $ melos exec --scope=feature_{name} --                 │
│      flutter test test/domain/usecase/                  │
│  - UseCase 로직 검증                                     │
│  - Mock 설정 확인                                        │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: BLoC Test 실행                                  │
├─────────────────────────────────────────────────────────┤
│  $ melos exec --scope=feature_{name} --                 │
│      flutter test test/presentation/bloc/               │
│  - State 전환 검증                                       │
│  - Event 처리 검증                                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: BDD Widget Test 실행                            │
├─────────────────────────────────────────────────────────┤
│  $ melos exec --scope=feature_{name} --                 │
│      flutter test test/src/bdd/                         │
│  - Gherkin 시나리오 실행                                  │
│  - UI 상호작용 검증                                       │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 5: 결과 분석 및 자동 수정                             │
├─────────────────────────────────────────────────────────┤
│  IF 실패 테스트 있음:                                      │
│    - 실패 원인 분석                                       │
│    - 자동 수정 가능 여부 판단                               │
│    - 자동 수정 시도 (최대 3회)                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 6: 커버리지 생성 (선택)                               │
├─────────────────────────────────────────────────────────┤
│  $ melos run test:with-html-coverage                    │
│  - lcov 파일 생성                                        │
│  - HTML 리포트 생성                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 자동 수정 패턴

### 수정 가능한 실패 유형

| 실패 유형 | 원인 | 자동 수정 방법 |
|---------|------|--------------|
| Mock 누락 | when() 설정 없음 | Mock 설정 추가 |
| State 불일치 | 예상 State와 실제 다름 | State 값 업데이트 |
| Widget 못 찾음 | Key/Finder 잘못됨 | Finder 수정 |
| Import 누락 | 필요한 import 없음 | import 추가 |
| Timeout | 비동기 처리 지연 | pumpAndSettle 조정 |

### 수정 불가능한 실패 유형

| 실패 유형 | 이유 |
|---------|------|
| 로직 오류 | 비즈니스 로직 판단 필요 |
| 아키텍처 문제 | 설계 변경 필요 |
| 외부 의존성 | 외부 서비스 문제 |

### 자동 수정 흐름

```
1. 실패 메시지 파싱
   ↓
2. 실패 유형 분류
   ↓
3. 수정 가능 여부 판단
   ↓
4. 수정 코드 생성
   ↓
5. 수정 적용
   ↓
6. 테스트 재실행
   ↓
7. 성공/실패 확인
```

---

## Melos 스크립트 활용

### 단일 Feature 테스트

```bash
# 특정 Feature만 테스트
melos exec --scope=feature_{feature_name} -- flutter test

# 또는
melos run test --scope=feature_{feature_name}
```

### 커버리지 포함 테스트

```bash
# 커버리지와 함께 테스트
melos run test:with-html-coverage
```

### 특정 테스트 파일만 실행

```bash
# 단일 파일 테스트
melos exec --scope=feature_{feature_name} -- \
  flutter test test/domain/usecase/get_posts_usecase_test.dart
```

---

## 결과 리포트

### 콘솔 출력 형식

```
╔════════════════════════════════════════════════════════╗
║  Test Results: feature_community                       ║
╠════════════════════════════════════════════════════════╣
║  Unit Tests (UseCase):                                 ║
║    ✅ GetPostsUseCase: 5 passed                        ║
║    ✅ GetPostUseCase: 3 passed                         ║
║    ✅ CreatePostUseCase: 4 passed                      ║
║                                                        ║
║  BLoC Tests:                                           ║
║    ✅ PostListBloc: 8 passed                           ║
║    ✅ PostDetailBloc: 6 passed                         ║
║    ❌ PostFormBloc: 4 passed, 1 failed                 ║
║                                                        ║
║  BDD Widget Tests:                                     ║
║    ✅ community_list.feature: 7 scenarios passed       ║
║    ✅ community_detail.feature: 5 scenarios passed     ║
║                                                        ║
╠════════════════════════════════════════════════════════╣
║  Summary: 42/43 passed (97.7%)                         ║
║  Duration: 45.3s                                       ║
║  Coverage: 85.2% (lines)                               ║
╚════════════════════════════════════════════════════════╝
```

### 실패 상세 리포트

```
╔════════════════════════════════════════════════════════╗
║  Failed Test Details                                   ║
╠════════════════════════════════════════════════════════╣
║  File: post_form_bloc_test.dart                        ║
║  Test: should emit error state when validation fails   ║
║                                                        ║
║  Error:                                                ║
║    Expected: PostFormError(message: "Title required")  ║
║    Actual:   PostFormError(message: "제목을 입력하세요")  ║
║                                                        ║
║  Fixable: ✅ Yes (message mismatch)                    ║
║  Auto-fix: Applied                                     ║
╚════════════════════════════════════════════════════════╝
```

---

## 에러 처리

### 빌드 실패 시

```
1. 분석 오류 확인
2. 코드 생성 재실행
3. 여전히 실패 → 실패 보고
```

### 테스트 타임아웃

```
1. 개별 테스트 타임아웃: 30초
2. 전체 테스트 타임아웃: 10분
3. 타임아웃 시 → 해당 테스트 스킵 후 계속
```

---

## 핵심 규칙

1. **빌드 우선**: 테스트 전 빌드 성공 확인
2. **순서 준수**: Unit → BLoC → BDD 순서로 실행
3. **자동 수정 제한**: 최대 3회까지만 시도
4. **실패 허용**: 수정 불가 시 스킵하고 보고
5. **커버리지 목표**: 최소 80% 라인 커버리지
6. **상세 로그**: 모든 실패에 대한 상세 정보 제공

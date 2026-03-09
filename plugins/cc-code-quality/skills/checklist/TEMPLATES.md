# Checklist Templates

Feature Complete 및 PR Review 체크리스트 템플릿입니다.

---

## Template A: Feature Complete 체크리스트

```markdown
# Feature Complete: [feature_name]

## 1. 구조 검증

### Domain Layer
- [ ] Entity 정의 완료 (Freezed)
- [ ] Repository Interface 정의 (I prefix)
- [ ] UseCase 구현 완료
- [ ] Failure 클래스 정의
- [ ] 단위 테스트 작성

### Data Layer
- [ ] Repository 구현체 완료
- [ ] Serverpod Mixin 구현 (필요시)
- [ ] Local Database 구현 (필요시)
- [ ] DTO ↔ Entity 매퍼 구현
- [ ] 캐싱 전략 적용 (SWR/Cache-First)

### Presentation Layer
- [ ] Page 위젯 구현
- [ ] 재사용 Widget 분리
- [ ] BLoC/Cubit 구현
- [ ] Event/State 정의 (Freezed)
- [ ] Widget 테스트 작성

### DI & Routing
- [ ] Injectable 어노테이션 추가
- [ ] Route 정의 (Auto_route)
- [ ] Route Guard 적용 (필요시)

## 2. 코드 생성
- [ ] Freezed 코드 생성됨 (*.freezed.dart)
- [ ] Injectable 코드 생성됨 (*.g.dart)
- [ ] Route 코드 생성됨
- [ ] 빌드 에러 없음

## 3. 테스트
- [ ] UseCase 테스트 (Happy path, Error, Edge cases)
- [ ] Repository 테스트 (mocked data source)
- [ ] BLoC 테스트 (초기/이벤트/에러)
- [ ] Widget 테스트 (렌더링/인터랙션)
- [ ] 모든 테스트 통과
- [ ] 커버리지 80% 이상

## 4. 문서화
- [ ] 공개 API에 dartdoc 주석
- [ ] 복잡한 로직에 설명 주석
- [ ] TODO 주석 해결 또는 이슈 등록

## 5. 국제화
- [ ] 모든 UI 텍스트 번역 키 사용
- [ ] 번역 파일 업데이트
- [ ] 복수형/파라미터 처리 확인

## 6. 성능 최적화
- [ ] const 위젯 활용
- [ ] BlocBuilder buildWhen 적용
- [ ] ListView.builder 사용 (긴 리스트)
- [ ] 이미지 cacheWidth/cacheHeight 적용
- [ ] dispose에서 리소스 해제

## 7. 보안 검토
- [ ] 민감 정보 하드코딩 없음
- [ ] 입력 값 검증 적용
- [ ] 적절한 에러 메시지

## 8. 접근성
- [ ] Semantics label 적용
- [ ] 터치 타겟 크기 확인 (48x48 이상)
- [ ] 색상 대비 확인

## 9. 정적 분석
- [ ] Lint 경고 없음
- [ ] 코드 포맷팅 완료

## 10. 통합 검증
- [ ] iOS 빌드 성공
- [ ] Android 빌드 성공
- [ ] 개발 환경에서 정상 동작

## 11. PR 준비
- [ ] 의미 있는 커밋 메시지 (한글, Conventional + Gitmoji)
- [ ] 관련 이슈 연결
- [ ] 리뷰어 지정

## 완료 요약

| 항목 | 상태 |
|------|------|
| 구조 검증 | ⬜ |
| 코드 생성 | ⬜ |
| 테스트 | ⬜ |
| 문서화 | ⬜ |
| 국제화 | ⬜ |
| 성능 최적화 | ⬜ |
| 보안 검토 | ⬜ |
| 접근성 | ⬜ |
| 정적 분석 | ⬜ |
| 통합 검증 | ⬜ |
| PR 준비 | ⬜ |
```

---

## Template B: PR Review 체크리스트

```markdown
# PR Review: [PR 제목]

**PR**: #[번호]
**리뷰어**: [이름]
**날짜**: [YYYY-MM-DD]

## Quick Review (5분 리뷰)

- [ ] 빌드 성공 여부 (CI)
- [ ] 테스트 통과 여부
- [ ] Lint 검사 통과
- [ ] 보안 이슈 없음
- [ ] Breaking Changes 확인

## Full Review Checklist

### 1. PR 메타 정보
- [ ] PR 제목이 컨벤션을 따름
- [ ] 관련 이슈가 연결됨
- [ ] 적절한 라벨이 지정됨

### 2. 변경 사항 범위
- [ ] PR의 목적이 명확함
- [ ] 단일 목적에 집중됨
- [ ] 변경 범위가 적절함
- [ ] 불필요한 파일 변경 없음

### 3. 코드 품질
- [ ] Clean Architecture 레이어 분리 준수
- [ ] 의존성 방향 올바름
- [ ] Feature 모듈 간 의존성 없음
- [ ] 의미 있는 변수/함수명
- [ ] 중복 코드 없음 (DRY)

### 4. 상태 관리 (BLoC)
- [ ] Event/State Freezed 사용
- [ ] 적절한 상태 분리
- [ ] 에러 처리 구현
- [ ] 로딩 상태 처리
- [ ] dispose에서 리소스 해제

### 5. 테스트
- [ ] 새 기능에 대한 테스트 추가
- [ ] 기존 테스트 통과
- [ ] Edge case 테스트 포함

### 6. 보안
- [ ] 하드코딩된 시크릿 없음
- [ ] 민감 정보 로깅 없음
- [ ] 입력 값 검증 적용

### 7. 성능
- [ ] N+1 쿼리 문제 없음
- [ ] 불필요한 리렌더링 방지
- [ ] 이미지 최적화 적용

### 8. 국제화
- [ ] 하드코딩된 문자열 없음
- [ ] 번역 키 추가됨

### 9. 접근성
- [ ] Semantic label 적용
- [ ] 터치 타겟 크기 적절

### 10. 문서화
- [ ] 공개 API 문서화
- [ ] Breaking Changes 문서화

## 리뷰 결과

**결과**: ✅ Approved / 🔄 Request Changes / 💬 Comment

**요약**:
[리뷰 요약 작성]
```

---

## Template C: 리뷰 코멘트 템플릿

### 필수 수정 (Blocking)

```markdown
🔴 **[필수]** {제목}

**위치**: `{파일}:{라인}`

**문제**: {문제 설명}

**제안**:
```dart
// 수정 코드
```

이 이슈가 해결되기 전까지 머지할 수 없습니다.
```

### 개선 요청 (Non-blocking)

```markdown
🟡 **[개선]** {제목}

**위치**: `{파일}:{라인}`

**현재 코드**:
```dart
// 현재 코드
```

**권장 코드**:
```dart
// 개선된 코드
```

{개선 이유 설명}
```

### 제안/질문

```markdown
🟢 **[제안]** {제목}

**위치**: `{파일}:{라인}`

{질문 또는 제안 내용}
```

### 칭찬

```markdown
✨ **좋아요!** {제목}

**위치**: `{파일}:{라인}`

{칭찬 내용}
```

---

## Template D: 리뷰 결과 템플릿

### Approve

```markdown
LGTM! 🎉

모든 체크리스트 항목 확인 완료했습니다.

**확인 항목**:
- ✅ 빌드 성공
- ✅ 테스트 통과
- ✅ 보안 이슈 없음
- ✅ 코드 품질 양호

좋은 작업입니다!
```

### Request Changes

```markdown
수정 요청 사항이 있습니다.

**필수 수정** (머지 전 해결 필요):
1. {항목 1} - `{파일}:{라인}`
2. {항목 2} - `{파일}:{라인}`

**권장 수정** (선택적):
1. {항목 1}
2. {항목 2}

필수 수정 사항 해결 후 다시 리뷰 요청해 주세요.
```

### Comment

```markdown
전반적으로 좋습니다. 몇 가지 질문/제안이 있습니다.

**질문**:
1. {질문 1}
2. {질문 2}

**제안**:
1. {제안 1}
2. {제안 2}

확인 후 답변 부탁드립니다.
```

---

## Template E: 완료 요약 테이블

### Feature Complete 요약

```markdown
## 완료 요약: [feature_name]

| 항목 | 상태 | 비고 |
|------|------|------|
| 구조 검증 | ✅ | Domain/Data/Presentation 완료 |
| 코드 생성 | ✅ | Freezed, Injectable 생성됨 |
| 테스트 | ⚠️ | Widget 테스트 일부 누락 |
| 문서화 | ✅ | dartdoc 추가 완료 |
| 국제화 | ✅ | 번역 키 적용 완료 |
| 성능 최적화 | ✅ | const, buildWhen 적용 |
| 보안 검토 | ✅ | 하드코딩 없음 |
| 접근성 | ⚠️ | Semantics 일부 누락 |
| 정적 분석 | ✅ | Lint 통과 |
| 통합 검증 | ✅ | iOS/Android 빌드 성공 |
| PR 준비 | ✅ | 이슈 연결 완료 |

**전체 상태**: 🟡 일부 개선 필요 (테스트, 접근성)
```

### PR Review 요약

```markdown
## PR Review 요약: #[번호]

| 카테고리 | 상태 | 주요 이슈 |
|---------|------|----------|
| 메타 정보 | ✅ | - |
| 변경 범위 | ✅ | - |
| 코드 품질 | ⚠️ | 중복 코드 발견 |
| 상태 관리 | ✅ | - |
| 테스트 | ❌ | UseCase 테스트 누락 |
| 보안 | ✅ | - |
| 성능 | ⚠️ | buildWhen 미적용 |
| 국제화 | ✅ | - |
| 접근성 | ✅ | - |
| 문서화 | ✅ | - |

**리뷰 결과**: 🔄 Request Changes
**필수 수정**: UseCase 테스트 추가
```

---

## Template F: CI/CD 확인

```bash
# PR 체크 상태 확인
gh pr checks [PR_NUMBER]

# PR 웹에서 보기
gh pr view [PR_NUMBER] --web

# PR 상세 정보
gh pr view [PR_NUMBER]
```

### CI 결과 템플릿

```markdown
## CI/CD 상태

| 체크 | 상태 | 소요 시간 |
|------|------|----------|
| Build (iOS) | ✅ | 5m 32s |
| Build (Android) | ✅ | 4m 18s |
| Test | ✅ | 2m 45s |
| Lint | ✅ | 0m 58s |
| Coverage | ⚠️ 78% | - |

**전체 상태**: 🟡 Coverage 임계값(80%) 미달
```

---

## Template G: 커밋 메시지 가이드

### 형식

```
<type>(<scope>): <gitmoji> <한글 설명>

[optional body]
[optional footer]
```

### 예시

```
feat(auth): ✨ 소셜 로그인 기능 추가

카카오, 네이버, 구글 OAuth 연동 구현
- 토큰 저장 및 갱신 로직
- 자동 로그인 기능

Closes #123
```

```
fix(home): 🐛 피드 무한 스크롤 버그 수정

스크롤 끝 도달 시 API 중복 호출 문제 해결

Fixes #456
```

```
refactor(store): ♻️ 상품 목록 쿼리 최적화

N+1 쿼리 문제 해결 (30% 성능 개선)
```

### 타입

| 타입 | 설명 | 깃모지 |
|------|------|--------|
| feat | 새로운 기능 | ✨ |
| fix | 버그 수정 | 🐛 |
| refactor | 리팩토링 | ♻️ |
| test | 테스트 | ✅ |
| docs | 문서 | 📝 |
| chore | 설정/빌드 | 🔧 |
| style | 포맷팅 | 🎨 |
| perf | 성능 개선 | ⚡ |

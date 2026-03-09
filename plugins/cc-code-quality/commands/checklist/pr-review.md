---
name: checklist/pr-review
description: "PR 리뷰 시 확인해야 할 체크리스트"
invoke: /checklist:pr-review
aliases: ["/check:pr", "/pr:checklist"]
category: petmedi-development
complexity: moderate
mcp-servers: [serena]
---

# /checklist/pr-review

> **Context Framework Note**: PR 리뷰 시 활성화됩니다.

## Triggers

- Pull Request 리뷰 시
- 코드 리뷰 요청 시
- 머지 전 최종 확인

## 사용법

```
/checklist/pr-review [PR 번호 또는 링크]
```

## 🎯 Quick Review (5분 리뷰)

빠른 검토가 필요한 경우 최소한 확인할 항목:

- [ ] 빌드 성공 여부 (CI)
- [ ] 테스트 통과 여부
- [ ] Lint 검사 통과
- [ ] 보안 이슈 없음
- [ ] Breaking Changes 확인

## 📋 Full Review Checklist

### 1. PR 메타 정보

- [ ] PR 제목이 컨벤션을 따름
  - 형식: `type(scope): gitmoji 한글 설명`
- [ ] 관련 이슈가 연결됨
- [ ] 적절한 라벨이 지정됨

### 2. 변경 사항 범위

- [ ] PR의 목적이 명확함
- [ ] 단일 목적에 집중됨 (한 PR = 한 기능/수정)
- [ ] 변경 범위가 적절함
- [ ] 불필요한 파일 변경 없음

### 3. 코드 품질

#### 아키텍처
- [ ] Clean Architecture 레이어 분리 준수
- [ ] 의존성 방향 올바름 (Domain ← Data ← Presentation)
- [ ] Feature 모듈 간 의존성 없음

#### 네이밍 & 가독성
- [ ] 의미 있는 변수/함수명
- [ ] 프로젝트 네이밍 컨벤션 준수
- [ ] 적절한 주석

#### 코드 구조
- [ ] 중복 코드 없음 (DRY)
- [ ] 단일 책임 원칙 준수
- [ ] 적절한 추상화 수준

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
- [ ] 적절한 캐싱 전략

### 8. 국제화

- [ ] 하드코딩된 문자열 없음
- [ ] 번역 키 추가됨

### 9. 접근성

- [ ] Semantic label 적용
- [ ] 터치 타겟 크기 적절

### 10. 문서화

- [ ] 공개 API 문서화
- [ ] Breaking Changes 문서화

## 리뷰 우선순위

### 🔴 Must-Have (Approve 불가)

1. **빌드 실패**
2. **테스트 실패**
3. **보안 취약점**
4. **Breaking Change 미문서화**
5. **Architecture 위반**

### 🟡 Should-Have (개선 요청 후 Approve 가능)

1. 성능 최적화 미비
2. 테스트 커버리지 부족
3. 문서화 부족
4. 접근성 미비

### 🟢 Nice-to-Have (코멘트만)

1. 네이밍 개선 제안
2. 코드 스타일 제안
3. 추가 최적화 제안

## 리뷰 코멘트 템플릿

### 필수 수정 (Blocking)
```
🔴 **[필수]** {설명}

{코드 위치}: {파일}:{라인}

**문제**: {문제 설명}
**제안**: {해결 방안}
```

### 개선 요청 (Non-blocking)
```
🟡 **[개선]** {설명}

{코드 위치}: {파일}:{라인}

**현재**: {현재 코드}
**제안**: {개선 코드}
```

### 제안/질문
```
🟢 **[제안]** {설명}

{코드 위치}: {파일}:{라인}

**질문/제안**: {내용}
```

### 칭찬
```
✨ **좋아요!** {설명}

{코드 위치}: {파일}:{라인}

{칭찬 내용}
```

## 리뷰 결과 템플릿

### Approve ✅
```
LGTM! 🎉

모든 체크리스트 항목 확인 완료.
- 빌드 성공
- 테스트 통과
- 보안 이슈 없음
```

### Request Changes 🔄
```
수정 요청 사항이 있습니다.

**필수 수정** (머지 전 해결 필요):
1. {항목 1}
2. {항목 2}

**권장 수정** (선택적):
1. {항목 1}
```

### Comment 💬
```
전반적으로 좋습니다. 몇 가지 질문/제안이 있습니다.

**질문**:
1. {질문 1}

**제안**:
1. {제안 1}
```

## CI/CD 확인

```bash
gh pr checks [PR_NUMBER]
gh pr view [PR_NUMBER] --web
```

- [ ] Build 성공
- [ ] Test 성공
- [ ] Lint 성공
- [ ] Coverage 체크

## 참조

- 상세 체크리스트: `.claude/checklists/pr-review.md`
- Feature 완료 체크리스트: `.claude/commands/checklist/feature-complete.md`
- 코드 리뷰 스킬: `.claude/commands/code-review.md`

# PR Lifecycle Agent

> PR 생성부터 머지까지 전체 라이프사이클 관리 에이전트

## 역할 및 책임

이 에이전트는 Pull Request의 전체 라이프사이클을 관리합니다.

1. **PR 생성**: 이슈 연결된 PR 생성
2. **리뷰 대기**: Gemini/Claude 자동 리뷰 코멘트 대기 (5분)
3. **피드백 반영**: 리뷰 코멘트 분석 및 코드 수정
4. **머지 실행**: CI 통과 후 스쿼시 머지

---

## 입력 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `branch_name` | ✅ | string | 소스 브랜치명 |
| `issue_number` | ✅ | number | 연결할 이슈 번호 |
| `issue_title` | ✅ | string | PR 제목용 이슈 제목 |
| `issue_type` | ❌ | string | `Feature` \| `Bug` \| `Task` (기본: `Feature`) |
| `base_branch` | ❌ | string | 대상 브랜치 (기본: `development`) |
| `auto_merge` | ❌ | boolean | 자동 머지 여부 (기본: true) |

---

## 출력

```typescript
interface PRResult {
  success: boolean;
  pr_number: number;
  pr_url: string;
  pr_status: 'open' | 'merged' | 'closed';
  review_comments: ReviewComment[];
  ci_status: 'passed' | 'failed' | 'pending';
  merged_at?: string;
  error?: string;
}

interface ReviewComment {
  author: string;
  body: string;
  file_path?: string;
  line?: number;
  resolved: boolean;
}
```

---

## PR 제목 규칙

### 형식

```
{type}({scope}): {gitmoji} {한글 설명}
```

### 타입별 매핑

| 이슈 타입 | PR 타입 | Gitmoji |
|---------|--------|---------|
| Feature | feat | ✨ |
| Bug | fix | 🐛 |
| Task | chore | 🔧 |
| Sub-task | feat/fix/chore | 상황별 |

### 예시

```
feat(community): ✨ 게시글 목록 화면 구현
fix(auth): 🐛 로그인 토큰 갱신 오류 수정
chore(deps): 🔧 패키지 버전 업데이트
```

---

## PR 본문 템플릿

```markdown
## Summary
{이슈 내용 요약 - 1~3줄}

## Changes
- {변경사항 1}
- {변경사항 2}
- {변경사항 3}

## Test Plan
- [ ] Unit 테스트 통과
- [ ] BLoC 테스트 통과
- [ ] BDD Widget 테스트 통과
- [ ] 빌드 성공

## Screenshots (if applicable)
{스크린샷 또는 N/A}

---
Closes #{issue_number}

🤖 Generated with [Claude Code](https://claude.ai/claude-code)
```

---

## 실행 흐름

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: PR 생성 준비                                     │
├─────────────────────────────────────────────────────────┤
│  - 브랜치 푸시 확인                                        │
│  - 커밋 목록 수집                                         │
│  - PR 제목/본문 생성                                      │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: PR 생성                                         │
├─────────────────────────────────────────────────────────┤
│  $ git push -u origin {branch_name}                     │
│  $ gh pr create --title "..." --body "..."              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: 리뷰 대기 (5분)                                   │
├─────────────────────────────────────────────────────────┤
│  - Gemini, Claude 자동 리뷰 코멘트 대기                     │
│  - 30초 간격으로 코멘트 체크                                │
│  - 최대 5분 대기                                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: 리뷰 코멘트 수집 및 분석                           │
├─────────────────────────────────────────────────────────┤
│  $ gh pr view {pr_number} --comments                    │
│  - 코멘트 파싱                                            │
│  - 수정 필요 항목 추출                                     │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 5: 피드백 반영 (필요시)                               │
├─────────────────────────────────────────────────────────┤
│  IF 수정 필요 항목 있음:                                   │
│    - 코드 수정                                            │
│    - 추가 커밋                                            │
│    $ git commit -m "refactor: ♻️ PR 리뷰 피드백 반영"      │
│    $ git push                                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 6: CI 상태 확인                                     │
├─────────────────────────────────────────────────────────┤
│  $ gh pr checks {pr_number}                             │
│  - 모든 체크 통과 대기                                     │
│  - 실패 시 → 수정 시도 또는 보고                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 7: 스쿼시 머지                                       │
├─────────────────────────────────────────────────────────┤
│  $ gh pr merge {pr_number} --squash --delete-branch     │
│  - PR 머지 완료                                          │
│  - 소스 브랜치 삭제                                       │
└─────────────────────────────────────────────────────────┘
```

---

## 명령어 상세

### Step 2: PR 생성

```bash
# 브랜치 푸시
git push -u origin feature/25-community-list

# PR 생성
gh pr create \
  --title "feat(community): ✨ 게시글 목록 화면 구현" \
  --body "$(cat <<'EOF'
## Summary
Community 게시글 목록 화면 구현

## Changes
- PostEntity 및 UseCase 구현
- PostListBloc 상태 관리 구현
- PostListPage UI 구현

## Test Plan
- [x] Unit 테스트 통과
- [x] BLoC 테스트 통과
- [x] BDD Widget 테스트 통과
- [x] 빌드 성공

---
Closes #25

🤖 Generated with [Claude Code](https://claude.ai/claude-code)
EOF
)" \
  --base development
```

### Step 3: 리뷰 대기

```bash
# 5분 동안 30초 간격으로 체크
for i in {1..10}; do
  sleep 30
  COMMENTS=$(gh pr view $PR_NUMBER --comments --json comments -q '.comments | length')
  if [ "$COMMENTS" -gt 0 ]; then
    break
  fi
done
```

### Step 4: 리뷰 코멘트 수집

```bash
# 코멘트 조회
gh pr view $PR_NUMBER --comments --json comments

# 리뷰 코멘트 조회
gh api repos/{owner}/{repo}/pulls/$PR_NUMBER/comments
```

### Step 6: CI 상태 확인

```bash
# CI 체크 상태 확인
gh pr checks $PR_NUMBER

# 체크 통과 대기 (최대 10분)
gh pr checks $PR_NUMBER --watch --fail-fast
```

### Step 7: 스쿼시 머지

```bash
# 스쿼시 머지 + 브랜치 삭제
gh pr merge $PR_NUMBER --squash --delete-branch

# 머지 커밋 메시지 (PR 제목 사용)
# "feat(community): ✨ 게시글 목록 화면 구현 (#25)"
```

---

## 리뷰 코멘트 분석

### 코멘트 유형 분류

| 유형 | 키워드 | 처리 방법 |
|------|--------|---------|
| 필수 수정 | `must`, `required`, `fix` | 즉시 수정 |
| 권장 수정 | `should`, `consider`, `suggest` | 가능하면 수정 |
| 질문 | `?`, `why`, `how` | 답변 또는 코드 주석 |
| 승인 | `LGTM`, `approved`, `good` | 수정 불필요 |

### 자동 반영 가능 항목

- 코드 스타일 수정 (포맷팅)
- 네이밍 변경
- Import 정리
- 주석 추가
- 간단한 로직 수정

### 수동 확인 필요 항목

- 아키텍처 변경 제안
- 비즈니스 로직 변경
- 성능 최적화 제안
- 보안 관련 이슈

---

## CI 체크 처리

### 통과해야 할 체크

| 체크 | 설명 | 실패 시 |
|------|------|--------|
| `build` | 빌드 성공 | 빌드 오류 수정 |
| `test` | 테스트 통과 | 테스트 수정 |
| `lint` | 린트 통과 | 포맷팅/린트 수정 |
| `analyze` | 정적 분석 | 분석 오류 수정 |

### 실패 시 처리

```
1. 실패 원인 분석
   ↓
2. 자동 수정 가능 여부 판단
   ↓
3. 수정 적용
   ↓
4. 커밋 & 푸시
   ↓
5. CI 재실행 대기
   ↓
6. 성공/실패 확인
```

---

## 에러 처리

### 일반적인 에러

| 에러 | 원인 | 해결 |
|------|------|------|
| `PR already exists` | 동일 브랜치 PR 존재 | 기존 PR 업데이트 |
| `merge conflict` | 베이스 브랜치와 충돌 | 충돌 해결 필요 |
| `checks failed` | CI 실패 | 수정 후 재시도 |
| `review required` | 리뷰 승인 필요 | 리뷰 대기 |

### 복구 전략

```bash
# 충돌 해결
git fetch origin development
git rebase origin/development
# 충돌 수동 해결
git add .
git rebase --continue
git push --force-with-lease
```

---

## Post-Merge 체크 ⚠️

PR 머지 후 development 브랜치에서 다음을 확인합니다.

### Backend 변경 감지

머지된 커밋에 다음 파일이 포함된 경우 Backend 코드 생성이 필요합니다:

| 파일 패턴 | 의미 |
|----------|------|
| `backend/kobic_server/lib/src/protocol/**/*.spy.yaml` | 모델 파일 변경 |
| `backend/kobic_server/lib/src/feature/**/*.dart` | 엔드포인트/서비스 변경 |

### 자동 실행

```bash
# 1. development 브랜치 최신화
git checkout development
git pull origin development

# 2. Backend 변경 감지 시 코드 생성 [필수]
melos run backend:pod:generate

# 3. 생성된 코드 커밋 (변경사항 있는 경우)
git add .
git commit -m "chore(backend): 🔧 코드 생성"
git push origin development
```

### ⚠️ 중요

**다른 브랜치에서 development를 머지받을 때도 동일하게 적용:**

```bash
# feature 브랜치에서 development 머지 후
git merge development

# Backend 변경이 있었다면 코드 생성 실행
melos run backend:pod:generate
```

이 단계를 생략하면:
- kobic_client와 kobic_server 간 타입 불일치
- 프론트엔드에서 새로운 API 호출 불가
- 빌드 오류 발생

---

## 핵심 규칙

1. **제목 규칙 준수**: Conventional Commits + Gitmoji + 한글
2. **이슈 연결 필수**: `Closes #이슈번호` 항상 포함
3. **리뷰 대기**: 5분간 자동 리뷰 코멘트 대기
4. **피드백 반영**: 리뷰 코멘트 분석 및 자동 반영
5. **스쿼시 머지**: 항상 스쿼시 머지로 히스토리 정리
6. **브랜치 정리**: 머지 후 소스 브랜치 자동 삭제
7. **Backend 코드 생성**: 머지 후 backend 변경 시 `backend:pod:generate` 실행

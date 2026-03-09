# Issue Branch Agent

> 이슈 기반 브랜치 생성 및 체크아웃 에이전트

## 역할 및 책임

이 에이전트는 ZenHub/GitHub 이슈를 기반으로 Git 브랜치를 생성하고 체크아웃합니다.

1. **브랜치명 생성**: 이슈 번호와 제목 기반 브랜치명 자동 생성
2. **안전한 체크아웃**: 현재 작업 상태 확인 후 안전하게 브랜치 전환
3. **베이스 브랜치 동기화**: development 브랜치 최신화 후 분기

---

## 입력 파라미터

| 파라미터 | 필수 | 타입 | 설명 |
|---------|------|------|------|
| `issue_number` | ✅ | number | GitHub 이슈 번호 |
| `issue_title` | ✅ | string | 이슈 제목 |
| `issue_type` | ❌ | string | `feature` \| `bugfix` \| `hotfix` (기본: `feature`) |
| `base_branch` | ❌ | string | 베이스 브랜치 (기본: `development`) |

---

## 출력

```typescript
interface BranchResult {
  success: boolean;
  branch_name: string;
  base_branch: string;
  error?: string;
}
```

---

## 브랜치 명명 규칙

### 형식
```
{type}/{issue_number}-{slug}
```

### 타입별 접두사

| 이슈 타입 | 브랜치 타입 | 예시 |
|---------|-----------|------|
| Feature | `feature` | `feature/25-community-list` |
| Bug | `bugfix` | `bugfix/30-fix-login-error` |
| Hotfix | `hotfix` | `hotfix/35-critical-security-fix` |
| Task | `feature` | `feature/28-entity-definition` |
| Sub-task | `feature` | `feature/29-usecase-implementation` |

### Slug 생성 규칙

1. **한글 제거**: 영문만 추출
2. **소문자 변환**: 모든 문자 소문자로
3. **특수문자 제거**: 알파벳, 숫자만 유지
4. **공백 → 하이픈**: 단어 구분
5. **최대 길이**: 50자 제한

```typescript
function createSlug(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^\w\s-]/g, '')  // 특수문자 제거
    .replace(/[\s_]+/g, '-')    // 공백/언더스코어 → 하이픈
    .replace(/-+/g, '-')        // 연속 하이픈 제거
    .substring(0, 50)           // 길이 제한
    .replace(/^-|-$/g, '');     // 앞뒤 하이픈 제거
}
```

---

## 실행 흐름

```
┌─────────────────────────────────────────────────────────┐
│  Step 1: 현재 상태 확인                                    │
├─────────────────────────────────────────────────────────┤
│  $ git status                                           │
│  - 커밋되지 않은 변경사항 확인                               │
│  - stash 필요 여부 판단                                    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 2: 변경사항 처리                                     │
├─────────────────────────────────────────────────────────┤
│  IF 변경사항 있음:                                         │
│    $ git stash push -m "WIP: before #{issue_number}"    │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 3: 베이스 브랜치 동기화                                │
├─────────────────────────────────────────────────────────┤
│  $ git checkout development                             │
│  $ git pull origin development                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 4: 브랜치 생성 및 체크아웃                             │
├─────────────────────────────────────────────────────────┤
│  $ git checkout -b {branch_name}                        │
│  - 기존 브랜치 존재 시 → 체크아웃만                          │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Step 5: 결과 확인                                        │
├─────────────────────────────────────────────────────────┤
│  $ git branch --show-current                            │
│  - 브랜치 생성 성공 여부 확인                                │
└─────────────────────────────────────────────────────────┘
```

---

## 명령어 상세

### Step 1: 상태 확인

```bash
# 현재 상태 확인
git status --porcelain

# 출력이 비어있지 않으면 변경사항 있음
```

### Step 2: Stash 처리

```bash
# 변경사항 임시 저장
git stash push -m "WIP: before issue #{issue_number}"

# stash 목록 확인
git stash list
```

### Step 3: 베이스 브랜치 동기화

```bash
# development로 이동
git checkout development

# 최신화
git pull origin development --rebase
```

### Step 4: 브랜치 생성

```bash
# 브랜치 존재 여부 확인
git rev-parse --verify {branch_name} 2>/dev/null

# 존재하지 않으면 생성
git checkout -b {branch_name}

# 존재하면 체크아웃만
git checkout {branch_name}
```

### Step 5: 결과 확인

```bash
# 현재 브랜치 확인
git branch --show-current

# 예상 브랜치와 일치하는지 확인
```

---

## 에러 처리

### 일반적인 에러

| 에러 | 원인 | 해결 |
|------|------|------|
| `uncommitted changes` | 커밋되지 않은 변경 | stash 처리 |
| `branch already exists` | 동일 브랜치 존재 | 기존 브랜치 체크아웃 |
| `merge conflict` | pull 시 충돌 | 충돌 해결 필요 알림 |
| `not a git repository` | git 저장소 아님 | 오류 반환 |

### 복구 전략

```bash
# stash 복구 (작업 완료 후)
git stash pop

# stash 목록에서 특정 항목 복구
git stash apply stash@{0}
```

---

## 사용 예시

### 기본 사용

```bash
# Feature 이슈
/workflow:issue-branch 25 "Community 목록 화면"

# 결과
branch_name: feature/25-community-list
```

### 버그 수정

```bash
# Bug 이슈
/workflow:issue-branch 30 "로그인 오류 수정" --type bugfix

# 결과
branch_name: bugfix/30-login-error
```

### 한글 제목 처리

```bash
# 한글 제목
/workflow:issue-branch 28 "[Story] Community 엔티티 정의"

# 결과 (한글 제거, 특수문자 제거)
branch_name: feature/28-story-community-entity
```

---

## 통합 시나리오

### /workflow:issue-cycle에서 호출

```
1. issue-cycle이 이슈 정보 조회
   ↓
2. issue-branch-agent 호출
   - issue_number: 25
   - issue_title: "Community 목록 화면"
   - issue_type: feature
   ↓
3. 브랜치 생성 완료
   - branch_name: feature/25-community-list
   ↓
4. implementation-agent로 전달
```

---

## 핵심 규칙

1. **안전 우선**: 항상 현재 상태 확인 후 작업
2. **Stash 활용**: 변경사항 있으면 stash로 보존
3. **최신 베이스**: development 최신화 후 분기
4. **일관된 명명**: 브랜치 명명 규칙 엄격 준수
5. **멱등성**: 같은 이슈로 다시 호출해도 안전하게 동작
6. **영문 slug**: 브랜치명에 한글 사용 금지

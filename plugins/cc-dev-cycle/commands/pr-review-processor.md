# PR 코드 리뷰 자동 처리

PR에 달린 AI 코드 리뷰(Claude, Gemini)를 자동으로 검토하고 반영합니다.

## 사용법

```
/pr-review-processor [PR번호]
```

## 워크플로우

### 1. 리뷰 수집
```bash
gh api repos/{owner}/{repo}/pulls/{pr_number}/comments
```

### 2. 리뷰 분석
각 리뷰 코멘트에 대해:
- **유효한 리뷰**: 코드 품질, UX, 성능, 보안 개선 제안
- **무효한 리뷰**: 프로젝트 컨벤션과 충돌하는 제안

### 3. 조치
- 유효한 리뷰 → 코드 수정 및 커밋
- 무효한 리뷰 → CLAUDE.md에 규칙 추가 (향후 방지)

### 4. 완료
- 변경사항 푸시
- 처리 결과 요약

## 리뷰어 식별

| 리뷰어 | 식별자 |
|--------|--------|
| Gemini | `gemini-code-assist[bot]` |
| Claude | `claude[bot]` |
| Copilot | `github-copilot[bot]` |

## 우선순위

리뷰 우선순위 아이콘:
- 🔴 `critical` - 즉시 수정 필요
- 🟠 `high` - 높은 우선순위
- 🟡 `medium` - 중간 우선순위
- 🟢 `low` - 낮은 우선순위

## 자동 거부 조건

다음 경우 리뷰를 무시하고 CLAUDE.md 규칙 추가:
- 프로젝트 린트 규칙과 충돌
- 기존 아키텍처 패턴과 불일치
- 성능 저하를 유발하는 제안

---
name: code-review
description: "8개 카테고리 기반 체계적 코드 리뷰"
invoke: /code-review
aliases: ["/review", "/pr:review"]
category: petmedi-development
complexity: moderate
mcp-servers: [serena, context7]
---

# /code-review

> **Context Framework Note**: 코드 리뷰 및 품질 검토 시 활성화됩니다.

## Triggers

- PR 리뷰 요청 시
- 코드 품질 검토 시
- 커밋 전 자체 리뷰 시

## Context Trigger Pattern

```
/code-review {target} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `target` | ✅ | 리뷰 대상 | 파일 경로, PR 링크 |
| `--focus` | ❌ | 집중 카테고리 | `security`, `performance` |
| `--quick` | ❌ | 빠른 리뷰 모드 | |
| `--verbose` | ❌ | 상세 리뷰 모드 | |
| `--no-suppress` | ❌ | suppression 비활성화 | |
| `--gate-mode` | ❌ | Review Gate 모드 (Critical/Informational 분리 출력) | |

## Suppression List

리뷰 시 false positive를 줄이기 위해 suppression 규칙을 자동 적용합니다.

### 로딩 순서
1. 플러그인 기본: `cc-code-quality/rules/suppression.md`
2. 프로젝트 커스텀: 프로젝트 루트 `.code-review-suppress.md` (있을 경우)

### 적용 방식
- 각 리뷰 지적 항목을 suppression 목록과 대조
- 매칭 시 해당 항목을 리뷰 결과에서 제외
- `--no-suppress` 옵션으로 비활성화 가능

### 결과 표시
```
## Suppressed (3건 제외)
- [가독성] Freezed generated 코드 패턴 (suppression: 코드 생성 관련)
- [성능] const 미적용 (suppression: 스타일/컨벤션 관련)
- [아키텍처] melos import 경로 (suppression: 프로젝트 구조 관련)
```

## Review Categories

### 1. 🏗️ 아키텍처 (Architecture)

- Clean Architecture 레이어 분리 준수
- Domain → Data → Presentation 의존성 방향
- UseCase를 통한 비즈니스 로직 접근
- Repository 인터페이스 분리
- Feature 모듈 독립성

### 2. 🧩 상태 관리 (State Management)

- BLoC/Cubit 패턴 준수
- Event → BLoC → State 흐름
- Freezed로 불변 상태 정의
- 적절한 에러 핸들링
- 로딩 상태 관리

### 3. 🔒 보안 (Security)

- API 키, 시크릿 하드코딩 없음
- 로그에 민감 정보 출력 없음
- 사용자 입력 sanitization
- 인증/인가 적절히 적용

### 4. ⚡ 성능 (Performance)

- const 위젯 활용
- BlocBuilder buildWhen 사용
- 이미지 cacheWidth/cacheHeight 적용
- dispose에서 리소스 해제
- Stream subscription 취소

### 5. 🧪 테스트 (Testing)

- UseCase 단위 테스트
- Repository 테스트 (mocked)
- BLoC 테스트
- Edge case 커버
- Arrange-Act-Assert 패턴

### 6. 📖 가독성 (Readability)

- 명확하고 의미 있는 네이밍
- 프로젝트 컨벤션 준수
- 적절한 파일/클래스 크기
- 단일 책임 원칙
- 중복 코드 제거

### 7. 🌐 국제화 (i18n)

- 모든 UI 텍스트 번역 키 사용
- context.t.* 패턴 사용
- 적절한 복수형 처리
- 동적 값 파라미터화

### 8. ♿ 접근성 (Accessibility)

- 적절한 semantic label
- 최소 48x48 터치 타겟
- WCAG 색상 대비 기준 충족

## Review Output Template

```markdown
## Summary

**Overall**: ⭐⭐⭐⭐☆ (4/5)

| 카테고리 | 점수 | 주요 이슈 |
|---------|------|----------|
| 아키텍처 | ✅ | - |
| 상태 관리 | ⚠️ | BlocBuilder 최적화 필요 |
| 보안 | ✅ | - |
| 성능 | ⚠️ | 이미지 캐시 크기 미지정 |
| 테스트 | ❌ | UseCase 테스트 누락 |
| 가독성 | ✅ | - |
| 국제화 | ✅ | - |
| 접근성 | ⚠️ | semantic label 일부 누락 |

### Critical Issues 🔴

1. **[보안]** API 키가 하드코딩됨
   - 파일: `lib/core/config.dart:15`
   - 수정: Envied를 통한 환경 변수 사용

### Improvements 🟡

1. **[성능]** 이미지 캐시 크기 지정 필요
   - 파일: `lib/presentation/widget/product_card.dart:42`
   - 권장: `cacheWidth: 200` 추가

### Suggestions 🟢

1. **[가독성]** 변수명 개선 제안
   - `data` → `userProfile`

### Suppressed (N건 제외)
> suppression 규칙에 의해 제외된 항목입니다. `--no-suppress`로 전체 확인 가능합니다.
```

## Gate Mode Output (--gate-mode)

`/code-review --gate-mode` 실행 시 워크플로우 게이트용 구조화된 출력:

```markdown
## Code Review Gate Result

**Status**: ✅ PASS / ❌ BLOCKED

### Critical Issues (Pass 1) 🔴
> PR 생성을 차단하는 이슈

| # | 카테고리 | 이슈 | 파일 | 자동수정 |
|---|---------|------|------|---------|
| 1 | 보안 | API 키 하드코딩 | config.dart:15 | ✅ 가능 |

### Informational (Pass 2) 📋
> PR body에 포함될 개선 제안

| # | 카테고리 | 이슈 | 파일 |
|---|---------|------|------|
| 1 | 성능 | 이미지 캐시 미지정 | product_card.dart:42 |

### Summary
- Critical: 0건 → ✅ Gate 통과
- Informational: 3건 → PR body에 포함
- Suppressed: 2건 → 제외됨
```

## Automation Commands

```bash
# Lint 검사
melos run analyze
melos run lint:parallel

# 테스트 실행
melos run test
melos run test:with-html-coverage

# 포맷팅 검사
melos run format
```

## MCP Integration

| 단계 | MCP 서버 | 용도 |
|------|----------|------|
| 코드 분석 | Serena | 심볼 및 참조 검색 |
| 패턴 검증 | Context7 | 베스트 프랙티스 확인 |

## Examples

### 파일 리뷰

```
/code-review feature/auth/lib/src/presentation/bloc/login_bloc.dart
```

### 보안 집중 리뷰

```
/code-review feature/auth/ --focus security
```

### 빠른 리뷰

```
/code-review . --quick
```

## 참조

- 상세 체크리스트: `.claude/prompts/code-review.md`
- PR 리뷰 가이드: `.claude/checklists/pr-review.md`

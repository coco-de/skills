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

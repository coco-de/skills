---
name: code-review
description: 체계적인 코드 리뷰를 위한 8개 카테고리 체크리스트. 아키텍처, 상태 관리, 보안, 성능, 테스트, 가독성, 국제화, 접근성 검토.
---

# Code Review

체계적인 코드 리뷰를 위한 마스터 스킬입니다. 8개 핵심 카테고리를 기반으로 품질을 평가합니다.

## Scope and Capabilities

### 리뷰 카테고리

| 카테고리 | 아이콘 | 주요 검토 항목 |
|---------|--------|---------------|
| 아키텍처 | 🏗️ | Clean Architecture, 레이어 분리, 의존성 |
| 상태 관리 | 🧩 | BLoC 패턴, Freezed, 사이드 이펙트 |
| 보안 | 🔒 | 시크릿 노출, 입력 검증, 인증 |
| 성능 | ⚡ | 리빌드 최적화, 이미지, 메모리 |
| 테스트 | 🧪 | 커버리지, 테스트 품질, Mocking |
| 가독성 | 📖 | 네이밍, 코드 구조, 주석 |
| 국제화 | 🌐 | 하드코딩 문자열, 복수형 |
| 접근성 | ♿ | Semantics, 터치 영역, 색상 대비 |

## Quick Start

### 리뷰 요청

```
@code-review [파일 경로 또는 PR 링크]
```

### 특정 카테고리 집중

```
@code-review --focus security,performance
```

## 리뷰 프로세스

### 1단계: 자동 분석

```bash
# 정적 분석
melos run analyze

# Lint 검사
melos run lint:parallel

# 테스트 실행
melos run test
```

### 2단계: 카테고리별 검토

각 카테고리 체크리스트를 순회하며 검토

### 3단계: 결과 작성

점수, 이슈, 개선사항을 구조화된 형식으로 작성

## 리뷰 결과 형식

### Summary

```markdown
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
```

### 이슈 분류

- 🔴 **Critical Issues**: 머지 전 필수 수정
- 🟡 **Improvements**: 권장 수정 사항
- 🟢 **Suggestions**: 선택적 개선 제안
- ❓ **Questions**: 의도 확인 필요

## Additional Resources

- [REFERENCE.md](REFERENCE.md) - 카테고리별 상세 체크리스트
- [TEMPLATES.md](TEMPLATES.md) - 리뷰 결과 템플릿

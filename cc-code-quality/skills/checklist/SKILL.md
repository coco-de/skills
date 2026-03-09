---
name: checklist
description: Feature 개발 완료 및 PR 리뷰를 위한 체계적인 검증 체크리스트. 구조 검증, 테스트, 보안, 성능, 국제화 등 11개 항목 검토.
---

# Checklist

Feature 개발 완료 검증 및 PR 리뷰를 위한 마스터 체크리스트 스킬입니다.

## Scope and Capabilities

### 체크리스트 유형

| 유형 | 용도 | 주요 검증 항목 |
|-----|------|--------------|
| Feature Complete | 개발 완료 전 자체 검증 | 구조, 코드 생성, 테스트, 문서화, i18n, 성능, 보안, 접근성 |
| PR Review | 코드 리뷰 시 검증 | 메타 정보, 변경 범위, 코드 품질, 상태 관리, 테스트, 보안 |

## Quick Start

### Feature 완료 검증

```
@checklist/feature-complete [feature_name]
```

### PR 리뷰

```
@checklist/pr-review [PR 번호 또는 링크]
```

## Feature Complete 검증 항목 (11개)

| # | 항목 | 설명 |
|---|------|------|
| 1 | 구조 검증 | Domain/Data/Presentation 레이어 완성도 |
| 2 | 코드 생성 | Freezed, Injectable, Route 코드 생성 |
| 3 | 테스트 | 단위/BLoC/Widget 테스트 |
| 4 | 문서화 | dartdoc, 주석, TODO 해결 |
| 5 | 국제화 | 번역 키, 복수형, 파라미터 |
| 6 | 성능 최적화 | const, buildWhen, ListView.builder |
| 7 | 보안 검토 | 하드코딩, 입력 검증 |
| 8 | 접근성 | Semantics, 터치 타겟, 색상 대비 |
| 9 | 정적 분석 | Lint, 포맷팅 |
| 10 | 통합 검증 | iOS/Android 빌드 |
| 11 | PR 준비 | 커밋 메시지, 이슈 연결 |

## PR Review 검증 항목 (10개)

| # | 항목 | 설명 |
|---|------|------|
| 1 | PR 메타 정보 | 제목 컨벤션, 이슈 연결, 라벨 |
| 2 | 변경 사항 범위 | 목적 명확성, 단일 목적 |
| 3 | 코드 품질 | 아키텍처, 네이밍, 구조 |
| 4 | 상태 관리 | BLoC, Freezed, 에러 처리 |
| 5 | 테스트 | 신규 테스트, Edge case |
| 6 | 보안 | 시크릿, 로깅, 입력 검증 |
| 7 | 성능 | N+1, 리렌더링, 캐싱 |
| 8 | 국제화 | 하드코딩 문자열, 번역 키 |
| 9 | 접근성 | Semantic label, 터치 타겟 |
| 10 | 문서화 | API 문서, Breaking Changes |

## 우선순위 분류

### Must-Have (Approve 불가)
- 빌드 실패
- 테스트 실패
- 보안 취약점
- Breaking Change 미문서화
- Architecture 위반

### Should-Have (개선 요청 후 Approve 가능)
- 성능 최적화 미비
- 테스트 커버리지 부족
- 문서화 부족
- 접근성 미비

### Nice-to-Have (코멘트만)
- 네이밍 개선 제안
- 코드 스타일 제안
- 추가 최적화 제안

## Additional Resources

- [REFERENCE.md](REFERENCE.md) - 검증 항목 상세 가이드
- [TEMPLATES.md](TEMPLATES.md) - 체크리스트 및 리뷰 템플릿

---
name: feature-orchestrator-agent
description: Full-stack Feature 오케스트레이션 전문가. 백엔드부터 프론트엔드까지 전체 Feature 생성 시 사용
invoke: /feature:create
aliases: ["/feature:full", "/feature:orchestrate"]
tools: Read, Edit, Write, Bash, Glob, Grep
model: inherit
skills: feature
---

# Feature Orchestrator Agent

> 전체 Feature 생성 워크플로우 오케스트레이션 에이전트

📚 **상세 패턴 참조**:
- [UseCase 패턴](../../references/patterns/usecase-patterns.md)
- [BLoC 패턴](../../references/patterns/bloc-patterns.md)
- [Repository 패턴](../../references/patterns/repository-patterns.md)
- [의존성 그래프](../../references/DEPENDENCY_GRAPH.md)

---

## 역할

Serverpod 백엔드부터 Flutter 프론트엔드까지 전체 Feature 생성을 오케스트레이션합니다.

---

## 실행 조건

- `/feature:create` 커맨드 호출 시 활성화

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) |
| `entity_name` | ✅ | Entity명 (PascalCase) |
| `location` | ❌ | `application`, `common`, `console` (기본: `application`) |
| `caching` | ❌ | `swr`, `cache-first`, `none` (기본: `swr`) |
| `endpoint_type` | ❌ | `app`, `console`, `both` (기본: `app`) |

---

## 실행 흐름 요약

```
Phase 0: 기존 Feature 확인
    ↓ (업데이트/스킵/재생성 선택)
Phase 1: 요구사항 수집 (Interactive)
    ↓
Phase 2: 계획 수립 (TodoWrite)
    ↓
Phase 3: Backend 구현
  - Step 1: /serverpod:model 호출
  - Step 2: /serverpod:endpoint 호출
  - Step 3: backend:pod:generate
  - Step 4: 마이그레이션
    ↓
Phase 4: Frontend 구현
  - Step 5: /feature:domain 호출
  - Step 6: /feature:data 호출
  - Step 7: /feature:presentation 호출
    ↓
Phase 4.5: 피그마 스타일 적용 (조건부)
    ↓
Phase 4.7: 실제 동작 구현
    ↓
Phase 5: 통합 및 검증
  - DI 등록, Route 등록
  - 코드 생성, 분석, 테스트
```

---

## 호출 커맨드 순서

| Step | 커맨드 | 생성 내용 |
|------|--------|----------|
| 1 | `/serverpod:model` | Entity, DTO, Enum |
| 2 | `/serverpod:endpoint` | Endpoint, Service |
| 3 | `backend:pod:generate` | 코드 생성 |
| 4 | `backend:pod:*-migration` | DB 마이그레이션 |
| 5 | `/feature:domain` | Entity, Repository I/F, UseCase |
| 6 | `/feature:data` | Repository 구현, Mixin, Cache |
| 7 | `/feature:presentation` | BLoC, Page, Widget, Route |

---

## 생성 파일 요약

```
backend/petmedi_server/lib/src/feature/{feature}/
├── model/entities/*.spy.yaml
├── model/dto/*.spy.yaml
├── endpoint/{feature}_endpoint.dart
└── service/{feature}_service.dart

feature/{location}/{feature}/lib/src/
├── domain/ (entity, repository, usecase)
├── data/ (repository, mixin, cache, local)
├── presentation/ (bloc, page, widget, route)
└── di/injection.dart
```

---

## 성공 기준

- ✅ 모든 파일이 올바른 위치에 생성됨
- ✅ `melos run analyze` 오류 없음
- ✅ `melos run test --scope={feature}` 통과
- ✅ DI 등록 완료
- ✅ Route 등록 완료

---

## 에러 처리

| 단계 | 실패 시 처리 |
|------|------------|
| Model 생성 | 필드 정의 재확인 |
| Endpoint 생성 | Import 경로 확인 |
| Domain 생성 | Entity 필드 매핑 확인 |
| Data 생성 | 네임스페이스 import 확인 |
| Presentation 생성 | BLoC 패턴, UseCase 호출 확인 |

---

## 관련 문서

- [Domain Layer Agent](./domain-layer-agent.md)
- [Data Layer Agent](./data-layer-agent.md)
- [Presentation Layer Agent](./presentation-layer-agent.md)
- [Serverpod Model Agent](./serverpod-model-agent.md)
- [Serverpod Endpoint Agent](./serverpod-endpoint-agent.md)

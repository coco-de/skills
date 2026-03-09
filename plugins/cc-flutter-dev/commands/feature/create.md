---
name: feature:create
description: "Serverpod 백엔드부터 Flutter 프론트엔드까지 전체 Feature 생성 오케스트레이션"
invoke: /feature:create
aliases: ["/feature", "/feature:new"]
category: petmedi-workflow
complexity: complex
mcp-servers: [serena, sequential, context7, magic]
---

# /feature:create

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/feature:create` patterns.

## Triggers

- 새로운 Feature를 처음부터 끝까지 생성할 때
- Serverpod 백엔드와 Flutter 프론트엔드를 동시에 구현할 때
- 전체 Clean Architecture 워크플로우가 필요할 때

## Context Trigger Pattern

```
/feature:create {feature_name} {entity_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `community`, `chat`, `wallet` |
| `entity_name` | ✅ | Entity명 (PascalCase) | `Post`, `Message`, `Transaction` |
| `--location` | ❌ | 위치 | `application`, `common`, `console` (기본: `application`) |
| `--caching` | ❌ | 캐싱 전략 | `swr`, `cache-first`, `none` (기본: `swr`) |
| `--endpoint-type` | ❌ | 엔드포인트 타입 | `app`, `console`, `both` (기본: `app`) |
| `--fields` | ❌ | 필드 정의 | `"title:String, content:String"` |
| `--with-bdd` | ❌ | BDD 테스트 생성 | `true`, `false` (기본: `true`) |
| `--bdd-from` | ❌ | BDD 시나리오 소스 | `claudedocs/{feature}/bdd/` |

## Execution Flow

```
┌─────────────────────────────────────────────────────────┐
│  Phase 1: 요구사항 수집 (Interactive)                      │
├─────────────────────────────────────────────────────────┤
│  1. Feature/Entity 이름 확인                              │
│  2. 필드 정의 수집                                        │
│  3. CRUD 메서드 범위 확인                                  │
│  4. 캐싱 전략 선택                                        │
│  5. BDD 테스트 포함 여부 확인                               │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 2: Backend 구현                                    │
├─────────────────────────────────────────────────────────┤
│  Step 1: /serverpod:model                                │
│  Step 2: /serverpod:endpoint                             │
│  Step 3: melos run backend:pod:generate                  │
│  Step 4: 마이그레이션 (필요 시)                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 3: Frontend 구현                                   │
├─────────────────────────────────────────────────────────┤
│  Step 5: /feature:domain                                 │
│  Step 6: /feature:data                                   │
│  Step 7: /feature:presentation                           │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 4: BDD 테스트 생성 (--with-bdd true 시) ⭐          │
├─────────────────────────────────────────────────────────┤
│  Step 8: /bdd:generate {feature_name}                    │
│  Step 9: melos run test:bdd:generate --scope={feature}   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│  Phase 5: 통합 및 검증                                     │
├─────────────────────────────────────────────────────────┤
│  Step 10: DI 등록 확인                                    │
│  Step 11: Route 등록 확인                                  │
│  Step 12: melos run build                                │
│  Step 13: melos run analyze                              │
│  Step 14: melos run test --scope={feature}               │
│  Step 15: melos run test:bdd --scope={feature}           │
└─────────────────────────────────────────────────────────┘
```

## Phase 1: 요구사항 수집

### Interactive Mode

```markdown
## Feature 생성 요구사항

### 기본 정보
- **Feature 이름**: {feature_name}
- **Entity 이름**: {entity_name}
- **위치**: application / common / console

### Entity 필드
| 필드명 | 타입 | 필수 | 설명 |
|--------|------|------|------|
| title | String | ✅ | 제목 |
| content | String | ✅ | 내용 |
| category | Enum | ✅ | 카테고리 |

### CRUD 메서드
- [x] 목록 조회 (페이지네이션)
- [x] 단건 조회
- [x] 생성
- [x] 수정
- [x] 삭제

### 캐싱 전략
- [x] SWR (Stale-While-Revalidate)
- [ ] Cache-First
- [ ] None
```

## Phase 2: Backend 구현

### Step 1: Serverpod Model

```bash
# /serverpod:model 커맨드 실행
/serverpod:model {feature_name} {entity_name}
  --fields "{fields}"
  --has-crud true
```

**생성 파일**:
- `backend/.../model/entities/{entity_name}.spy.yaml`
- `backend/.../model/dto/...`
- `backend/.../model/enum/...`

### Step 2: Serverpod Endpoint

```bash
# /serverpod:endpoint 커맨드 실행
/serverpod:endpoint {feature_name} {entity_name}
  --type {endpoint_type}
```

**생성 파일**:
- `backend/.../endpoint/{feature_name}_endpoint.dart`
- `backend/.../service/{feature_name}_service.dart`

### Step 3: 코드 생성

```bash
melos run backend:pod:generate
```

### Step 4: 마이그레이션

```bash
melos run backend:pod:create-migration
melos run backend:pod:run-migration
```

## Phase 3: Frontend 구현

### Step 5: Domain Layer

```bash
# /feature:domain 커맨드 실행
/feature:domain {feature_name} {entity_name}
  --location {location}
```

**생성 파일**:
- Entity, Repository Interface, UseCase
- UseCase 테스트

### Step 6: Data Layer

```bash
# /feature:data 커맨드 실행
/feature:data {feature_name} {entity_name}
  --location {location}
  --caching {caching}
```

**생성 파일**:
- Repository 구현체, Serverpod Mixin
- Cache 전략, Local DB (Drift)

### Step 7: Presentation Layer

```bash
# /feature:presentation 커맨드 실행
/feature:presentation {feature_name} {entity_name}
  --location {location}
```

**생성 파일**:
- BLoC (Event, State), BLoC 테스트
- Page, Widget, Widget 테스트
- Route, Widgetbook UseCase

## Phase 4: BDD 테스트 생성

**`--with-bdd true` (기본값) 시 실행:**

### Step 8: BDD 시나리오 및 Step 생성

```bash
# /bdd:generate 커맨드 실행
/bdd:generate {feature_name}
  --entity-name {entity_name}
  --location {location}
  --from-claudedocs true  # claudedocs에 BDD 파일이 있는 경우
```

**생성 파일**:
```
feature/{location}/{feature_name}/
├── build.yaml                    # BDD 빌더 설정
└── test/src/bdd/
    ├── {feature}_list.feature
    ├── {feature}_detail.feature
    ├── {feature}_form.feature
    ├── step/
    │   ├── common_steps.dart     # 공용 스텝 import
    │   └── {feature}_steps.dart  # Feature 전용 스텝
    └── hooks/
        └── hooks.dart            # Setup/Teardown
```

### Step 9: BDD 테스트 코드 생성

```bash
# bdd_widget_test 빌더 실행
melos run test:bdd:generate --scope={feature_name}
```

**생성 결과**: `.feature` 파일에서 자동 생성된 테스트 코드

## Phase 5: 통합 및 검증

### Step 10: DI 등록 확인

**확인 파일**: `feature/{location}/{feature_name}/lib/src/di/injection.dart`

```dart
@module
abstract class {Feature}Module {
  @lazySingleton
  {Feature}Database get database => {Feature}Database();
}
```

### Step 9: Route 등록 확인

**확인 파일**: `app/petmedi/lib/src/route/app_router.dart`

### Step 10-12: 빌드 및 테스트

```bash
melos run build
melos run analyze
melos run test --scope={feature_name}
```

## TodoWrite Template

```dart
TodoWrite([
  // Backend
  {"content": "Serverpod 모델 생성", "status": "pending", "activeForm": "Serverpod 모델 생성 중"},
  {"content": "Serverpod 엔드포인트 생성", "status": "pending", "activeForm": "Serverpod 엔드포인트 생성 중"},
  {"content": "backend:pod:generate 실행", "status": "pending", "activeForm": "backend:pod:generate 실행 중"},

  // Frontend - Domain
  {"content": "Domain Entity 생성", "status": "pending", "activeForm": "Domain Entity 생성 중"},
  {"content": "Repository Interface 생성", "status": "pending", "activeForm": "Repository Interface 생성 중"},
  {"content": "UseCase 생성", "status": "pending", "activeForm": "UseCase 생성 중"},
  {"content": "UseCase 테스트 생성", "status": "pending", "activeForm": "UseCase 테스트 생성 중"},

  // Frontend - Data
  {"content": "Repository 구현체 생성", "status": "pending", "activeForm": "Repository 구현체 생성 중"},
  {"content": "Serverpod Mixin 생성", "status": "pending", "activeForm": "Serverpod Mixin 생성 중"},

  // Frontend - Presentation
  {"content": "BLoC 생성", "status": "pending", "activeForm": "BLoC 생성 중"},
  {"content": "BLoC 테스트 생성", "status": "pending", "activeForm": "BLoC 테스트 생성 중"},
  {"content": "Page/Widget 생성", "status": "pending", "activeForm": "Page/Widget 생성 중"},
  {"content": "Widget 테스트 생성", "status": "pending", "activeForm": "Widget 테스트 생성 중"},
  {"content": "Route 정의", "status": "pending", "activeForm": "Route 정의 중"},
  {"content": "Widgetbook UseCase 생성", "status": "pending", "activeForm": "Widgetbook UseCase 생성 중"},

  // BDD 테스트 (--with-bdd true 시)
  {"content": "BDD .feature 파일 생성", "status": "pending", "activeForm": "BDD .feature 파일 생성 중"},
  {"content": "BDD Step 정의 생성", "status": "pending", "activeForm": "BDD Step 정의 생성 중"},
  {"content": "BDD Hooks 설정", "status": "pending", "activeForm": "BDD Hooks 설정 중"},
  {"content": "BDD 테스트 코드 생성", "status": "pending", "activeForm": "BDD 테스트 코드 생성 중"},

  // Integration
  {"content": "코드 생성 및 분석", "status": "pending", "activeForm": "코드 생성 및 분석 중"},
  {"content": "단위 테스트 실행", "status": "pending", "activeForm": "단위 테스트 실행 중"},
  {"content": "BDD 테스트 실행", "status": "pending", "activeForm": "BDD 테스트 실행 중"},
])
```

## MCP Integration

| Phase | MCP 서버 | 용도 |
|-------|----------|------|
| 요구사항 분석 | Sequential | 복잡한 분석 및 계획 |
| Backend | Serena, Context7 | 패턴 분석, Serverpod 문서 |
| Domain | Serena, Context7 | UseCase 패턴, Clean Architecture |
| Data | Serena, Context7 | Mixin 패턴, Drift 문서 |
| Presentation | Magic, Serena | UI 생성, BLoC 패턴 |
| 검증 | Serena | 심볼 검색, 참조 확인 |

## 참조 에이전트

상세 구현 규칙은 `~/.claude/commands/agents/feature-orchestrator-agent.md` 참조

## Examples

### 커뮤니티 게시글 Feature 생성

```
/feature:create community Post
  --location application
  --caching swr
  --endpoint-type app
  --fields "title:String, content:String, category:PostCategory, imageUrls:List<String>?"
```

### 채팅 메시지 Feature 생성

```
/feature:create chat Message
  --location application
  --caching cache-first
  --endpoint-type app
  --fields "content:String, senderId:int, chatRoomId:int, readAt:DateTime?"
```

### 관리자 대시보드 Feature 생성

```
/feature:create dashboard Stats
  --location console
  --caching none
  --endpoint-type console
  --fields "totalUsers:int, totalPosts:int, activeUsers:int"
```

## 성공 기준

1. ✅ 모든 파일이 올바른 위치에 생성됨
2. ✅ `melos run analyze` 오류 없음
3. ✅ `melos run test --scope={feature_name}` 통과
4. ✅ `melos run test:bdd --scope={feature_name}` 통과 (--with-bdd true 시)
5. ✅ DI 등록 완료
6. ✅ Route 등록 완료
7. ✅ Widgetbook에서 컴포넌트 확인 가능
8. ✅ BDD .feature 파일 Gherkin 문법 준수

## 핵심 규칙 요약

### Backend
- 모든 필드에 한글 주석
- Import 순서 준수
- Service에 비즈니스 로직 분리

### Domain
- UseCase 상수 생성자 + ServiceLocator
- @injectable 금지
- 모든 UseCase 테스트 필수

### Data
- Serverpod Mixin `as pod` 네임스페이스 필수
- SWR/Cache-First 캐싱 전략

### Presentation
- BLoC Event: sealed class + private implementation
- UseCase 직접 생성 (`const UseCase().call()`)
- Widget `super.key` 마지막 위치
- BLoC/Widget 테스트 필수
- Widgetbook 반영 필수

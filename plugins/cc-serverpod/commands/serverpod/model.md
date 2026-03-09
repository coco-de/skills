---
name: serverpod:model
description: "Serverpod .spy.yaml 모델 파일 생성"
category: petmedi-workflow
complexity: standard
mcp-servers: [serena, context7]
---

# /serverpod:model

> **Context Framework Note**: This behavioral instruction activates when Claude Code users type `/serverpod:model` patterns.

## Triggers

- 새로운 Serverpod 모델 (Entity, DTO, Enum) 생성이 필요할 때
- 백엔드 데이터 모델 정의가 필요할 때
- `/feature:create` 오케스트레이션의 Step 1에서 호출될 때

## Context Trigger Pattern

```
/serverpod:model {feature_name} {entity_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 (snake_case) | `community`, `chat`, `wallet` |
| `entity_name` | ✅ | Entity명 (PascalCase) | `Post`, `Message`, `Transaction` |
| `--fields` | ❌ | 필드 정의 목록 | `"title:String, content:String"` |
| `--has-crud` | ❌ | CRUD DTO 자동 생성 | `true` (기본값) |
| `--has-enum` | ❌ | Enum 파일 생성 | `true` (기본값) |

## Behavioral Flow

### 1. 기존 패턴 분석

```
Serena MCP를 사용하여 기존 모델 패턴 분석:
- backend/petmedi_server/lib/src/feature/community/model/entity/post.spy.yaml
- backend/petmedi_server/lib/src/feature/chat/model/entity/chat_room.spy.yaml
```

### 2. 모델 파일 생성

**Entity 파일 생성** (`entities/{entity_name}.spy.yaml`):

```yaml
### {엔티티 한글 설명}
class: {EntityName}
table: {table_name}

fields:
  ### 고유 식별자
  id: int?

  ### {필드1 설명}
  {field1}: {Type}

  ### {필드2 설명}
  {field2}: {Type}?

  ### 작성자 ID
  authorId: int

  ### 작성자 이름
  authorName: String

  ### 작성자 프로필 이미지 URL
  authorProfileUrl: String?

  ### 생성일시
  createdAt: DateTime

  ### 수정일시
  updatedAt: DateTime?

indexes:
  {entity}_author_idx:
    fields: authorId
  {entity}_created_idx:
    fields: createdAt
```

**Request DTO 생성** (`dto/{entity_name}_create_request.spy.yaml`):

```yaml
### {엔티티} 생성 요청
class: {EntityName}CreateRequest

fields:
  ### {필드 설명}
  {requiredField}: {Type}
  ### {선택 필드 설명}
  {optionalField}: {Type}?
```

**Response DTO 생성** (`dto/{entity_name}_list_response.spy.yaml`):

```yaml
### {엔티티} 목록 응답
class: {EntityName}ListResponse

fields:
  ### {엔티티} 목록
  items: List<{EntityName}>
  ### 전체 개수
  total: int
  ### 다음 페이지 존재 여부
  hasMore: bool
```

**Enum 생성** (`enum/{entity_name}_category.spy.yaml`):

```yaml
### {엔티티} 카테고리
enum: {EntityName}Category
serialized: byName
values:
  - general
  - notice
  - event
```

### 3. 검증

- 모든 필드에 한글 주석 확인
- 필수 필드 (createdAt, updatedAt) 포함 확인
- 인덱스 정의 확인

## Output Files

```
backend/petmedi_server/lib/src/feature/{feature_name}/model/
├── entities/
│   └── {entity_name}.spy.yaml
├── dto/
│   ├── {entity_name}_create_request.spy.yaml
│   ├── {entity_name}_update_request.spy.yaml
│   └── {entity_name}_list_response.spy.yaml
└── enum/
    └── {entity_name}_category.spy.yaml
```

## Post-Generation Commands

```bash
# 모델 코드 생성
melos run backend:pod:generate

# 마이그레이션 생성 (Entity 변경 시)
melos run backend:pod:create-migration

# 마이그레이션 적용
melos run backend:pod:run-migration
```

## MCP Integration

- **Serena**: 기존 모델 패턴 분석, 심볼 검색
- **Context7**: Serverpod 모델 정의 문서 참조

## Examples

### 게시글 모델 생성

```
/serverpod:model community Post
  --fields "title:String, content:String, category:PostCategory, imageUrls:List<String>?"
```

### 채팅 메시지 모델 생성

```
/serverpod:model chat Message
  --fields "content:String, senderId:int, chatRoomId:int, readAt:DateTime?"
```

### 지갑 거래 모델 생성

```
/serverpod:model wallet Transaction
  --fields "amount:double, type:TransactionType, description:String?, balanceAfter:double"
```

## 참조 에이전트

상세 구현 규칙은 `~/.claude/commands/agents/serverpod-model-agent.md` 참조

## 핵심 규칙 요약

1. **모든 필드에 한글 주석 (`###`) 필수**
2. **createdAt, updatedAt 필드 필수 포함**
3. **적절한 인덱스 정의 필수**
4. **외래키 관계 정의 (필요 시)**
5. **기본값 설정 (카운터, 상태 필드)**

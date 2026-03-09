# API 설계 원칙

Serverpod 엔드포인트를 위한 REST API 설계 원칙. 리소스 설계, HTTP 시맨틱, 버전관리, 에러 처리, 페이지네이션을 다룹니다.

## 트리거

- 새 API 설계
- 엔드포인트 리뷰
- API 버전관리 전략
- 에러 응답 표준화

## 리소스 중심 설계

Serverpod 엔드포인트는 RPC 스타일이지만, 리소스 중심 사고를 적용:

```dart
// GOOD — 리소스(명사) 중심 메서드명
class UserEndpoint extends Endpoint {
  Future<User> getUser(Session session, int id) async { ... }
  Future<List<User>> listUsers(Session session, {int page = 0}) async { ... }
  Future<User> createUser(Session session, User user) async { ... }
  Future<User> updateUser(Session session, User user) async { ... }
  Future<bool> deleteUser(Session session, int id) async { ... }
}

// BAD — 동사 중심, 일관성 없음
class UserEndpoint extends Endpoint {
  Future<User> fetchOneUser(Session session, int id) async { ... }
  Future<void> doUserCreation(Session session, User user) async { ... }
}
```

## 메서드 명명 규칙

| 동작 | 패턴 | 예시 |
|------|------|------|
| 단건 조회 | `get{Entity}` | `getUser`, `getPost` |
| 목록 조회 | `list{Entity}s` | `listUsers`, `listPosts` |
| 생성 | `create{Entity}` | `createUser` |
| 수정 | `update{Entity}` | `updateUser` |
| 삭제 | `delete{Entity}` | `deleteUser` |
| 검색 | `search{Entity}s` | `searchUsers` |
| 관계 조회 | `list{Child}sFor{Parent}` | `listPostsForUser` |

## 페이지네이션

### Offset 기반 (간단한 경우)

```dart
Future<ListResponse<User>> listUsers(
  Session session, {
  int page = 0,
  int pageSize = 20,
}) async {
  final users = await User.db.find(session,
    limit: pageSize,
    offset: page * pageSize,
    orderBy: (t) => t.createdAt,
    orderDescending: true,
  );
  final total = await User.db.count(session);

  return ListResponse(
    items: users,
    page: page,
    pageSize: pageSize,
    totalCount: total,
  );
}
```

### Cursor 기반 (대규모 데이터)

```dart
Future<CursorResponse<User>> listUsers(
  Session session, {
  int? afterId,
  int limit = 20,
}) async {
  final users = await User.db.find(session,
    where: afterId != null ? (t) => t.id > afterId : null,
    orderBy: (t) => t.id,
    limit: limit + 1, // 다음 페이지 존재 여부 확인
  );

  final hasMore = users.length > limit;
  final items = hasMore ? users.sublist(0, limit) : users;

  return CursorResponse(
    items: items,
    nextCursor: hasMore ? items.last.id : null,
    hasMore: hasMore,
  );
}
```

## 에러 처리

### Serializable Exception 활용

```yaml
# error_response.spy.yaml
exception: AppException
fields:
  code: String
  message: String
  details: String?
```

```dart
// 서버에서 throw
throw AppException(
  code: 'USER_NOT_FOUND',
  message: 'User not found: $id',
);

// 클라이언트에서 catch
try {
  await client.user.getUser(id);
} on AppException catch (e) {
  showError(e.message);
}
```

### 에러 코드 표준화

| 코드 | 설명 |
|------|------|
| `NOT_FOUND` | 리소스 없음 |
| `DUPLICATE` | 중복 리소스 |
| `VALIDATION_ERROR` | 입력값 검증 실패 |
| `UNAUTHORIZED` | 인증 필요 |
| `FORBIDDEN` | 권한 부족 |
| `CONFLICT` | 상태 충돌 |

## 버전관리

Serverpod 엔드포인트 버전관리 전략:

```dart
// V1 — 기존 클라이언트 유지
@Deprecated('Use TeamV2Endpoint instead')
class TeamEndpoint extends Endpoint {
  Future<TeamInfo> join(Session session) async { ... }
}

// V2 — 새 API
class TeamV2Endpoint extends TeamEndpoint {
  @override
  @doNotGenerate
  Future<TeamInfo> join(Session session) async => throw UnimplementedError();

  Future<NewTeamInfo> joinWithCode(
    Session session, String invitationCode) async { ... }
}
```

## 하위 호환성 규칙

- 파라미터 이름 변경 금지 (REST API는 이름으로 전달)
- 메서드/시그니처 삭제 금지 — 새 메서드 추가 또는 optional named parameter 추가
- Breaking change 시 버전 엔드포인트 생성

## 요청 크기 제한

기본: 512 kB. 변경:

```yaml
# config
maxRequestSize: 1048576  # 1 MB
```

대용량은 파일 업로드 API 사용.

## 체크리스트

- [ ] 리소스 중심 메서드 명명
- [ ] 일관된 페이지네이션 패턴
- [ ] Serializable Exception으로 에러 응답
- [ ] 표준화된 에러 코드
- [ ] 하위 호환성 고려
- [ ] 민감 데이터 exception 필드에 포함 금지

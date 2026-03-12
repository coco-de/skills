---
name: caching
description: Serverpod 캐싱 전략 및 구현
---

# Serverpod 캐싱

session.caches를 활용한 캐싱 전략. Local, Redis, CacheMissHandler 패턴을 다룹니다.

## 트리거

- 데이터 캐싱, 쿼리 최적화
- Redis 캐시 설정
- CacheMissHandler 패턴

## 캐시 타입

| 타입 | 저장소 | 범위 |
|------|--------|------|
| `session.caches.local` | 메모리 | 현재 서버 인스턴스 |
| `session.caches.localPriority` | 메모리 | 자주 접근하는 항목 우선 |
| `session.caches.global` | Redis | 모든 서버 인스턴스 공유 |

## 기본 사용

```dart
// 저장
await session.caches.local.put('UserData-$userId', userData,
  lifetime: Duration(minutes: 5));

// 조회
var userData = await session.caches.local.get<UserData>('UserData-$userId');
```

## CacheMissHandler

캐시 미스 시 자동으로 로드 & 저장:

```dart
var userData = await session.caches.local.get(
  'UserData-$userId',
  CacheMissHandler(
    () async => UserData.db.findById(session, userId),
    lifetime: Duration(minutes: 5),
  ),
);
```

핸들러가 `null`을 반환하면 캐시에 저장하지 않고 `null` 반환.

## 프리미티브 & 컬렉션

```dart
await session.caches.local.put('userCount', 17,
  lifetime: Duration(minutes: 5));
var count = await session.caches.local.get<int>('userCount');
```

## 캐시 키 전략

| 패턴 | 예시 |
|------|------|
| 단일 엔티티 | `'User-$userId'` |
| 목록 | `'UserList-page$page-size$size'` |
| 관계 포함 | `'User-$userId-withPosts'` |
| 필터 기반 | `'Products-category$cat-sort$sort'` |

## 캐시 무효화 패턴

```dart
// 엔티티 수정 시 관련 캐시 삭제
Future<User> updateUser(Session session, User user) async {
  final updated = await User.db.updateRow(session, user);

  // 개별 캐시 무효화
  await session.caches.local.put('User-${user.id}', updated,
    lifetime: Duration(minutes: 5));

  return updated;
}
```

## 멀티 인스턴스 환경

- **단일 서버**: `local` 캐시로 충분
- **다중 서버**: `global` (Redis) 캐시 사용
- **하이브리드**: 자주 변경되지 않는 데이터는 `local`, 공유 상태는 `global`

## 체크리스트

- [ ] 반드시 `lifetime` 설정 (무한 증가 방지)
- [ ] 안정적이고 고유한 캐시 키 사용
- [ ] 엔티티 수정 시 캐시 무효화
- [ ] 다중 서버 환경에서 `global` 캐시 사용
- [ ] CacheMissHandler로 캐시-DB 동기화

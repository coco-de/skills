# 캐싱 전략 패턴

> **참조 위치**: `.claude/references/patterns/caching-patterns.md`

데이터 캐싱 전략으로 사용자 경험과 네트워크 효율성을 최적화합니다.

---

## 전략 비교

| 전략 | 사용 시점 | 장점 | 단점 |
|------|----------|------|------|
| **SWR** | 자주 변경되는 데이터 | 즉시 응답 + 최신 데이터 | 네트워크 호출 빈번 |
| **Cache-First** | 정적 데이터 | 네트워크 절약, 오프라인 지원 | 데이터 오래될 수 있음 |

---

## SWR 패턴 (Stale-While-Revalidate)

실시간 데이터를 위한 패턴. 캐시된 데이터를 즉시 반환하고 백그라운드에서 갱신합니다.

### Repository Interface

```dart
// domain/repository/i_feature_repository.dart
abstract interface class IFeatureRepository {
  /// SWR 방식으로 Entity를 Stream으로 반환
  Stream<SWRResult<Entity>> getEntityAsStream(int id);

  /// 수동 새로고침
  Future<Either<Failure, Entity>> refreshEntity(int id);
}
```

### Repository 구현

```dart
// data/repository/mixins/feature_serverpod_mixin.dart
import 'package:serverpod_service/serverpod_service.dart' as serverpod;

mixin FeatureServerpodMixin implements IFeatureRepository {
  serverpod.ServerpodClient get client;

  @override
  Stream<SWRResult<Entity>> getEntityAsStream(int id) async* {
    // 1. 캐시된 데이터 즉시 반환
    final cached = await _getCachedEntity(id);
    if (cached != null) {
      yield SWRResult(
        data: cached,
        fromCache: true,
        isRefreshing: true,  // 백그라운드 갱신 중임을 표시
      );
    }

    // 2. 백그라운드에서 새 데이터 fetch
    try {
      final fresh = await client.feature.getEntity(id);
      await _cacheEntity(fresh);  // 캐시 업데이트

      yield SWRResult(
        data: fresh.toEntity(),
        fromCache: false,
        isRefreshing: false,
      );
    } catch (error) {
      // fetch 실패 시 캐시가 있으면 에러 무시
      if (cached == null) rethrow;
    }
  }

  @override
  Future<Either<Failure, Entity>> refreshEntity(int id) async {
    try {
      final entity = await client.feature.getEntity(id);
      await _cacheEntity(entity);
      return right(entity.toEntity());
    } on serverpod.ServerpodClientException catch (e, st) {
      return left(ServerFailure(e.message, error: e, stackTrace: st));
    }
  }
}
```

### BLoC 연동: emit.forEach + restartable() (권장)

```dart
import 'package:bloc_concurrency/bloc_concurrency.dart';

// ❌ @injectable 사용 금지
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  FeatureBloc({
    GetEntityStreamUseCase? getEntityStream,
  }) : _getEntityStream = getEntityStream ?? const GetEntityStreamUseCase(),
       super(const FeatureState()) {
    on<FeatureLoad>(
      _onLoad,
      transformer: restartable(),  // 파라미터 변경 시 이전 스트림 자동 취소
    );
  }

  final GetEntityStreamUseCase _getEntityStream;

  Future<void> _onLoad(FeatureLoad event, Emitter<FeatureState> emit) async {
    if (state.entity == null) {
      emit(state.copyWith(status: LoadingStatus.loading));
    }

    await emit.forEach<SWRResult<Entity>>(
      _getEntityStream(GetEntityParams(id: event.id)),
      onData: (result) => state.copyWith(
        status: LoadingStatus.loaded,
        entity: result.data,
        fromCache: result.fromCache,
        isRefreshing: result.isRefreshing,
      ),
    );
  }
}
```

#### restartable() 동작 원리

```
1. add(FeatureLoad(id: 1))  → 스트림A 구독 (캐시 → 서버 순차 yield)
2. add(FeatureLoad(id: 2))  → restartable()가 핸들러1 취소 → 스트림A 해제
                               → 핸들러2 시작 → 스트림B 구독
```

`emit.forEach`는 내부적으로 `stream.listen()`을 호출하며, `restartable()`가 핸들러를 취소하면 구독도 자동 정리됩니다. `close()` 오버라이드와 `StreamSubscription` 관리가 불필요합니다.

#### 레거시: 수동 StreamSubscription (비권장)

<details>
<summary>수동 StreamSubscription 패턴 (기존 코드 참조용)</summary>

```dart
class FeatureBloc extends Bloc<FeatureEvent, FeatureState> {
  FeatureBloc() : super(FeatureInitial()) {
    on<FeatureLoad>(_onLoad);
    on<_FeatureUpdated>(_onUpdated);
  }

  StreamSubscription<SWRResult<Entity>>? _subscription;

  Future<void> _onLoad(FeatureLoad event, Emitter<FeatureState> emit) async {
    emit(FeatureLoading());
    await _subscription?.cancel();
    _subscription = const GetEntityStreamUseCase().call(
      GetEntityParams(id: event.id),
    ).listen(
      (result) => add(_FeatureUpdated(result)),
      onError: (error) => add(_FeatureError(error)),
    );
  }

  @override
  Future<void> close() {
    _subscription?.cancel();
    return super.close();
  }
}
```

</details>

---

## Cache-First 패턴

정적 데이터를 위한 패턴. 캐시가 있으면 네트워크 호출 없이 즉시 반환합니다.

### Repository 구현

```dart
// data/repository/mixins/feature_serverpod_mixin.dart
mixin FeatureServerpodMixin implements IFeatureRepository {
  serverpod.ServerpodClient get client;

  @override
  Stream<CacheFirstResult<Entity>> getEntityCacheFirst(int id) async* {
    // 1. 캐시 우선 확인
    final cached = await _getCachedEntity(id);

    if (cached != null) {
      // 캐시 있으면 즉시 반환하고 종료
      yield CacheFirstResult(
        data: cached,
        fromCache: true,
        isRefreshing: false,
      );
      return;  // 네트워크 호출 안 함
    }

    // 2. 캐시 없으면 네트워크 호출
    try {
      final fresh = await client.feature.getEntity(id);
      await _cacheEntity(fresh);  // 캐시 저장

      yield CacheFirstResult(
        data: fresh.toEntity(),
        fromCache: false,
        isRefreshing: false,
      );
    } catch (error) {
      rethrow;  // 캐시도 없고 네트워크도 실패
    }
  }
}
```

---

## SWRResult / CacheFirstResult 클래스

```dart
// core/lib/src/cache/swr_result.dart
class SWRResult<T> {
  const SWRResult({
    required this.data,
    required this.fromCache,
    required this.isRefreshing,
  });

  final T data;
  final bool fromCache;
  final bool isRefreshing;  // 백그라운드에서 갱신 중인지
}

class CacheFirstResult<T> {
  const CacheFirstResult({
    required this.data,
    required this.fromCache,
    required this.isRefreshing,
  });

  final T data;
  final bool fromCache;
  final bool isRefreshing;
}
```

---

## 로컬 캐시 구현 (Drift)

```dart
// data/local/dao/entity_dao.dart
@DriftAccessor(tables: [Entities])
class EntityDao extends DatabaseAccessor<AppDatabase> with _$EntityDaoMixin {
  EntityDao(super.db);

  Future<EntityData?> getById(int id) =>
      (select(entities)..where((t) => t.id.equals(id)))
          .getSingleOrNull();

  Future<void> insertOrUpdate(EntityData data) =>
      into(entities).insertOnConflictUpdate(data);

  Future<void> deleteById(int id) =>
      (delete(entities)..where((t) => t.id.equals(id))).go();
}
```

---

## 선택 가이드

```
데이터 자주 변경? ─Yes→ SWR (실시간)
                 └No→ 오프라인 필요? ─Yes→ Cache-First
                                    └No→ SWR
```

### SWR 적합 케이스

- 피드, 타임라인
- 채팅 메시지
- 알림 목록
- 실시간 상태

### Cache-First 적합 케이스

- 사용자 프로필
- 앱 설정
- 카테고리 목록
- 정적 콘텐츠

---

## 체크리스트

- [ ] 캐싱 전략 선택 (SWR / Cache-First)
- [ ] Repository Interface에 Stream 메서드 정의
- [ ] Mixin에서 캐싱 로직 구현
- [ ] Drift DAO 구현 (로컬 캐시)
- [ ] BLoC에서 `emit.forEach` + `restartable()` 사용
- [ ] 파라미터 변경 시 이전 스트림 자동 취소 확인
- [ ] UI에서 fromCache/isRefreshing 상태 표시

---

## 참조하는 에이전트

- `/feature:data` - Data Layer 캐싱 구현
- `/feature:bloc` - Stream 연동 BLoC

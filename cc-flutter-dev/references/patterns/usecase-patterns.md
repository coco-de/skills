# UseCase 패턴

> **참조 위치**: `.claude/references/patterns/usecase-patterns.md`

UseCase는 비즈니스 로직을 캡슐화하는 Clean Architecture의 핵심 컴포넌트입니다.

---

## 패턴 비교

| 패턴 | 장점 | 단점 | 권장 |
|------|------|------|------|
| **직접 인스턴스화** | DI 설정 단순화, BLoC 코드 간결 | 테스트 시 GetIt 모킹 필요 | ✅ **권장** |
| **생성자 주입** | Mock 주입 간편 | BLoC에 @injectable 필요 (금지됨) | ❌ 금지 |

> ⚠️ **중요**: BLoC에 `@injectable` 사용 금지! 직접 인스턴스화 패턴만 사용

---

## 패턴 A: 직접 인스턴스화 (Direct Instantiation) ✅ 권장

### UseCase 정의

```dart
// domain/usecase/get_user_usecase.dart
import 'package:dependencies/dependencies.dart';

class GetUserUseCase {
  // Repository는 GetIt에서 가져옴
  IUserRepository get _repository => getIt<IUserRepository>();

  Future<Either<Failure, User>> call(GetUserParams params) async {
    return _repository.getUser(params.id);
  }
}

class GetUserParams {
  const GetUserParams({required this.id});
  final int id;
}
```

### BLoC에서 사용

```dart
// ❌ @injectable 사용 금지 - Provider 사용
class UserBloc extends Bloc<UserEvent, UserState> {
  UserBloc() : super(const UserInitial()) {
    on<UserLoad>(_onLoad);
  }

  Future<void> _onLoad(UserLoad event, Emitter<UserState> emit) async {
    emit(const UserLoading());

    // ✅ UseCase 직접 인스턴스화하여 호출
    final result = await GetUserUseCase().call(
      GetUserParams(id: event.userId),
    );

    if (isClosed) return; // await 후 체크 필수!

    result.fold(
      (failure) => emit(UserError(failure: failure)),
      (user) => emit(UserLoaded(user: user)),
    );
  }
}
```

### 테스트

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:get_it/get_it.dart';

class MockUserRepository extends Mock implements IUserRepository {}

void main() {
  late MockUserRepository mockRepository;

  setUp(() {
    mockRepository = MockUserRepository();
    // GetIt에 Mock Repository 등록
    getIt.registerSingleton<IUserRepository>(mockRepository);
  });

  tearDown(() {
    getIt.reset();
  });

  blocTest<UserBloc, UserState>(
    'emits [loading, loaded] when load succeeds',
    setUp: () {
      when(() => mockRepository.getUser(any()))
          .thenAnswer((_) async => right(testUser));
    },
    build: () => UserBloc(),
    act: (bloc) => bloc.add(const UserLoad(userId: 1)),
    expect: () => [
      const UserLoading(),
      UserLoaded(user: testUser),
    ],
  );
}
```

---

## 선택 가이드

> ⚠️ **결론**: 항상 **직접 인스턴스화** 패턴 사용

```text
UseCase 사용? ─Yes→ 직접 인스턴스화 (UseCase().call())
             └No→ Repository 직접 접근 금지 (UseCase 통해서만!)
```

### 직접 인스턴스화 사용 이유

- ✅ BLoC에 `@injectable` 불필요 (Provider 사용)
- ✅ DI 설정 단순화
- ✅ BLoC 생성 코드 간결
- ✅ 테스트 시 GetIt에 Mock Repository 등록으로 해결

### ❌ 금지 패턴

- ❌ BLoC에 `@injectable` 사용
- ❌ BLoC 생성자에 UseCase 주입
- ❌ BLoC에서 Repository 직접 접근

---

## 참조하는 에이전트

- `/feature:domain` - Domain Layer 생성
- `/feature:bloc` - BLoC 상태 관리
- `/feature:presentation` - Presentation Layer 생성

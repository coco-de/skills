# Checklist Reference Guide

Feature Complete 및 PR Review 체크리스트 상세 가이드입니다.

---

## 1. Feature Complete 검증 상세

### 1.1 구조 검증

#### Domain Layer

| 항목 | 검증 기준 | 심각도 |
|------|----------|--------|
| Entity 정의 | Freezed 사용, 불변 객체 | 🔴 |
| Repository Interface | I 접두사, Domain 레이어에 정의 | 🔴 |
| UseCase 구현 | Either 패턴, Failure 처리 | 🔴 |
| Failure 클래스 | 도메인별 Failure 정의 | 🟡 |
| 단위 테스트 | UseCase 테스트 작성 | 🟡 |

```dart
// ✅ Entity 예시
@freezed
class User with _$User {
  const factory User({
    required int id,
    required String name,
  }) = _User;
}

// ✅ Repository Interface 예시
abstract interface class IUserRepository {
  Future<Either<Failure, User>> getUser(int id);
}

// ✅ UseCase 예시 (직접 인스턴스화 패턴)
class GetUserUseCase {
  const GetUserUseCase();  // 상수 생성자

  IUserRepository get _repository => getIt<IUserRepository>();

  Future<Either<Failure, User>> call(GetUserParams params) async {
    return _repository.getUser(params.id);
  }
}
```

#### Data Layer

| 항목 | 검증 기준 | 심각도 |
|------|----------|--------|
| Repository 구현체 | Interface 구현, @LazySingleton | 🔴 |
| Serverpod Mixin | 네트워크 로직 분리 | 🟡 |
| Local Database | Drift DAO 패턴 | 🟡 |
| DTO ↔ Entity 매퍼 | toEntity(), toDto() | 🟡 |
| 캐싱 전략 | SWR 또는 Cache-First | 🟡 |

#### Presentation Layer

| 항목 | 검증 기준 | 심각도 |
|------|----------|--------|
| Page 위젯 | 화면 단위 위젯 | 🔴 |
| 재사용 Widget | 컴포넌트 분리 | 🟡 |
| BLoC/Cubit | 상태 관리 구현 | 🔴 |
| Event/State | Freezed Union Type | 🔴 |
| Widget 테스트 | 주요 UI 테스트 | 🟡 |

### 1.2 코드 생성

```bash
# 코드 생성 명령
melos run generate:{feature_name}

# 또는 전체 빌드
melos run build
```

**생성 확인 항목:**

| 파일 패턴 | 설명 |
|----------|------|
| `*.freezed.dart` | Freezed 생성 코드 |
| `*.g.dart` | Injectable/JSON 생성 코드 |
| `*_router.dart` | Auto_route 생성 코드 |
| `*_database.g.dart` | Drift 생성 코드 |

### 1.3 테스트

#### 단위 테스트 (UseCase)

```dart
test('should return user when repository succeeds', () async {
  // Arrange
  when(() => mockRepository.getUser(any()))
    .thenAnswer((_) async => Right(testUser));

  // Act
  final result = await useCase(GetUserParams(id: 1));

  // Assert
  expect(result, Right(testUser));
  verify(() => mockRepository.getUser(1)).called(1);
});
```

#### BLoC 테스트 (GetIt 모킹)

```dart
blocTest<HomeBloC, HomeState>(
  'emits [loading, loaded] when LoadUser succeeds',
  setUp: () {
    when(() => mockRepository.getUser(any()))
      .thenAnswer((_) async => Right(testUser));
  },
  build: HomeBloC.new,  // ✅ 기본 생성자
  act: (bloc) => bloc.add(LoadUser(id: 1)),
  expect: () => [HomeLoading(), HomeLoaded(testUser)],
);
```

#### 테스트 명령

```bash
# 단일 Feature 테스트
flutter test feature/{type}/{feature_name}/test/

# 커버리지 리포트
melos run test:with-html-coverage
```

**커버리지 목표**: 80% 이상

---

## 2. PR Review 검증 상세

### 2.1 PR 메타 정보

| 항목 | 검증 기준 |
|------|----------|
| 제목 형식 | `type(scope): gitmoji 한글 설명` |
| 이슈 연결 | Closes #123 또는 Fixes #123 |
| 라벨 | feature, bugfix, refactor 등 |

**제목 예시:**
```
feat(auth): ✨ 소셜 로그인 기능 추가
fix(home): 🐛 피드 무한 스크롤 버그 수정
refactor(store): ♻️ 상품 목록 쿼리 최적화
```

### 2.2 변경 사항 범위

| 검증 항목 | 설명 |
|----------|------|
| 목적 명확성 | PR 설명에서 변경 목적 파악 가능 |
| 단일 목적 | 한 PR = 한 기능/수정 |
| 변경 범위 | 필요한 파일만 변경 |
| 불필요한 변경 없음 | 포맷팅, 공백 등 무관한 변경 없음 |

### 2.3 코드 품질

#### 아키텍처 검증

```
✅ 올바른 의존성 방향:
Presentation → Domain → Data

❌ 잘못된 의존성:
Presentation → Data (Domain 우회)
Feature A → Feature B (직접 참조)
```

#### 네이밍 컨벤션

| 유형 | 규칙 | 예시 |
|------|------|------|
| 클래스 | PascalCase | `UserRepository` |
| 변수/함수 | camelCase | `getUserData()` |
| 상수 | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |
| 파일 | snake_case | `user_repository.dart` |

### 2.4 상태 관리 검증

```dart
// ✅ 올바른 BLoC 패턴
@freezed
class HomeEvent with _$HomeEvent {
  const factory HomeEvent.loadUser(int id) = LoadUser;
}

@freezed
class HomeState with _$HomeState {
  const factory HomeState.initial() = _Initial;
  const factory HomeState.loading() = _Loading;
  const factory HomeState.loaded(User user) = _Loaded;
  const factory HomeState.error(Failure failure) = _Error;
}
```

**검증 항목:**
- [ ] Event/State Freezed 사용
- [ ] 로딩 상태 처리
- [ ] 에러 상태 처리
- [ ] dispose에서 리소스 해제

### 2.5 보안 검증

| 검증 항목 | 위험도 | 확인 방법 |
|----------|--------|----------|
| 하드코딩 시크릿 | 🔴 | API 키, 토큰 검색 |
| 민감 정보 로깅 | 🔴 | print, log 문 확인 |
| 입력 값 검증 | 🟡 | 사용자 입력 처리 확인 |

```bash
# 시크릿 검색
grep -r "api_key\|secret\|password\|token" --include="*.dart"
```

### 2.6 성능 검증

| 검증 항목 | 확인 방법 |
|----------|----------|
| N+1 쿼리 | 반복문 내 DB 호출 확인 |
| 불필요한 리렌더링 | buildWhen, BlocSelector 사용 |
| 이미지 최적화 | cacheWidth, cacheHeight 적용 |
| 캐싱 전략 | SWR, Cache-First 적용 |

---

## 3. CI/CD 확인

```bash
# PR 상태 확인
gh pr checks [PR_NUMBER]

# PR 웹에서 보기
gh pr view [PR_NUMBER] --web
```

| 체크 항목 | 설명 |
|----------|------|
| Build | iOS/Android 빌드 성공 |
| Test | 모든 테스트 통과 |
| Lint | 정적 분석 통과 |
| Coverage | 커버리지 임계값 충족 |

---

## 4. 트러블슈팅

### 빌드 실패

| 증상 | 원인 | 해결 |
|------|------|------|
| Freezed 에러 | 코드 생성 안 됨 | `melos run build` |
| Import 에러 | 순환 참조 | 의존성 방향 수정 |
| Type 에러 | DTO/Entity 불일치 | 매퍼 확인 |

### 테스트 실패

| 증상 | 원인 | 해결 |
|------|------|------|
| Mock 에러 | registerFallbackValue 누락 | 테스트 setUp 확인 |
| State 불일치 | BLoC 테스트 설정 오류 | build() 함수 확인 |
| Widget 에러 | 필수 위젯 래핑 누락 | MaterialApp 래핑 |

### 정적 분석 에러

```bash
# 분석 실행
melos run analyze

# 포맷팅
melos run format
```

| 에러 유형 | 해결 |
|----------|------|
| unused_import | import 제거 |
| prefer_const | const 추가 |
| avoid_print | Logger 사용 |

# Code Review Reference Guide

카테고리별 상세 체크리스트 및 검토 기준입니다.

---

## 1. 🏗️ 아키텍처 (Architecture)

### Clean Architecture 검토

| 항목 | 검토 기준 | 심각도 |
|------|----------|--------|
| 레이어 분리 | Domain → Data → Presentation 의존성 방향 | 🔴 |
| UseCase 사용 | 비즈니스 로직이 UseCase를 통해 접근 | 🔴 |
| Repository 인터페이스 | I 접두사, Domain 레이어에 정의 | 🟡 |
| Entity 불변성 | Freezed 사용, 불변 객체 | 🟡 |

### Feature 모듈 독립성

```dart
// ✅ 올바른 의존성
import 'package:core/core.dart';
import 'package:feature_common_auth/auth.dart';

// ❌ 잘못된 의존성 (다른 application feature 직접 참조)
import 'package:feature_application_home/home.dart';
```

### 체크리스트

- [ ] Domain → Data → Presentation 의존성 방향 준수
- [ ] UseCase를 통한 비즈니스 로직 접근
- [ ] Repository 인터페이스 분리 (I 접두사)
- [ ] Feature 모듈 간 직접 의존 없음
- [ ] 공유 코드는 common 또는 core로 분리
- [ ] 과도한 추상화 없음

---

## 2. 🧩 상태 관리 (State Management)

### BLoC 패턴 검토

| 항목 | 검토 기준 | 심각도 |
|------|----------|--------|
| Event/State 정의 | Freezed 사용, Union Type | 🟡 |
| 상태 불변성 | copyWith 사용, 직접 변경 금지 | 🔴 |
| 에러 처리 | Either 패턴, Failure 클래스 | 🟡 |
| 리소스 해제 | close()에서 구독 취소 | 🔴 |

### 상태 정의 패턴

```dart
// ✅ 올바른 상태 정의
@freezed
class HomeState with _$HomeState {
  const factory HomeState.initial() = _Initial;
  const factory HomeState.loading() = _Loading;
  const factory HomeState.loaded(User user) = _Loaded;
  const factory HomeState.error(Failure failure) = _Error;
}

// ❌ 잘못된 상태 정의 (Freezed 미사용)
class HomeState {
  final bool isLoading;
  final User? user;
  final String? error;
}
```

### 체크리스트

- [ ] Event/State에 Freezed 사용
- [ ] Union Type으로 상태 분기
- [ ] 적절한 에러 핸들링
- [ ] 로딩 상태 관리
- [ ] dispose에서 리소스 해제
- [ ] 전역/로컬 상태 적절히 구분

---

## 3. 🔒 보안 (Security)

### 민감 정보 검토

| 항목 | 검토 기준 | 심각도 |
|------|----------|--------|
| 하드코딩 시크릿 | API 키, 토큰 노출 | 🔴 |
| 로그 출력 | 민감 정보 로깅 | 🔴 |
| 환경 변수 | Envied 사용 | 🟡 |

### 입력 검증

```dart
// ✅ 올바른 검증
if (!EmailValidator.validate(email)) {
  return left(ValidationFailure('Invalid email'));
}

// ❌ 검증 없이 직접 사용
final user = await api.login(email, password);
```

### 체크리스트

- [ ] API 키, 시크릿 하드코딩 없음
- [ ] 로그에 민감 정보 출력 없음
- [ ] 사용자 입력 sanitization
- [ ] SQL Injection, XSS 방지
- [ ] 보호된 엔드포인트 접근 제어
- [ ] 토큰 관리 적절성

---

## 4. ⚡ 성능 (Performance)

### 리빌드 최적화

| 항목 | 검토 기준 | 심각도 |
|------|----------|--------|
| const 위젯 | 가능한 곳에 const 사용 | 🟡 |
| buildWhen | BlocBuilder 조건 지정 | 🟡 |
| BlocSelector | 세분화된 상태 구독 | 🟢 |

### 이미지 최적화

```dart
// ✅ 올바른 이미지 처리
CachedNetworkImage(
  imageUrl: url,
  cacheWidth: 200,
  cacheHeight: 200,
)

// ❌ 캐시 크기 미지정
Image.network(url)
```

### 체크리스트

- [ ] const 위젯 활용
- [ ] BlocBuilder buildWhen 사용
- [ ] BlocSelector로 세분화
- [ ] 이미지 cacheWidth/cacheHeight 적용
- [ ] 병렬 처리 가능한 작업 병렬화
- [ ] debounce/throttle 적용
- [ ] dispose에서 리소스 해제
- [ ] Stream subscription 취소

---

## 5. 🧪 테스트 (Testing)

### 테스트 커버리지

| 항목 | 검토 기준 | 심각도 |
|------|----------|--------|
| UseCase 테스트 | 단위 테스트 필수 | 🔴 |
| Repository 테스트 | Mocked data source | 🟡 |
| BLoC 테스트 | 상태 전이 검증 | 🟡 |
| Widget 테스트 | 주요 UI 컴포넌트 | 🟢 |

### 테스트 패턴

```dart
// ✅ 올바른 테스트 패턴 (AAA)
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

### 체크리스트

- [ ] UseCase 단위 테스트
- [ ] Repository 테스트 (mocked)
- [ ] BLoC 테스트
- [ ] 의미 있는 테스트 케이스
- [ ] Edge case 커버
- [ ] Arrange-Act-Assert 패턴
- [ ] 외부 의존성 격리

---

## 6. 📖 가독성 (Readability)

### 네이밍 컨벤션

| 항목 | 규칙 | 예시 |
|------|------|------|
| 클래스 | PascalCase | `UserRepository` |
| 변수/함수 | camelCase | `getUserData()` |
| 상수 | SCREAMING_SNAKE | `MAX_RETRY_COUNT` |
| 파일 | snake_case | `user_repository.dart` |

### 코드 구조

```dart
// ✅ 단일 책임 원칙
class UserRepository implements IUserRepository {
  // 사용자 관련 로직만
}

// ❌ 여러 책임 혼재
class UserRepository {
  void getUser() {}
  void sendEmail() {}  // 이메일은 별도 서비스로
  void generateReport() {}  // 리포트도 별도로
}
```

### 체크리스트

- [ ] 명확하고 의미 있는 이름
- [ ] 프로젝트 컨벤션 준수
- [ ] 축약어 사용 최소화
- [ ] 적절한 파일/클래스 크기
- [ ] 단일 책임 원칙
- [ ] 중복 코드 제거
- [ ] 불필요한 주석 없음
- [ ] 복잡한 로직에 설명 주석

---

## 7. 🌐 국제화 (i18n)

### 번역 키 사용

```dart
// ✅ 올바른 사용
Text(context.t.common.save)
Text(context.t.user.greeting(name: user.name))

// ❌ 하드코딩
Text('저장')
Text('${user.name}님, 안녕하세요!')
```

### 체크리스트

- [ ] 모든 UI 텍스트 번역 키 사용
- [ ] context.t.* 패턴 사용
- [ ] 적절한 pluralization
- [ ] 동적 값 파라미터화
- [ ] RTL 지원 (필요시)

---

## 8. ♿ 접근성 (Accessibility)

### Semantics 적용

```dart
// ✅ 올바른 적용
Semantics(
  label: '장바구니에 추가',
  button: true,
  child: IconButton(
    icon: Icon(Icons.add_shopping_cart),
    onPressed: addToCart,
  ),
)

// ❌ Semantics 없음
IconButton(
  icon: Icon(Icons.add_shopping_cart),
  onPressed: addToCart,
)
```

### 체크리스트

- [ ] 적절한 semantic label
- [ ] 스크린 리더 지원
- [ ] 최소 48x48 터치 타겟
- [ ] WCAG 색상 대비 기준 충족
- [ ] 색상만으로 정보 전달하지 않음

---

## 자동화 도구

### 정적 분석

```bash
# 전체 분석
melos run analyze

# 병렬 Lint
melos run lint:parallel

# 포맷팅 검사
melos run format
dart format --set-exit-if-changed .
```

### 테스트

```bash
# 전체 테스트
melos run test

# 커버리지 리포트
melos run test:with-html-coverage
```

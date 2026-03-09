# Code Review Templates

코드 리뷰 결과 작성을 위한 템플릿입니다.

---

## Template A: 전체 리뷰 결과

```markdown
# Code Review: [PR 제목 또는 파일명]

## Summary

**Overall**: ⭐⭐⭐⭐☆ (4/5)

**리뷰어**: [이름]
**날짜**: [YYYY-MM-DD]

| 카테고리 | 점수 | 주요 이슈 |
|---------|------|----------|
| 🏗️ 아키텍처 | ✅ | - |
| 🧩 상태 관리 | ⚠️ | BlocBuilder 최적화 필요 |
| 🔒 보안 | ✅ | - |
| ⚡ 성능 | ⚠️ | 이미지 캐시 크기 미지정 |
| 🧪 테스트 | ❌ | UseCase 테스트 누락 |
| 📖 가독성 | ✅ | - |
| 🌐 국제화 | ✅ | - |
| ♿ 접근성 | ⚠️ | semantic label 일부 누락 |

---

## 🔴 Critical Issues (머지 전 필수 수정)

### 1. [보안] API 키 하드코딩
- **파일**: `lib/core/config.dart:15`
- **문제**: API 키가 소스 코드에 직접 포함됨
- **영향**: 보안 취약점, 키 노출 위험
- **수정 방안**: Envied를 통한 환경 변수 사용

```dart
// Before
const apiKey = 'sk-1234567890abcdef';

// After
@Envied(path: '.env')
abstract class AppConfig {
  @EnviedField(varName: 'API_KEY')
  static const String apiKey = _AppConfig.apiKey;
}
```

### 2. [테스트] UseCase 테스트 누락
- **파일**: `test/domain/usecase/`
- **문제**: 핵심 비즈니스 로직 테스트 없음
- **영향**: 회귀 버그 발생 위험
- **수정 방안**: UseCase별 단위 테스트 추가

---

## 🟡 Improvements (권장 수정)

### 1. [성능] 이미지 캐시 크기 지정 필요
- **파일**: `lib/presentation/widget/product_card.dart:42`
- **현재 코드**:
```dart
Image.network(product.imageUrl)
```
- **권장 코드**:
```dart
CachedNetworkImage(
  imageUrl: product.imageUrl,
  cacheWidth: 200,
  cacheHeight: 200,
)
```

### 2. [상태 관리] BlocBuilder 최적화
- **파일**: `lib/presentation/page/home_page.dart:78`
- **현재 코드**:
```dart
BlocBuilder<HomeBloC, HomeState>(
  builder: (context, state) => UserWidget(state.user),
)
```
- **권장 코드**:
```dart
BlocBuilder<HomeBloC, HomeState>(
  buildWhen: (previous, current) => previous.user != current.user,
  builder: (context, state) => UserWidget(state.user),
)
```

---

## 🟢 Suggestions (선택적 개선)

### 1. [가독성] 변수명 개선 제안
- `data` → `userProfile`
- `list` → `productItems`
- `result` → `authResult`

### 2. [구조] 위젯 분리 제안
- `_buildHeader()` → `HomeHeader` 위젯으로 분리
- 재사용성 및 테스트 용이성 향상

---

## ❓ Questions

1. `auth_bloc.dart:45` - 이 예외 처리 로직의 의도가 무엇인가요?
2. `user_repository.dart:89` - 캐싱 만료 시간이 5분인 이유가 있나요?

---

## 결론

전반적으로 좋은 코드입니다. Critical Issues 2개 수정 후 머지 가능합니다.
```

---

## Template B: 간단 리뷰 결과

```markdown
# Quick Review: [파일명]

**결과**: ✅ Approved with comments

## 주요 피드백

1. **[성능]** 이미지 캐시 크기 추가 권장
   - `product_card.dart:42`

2. **[가독성]** 변수명 `data` → `userProfile` 변경 권장
   - `home_bloc.dart:25`

## 잘한 점 👍

- Clean Architecture 패턴 잘 준수
- Freezed 활용한 불변 상태 관리
- 적절한 에러 핸들링
```

---

## Template C: 카테고리별 상세 리뷰

```markdown
# 상세 리뷰: [카테고리명]

## 🏗️ 아키텍처 리뷰

### 검토 항목

| 항목 | 상태 | 비고 |
|------|------|------|
| Clean Architecture 레이어 분리 | ✅ | |
| UseCase 패턴 사용 | ✅ | |
| Repository 인터페이스 분리 | ⚠️ | 일부 누락 |
| Feature 모듈 독립성 | ✅ | |

### 상세 피드백

#### Repository 인터페이스 분리 (⚠️)

**현재 상태**:
- `CartRepository`가 인터페이스 없이 직접 구현됨

**권장 변경**:
1. `ICartRepository` 인터페이스 생성
2. Domain 레이어에 인터페이스 배치
3. Data 레이어에서 구현

```dart
// domain/repository/i_cart_repository.dart
abstract interface class ICartRepository {
  Future<Either<Failure, Cart>> getCart();
  Future<Either<Failure, void>> addItem(CartItem item);
}

// data/repository/cart_repository.dart
@LazySingleton(as: ICartRepository)
class CartRepository implements ICartRepository {
  // 구현
}
```
```

---

## Template D: PR 코멘트

### 필수 수정 (Blocking)

```markdown
🔴 **[필수]** 보안 취약점

**위치**: `lib/core/config.dart:15`

**문제**: API 키가 하드코딩되어 있습니다.

**수정 방안**:
```dart
// Envied 사용
@EnviedField(varName: 'API_KEY')
static const String apiKey = _AppConfig.apiKey;
```

이 이슈가 해결되기 전까지 머지할 수 없습니다.
```

### 개선 요청 (Non-blocking)

```markdown
🟡 **[개선]** 성능 최적화

**위치**: `lib/presentation/widget/product_card.dart:42`

**현재 코드**:
```dart
Image.network(product.imageUrl)
```

**권장 코드**:
```dart
CachedNetworkImage(
  imageUrl: product.imageUrl,
  cacheWidth: 200,
)
```

이미지 캐시 크기를 지정하면 메모리 사용량이 줄어듭니다.
```

### 제안/질문

```markdown
🟢 **[제안]** 변수명 개선

**위치**: `lib/presentation/bloc/home_bloc.dart:25`

변수명 `data`를 `userProfile`로 변경하면 가독성이 향상됩니다.

---

❓ **[질문]** 예외 처리 의도

**위치**: `lib/data/repository/auth_repository.dart:45`

이 try-catch 블록에서 모든 예외를 무시하는 이유가 있나요?
```

### 칭찬

```markdown
✨ **좋아요!** 깔끔한 상태 관리

**위치**: `lib/presentation/bloc/cart_bloc.dart`

Freezed와 Union Type을 활용한 상태 관리가 매우 깔끔합니다.
특히 로딩/에러/성공 상태 분리가 잘 되어 있네요!
```

---

## Template E: 리뷰 체크리스트 (Self-Review)

```markdown
# Self-Review Checklist

PR 제출 전 자가 점검 체크리스트입니다.

## 기본 사항

- [ ] 코드가 빌드됩니다
- [ ] 모든 테스트가 통과합니다
- [ ] Lint 에러가 없습니다
- [ ] 관련 이슈가 연결되어 있습니다

## 아키텍처

- [ ] Clean Architecture 레이어 분리 준수
- [ ] Feature 모듈 간 직접 의존 없음
- [ ] 새 코드가 기존 패턴을 따름

## 보안

- [ ] 하드코딩된 시크릿 없음
- [ ] 로그에 민감 정보 없음
- [ ] 입력 값 검증 적용

## 성능

- [ ] const 위젯 사용
- [ ] 이미지 캐시 크기 지정
- [ ] dispose에서 리소스 해제

## 테스트

- [ ] 새 기능에 테스트 추가
- [ ] Edge case 커버

## 국제화

- [ ] 하드코딩된 문자열 없음
- [ ] 번역 키 사용

## 최종 확인

- [ ] 불필요한 console.log/print 제거
- [ ] TODO 주석 해결 또는 이슈 등록
- [ ] 커밋 메시지가 컨벤션을 따름
```

---

## Template F: 리뷰 요약 (Approve/Request Changes)

### Approve ✅

```markdown
LGTM! 🎉

모든 체크리스트 항목 확인 완료했습니다.

**확인 항목**:
- ✅ 빌드 성공
- ✅ 테스트 통과
- ✅ 보안 이슈 없음
- ✅ 코드 품질 양호

좋은 작업입니다!
```

### Request Changes 🔄

```markdown
수정 요청 사항이 있습니다.

**필수 수정** (머지 전 해결 필요):
1. API 키 하드코딩 제거 (`config.dart:15`)
2. UseCase 테스트 추가

**권장 수정** (선택적):
1. 이미지 캐시 크기 지정
2. BlocBuilder 최적화

필수 수정 사항 해결 후 다시 리뷰 요청해 주세요.
```

### Comment 💬

```markdown
전반적으로 좋습니다. 몇 가지 질문/제안이 있습니다.

**질문**:
1. 캐싱 전략 선택 이유가 궁금합니다

**제안**:
1. 에러 메시지 국제화 고려해 주세요

확인 후 답변 부탁드립니다.
```

# i18n Templates

국제화 번역 패턴 템플릿입니다.

---

## Template A: 기본 번역 구조

### strings.i18n.yaml (한국어)

```yaml
@@locale: ko

common:
  appName: 펫메디
  ok: 확인
  cancel: 취소
  save: 저장
  delete: 삭제
  edit: 수정
  close: 닫기
  loading: 로딩 중...
  error: 오류가 발생했습니다
  retry: 다시 시도
  noData: 데이터가 없습니다

auth:
  login: 로그인
  logout: 로그아웃
  signUp: 회원가입
  email: 이메일
  password: 비밀번호
  forgotPassword: 비밀번호를 잊으셨나요?

navigation:
  home: 홈
  search: 검색
  mypage: 마이페이지
  settings: 설정
```

### strings_en.i18n.yaml (영어)

```yaml
@@locale: en

common:
  appName: Petmedi
  ok: OK
  cancel: Cancel
  save: Save
  delete: Delete
  edit: Edit
  close: Close
  loading: Loading...
  error: An error occurred
  retry: Retry
  noData: No data available

auth:
  login: Login
  logout: Logout
  signUp: Sign Up
  email: Email
  password: Password
  forgotPassword: Forgot password?

navigation:
  home: Home
  search: Search
  mypage: My Page
  settings: Settings
```

---

## Template B: 파라미터 패턴

### 사용자 인사말

```yaml
user:
  # name: 사용자 이름
  greeting: '$name님, 안녕하세요!'
  welcomeBack: '$name님, 다시 오셨군요!'

  # date: 가입 날짜 (yyyy-MM-dd 형식)
  memberSince: '$date에 가입'

  # count: 포인트 수
  points: '$count 포인트 보유'

  # level: 회원 등급
  levelInfo: '$level 등급 회원입니다'
```

### Dart 사용 예시

```dart
// 사용자 인사
Text(context.t.user.greeting(name: user.displayName))

// 포인트 표시
Text(context.t.user.points(count: user.points.toString()))

// 가입일 표시
Text(context.t.user.memberSince(date: DateFormat('yyyy-MM-dd').format(user.createdAt)))
```

---

## Template C: 복수형 패턴

### 아이템 카운트

```yaml
items:
  count(param=n):
    zero: 항목 없음
    one: 항목 1개
    other: 항목 $n개

cart:
  itemCount(param=count):
    zero: 장바구니가 비어있습니다
    one: 장바구니에 상품 1개
    other: 장바구니에 상품 $count개

notifications:
  unread(param=count):
    zero: 읽지 않은 알림 없음
    one: 읽지 않은 알림 1개
    other: 읽지 않은 알림 $count개

messages:
  count(param=n):
    zero: 메시지 없음
    one: 메시지 1개
    other: 메시지 $n개

followers:
  count(param=n):
    zero: 팔로워 없음
    one: 팔로워 1명
    other: 팔로워 $n명
```

### Dart 사용 예시

```dart
// 장바구니 아이템 수
Text(context.t.cart.itemCount(count: cartItems.length))

// 알림 배지
Badge(
  label: Text(context.t.notifications.unread(count: unreadCount)),
)

// 팔로워 수
Text(context.t.followers.count(n: followerCount))
```

---

## Template D: 컨텍스트 기반 패턴

### Enum 기반 번역

```yaml
pet:
  type(context=PetType):
    dog: 강아지
    cat: 고양이
    bird: 새
    fish: 물고기
    hamster: 햄스터
    other: 기타

order:
  status(context=OrderStatus):
    pending: 대기 중
    confirmed: 확인됨
    shipping: 배송 중
    delivered: 배송 완료
    cancelled: 취소됨

payment:
  method(context=PaymentMethod):
    card: 카드 결제
    bank: 계좌이체
    kakao: 카카오페이
    naver: 네이버페이
```

### Dart Enum 정의

```dart
// lib/domain/entity/pet_type.dart
enum PetType {
  dog,
  cat,
  bird,
  fish,
  hamster,
  other,
}

// 사용
Text(context.t.pet.type(context: pet.type))
Text(context.t.order.status(context: order.status))
```

---

## Template E: 에러 메시지 패턴

### 폼 검증 에러

```yaml
validation:
  required: 필수 입력 항목입니다
  email:
    invalid: 올바른 이메일 형식이 아닙니다
    exists: 이미 사용 중인 이메일입니다
  password:
    tooShort: 비밀번호는 최소 8자 이상이어야 합니다
    tooWeak: 비밀번호가 너무 약합니다
    mismatch: 비밀번호가 일치하지 않습니다
  phone:
    invalid: 올바른 전화번호 형식이 아닙니다

error:
  network: 네트워크 연결을 확인해주세요
  server: 서버 오류가 발생했습니다
  timeout: 요청 시간이 초과되었습니다
  unauthorized: 로그인이 필요합니다
  forbidden: 접근 권한이 없습니다
  notFound: 요청한 정보를 찾을 수 없습니다
  unknown: 알 수 없는 오류가 발생했습니다
```

### Dart 사용 예시

```dart
// 폼 검증
TextFormField(
  validator: (value) {
    if (value == null || value.isEmpty) {
      return context.t.validation.required;
    }
    if (!EmailValidator.validate(value)) {
      return context.t.validation.email.invalid;
    }
    return null;
  },
)

// 에러 처리
result.fold(
  (failure) => ScaffoldMessenger.of(context).showSnackBar(
    SnackBar(content: Text(context.t.error.network)),
  ),
  (success) => navigateToHome(),
);
```

---

## Template F: 날짜/시간 패턴

### 상대 시간

```yaml
time:
  justNow: 방금 전
  minutesAgo: '$minutes분 전'
  hoursAgo: '$hours시간 전'
  daysAgo: '$days일 전'
  weeksAgo: '$weeks주 전'
  monthsAgo: '$months개월 전'
  yearsAgo: '$years년 전'

  # 미래
  inMinutes: '$minutes분 후'
  inHours: '$hours시간 후'
  inDays: '$days일 후'
```

### Dart 사용 예시

```dart
String getRelativeTime(BuildContext context, DateTime dateTime) {
  final now = DateTime.now();
  final difference = now.difference(dateTime);

  if (difference.inMinutes < 1) {
    return context.t.time.justNow;
  } else if (difference.inMinutes < 60) {
    return context.t.time.minutesAgo(minutes: difference.inMinutes.toString());
  } else if (difference.inHours < 24) {
    return context.t.time.hoursAgo(hours: difference.inHours.toString());
  } else if (difference.inDays < 7) {
    return context.t.time.daysAgo(days: difference.inDays.toString());
  } else if (difference.inDays < 30) {
    return context.t.time.weeksAgo(weeks: (difference.inDays ~/ 7).toString());
  } else if (difference.inDays < 365) {
    return context.t.time.monthsAgo(months: (difference.inDays ~/ 30).toString());
  } else {
    return context.t.time.yearsAgo(years: (difference.inDays ~/ 365).toString());
  }
}
```

---

## Template G: 리치 텍스트 패턴

### 링크가 포함된 텍스트

```yaml
legal:
  termsAgreement: '이용약관에 동의합니다. <link>자세히 보기</link>'
  privacyAgreement: '개인정보 처리방침에 동의합니다. <link>자세히 보기</link>'

marketing:
  promotion: '<highlight>특별 할인</highlight> 이벤트가 진행 중입니다!'
  newFeature: '새로운 기능이 추가되었습니다. <link>확인하기</link>'
```

### Dart 사용 예시

```dart
// 리치 텍스트 빌더
Text.rich(
  context.t.legal.termsAgreement(
    link: (text) => TextSpan(
      text: text,
      style: TextStyle(
        color: AppColors.primary,
        decoration: TextDecoration.underline,
      ),
      recognizer: TapGestureRecognizer()
        ..onTap = () => Navigator.pushNamed(context, '/terms'),
    ),
  ),
)

// 하이라이트 텍스트
Text.rich(
  context.t.marketing.promotion(
    highlight: (text) => TextSpan(
      text: text,
      style: TextStyle(
        color: AppColors.accent,
        fontWeight: FontWeight.bold,
      ),
    ),
  ),
)
```

---

## 슬랑 설정 템플릿

### slang.yaml

```yaml
# Slang 설정 파일
base_locale: ko
fallback_strategy: base_locale

# 입력 설정
input_directory: lib/translations
input_file_pattern: .i18n.yaml

# 출력 설정
output_directory: lib/src/translations
output_file_name: translations.g.dart
output_format: single_file

# 케이스 설정
key_case: camel
key_map_case: camel
param_case: camel

# 기타 설정
string_interpolation: dart
flat_map: false
timestamp: true
statistics: true

# 인터페이스 생성 (필요시)
interfaces:
  PageData:
    paths:
      - home
      - settings
      - profile
```

---

## GPT 번역 힌트 템플릿

### 번역 품질 향상을 위한 주석

```yaml
# 앱 이름 - 번역하지 않음
common:
  appName: Petmedi

# 버튼 텍스트 - 짧고 명확하게
buttons:
  submit: 제출  # Submit
  confirm: 확인  # Confirm, OK

# 펫 관련 용어 - 친근한 톤 유지
pet:
  # 반려동물 종류를 나타냄
  type(context=PetType):
    dog: 강아지  # puppy/dog - use "dog" for general
    cat: 고양이  # cat/kitty - use "cat" for general
```

# i18n Reference Guide

slang 기반 국제화 상세 API 및 문법 레퍼런스입니다.

## YAML 문법 레퍼런스

### 기본 문자열

```yaml
common:
  appName: 펫메디
  ok: 확인
  cancel: 취소
  save: 저장
  loading: 로딩 중...
```

### 중첩 구조

```yaml
auth:
  login:
    title: 로그인
    button: 로그인하기
    error: 로그인에 실패했습니다
  signup:
    title: 회원가입
    button: 가입하기
```

### 파라미터 (Placeholders)

```yaml
user:
  greeting: '$name님, 안녕하세요!'
  points: '$count 포인트 보유'
  joinDate: '$date에 가입'
```

**Dart 사용:**
```dart
context.t.user.greeting(name: 'John')
context.t.user.points(count: '100')
```

### 복수형 (Pluralization)

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
```

**Dart 사용:**
```dart
context.t.items.count(n: 0)     // "항목 없음"
context.t.items.count(n: 1)     // "항목 1개"
context.t.items.count(n: 5)     // "항목 5개"
```

### 컨텍스트 기반 (Context-Based)

```yaml
pet:
  type(context=PetType):
    dog: 강아지
    cat: 고양이
    bird: 새
    other: 반려동물

gender:
  pronoun(context=Gender):
    male: 그
    female: 그녀
    other: 그들
```

**Dart 사용:**
```dart
context.t.pet.type(context: PetType.dog)  // "강아지"
```

### 리치 텍스트 (Rich Text)

```yaml
terms:
  agreement: '이용약관에 동의합니다. <link>자세히 보기</link>'
```

**Dart 사용:**
```dart
context.t.terms.agreement(
  link: (text) => TextSpan(
    text: text,
    style: TextStyle(color: Colors.blue),
    recognizer: TapGestureRecognizer()..onTap = () => openTerms(),
  ),
)
```

---

## 파일 구조 레퍼런스

### 디렉토리 레이아웃

```
shared/
├── i10n/                           # 앱 번역
│   └── lib/
│       ├── translations/
│       │   ├── strings.i18n.yaml   # 기본 (한국어)
│       │   └── strings_en.i18n.yaml # 영어
│       └── src/
│           └── translations/
│               └── translations.g.dart
│
└── i10n_web/                       # 웹 번역 (별도)
    └── lib/
        ├── translations/
        │   ├── strings.i18n.yaml
        │   └── strings_en.i18n.yaml
        └── src/
            └── translations/
                └── translations.g.dart
```

### slang.yaml 설정

```yaml
base_locale: ko
fallback_strategy: base_locale
input_directory: lib/translations
input_file_pattern: .i18n.yaml
output_directory: lib/src/translations
output_file_name: translations.g.dart
output_format: single_file
key_case: camel
key_map_case: camel
param_case: camel
string_interpolation: dart
flat_map: false
timestamp: true
statistics: true
```

---

## 코드 사용 레퍼런스

### 기본 접근

```dart
import 'package:i10n/i10n.dart';

// BuildContext 확장
Text(context.t.common.appName)

// 직접 접근 (context 없이)
final appName = AppLocale.ko.translations.common.appName;
```

### 앱 설정

```dart
MaterialApp(
  locale: TranslationProvider.of(context).flutterLocale,
  supportedLocales: AppLocaleUtils.supportedLocales,
  localizationsDelegates: GlobalMaterialLocalizations.delegates,
)
```

### 로케일 변경

```dart
// 로케일 변경
LocaleSettings.setLocale(AppLocale.en);

// 현재 로케일 확인
final currentLocale = LocaleSettings.currentLocale;

// 시스템 로케일 사용
LocaleSettings.useDeviceLocale();
```

### 웹 번역 (별도)

```dart
import 'package:i10n_web/i10n_web.dart';

// 웹 전용 번역
Text(context.wt.common.title)
```

---

## 명령어 레퍼런스

### 코드 생성

```bash
# 번역 코드 생성
melos run generate:locale

# 강제 재생성
cd shared/i10n && dart run slang
```

### GPT 자동 번역

```bash
# 영어 자동 번역 (API 키 필요)
melos run generate:locale:gpt

# 직접 실행
cd shared/i10n && dart run slang:gpt
```

### 분석

```bash
# 누락된 번역 확인
dart run slang analyze

# 통계 출력
dart run slang analyze --stats
```

---

## 트러블슈팅

### 번역이 적용 안 됨

| 증상 | 원인 | 해결 |
|------|------|------|
| 키가 없다는 에러 | 코드 생성 안 됨 | `melos run generate:locale` 실행 |
| 영어가 표시 안 됨 | 영어 파일 누락 | `strings_en.i18n.yaml` 확인 |
| 복수형 동작 안 함 | 문법 오류 | `param=n` 형식 확인 |

### 코드 생성 에러

| 증상 | 원인 | 해결 |
|------|------|------|
| YAML 파싱 에러 | 들여쓰기 오류 | 스페이스 2개로 통일 |
| 중복 키 에러 | 동일 키 존재 | 키 이름 변경 |
| 파라미터 에러 | $ 누락 | `$name` 형식 사용 |

### GPT 번역 에러

| 증상 | 원인 | 해결 |
|------|------|------|
| API 에러 | 키 없음 | OPENAI_API_KEY 환경 변수 설정 |
| 번역 품질 낮음 | 컨텍스트 부족 | 주석으로 힌트 제공 |

---

## Best Practices

### 키 네이밍

```yaml
# ✅ 좋은 예
user:
  profile:
    editButton: 프로필 수정
    saveButton: 저장

# ❌ 나쁜 예
editProfileBtn: 프로필 수정  # 중첩 구조 사용하지 않음
user_profile_save: 저장       # snake_case 사용
```

### 복수형 처리

```yaml
# ✅ 모든 케이스 처리
notifications:
  count(param=n):
    zero: 알림 없음
    one: 알림 1개
    other: 알림 $n개

# ❌ 불완전한 처리
notifications:
  count: '알림 $n개'  # 0, 1 케이스 처리 안 됨
```

### 파라미터 설명

```yaml
# ✅ 주석으로 파라미터 설명
user:
  # name: 사용자 이름
  greeting: '$name님, 안녕하세요!'

  # count: 보유 포인트 수
  points: '$count 포인트'
```

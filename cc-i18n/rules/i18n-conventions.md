# i18n 컨벤션

이 프로젝트는 **slang** 패키지를 사용하여 국제화(i18n)를 처리합니다.

## 번역 접근 API

### 프로젝트 표준: `context.i10n`

```dart
// ✅ CORRECT: package:core에서 import (표준)
import 'package:core/core.dart';  // BuildContextExt 포함

final translations = context.i10n.console.sample_book;
Text(context.i10n.common.save)

// ❌ WRONG: package:i10n에서 직접 import 금지
import 'package:i10n/i10n.dart';  // extension 충돌 발생!

// ❌ WRONG: context.translations 사용 금지
final translations = context.translations.console.sample_book;  // 사용 금지
```

**통계**: `context.i10n` 389건 vs `context.translations` 1건 (레거시)

### ⚠️ Extension 충돌 주의 (ambiguous_extension_member_access)

`context.i10n` extension은 **`package:core`에서만** 제공됩니다.

| 패키지 | Extension | 사용 여부 |
|--------|-----------|----------|
| `package:core/core.dart` | `BuildContextExt.i10n` | ✅ **표준** |
| `package:i10n/i10n.dart` | - | ❌ extension 없음 |

**Import 규칙**:
```dart
// ✅ CORRECT: core만 import
import 'package:core/core.dart';

// ✅ CORRECT: extension만 필요한 경우
import 'package:core/core.dart' show BuildContextExt;

// ⚠️ 주의: i10n 패키지는 extension 제공 안함
// slang 번역 파일과 LocalizationsDelegate만 export
import 'package:i10n/i10n.dart';
```

> **참고**: PR #2079에서 `package:i10n`의 중복 extension이 제거되었습니다.
> 과거에는 두 패키지 모두 `context.i10n`을 제공하여 `ambiguous_extension_member_access` 에러가 발생했습니다.

### 사용 가능한 API

| API | 상태 | 설명 |
|-----|------|------|
| `context.i10n` | ✅ **표준** | 프로젝트 전체에서 사용 |
| `context.translations` | ❌ 사용 금지 | 레거시 코드에만 존재 |

---

## JSON 키 네이밍 규칙

### snake_case 사용 (필수)

```json
// ✅ CORRECT: snake_case 사용
{
  "console": {
    "sample_book": {
      "user_status": {
        "active": "활성",
        "inactive": "비활성"
      }
    }
  }
}

// ❌ WRONG: camelCase 사용 금지
{
  "console": {
    "sampleBook": {  // 잘못됨!
      "userStatus": {  // 잘못됨!
        "active": "활성"
      }
    }
  }
}
```

### 키 네이밍 패턴

| 패턴 | 예시 | 설명 |
|------|------|------|
| 기능명 | `sample_book`, `sales_analysis` | 기능 모듈명 |
| 동작 | `create`, `update`, `delete` | CRUD 동작 |
| 상태 | `loading`, `error`, `success` | 상태 메시지 |
| 에러 | `invalid_date_range`, `not_found` | 에러 메시지 |

---

## JSON 파일 구조

### 파일 위치

```
shared/i10n/lib/src/json/
├── ko.i18n.json      # 한국어 (기준)
├── en.i18n.json      # 영어
├── ja.i18n.json      # 일본어
├── zh-Hans.i18n.json # 중국어 간체
├── de.i18n.json      # 독일어
├── fr.i18n.json      # 프랑스어
├── es.i18n.json      # 스페인어
├── it.i18n.json      # 이탈리아어
├── pt.i18n.json      # 포르투갈어
├── ru.i18n.json      # 러시아어
└── ar.i18n.json      # 아랍어
```

### 계층 구조

```json
{
  "common": {
    "save": "저장",
    "cancel": "취소",
    "confirm": "확인"
  },
  "console": {
    "sample_book": { ... },
    "sales_analysis": {
      "period": {
        "all": "전체",
        "today": "오늘",
        "yesterday": "어제",
        "last7_days": "최근 7일",
        "this_week": "이번 주",
        "this_month": "이번 달",
        "last_month": "지난 달",
        "custom": "기간 선택",
        "invalid_date_range": "종료일은 시작일 이후여야 합니다"
      }
    }
  },
  "main": { ... }
}
```

---

## 번역 코드 생성

### 번역 파일 수정 후

```bash
# 번역 코드 재생성
cd shared/i10n && dart run slang

# 또는 melos 명령어
melos run generate:locale
```

### 생성되는 파일

```
shared/i10n/lib/src/translations/
├── translations.g.dart         # 기본 인터페이스
├── translations_ko.g.dart      # 한국어
├── translations_en.g.dart      # 영어
└── ... (각 언어별 파일)
```

---

## 사용 예시

### 단순 텍스트

```dart
Text(context.i10n.common.save)
Text(context.i10n.console.sales_analysis.period.all)
```

### 파라미터가 있는 번역

```dart
// JSON 정의 ($ 형식 사용)
// "greeting": "안녕하세요, $name님!"

// Dart 사용
Text(context.i10n.common.greeting(name: user.name))
```

### 복수형

```dart
// JSON 정의 ($ 형식 사용)
// "items": {
//   "one": "$count개 항목",
//   "other": "$count개 항목들"
// }

// Dart 사용
Text(context.i10n.common.items(count: items.length))
```

---

## 주의사항

1. **새 키 추가 시**: 모든 언어 JSON 파일에 추가해야 함
2. **키 네이밍**: 반드시 snake_case 사용
3. **코드 생성**: JSON 수정 후 `dart run slang` 필수
4. **API 선택**: `context.i10n`만 사용 (translations 금지)
5. **파라미터 형식**: `$param` 형식 사용 (중괄호 `{param}` 금지)
   - ✅ `"greeting": "안녕하세요, $name님!"`
   - ❌ `"greeting": "안녕하세요, {name}님!"` (오류 발생)
6. **파라미터명 일관성**: 모든 언어 파일에서 동일한 파라미터명 사용
   - 예: `$maxSizeMB` (모든 언어에서 동일해야 함)

---

## 관련 문서

- [CLAUDE.md](../../CLAUDE.md) - 프로젝트 전체 가이드
- [슬랭 공식 문서](https://pub.dev/packages/slang)

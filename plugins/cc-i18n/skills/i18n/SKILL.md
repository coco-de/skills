---
name: i18n
description: slang 기반 국제화(i18n) 번역 관리. 다국어 텍스트 추가, 복수형 처리, 파라미터화, 번역 코드 생성 등 국제화 작업 시 사용.
---

# i18n (Internationalization)

slang 기반 Flutter 국제화를 위한 마스터 스킬입니다. 번역 키 관리, 코드 생성, GPT 자동 번역을 지원합니다.

## Scope and Capabilities

### 지원 기능

| 기능 | 설명 | 명령어 |
|------|------|--------|
| 번역 추가 | 새 번역 키 생성 | `/i18n add` |
| 번역 수정 | 기존 번역 업데이트 | `/i18n update` |
| 누락 확인 | 미번역 키 검색 | `/i18n check` |
| 코드 생성 | .g.dart 파일 생성 | `melos run generate:locale` |
| GPT 번역 | 자동 영어 번역 | `melos run generate:locale:gpt` |

### 파일 구조

```
shared/i10n/lib/
├── translations/
│   ├── strings.i18n.yaml      # 기본 언어 (한국어)
│   └── strings_en.i18n.yaml   # 영어 번역
└── src/
    └── translations/
        └── translations.g.dart # 자동 생성 코드
```

## Quick Start

### 1. 번역 사용법

```dart
// BuildContext 확장으로 접근
Text(context.t.common.appName)
Text(context.t.auth.login)
```

### 2. 파라미터 사용

```dart
Text(context.t.user.greeting(name: user.name))
Text(context.t.user.points(count: points.toString()))
```

### 3. 복수형 사용

```dart
Text(context.t.items.count(n: itemCount))
// n=0: "항목 없음"
// n=1: "항목 1개"
// n>1: "항목 n개"
```

## Workflow

### 번역 추가 플로우

```
1. strings.i18n.yaml에 한국어 키 추가
2. strings_en.i18n.yaml에 영어 번역 추가 (또는 GPT 자동 번역)
3. melos run generate:locale 실행
4. context.t.{path} 로 코드에서 사용
```

### 명령어

```bash
# 번역 코드 생성
melos run generate:locale

# GPT 자동 번역 (영어)
melos run generate:locale:gpt

# 누락된 번역 분석
dart run slang analyze
```

## 핵심 규칙

### Naming Convention

- 중첩 구조 권장: `user.profile.title`
- camelCase 사용
- 의미 있는 키 이름

### 필수 규칙

- 모든 UI 텍스트 → 번역 키 사용
- 하드코딩된 문자열 금지
- 숫자 관련 텍스트 → 복수형 필수

### 코드 생성

- 번역 파일 수정 후 → `melos run generate:locale` 필수
- 생성된 `.g.dart` 파일 직접 수정 금지

## Additional Resources

- [REFERENCE.md](REFERENCE.md) - 상세 API 및 문법 레퍼런스
- [TEMPLATES.md](TEMPLATES.md) - 번역 패턴 템플릿

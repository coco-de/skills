---
name: code-review-suppression
description: "코드 리뷰 시 false positive를 억제하는 프로젝트별 규칙"
---

# Code Review Suppression List

> gstack 패턴 참고: 리뷰 체크리스트에 "이건 지적하지 마라"를 명시하여 alert fatigue를 줄인다.

## 기본 Suppressions (Dart 풀스택)

### 코드 생성 관련
- **Freezed generated 코드** (`*.freezed.dart`, `*.g.dart`): 자동 생성 파일은 리뷰 대상에서 제외
- **Serverpod generated 코드** (`*_server/lib/src/generated/`): 서버 자동 생성 코드 제외
- **slang i18n 생성 파일** (`*_gen/*.g.dart`): 번역 자동 생성 제외

### 프레임워크 패턴 관련
- **BLoC boilerplate**: sealed class Event/State 정의는 boilerplate로 지적하지 않음
- **`context.read<>()`**: BLoC 이벤트 디스패치에서의 사용은 anti-pattern이 아님 (build 내부에서만 문제)
- **Freezed copyWith**: `.copyWith()` 체인이 길어도 리팩토링 제안하지 않음
- **sealed class 패턴**: when/map 메서드의 긴 case 목록은 정상 패턴

### CoUI 컴포넌트 관련
- **Co prefix 없음**: CoUI 위젯은 `Button`, `Card` 등 prefix 없이 사용 (Flutter Material과 다름)
- **ButtonSize.medium 없음**: `ButtonSize.normal`이 기본값, medium 사용 제안하지 않음
- **Dot shorthand**: Dart 3.10+ `.start`, `.all()` 등 축약 문법은 정상

### 프로젝트 구조 관련
- **melos 모노레포 import**: 패키지 간 상대 경로 import는 melos 구조상 정상
- **feature 모듈 내 barrel export**: `feature.dart` barrel file은 convention
- **GetIt DI 등록**: `getIt.registerFactory/Singleton` 패턴 지적 불필요

### 스타일/컨벤션 관련
- **가독성 위한 중복 코드**: 명시적으로 의미 전달을 위한 반복 코드는 DRY 위반으로 지적하지 않음
- **const 누락 (위젯 내부)**: `const` 추가가 가독성을 해치는 경우 강제하지 않음
- **한국어 주석/문자열**: 한국어 사용은 프로젝트 표준

## 프로젝트별 커스텀 Suppressions

사용자 프로젝트 루트에 `.code-review-suppress.md`를 생성하면 추가 suppression을 정의할 수 있습니다:

```markdown
# Project-Specific Suppressions

- **Legacy API 호출**: `api/v1/` 경로의 deprecated API 사용은 마이그레이션 중이므로 지적하지 않음
- **TODO 주석**: 현재 스프린트에서 해결 예정인 TODO는 무시
```

## Suppression 적용 방법

1. 리뷰 실행 시 이 파일과 프로젝트의 `.code-review-suppress.md`를 자동 로딩
2. 각 지적 항목을 suppression 목록과 대조
3. 매칭되는 항목은 리뷰 결과에서 제외
4. 제외된 항목 수를 하단에 표시: "N개 항목이 suppression으로 제외됨"

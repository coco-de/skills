# CoUI Flutter Quick Reference

> 💡 **전체 가이드는 [CLAUDE.md](../../CLAUDE.md)를 참조하세요.**
> 이 문서는 CoUI 컴포넌트 사용 시 빠른 참조를 위한 요약본입니다.

## Typography API 가이드

### 프로젝트 표준: `context.textStyles`

이 프로젝트에서는 **`context.textStyles`**를 사용합니다 (22개 파일에서 사용 중).

```dart
// ✅ 프로젝트 표준: textStyles 사용
style: context.textStyles.lgSemibold
style: context.textStyles.smSemibold
style: context.textStyles.sm.merge(context.textStyles.medium)

// ✅ copyWith 조합
style: context.textStyles.lgSemibold.copyWith(
  color: context.appColors.neutral5,
)
```

### API 선택

| API | 상태 |
|-----|------|
| `context.textStyles` | ✅ **프로젝트 표준** (22개 파일 사용) |
| `context.typography` | ❌ 사용 금지 (0건) |

### 조합 Getters (자주 사용)

| Getter | 구성 | 예시 |
|--------|------|------|
| `lgSemibold` | 16px + 600 weight | 제목, 강조 텍스트 |
| `smSemibold` | 12px + 600 weight | 라벨, 배지 |
| `baseMedium` | 14px + 500 weight | 본문 강조 |
| `sm` | 12px | 보조 텍스트 |
| `xs` | 10px | 캡션 |

### Font Size 전체 목록

| Getter | Size | 용도 |
|--------|------|------|
| `xs` | 10px | 캡션, 주석 |
| `sm` | 12px | 보조 텍스트, 라벨 |
| `base` | 14px | 기본 본문 |
| `lg` | 16px | 강조 본문, 소제목 |
| `xl` | 20px | 제목 |
| `x2l` | 24px | 큰 제목 |
| `x3l` | 30px | 페이지 제목 |
| `x4l` | 36px | 대형 제목 |
| `x5l` | 48px | Hero 텍스트 |

---

## TextField features 파라미터

> ⚠️ **deprecated**: `leading`, `trailing` 파라미터는 deprecated되었습니다.

```dart
// ✅ 새로운 API: features 파라미터
TextField(
  controller: controller,
  placeholder: const Text('입력해주세요'),
  filled: true,  // 배경색 적용 (base200)
  features: [
    InputFeature.leading(const Icon(Icons.search, size: 20)),
    InputFeature.trailing(const Icon(Icons.clear, size: 18)),
  ],
  onChanged: (value) => ...,
)

// ❌ deprecated: leading/trailing 파라미터
TextField(
  leading: Icon(Icons.search),   // deprecated
  trailing: Icon(Icons.clear),   // deprecated
)
```

### TextField 주요 속성

| 속성 | 타입 | 설명 |
|------|------|------|
| `filled` | bool | `true`면 배경색(base200) 적용 |
| `border` | Border | 테두리 설정 (`Border.all(color: context.colorScheme.base300)`) |
| `borderRadius` | BorderRadius | 테두리 반경 |
| `features` | List<InputFeature> | leading, trailing, clear 등 |

---

## ButtonSize & ButtonDensity

### ButtonSize 옵션

> ⚠️ **주의**: `ButtonSize.medium`은 **존재하지 않습니다**!

| 상수 | 스케일 | 용도 |
|------|--------|------|
| `ButtonSize.xSmall` | 0.5x | 매우 작은 버튼 |
| `ButtonSize.small` | 0.75x | 작은 버튼 |
| `ButtonSize.normal` | 1.0x | **기본값** |
| `ButtonSize.large` | 2.0x | 큰 버튼 |
| `ButtonSize.xLarge` | 3.0x | 매우 큰 버튼 |

```dart
// ✅ CORRECT: 존재하는 크기 사용
ButtonStyle.primary(size: .normal)
ButtonStyle.primary(size: .small)

// ❌ WRONG: medium 없음 (컴파일 에러)
ButtonStyle.primary(size: .medium)  // 에러!
```

### ButtonDensity 옵션

| 상수 | 용도 |
|------|------|
| `ButtonDensity.normal` | 기본 밀도 |
| `ButtonDensity.comfortable` | 여유로운 패딩 |
| `ButtonDensity.dense` | **컴팩트한 버튼** (테이블 내 버튼) |
| `ButtonDensity.compact` | 최소 패딩 |
| `ButtonDensity.icon` | 아이콘 전용 |
| `ButtonDensity.iconComfortable` | 아이콘 + 여유 패딩 |
| `ButtonDensity.iconDense` | 아이콘 + 컴팩트 |

```dart
// 테이블 내 컴팩트한 버튼
Button.outline(
  style: const ButtonStyle.outline(density: .dense),
  onPressed: handleTap,
  child: const Text('복사'),
)
```

---

## Badge 컴포넌트

상태 표시용 배지 컴포넌트입니다. ButtonStyle과 함께 사용합니다.

### Badge 종류

| 컴포넌트 | 용도 | 기본 색상 |
|----------|------|----------|
| `PrimaryBadge` | 긍정적 상태 (판매중, 활성 등) | primary |
| `DestructiveBadge` | 부정적 상태 (중지, 삭제 등) | destructive (red) |

### 사용 예시

```dart
// ✅ 기본 사용
const PrimaryBadge(child: Text('판매중'))
const DestructiveBadge(child: Text('판매 중지'))

// ✅ density 조절로 컴팩트하게
const PrimaryBadge(
  style: ButtonStyle.primary(density: .dense),
  child: Text('판매중'),
)

const DestructiveBadge(
  style: ButtonStyle.destructive(density: .dense),
  child: Text('판매 중지'),
)

// ✅ 조건부 배지
child: book.isActive
    ? const PrimaryBadge(
        style: ButtonStyle.primary(density: .dense),
        child: Text('판매중'),
      )
    : const DestructiveBadge(
        style: ButtonStyle.destructive(density: .dense),
        child: Text('판매 중지'),
      ),
```

---

## Gap & Insets 상수

### Gap 사용법
```dart
const Gap.s1()        // 4px
const Gap.s2()        // 8px
const Gap.s4()        // 16px
Gap(Insets.small)     // 8px
Gap(Insets.medium)    // 16px
Gap(Insets.large)     // 24px
```

### Insets 상수 표

| 상수 | 값 | 용도 |
|------|-----|------|
| `Insets.xSmall` | 4px | 아이콘 간격 |
| `Insets.small` | 8px | 요소 간격 |
| `Insets.medium` | 16px | 섹션 패딩 |
| `Insets.large` | 24px | 카드 패딩 |
| `Insets.xLarge` | 32px | 페이지 마진 |

---

## 로딩/스켈레톤 패턴

```dart
// 스켈레톤 로딩 (전체 위젯)
widget.skeletonizer(enabled: state.isLoading)

// 조건부 로딩 (스피너)
widget.loadingOr(
  isLoading: state.isLoading,
  loadingWidget: const CircularProgressIndicator(),
)

// 빈 상태 처리
listWidget.emptyOrWhen(
  condition: () => list.isEmpty,
  emptyWidget: const EmptyStateWidget(),
)
```

---

## 완전한 페이지 예시

```dart
class MyPage extends HookWidget {
  const MyPage({super.key});

  @override
  Widget build(BuildContext context) {
    final appColors = context.appColors;

    return BlocProvider(
      create: (_) => getIt<MyBloc>(),
      child: BlocBuilder<MyBloc, MyState>(
        builder: (context, state) {
          return Scaffold(
            headers: [
              AppBar(
                title: Text(
                  '페이지 제목',
                  style: context.textStyles.lgSemibold.copyWith(
                    color: appColors.neutral5,
                  ),
                ),
              ),
            ],
            child: Padding(
              padding: const .symmetric(horizontal: Insets.medium),
              child: Column(
                crossAxisAlignment: .start,
                children: [
                  const Gap(Insets.medium),
                  TextField(
                    placeholder: const Text('이름을 입력하세요'),
                    features: const [
                      InputFeature.leading(Icon(Icons.person, size: 20)),
                    ],
                    onChanged: (value) => context.read<MyBloc>().add(
                      MyEvent.nameChanged(value),
                    ),
                  ),
                  const Gap(Insets.medium),
                  Button.primary(
                    expanded: true,
                    enabled: state.isValid,
                    onPressed: () => context.read<MyBloc>().add(
                      const MyEvent.submitted(),
                    ),
                    child: const Text('저장'),
                  ),
                ],
              ),
            ).skeletonizer(enabled: state.isLoading),
          );
        },
      ),
    );
  }
}
```

---

## 색상 체계 (Console UI)

### AppColors neutral 시리즈

| 색상 | HEX | 용도 |
|------|-----|------|
| `neutral100` | #FFFFFF | 흰색 배경 |
| `neutral95` | #F9FAFB | 헤더/섹션 배경 (본문과 구분) |
| `neutral85` | #F4F5F6 | 밝은 회색 |
| `neutral80` | #ECEEEF | 기본 테두리 |
| `neutral70` | #B4B8C4 | **진한 테두리** (선명한 구분선) |
| `neutral60` | #8F929A | 비활성 텍스트 |
| `neutral30` | - | 본문 텍스트 |

```dart
// 헤더 배경 (본문과 구분)
color: context.appColors.neutral95,

// 진한 테두리 (선명하게)
border: Border(
  right: .new(color: context.appColors.neutral70),
),

// 기본 테두리
border: Border.all(color: context.appColors.neutral80),
```

### ColorScheme base 시리즈

CoUI의 색상 체계입니다.

| 색상 | 용도 |
|------|------|
| `base100` | 가장 밝은 배경 |
| `base200` | 중간 배경 (filled TextField) |
| `base300` | **가장 진한 배경/테두리** |

```dart
// TextField 배경
TextField(
  filled: true,  // base200 배경
  border: Border.all(color: context.colorScheme.base300),
)

// 필터 다이얼로그 테두리
OutlinedContainer(
  backgroundColor: theme.colorScheme.base100,
  borderColor: theme.colorScheme.base300,  // 진한 테두리
)
```

---

## 참조 문서

다음 내용은 **[CLAUDE.md](../../CLAUDE.md)**를 참조하세요:

- 색상 규칙 (AppColors, context.appColors)
- Dot Shorthand 규칙 (Dart 3.10+)
- Button/IconButton 사용법
- BLoC Event/State 패턴 (sealed class)
- BLoC async 핸들러 (isClosed 체크)
- Context Extensions 전체 목록

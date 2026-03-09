---
name: bloc
description: "BLoC/Cubit 상태 관리 패턴 + Freezed 구현"
invoke: /bloc:create
aliases: ["/state:bloc", "/flutter:bloc"]
category: petmedi-development
complexity: moderate
mcp-servers: [serena, context7]
---

# /bloc:create

BLoC/Cubit 상태 관리 컴포넌트를 생성합니다.

> 📚 **상세 패턴**: [BLoC 패턴](../references/patterns/bloc-patterns.md)

---

## 사용법

```bash
/bloc:create {feature_name} {bloc_name} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `feature_name` | ✅ | Feature 모듈명 | `home`, `auth`, `store` |
| `bloc_name` | ✅ | BLoC 이름 | `Home`, `Login`, `Cart` |
| `--type` | ❌ | 타입 | `bloc`, `cubit` (기본: `bloc`) |
| `--location` | ❌ | 위치 | `application`, `common`, `console` |
| `--usecases` | ❌ | 연결할 UseCase | `GetUser,UpdateUser` |

---

## 생성 파일

```
feature/{location}/{feature_name}/lib/src/presentation/bloc/
├── {bloc_name}_bloc.dart      # BLoC 구현
├── {bloc_name}_event.dart     # Event 정의 (sealed class)
└── {bloc_name}_state.dart     # State 정의 (Freezed)
```

---

## 핵심 규칙

- **Event**: `sealed class` + private `_` prefix 클래스
- **State**: Freezed union type (`initial`, `loading`, `loaded`, `error`)
- **UseCase**: `const UseCase()` 직접 생성 (DI 미사용)
- **안전성**: `await` 후 반드시 `if (isClosed) return;` 체크

---

## Examples

```bash
# Home 피드 BLoC
/bloc:create home Home --usecases GetFeed,RefreshFeed

# Auth 로그인 Cubit
/bloc:create auth Login --type cubit --location common

# 관리자 대시보드 BLoC
/bloc:create dashboard Dashboard --location console
```

---

## MCP 연동

| MCP 서버 | 용도 |
|----------|------|
| Context7 | flutter_bloc 공식 문서 |
| Serena | 기존 BLoC 패턴 분석 |

---

## 관련 문서

- [BLoC 패턴 상세](../references/patterns/bloc-patterns.md)
- [UseCase 패턴](../references/patterns/usecase-patterns.md)
- [의존성 그래프](../references/DEPENDENCY_GRAPH.md)

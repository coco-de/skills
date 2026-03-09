---
name: inspector
description: "Flutter 앱 런타임 디버깅 마스터 인스펙터"
invoke: /inspector
aliases: ["/debug", "/inspect", "/flutter:debug"]
category: petmedi-development
complexity: moderate
mcp-servers: [flutter-inspector, serena]
---

# /inspector

> **Context Framework Note**: Flutter 앱 런타임 디버깅 시 활성화됩니다.

## Triggers

- 앱 디버깅 요청 시
- 런타임 상태 확인 시
- MCP toolkit 기반 검사 시

## Context Trigger Pattern

```
/inspector {area} [--options]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `area` | ❌ | 검사 영역 | `nav`, `bloc`, `auth`, `network`, `log`, `ui`, `config`, `form`, `image` |
| `--verbose` | ❌ | 상세 출력 | |
| `--all` | ❌ | 전체 영역 검사 | |

## Sub-Inspectors

### 9개 전문 인스펙터

| 인스펙터 | 역할 | 주요 도구 |
|---------|------|----------|
| `/inspector/nav` | GoRouter 네비게이션 | nav_get_current_route, nav_get_history |
| `/inspector/bloc` | BLoC 상태 추적 | bloc_list_active, bloc_get_state |
| `/inspector/auth` | 인증 상태 확인 | auth_get_status, auth_get_user |
| `/inspector/network` | HTTP 요청 로깅 | network_get_logs, network_get_errors |
| `/inspector/log` | 앱 로그 관리 | log_get_recent, log_get_errors |
| `/inspector/ui` | 위젯 트리 검사 | ui_get_widget_tree, ui_find_overflow |
| `/inspector/config` | 설정/피처 플래그 | config_get_all, config_get_feature_flags |
| `/inspector/form` | 폼 유효성 디버깅 | form_get_state, form_get_errors |
| `/inspector/image` | 이미지 캐시/메모리 | img_get_cache_stats, img_analyze_warnings |

## Prerequisites

### Flutter 앱 실행 조건

```bash
# 디버그 모드로 실행 (VM Service 활성화)
flutter run --debug \
  --enable-vm-service \
  --host-vmservice-port=8182 \
  --dds-port=8181 \
  --disable-service-auth-codes
```

### MCP Toolkit 통합

```dart
// main.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  MCPToolkitBinding.instance
    ..initialize()
    ..initializeFlutterToolkit();

  if (kDebugMode) {
    // 커스텀 도구 등록
    registerDebugTools();
  }

  runApp(const MyApp());
}
```

## Diagnostic Workflow

```
┌─────────────────────────────────────────┐
│  1. 앱 연결 확인                          │
├─────────────────────────────────────────┤
│  • hot_reload_flutter 테스트             │
│  • listClientToolsAndResources 확인      │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  2. 문제 영역 특정                        │
├─────────────────────────────────────────┤
│  • 화면 전환 문제 → @flutter-inspector-nav │
│  • 상태 문제 → @flutter-inspector-bloc    │
│  • 로그인 문제 → @flutter-inspector-auth  │
│  • API 문제 → @flutter-inspector-network │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  3. 상세 분석                            │
├─────────────────────────────────────────┤
│  • 전문 인스펙터 도구 실행                 │
│  • 로그 및 상태 추적                      │
│  • 문제점 식별                           │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│  4. 해결 및 검증                          │
├─────────────────────────────────────────┤
│  • 코드 수정 제안                        │
│  • hot_reload_flutter로 적용             │
│  • 재검사로 확인                         │
└─────────────────────────────────────────┘
```

## Quick Diagnostics

### 화면 전환 문제
```
1. /inspector/nav → 현재 라우트 확인
2. nav_get_history → 전환 히스토리 추적
3. nav_get_params → 전달된 파라미터 검증
```

### 상태 관리 문제
```
1. /inspector/bloc → 활성 BLoC 목록
2. bloc_get_state → 현재 상태 확인
3. bloc_get_events → 이벤트 히스토리
```

### API 오류
```
1. /inspector/network → 요청/응답 로그
2. network_get_errors → 실패 요청 확인
3. /inspector/auth → 토큰 상태 확인
```

### UI 레이아웃 문제
```
1. /inspector/ui → 위젯 트리 확인
2. ui_find_overflow → 오버플로우 검색
3. ui_get_screen_info → 화면 정보
```

### 성능 문제
```
1. /inspector/image → 이미지 캐시 분석
2. img_analyze_warnings → 메모리 경고
3. /inspector/log → 성능 관련 로그
```

## MCP Integration

| 단계 | MCP 서버 | 용도 |
|------|----------|------|
| 앱 연결 | flutter-inspector | VM Service 연결 |
| 도구 조회 | flutter-inspector | listClientToolsAndResources |
| 도구 실행 | flutter-inspector | runClientTool |
| 코드 분석 | serena | 관련 코드 검색 |

## Examples

### 전체 상태 점검

```
/inspector --all
```

### 네비게이션 디버깅

```
/inspector nav
```

### BLoC 상태 확인

```
/inspector bloc --verbose
```

### 네트워크 오류 분석

```
/inspector network
```

## 참조

- 상세 구현: `.claude/agents/flutter-inspector.md`
- Sub-inspectors: `.claude/commands/inspector/`
- MCP toolkit: `package/mcp_toolkit/`

---
name: flutter-inspector-bloc
description: BLoC 상태 디버깅 전문가. 상태 추적, 이벤트 히스토리 검사 시 사용
tools: Read, Glob, Grep
model: haiku
skills: flutter-inspector
---

# Flutter Inspector - BLoC Agent

BLoC/Cubit 상태를 런타임에서 추적하고 디버깅하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-bloc` 또는 다음 키워드 감지 시 자동 활성화:
- BLoC 상태, 상태 변화
- 이벤트 추적, 상태 히스토리
- Cubit, emit

## MCP 도구

### bloc_list_active
현재 활성화된 모든 BLoC/Cubit 목록을 반환합니다.

```json
{
  "name": "bloc_list_active",
  "description": "활성 BLoC/Cubit 목록",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "blocs": [
    {
      "type": "AuthBloc",
      "state": "Authenticated",
      "stateType": "AuthState.authenticated",
      "instanceId": "AuthBloc#12345"
    },
    {
      "type": "HomeBloc",
      "state": "Loaded",
      "stateType": "HomeState.loaded",
      "instanceId": "HomeBloc#67890"
    },
    {
      "type": "ThemeCubit",
      "state": "light",
      "stateType": "ThemeMode",
      "instanceId": "ThemeCubit#11111"
    }
  ],
  "count": 3
}
```

### bloc_get_state
특정 BLoC의 현재 상태를 상세하게 반환합니다.

```json
{
  "name": "bloc_get_state",
  "description": "BLoC 상태 상세 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "blocType": {
        "type": "string",
        "description": "BLoC 타입명 (예: AuthBloc)"
      },
      "instanceId": {
        "type": "string",
        "description": "인스턴스 ID (선택)"
      }
    },
    "required": ["blocType"]
  }
}
```

**응답 예시**:
```json
{
  "blocType": "HomeBloc",
  "state": {
    "status": "loaded",
    "posts": [
      {"id": 1, "title": "첫 번째 글"},
      {"id": 2, "title": "두 번째 글"}
    ],
    "hasMore": true,
    "page": 1,
    "error": null
  },
  "stateType": "HomeState",
  "lastUpdated": "2024-01-01T10:05:00Z"
}
```

### bloc_get_history
BLoC의 상태 변화 히스토리를 반환합니다.

```json
{
  "name": "bloc_get_history",
  "description": "상태 변화 히스토리",
  "inputSchema": {
    "type": "object",
    "properties": {
      "blocType": {
        "type": "string",
        "description": "BLoC 타입명"
      },
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 20
      }
    },
    "required": ["blocType"]
  }
}
```

**응답 예시**:
```json
{
  "blocType": "AuthBloc",
  "history": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "fromState": "AuthState.initial",
      "toState": "AuthState.loading",
      "trigger": "AuthEvent.login"
    },
    {
      "timestamp": "2024-01-01T10:00:02Z",
      "fromState": "AuthState.loading",
      "toState": "AuthState.authenticated",
      "trigger": "AuthEvent.login"
    }
  ],
  "totalTransitions": 2
}
```

### bloc_get_events
BLoC에 발생한 이벤트 로그를 반환합니다.

```json
{
  "name": "bloc_get_events",
  "description": "이벤트 로그 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "blocType": {
        "type": "string",
        "description": "BLoC 타입명"
      },
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 50
      }
    },
    "required": ["blocType"]
  }
}
```

**응답 예시**:
```json
{
  "blocType": "HomeBloc",
  "events": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "event": "HomeEvent.load",
      "params": {},
      "processed": true
    },
    {
      "timestamp": "2024-01-01T10:00:05Z",
      "event": "HomeEvent.refresh",
      "params": {},
      "processed": true
    },
    {
      "timestamp": "2024-01-01T10:00:10Z",
      "event": "HomeEvent.loadMore",
      "params": {"page": 2},
      "processed": false,
      "error": "Network timeout"
    }
  ]
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_bloc_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

class MCPBlocObserver extends BlocObserver {
  final _history = <String, List<Map<String, dynamic>>>{};
  final _events = <String, List<Map<String, dynamic>>>{};
  final _activeBlocs = <String, BlocBase>{};

  static final instance = MCPBlocObserver._();
  MCPBlocObserver._();

  @override
  void onCreate(BlocBase bloc) {
    _activeBlocs[bloc.runtimeType.toString()] = bloc;
    super.onCreate(bloc);
  }

  @override
  void onClose(BlocBase bloc) {
    _activeBlocs.remove(bloc.runtimeType.toString());
    super.onClose(bloc);
  }

  @override
  void onTransition(Bloc bloc, Transition transition) {
    final type = bloc.runtimeType.toString();
    _history[type] ??= [];
    _history[type]!.add({
      'timestamp': DateTime.now().toIso8601String(),
      'fromState': transition.currentState.runtimeType.toString(),
      'toState': transition.nextState.runtimeType.toString(),
      'trigger': transition.event.runtimeType.toString(),
    });
    super.onTransition(bloc, transition);
  }

  @override
  void onEvent(Bloc bloc, Object? event) {
    final type = bloc.runtimeType.toString();
    _events[type] ??= [];
    _events[type]!.add({
      'timestamp': DateTime.now().toIso8601String(),
      'event': event.runtimeType.toString(),
      'processed': true,
    });
    super.onEvent(bloc, event);
  }

  Map<String, dynamic> getActiveBlocs() {
    return {
      'blocs': _activeBlocs.entries.map((e) => {
        'type': e.key,
        'state': e.value.state.toString(),
        'stateType': e.value.state.runtimeType.toString(),
      }).toList(),
      'count': _activeBlocs.length,
    };
  }

  Map<String, dynamic> getState(String blocType) {
    final bloc = _activeBlocs[blocType];
    if (bloc == null) return {'error': 'BLoC not found'};
    return {
      'blocType': blocType,
      'state': bloc.state,
      'stateType': bloc.state.runtimeType.toString(),
    };
  }

  List<Map<String, dynamic>> getHistory(String blocType, int limit) {
    return (_history[blocType] ?? []).take(limit).toList();
  }

  List<Map<String, dynamic>> getEvents(String blocType, int limit) {
    return (_events[blocType] ?? []).take(limit).toList();
  }
}

void registerBlocTools() {
  if (!kDebugMode) return;

  Bloc.observer = MCPBlocObserver.instance;

  addMcpTool(MCPCallEntry.tool(
    handler: (_) => MCPCallResult(
      message: 'Active BLoCs',
      parameters: MCPBlocObserver.instance.getActiveBlocs(),
    ),
    definition: MCPToolDefinition(
      name: 'bloc_list_active',
      description: '활성 BLoC 목록',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final blocType = params['blocType'] as String;
      return MCPCallResult(
        message: 'BLoC State',
        parameters: MCPBlocObserver.instance.getState(blocType),
      );
    },
    definition: MCPToolDefinition(
      name: 'bloc_get_state',
      description: 'BLoC 상태 조회',
      inputSchema: {
        'type': 'object',
        'properties': {
          'blocType': {'type': 'string'},
        },
        'required': ['blocType'],
      },
    ),
  ));

  // bloc_get_history, bloc_get_events도 유사하게 구현
}
```

## 사용 예시

### 활성 BLoC 확인
```
Q: 현재 어떤 BLoC이 활성화되어 있나요?
A: bloc_list_active 실행
   → AuthBloc (Authenticated), HomeBloc (Loaded), ThemeCubit (light)
```

### BLoC 상태 상세 확인
```
Q: HomeBloc의 현재 상태를 자세히 보여줘
A: bloc_get_state blocType="HomeBloc" 실행
   → status: loaded, posts: 10개, hasMore: true, page: 1
```

### 상태 변화 추적
```
Q: AuthBloc이 어떻게 변했는지 히스토리 보여줘
A: bloc_get_history blocType="AuthBloc" 실행
   → initial → loading → authenticated
```

### 이벤트 디버깅
```
Q: HomeBloc에 어떤 이벤트가 발생했나요?
A: bloc_get_events blocType="HomeBloc" 실행
   → load, refresh, loadMore (error: timeout)
```

## 일반적인 문제 진단

### 상태가 업데이트 안 됨
```
1. bloc_list_active로 BLoC 활성화 확인
2. bloc_get_events로 이벤트 발생 확인
3. bloc_get_history로 상태 변화 추적
```

### 잘못된 상태
```
1. bloc_get_state로 현재 상태 확인
2. bloc_get_history로 어디서 잘못됐는지 추적
3. 관련 이벤트 핸들러 코드 검토
```

### 이벤트 무시됨
```
1. bloc_get_events로 이벤트 발생 확인
2. processed: false인 이벤트 찾기
3. 에러 메시지 확인
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@bloc`: BLoC 구현 가이드
- `@flutter-inspector-ui`: 상태와 UI 연결 확인

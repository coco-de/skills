# Flutter Inspector Templates

커스텀 인스펙터 도구 등록 및 디버깅 패턴 템플릿입니다.

## Template A: Custom BLoC Inspector Tool

BLoC 상태를 검사하는 커스텀 도구 등록

### lib/debug/bloc_inspector_tool.dart

```dart
import 'package:flutter/foundation.dart';
import 'package:mcp_toolkit/mcp_toolkit.dart';

/// BLoC 상태 검사 도구 등록
void registerBlocInspectorTools() {
  if (!kDebugMode) return;

  // 모든 BLoC 목록 조회
  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final blocs = _getAllRegisteredBlocs();
      return MCPCallResult(
        message: '${blocs.length}개의 BLoC이 등록되어 있습니다',
        parameters: {
          'blocs': blocs.map((b) => {
            'name': b.runtimeType.toString(),
            'state': b.state.runtimeType.toString(),
          }).toList(),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'bloc_get_all',
      description: '모든 등록된 BLoC/Cubit 인스턴스 반환',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  // 특정 BLoC 상태 조회
  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final blocName = params['blocName'] as String?;
      if (blocName == null) {
        return MCPCallResult(
          message: 'blocName 파라미터가 필요합니다',
          parameters: {'error': true},
        );
      }

      final bloc = _findBlocByName(blocName);
      if (bloc == null) {
        return MCPCallResult(
          message: '$blocName을 찾을 수 없습니다',
          parameters: {'error': true},
        );
      }

      return MCPCallResult(
        message: '$blocName 상태 조회 완료',
        parameters: {
          'blocName': blocName,
          'state': _serializeState(bloc.state),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'bloc_get_state',
      description: '특정 BLoC의 현재 상태 반환',
      inputSchema: {
        'type': 'object',
        'properties': {
          'blocName': {
            'type': 'string',
            'description': 'BLoC 클래스 이름',
          },
        },
        'required': ['blocName'],
      },
    ),
  ));
}
```

---

## Template B: Navigation Inspector Tool

GoRouter 네비게이션 검사 도구

### lib/debug/nav_inspector_tool.dart

```dart
import 'package:flutter/foundation.dart';
import 'package:go_router/go_router.dart';
import 'package:mcp_toolkit/mcp_toolkit.dart';

/// 네비게이션 인스펙터 도구 등록
void registerNavInspectorTools(GoRouter router) {
  if (!kDebugMode) return;

  // 현재 라우트 조회
  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final config = router.routerDelegate.currentConfiguration;
      final location = config.uri.toString();

      return MCPCallResult(
        message: '현재 라우트: $location',
        parameters: {
          'route': {
            'path': location,
            'pathParameters': config.pathParameters,
            'queryParameters': config.uri.queryParameters,
          },
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'nav_get_current_route',
      description: '현재 활성화된 라우트 정보 반환',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  // 딥링크 테스트
  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final uri = params['uri'] as String?;
      if (uri == null) {
        return MCPCallResult(
          message: 'uri 파라미터가 필요합니다',
          parameters: {'error': true},
        );
      }

      try {
        final parsedUri = Uri.parse(uri);
        final match = router.configuration.findMatch(parsedUri);

        return MCPCallResult(
          message: '딥링크 매칭 성공',
          parameters: {
            'uri': uri,
            'matched': match != null,
            'route': match?.route.path,
            'params': match?.pathParameters,
          },
        );
      } catch (e) {
        return MCPCallResult(
          message: '딥링크 파싱 실패: $e',
          parameters: {'error': true},
        );
      }
    },
    definition: MCPToolDefinition(
      name: 'nav_test_deep_link',
      description: '딥링크 URI를 테스트하고 매칭되는 라우트 반환',
      inputSchema: {
        'type': 'object',
        'properties': {
          'uri': {
            'type': 'string',
            'description': '테스트할 딥링크 URI',
          },
        },
        'required': ['uri'],
      },
    ),
  ));
}
```

---

## Template C: Network Inspector Tool

HTTP 요청 로깅 도구

### lib/debug/network_inspector_tool.dart

```dart
import 'package:dio/dio.dart';
import 'package:flutter/foundation.dart';
import 'package:mcp_toolkit/mcp_toolkit.dart';

/// 네트워크 로그 저장소
class NetworkLogStore {
  static final List<Map<String, dynamic>> _logs = [];
  static const int maxLogs = 100;

  static void addLog(Map<String, dynamic> log) {
    _logs.add(log);
    if (_logs.length > maxLogs) {
      _logs.removeAt(0);
    }
  }

  static List<Map<String, dynamic>> getLogs({
    int? limit,
    String? statusFilter,
  }) {
    var result = _logs.reversed.toList();

    if (statusFilter != null) {
      result = result.where((log) {
        final status = log['status'] as int?;
        if (status == null) return false;
        return status.toString().startsWith(statusFilter[0]);
      }).toList();
    }

    if (limit != null) {
      result = result.take(limit).toList();
    }

    return result;
  }

  static void clear() => _logs.clear();
}

/// Dio 인터셉터
class NetworkInspectorInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    options.extra['startTime'] = DateTime.now();
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    _logRequest(response.requestOptions, response.statusCode, response.data);
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    _logRequest(err.requestOptions, err.response?.statusCode, err.message);
    handler.next(err);
  }

  void _logRequest(RequestOptions options, int? status, dynamic data) {
    final startTime = options.extra['startTime'] as DateTime?;
    final duration = startTime != null
        ? DateTime.now().difference(startTime).inMilliseconds
        : null;

    NetworkLogStore.addLog({
      'timestamp': DateTime.now().toIso8601String(),
      'method': options.method,
      'url': options.uri.toString(),
      'status': status,
      'duration': duration,
    });
  }
}

/// 네트워크 인스펙터 도구 등록
void registerNetworkInspectorTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final limit = params['limit'] as int? ?? 50;
      final status = params['status'] as String?;

      final logs = NetworkLogStore.getLogs(limit: limit, statusFilter: status);

      return MCPCallResult(
        message: '${logs.length}개의 네트워크 로그',
        parameters: {'logs': logs},
      );
    },
    definition: MCPToolDefinition(
      name: 'network_get_logs',
      description: 'HTTP 요청/응답 로그 조회',
      inputSchema: {
        'type': 'object',
        'properties': {
          'limit': {'type': 'integer', 'description': '최대 개수'},
          'status': {'type': 'string', 'description': '상태 필터 (2xx, 4xx, 5xx)'},
        },
      },
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      NetworkLogStore.clear();
      return MCPCallResult(
        message: '네트워크 로그가 초기화되었습니다',
        parameters: {'success': true},
      );
    },
    definition: MCPToolDefinition(
      name: 'network_clear_logs',
      description: '네트워크 로그 초기화',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));
}
```

---

## Template D: Image Cache Inspector Tool

이미지 캐시 분석 도구

### lib/debug/image_inspector_tool.dart

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/painting.dart';
import 'package:mcp_toolkit/mcp_toolkit.dart';

/// 이미지 캐시 인스펙터 도구 등록
void registerImageInspectorTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final cache = PaintingBinding.instance.imageCache;

      return MCPCallResult(
        message: '이미지 캐시 통계',
        parameters: {
          'cache': {
            'currentSize': cache.currentSize,
            'currentSizeFormatted': _formatBytes(cache.currentSize),
            'maximumSize': cache.maximumSize,
            'maximumSizeFormatted': _formatBytes(cache.maximumSize),
            'usagePercent': (cache.currentSize / cache.maximumSize * 100).round(),
            'liveImageCount': cache.liveImageCount,
            'pendingImageCount': cache.pendingImageCount,
          },
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'img_get_cache_stats',
      description: '이미지 캐시 통계 반환',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final type = params['type'] as String? ?? 'all';
      final cache = PaintingBinding.instance.imageCache;

      switch (type) {
        case 'all':
          cache.clear();
          break;
        case 'live':
          cache.clearLiveImages();
          break;
      }

      return MCPCallResult(
        message: '이미지 캐시가 정리되었습니다 (type: $type)',
        parameters: {'success': true},
      );
    },
    definition: MCPToolDefinition(
      name: 'img_clear_cache',
      description: '이미지 캐시 정리',
      inputSchema: {
        'type': 'object',
        'properties': {
          'type': {
            'type': 'string',
            'enum': ['all', 'live'],
            'description': '정리 유형',
          },
        },
      },
    ),
  ));
}

String _formatBytes(int bytes) {
  if (bytes < 1024) return '$bytes B';
  if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
  return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
}
```

---

## Template E: Form Inspector Tool

폼 상태 검사 도구

### lib/debug/form_inspector_tool.dart

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:mcp_toolkit/mcp_toolkit.dart';

/// 폼 레지스트리 (앱에서 폼 등록 필요)
class FormRegistry {
  static final Map<String, GlobalKey<FormState>> _forms = {};

  static void register(String key, GlobalKey<FormState> formKey) {
    _forms[key] = formKey;
  }

  static void unregister(String key) {
    _forms.remove(key);
  }

  static GlobalKey<FormState>? get(String key) => _forms[key];

  static Map<String, GlobalKey<FormState>> get all => _forms;
}

/// 폼 인스펙터 도구 등록
void registerFormInspectorTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final forms = FormRegistry.all;

      return MCPCallResult(
        message: '${forms.length}개의 폼이 등록되어 있습니다',
        parameters: {
          'forms': forms.entries.map((e) {
            final state = e.value.currentState;
            return {
              'key': e.key,
              'isValid': state?.validate() ?? false,
            };
          }).toList(),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'form_list',
      description: '등록된 모든 폼 목록 반환',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final formKey = params['formKey'] as String?;
      if (formKey == null) {
        return MCPCallResult(
          message: 'formKey 파라미터가 필요합니다',
          parameters: {'error': true},
        );
      }

      final form = FormRegistry.get(formKey);
      if (form == null) {
        return MCPCallResult(
          message: '$formKey 폼을 찾을 수 없습니다',
          parameters: {'error': true},
        );
      }

      final isValid = form.currentState?.validate() ?? false;

      return MCPCallResult(
        message: '$formKey 유효성 검사 완료',
        parameters: {
          'formKey': formKey,
          'isValid': isValid,
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'form_validate',
      description: '폼 유효성 검사 실행',
      inputSchema: {
        'type': 'object',
        'properties': {
          'formKey': {
            'type': 'string',
            'description': '폼 키',
          },
        },
        'required': ['formKey'],
      },
    ),
  ));
}
```

---

## Template F: App Initialization

모든 인스펙터 도구 초기화

### lib/main.dart

```dart
import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:mcp_toolkit/mcp_toolkit.dart';

import 'debug/bloc_inspector_tool.dart';
import 'debug/form_inspector_tool.dart';
import 'debug/image_inspector_tool.dart';
import 'debug/nav_inspector_tool.dart';
import 'debug/network_inspector_tool.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();

  // MCP Toolkit 초기화
  MCPToolkitBinding.instance
    ..initialize()
    ..initializeFlutterToolkit();

  // 디버그 모드에서만 인스펙터 도구 등록
  if (kDebugMode) {
    registerBlocInspectorTools();
    registerNavInspectorTools(appRouter);
    registerNetworkInspectorTools();
    registerImageInspectorTools();
    registerFormInspectorTools();

    debugPrint('🔍 Flutter Inspector tools registered');
  }

  runApp(const MyApp());
}
```

---

## Debugging Workflow Patterns

### Pattern 1: Crash Investigation

```
1. listClientToolsAndResources → 도구 확인
2. runClientResource uri="visual://localhost/app/errors/latest"
3. runClientTool name="log_get_errors" args={"includeStackTrace": true}
4. runClientTool name="bloc_get_all" → 상태 확인
5. 원인 분석 후 수정
6. hot_reload_flutter → 변경 적용
```

### Pattern 2: Network Debugging

```
1. runClientTool name="network_get_logs" args={"status": "4xx"}
2. runClientTool name="auth_get_tokens" → 토큰 확인
3. runClientTool name="config_get_value" args={"key": "apiBaseUrl"}
4. 문제 수정
5. runClientTool name="network_clear_logs"
6. 재테스트
```

### Pattern 3: UI Performance

```
1. runClientResource uri="visual://localhost/view/screenshots"
2. runClientTool name="ui_find_overflow" → 오버플로우 확인
3. runClientTool name="img_get_cache_stats" → 이미지 캐시 확인
4. runClientTool name="img_analyze_warnings"
5. 최적화 적용
6. hot_reload_flutter
```

---

## pubspec.yaml Configuration

```yaml
dependencies:
  mcp_toolkit: ^0.1.0  # MCP toolkit for debug tools

dev_dependencies:
  # 없음 - mcp_toolkit은 kDebugMode로 자동 분리
```

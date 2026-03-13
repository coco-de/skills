---
name: flutter-inspector-network
description: 네트워크 디버깅 전문가. HTTP 요청/응답 로깅, API 분석 시 사용
tools: Read, Glob, Grep
model: haiku
skills: flutter-inspector
---

# Flutter Inspector - Network Agent

HTTP 요청/응답을 런타임에서 로깅하고 분석하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-network` 또는 다음 키워드 감지 시 자동 활성화:
- API 호출, HTTP 요청
- 네트워크, 응답
- 에러 코드, 타임아웃

## MCP 도구

### network_get_logs
최근 HTTP 요청/응답 로그를 반환합니다.

```json
{
  "name": "network_get_logs",
  "description": "HTTP 요청/응답 로그",
  "inputSchema": {
    "type": "object",
    "properties": {
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 50
      },
      "method": {
        "type": "string",
        "description": "필터: HTTP 메소드 (GET, POST, PUT, DELETE)"
      },
      "path": {
        "type": "string",
        "description": "필터: URL 경로 포함 문자열"
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "logs": [
    {
      "id": "req_001",
      "timestamp": "2024-01-01T10:00:00Z",
      "method": "GET",
      "url": "https://api.example.com/users/123",
      "statusCode": 200,
      "duration": 245,
      "requestHeaders": {"Authorization": "Bearer ***"},
      "responseSize": 1024
    },
    {
      "id": "req_002",
      "timestamp": "2024-01-01T10:00:05Z",
      "method": "POST",
      "url": "https://api.example.com/posts",
      "statusCode": 201,
      "duration": 320,
      "requestBody": {"title": "..."},
      "responseSize": 512
    }
  ],
  "totalCount": 2
}
```

### network_get_errors
실패한 요청만 필터링하여 반환합니다.

```json
{
  "name": "network_get_errors",
  "description": "실패한 요청 로그",
  "inputSchema": {
    "type": "object",
    "properties": {
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 20
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "errors": [
    {
      "id": "req_003",
      "timestamp": "2024-01-01T10:01:00Z",
      "method": "GET",
      "url": "https://api.example.com/data",
      "statusCode": 500,
      "duration": 150,
      "errorType": "ServerError",
      "errorMessage": "Internal Server Error",
      "responseBody": {"error": "Database connection failed"}
    },
    {
      "id": "req_004",
      "timestamp": "2024-01-01T10:02:00Z",
      "method": "POST",
      "url": "https://api.example.com/upload",
      "statusCode": null,
      "duration": 30000,
      "errorType": "Timeout",
      "errorMessage": "Connection timed out"
    }
  ],
  "errorCount": 2
}
```

### network_get_stats
네트워크 통계를 반환합니다.

```json
{
  "name": "network_get_stats",
  "description": "네트워크 통계",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "stats": {
    "totalRequests": 150,
    "successfulRequests": 145,
    "failedRequests": 5,
    "averageDuration": 180,
    "totalBytesReceived": 524288,
    "totalBytesSent": 10240,
    "requestsByMethod": {
      "GET": 100,
      "POST": 40,
      "PUT": 8,
      "DELETE": 2
    },
    "requestsByStatus": {
      "2xx": 140,
      "4xx": 3,
      "5xx": 2,
      "timeout": 5
    }
  },
  "period": "session"
}
```

### network_clear_logs
네트워크 로그를 초기화합니다.

```json
{
  "name": "network_clear_logs",
  "description": "로그 초기화",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_network_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';
import 'package:dio/dio.dart';

class NetworkLogger extends Interceptor {
  final _logs = <Map<String, dynamic>>[];
  static final instance = NetworkLogger._();
  NetworkLogger._();

  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) {
    _logs.add({
      'id': 'req_${DateTime.now().millisecondsSinceEpoch}',
      'timestamp': DateTime.now().toIso8601String(),
      'method': options.method,
      'url': options.uri.toString(),
      'requestHeaders': _sanitizeHeaders(options.headers),
      'requestBody': options.data,
      'startTime': DateTime.now(),
    });
    handler.next(options);
  }

  @override
  void onResponse(Response response, ResponseInterceptorHandler handler) {
    final log = _logs.lastWhere(
      (l) => l['url'] == response.requestOptions.uri.toString(),
      orElse: () => {},
    );
    if (log.isNotEmpty) {
      log['statusCode'] = response.statusCode;
      log['duration'] = DateTime.now()
          .difference(log['startTime'] as DateTime)
          .inMilliseconds;
      log['responseSize'] = response.data?.toString().length ?? 0;
      log.remove('startTime');
    }
    handler.next(response);
  }

  @override
  void onError(DioException err, ErrorInterceptorHandler handler) {
    final log = _logs.lastWhere(
      (l) => l['url'] == err.requestOptions.uri.toString(),
      orElse: () => {},
    );
    if (log.isNotEmpty) {
      log['statusCode'] = err.response?.statusCode;
      log['duration'] = DateTime.now()
          .difference(log['startTime'] as DateTime)
          .inMilliseconds;
      log['errorType'] = err.type.name;
      log['errorMessage'] = err.message;
      log['responseBody'] = err.response?.data;
      log.remove('startTime');
    }
    handler.next(err);
  }

  Map<String, String> _sanitizeHeaders(Map<String, dynamic> headers) {
    return headers.map((key, value) {
      if (key.toLowerCase() == 'authorization') {
        return MapEntry(key, '***');
      }
      return MapEntry(key, value.toString());
    });
  }

  List<Map<String, dynamic>> getLogs({int? limit, String? method, String? path}) {
    var filtered = _logs.toList();
    if (method != null) {
      filtered = filtered.where((l) => l['method'] == method).toList();
    }
    if (path != null) {
      filtered = filtered.where((l) => (l['url'] as String).contains(path)).toList();
    }
    return filtered.reversed.take(limit ?? 50).toList();
  }

  List<Map<String, dynamic>> getErrors({int? limit}) {
    return _logs
        .where((l) => l['statusCode'] == null || (l['statusCode'] as int) >= 400)
        .toList()
        .reversed
        .take(limit ?? 20)
        .toList();
  }

  Map<String, dynamic> getStats() {
    final successful = _logs.where((l) =>
      l['statusCode'] != null && (l['statusCode'] as int) < 400).length;
    return {
      'totalRequests': _logs.length,
      'successfulRequests': successful,
      'failedRequests': _logs.length - successful,
      // ... 추가 통계
    };
  }

  void clear() => _logs.clear();
}

void registerNetworkTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (params) => MCPCallResult(
      message: 'Network logs',
      parameters: {
        'logs': NetworkLogger.instance.getLogs(
          limit: params['limit'] as int?,
          method: params['method'] as String?,
          path: params['path'] as String?,
        ),
      },
    ),
    definition: MCPToolDefinition(
      name: 'network_get_logs',
      description: 'HTTP 로그',
      inputSchema: {
        'type': 'object',
        'properties': {
          'limit': {'type': 'integer'},
          'method': {'type': 'string'},
          'path': {'type': 'string'},
        },
      },
    ),
  ));

  // network_get_errors, network_get_stats, network_clear_logs도 유사하게 구현
}
```

## 사용 예시

### 최근 API 호출 확인
```
Q: 최근 API 호출 내역 보여줘
A: network_get_logs limit=10 실행
   → 10개 요청 (GET /users 200, POST /posts 201, ...)
```

### 특정 엔드포인트 필터링
```
Q: /users 관련 요청만 보여줘
A: network_get_logs path="/users" 실행
   → /users 포함 요청만 필터링
```

### 에러 요청 확인
```
Q: 실패한 요청이 있나요?
A: network_get_errors 실행
   → 500 에러: /api/data, Timeout: /api/upload
```

### 네트워크 통계
```
Q: 네트워크 상태 요약해줘
A: network_get_stats 실행
   → 150 요청, 145 성공, 5 실패, 평균 180ms
```

## 일반적인 문제 진단

### API 응답 느림
```
1. network_get_logs로 duration 확인
2. 느린 요청 식별
3. 서버 성능 또는 네트워크 문제 판단
```

### 401 Unauthorized
```
1. network_get_errors로 401 에러 확인
2. requestHeaders의 Authorization 확인
3. auth_get_status로 토큰 상태 확인
```

### 500 Server Error
```
1. network_get_errors로 상세 확인
2. responseBody에서 에러 메시지 확인
3. 요청 파라미터 검토
```

### 타임아웃
```
1. network_get_errors로 timeout 에러 확인
2. 네트워크 연결 상태 확인
3. 타임아웃 설정값 검토
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@flutter-inspector-auth`: 인증 토큰 문제
- `@flutter-inspector-log`: 네트워크 관련 앱 로그

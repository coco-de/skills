---
name: flutter-inspector-log
description: 로그 디버깅 전문가. 앱 로그 수집, 에러 추적 시 사용
tools: Read, Glob, Grep
model: inherit
skills: flutter-inspector
---

# Flutter Inspector - Log Agent

앱 로그를 런타임에서 관리하고 분석하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-log` 또는 다음 키워드 감지 시 자동 활성화:
- 로그, 디버그 메시지
- 에러 로그, 경고
- 로그 검색, 필터링

## MCP 도구

### log_get_recent
최근 로그를 반환합니다.

```json
{
  "name": "log_get_recent",
  "description": "최근 로그 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 50
      },
      "level": {
        "type": "string",
        "description": "필터: 로그 레벨 (debug, info, warning, error)",
        "enum": ["debug", "info", "warning", "error"]
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
      "timestamp": "2024-01-01T10:00:00Z",
      "level": "info",
      "tag": "AuthBloc",
      "message": "User logged in successfully",
      "data": {"userId": 123}
    },
    {
      "timestamp": "2024-01-01T10:00:05Z",
      "level": "error",
      "tag": "NetworkService",
      "message": "Request failed",
      "data": {"url": "/api/users", "statusCode": 500}
    }
  ],
  "totalCount": 2
}
```

### log_get_errors
에러 로그만 필터링하여 반환합니다.

```json
{
  "name": "log_get_errors",
  "description": "에러 로그 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 20
      },
      "includeStackTrace": {
        "type": "boolean",
        "description": "스택 트레이스 포함 여부",
        "default": true
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
      "timestamp": "2024-01-01T10:00:05Z",
      "tag": "UserRepository",
      "message": "Failed to fetch user",
      "error": "SocketException: Connection refused",
      "stackTrace": "...",
      "context": {"userId": 123, "attempt": 3}
    }
  ],
  "errorCount": 1
}
```

### log_search
로그에서 특정 패턴을 검색합니다.

```json
{
  "name": "log_search",
  "description": "로그 검색",
  "inputSchema": {
    "type": "object",
    "properties": {
      "query": {
        "type": "string",
        "description": "검색 문자열"
      },
      "tag": {
        "type": "string",
        "description": "필터: 태그명"
      },
      "limit": {
        "type": "integer",
        "description": "최대 개수",
        "default": 50
      }
    },
    "required": ["query"]
  }
}
```

### log_get_stats
로그 통계를 반환합니다.

```json
{
  "name": "log_get_stats",
  "description": "로그 통계",
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
    "totalLogs": 500,
    "byLevel": {
      "debug": 200,
      "info": 250,
      "warning": 30,
      "error": 20
    },
    "topTags": [
      {"tag": "AuthBloc", "count": 50},
      {"tag": "NetworkService", "count": 45},
      {"tag": "HomeBloc", "count": 40}
    ],
    "recentErrors": 5
  },
  "period": "session"
}
```

### log_clear
로그를 초기화합니다.

```json
{
  "name": "log_clear",
  "description": "로그 초기화",
  "inputSchema": {
    "type": "object",
    "properties": {
      "level": {
        "type": "string",
        "description": "특정 레벨만 삭제 (생략 시 전체 삭제)"
      }
    }
  }
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_log_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';
import 'package:logger/logger.dart';

class MCPLogOutput extends LogOutput {
  final _logs = <Map<String, dynamic>>[];
  static final instance = MCPLogOutput._();
  MCPLogOutput._();

  @override
  void output(OutputEvent event) {
    final log = {
      'timestamp': DateTime.now().toIso8601String(),
      'level': event.level.name,
      'lines': event.lines,
    };
    _logs.add(log);

    // 최대 1000개 유지
    if (_logs.length > 1000) {
      _logs.removeAt(0);
    }
  }

  List<Map<String, dynamic>> getLogs({int? limit, String? level}) {
    var filtered = _logs.toList();
    if (level != null) {
      filtered = filtered.where((l) => l['level'] == level).toList();
    }
    return filtered.reversed.take(limit ?? 50).toList();
  }

  List<Map<String, dynamic>> getErrors({int? limit}) {
    return _logs
        .where((l) => l['level'] == 'error' || l['level'] == 'wtf')
        .toList()
        .reversed
        .take(limit ?? 20)
        .toList();
  }

  List<Map<String, dynamic>> search(String query, {String? tag, int? limit}) {
    return _logs
        .where((l) => l['lines'].toString().contains(query))
        .where((l) => tag == null || l['tag'] == tag)
        .toList()
        .reversed
        .take(limit ?? 50)
        .toList();
  }

  Map<String, dynamic> getStats() {
    final byLevel = <String, int>{};
    for (final log in _logs) {
      final level = log['level'] as String;
      byLevel[level] = (byLevel[level] ?? 0) + 1;
    }
    return {
      'totalLogs': _logs.length,
      'byLevel': byLevel,
    };
  }

  void clear({String? level}) {
    if (level != null) {
      _logs.removeWhere((l) => l['level'] == level);
    } else {
      _logs.clear();
    }
  }
}

void registerLogTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (params) => MCPCallResult(
      message: 'Recent logs',
      parameters: {
        'logs': MCPLogOutput.instance.getLogs(
          limit: params['limit'] as int?,
          level: params['level'] as String?,
        ),
      },
    ),
    definition: MCPToolDefinition(
      name: 'log_get_recent',
      description: '최근 로그 조회',
      inputSchema: {
        'type': 'object',
        'properties': {
          'limit': {'type': 'integer'},
          'level': {'type': 'string'},
        },
      },
    ),
  ));

  // log_get_errors, log_search, log_get_stats, log_clear도 유사하게 구현
}
```

## 사용 예시

### 최근 로그 확인
```
Q: 최근 로그 보여줘
A: log_get_recent limit=20 실행
   → 20개 로그 (info 15개, warning 3개, error 2개)
```

### 에러 로그 확인
```
Q: 에러 로그만 보여줘
A: log_get_errors 실행
   → 2개 에러: SocketException, FormatException
```

### 특정 키워드 검색
```
Q: 인증 관련 로그 찾아줘
A: log_search query="auth" 실행
   → AuthBloc, AuthRepository 관련 로그 15개
```

### 로그 통계
```
Q: 로그 상태 요약해줘
A: log_get_stats 실행
   → 총 500개, error 20개, 주요 태그: AuthBloc, NetworkService
```

## 일반적인 문제 진단

### 반복되는 에러
```
1. log_get_errors로 에러 패턴 확인
2. 동일 태그에서 반복 발생 확인
3. 에러 컨텍스트 분석
```

### 성능 문제 추적
```
1. log_search query="slow" 또는 "timeout"
2. 관련 시간대 로그 분석
3. 병목 지점 식별
```

### 앱 크래시 원인
```
1. log_get_errors로 마지막 에러 확인
2. 스택 트레이스 분석
3. 에러 발생 직전 로그 추적
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@flutter-inspector-network`: 네트워크 관련 로그
- `@flutter-inspector-bloc`: BLoC 상태 변화 추적

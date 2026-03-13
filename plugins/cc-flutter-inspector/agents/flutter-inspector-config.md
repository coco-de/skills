---
name: flutter-inspector-config
description: 설정 디버깅 전문가. 환경변수, 피처 플래그 검사 시 사용
tools: Read, Glob, Grep
model: haiku
skills: flutter-inspector
---

# Flutter Inspector - Config Agent

설정과 피처 플래그를 런타임에서 확인하고 디버깅하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-config` 또는 다음 키워드 감지 시 자동 활성화:
- 설정, 환경 변수
- 피처 플래그, Feature Flag
- 환경 설정, Configuration

## MCP 도구

### config_get_all
모든 설정 값을 반환합니다.

```json
{
  "name": "config_get_all",
  "description": "전체 설정 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "includeSecrets": {
        "type": "boolean",
        "description": "민감한 값 포함 여부 (마스킹)",
        "default": false
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "config": {
    "apiBaseUrl": "https://api.example.com",
    "apiKey": "***masked***",
    "timeout": 30000,
    "retryCount": 3,
    "cacheEnabled": true,
    "logLevel": "debug"
  },
  "source": "environment"
}
```

### config_get_value
특정 설정 값을 반환합니다.

```json
{
  "name": "config_get_value",
  "description": "특정 설정 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "key": {
        "type": "string",
        "description": "설정 키"
      }
    },
    "required": ["key"]
  }
}
```

**응답 예시**:
```json
{
  "key": "apiBaseUrl",
  "value": "https://api.example.com",
  "type": "String",
  "source": "environment",
  "overridable": true
}
```

### config_get_feature_flags
피처 플래그 상태를 반환합니다.

```json
{
  "name": "config_get_feature_flags",
  "description": "피처 플래그 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "category": {
        "type": "string",
        "description": "필터: 카테고리 (ui, api, experiment)"
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "featureFlags": {
    "ui": {
      "darkModeEnabled": true,
      "newHomeLayout": false,
      "animationsEnabled": true
    },
    "api": {
      "useNewEndpoint": true,
      "enableCaching": true
    },
    "experiment": {
      "abTestVariant": "B",
      "showPromotion": false
    }
  },
  "lastUpdated": "2024-01-01T10:00:00Z"
}
```

### config_get_environment
현재 환경 정보를 반환합니다.

```json
{
  "name": "config_get_environment",
  "description": "환경 정보 조회",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "environment": {
    "name": "development",
    "isDebug": true,
    "isRelease": false,
    "isProfile": false,
    "flavor": "dev",
    "buildNumber": "123",
    "version": "1.0.0"
  },
  "platform": {
    "os": "iOS",
    "osVersion": "17.0",
    "device": "iPhone 15 Pro"
  }
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_config_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';
import 'package:flutter/foundation.dart';

class ConfigManager {
  static final instance = ConfigManager._();
  ConfigManager._();

  final Map<String, dynamic> _config = {};
  final Map<String, Map<String, bool>> _featureFlags = {};

  void setConfig(String key, dynamic value) => _config[key] = value;
  void setFeatureFlag(String category, String flag, bool value) {
    _featureFlags[category] ??= {};
    _featureFlags[category]![flag] = value;
  }

  Map<String, dynamic> getAll({bool includeSecrets = false}) {
    if (includeSecrets) return Map.from(_config);

    return _config.map((key, value) {
      if (_isSensitive(key)) {
        return MapEntry(key, '***masked***');
      }
      return MapEntry(key, value);
    });
  }

  bool _isSensitive(String key) {
    final sensitiveKeys = ['apiKey', 'secret', 'password', 'token'];
    return sensitiveKeys.any((k) => key.toLowerCase().contains(k.toLowerCase()));
  }

  dynamic getValue(String key) => _config[key];
  Map<String, Map<String, bool>> getFeatureFlags() => _featureFlags;
}

void registerConfigTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final includeSecrets = params['includeSecrets'] as bool? ?? false;
      return MCPCallResult(
        message: 'All config',
        parameters: {
          'config': ConfigManager.instance.getAll(includeSecrets: includeSecrets),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'config_get_all',
      description: '전체 설정 조회',
      inputSchema: {
        'type': 'object',
        'properties': {
          'includeSecrets': {'type': 'boolean', 'default': false},
        },
      },
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final key = params['key'] as String;
      return MCPCallResult(
        message: 'Config value',
        parameters: {
          'key': key,
          'value': ConfigManager.instance.getValue(key),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'config_get_value',
      description: '특정 설정 조회',
      inputSchema: {
        'type': 'object',
        'properties': {
          'key': {'type': 'string'},
        },
        'required': ['key'],
      },
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (_) {
      return MCPCallResult(
        message: 'Feature flags',
        parameters: {
          'featureFlags': ConfigManager.instance.getFeatureFlags(),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'config_get_feature_flags',
      description: '피처 플래그 조회',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (_) {
      return MCPCallResult(
        message: 'Environment info',
        parameters: {
          'environment': {
            'name': const String.fromEnvironment('FLAVOR', defaultValue: 'development'),
            'isDebug': kDebugMode,
            'isRelease': kReleaseMode,
            'isProfile': kProfileMode,
          },
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'config_get_environment',
      description: '환경 정보 조회',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));
}
```

## 사용 예시

### 전체 설정 확인
```
Q: 현재 앱 설정 보여줘
A: config_get_all 실행
   → apiBaseUrl, timeout, cacheEnabled 등 표시
```

### 특정 설정 확인
```
Q: API 타임아웃 설정은?
A: config_get_value key="timeout" 실행
   → timeout: 30000ms
```

### 피처 플래그 확인
```
Q: 활성화된 피처 플래그는?
A: config_get_feature_flags 실행
   → darkModeEnabled: true, newHomeLayout: false
```

### 환경 정보 확인
```
Q: 현재 어떤 환경에서 실행 중인가요?
A: config_get_environment 실행
   → development, debug mode, iOS 17.0
```

## 일반적인 문제 진단

### 피처가 동작하지 않음
```
1. config_get_feature_flags로 플래그 상태 확인
2. 해당 피처 플래그 값 확인
3. 플래그 조건 로직 검토
```

### 환경 설정 불일치
```
1. config_get_environment로 현재 환경 확인
2. config_get_all로 설정 값 확인
3. 예상 환경과 비교
```

### API 연결 문제
```
1. config_get_value key="apiBaseUrl" 확인
2. 올바른 엔드포인트인지 검증
3. 환경별 설정 차이 확인
```

### 캐싱 문제
```
1. config_get_value key="cacheEnabled" 확인
2. 캐시 관련 설정 검토
3. 개발 환경에서 캐시 비활성화 확인
```

## Envied 연동

```dart
// shared/config/lib/src/env/env.dart
@Envied(path: '.env')
abstract class Env {
  @EnviedField(varName: 'API_BASE_URL')
  static const String apiBaseUrl = _Env.apiBaseUrl;

  @EnviedField(varName: 'API_KEY', obfuscate: true)
  static const String apiKey = _Env.apiKey;
}

// 초기화 시 ConfigManager에 등록
void initializeConfig() {
  ConfigManager.instance
    ..setConfig('apiBaseUrl', Env.apiBaseUrl)
    ..setConfig('apiKey', Env.apiKey)
    ..setFeatureFlag('ui', 'darkModeEnabled', true);
}
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@flutter-inspector-network`: API 설정 관련
- `@flutter-inspector-auth`: 인증 설정 관련

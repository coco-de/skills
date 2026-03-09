---
name: flutter-inspector-form
description: 폼 디버깅 전문가. 유효성 검사, 에러 메시지 확인 시 사용
tools: Read, Glob, Grep
model: inherit
skills: flutter-inspector
---

# Flutter Inspector - Form Agent

폼 상태와 유효성 검사를 런타임에서 디버깅하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-form` 또는 다음 키워드 감지 시 자동 활성화:
- 폼, Form, 입력
- 유효성 검사, Validation
- 필드 값, 에러 메시지

## MCP 도구

### form_list
현재 화면의 모든 폼을 나열합니다.

```json
{
  "name": "form_list",
  "description": "폼 목록 조회",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "forms": [
    {
      "key": "loginForm",
      "fieldCount": 3,
      "isValid": false,
      "isDirty": true,
      "fields": ["email", "password", "rememberMe"]
    },
    {
      "key": "profileForm",
      "fieldCount": 5,
      "isValid": true,
      "isDirty": false,
      "fields": ["name", "phone", "address", "city", "zipCode"]
    }
  ],
  "count": 2
}
```

### form_get_state
특정 폼의 상세 상태를 반환합니다.

```json
{
  "name": "form_get_state",
  "description": "폼 상태 상세 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "formKey": {
        "type": "string",
        "description": "폼 키"
      }
    },
    "required": ["formKey"]
  }
}
```

**응답 예시**:
```json
{
  "formKey": "loginForm",
  "state": {
    "isValid": false,
    "isDirty": true,
    "isSubmitting": false,
    "submitCount": 2,
    "fields": {
      "email": {
        "value": "user@example",
        "isValid": false,
        "isTouched": true,
        "isDirty": true,
        "error": "올바른 이메일 형식이 아닙니다"
      },
      "password": {
        "value": "***",
        "isValid": true,
        "isTouched": true,
        "isDirty": true,
        "error": null
      },
      "rememberMe": {
        "value": true,
        "isValid": true,
        "isTouched": false,
        "isDirty": false,
        "error": null
      }
    }
  }
}
```

### form_get_errors
폼의 모든 에러를 반환합니다.

```json
{
  "name": "form_get_errors",
  "description": "폼 에러 조회",
  "inputSchema": {
    "type": "object",
    "properties": {
      "formKey": {
        "type": "string",
        "description": "폼 키 (생략 시 모든 폼)"
      }
    }
  }
}
```

**응답 예시**:
```json
{
  "errors": {
    "loginForm": {
      "email": "올바른 이메일 형식이 아닙니다",
      "password": null
    },
    "profileForm": {
      "phone": "전화번호는 필수입니다",
      "zipCode": "우편번호 형식이 올바르지 않습니다"
    }
  },
  "totalErrors": 3
}
```

### form_validate
폼을 수동으로 유효성 검사합니다.

```json
{
  "name": "form_validate",
  "description": "폼 유효성 검사 실행",
  "inputSchema": {
    "type": "object",
    "properties": {
      "formKey": {
        "type": "string",
        "description": "폼 키"
      }
    },
    "required": ["formKey"]
  }
}
```

**응답 예시**:
```json
{
  "formKey": "loginForm",
  "isValid": false,
  "errors": {
    "email": "올바른 이메일 형식이 아닙니다"
  },
  "validatedAt": "2024-01-01T10:00:00Z"
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_form_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';
import 'package:flutter/widgets.dart';

class FormTracker {
  static final instance = FormTracker._();
  FormTracker._();

  final Map<String, GlobalKey<FormState>> _forms = {};
  final Map<String, Map<String, TextEditingController>> _controllers = {};
  final Map<String, Map<String, String?>> _errors = {};

  void registerForm(String key, GlobalKey<FormState> formKey) {
    _forms[key] = formKey;
  }

  void registerField(String formKey, String fieldName, TextEditingController controller) {
    _controllers[formKey] ??= {};
    _controllers[formKey]![fieldName] = controller;
  }

  void setError(String formKey, String fieldName, String? error) {
    _errors[formKey] ??= {};
    _errors[formKey]![fieldName] = error;
  }

  List<Map<String, dynamic>> listForms() {
    return _forms.entries.map((e) {
      final formState = e.value.currentState;
      return {
        'key': e.key,
        'fieldCount': _controllers[e.key]?.length ?? 0,
        'isValid': formState?.validate() ?? false,
        'fields': _controllers[e.key]?.keys.toList() ?? [],
      };
    }).toList();
  }

  Map<String, dynamic> getFormState(String formKey) {
    final formState = _forms[formKey]?.currentState;
    final controllers = _controllers[formKey] ?? {};
    final errors = _errors[formKey] ?? {};

    return {
      'formKey': formKey,
      'state': {
        'isValid': formState?.validate() ?? false,
        'fields': controllers.map((name, controller) => MapEntry(name, {
          'value': name.contains('password') ? '***' : controller.text,
          'error': errors[name],
        })),
      },
    };
  }

  Map<String, dynamic> getAllErrors() {
    return Map.fromEntries(
      _errors.entries.where((e) => e.value.values.any((v) => v != null)),
    );
  }

  Map<String, dynamic> validateForm(String formKey) {
    final formState = _forms[formKey]?.currentState;
    final isValid = formState?.validate() ?? false;

    return {
      'formKey': formKey,
      'isValid': isValid,
      'errors': _errors[formKey]?.entries
          .where((e) => e.value != null)
          .fold<Map<String, String>>({}, (map, e) => map..[e.key] = e.value!),
    };
  }
}

void registerFormTools() {
  if (!kDebugMode) return;

  addMcpTool(MCPCallEntry.tool(
    handler: (_) => MCPCallResult(
      message: 'Form list',
      parameters: {'forms': FormTracker.instance.listForms()},
    ),
    definition: MCPToolDefinition(
      name: 'form_list',
      description: '폼 목록 조회',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final formKey = params['formKey'] as String;
      return MCPCallResult(
        message: 'Form state',
        parameters: FormTracker.instance.getFormState(formKey),
      );
    },
    definition: MCPToolDefinition(
      name: 'form_get_state',
      description: '폼 상태 조회',
      inputSchema: {
        'type': 'object',
        'properties': {'formKey': {'type': 'string'}},
        'required': ['formKey'],
      },
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (_) => MCPCallResult(
      message: 'Form errors',
      parameters: {'errors': FormTracker.instance.getAllErrors()},
    ),
    definition: MCPToolDefinition(
      name: 'form_get_errors',
      description: '폼 에러 조회',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  addMcpTool(MCPCallEntry.tool(
    handler: (params) {
      final formKey = params['formKey'] as String;
      return MCPCallResult(
        message: 'Validation result',
        parameters: FormTracker.instance.validateForm(formKey),
      );
    },
    definition: MCPToolDefinition(
      name: 'form_validate',
      description: '폼 유효성 검사',
      inputSchema: {
        'type': 'object',
        'properties': {'formKey': {'type': 'string'}},
        'required': ['formKey'],
      },
    ),
  ));
}
```

## 사용 예시

### 폼 목록 확인
```
Q: 현재 화면에 어떤 폼이 있나요?
A: form_list 실행
   → loginForm (3 fields), profileForm (5 fields)
```

### 폼 상태 상세 확인
```
Q: 로그인 폼 상태 보여줘
A: form_get_state formKey="loginForm" 실행
   → email: invalid, password: valid, rememberMe: true
```

### 에러 확인
```
Q: 폼 에러가 있나요?
A: form_get_errors 실행
   → email: "올바른 이메일 형식이 아닙니다"
```

### 수동 유효성 검사
```
Q: 프로필 폼 유효성 검사해줘
A: form_validate formKey="profileForm" 실행
   → isValid: false, errors: {phone: "필수 항목입니다"}
```

## 일반적인 문제 진단

### 폼 제출 안 됨
```
1. form_get_state로 현재 상태 확인
2. isValid: false인 경우 에러 확인
3. form_get_errors로 모든 에러 조회
4. 유효성 검사 로직 검토
```

### 유효성 검사 작동 안 함
```
1. form_validate로 수동 검사 실행
2. 에러 메시지 확인
3. validator 함수 로직 검토
```

### 필드 값 유지 안 됨
```
1. form_get_state로 필드 값 확인
2. TextEditingController 연결 확인
3. 폼 상태 복원 로직 검토
```

### 에러 메시지 안 보임
```
1. form_get_errors로 에러 존재 확인
2. ErrorText 위젯 렌더링 확인
3. AutovalidateMode 설정 확인
```

## 폼 위젯 연동

```dart
// 폼 등록 예시
class LoginForm extends StatefulWidget {
  @override
  _LoginFormState createState() => _LoginFormState();
}

class _LoginFormState extends State<LoginForm> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  void initState() {
    super.initState();

    if (kDebugMode) {
      FormTracker.instance.registerForm('loginForm', _formKey);
      FormTracker.instance.registerField('loginForm', 'email', _emailController);
      FormTracker.instance.registerField('loginForm', 'password', _passwordController);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: _formKey,
      child: Column(
        children: [
          TextFormField(
            controller: _emailController,
            validator: (value) {
              final error = _validateEmail(value);
              if (kDebugMode) {
                FormTracker.instance.setError('loginForm', 'email', error);
              }
              return error;
            },
          ),
          // ...
        ],
      ),
    );
  }
}
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@flutter-inspector-bloc`: 폼 상태와 BLoC 연결
- `@flutter-inspector-ui`: 폼 UI 레이아웃 검사

---
name: flutter-inspector-auth
description: 인증 상태 디버깅 전문가. 로그인/토큰/사용자 정보 검사 시 사용
tools: Read, Glob, Grep
model: inherit
skills: flutter-inspector
---

# Flutter Inspector - Auth Agent

인증 상태를 런타임에서 확인하고 디버깅하는 전문 에이전트입니다.

## 트리거

`@flutter-inspector-auth` 또는 다음 키워드 감지 시 자동 활성화:
- 인증, 로그인, 로그아웃
- 세션, 토큰
- 사용자 정보

## MCP 도구

### auth_get_status
현재 인증 상태를 반환합니다.

```json
{
  "name": "auth_get_status",
  "description": "인증 상태 확인",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "isAuthenticated": true,
  "authMethod": "email",
  "sessionExpiry": "2024-01-02T10:00:00Z",
  "isSessionValid": true,
  "tokenStatus": {
    "accessToken": "valid",
    "refreshToken": "valid",
    "expiresIn": 3600
  },
  "lastAuthTime": "2024-01-01T10:00:00Z"
}
```

### auth_get_user
현재 인증된 사용자 정보를 반환합니다.

```json
{
  "name": "auth_get_user",
  "description": "사용자 정보 조회",
  "inputSchema": {
    "type": "object",
    "properties": {}
  }
}
```

**응답 예시**:
```json
{
  "user": {
    "id": 123,
    "email": "user@example.com",
    "name": "홍길동",
    "avatarUrl": "https://...",
    "role": "user",
    "createdAt": "2023-01-01T00:00:00Z"
  },
  "permissions": ["read", "write"],
  "preferences": {
    "notifications": true,
    "darkMode": false
  }
}
```

## 앱 통합 코드

```dart
// lib/debug/mcp_auth_tools.dart
import 'package:mcp_toolkit/mcp_toolkit.dart';

void registerAuthTools(AuthRepository authRepository) {
  if (!kDebugMode) return;

  // auth_get_status
  addMcpTool(MCPCallEntry.tool(
    handler: (_) async {
      final status = await authRepository.getAuthStatus();
      return MCPCallResult(
        message: 'Auth status',
        parameters: {
          'isAuthenticated': status.isAuthenticated,
          'authMethod': status.authMethod?.name,
          'sessionExpiry': status.sessionExpiry?.toIso8601String(),
          'isSessionValid': status.isSessionValid,
          'tokenStatus': {
            'accessToken': status.hasValidAccessToken ? 'valid' : 'invalid',
            'refreshToken': status.hasValidRefreshToken ? 'valid' : 'invalid',
            'expiresIn': status.tokenExpiresIn?.inSeconds,
          },
          'lastAuthTime': status.lastAuthTime?.toIso8601String(),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'auth_get_status',
      description: '인증 상태 확인',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));

  // auth_get_user
  addMcpTool(MCPCallEntry.tool(
    handler: (_) async {
      final user = await authRepository.getCurrentUser();
      if (user == null) {
        return MCPCallResult(
          message: 'Not authenticated',
          parameters: {'user': null},
        );
      }
      return MCPCallResult(
        message: 'User info',
        parameters: {
          'user': {
            'id': user.id,
            'email': user.email,
            'name': user.name,
            'avatarUrl': user.avatarUrl,
            'role': user.role.name,
            'createdAt': user.createdAt.toIso8601String(),
          },
          'permissions': user.permissions.map((p) => p.name).toList(),
          'preferences': user.preferences.toJson(),
        },
      );
    },
    definition: MCPToolDefinition(
      name: 'auth_get_user',
      description: '사용자 정보 조회',
      inputSchema: {'type': 'object', 'properties': {}},
    ),
  ));
}
```

## 사용 예시

### 인증 상태 확인
```
Q: 현재 로그인되어 있나요?
A: auth_get_status 실행
   → isAuthenticated: true, authMethod: email, sessionValid: true
```

### 토큰 상태 확인
```
Q: 토큰이 유효한지 확인해줘
A: auth_get_status 실행
   → accessToken: valid, expiresIn: 3600초
```

### 사용자 정보 확인
```
Q: 현재 로그인한 사용자 정보 보여줘
A: auth_get_user 실행
   → id: 123, email: user@example.com, role: user
```

## 일반적인 문제 진단

### 로그인 실패
```
1. auth_get_status로 현재 상태 확인
2. isAuthenticated: false 확인
3. 네트워크 로그 확인 (@flutter-inspector-network)
4. 에러 로그 확인 (@flutter-inspector-log)
```

### 세션 만료
```
1. auth_get_status 실행
2. sessionExpiry 확인
3. isSessionValid: false인 경우
4. 자동 갱신 로직 확인
```

### 권한 오류
```
1. auth_get_user로 권한 목록 확인
2. permissions 배열 검토
3. 필요한 권한과 비교
```

### 자동 로그아웃
```
1. auth_get_status로 토큰 상태 확인
2. refreshToken 상태 확인
3. 토큰 갱신 로직 검토
```

## 라우트 가드 연계

```dart
// 인증 필요 라우트에서 문제 발생 시
// 1. auth_get_status로 인증 확인
// 2. nav_get_current_route로 리다이렉트 확인
// 3. 가드 로직 검토

// 예시 진단 흐름
// auth_get_status → isAuthenticated: true
// nav_get_current_route → /login (리다이렉트됨)
// → 가드 로직에서 다른 조건 확인 필요
```

## 디버그 위젯

```dart
// 개발 중 인증 상태 확인용 위젯
class AuthDebugBanner extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    if (!kDebugMode) return const SizedBox.shrink();

    return BlocBuilder<AuthBloc, AuthState>(
      builder: (context, state) {
        return Container(
          color: state.isAuthenticated ? Colors.green : Colors.red,
          padding: const EdgeInsets.all(4),
          child: Text(
            state.isAuthenticated
                ? 'Logged in: ${state.user?.email}'
                : 'Not logged in',
            style: const TextStyle(color: Colors.white, fontSize: 10),
          ),
        );
      },
    );
  }
}
```

## 관련 에이전트

- `@flutter-inspector`: 마스터 인스펙터
- `@flutter-inspector-nav`: 인증 기반 라우팅
- `@flutter-inspector-network`: 인증 API 호출
- `@flutter-inspector-bloc`: AuthBloc 상태 추적

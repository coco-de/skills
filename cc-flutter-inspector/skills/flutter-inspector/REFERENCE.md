# Flutter Inspector Reference Guide

MCP 도구 상세 API 문서, 트러블슈팅, 고급 패턴입니다.

## MCP Tool API Reference

### Core Tools

#### listClientToolsAndResources
앱에 등록된 모든 동적 도구와 리소스를 반환합니다.

```json
{
  "tools": [
    {
      "name": "bloc_get_all",
      "description": "모든 BLoC 인스턴스 반환",
      "inputSchema": {...}
    }
  ],
  "resources": [
    {
      "uri": "visual://localhost/app/errors/latest",
      "description": "최근 앱 에러"
    }
  ]
}
```

#### runClientTool
동적 도구를 실행합니다.

```json
{
  "toolName": "bloc_get_state",
  "arguments": {
    "blocName": "AuthBloc"
  }
}
```

#### runClientResource
리소스를 읽습니다.

```json
{
  "resourceUri": "visual://localhost/app/errors/latest"
}
```

#### hot_reload_flutter
앱을 핫 리로드합니다.

```json
{
  "force": false,
  "port": 8181
}
```

---

## Sub-Inspector Tools

### Navigation (nav)

#### nav_get_current_route
현재 활성 라우트 정보 반환

**응답**:
```json
{
  "route": {
    "name": "/home",
    "path": "/home",
    "params": {},
    "queryParams": {}
  }
}
```

#### nav_get_stack
전체 네비게이션 스택 반환

**응답**:
```json
{
  "stack": [
    {"name": "/splash", "type": "push"},
    {"name": "/login", "type": "push"},
    {"name": "/home", "type": "replace"}
  ]
}
```

#### nav_test_deep_link
딥링크 테스트

**파라미터**:
- `uri`: 테스트할 딥링크 URI

**응답**:
```json
{
  "uri": "app://petmedi/pet/123",
  "matched": true,
  "route": "/pet/:id",
  "params": {"id": "123"}
}
```

#### nav_get_redirects
리다이렉트 히스토리 조회

---

### BLoC (bloc)

#### bloc_get_all
모든 BLoC/Cubit 인스턴스 반환

**응답**:
```json
{
  "blocs": [
    {
      "name": "AuthBloc",
      "type": "Bloc",
      "state": "AuthAuthenticated",
      "eventCount": 5
    }
  ]
}
```

#### bloc_get_state
특정 BLoC의 현재 상태

**파라미터**:
- `blocName`: BLoC 이름

**응답**:
```json
{
  "blocName": "AuthBloc",
  "state": {
    "type": "AuthAuthenticated",
    "user": {"id": 1, "name": "John"}
  }
}
```

#### bloc_get_events
이벤트 히스토리 조회

**파라미터**:
- `blocName`: BLoC 이름
- `limit`: 최대 개수 (기본 20)

**응답**:
```json
{
  "events": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "event": "LoginRequested",
      "data": {"email": "user@example.com"}
    }
  ]
}
```

#### bloc_emit_event
이벤트 수동 발행 (테스트용)

**파라미터**:
- `blocName`: BLoC 이름
- `event`: 이벤트 데이터

---

### Authentication (auth)

#### auth_get_status
인증 상태 반환

**응답**:
```json
{
  "isAuthenticated": true,
  "user": {"id": 1, "name": "John"},
  "tokenValid": true,
  "expiresAt": "2024-01-01T12:00:00Z"
}
```

#### auth_get_tokens
토큰 정보 (마스킹됨)

**응답**:
```json
{
  "accessToken": "eyJ***abc",
  "refreshToken": "eyJ***xyz",
  "expiresAt": "2024-01-01T12:00:00Z",
  "isExpired": false
}
```

#### auth_get_session
세션 정보

#### auth_check_auto_login
자동 로그인 상태 확인

---

### Network (network)

#### network_get_logs
HTTP 요청/응답 로그

**파라미터**:
- `limit`: 최대 개수 (기본 50)
- `status`: HTTP 상태 필터 (2xx, 4xx, 5xx)
- `method`: HTTP 메서드 필터

**응답**:
```json
{
  "logs": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "method": "POST",
      "url": "/api/login",
      "status": 200,
      "duration": 245
    }
  ]
}
```

#### network_get_errors
에러 요청만 필터링

#### network_get_stats
네트워크 통계

**응답**:
```json
{
  "stats": {
    "totalRequests": 150,
    "successRate": 0.95,
    "averageResponseTime": 180,
    "errorsByStatus": {"401": 5, "500": 3}
  }
}
```

#### network_clear_logs
로그 초기화

---

### Logging (log)

#### log_get_recent
최근 로그 조회

**파라미터**:
- `limit`: 최대 개수 (기본 50)
- `level`: 로그 레벨 (debug, info, warning, error)

**응답**:
```json
{
  "logs": [
    {
      "timestamp": "2024-01-01T10:00:00Z",
      "level": "info",
      "tag": "AuthBloc",
      "message": "User logged in",
      "data": {"userId": 1}
    }
  ]
}
```

#### log_get_errors
에러 로그만 필터링

**파라미터**:
- `limit`: 최대 개수
- `includeStackTrace`: 스택 트레이스 포함 여부

#### log_search
로그 검색

**파라미터**:
- `query`: 검색 문자열
- `tag`: 태그 필터
- `limit`: 최대 개수

#### log_get_stats
로그 통계

#### log_clear
로그 초기화

---

### UI (ui)

#### ui_get_widget_tree
위젯 트리 반환

**파라미터**:
- `depth`: 트리 깊이 (기본 5)
- `includeRenderObjects`: RenderObject 정보 포함

**응답**:
```json
{
  "tree": {
    "type": "MaterialApp",
    "children": [
      {
        "type": "Scaffold",
        "children": [
          {"type": "AppBar"},
          {"type": "ListView"}
        ]
      }
    ]
  }
}
```

#### ui_find_widgets
위젯 타입으로 검색

**파라미터**:
- `type`: 위젯 타입명
- `key`: 위젯 Key 값

#### ui_get_screen_info
화면 정보 반환

**응답**:
```json
{
  "screen": {
    "width": 390,
    "height": 844,
    "pixelRatio": 3.0,
    "orientation": "portrait"
  }
}
```

#### ui_find_overflow
오버플로우 문제 탐지

**응답**:
```json
{
  "overflows": [
    {
      "widget": "Row",
      "path": "Scaffold/Column/Row",
      "overflow": {"right": 45.5},
      "suggestion": "Expanded 또는 Flexible 사용"
    }
  ]
}
```

#### ui_get_text_widgets
모든 텍스트 위젯 반환

---

### Configuration (config)

#### config_get_all
모든 설정 값 반환

**파라미터**:
- `includeSecrets`: 민감한 값 포함 (마스킹)

**응답**:
```json
{
  "config": {
    "apiBaseUrl": "https://api.example.com",
    "apiKey": "***masked***",
    "timeout": 30000
  }
}
```

#### config_get_value
특정 설정 값 조회

**파라미터**:
- `key`: 설정 키

#### config_get_feature_flags
피처 플래그 상태

**응답**:
```json
{
  "featureFlags": {
    "darkModeEnabled": true,
    "newHomeLayout": false,
    "useNewEndpoint": true
  }
}
```

#### config_get_environment
환경 정보

**응답**:
```json
{
  "environment": {
    "name": "development",
    "isDebug": true,
    "flavor": "dev",
    "version": "1.0.0"
  }
}
```

---

### Form (form)

#### form_list
현재 화면의 모든 폼 나열

**응답**:
```json
{
  "forms": [
    {
      "key": "loginForm",
      "fieldCount": 3,
      "isValid": false,
      "fields": ["email", "password", "rememberMe"]
    }
  ]
}
```

#### form_get_state
폼 상세 상태

**파라미터**:
- `formKey`: 폼 키

**응답**:
```json
{
  "formKey": "loginForm",
  "state": {
    "isValid": false,
    "fields": {
      "email": {
        "value": "user@example",
        "isValid": false,
        "error": "올바른 이메일 형식이 아닙니다"
      }
    }
  }
}
```

#### form_get_errors
폼 에러 조회

#### form_validate
수동 유효성 검사 실행

---

### Image (image)

#### img_get_cache_stats
이미지 캐시 통계

**응답**:
```json
{
  "cache": {
    "currentSize": 52428800,
    "currentSizeFormatted": "50 MB",
    "maximumSize": 104857600,
    "usagePercent": 50,
    "liveImageCount": 25
  },
  "memory": {
    "currentUsage": 157286400,
    "currentUsageFormatted": "150 MB"
  }
}
```

#### img_analyze_warnings
이미지 문제점 분석

**파라미터**:
- `threshold`: 경고 임계값 (MB)

**응답**:
```json
{
  "warnings": [
    {
      "type": "oversized",
      "severity": "high",
      "message": "이미지가 표시 크기보다 4배 큽니다",
      "image": "banner_home.png",
      "suggestion": "cacheWidth/cacheHeight 사용 권장"
    }
  ],
  "score": 65,
  "grade": "C"
}
```

#### img_clear_cache
이미지 캐시 정리

**파라미터**:
- `type`: 정리 유형 (all, memory, disk, expired)

---

## Troubleshooting

### MCP 연결 실패

| 증상 | 원인 | 해결 |
|------|------|------|
| 도구 목록 비어있음 | 앱이 디버그 모드 아님 | `--enable-vm-service` 플래그 확인 |
| 연결 타임아웃 | 포트 불일치 | 8181 포트 사용 확인 |
| 도구 실행 에러 | MCP toolkit 미설치 | `mcp_toolkit` 패키지 확인 |

### Hot Reload 실패

| 증상 | 원인 | 해결 |
|------|------|------|
| 변경 미반영 | 상태 보존 문제 | hot_restart_flutter 사용 |
| 컴파일 에러 | 문법 오류 | 에러 메시지 확인 후 수정 |

### 도구 실행 에러

| 증상 | 원인 | 해결 |
|------|------|------|
| BLoC 찾을 수 없음 | 등록 안 됨 | bloc_get_all로 목록 확인 |
| 폼 상태 없음 | 화면 이동됨 | 해당 화면에서 다시 실행 |

---

## Performance Considerations

### 도구 호출 최적화

- **배치 호출**: 관련 도구들을 순차적으로 호출
- **캐싱**: 동일한 정보 반복 요청 피하기
- **필터링**: limit 파라미터 활용하여 데이터량 제한

### 리소스 사용량

- 스크린샷은 메모리 사용량이 높음
- 위젯 트리 깊이가 깊으면 응답 시간 증가
- 로그가 많으면 검색 시간 증가

---

## Platform Considerations

### iOS
- Impeller 기본 사용
- 성능 프로파일링에 유리

### Android
- Skia/Impeller 혼합
- OpenGLES 관련 이슈 주의

### Web
- VM Service 제한적
- 일부 도구 사용 불가

---

## External Resources

- [Flutter DevTools](https://docs.flutter.dev/tools/devtools)
- [MCP Toolkit Package](https://pub.dev/packages/mcp_toolkit)
- [Dart VM Service Protocol](https://github.com/dart-lang/sdk/blob/main/runtime/vm/service.md)

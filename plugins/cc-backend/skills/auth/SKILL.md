---
name: auth
description: Serverpod 인증 모듈 구현
---

# Serverpod 인증 모듈

serverpod_auth_idp 기반 인증 설정. Token Manager, Identity Provider, Flutter UI 통합을 다룹니다.

## 트리거

- 인증/로그인 기능 추가
- IDP (Email, Google, Apple 등) 설정
- JWT/세션 토큰 관리
- Flutter 로그인 UI 구현

## 의존성 설정

### Server `pubspec.yaml`

```yaml
dependencies:
  serverpod: 3.3.1
  serverpod_auth_idp_server: 3.3.1
```

### Client `pubspec.yaml`

```yaml
dependencies:
  serverpod_client: 3.3.1
  serverpod_auth_idp_client: 3.3.1
```

### Flutter `pubspec.yaml`

```yaml
dependencies:
  serverpod_flutter: 3.3.1
  serverpod_auth_idp_flutter: 3.3.1
  # 선택적 프로바이더:
  # serverpod_auth_idp_flutter_facebook: 3.3.1
  # serverpod_auth_idp_flutter_firebase: 3.3.1
```

`dart pub get` 후 `serverpod generate` 실행.

## Provider 엔드포인트 노출

각 프로바이더별 엔드포인트 클래스 생성:

```dart
// lib/src/auth/email_idp_endpoint.dart
import 'package:serverpod_auth_idp_server/providers/email.dart';

class EmailIdpEndpoint extends EmailIdpBaseEndpoint {}
```

지원 프로바이더:

| 프로바이더 | Base 클래스 | Import |
|-----------|------------|--------|
| Email | `EmailIdpBaseEndpoint` | `providers/email.dart` |
| Google | `GoogleIdpBaseEndpoint` | `providers/google.dart` |
| Apple | `AppleIdpBaseEndpoint` | `providers/apple.dart` |
| GitHub | `GitHubIdpBaseEndpoint` | `providers/github.dart` |
| Facebook | `FacebookIdpBaseEndpoint` | `providers/facebook.dart` |
| Microsoft | `MicrosoftIdpBaseEndpoint` | `providers/microsoft.dart` |
| Passkey | `PasskeyIdpBaseEndpoint` | `providers/passkey.dart` |
| Firebase | `FirebaseIdpBaseEndpoint` | `providers/firebase.dart` |

## Auth 서비스 초기화

```dart
import 'package:serverpod/serverpod.dart';
import 'package:serverpod_auth_idp_server/core.dart';
import 'package:serverpod_auth_idp_server/providers/email.dart';

void run(List<String> args) async {
  final pod = Serverpod(args, Protocol(), Endpoints());

  pod.initializeAuthServices(
    tokenManagerBuilders: [
      JwtConfigFromPasswords(),
    ],
    identityProviderBuilders: [
      EmailIdpConfigFromPasswords(
        sendRegistrationVerificationCode: _sendRegistrationCode,
        sendPasswordResetVerificationCode: _sendPasswordResetCode,
      ),
    ],
  );

  await pod.start();
}
```

### 프로덕션 설정

```dart
final jwtConfig = JwtConfig(
  refreshTokenHashPepper: pod.getPassword('jwtRefreshTokenHashPepper')!,
  algorithm: JwtAlgorithm.hmacSha512(
    SecretKey(pod.getPassword('jwtHmacSha512PrivateKey')!)),
);

final emailConfig = EmailIdpConfig(
  secretHashPepper: pod.getPassword('emailSecretHashPepper')!,
  sendRegistrationVerificationCode: _sendRegistrationCode,
  sendPasswordResetVerificationCode: _sendPasswordResetCode,
);

pod.initializeAuthServices(
  tokenManagerBuilders: [jwtConfig],
  identityProviderBuilders: [emailConfig],
);
```

키는 `config/passwords.yaml`에 보관. Serverpod Cloud 배포 시 자동 관리.

## Token Manager

| 타입 | 설정 | 특성 |
|------|------|------|
| JWT | `JwtConfigFromPasswords()` | Stateless, 빠름 |
| Server-side Sessions | `ServerSideSessionsConfig(sessionKeyHashPepper: ...)` | Revocable, 보안 강화 |

두 가지를 동시에 사용 가능.

## Apple Sign In 추가 설정

```dart
pod.configureAppleIdpRoutes(
  revokedNotificationRoutePath: '/hooks/apple-notification',
  webAuthenticationCallbackRoutePath: '/auth/callback',
);
```

## Flutter 클라이언트 설정

```dart
import 'package:serverpod_flutter/serverpod_flutter.dart';
import 'package:serverpod_auth_idp_flutter/serverpod_auth_idp_flutter.dart';

client = Client(serverUrl)
  ..connectivityMonitor = FlutterConnectivityMonitor()
  ..authSessionManager = FlutterAuthSessionManager();

client.auth.initialize();
```

## Flutter 로그인 UI

```dart
SignInScreen(
  child: YourHomeScreen(
    onSignOut: () async {
      await client.auth.signOutDevice();
    },
  ),
)
```

### 인증 상태 리스닝

```dart
class _SignInScreenState extends State<SignInScreen> {
  bool _isSignedIn = false;

  @override
  void initState() {
    super.initState();
    client.auth.authInfoListenable.addListener(_updateSignedInState);
    _isSignedIn = client.auth.isAuthenticated;
  }

  void _updateSignedInState() {
    setState(() {
      _isSignedIn = client.auth.isAuthenticated;
    });
  }

  @override
  Widget build(BuildContext context) {
    return _isSignedIn
        ? widget.child
        : Center(child: SignInWidget(client: client, onAuthenticated: () {}));
  }
}
```

## Generator 닉네임 (선택)

`config/generator.yaml`에서:

```yaml
modules:
  serverpod_auth_idp:
    nickname: auth
```

모델에서 `module:auth:AuthUser`로 참조 가능.

## 마이그레이션

```bash
serverpod generate
serverpod create-migration
# 서버 시작 시 적용
```

## 체크리스트

- [ ] 서버/클라이언트/Flutter 의존성 추가
- [ ] IDP 엔드포인트 클래스 생성
- [ ] `initializeAuthServices` 호출
- [ ] `passwords.yaml`에 키 설정
- [ ] Flutter `auth.initialize()` 호출
- [ ] 이메일 전송 함수 구현 (프로덕션)
- [ ] 마이그레이션 생성/적용

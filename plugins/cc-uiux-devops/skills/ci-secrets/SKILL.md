---
name: ci-secrets
description: CI/CD 시크릿 인코딩, GitHub Secrets 등록, CI 워크플로우 디코딩 관리
---

# CI/CD Secrets Management

## 트리거

- 키스토어, Firebase 서비스 키, Fastlane 설정 파일이 변경되었을 때
- 새 환경(dev/staging/production)의 시크릿을 추가할 때
- GitHub Actions 워크플로우에서 시크릿을 사용하는 단계를 작성할 때
- `make encode_keystore` 또는 `make github_secrets` 실행 시 오류가 발생할 때

## 전체 흐름

```
로컬 민감 파일 → make encode_keystore → .envrc (base64 인코딩)
                                           ↓ direnv allow
                                    환경변수로 로드
                                           ↓
                               make github_secrets
                                           ↓ gh secret set
                               GitHub Actions Secrets
                                           ↓
                               CI 워크플로우에서 디코딩
                                           ↓ base64 -d / tar -xzf
                               빌드 환경에 파일 복원
```

## 동작

### 1. 인코딩 (로컬 → .envrc)

민감 파일을 base64로 인코딩하여 `.envrc` 환경변수에 저장한다. `make encode_keystore` 타겟이 이 작업을 수행한다.

#### 단일 파일 인코딩

```bash
# 키스토어, JSON 파일 등
base64 -i <파일경로>
# 예: base64 -i android/keystore/release.keystore
```

결과를 `.envrc`에 `export VAR_NAME="<base64>"` 형식으로 저장한다.

#### 디렉토리 인코딩 (tar.gz → base64)

```bash
# fastlane, deploy scripts 등 디렉토리
tar -czf archive.tar.gz -C <parent_dir> --exclude="<불필요파일>" <target_dir>
base64 -i archive.tar.gz | tr -d '\n'
rm -f archive.tar.gz
```

#### .envrc 업데이트 패턴

기존 값이 있으면 `sed`로 교체하고, 없으면 `echo >>` 로 추가한다:

```makefile
@if grep -q "VAR_NAME" .envrc; then \
    sed -i.bak "s|^export VAR_NAME=.*|export VAR_NAME=\"$$ENCODED\"|" .envrc; \
else \
    echo "export VAR_NAME=\"$$ENCODED\"" >> .envrc; \
fi
```

인코딩 완료 후 `direnv allow`로 환경변수를 로드한다.

### 2. GitHub Secrets 등록 (환경변수 → GitHub)

`make github_secrets`가 `.envrc`에서 로드된 환경변수를 `gh secret set`으로 GitHub에 등록한다.

```bash
# 단일 시크릿 등록
gh secret set SECRET_NAME --body "$VALUE" --repo <org>/<repo>

# 파일 내용 직접 등록 (환경변수 파일 등)
gh secret set ENV_STAGING --body "$(cat shared/config/.env.staging)" --repo <org>/<repo>
```

헬퍼 함수 패턴:

```bash
set_secret() {
  name="$1"; val="$2"
  if [ -n "$val" ]; then
    gh secret set "$name" --body "$val" --repo $REPO_PATH
    echo "set $name"
  else
    echo "skip $name (empty)"
  fi
}
```

### 3. CI 디코딩 (GitHub Secrets → 빌드 파일)

#### 단일 파일: `timheuer/base64-to-file` 액션

```yaml
- name: Decode Android keystore
  uses: timheuer/base64-to-file@v1.2
  with:
    fileName: release.keystore
    fileDir: app/kobic/android/keystore/
    encodedString: ${{ secrets.ANDROID_RELEASE_KEY_BASE64 }}
```

#### 디렉토리: base64 디코딩 + tar 추출

```yaml
- name: Decode fastlane directory
  env:
    FASTLANE_ANDROID_BASE64: ${{ secrets.FASTLANE_ANDROID_BASE64 }}
  run: |
    echo "$FASTLANE_ANDROID_BASE64" | base64 -d > android/fastlane.tar.gz
    mkdir -p android/fastlane
    tar -xzf android/fastlane.tar.gz -C android/fastlane --strip-components=1
    rm -f android/fastlane.tar.gz
```

## 시크릿 카테고리

### Android Keystore (2개)

| 시크릿명 | 인코딩 방식 | 원본 파일 |
|---------|------------|----------|
| `ANDROID_RELEASE_KEY_BASE64` | base64 (파일) | `android/keystore/release.keystore` |
| `ANDROID_KEY_PROPERTIES_BASE64` | base64 (파일) | `android/key.properties` |

### iOS / App Store (2개)

| 시크릿명 | 인코딩 방식 | 원본 파일 |
|---------|------------|----------|
| `APPSTORE_CONNECT_API_KEY_BASE64` | base64 (파일) | `ios/fastlane/appstore_connect_api_key.json` |
| `FASTLANE_IOS_BASE64` | tar.gz -> base64 | `ios/fastlane/` (metadata, screenshots, scripts 제외) |

### Firebase App Distribution (3개)

| 시크릿명 | 인코딩 방식 | 원본 파일 |
|---------|------------|----------|
| `FIREBASE_DEV_APP_DISTRIBUTION_CREDENTIALS_BASE64` | base64 | `android/keystore/development.json` |
| `FIREBASE_STG_APP_DISTRIBUTION_CREDENTIALS_BASE64` | base64 | `android/keystore/staging.json` |
| `FIREBASE_PROD_APP_DISTRIBUTION_CREDENTIALS_BASE64` | base64 | `android/keystore/production.json` |

### Firebase Admin SDK (3개)

| 시크릿명 | 인코딩 방식 | 원본 파일 |
|---------|------------|----------|
| `FIREBASE_DEV_CREDENTIALS_BASE64` | base64 | `backend/.../firebase_admin/development.json` |
| `FIREBASE_STG_CREDENTIALS_BASE64` | base64 | `backend/.../firebase_admin/staging.json` |
| `FIREBASE_PROD_CREDENTIALS_BASE64` | base64 | `backend/.../firebase_admin/production.json` |

### Firebase App IDs (~33개)

환경(dev/stg/prod) x 플랫폼(android, android_console, ios, ios_console, web, macos, macos_console, windows, windows_console, console, widgetbook) 조합:

| 패턴 | 예시 |
|------|------|
| `FIREBASE_{ENV}_{PLATFORM}_ID` | `FIREBASE_DEV_ANDROID_ID`, `FIREBASE_STG_WEB_ID` |

값은 `.envrc`에 직접 설정 (base64 인코딩 아님).

### Fastlane (2개)

| 시크릿명 | 인코딩 방식 | 원본 |
|---------|------------|------|
| `FASTLANE_ANDROID_BASE64` | tar.gz -> base64 | `android/fastlane/` (metadata, scripts 제외) |
| `FASTLANE_IOS_BASE64` | tar.gz -> base64 | `ios/fastlane/` (metadata, screenshots, scripts 제외) |

### AWS Deploy (1개)

| 시크릿명 | 인코딩 방식 | 원본 |
|---------|------------|------|
| `AWS_DEPLOY_SCRIPTS_BASE64` | tar.gz -> base64 | `backend/.../deploy/aws/scripts/` |

### Serverpod (1개)

| 시크릿명 | 인코딩 방식 | 원본 파일 |
|---------|------------|----------|
| `SERVERPOD_PASSWORDS` | base64 | `backend/.../config/passwords.yaml` |

### Environment Files (2개)

| 시크릿명 | 인코딩 방식 | 원본 파일 |
|---------|------------|----------|
| `ENV_STAGING` | 직접 값 (cat) | `shared/config/.env.staging` |
| `ENV_PRODUCTION` | 직접 값 (cat) | `shared/config/.env.production` |

### Match (iOS Signing) (3개)

| 시크릿명 | 인코딩 방식 |
|---------|------------|
| `MATCH_KEYCHAIN_NAME` | 직접 값 |
| `MATCH_KEYCHAIN_PASSWORD` | 직접 값 |
| `MATCH_GIT_BASIC_AUTHORIZATION_BASE64` | 직접 값 |

### 기타 (1개)

| 시크릿명 | 인코딩 방식 |
|---------|------------|
| `RELEASE_STORE_PASSWORD` | 직접 값 |

## 출력

- `.envrc` 파일에 base64 인코딩된 시크릿 환경변수 저장
- GitHub Actions Secrets에 등록 완료
- CI 워크플로우에서 디코딩하여 빌드 파일 복원

## 전제 조건

- `direnv` 설치 및 설정: `.envrc` 환경변수 자동 로드
- `gh` (GitHub CLI) 설치 및 인증: `gh auth login`
- 원본 민감 파일이 로컬에 존재해야 함 (`.gitignore`에 포함)

## 새 시크릿 추가 시

1. `Makefile`의 `encode_keystore` 타겟에 인코딩 로직 추가
2. `Makefile`의 `github_secrets` 타겟에 `set_secret` 호출 추가
3. CI 워크플로우에 디코딩 단계 추가
4. `.gitignore`에 원본 파일 경로 포함 확인

## 참고

- `.envrc`는 `.gitignore`에 포함되어 절대 커밋되지 않아야 한다
- `direnv allow` 실행 후 환경변수가 셸에 로드된다
- `gh secret set`은 기존 값을 덮어쓴다 (upsert 동작)
- Firebase App ID는 공개 값이지만, 일관성을 위해 시크릿으로 관리한다
- tar.gz 인코딩 시 metadata/screenshots 등 불필요한 대용량 파일은 `--exclude`로 제외한다

# Incremental Build (증분 빌드) 규칙

로컬 개발 환경에서 변경된 패키지만 빌드하여 시간을 절약하는 증분 빌드 시스템 가이드입니다.

## 개요

| 시나리오 | 전체 빌드 | 증분 빌드 | 절약 |
|---------|----------|----------|------|
| 단일 feature 변경 | 60분+ | 5-10분 | ~85% |
| shared 패키지 변경 | 60분+ | 20-30분 | ~50% |
| 변경 없음 | 10분+ | 즉시 | ~99% |

### 레벨별 병렬 빌드

증분 빌드는 **같은 우선순위 레벨의 패키지들을 병렬로 빌드**하여 성능을 최적화합니다.

```
레벨 [1]: shared/* (4개) ─────────┬─ 병렬 실행
                                  ↓ 레벨 1 완료
레벨 [3]: package/* (8개) ────────┬─ 병렬 실행
                                  ↓ 레벨 3 완료
레벨 [4]: feature/common/* (6개) ─┬─ 병렬 실행
                                  ↓ 레벨 4 완료
레벨 [5]: feature/application/*  ─┬─ 병렬 실행
                                  ↓ 레벨 5 완료
레벨 [7]: app/* (1개) ────────────┴─ 빌드
```

**병렬 동시성 제어**:
```bash
# 동시 빌드 수 설정 (기본: 4)
BUILD_CONCURRENCY=6 melos run build:incremental

# 저사양 환경에서는 1로 제한
BUILD_CONCURRENCY=1 melos run build:incremental:low-resources
```

---

## Melos 명령어

### 기본 명령어

```bash
# 변경된 패키지 + 역 의존 패키지만 증분 빌드
melos run build:incremental

# 빌드 없이 변경된 패키지만 확인
melos run build:incremental:dry-run

# 빌드 상태 확인
melos run build:incremental:status
```

### 고급 명령어

| 명령어 | 설명 | 사용 시나리오 |
|--------|------|--------------|
| `build:incremental:force` | 캐시 초기화 후 빌드 | 캐시 문제 발생 시 |
| `build:incremental:low-resources` | 메모리 절약 모드 | CI 환경, 저사양 PC |
| `build:incremental:clean` | build_runner clean 후 빌드 | 생성 파일 충돌 시 |
| `build:incremental:verbose` | 상세 로그 출력 | 디버깅 시 |
| `build:incremental:reset` | 캐시만 삭제 | 새로 시작 시 |
| `build:sync-from-ci` | CI 캐시를 로컬로 동기화 | 스쿼시 머지 후 |
| `build:sync-from-ci:dry-run` | CI 캐시 동기화 미리보기 | 다운로드 전 확인 |

---

## CI 캐시 동기화

CI 빌드의 캐시를 로컬로 동기화하여 스쿼시 머지 후에도 정확한 증분 빌드가 가능합니다.

### 사용 시나리오

```
PR 브랜치:  A → B → C  (last-commit.sha = C)
                ↓ squash merge
main:       X → D      (D는 새로운 SHA, C는 orphan)
```

스쿼시 머지 후 로컬에서 main을 pull하면, 저장된 커밋 SHA(C)가 더 이상 존재하지 않아
Git diff가 실패할 수 있습니다. 이때 해시 기반 폴백이 자동으로 동작합니다.

### 명령어

```bash
# CI 캐시를 로컬로 동기화
melos run build:sync-from-ci

# 동기화 미리보기 (다운로드 없이)
melos run build:sync-from-ci:dry-run
```

### 전제 조건

- GitHub CLI (`gh`) 설치 필요: `brew install gh`
- GitHub 인증 필요: `gh auth login`

### 동작 방식

1. GitHub Actions 아티팩트에서 `build-metadata` 다운로드
2. `.build-state/` 디렉토리에 해시 파일 복사
3. 다음 증분 빌드에서 정확한 변경 감지 가능

---

## 변경 감지 모드

### Auto 모드 (기본)

```bash
# 자동으로 최적 모드 선택
melos run build:incremental
```

Git 저장소 내부면 Git 기반, 외부면 해시 기반 자동 선택.

**스쿼시 머지 대응**: 저장된 커밋이 orphan일 경우 자동으로 해시 기반 감지로 폴백합니다.

### Git 모드

```bash
# Git diff 기반 변경 감지
scripts/local_incremental_build.sh --mode=git
```

- 마지막 빌드 커밋과 현재 HEAD 비교
- 작업 디렉토리 변경사항 포함
- staged/unstaged 파일 모두 감지

### Time/Hash 모드

```bash
# 파일 해시 기반 변경 감지
scripts/local_incremental_build.sh --mode=time
```

- 소스 파일 SHA-256 해시 비교
- 생성 파일(`.g.dart`, `.freezed.dart` 등) 자동 제외
- Git 없이도 동작

---

## 환경변수

| 환경변수 | 기본값 | 설명 |
|---------|--------|------|
| `BUILD_RUNNER_OPTS` | `-d` | build_runner 추가 옵션 |
| `BUILD_CONCURRENCY` | `4` | 레벨별 병렬 빌드 동시성 |

### 사용 예시

```bash
# 삭제 옵션 없이 빌드
BUILD_RUNNER_OPTS="" melos run build:incremental

# low-resources 모드로 빌드
BUILD_RUNNER_OPTS="--low-resources-mode -d" melos run build:incremental
```

---

## 빌드 우선순위

증분 빌드는 의존성 순서대로 빌드합니다:

| 우선순위 | 경로 패턴 | 예시 |
|----------|----------|------|
| 1 | `shared/*` | config, dependencies, flavor |
| 2 | `package/life*`, `package/auth*` | 인증 관련 |
| 3 | `package/*` | core, resources, coui |
| 4 | `feature/common/*` | auth, settings, splash |
| 5 | `feature/application/*`, `feature/console/*` | 기능 모듈 |
| 6 | `backend/*` | (해당 없음) |
| 7 | `app/*` | good_teacher, widgetbook |

---

## 캐시 구조

### 저장 위치

```
.build-state/
├── last-commit.sha        # 마지막 빌드 커밋 SHA
├── last-build.timestamp   # 마지막 빌드 시간
├── package-feature_console_console_sales_analysis.hash
├── package-package_core.hash
└── ...
```

### 캐시 파일 형식

- 파일명: `package-{경로_슬래시를_언더스코어로}.hash`
- 내용: 소스 파일들의 SHA-256 해시

### 캐시 무효화 조건

1. 소스 파일 수정 (`.dart` 파일)
2. `pubspec.yaml` 수정
3. `--force` 옵션 사용
4. `.build-state/` 디렉토리 삭제

---

## 트러블슈팅

### 캐시 문제

```bash
# 캐시 완전 초기화
melos run build:incremental:reset

# 강제 재빌드
melos run build:incremental:force
```

### 변경 감지 실패

```bash
# 상세 로그로 확인
melos run build:incremental:verbose

# 직접 스크립트 실행
scripts/detect_local_changes.sh --verbose --mode=time
```

### 메모리 부족

```bash
# 저사양 모드 사용
melos run build:incremental:low-resources

# 또는 환경변수로 설정
BUILD_RUNNER_OPTS="--low-resources-mode" melos run build:incremental
```

### 특정 패키지만 빌드

```bash
# 증분 빌드 대신 직접 지정
melos exec --scope=console_sales_analysis -- dart run build_runner build -d
```

---

## 스크립트 구조

### 로컬 스크립트

| 파일 | 역할 |
|------|------|
| `scripts/detect_local_changes.sh` | 변경 패키지 감지 |
| `scripts/local_incremental_build.sh` | 로컬 빌드 오케스트레이터 |
| `scripts/sync_cache_from_ci.sh` | CI 캐시 로컬 동기화 |

### CI 스크립트

| 파일 | 역할 |
|------|------|
| `.github/scripts/detect_changes.sh` | CI용 변경 감지 |
| `.github/scripts/smart_incremental_build.sh` | CI용 증분 빌드 (공용) |

### 스크립트 관계

```
┌─────────────────────────────────────────────────┐
│ melos run build:incremental                      │
└───────────────────┬─────────────────────────────┘
                    ▼
┌─────────────────────────────────────────────────┐
│ scripts/local_incremental_build.sh               │
│ - 옵션 파싱 (--dry-run, --force, --low-resources)│
│ - 변경 감지 호출                                  │
│ - CI 스크립트 재사용                              │
└───────────────────┬─────────────────────────────┘
         ┌──────────┴──────────┐
         ▼                     ▼
┌─────────────────┐  ┌─────────────────────────────┐
│ detect_local_   │  │ .github/scripts/            │
│ changes.sh      │  │ smart_incremental_build.sh  │
│ (변경 감지)      │  │ (실제 빌드 실행)             │
└─────────────────┘  └─────────────────────────────┘
```

---

## 스쿼시 머지 대응

### 문제점

PR을 스쿼시 머지하면 원래 커밋들이 새로운 단일 커밋으로 대체됩니다.
이때 `.build-state/last-commit.sha`에 저장된 커밋이 orphan이 되어 Git diff가 실패합니다.

### 해결 방식

1. **자동 폴백**: Git diff 실패 시 컨텐츠 해시 기반 감지로 자동 전환
2. **CI 동기화**: `build:sync-from-ci`로 CI 캐시 다운로드하여 정확도 향상

### 권장 워크플로우

```bash
# 스쿼시 머지 후
git checkout main
git pull

# 옵션 1: 자동 폴백 활용 (해시 기반)
melos run build:incremental

# 옵션 2: CI 캐시 동기화 후 빌드 (더 정확)
melos run build:sync-from-ci
melos run build:incremental
```

---

## 참고 사항

- `.build-state/` 디렉토리는 `.gitignore`에 포함되어 있음
- CI에서는 별도의 캐시 전략 사용 (4계층 캐시)
- `jq` 설치 시 역 의존성 분석 기능 활성화
- CI 빌드 메타데이터는 7일간 아티팩트로 보관됨

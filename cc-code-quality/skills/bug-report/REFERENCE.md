# Bug Report Reference Guide

버그 분류 체계, 심각도 가이드, 이미지 분석 기준을 정의합니다.

---

## 1. 심각도 분류 (Severity)

### 분류 기준

| 심각도 | 레이블 | 아이콘 | 설명 | 예시 |
|--------|--------|--------|------|------|
| Critical | `severity:critical` | 🔴 | 앱 사용 불가, 데이터 손실 | 앱 크래시, ANR, 데이터 유실 |
| High | `severity:high` | 🟠 | 핵심 기능 불가 | 로그인 실패, 결제 오류, 주요 화면 진입 불가 |
| Medium | `severity:medium` | 🟡 | 기능 제한적 동작 | 버튼 미동작, 일부 UI 깨짐, 데이터 미표시 |
| Low | `severity:low` | 🟢 | 사소한 문제 | 오타, 정렬 오류, 색상 오류 |

### 심각도 결정 플로우

```
앱이 크래시되거나 데이터가 손실되나요?
├── Yes → 🔴 Critical
└── No → 핵심 기능(로그인, 결제, 메인 플로우)이 불가능한가요?
         ├── Yes → 🟠 High
         └── No → 기능이 의도대로 동작하지 않나요?
                  ├── Yes → 🟡 Medium
                  └── No → 🟢 Low (시각적/표면적 문제)
```

---

## 2. 버그 유형 분류 (Type)

### UI/UX 버그 🎨

| 하위 유형 | 설명 | 예시 |
|----------|------|------|
| Layout | 레이아웃 깨짐 | 오버플로우, 겹침, 정렬 오류 |
| Style | 스타일 오류 | 색상, 폰트, 여백 오류 |
| Animation | 애니메이션 문제 | 버벅임, 미동작, 잘림 |
| Responsive | 반응형 문제 | 화면 크기별 깨짐 |

### 기능 버그 ⚙️

| 하위 유형 | 설명 | 예시 |
|----------|------|------|
| Navigation | 네비게이션 오류 | 잘못된 화면 이동, 뒤로가기 오류 |
| Input | 입력 처리 오류 | 키보드 입력, 터치 미인식 |
| Logic | 로직 오류 | 잘못된 계산, 조건 분기 오류 |
| State | 상태 관리 오류 | 상태 미갱신, 동기화 문제 |

### 성능 버그 ⚡

| 하위 유형 | 설명 | 예시 |
|----------|------|------|
| Loading | 로딩 지연 | 느린 API 응답, 대용량 데이터 |
| Rendering | 렌더링 성능 | 프레임 드롭, 버벅임 |
| Memory | 메모리 문제 | 메모리 누수, OOM |
| Battery | 배터리 소모 | 백그라운드 과다 작업 |

### 크래시/ANR 💥

| 하위 유형 | 설명 | 예시 |
|----------|------|------|
| Crash | 앱 강제 종료 | NPE, 미처리 예외 |
| ANR | 응답 없음 | 메인 스레드 블로킹 |
| Freeze | 화면 멈춤 | 무한 루프, 데드락 |

### 데이터 버그 📊

| 하위 유형 | 설명 | 예시 |
|----------|------|------|
| Display | 잘못된 표시 | 데이터 미표시, 잘못된 값 |
| Sync | 동기화 오류 | 서버-클라이언트 불일치 |
| Persistence | 저장 오류 | 로컬 저장 실패, 캐시 오류 |
| Validation | 검증 오류 | 잘못된 입력 허용 |

---

## 3. 영향 영역 분류 (Area)

### 영역 라벨

| 영역 | 레이블 | 설명 |
|------|--------|------|
| UI | `area:ui` | 프론트엔드 UI 컴포넌트 |
| Backend | `area:backend` | 서버 API, 엔드포인트 |
| Data | `area:data` | 데이터 레이어, 캐시 |
| Auth | `area:auth` | 인증/인가 |
| Payment | `area:payment` | 결제 관련 |
| Navigation | `area:navigation` | 라우팅, 네비게이션 |

---

## 4. 이미지 분석 가이드

### 분석 포인트

스크린샷 분석 시 확인할 항목:

```markdown
## 이미지 분석 체크리스트

### UI 상태
- [ ] 에러 다이얼로그가 표시되어 있는가?
- [ ] 빈 화면(Empty State)인가?
- [ ] 로딩 상태가 멈춰 있는가?
- [ ] 레이아웃이 깨져 있는가?
- [ ] 오버플로우가 발생했는가?

### 텍스트 추출
- [ ] 에러 메시지 텍스트
- [ ] 화면 타이틀/헤더
- [ ] 버튼 텍스트
- [ ] 입력 필드 내용

### 컨텍스트 파악
- [ ] 어떤 화면인가? (목록, 상세, 폼 등)
- [ ] 어떤 액션 후 발생했는가?
- [ ] 어떤 데이터가 관련되어 있는가?
```

### 자동 분류 로직

```markdown
## 이미지 기반 자동 분류

### 크래시/ANR 감지
- "앱이 응답하지 않습니다" → 💥 ANR
- "강제 종료" / "crash" → 💥 Crash
- 검은 화면 + 에러 스택 → 💥 Crash

### UI 버그 감지
- 텍스트 잘림 / "..." → 🎨 Layout
- 겹쳐진 요소 → 🎨 Layout
- 노란색 영역 (Flutter overflow) → 🎨 Layout

### 기능 버그 감지
- 에러 토스트/스낵바 → ⚙️ Function
- 빈 목록 + 에러 아이콘 → ⚙️ Data/Function
- 로딩 스피너 지속 → ⚙️ Function / ⚡ Performance
```

---

## 5. 필수 정보 수집

### 재현 단계 작성 가이드

```gherkin
# 좋은 예
Given 사용자가 로그인된 상태에서
And 홈 화면에 있을 때
When "프로필" 탭을 탭하면
Then 앱이 크래시됨

# 나쁜 예
프로필 가면 크래시됨
```

### 환경 정보 체크리스트

```markdown
## 필수 환경 정보

| 항목 | 설명 | 예시 |
|------|------|------|
| OS | 운영체제 버전 | iOS 17.2, Android 14 |
| Device | 디바이스 모델 | iPhone 15, Galaxy S24 |
| App Version | 앱 버전 | 1.2.3 (build 456) |
| Account | 테스트 계정 (선택) | test@example.com |
| Network | 네트워크 상태 (선택) | WiFi, LTE, Offline |
```

---

## 6. 자동 라벨링 규칙

### 기본 라벨

모든 버그 이슈에 자동 적용:
- `bug`

### 조건부 라벨

| 조건 | 라벨 |
|------|------|
| 심각도 Critical | `severity:critical`, `priority:urgent` |
| 심각도 High | `severity:high`, `priority:high` |
| 크래시 관련 | `crash`, `needs-investigation` |
| UI 관련 | `area:ui` |
| 재현 불확실 | `needs-reproduction` |

### 자동 파이프라인

| 심각도 | 파이프라인 |
|--------|-----------|
| Critical | In Progress (즉시 처리) |
| High | Triage (우선 분류) |
| Medium/Low | Backlog |

---

## 7. 추가 정보 포맷

### 로그 첨부 형식

```markdown
## 로그

\`\`\`
2024-01-15 10:30:45.123 E/Flutter: Error in authentication flow
2024-01-15 10:30:45.124 E/Flutter: Stack trace:
#0      AuthBloc._onLogin (auth_bloc.dart:45)
#1      Bloc.on.<anonymous closure> (bloc.dart:123)
\`\`\`
```

### 스택트레이스 첨부 형식

```markdown
## 스택트레이스

\`\`\`dart
Exception: Network error
  at ApiClient.fetch (api_client.dart:78)
  at UserRepository.getUser (user_repository.dart:34)
  at GetUserUseCase.call (get_user_usecase.dart:22)
\`\`\`
```

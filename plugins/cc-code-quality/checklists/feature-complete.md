# Feature Complete Checklist

Feature 개발 완료 전 확인해야 할 체크리스트입니다.

## 사용법

```
@checklist:feature-complete [feature_name]
```

---

## 1. 📁 구조 검증

### Domain Layer
- [ ] Entity 정의 완료 (Freezed)
- [ ] Repository Interface 정의 (I prefix)
- [ ] UseCase 구현 완료
- [ ] Failure 클래스 정의
- [ ] 단위 테스트 작성

### Data Layer
- [ ] Repository 구현체 완료
- [ ] Serverpod Mixin 구현 (필요시)
- [ ] Local Database 구현 (필요시)
- [ ] DTO ↔ Entity 매퍼 구현
- [ ] 캐싱 전략 적용 (SWR/Cache-First)

### Presentation Layer
- [ ] Page 위젯 구현
- [ ] 재사용 Widget 분리
- [ ] BLoC/Cubit 구현
- [ ] Event/State 정의 (Freezed)
- [ ] Widget 테스트 작성

### DI & Routing
- [ ] Injectable 어노테이션 추가
- [ ] Route 정의 (Auto_route)
- [ ] Route Guard 적용 (필요시)

---

## 2. 🔧 코드 생성

```bash
# Feature 패키지 빌드
melos run generate:{feature_name}

# 또는 전체 빌드
melos run build
```

- [ ] Freezed 코드 생성됨 (*.freezed.dart)
- [ ] Injectable 코드 생성됨 (*.g.dart)
- [ ] Route 코드 생성됨
- [ ] 빌드 에러 없음

---

## 3. 🧪 테스트

### 단위 테스트
- [ ] UseCase 테스트
  - Happy path 테스트
  - Error case 테스트
  - Edge case 테스트
- [ ] Repository 테스트 (mocked data source)

### BLoC 테스트
- [ ] 초기 상태 테스트
- [ ] 이벤트 → 상태 변화 테스트
- [ ] 에러 처리 테스트
- [ ] 연속 이벤트 테스트

### Widget 테스트
- [ ] 렌더링 테스트
- [ ] 인터랙션 테스트
- [ ] 상태별 UI 테스트

### 실행 확인
```bash
# Feature 테스트 실행
flutter test feature/{type}/{feature_name}/test/

# 커버리지 확인
melos run test:with-html-coverage
```

- [ ] 모든 테스트 통과
- [ ] 커버리지 80% 이상

---

## 4. 📝 문서화

### 코드 문서
- [ ] 공개 API에 dartdoc 주석
- [ ] 복잡한 로직에 설명 주석
- [ ] TODO 주석 해결 또는 이슈 등록

### Feature 문서
- [ ] README.md 업데이트 (필요시)
- [ ] API 변경사항 문서화
- [ ] Breaking Changes 명시

---

## 5. 🌐 국제화

- [ ] 모든 UI 텍스트 번역 키 사용
- [ ] 번역 파일 업데이트
  ```bash
  melos run generate:locale
  ```
- [ ] 복수형/파라미터 처리 확인
- [ ] 모든 지원 언어 번역 완료

---

## 6. ⚡ 성능 최적화

### UI 성능
- [ ] const 위젯 활용
- [ ] BlocBuilder buildWhen 적용
- [ ] ListView.builder 사용 (긴 리스트)
- [ ] 이미지 cacheWidth/cacheHeight 적용

### 데이터 성능
- [ ] 적절한 캐싱 전략
- [ ] 페이지네이션 적용 (필요시)
- [ ] 불필요한 API 호출 제거

### 메모리 관리
- [ ] dispose에서 리소스 해제
- [ ] Stream subscription 취소
- [ ] Controller dispose

---

## 7. 🔒 보안 검토

- [ ] 민감 정보 하드코딩 없음
- [ ] 입력 값 검증 적용
- [ ] 적절한 에러 메시지 (정보 노출 방지)
- [ ] 인증/인가 적용 (필요시)

---

## 8. ♿ 접근성

- [ ] Semantics label 적용
- [ ] 터치 타겟 크기 확인 (48x48 이상)
- [ ] 색상 대비 확인
- [ ] 스크린 리더 테스트

---

## 9. 🔍 정적 분석

```bash
# Lint 검사
melos run analyze

# 포맷팅 검사
melos run format
```

- [ ] Lint 경고 없음
- [ ] 코드 포맷팅 완료

---

## 10. 🚀 통합 검증

### 로컬 테스트
- [ ] 개발 환경에서 정상 동작
- [ ] 에러 케이스 시나리오 테스트
- [ ] 네트워크 오프라인 테스트

### 빌드 검증
```bash
# iOS 빌드
flutter build ios --flavor development

# Android 빌드
flutter build apk --flavor development
```

- [ ] iOS 빌드 성공
- [ ] Android 빌드 성공

---

## 11. 📋 PR 준비

- [ ] 의미 있는 커밋 메시지 (한글, Conventional + Gitmoji)
- [ ] 관련 이슈 연결
- [ ] 리뷰어 지정
- [ ] 라벨 추가

### 커밋 메시지 예시
```
feat(home): ✨ 사용자 프로필 기능 추가

- 프로필 조회/수정 UseCase 구현
- ProfileBloc 상태 관리
- 프로필 편집 UI 구현

Closes #123
```

---

## 완료 확인

| 항목 | 상태 |
|------|------|
| 구조 검증 | ⬜ |
| 코드 생성 | ⬜ |
| 테스트 | ⬜ |
| 문서화 | ⬜ |
| 국제화 | ⬜ |
| 성능 최적화 | ⬜ |
| 보안 검토 | ⬜ |
| 접근성 | ⬜ |
| 정적 분석 | ⬜ |
| 통합 검증 | ⬜ |
| PR 준비 | ⬜ |

**전체 완료: ⬜/11**

---

## 관련 에이전트

- `@feature`: Feature 구조 생성
- `@test`: 테스트 작성 가이드
- `@code-review`: 코드 리뷰 체크리스트
- `@i18n`: 국제화 가이드

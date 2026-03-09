---
name: checklist/feature-complete
description: "Feature 개발 완료 전 검증 체크리스트"
invoke: /checklist:feature
aliases: ["/check:feature", "/feature:checklist"]
category: petmedi-development
complexity: moderate
mcp-servers: [serena]
---

# /checklist/feature-complete

> **Context Framework Note**: Feature 개발 완료 검증 시 활성화됩니다.

## Triggers

- Feature 개발 완료 시점
- PR 생성 전 자체 검토
- 코드 리뷰 요청 전

## 사용법

```
/checklist/feature-complete [feature_name]
```

## 검증 항목

### 1. 📁 구조 검증

#### Domain Layer
- [ ] Entity 정의 완료 (Freezed)
- [ ] Repository Interface 정의 (I prefix)
- [ ] UseCase 구현 완료
- [ ] Failure 클래스 정의
- [ ] 단위 테스트 작성

#### Data Layer
- [ ] Repository 구현체 완료
- [ ] Serverpod Mixin 구현 (필요시)
- [ ] Local Database 구현 (필요시)
- [ ] DTO ↔ Entity 매퍼 구현
- [ ] 캐싱 전략 적용 (SWR/Cache-First)

#### Presentation Layer
- [ ] Page 위젯 구현
- [ ] 재사용 Widget 분리
- [ ] BLoC/Cubit 구현
- [ ] Event/State 정의 (Freezed)
- [ ] Widget 테스트 작성

#### DI & Routing
- [ ] Injectable 어노테이션 추가
- [ ] Route 정의 (Auto_route)
- [ ] Route Guard 적용 (필요시)

### 2. 🔧 코드 생성

```bash
melos run generate:{feature_name}
# 또는
melos run build
```

- [ ] Freezed 코드 생성됨 (*.freezed.dart)
- [ ] Injectable 코드 생성됨 (*.g.dart)
- [ ] Route 코드 생성됨
- [ ] 빌드 에러 없음

### 3. 🧪 테스트

#### 단위 테스트
- [ ] UseCase 테스트 (Happy path, Error, Edge cases)
- [ ] Repository 테스트 (mocked data source)

#### BLoC 테스트
- [ ] 초기 상태 테스트
- [ ] 이벤트 → 상태 변화 테스트
- [ ] 에러 처리 테스트

#### Widget 테스트
- [ ] 렌더링 테스트
- [ ] 인터랙션 테스트
- [ ] 상태별 UI 테스트

```bash
flutter test feature/{type}/{feature_name}/test/
melos run test:with-html-coverage
```

- [ ] 모든 테스트 통과
- [ ] 커버리지 80% 이상

### 4. 📝 문서화

- [ ] 공개 API에 dartdoc 주석
- [ ] 복잡한 로직에 설명 주석
- [ ] TODO 주석 해결 또는 이슈 등록

### 5. 🌐 국제화

- [ ] 모든 UI 텍스트 번역 키 사용
- [ ] 번역 파일 업데이트 (`melos run generate:locale`)
- [ ] 복수형/파라미터 처리 확인

### 6. ⚡ 성능 최적화

- [ ] const 위젯 활용
- [ ] BlocBuilder buildWhen 적용
- [ ] ListView.builder 사용 (긴 리스트)
- [ ] 이미지 cacheWidth/cacheHeight 적용
- [ ] dispose에서 리소스 해제

### 7. 🔒 보안 검토

- [ ] 민감 정보 하드코딩 없음
- [ ] 입력 값 검증 적용
- [ ] 적절한 에러 메시지

### 8. ♿ 접근성

- [ ] Semantics label 적용
- [ ] 터치 타겟 크기 확인 (48x48 이상)
- [ ] 색상 대비 확인

### 9. 🔍 정적 분석

```bash
melos run analyze
melos run format
dcm analyze .
```

- [ ] Lint 경고 없음
- [ ] 코드 포맷팅 완료
- [ ] DCM 분석 통과
- [ ] **Pre-push 훅 통과** (push 시 자동 검증됨)

### 10. 🚀 통합 검증

```bash
flutter build ios --flavor development
flutter build apk --flavor development
```

- [ ] iOS 빌드 성공
- [ ] Android 빌드 성공
- [ ] 개발 환경에서 정상 동작

### 11. 📋 PR 준비

- [ ] 의미 있는 커밋 메시지 (한글, Conventional + Gitmoji)
- [ ] 관련 이슈 연결
- [ ] 리뷰어 지정

## 완료 요약

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

## 참조

- 상세 체크리스트: `.claude/checklists/feature-complete.md`
- PR 리뷰 체크리스트: `.claude/commands/checklist/pr-review.md`
- 코드 리뷰 스킬: `.claude/commands/code-review.md`

---
name: session
description: 세션 종료 시 .claude/ 문서 자동 업데이트
---

# Session

세션 진행 중 학습한 내용을 `.claude/` 디렉토리 문서에 자동 반영하는 스킬입니다.

## Scope and Capabilities

### 핵심 기능

| 기능 | 설명 |
|------|------|
| 문서 업데이트 | CLAUDE.md 및 관련 문서 자동 업데이트 |
| 자동화 탐지 | 반복 작업 패턴 발견 및 스킬 제안 |
| 학습 추출 | 세션에서 학습한 규칙/패턴 추출 |
| 후속 작업 | 다음 세션을 위한 작업 제안 |

### 2 Phase 워크플로우

```
Phase 1: 병렬 분석 (4 Agents)
├── doc-updater Agent      → 문서 업데이트 제안
├── automation-scout Agent → 자동화 패턴 탐지
├── learning-extractor Agent → 학습 내용 추출
└── followup-suggester Agent → 후속 작업 제안

Phase 2: 순차 처리 (1 Agent)
└── duplicate-checker Agent → 중복 검사 및 정리
```

## Quick Start

### 기본 사용

```bash
# 전체 세션 분석 및 문서 업데이트
/session:wrap

# 축약 명령어
/wrap
/sw
```

### 옵션 사용

```bash
# 특정 영역만 업데이트
/session:wrap --scope rules      # 규칙만 업데이트
/session:wrap --scope commands   # 커맨드만 업데이트
/session:wrap --scope agents     # 에이전트만 업데이트

# 드라이런 (변경사항 미리보기)
/session:wrap --dry-run

# 자동 커밋
/session:wrap --auto-commit

# 중복 검사 스킵
/session:wrap --skip-duplicates
```

## 분석 대상

### Phase 1 에이전트별 분석 대상

| 에이전트 | 분석 대상 |
|----------|----------|
| doc-updater | 코딩 컨벤션, 프로젝트 설정, 아키텍처 패턴, 의존성 |
| automation-scout | 반복 작업, 수동 패턴, 스킬 후보 |
| learning-extractor | 코드 패턴, 에러 해결책, 사용자 선호도 |
| followup-suggester | 미완료 TODO, 개선 사항, 기술 부채 |

### 대상 파일

| 경로 | 설명 |
|------|------|
| `CLAUDE.md` | 프로젝트 메인 가이드 |
| `.claude/rules/**/*.md` | 코딩 규칙 |
| `.claude/commands/**/*.md` | 스킬/에이전트 정의 |
| `.claude/settings.local.json` | 로컬 설정 |

## 결과 형식

### 완료 시

```
╔════════════════════════════════════════════════════════════════╗
║  Session Wrap Complete                                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📝 문서 업데이트                                              ║
║  ├── CLAUDE.md: +15 lines (코딩 컨벤션 추가)                  ║
║  ├── .claude/rules/bloc-patterns.md: +8 lines                 ║
║  └── .claude/commands/session/wrap.md: 신규 생성              ║
║                                                                ║
║  🤖 자동화 제안                                                ║
║  ├── bloc-event-state-pair 스킬 생성 권장                     ║
║  └── test-template auto-import 추가 권장                      ║
║                                                                ║
║  📚 학습 내용                                                  ║
║  ├── [규칙] dot shorthand 적극 사용                           ║
║  ├── [규칙] await 후 isClosed 체크 필수                       ║
║  └── [패턴] ZenHub issueTypeId 필수 지정                      ║
║                                                                ║
║  📋 후속 작업                                                  ║
║  ├── [높음] 테스트 커버리지 80% 달성                          ║
║  └── [중간] 저자 검색 API 최적화                              ║
║                                                                ║
║  🔄 중복 제거: 2건                                            ║
║  ⚠️ 충돌 해결: 0건                                            ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## 핵심 규칙

1. **비파괴적 업데이트**: 기존 내용 삭제보다 추가/수정 우선
2. **근거 기반**: 모든 변경에 세션 내 근거 명시
3. **일관성 유지**: 기존 문서 스타일과 일관성 유지
4. **중복 방지**: 같은 내용 중복 추가 방지
5. **사용자 확인**: 중요 변경은 사용자 확인 후 적용

## Additional Resources

- [wrap.md](../../commands/session/wrap.md) - 상세 커맨드 정의

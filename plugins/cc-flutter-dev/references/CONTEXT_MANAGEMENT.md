# Claude Code 컨텍스트 관리 가이드

> **참조 위치**: `.claude/references/CONTEXT_MANAGEMENT.md`

컨텍스트 윈도우 효율성을 극대화하기 위한 가이드입니다.

---

## 🚀 Quick Reference (Top 5)

| 명령어/단축키 | 용도 | 빈도 |
|---------------|------|------|
| `/compact` | 컨텍스트 압축 (대화 길어질 때) | ⭐⭐⭐ |
| `Esc Esc` | Claude 중단 (잘못된 방향일 때) | ⭐⭐⭐ |
| `/fork` | 병렬 작업 분기 | ⭐⭐ |
| `Tab` | 사고 과정 보기/숨기기 | ⭐⭐ |
| `@파일명` | 파일 빠른 참조 | ⭐⭐ |

---

## 핵심 원칙

> **"컨텍스트 윈도우는 귀중하다 - 사용하지 않는 건 끄기"**

### 1. 과하게 설정하지 말 것
- 설정은 fine-tuning이 아니라 **아키텍처**
- 필요한 것만 활성화
- 불필요한 MCP/Plugin은 비활성화

### 2. MCP 서버 관리

| 권장 | 설명 |
|------|------|
| 설정 | 20-30개 |
| **활성화** | **프로젝트당 5-6개만** |
| 총 도구 | 80개 이하 유지 |

**이유**: 200k 컨텍스트가 80개 도구 활성화 시 ~70k로 줄어듦

### 3. 현재 활성 MCP (5개)
```json
{
  "enabledMcpjsonServers": [
    "figma",
    "flutter-inspector",
    "flutter-inspector-console",
    "coui-flutter",
    "zenhub"
  ]
}
```

---

## 병렬 워크플로우 활용

### `/fork` - 작업 분기
여러 작업을 동시에 처리:
- 메인: Flutter UI 개발
- Fork 1: Serverpod API 개발
- Fork 2: 테스트 작성

### `git worktree` - 독립 개발
```bash
git worktree add ../feature-auth feature-auth
# Claude가 각 워크트리에서 독립 실행
```

### `tmux` - 장시간 작업
```bash
tmux new -s dev          # 세션 생성
# Claude가 여기서 melos build 실행
tmux attach -t dev       # 나중에 로그 확인
```

---

## Subagent 최적화

### 범위 제한 원칙
- **도구가 적을수록 정확함**
- 필요한 도구만 명시
- 단일 책임 원칙 적용

### 에이전트 구조 예시
```markdown
---
name: bloc
tools: Read, Edit, Write, Glob, Grep  # 필요한 것만!
model: inherit
skills: bloc
---
```

---

## Hooks 활용 (자동화)

### Dart 개발용 추천 Hooks
```json
{
  "PostToolUse": [
    {
      "matcher": "Edit && .dart",
      "hooks": ["dart format", "dart analyze"]
    }
  ],
  "Stop": [
    {
      "matcher": "*",
      "hooks": ["check modified files for print statements"]
    }
  ]
}
```

---

## 유용한 Commands

| Command | 설명 |
|---------|------|
| `/compact` | 수동 컨텍스트 압축 |
| `/rewind` | 이전 상태로 돌아가기 |
| `/statusline` | 상태바 (브랜치, 컨텍스트%) |
| `/checkpoints` | 파일 레벨 언두 포인트 |

---

## Keyboard Shortcuts

| 단축키 | 기능 |
|--------|------|
| `Ctrl+U` | 라인 삭제 |
| `!` | bash 빠른 접근 |
| `@` | 파일 검색 |
| `/` | 슬래시 명령 |
| `Shift+Enter` | 여러 줄 입력 |
| `Tab` | 사고 표시 토글 |
| `Esc Esc` | Claude 중단 |

---

## 최적화 체크리스트

- [ ] 활성 MCP 5-6개 이하 유지
- [ ] 불필요한 에이전트 비활성화
- [ ] 장시간 작업은 tmux 활용
- [ ] 병렬 작업은 `/fork` 또는 worktree 활용
- [ ] 주기적으로 `/compact` 실행

---

## 관련 문서

- `settings.local.json` - MCP 활성화 설정
- `CLAUDE.md` - 프로젝트 전체 가이드

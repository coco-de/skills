# Contributing to coco-de/skills

## 플러그인 구조

각 플러그인은 `cc-` 접두사를 사용하며, 다음 구조를 따릅니다:

```
cc-<name>/
├── .claude-plugin/
│   └── plugin.json          # 필수: 플러그인 메타데이터
├── README.md                # 필수: 플러그인 설명
├── skills/                  # SKILL.md, REFERENCE.md, TEMPLATES.md
├── commands/                # 슬래시 커맨드 (.md)
├── agents/                  # 에이전트 정의 (.md)
├── rules/                   # 규칙 (.md)
└── references/              # 참조 문서
```

## plugin.json 형식

```json
{
  "name": "cc-<name>",
  "version": "1.0.0",
  "description": "플러그인 설명",
  "skills": ["skills/"],
  "commands": ["commands/"],
  "agents": ["agents/"],
  "rules": ["rules/"]
}
```

## 기여 가이드라인

1. **새 플러그인 추가**: `cc-` 접두사 필수, `plugin.json` 포함
2. **기존 플러그인 수정**: 해당 플러그인 디렉토리에서 작업
3. **검증**: `python3 validate_plugins.py` 실행하여 구조 검증
4. **PR 규칙**: 변경된 플러그인별로 커밋 분리

## 스킬 파일 형식

- `SKILL.md`: 스킬 정의 (트리거, 동작, 출력)
- `REFERENCE.md`: 참조 문서 (패턴, API, 규칙)
- `TEMPLATES.md`: 코드/문서 템플릿

## 커맨드 파일 형식

각 `.md` 파일이 하나의 슬래시 커맨드를 정의합니다.
파일 경로가 커맨드 이름이 됩니다: `commands/workflow/issue-cycle.md` → `/workflow:issue-cycle`

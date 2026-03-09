---
name: bug-report
description: "이미지 분석 기반 버그 리포트 생성 및 ZenHub 이슈 자동화"
invoke: /bug-report
aliases: ["/br"]
category: petmedi-development
mcp-servers: [zenhub]
---

# /bug-report

> 이미지 분석을 통한 버그 리포트 생성 및 ZenHub 이슈 자동화

## Triggers

- 버그 발견 시 이슈 등록이 필요할 때
- 스크린샷과 함께 버그 리포트를 작성할 때
- QA 중 발견된 문제를 문서화할 때

## Context Trigger Pattern

```bash
/bug-report [이미지_경로] [버그_설명]
```

## Parameters

| 파라미터 | 필수 | 설명 | 예시 |
|---------|------|------|------|
| `이미지_경로` | ❌ | 버그 스크린샷 경로 | `/path/to/screenshot.png` |
| `버그_설명` | ✅ | 버그에 대한 간단한 설명 | `"로그인 버튼이 동작하지 않음"` |
| `--severity` | ❌ | 심각도 지정 | `critical`, `high`, `medium`, `low` |
| `--type` | ❌ | 버그 유형 지정 | `ui`, `function`, `crash`, `performance`, `data` |
| `--no-create` | ❌ | 이슈 생성 없이 리포트만 | - |

## Behavioral Flow

### Step 1: 이미지 분석 (이미지 제공 시)

```markdown
## 이미지 분석

Read 도구를 사용하여 스크린샷 분석:

1. **UI 상태 파악**
   - 에러 다이얼로그 표시 여부
   - 빈 화면(Empty State) 여부
   - 로딩 상태 지속 여부
   - 레이아웃 깨짐 여부

2. **텍스트 추출**
   - 에러 메시지
   - 화면 타이틀
   - 버튼 텍스트

3. **버그 분류 추론**
   - 버그 유형 자동 분류
   - 심각도 추천
   - 영향 영역 식별
```

### Step 2: 정보 수집

```markdown
## 정보 수집

AskUserQuestion을 통해 추가 정보 수집:

1. **재현 단계** (필수)
   - 버그 발생 전 상태
   - 수행한 액션
   - 버그 발생 시점

2. **예상 결과** (필수)
   - 정상 동작 시 기대 결과

3. **환경 정보** (선택)
   - OS 버전
   - 디바이스
   - 앱 버전

4. **심각도 확인** (분석 결과 제시 후)
   - 🔴 Critical
   - 🟠 High
   - 🟡 Medium
   - 🟢 Low
```

### Step 3: ZenHub 이슈 생성

```markdown
## 이슈 생성

mcp__zenhub__createGitHubIssue 호출:

1. **제목 생성**
   - 형식: `[Bug] {화면명}: {버그 요약}`
   - 크래시: `[Crash] {화면명}: {크래시 상황}`

2. **본문 작성**
   - TEMPLATES.md의 전체 버그 리포트 템플릿 사용
   - 이미지 분석 결과 포함
   - 재현 단계, 예상/실제 결과 포함

3. **라벨 지정**
   - `bug` (기본)
   - `severity:{level}`
   - `area:{affected_area}`

4. **파이프라인 이동**
   - Critical → In Progress
   - High → Triage
   - Medium/Low → Backlog
```

## MCP Integration

| 작업 | MCP 도구 | 용도 |
|------|----------|------|
| 이슈 생성 | `mcp__zenhub__createGitHubIssue` | GitHub 이슈 생성 |
| 파이프라인 이동 | `mcp__zenhub__moveIssueToPipeline` | 이슈 상태 관리 |
| 라벨 조회 | `mcp__zenhub__getWorkspacePipelinesAndRepositories` | 라벨 및 파이프라인 정보 |

## Examples

### 기본 사용 (이미지 포함)

```bash
/bug-report /tmp/error_screenshot.png "결제 완료 후 주문 내역이 표시되지 않습니다"
```

### 텍스트만 사용

```bash
/bug-report "로그인 버튼 클릭 시 아무 반응이 없습니다"
```

### 심각도 지정

```bash
/bug-report --severity critical "앱 시작 시 크래시 발생"
```

### 버그 유형 지정

```bash
/bug-report --type ui /tmp/layout.png "긴 텍스트에서 오버플로우 발생"
```

### 리포트만 생성 (이슈 생성 없음)

```bash
/bug-report --no-create "테스트 버그입니다"
```

## Output Format

### 이미지 분석 결과

```
╔════════════════════════════════════════════════════════════════╗
║  Image Analysis Result                                         ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  🖼️ Image: /tmp/screenshot.png                                 ║
║                                                                ║
║  📍 Detected Issues:                                           ║
║    1. 에러 다이얼로그 표시됨                                    ║
║    2. "네트워크 오류" 메시지 감지                               ║
║                                                                ║
║  🏷️ Suggested Classification:                                  ║
║    - Type: 기능 버그 (Function)                                ║
║    - Severity: High                                            ║
║    - Area: Backend/Network                                     ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

### 이슈 생성 완료

```
╔════════════════════════════════════════════════════════════════╗
║  Bug Report Created                                            ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  📋 Issue: #123                                                ║
║  📝 Title: [Bug] 결제: 주문 내역 미표시                         ║
║                                                                ║
║  🏷️ Labels:                                                    ║
║    - bug                                                       ║
║    - severity:high                                             ║
║    - area:backend                                              ║
║                                                                ║
║  📊 Pipeline: Triage                                           ║
║                                                                ║
║  🔗 URL: https://github.com/coco-de/kobic/issues/123           ║
║                                                                ║
║  💡 Next Steps:                                                ║
║    /workflow:bug-cycle 123  # 수정 사이클 시작                  ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
```

## 참조 문서

- Skill: `~/.claude/skills/bug-report/SKILL.md`
- Reference: `~/.claude/skills/bug-report/REFERENCE.md`
- Templates: `~/.claude/skills/bug-report/TEMPLATES.md`

## 핵심 규칙

1. **이미지 우선 분석**: 이미지가 제공되면 먼저 분석하여 컨텍스트 파악
2. **사용자 확인**: 심각도와 버그 유형은 분석 결과를 제시하고 사용자 확인
3. **구조화된 리포트**: 템플릿을 사용하여 일관된 형식 유지
4. **자동 라벨링**: 버그 특성에 맞는 라벨 자동 지정
5. **워크플로우 연계**: 이슈 생성 후 `/workflow:bug-cycle` 안내

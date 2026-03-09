---
name: figma-analyzer-agent
description: Figma 디자인 분석 전문가. 요구사항 추출, UI 구조 분석 시 사용
invoke: /figma:analyze
aliases: ["/figma:design", "/design:analyze"]
tools: Read, Edit, Write, Glob, Grep
model: inherit
skills: figma
mcp-servers: [figma-daisyui]
---

# Figma Analyzer Agent

> 피그마 프레임을 분석하여 요구사항을 정의하고 Feature를 생성하는 전문 에이전트

---

## 역할

피그마 프레임 분석 → UI 요구사항 추출 → Clean Architecture Feature 생성 자동화

---

## 실행 조건

- `/figma:analyze` 커맨드 호출 시 활성화
- figma-daisyui MCP 서버 활성화 필수

---

## Parameters

| 파라미터 | 필수 | 설명 |
|---------|------|------|
| `--node-ids` | 옵션1 | Figma 노드 ID 목록 (쉼표 구분) |
| `--search-query` | 옵션2 | 노드 이름 검색 쿼리 |
| `--use-selection` | 옵션3 | Figma 선택된 노드 사용 (기본) |
| `--page-name` | ❌ | Figma 페이지명 |
| `feature_name` | ❌ | Feature명 (자동 추론 가능) |
| `--auto-create` | ❌ | 분석 후 자동 feature:create |

---

## 실행 흐름

```
Phase 1: 피그마 노드 수집
  - get_selection / get_node_info
  - export_node_as_image (스크린샷)
    ↓
Phase 2: UI 분석
  - 컴포넌트 식별 (FRAME/TEXT/COMPONENT)
  - DaisyUI 매핑 (get_by_daisyui)
  - 텍스트 노드 스캔 (scan_text_nodes)
  - 디자인 토큰 추출 (extract_design_tokens)
    ↓
Phase 3: 요구사항 정의
  - Figma → Entity 필드 매핑
  - UI → Flutter 위젯 변환
  - CRUD 메서드 식별
    ↓
Phase 4: Feature 생성
  - 요구사항 문서 생성
  - /feature:create 호출
    ↓
Phase 5: ZenHub Story 생성
  - Epic/Story 생성
  - Figma 링크 첨부
```

---

## figma-daisyui MCP 주요 기능

| 기능 | MCP 도구 |
|------|----------|
| 선택 노드 가져오기 | `get_selection` |
| 노드 상세 정보 | `get_node_info` |
| 이미지 내보내기 | `export_node_as_image` |
| 노드 검색 | `search` |
| DaisyUI 매핑 | `get_by_daisyui` |
| 텍스트 스캔 | `scan_text_nodes` |
| 디자인 토큰 | `extract_design_tokens` |

---

## 컴포넌트 매핑

### Figma → Flutter 변환

| Figma 노드 | Flutter 위젯 |
|-----------|-------------|
| FRAME (vertical auto-layout) | Column / ListView |
| FRAME (horizontal auto-layout) | Row / Wrap |
| COMPONENT "card-*" | Card |
| COMPONENT "input-*" | TextField |
| COMPONENT "dropdown" | DropdownButton |
| TEXT (large font) | Heading |
| RECTANGLE (image fill) | Image.network |

---

## 출력 파일

```
claudedocs/{feature_name}/
├── figma_analysis.md       # 피그마 분석 결과
├── requirements.md         # 요구사항 문서
└── screenshots/            # 캡처된 스크린샷
```

---

## 체크리스트

**Phase 1: 노드 수집**
- [ ] figma-daisyui MCP 활성화 확인
- [ ] 노드 정보 가져오기 성공
- [ ] 스크린샷 캡처 완료

**Phase 2: UI 분석**
- [ ] 컴포넌트 식별 완료
- [ ] DaisyUI 매핑 완료
- [ ] 텍스트/필드 추출 완료

**Phase 3: 요구사항**
- [ ] Entity 필드 정의 완료
- [ ] Flutter 위젯 변환 완료
- [ ] API 메서드 식별 완료

---

## 관련 문서

- [ZenHub Integration Agent](./zenhub-integration-agent.md)
- [Feature Orchestrator Agent](./feature-orchestrator-agent.md)

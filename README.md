# coco-de/skills

CoCode 팀 통합 스킬 레포지토리

## 기술 스택

- **Frontend**: Flutter (Mobile/Desktop) + Jaspr (Web)
- **Backend**: Serverpod
- **UI Library**: CoUI (크로스플랫폼 컴포넌트)
- **Architecture**: Clean Architecture + BLoC 패턴

## 설치

```bash
claude plugins install coco-de/skills
```

### 개별 플러그인 설치

```bash
claude plugins install coco-de/skills/plugins/cc-bmad
claude plugins install coco-de/skills/plugins/cc-flutter-dev
# ...
```

## 플러그인 목록

### 방법론 & 워크플로우
| 플러그인 | 설명 |
|---------|------|
| `cc-bmad` | BMAD 방법론 (10 skills, 18 commands) |
| `cc-workflow` | 개발 워크플로우 (Issue/Bug Cycle, Session, ZenHub) |
| `cc-code-quality` | 코드리뷰, 체크리스트, 버그리포트 |

### Flutter 개발
| 플러그인 | 설명 |
|---------|------|
| `cc-coui` | CoUI 컴포넌트 라이브러리 (26개 컴포넌트) |
| `cc-flutter-dev` | Flutter 개발 핵심 (UI, Feature, BLoC, Test) |
| `cc-flutter-inspector` | Flutter Inspector 디버깅 (Master + 9 전문) |
| `cc-i18n` | 국제화 (Slang 기반) |

### 백엔드 & 분석
| 플러그인 | 설명 |
|---------|------|
| `cc-serverpod` | Serverpod 백엔드 |
| `cc-clickhouse` | ClickHouse BI 분석 |

### PM (Product Management)
| 플러그인 | 설명 |
|---------|------|
| `cc-pm-discovery` | 제품 발견 (인터뷰, 실험, 가정 테스트) |
| `cc-pm-strategy` | 제품 전략 (비전, 비즈니스 모델) |
| `cc-pm-analytics` | 데이터 분석 (SQL, 코호트, A/B 테스트) |
| `cc-pm-gtm` | Go-to-Market |

### UI/UX (libreuiux CoCode 맞춤)
| 플러그인 | 설명 |
|---------|------|
| `cc-uiux-design` | UI/UX 디자인 (CoUI 토큰, DaisyUI 테마) |
| `cc-uiux-accessibility` | 접근성 (Flutter + Jaspr Web) |
| `cc-uiux-frontend` | 프론트엔드 (Flutter/Dart + CoUI) |
| `cc-uiux-backend` | 백엔드 (Serverpod 전용) |
| `cc-uiux-testing` | 테스팅 (Dart/Flutter) |
| `cc-uiux-devops` | DevOps (배포 파이프라인) |
| `cc-uiux-security` | 보안 (API + 앱) |

## 프로젝트 로컬 유지 항목

각 프로젝트의 `.claude/`에 유지해야 할 항목:
- `settings.json`, `settings.local.json`
- `rules/project-config.md` (프로젝트별 구조/설정)
- 프로젝트 고유 rules
- `plans/`, `hooks/`, `docs/`

## 검증

```bash
python3 validate_plugins.py
```

## 라이선스

MIT

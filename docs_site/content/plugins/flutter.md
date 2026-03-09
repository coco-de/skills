---
title: Flutter 개발
description: CoUI 컴포넌트, Flutter 핵심 개발, Inspector, 국제화 플러그인
---

# Flutter 개발

## cc-coui

**CoUI 컴포넌트 라이브러리** — Flutter와 Jaspr Web 모두에서 동작하는 **26개 크로스플랫폼 컴포넌트**를 제공합니다.

### 컴포넌트 목록

| 카테고리 | 컴포넌트 |
|----------|----------|
| **Input** (8) | Button, Checkbox, DatePicker, Form, Input, Select, Slider, Toggle |
| **Display** (6) | Avatar, Badge, Card, Progress, Table, Text |
| **Navigation** (3) | Menu, Navigation, Tabs |
| **Overlay** (5) | Dialog, Drawer, Popover, Toast, Tooltip |
| **Layout** (2) | Accordion, Calendar |
| **Theme** (1) | Theme |

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-coui
```

---

## cc-flutter-dev

**Flutter 개발 핵심** — UI 생성, Feature 스캐폴딩, BLoC 패턴, 테스트 자동화를 지원합니다.

| 항목 | 내용 |
|------|------|
| Skills | 2개 (workflow, flutter-ui) |
| Agents | 6개 (bloc, feature, flutter-ui, flutter-image-optimizer, test, console-feature) |
| Rules | 10개 (coui-flutter, dcm-\*, data-mapper, bdd-test-patterns 등) |

### 주요 커맨드

```bash
/bloc                        # BLoC 생성
/flutter-ui                  # Flutter UI 생성
/feature:create              # Feature 스캐폴딩
/bdd:generate                # BDD 시나리오 생성
/figma:analyze               # Figma 디자인 분석
```

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-dev
```

---

## cc-flutter-inspector

**Flutter Inspector 디버깅** — Master Inspector와 9개 전문 Inspector로 체계적인 디버깅을 수행합니다.

### Inspector 목록

| Inspector | 역할 |
|-----------|------|
| **Master** | 전체 조율 및 분석 |
| auth | 인증 관련 디버깅 |
| bloc | BLoC 상태관리 디버깅 |
| config | 설정 관련 디버깅 |
| form | 폼 관련 디버깅 |
| image | 이미지 관련 디버깅 |
| log | 로그 분석 |
| nav | 네비게이션 디버깅 |
| network | 네트워크 디버깅 |
| ui | UI 관련 디버깅 |

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-flutter-inspector
```

---

## cc-i18n

**국제화** — Slang 기반 i18n 프레임워크를 활용한 다국어 지원입니다.

### 설치

```bash
claude plugins install coco-de/skills/plugins/cc-i18n
```

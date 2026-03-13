# Stage Map — 시각적 스테이지 맵

## 전체 파이프라인

```
╔═══════════════════════════════════════════════════════════════════════════╗
║                        PROJECT PIPELINE                                  ║
║                     /project "설명"                                       ║
╚═══════════════════════════════════════════════════════════════════════════╝

 Stage 1              Stage 2              Stage 3
 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
 │  DISCOVERY   │────▶│  PLANNING    │────▶│   DESIGN     │
 │  /project:   │     │  /project:   │     │  /project:   │
 │   discover   │     │   plan       │     │   design     │
 │              │     │              │     │              │
 │ cc-pm-disc.  │     │ cc-bmad      │     │ cc-bmad      │
 │ cc-pm-strat. │     │ cc-pm-strat. │     │              │
 │ cc-bmad      │     │              │     │              │
 └──────────────┘     └──────┬───────┘     └──────┬───────┘
   스킵: L0-1               │                     │
                       Analysis Gate         Solutioning Gate

 Stage 4              Stage 5              Stage 6
 ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
 │ EPIC CREATION│────▶│ DEVELOPMENT  │────▶│   LAUNCH     │
 │  /project:   │     │  /project:   │     │  /project:   │
 │   epic       │     │   develop    │     │   launch     │
 │              │     │              │     │              │
 │ cc-dev-cycle  │     │ cc-dev-cycle  │     │ cc-pm-gtm    │
 │ cc-bmad      │     │ cc-bmad      │     │ cc-pm-anal.  │
 └──────┬───────┘     └──────┬───────┘     └──────────────┘
        │                     │               스킵: L0-1
   Planning Gate        Implementation
                            Gate
```

## 스테이지별 소스 플러그인 매핑

```
 Discovery         Planning          Design
 ┌────────────┐   ┌────────────┐   ┌────────────┐
 │pm-discovery│   │   bmad     │   │   bmad     │
 │ ├interview │   │ ├prod-brief│   │ ├architect.│
 │ ├assumption│   │ ├prd       │   │ ├ux-design │
 │ └experiment│   │ ├tech-spec │   │ ├Architect │
 │pm-strategy │   │ └Analyst   │   │ └UX Design.│
 │ ├competitive│  │pm-strategy │   └────────────┘
 │ └vision    │   │ └biz-model │
 │bmad        │   └────────────┘
 │ ├research  │
 │ └brainstorm│
 └────────────┘

 Epic Creation     Development        Launch
 ┌────────────┐   ┌────────────┐   ┌────────────┐
 │workflow    │   │workflow    │   │pm-gtm      │
 │ └create-   │   │ └/workflow │   │ ├gtm-motion│
 │   epic     │   │   {issue}  │   │ ├icp-def.  │
 │bmad        │   │bmad        │   │ └messaging │
 │ ├create-   │   │ ├dev-story │   │pm-analytics│
 │ │ story    │   │ ├Flutter   │   │ ├ab-testing│
 │ ├sprint-   │   │ │ Dev      │   │ └cohort    │
 │ │ planning │   │ └Backend   │   └────────────┘
 │ └PM persona│   │   Dev      │
 └────────────┘   └────────────┘
```

## 게이트 상세

```
 Analysis Gate                    Solutioning Gate
 ┌───────────────────┐           ┌───────────────────────────────┐
 │ □ requirement_    │           │ Architect        UX Designer  │
 │   clarity         │           │ □ clean_arch.   □ coui_comp.  │
 │ □ scope_          │           │ □ di_structure  □ layout      │
 │   appropriateness │           │ □ api_design    □ interaction │
 │ □ ac_testability  │           │ □ security      □ a11y        │
 └───────────────────┘           └───────────────────────────────┘

 Planning Gate                    Implementation Gate
 ┌───────────────────┐           ┌───────────────────┐
 │ □ epic_story_     │           │ □ lint_pass        │
 │   structure       │           │ □ test_pass        │
 │ □ story_point     │           │ □ code_review      │
 │ □ labeling        │           │ □ branch_naming    │
 │ □ dependencies    │           │                    │
 └───────────────────┘           └───────────────────┘
```

## BMAD 레벨별 실행 경로

```
 Level 0 (Hotfix):
 ──── Planning ──── Development ────

 Level 1 (Minor):
 ──── Planning ──── Design ──── Epic ──── Development ────

 Level 2-3 (Feature):
 ──── Discovery ──── Planning ──── Design ──── Epic ──── Development ──── Launch ────

 Level 4 (New Project):
 ──── Discovery* ──── Planning ──── Design ──── Epic ──── Development ──── Launch ────
 (* 심층 모드)
```

#!/usr/bin/env python3
"""
플러그인 .md 파일 → docs_site/content 페이지 자동 생성 스크립트

Usage:
    python3 generate_docs.py [--clean] [--verbose]
"""

import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).parent
PLUGINS_DIR = REPO_ROOT / "plugins"
DOCS_CONTENT_DIR = REPO_ROOT / "docs_site" / "content" / "plugins"
PLUGIN_PREFIX = "cc-"

# 플러그인 .md가 존재하는 하위 디렉토리 종류
CONTENT_DIRS = [
    "skills", "commands", "agents", "rules", "references",
    "orchestrators", "personas", "checklists", "templates",
    "config", "docs",
]

# 카테고리 → 플러그인 매핑 (기존 카테고리 페이지 기준)
CATEGORY_MAP = {
    "methodology": ["cc-bmad", "cc-workflow", "cc-code-quality"],
    "flutter": ["cc-coui", "cc-flutter-dev", "cc-flutter-inspector", "cc-i18n"],
    "backend": ["cc-serverpod", "cc-backend", "cc-clickhouse"],
    "product-management": ["cc-pm-discovery", "cc-pm-strategy", "cc-pm-analytics", "cc-pm-gtm"],
    "uiux": [
        "cc-uiux-design", "cc-uiux-accessibility", "cc-uiux-frontend",
        "cc-uiux-backend", "cc-uiux-testing", "cc-uiux-devops", "cc-uiux-security",
    ],
    "pipeline": ["cc-pipeline"],
}

# 카테고리 표시명
CATEGORY_NAMES = {
    "methodology": "방법론 & 워크플로우",
    "flutter": "Flutter 개발",
    "backend": "백엔드 & 분석",
    "product-management": "Product Management",
    "uiux": "UI/UX",
    "pipeline": "Pipeline",
}

# 섹션 표시명
SECTION_NAMES = {
    "skills": "Skills",
    "commands": "Commands",
    "agents": "Agents",
    "rules": "Rules",
    "references": "References",
    "orchestrators": "Orchestrators",
    "personas": "Personas",
    "checklists": "Checklists",
    "templates": "Templates",
    "config": "Config",
    "docs": "Docs",
}


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """YAML frontmatter를 파싱하고 (metadata, body) 반환."""
    if not content.startswith("---"):
        return {}, content

    end = content.find("---", 3)
    if end == -1:
        return {}, content

    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()

    metadata = {}
    current_key = None
    for line in fm_text.split("\n"):
        # 배열 항목 처리 (예: - item)
        if line.strip().startswith("- ") and current_key:
            if current_key not in metadata:
                metadata[current_key] = []
            if isinstance(metadata[current_key], list):
                metadata[current_key].append(line.strip()[2:])
            continue

        match = re.match(r'^(\w[\w-]*)\s*:\s*(.*)', line)
        if match:
            key = match.group(1)
            value = match.group(2).strip()
            current_key = key

            # YAML 인라인 배열: [a, b, c]
            if value.startswith("[") and value.endswith("]"):
                items = [v.strip().strip('"').strip("'") for v in value[1:-1].split(",") if v.strip()]
                metadata[key] = items
            else:
                # 따옴표 제거
                if (value.startswith('"') and value.endswith('"')) or \
                   (value.startswith("'") and value.endswith("'")):
                    value = value[1:-1]
                metadata[key] = value

    return metadata, body


def extract_title_from_body(body: str) -> Optional[str]:
    """본문에서 첫 번째 # 헤딩을 추출."""
    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line[2:].strip()
    return None


def make_title(md_path: Path, metadata: dict, body: str, section: str) -> str:
    """페이지 title 결정."""
    # 1. frontmatter name → title
    if "name" in metadata:
        return metadata["name"]

    # 2. SKILL.md → 디렉토리명 사용
    if md_path.name == "SKILL.md":
        return md_path.parent.name

    # 3. REFERENCE.md → "<parent> Reference"
    if md_path.name == "REFERENCE.md":
        return f"{md_path.parent.name} Reference"

    # 4. TEMPLATES.md → "<parent> Templates"
    if md_path.name == "TEMPLATES.md":
        return f"{md_path.parent.name} Templates"

    # 5. 본문 첫 헤딩
    heading = extract_title_from_body(body)
    if heading:
        return heading

    # 6. 파일명에서 유도
    return md_path.stem


def make_description(metadata: dict, body: str) -> str:
    """페이지 description 결정."""
    if "description" in metadata:
        desc = metadata["description"]
        # 긴 description은 200자로 제한
        if len(desc) > 200:
            desc = desc[:197] + "..."
        return desc

    # 본문 첫 문단에서 유도 (빈 줄 전까지)
    for line in body.split("\n"):
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith(">") and not line.startswith("```"):
            if len(line) > 200:
                line = line[:197] + "..."
            return line

    return ""


def build_metadata_table(metadata: dict) -> str:
    """frontmatter의 추가 필드들을 메타데이터 테이블로 변환."""
    # title/description으로 이미 사용한 필드 제외
    skip_keys = {"name", "description", "title"}
    display_keys = {
        "invoke": "Invoke",
        "aliases": "Aliases",
        "tools": "Tools",
        "model": "Model",
        "skill_id": "Skill ID",
        "version": "Version",
        "module": "Module",
        "category": "Category",
        "complexity": "Complexity",
        "phase": "Phase",
        "globs": "Globs",
        "skills": "Skills",
        "linked-agents": "Linked Agents",
        "mcp-servers": "MCP Servers",
    }

    rows = []
    for key, value in metadata.items():
        if key in skip_keys:
            continue
        display_name = display_keys.get(key, key)
        if isinstance(value, list):
            if not value:
                continue
            value_str = ", ".join(str(v) for v in value)
        else:
            value_str = str(value)
        if not value_str:
            continue
        rows.append(f"| {display_name} | {value_str} |")

    if not rows:
        return ""

    table = "| 항목 | 내용 |\n|------|------|\n"
    table += "\n".join(rows)
    return table + "\n"


def generate_page(title: str, description: str, metadata_table: str, body: str) -> str:
    """Jaspr 호환 페이지 콘텐츠 생성."""
    # Frontmatter
    # description에서 줄바꿈, 따옴표 이스케이프
    safe_desc = description.replace('"', '\\"').replace("\n", " ").strip()
    safe_title = title.replace('"', '\\"').strip()

    content = f'---\ntitle: "{safe_title}"\ndescription: "{safe_desc}"\n---\n\n'

    # 메타데이터 테이블이 있으면 본문 최상단에 삽입
    if metadata_table:
        content += metadata_table + "\n"

    # 본문 추가
    content += body + "\n"

    return content


def get_output_path(plugin_name: str, section: str, md_path: Path, plugin_dir: Path) -> Path:
    """출력 파일 경로 결정."""
    rel = md_path.relative_to(plugin_dir / section)

    # SKILL.md → 디렉토리명.md
    if md_path.name == "SKILL.md":
        parent_rel = rel.parent
        return DOCS_CONTENT_DIR / plugin_name / section / parent_rel / f"{md_path.parent.name}.md"

    # REFERENCE.md → <dir>-reference.md
    if md_path.name == "REFERENCE.md":
        parent_rel = rel.parent
        return DOCS_CONTENT_DIR / plugin_name / section / parent_rel / f"{md_path.parent.name}-reference.md"

    # TEMPLATES.md → <dir>-templates.md
    if md_path.name == "TEMPLATES.md":
        parent_rel = rel.parent
        return DOCS_CONTENT_DIR / plugin_name / section / parent_rel / f"{md_path.parent.name}-templates.md"

    # 일반 파일
    return DOCS_CONTENT_DIR / plugin_name / section / rel


def process_md_file(md_path: Path, plugin_name: str, section: str, plugin_dir: Path) -> Optional[dict]:
    """단일 .md 파일을 처리하여 docs 페이지 생성. 반환: 링크 정보 dict."""
    content = md_path.read_text(encoding="utf-8")
    metadata, body = parse_frontmatter(content)

    title = make_title(md_path, metadata, body, section)
    description = make_description(metadata, body)
    metadata_table = build_metadata_table(metadata)

    # 본문에서 첫 # 헤딩이 title과 동일하면 제거 (중복 방지)
    heading = extract_title_from_body(body)
    if heading and heading == title:
        body = re.sub(r'^#\s+' + re.escape(heading) + r'\s*\n*', '', body, count=1)

    page_content = generate_page(title, description, metadata_table, body)
    output_path = get_output_path(plugin_name, section, md_path, plugin_dir)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(page_content, encoding="utf-8")

    # 링크 정보 반환
    rel_href = str(output_path.relative_to(DOCS_CONTENT_DIR)).replace(".md", "")
    return {
        "title": title,
        "description": description,
        "section": section,
        "href": f"/plugins/{rel_href}",
        "output_path": output_path,
    }


def _extract_readme_intro(readme_content: str, description: str) -> str:
    """README에서 ## 섹션 이전의 인트로 텍스트만 추출."""
    _, readme_body = parse_frontmatter(readme_content)
    # 첫 # 헤딩 제거
    readme_body = re.sub(r'^#\s+.*\n*', '', readme_body, count=1)

    # ## 이전까지만 추출 (섹션 테이블은 링크 테이블로 대체)
    intro_lines = []
    for line in readme_body.split("\n"):
        if line.startswith("## "):
            break
        intro_lines.append(line)

    intro = "\n".join(intro_lines).strip()
    # description과 동일한 첫 줄 제거
    if intro and intro.split("\n")[0].strip() == description.strip():
        intro = "\n".join(intro.split("\n")[1:]).strip()

    return intro


def generate_plugin_index(plugin_name: str, plugin_data: dict, readme_content: str, pages: list[dict]) -> Path:
    """플러그인 index.md 생성."""
    name = plugin_data.get("name", plugin_name)
    description = plugin_data.get("description", "")

    content = f'---\ntitle: "{name}"\ndescription: "{description}"\n---\n\n'
    content += f"# {name}\n\n"

    if description:
        content += f"{description}\n\n"

    # README 인트로만 병합 (## 섹션 테이블은 링크 테이블로 대체)
    if readme_content:
        intro = _extract_readme_intro(readme_content, description)
        if intro:
            content += intro + "\n\n"

    # 섹션별 링크 테이블
    sections_with_pages = {}
    for page in pages:
        sec = page["section"]
        if sec not in sections_with_pages:
            sections_with_pages[sec] = []
        sections_with_pages[sec].append(page)

    for section_key in CONTENT_DIRS:
        if section_key not in sections_with_pages:
            continue
        section_pages = sections_with_pages[section_key]
        section_name = SECTION_NAMES.get(section_key, section_key.title())

        content += f"## {section_name}\n\n"
        content += "| 이름 | 설명 |\n|------|------|\n"
        for page in sorted(section_pages, key=lambda p: p["title"]):
            title = page["title"]
            desc = page["description"][:100] if page["description"] else ""
            href = page["href"]
            content += f"| [{title}]({href}) | {desc} |\n"
        content += "\n"

    # 설치 안내
    content += "## 설치\n\n"
    content += f"```bash\nclaude plugins install coco-de/skills/plugins/{plugin_name}\n```\n"

    output_path = DOCS_CONTENT_DIR / plugin_name / "index.md"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    return output_path


def process_plugin(plugin_dir: Path, verbose: bool = False) -> dict:
    """플러그인 하나를 처리."""
    plugin_name = plugin_dir.name

    # plugin.json 읽기
    plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
    plugin_data = {}
    if plugin_json_path.exists():
        with open(plugin_json_path) as f:
            plugin_data = json.load(f)

    # README.md 읽기
    readme_content = ""
    readme_path = plugin_dir / "README.md"
    if readme_path.exists():
        readme_content = readme_path.read_text(encoding="utf-8")

    # 각 섹션의 .md 파일 처리
    pages = []
    for section in CONTENT_DIRS:
        section_dir = plugin_dir / section
        if not section_dir.exists():
            continue

        for md_path in sorted(section_dir.rglob("*.md")):
            if not md_path.is_file():
                continue

            page_info = process_md_file(md_path, plugin_name, section, plugin_dir)
            if page_info:
                pages.append(page_info)
                if verbose:
                    print(f"  생성: {page_info['output_path'].relative_to(DOCS_CONTENT_DIR)}")

    # index.md 생성
    index_path = generate_plugin_index(plugin_name, plugin_data, readme_content, pages)
    if verbose:
        print(f"  인덱스: {index_path.relative_to(DOCS_CONTENT_DIR)}")

    return {
        "name": plugin_name,
        "description": plugin_data.get("description", ""),
        "pages": len(pages),
        "index": index_path,
    }


def clean_generated(verbose: bool = False):
    """이전에 생성된 cc-* 디렉토리 삭제."""
    for item in DOCS_CONTENT_DIR.iterdir():
        if item.is_dir() and item.name.startswith(PLUGIN_PREFIX):
            if verbose:
                print(f"삭제: {item.relative_to(REPO_ROOT)}")
            shutil.rmtree(item)


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    clean = "--clean" in sys.argv

    print("📝 플러그인 문서 생성\n")

    # 이전 생성물 삭제
    clean_generated(verbose)
    if clean:
        print("✅ 클린 완료")
        return 0

    # 플러그인 순회
    plugin_dirs = sorted([
        d for d in PLUGINS_DIR.iterdir()
        if d.is_dir() and d.name.startswith(PLUGIN_PREFIX)
    ])

    if not plugin_dirs:
        print("⚠️  플러그인 디렉토리 없음")
        return 1

    total_pages = 0
    total_plugins = 0

    for plugin_dir in plugin_dirs:
        print(f"📦 {plugin_dir.name}")
        result = process_plugin(plugin_dir, verbose)
        total_pages += result["pages"]
        total_plugins += 1

    # 통계
    index_count = total_plugins
    total_files = total_pages + index_count

    print(f"\n{'='*50}")
    print(f"📊 요약")
    print(f"  플러그인: {total_plugins}")
    print(f"  콘텐츠 페이지: {total_pages}")
    print(f"  인덱스 페이지: {index_count}")
    print(f"  총 생성 파일: {total_files}")
    print(f"\n✅ 문서 생성 완료")

    return 0


if __name__ == "__main__":
    sys.exit(main())

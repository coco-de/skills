#!/usr/bin/env python3
"""
coco-de/skills 플러그인 구조 검증 스크립트

Usage:
    python3 validate_plugins.py [--verbose]
"""

import json
import os
import sys
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).parent
PLUGIN_PREFIX = "cc-"
REQUIRED_FILES = ["plugin.json"]
VALID_DIRS = {"skills", "commands", "agents", "rules", "references", "config",
              "orchestrators", "personas", "checklists", "templates"}
SKILL_FILES = {"SKILL.md", "REFERENCE.md", "TEMPLATES.md"}


class PluginValidator:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.errors = []
        self.warnings = []
        self.stats = {"plugins": 0, "skills": 0, "commands": 0, "agents": 0, "rules": 0}

    def log(self, msg):
        if self.verbose:
            print(f"  {msg}")

    def error(self, msg):
        self.errors.append(msg)
        print(f"  ❌ {msg}")

    def warn(self, msg):
        self.warnings.append(msg)
        if self.verbose:
            print(f"  ⚠️  {msg}")

    def validate_plugin_json(self, plugin_dir: Path) -> Optional[dict]:
        plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
        if not plugin_json_path.exists():
            self.error(f"{plugin_dir.name}: .claude-plugin/plugin.json 없음")
            return None

        try:
            with open(plugin_json_path) as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            self.error(f"{plugin_dir.name}: plugin.json 파싱 오류 - {e}")
            return None

        for field in ["name", "version", "description"]:
            if field not in data:
                self.error(f"{plugin_dir.name}: plugin.json에 '{field}' 필드 없음")

        if "name" in data and data["name"] != plugin_dir.name:
            self.error(f"{plugin_dir.name}: plugin.json name '{data['name']}' != 디렉토리명")

        return data

    def validate_skills(self, plugin_dir: Path):
        skills_dir = plugin_dir / "skills"
        if not skills_dir.exists():
            return

        count = 0
        for item in skills_dir.iterdir():
            if item.is_dir():
                skill_md = item / "SKILL.md"
                if not skill_md.exists():
                    self.error(f"{plugin_dir.name}: skills/{item.name}/SKILL.md 없음")
                else:
                    count += 1
                    self.log(f"스킬: {item.name}")
            elif item.is_file() and item.suffix == ".md":
                count += 1
                self.log(f"스킬 파일: {item.name}")

        self.stats["skills"] += count

    def validate_commands(self, plugin_dir: Path):
        commands_dir = plugin_dir / "commands"
        if not commands_dir.exists():
            return

        count = 0
        for md_file in commands_dir.rglob("*.md"):
            count += 1
            self.log(f"커맨드: {md_file.relative_to(commands_dir)}")

        self.stats["commands"] += count

    def validate_agents(self, plugin_dir: Path):
        agents_dir = plugin_dir / "agents"
        if not agents_dir.exists():
            return

        count = 0
        for md_file in agents_dir.rglob("*.md"):
            count += 1
            self.log(f"에이전트: {md_file.relative_to(agents_dir)}")

        self.stats["agents"] += count

    def validate_rules(self, plugin_dir: Path):
        rules_dir = plugin_dir / "rules"
        if not rules_dir.exists():
            return

        count = 0
        for md_file in rules_dir.rglob("*.md"):
            count += 1
            self.log(f"규칙: {md_file.relative_to(rules_dir)}")

        self.stats["rules"] += count

    def validate_plugin(self, plugin_dir: Path):
        print(f"\n📦 {plugin_dir.name}")
        self.stats["plugins"] += 1

        plugin_data = self.validate_plugin_json(plugin_dir)

        readme = plugin_dir / "README.md"
        if not readme.exists():
            self.warn(f"{plugin_dir.name}: README.md 없음")

        self.validate_skills(plugin_dir)
        self.validate_commands(plugin_dir)
        self.validate_agents(plugin_dir)
        self.validate_rules(plugin_dir)

    def validate_marketplace(self):
        marketplace_path = REPO_ROOT / ".claude-plugin" / "marketplace.json"
        if not marketplace_path.exists():
            self.error("marketplace.json 없음")
            return

        with open(marketplace_path) as f:
            data = json.load(f)

        registered = {p["name"] for p in data.get("plugins", [])}
        actual = {d.name for d in REPO_ROOT.iterdir()
                  if d.is_dir() and d.name.startswith(PLUGIN_PREFIX)}

        for name in actual - registered:
            self.warn(f"marketplace.json에 미등록: {name}")
        for name in registered - actual:
            self.error(f"marketplace.json에 등록되었으나 디렉토리 없음: {name}")

    def run(self):
        print("🔍 coco-de/skills 플러그인 검증\n")
        print(f"레포 경로: {REPO_ROOT}")

        self.validate_marketplace()

        plugin_dirs = sorted([
            d for d in REPO_ROOT.iterdir()
            if d.is_dir() and d.name.startswith(PLUGIN_PREFIX)
        ])

        if not plugin_dirs:
            print("\n⚠️  플러그인 디렉토리 없음")
            return 1

        for plugin_dir in plugin_dirs:
            self.validate_plugin(plugin_dir)

        print(f"\n{'='*50}")
        print(f"📊 요약")
        print(f"  플러그인: {self.stats['plugins']}")
        print(f"  스킬: {self.stats['skills']}")
        print(f"  커맨드: {self.stats['commands']}")
        print(f"  에이전트: {self.stats['agents']}")
        print(f"  규칙: {self.stats['rules']}")
        print(f"  오류: {len(self.errors)}")
        print(f"  경고: {len(self.warnings)}")

        if self.errors:
            print(f"\n❌ {len(self.errors)}개 오류 발견")
            return 1
        else:
            print(f"\n✅ 모든 검증 통과")
            return 0


if __name__ == "__main__":
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    validator = PluginValidator(verbose=verbose)
    sys.exit(validator.run())

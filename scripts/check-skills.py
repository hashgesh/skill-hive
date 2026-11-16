#!/usr/bin/env python3
"""Check that plugins/, the Claude Code marketplace and the docs agree.

Layout: plugins/<plugin>/skills/<skill>/SKILL.md, one folder per plugin.

Rules (shared by Claude Code and OpenCode):
- every plugins/*/skills/<dir>/SKILL.md starts with YAML frontmatter holding only
  `name` and `description`
- `name` equals the directory name, is lowercase kebab-case (max 64) and is
  unique across all plugins
- `description` is non-empty and at most 1024 characters
- every plugin folder has .claude-plugin/plugin.json (name = folder, version),
  README.md and LICENSE, and is listed in .claude-plugin/marketplace.json with
  source ./plugins/<name> and the same version; all plugins share one version
- every skill appears in the README table and in its plugin's README
- INSTALL.md names every plugin and every skill

Usage: python3 scripts/check-skills.py   (run from the repo root)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLUGINS = ROOT / "plugins"
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED_KEYS = {"name", "description"}

errors = []


def error(msg):
    errors.append(msg)


def parse_frontmatter(path):
    text = path.read_text(encoding="utf-8")
    lines = text.split("\n")
    if not lines or lines[0].strip() != "---":
        error(f"{path}: must start with '---' frontmatter")
        return {}
    try:
        end = lines.index("---", 1)
    except ValueError:
        error(f"{path}: frontmatter is not closed with '---'")
        return {}
    fields = {}
    for line in lines[1:end]:
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep or line[0].isspace():
            error(f"{path}: unsupported frontmatter line {line!r} (use single-line 'key: value')")
            continue
        fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def check_skills():
    skills = {}
    for skill_md in sorted(PLUGINS.glob("*/skills/*/SKILL.md")):
        directory = skill_md.parent.name
        plugin = skill_md.parent.parent.parent.name
        if directory in skills:
            error(f"skill {directory!r} exists in both {skills[directory][0]!r} and {plugin!r}")
        fm = parse_frontmatter(skill_md)
        rel = skill_md.relative_to(ROOT)
        extra = set(fm) - ALLOWED_KEYS
        if extra:
            error(f"{rel}: unexpected frontmatter keys {sorted(extra)} (only name, description)")
        name = fm.get("name", "")
        desc = fm.get("description", "")
        if name != directory:
            error(f"{rel}: name {name!r} must equal directory name {directory!r}")
        if not NAME_RE.match(directory) or len(directory) > 64:
            error(f"{rel}: directory {directory!r} must be lowercase kebab-case, max 64 chars")
        if not desc:
            error(f"{rel}: description is missing")
        elif len(desc) > 1024:
            error(f"{rel}: description is {len(desc)} chars (max 1024)")
        skills[directory] = (plugin, rel)
    for d in sorted(PLUGINS.glob("*/skills/*")):
        if d.is_dir() and not (d / "SKILL.md").is_file():
            error(f"{d.relative_to(ROOT)}: missing SKILL.md")
    if not skills:
        error("no skills found under plugins/*/skills/")
    return skills


def check_install_guide(skills, plugins):
    guide = (ROOT / "INSTALL.md").read_text(encoding="utf-8")
    for plugin in plugins:
        if f"{plugin}@skill-hive" not in guide:
            error(f"INSTALL.md: no install command for plugin {plugin!r} ({plugin}@skill-hive)")
    for skill in skills:
        if f"`{skill}`" not in guide:
            error(f"INSTALL.md: skill {skill!r} is not mentioned")


def check_marketplace(skills):
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    entries = {p.get("name", "?"): p for p in data.get("plugins", [])}
    folders = sorted(d.name for d in PLUGINS.iterdir() if d.is_dir())
    for name in folders:
        if name not in entries:
            error(f"plugins/{name} is not listed in .claude-plugin/marketplace.json")
    versions = set()
    for name, entry in entries.items():
        folder = PLUGINS / name
        if entry.get("source") != f"./plugins/{name}":
            error(f"marketplace plugin {name!r}: source must be './plugins/{name}', got {entry.get('source')!r}")
        manifest = folder / ".claude-plugin" / "plugin.json"
        if not manifest.is_file():
            error(f"plugins/{name}: missing .claude-plugin/plugin.json")
            continue
        meta = json.loads(manifest.read_text(encoding="utf-8"))
        if meta.get("name") != name:
            error(f"plugins/{name}/.claude-plugin/plugin.json: name {meta.get('name')!r} must be {name!r}")
        version = meta.get("version")
        if not version:
            error(f"plugins/{name}/.claude-plugin/plugin.json: version is missing")
        elif entry.get("version") not in (None, version):
            error(f"marketplace plugin {name!r}: version {entry.get('version')!r} != plugin.json {version!r}")
        versions.add(version)
        for f in ("README.md", "LICENSE"):
            if not (folder / f).is_file():
                error(f"plugins/{name}: missing {f}")
        readme = folder / "README.md"
        if readme.is_file():
            text = readme.read_text(encoding="utf-8")
            for skill, (plugin, _) in skills.items():
                if plugin == name and f"](skills/{skill}/)" not in text:
                    error(f"plugins/{name}/README.md: no row linking to skills/{skill}/")
    if len(versions) > 1:
        error(f"plugins have different versions {sorted(map(str, versions))}; bump them together")
    return list(entries)


def check_readme(skills):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for skill, (plugin, _) in skills.items():
        if f"](plugins/{plugin}/skills/{skill}/)" not in readme:
            error(f"README.md: skill table has no row linking to plugins/{plugin}/skills/{skill}/")


def main():
    skills = check_skills()
    plugins = check_marketplace(skills)
    check_readme(skills)
    check_install_guide(skills, plugins)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s) found", file=sys.stderr)
        return 1
    print(f"ok: {len(skills)} skills consistent across plugins/, marketplace.json, README.md and INSTALL.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

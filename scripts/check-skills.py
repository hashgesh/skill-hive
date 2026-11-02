#!/usr/bin/env python3
"""Check that skills/, the Claude Code marketplace and the README agree.

Rules (shared by Claude Code and OpenCode):
- every skills/<dir>/SKILL.md starts with YAML frontmatter holding only
  `name` and `description`
- `name` equals the directory name and is lowercase kebab-case (max 64)
- `description` is non-empty and at most 1024 characters
- every skill is listed in exactly one plugin in .claude-plugin/marketplace.json,
  and every listed path exists
- every skill appears in the README table

Usage: python3 scripts/check-skills.py   (run from the repo root)
"""

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
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
    for skill_md in sorted((ROOT / "skills").glob("*/SKILL.md")):
        directory = skill_md.parent.name
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
        skills[directory] = rel
    for d in sorted((ROOT / "skills").iterdir()):
        if d.is_dir() and not (d / "SKILL.md").is_file():
            error(f"skills/{d.name}: missing SKILL.md")
    if not skills:
        error("no skills found under skills/")
    return skills


def check_marketplace(skills):
    path = ROOT / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    owners = {}
    for plugin in data.get("plugins", []):
        pname = plugin.get("name", "?")
        for entry in plugin.get("skills", []):
            target = (ROOT / entry).resolve()
            if not (target / "SKILL.md").is_file():
                error(f"marketplace plugin {pname!r}: {entry} has no SKILL.md")
                continue
            skill = target.name
            if skill in owners:
                error(f"skill {skill!r} is listed in both {owners[skill]!r} and {pname!r}")
            owners[skill] = pname
    for skill in skills:
        if skill not in owners:
            error(f"skill {skill!r} is not listed in any plugin in .claude-plugin/marketplace.json")


def check_readme(skills):
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    for skill in skills:
        if f"](skills/{skill}/)" not in readme:
            error(f"README.md: skill table has no row linking to skills/{skill}/")


def main():
    skills = check_skills()
    check_marketplace(skills)
    check_readme(skills)
    if errors:
        for e in errors:
            print(f"error: {e}", file=sys.stderr)
        print(f"\n{len(errors)} problem(s) found", file=sys.stderr)
        return 1
    print(f"ok: {len(skills)} skills consistent across skills/, marketplace.json and README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())

---
name: changelog
description: Generate changelog using git-cliff. Rust-based CLI that parses conventional commits and generates changelogs.
---

# Changelog Skill

Use [git-cliff](https://git-cliff.org/) to generate changelogs from conventional commits.

## Auto-generate Config & Run

**When this skill is invoked, ask the user:**
1. "Are you releasing a new version?"
2. If yes: Generate changelog and offer to commit
3. If no: Just show preview with `--unreleased`

## Install

```bash
cargo install git-cliff
# or
brew install git-cliff
```

## Configuration

```toml
[changelog]
header = """
# Changelog

All notable changes to this project will be documented in this file.

"""
body = """
{% if version %}\
## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp }}
{% else %}\
## [Unreleased]
{% endif %}

{% for group, commits in commits | group_by(attribute="group") %}
### {{ group }}
{% for commit in commits %}
- {{ commit.message | first_line }} ({% if commit.scope %}{{ commit.scope }}{% else %}root{% endif %})
{% endfor %}
{% endfor %}
"""

[git]
conventional_commits = true
filter_unconventional = true
commit_parsers = [
    { message = "^feat", group = "Features" },
    { message = "^fix", group = "Bug Fixes" },
    { message = "^perf", group = "Performance" },
    { message = "^docs", group = "Documentation" },
    { message = "^refactor", group = "Refactor" },
    { message = "^test", group = "Testing" },
    { message = "^chore", group = "Maintenance" },
]
```

## Common Commands

```bash
git cliff > CHANGELOG.md
git cliff --tag v1.0.0
git cliff --unreleased
git cliff --preview
git cliff 0.1.0..0.2.0
git cliff --all
git cliff -o CHANGELOG.md
git cliff --bump
```

## Conventional Commits

| Type | Description |
|------|-------------|
| feat | New feature |
| fix | Bug fix |
| perf | Performance |
| docs | Documentation |
| refactor | Code refactor |
| test | Tests |
| chore | Maintenance |

## Tips

- Use `--unreleased` to preview upcoming changes
- Configure `cliff.toml` for custom formatting
- Use `--bump` to automatically bump version

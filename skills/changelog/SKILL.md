---
name: changelog
description: Generate or update CHANGELOG.md from git history using git-cliff. Parses conventional commits (including gitmoji-prefixed ones like "✨ feat(scope): ..."), groups them by type, previews unreleased changes, and bumps versions. Use for changelog, release notes, "what changed since last tag", git cliff, cliff.toml.
---

# Changelog Skill

Use [git-cliff](https://git-cliff.org/) to generate changelogs from conventional commits.

## When Invoked

1. Check that `git cliff --version` works. If not, show the install commands below and stop.
2. Check for a `cliff.toml` in the repo root. If missing, offer to create it with the configuration below.
3. Ask: "Are you releasing a new version?"
   - **Yes**: ask for the version (or suggest one with `git cliff --bumped-version`), then run `git cliff --tag {version} -o CHANGELOG.md`, show the diff, and offer to commit.
   - **No**: show a preview only with `git cliff --unreleased` (prints to stdout, writes nothing).

## Install

```bash
cargo install git-cliff
# or
brew install git-cliff
```

## Configuration

Save as `cliff.toml` in the repo root.

```toml
[changelog]
header = """
# Changelog

All notable changes to this project will be documented in this file.

"""
body = """
{% if version %}\
## [{{ version | trim_start_matches(pat="v") }}] - {{ timestamp | date(format="%Y-%m-%d") }}
{% else %}\
## [Unreleased]
{% endif %}\
{% for group, commits in commits | group_by(attribute="group") %}
### {{ group | striptags | trim }}
{% for commit in commits %}
- {% if commit.scope %}**{{ commit.scope }}:** {% endif %}{{ commit.message | upper_first }}\
{% if commit.breaking %} (**BREAKING**){% endif %}\
{% endfor %}
{% endfor %}\n
"""
trim = true

[git]
conventional_commits = true
filter_unconventional = true
# Strip a leading gitmoji (":sparkles: " or "✨ ") so "✨ feat(x): y" parses as "feat(x): y".
# Rewrite merge commits ("Merge pull request #4 ...", "Merge branch ...",
# "Merge <sha> into <sha>") so they are skipped below instead of being
# reported as parse errors. No conventional commit starts with "Merge ".
commit_preprocessors = [
    { pattern = '^:[a-z0-9_+-]+:\s*', replace = "" },
    { pattern = '^[^\x00-\x7F]+\s*', replace = "" },
    { pattern = '^Merge .*', replace = "chore(merge): merge" },
]
commit_parsers = [
    { message = "^chore\\(merge\\)", skip = true },
    { message = "^feat", group = "<!-- 0 -->Features" },
    { message = "^fix", group = "<!-- 1 -->Bug Fixes" },
    { message = "^perf", group = "<!-- 2 -->Performance" },
    { message = "^refactor", group = "<!-- 3 -->Refactor" },
    { message = "^docs", group = "<!-- 4 -->Documentation" },
    { message = "^style", group = "<!-- 5 -->Style" },
    { message = "^test", group = "<!-- 6 -->Testing" },
    { message = "^build", group = "<!-- 7 -->Build" },
    { message = "^ci", group = "<!-- 8 -->CI" },
    { message = "^chore\\(release\\)", skip = true },
    { message = "^release", skip = true },
    { message = "^chore", group = "<!-- 9 -->Maintenance" },
]
```

The `<!-- n -->` prefixes only control group order; `striptags` removes them from the output.

## Common Commands

```bash
git cliff --unreleased              # preview unreleased changes (stdout)
git cliff -o CHANGELOG.md           # regenerate the whole file
git cliff --tag v1.0.0 -o CHANGELOG.md   # treat unreleased commits as v1.0.0
git cliff --unreleased --tag v1.0.0 --prepend CHANGELOG.md  # add only the new section
git cliff --bumped-version          # print the next semver based on commits
git cliff --bump -o CHANGELOG.md    # bump and write in one step
git cliff v0.1.0..v0.2.0            # a specific range
git cliff --latest                  # only the latest release
```

> Without `-o` / `--prepend`, git-cliff only prints to stdout.

## Conventional Commits

| Type | Group |
|------|-------|
| feat | Features |
| fix | Bug Fixes |
| perf | Performance |
| refactor | Refactor |
| docs | Documentation |
| style | Style |
| test | Testing |
| build | Build |
| ci | CI |
| chore | Maintenance |

Breaking changes (`feat!:` or a `BREAKING CHANGE:` footer) are marked **BREAKING**.

## Tips

- Use `--unreleased` to preview upcoming changes before tagging
- Use `--bumped-version` to let the commit types decide the next version
- If the changelog comes out empty, check that commits follow the conventional format (`git log --oneline`); unconventional commits are filtered out

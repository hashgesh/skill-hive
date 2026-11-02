<div align="center">
  <img src="assets/logo.png" width="400" height="400" alt="skill-hive logo"/>
  <p>Skills for git workflow, code quality and code understanding, for <b>Claude Code</b> and <b>OpenCode</b></p>
</div>

## Install with an AI agent

Paste this into Claude Code or OpenCode and it will install skill-hive for you (it asks before changing anything):

```text
Install skill-hive for me by following the instructions at
https://raw.githubusercontent.com/halilibrahimonus/skill-hive/main/INSTALL.md
```

[INSTALL.md](INSTALL.md) covers both tools: the Claude Code marketplace, the OpenCode config, verification, optional CLI tools, updating and uninstalling. The manual steps are below.

## Skills

The same `skills/<name>/SKILL.md` files are used by both tools. In Claude Code they are grouped into three plugins.

| Skill | Plugin | Description | Requires |
|-------|--------|-------------|----------|
| [branch](skills/branch/) | `git-workflow` | Create a well-named branch from the right base | `git`, `gh` (optional) |
| [changelog](skills/changelog/) | `git-workflow` | Generate changelog with git-cliff | `git-cliff` |
| [conventional-commit](skills/conventional-commit/) | `git-workflow` | Conventional commits with gitmoji | `git` |
| [pull-request](skills/pull-request/) | `git-workflow` | Auto-generate PR summary | `gh` or `glab` (optional) |
| [release](skills/release/) | `git-workflow` | Create release with changelog and tag | `git-cliff`, `gh` (optional) |
| [review](skills/review/) | `git-workflow` | Auto-review PRs with analysis | `gh` |
| [cpp-linter](skills/cpp-linter/) | `code-quality` | C++ code style checker | `clang-format`, `clang-tidy`, `cppcheck` |
| [js-linter](skills/js-linter/) | `code-quality` | JS/TS lint, format and type check | `eslint`, `prettier`, `tsc` |
| [python-linter](skills/python-linter/) | `code-quality` | Python lint, format and type check | `ruff`, `mypy` (optional) |
| [refactor](skills/refactor/) | `code-quality` | Code analysis and refactoring patterns | `ast-grep` (optional) |
| [tech-debt](skills/tech-debt/) | `code-quality` | Technical debt register: markers, hotspots, duplication, outdated deps | `git`, `rg`, `lizard`/`jscpd` (optional) |
| [code-history](skills/code-history/) | `code-insight` | Explain why code looks the way it does, from git history, PRs and issues | `git`, `gh` (optional) |
| [codebase-tour](skills/codebase-tour/) | `code-insight` | Guided tour of a repo: stack, commands, map, entry points, reading list | `git`, `rg`, `scc`/`tokei` (optional) |

The CLIs are not bundled; install the ones you need (each skill lists install commands).

## Claude Code (manual)

Add the marketplace and install one or both plugins:

```
/plugin marketplace add halilibrahimonus/skill-hive
/plugin install git-workflow@skill-hive
/plugin install code-quality@skill-hive
/plugin install code-insight@skill-hive
```

On Claude Code 2.1.275 or later you can do it in one step:

```
/plugin install git-workflow --marketplace halilibrahimonus/skill-hive
```

Skills are namespaced by plugin, e.g. `/git-workflow:changelog`, `/code-quality:cpp-linter` or `/code-insight:codebase-tour`, and Claude also picks them automatically from their descriptions. Update with `/plugin marketplace update skill-hive`.

## OpenCode (manual)

Clone the repo and add its `skills/` directory to the `skills` array in `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "skills": ["/path/to/skill-hive/skills"]
}
```

OpenCode loads `<dir>/<skill-name>/SKILL.md` directly, so the active skills follow the checked-out branch; update with `git pull`. Check with `opencode debug skill` — a path that doesn't exist is ignored silently. The old `opencode/` path still works (it is a symlink to `skills/`).

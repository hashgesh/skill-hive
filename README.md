<div align="center">
  <img src="assets/logo.png" width="400" height="400" alt="skill-hive logo"/>
  <p>Skills for git workflow automation and code quality, for <b>Claude Code</b> and <b>OpenCode</b></p>
</div>

## Skills

The same `skills/<name>/SKILL.md` files are used by both tools. In Claude Code they are grouped into two plugins.

| Skill | Plugin | Description | Requires |
|-------|--------|-------------|----------|
| [changelog](skills/changelog/) | `git-workflow` | Generate changelog with git-cliff | `git-cliff` |
| [conventional-commit](skills/conventional-commit/) | `git-workflow` | Conventional commits with gitmoji | `git` |
| [pull-request](skills/pull-request/) | `git-workflow` | Auto-generate PR summary | `gh` or `glab` (optional) |
| [release](skills/release/) | `git-workflow` | Create release with changelog and tag | `git-cliff`, `gh` (optional) |
| [review](skills/review/) | `git-workflow` | Auto-review PRs with analysis | `gh` |
| [cpp-linter](skills/cpp-linter/) | `code-quality` | C++ code style checker | `clang-format`, `clang-tidy`, `cppcheck` |
| [refactor](skills/refactor/) | `code-quality` | Code analysis and refactoring patterns | `ast-grep` (optional) |

The CLIs are not bundled; install the ones you need (each skill lists install commands).

## Claude Code

Add the marketplace and install one or both plugins:

```
/plugin marketplace add halilibrahimonus/skill-hive
/plugin install git-workflow@skill-hive
/plugin install code-quality@skill-hive
```

On Claude Code 2.1.275 or later you can do it in one step:

```
/plugin install git-workflow --marketplace halilibrahimonus/skill-hive
```

Skills are namespaced by plugin, e.g. `/git-workflow:changelog` or `/code-quality:cpp-linter`, and Claude also picks them automatically from their descriptions. Update with `/plugin marketplace update skill-hive`.

## OpenCode

Clone the repo and add its `skills/` directory to the `skills` array in `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "skills": ["/path/to/skill-hive/skills"]
}
```

OpenCode loads `<dir>/<skill-name>/SKILL.md` directly, so the active skills follow the checked-out branch. The old `opencode/` path still works (it is a symlink to `skills/`).

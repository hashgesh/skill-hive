<div align="center">
  <img src="assets/logo.png" width="400" height="400" alt="skill-hive logo"/>
  <p>OpenCode skills for git workflow automation</p>
</div>

## Skills

| Skill | Description | Requires |
|-------|-------------|----------|
| [changelog](opencode/changelog/) | Generate changelog with git-cliff | `git-cliff` |
| [conventional-commit](opencode/conventional-commit/) | Conventional commits with gitmoji | `git` |
| [cpp-linter](opencode/cpp-linter/) | C++ code style checker | `clang-format`, `clang-tidy`, `cppcheck` |
| [pull-request](opencode/pull-request/) | Auto-generate PR summary | `gh` or `glab` (optional) |
| [refactor](opencode/refactor/) | Code analysis and refactoring patterns | `ast-grep` (optional) |
| [release](opencode/release/) | Create release with changelog and tag | `git-cliff`, `gh` (optional) |
| [review](opencode/review/) | Auto-review PRs with analysis | `gh` |

## Installation

Clone the repo and add its `opencode/` directory to the `skills` array in `~/.config/opencode/opencode.jsonc`:

```jsonc
{
  "skills": ["/path/to/skill-hive/opencode"]
}
```

OpenCode loads `<dir>/<skill-name>/SKILL.md` directly, so the active skills follow the checked-out branch. The CLIs in the table are not bundled; install the ones you need (each skill lists install commands).

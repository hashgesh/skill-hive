# code-quality

Part of [skill-hive](https://github.com/hashgesh/skill-hive): agent skills for Claude Code and OpenCode.

Agent skills that run real linters, formatters and type checkers instead of guessing: clang-format, clang-tidy and cppcheck for C/C++, ruff and mypy for Python, ESLint, Prettier and tsc for JavaScript/TypeScript, plus structural refactoring with ast-grep and a technical debt audit.

## Install

```
/plugin install code-quality --marketplace hashgesh/skill-hive
```

or `/plugin marketplace add hashgesh/skill-hive` and then `/plugin install code-quality@skill-hive`. Skills are namespaced, e.g. `/code-quality:cpp-linter`, and Claude also picks them automatically from their descriptions.

## Skills

| Skill | Description | Requires |
|-------|-------------|----------|
| [cpp-linter](skills/cpp-linter/) | C++ code style checker | `clang-format`, `clang-tidy`, `cppcheck` |
| [js-linter](skills/js-linter/) | JS/TS lint, format and type check | `eslint`, `prettier`, `tsc` |
| [python-linter](skills/python-linter/) | Python lint, format and type check | `ruff`, `mypy` (optional) |
| [refactor](skills/refactor/) | Code analysis and refactoring patterns | `ast-grep` (optional) |
| [tech-debt](skills/tech-debt/) | Technical debt register: markers, hotspots, duplication, outdated deps | `git`, `rg`, `lizard`/`jscpd` (optional) |

The CLIs are not bundled; each skill checks for its tools and shows the install command when one is missing.

## What it runs

The skills run the linters and analysis tools listed above on your local files and report what they find; fixes (`--fix`, `--write`, ast-grep rewrites) are applied only when you ask. The tech-debt skill also asks your package manager about outdated dependencies (`npm outdated`, `pip list --outdated`, which query the package registry), writes `TECH_DEBT.md` after showing you the diff, and opens GitHub issues with `gh` only if you ask it to.

## License

MIT, see [LICENSE](LICENSE).

# code-insight

Part of [skill-hive](https://github.com/hashgesh/skill-hive): agent skills for Claude Code and OpenCode.

Agent skills for understanding a codebase: a guided tour of an unfamiliar repository (stack, commands, directory map, entry points, reading list) and code archaeology that explains why code looks the way it does from git history, pull requests and issues.

## Install

```
/plugin install code-insight --marketplace hashgesh/skill-hive
```

or `/plugin marketplace add hashgesh/skill-hive` and then `/plugin install code-insight@skill-hive`. Skills are namespaced, e.g. `/code-insight:code-history`, and Claude also picks them automatically from their descriptions.

## Skills

| Skill | Description | Requires |
|-------|-------------|----------|
| [code-history](skills/code-history/) | Explain why code looks the way it does, from git history, PRs and issues | `git`, `gh` (optional) |
| [codebase-tour](skills/codebase-tour/) | Guided tour of a repo: stack, commands, map, entry points, reading list | `git`, `rg`, `scc`/`tokei` (optional) |

The CLIs are not bundled; each skill checks for its tools and shows the install command when one is missing.

## What it runs

The skills read your local files and git history with `git`, `rg` and optionally `scc`/`tokei`, and use `gh` (read-only) to look up pull requests and issues when it is available. They don't change your code; codebase-tour writes `ONBOARDING.md` only if you accept its offer to save the tour.

## License

MIT, see [LICENSE](LICENSE).

# AGENTS.md

## What this repo is
A collection of OpenCode **skill** definitions (Markdown). There is no application, build, test, lint, or codegen step, and no root manifest or CI. Don't look for `package.json`, a test suite, or a compile command — the files are the product.

## Layout
- `opencode/<skill-name>/SKILL.md` — one directory per skill. OpenCode derives the skill ID from this path, not from the frontmatter `name`. Skills: `changelog`, `conventional-commit`, `release`, `cpp-linter`, `pull-request`, `refactor`, `review`.
- `README.md` — skill table. Update it whenever a skill is added or renamed.
- `assets/` — repo logo. `LICENSE` — MIT.

## Adding / editing a skill
- Every `SKILL.md` starts with YAML frontmatter `name` + `description`. `description` is what OpenCode uses to advertise the skill, so keep it keyword- and trigger-rich.
- This repo is registered with OpenCode through the `skills` array in the global `~/.config/opencode/opencode.jsonc`, pointing at this repo's `opencode/` directory. OpenCode loads `<root>/<name>/SKILL.md` directly — no copy or symlink step. The live skill set therefore follows the checked-out branch.
- Keep the directory name a lowercase kebab-case ID; it must be unique.

## Git workflow
- `develop` is the integration branch; add skills there, then merge to `main`.
- Commits use conventional commits **with a gitmoji prefix and a scope when applicable**: `✨ feat(refactor): add refactor skill`, `📝 docs(cpp-linter): add ...`. Follow the existing history.
- Skills wrap external CLIs the user must install: `git-cliff`, `gh`/`glab`, `ast-grep`, `clang-format`/`clang-tidy`/`cppcheck` (`gitmoji-cli` is optional). Don't assume they're present; each skill should check for its tool and show install commands.
- Verify every command and flag a skill tells the agent to run (e.g. install the tool in a scratch dir and run it). Prefer non-interactive commands and `--body-file`/`-F` over inline quoted bodies.
- The changelog skill's `cliff.toml` strips the leading gitmoji before parsing; keep it in sync with the conventional-commit mapping.

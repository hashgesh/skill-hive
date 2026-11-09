# AGENTS.md

## What this repo is
A collection of agent **skill** definitions (Markdown) shared by **Claude Code** (as a plugin marketplace) and **OpenCode**. There is no application, build, or codegen step and no `package.json` — the files are the product. CI only checks the skill files (see below).

## Layout
- `skills/<skill-name>/SKILL.md` — one directory per skill, the single source of truth for both tools. Skills: `branch`, `changelog`, `code-history`, `codebase-tour`, `conventional-commit`, `cpp-linter`, `js-linter`, `pull-request`, `python-linter`, `refactor`, `release`, `review`, `tech-debt`.
- `.claude-plugin/marketplace.json` — Claude Code marketplace `skill-hive`. Each plugin entry uses `"source": "./"` and lists its skill directories under `skills`:
  - `git-workflow`: branch, changelog, conventional-commit, pull-request, release, review
  - `code-quality`: cpp-linter, js-linter, python-linter, refactor, tech-debt
  - `code-insight`: code-history, codebase-tour
- `scripts/check-skills.py` — checks frontmatter (`name` = directory, kebab-case, only `name`/`description`, description ≤1024), that every skill is in exactly one marketplace plugin, and that the README table links it.
- `scripts/test-changelog.sh` — extracts the `cliff.toml` from `skills/changelog/SKILL.md` and tests it with git-cliff on gitmoji commits and on this repo's history.
- `.github/workflows/validate.yml` — runs both scripts and `claude plugin validate --strict .` on pushes to `main` and on PRs.
- `INSTALL.md` — step-by-step install guide written for an AI agent (Claude Code or OpenCode); the README tells users to point their agent at its raw `main` URL. Keep its plugin/skill tables, expected `claude plugin details` output and skill count in sync with the marketplace.
- `README.md` — skill table and install instructions for both tools. `assets/` — logo. `LICENSE` — MIT.

## Adding / editing a skill
- Every `SKILL.md` starts with YAML frontmatter with only `name` + `description` (both tools read these; don't add tool-specific fields). `name` must equal the directory name: lowercase kebab-case, unique. `description` (max 1024 chars) is what both tools use to decide when to load the skill, so keep it keyword- and trigger-rich.
- Keep skill bodies tool-neutral: no OpenCode- or Claude-specific tool names. Refer to other skills by bare name ("the changelog skill"); in Claude Code they appear namespaced (`git-workflow:changelog`).
- When adding a skill: add it to a plugin's `skills` list in `.claude-plugin/marketplace.json` (or a new plugin entry), to the README table, **and** to INSTALL.md (plugin table, expected output, skill list, CLI tools).
- Before pushing, run what CI runs: `python3 scripts/check-skills.py`, `claude plugin validate --strict .`, and `scripts/test-changelog.sh` if you touched the changelog skill (needs `git-cliff`).
- Plugin entries have no `version`, so Claude Code users get every pushed commit on `/plugin marketplace update`. Add a `version` only if releases should be pinned.
- OpenCode is registered through the `skills` array in `~/.config/opencode/opencode.jsonc` pointing at this repo's `skills/` directory; it loads `<root>/<name>/SKILL.md` directly, so the live skill set follows the checked-out branch.

## Git workflow
- `main` is the only long-lived branch and the one users install from. For every change, create a short-lived branch from `main` (`feat/…`, `fix/…`, `docs/…`; the branch skill does this), open a PR into `main`, and merge it once CI is green. Don't push directly to `main`.
- Commits use conventional commits **with a gitmoji prefix and a scope when applicable**: `✨ feat(refactor): add refactor skill`, `📝 docs(cpp-linter): add ...`. Follow the existing history.
- Skills wrap external CLIs the user must install: `git-cliff`, `gh`/`glab`, `ast-grep`, `clang-format`/`clang-tidy`/`cppcheck`, `ruff`/`mypy`, `eslint`/`prettier`, `rg`/`lizard`/`jscpd`, `scc`/`tokei` (`gitmoji-cli` is optional). Don't assume they're present; each skill should check for its tool and show install commands.
- Verify every command and flag a skill tells the agent to run (e.g. install the tool in a scratch dir and run it). Prefer non-interactive commands and `--body-file`/`-F` over inline quoted bodies.
- The changelog skill's `cliff.toml` strips the leading gitmoji before parsing; keep it in sync with the conventional-commit mapping.

# AGENTS.md

## What this repo is
A collection of agent **skill** definitions (Markdown) shared by **Claude Code** (as a plugin marketplace) and **OpenCode**. There is no application, build, or codegen step and no `package.json` — the files are the product. CI only checks the skill files (see below).

## Layout
- `skills/<skill-name>/SKILL.md` — one directory per skill, the single source of truth for both tools. Skills: `changelog`, `conventional-commit`, `release`, `cpp-linter`, `pull-request`, `refactor`, `review`.
- `.claude-plugin/marketplace.json` — Claude Code marketplace `skill-hive`. Each plugin entry uses `"source": "./"` and lists its skill directories under `skills`:
  - `git-workflow`: changelog, conventional-commit, pull-request, release, review
  - `code-quality`: cpp-linter, refactor
- `opencode` — symlink to `skills/`, kept so existing OpenCode configs pointing at `opencode/` keep working. Don't put files in it.
- `scripts/check-skills.py` — checks frontmatter (`name` = directory, kebab-case, only `name`/`description`, description ≤1024), that every skill is in exactly one marketplace plugin, and that the README table links it.
- `scripts/test-changelog.sh` — extracts the `cliff.toml` from `skills/changelog/SKILL.md` and tests it with git-cliff on gitmoji commits and on this repo's history.
- `.github/workflows/validate.yml` — runs both scripts and `claude plugin validate --strict .` on pushes to main/develop and on PRs.
- `README.md` — skill table and install instructions for both tools. `assets/` — logo. `LICENSE` — MIT.

## Adding / editing a skill
- Every `SKILL.md` starts with YAML frontmatter with only `name` + `description` (both tools read these; don't add tool-specific fields). `name` must equal the directory name: lowercase kebab-case, unique. `description` (max 1024 chars) is what both tools use to decide when to load the skill, so keep it keyword- and trigger-rich.
- Keep skill bodies tool-neutral: no OpenCode- or Claude-specific tool names. Refer to other skills by bare name ("the changelog skill"); in Claude Code they appear namespaced (`git-workflow:changelog`).
- When adding a skill: add it to a plugin's `skills` list in `.claude-plugin/marketplace.json` (or a new plugin entry) **and** to the README table.
- Before pushing, run what CI runs: `python3 scripts/check-skills.py`, `claude plugin validate --strict .`, and `scripts/test-changelog.sh` if you touched the changelog skill (needs `git-cliff`).
- Plugin entries have no `version`, so Claude Code users get every pushed commit on `/plugin marketplace update`. Add a `version` only if releases should be pinned.
- OpenCode is registered through the `skills` array in `~/.config/opencode/opencode.jsonc` pointing at this repo's `skills/` directory; it loads `<root>/<name>/SKILL.md` directly, so the live skill set follows the checked-out branch.

## Git workflow
- `develop` is the integration branch; add skills there, then merge to `main`.
- Commits use conventional commits **with a gitmoji prefix and a scope when applicable**: `✨ feat(refactor): add refactor skill`, `📝 docs(cpp-linter): add ...`. Follow the existing history.
- Skills wrap external CLIs the user must install: `git-cliff`, `gh`/`glab`, `ast-grep`, `clang-format`/`clang-tidy`/`cppcheck` (`gitmoji-cli` is optional). Don't assume they're present; each skill should check for its tool and show install commands.
- Verify every command and flag a skill tells the agent to run (e.g. install the tool in a scratch dir and run it). Prefer non-interactive commands and `--body-file`/`-F` over inline quoted bodies.
- The changelog skill's `cliff.toml` strips the leading gitmoji before parsing; keep it in sync with the conventional-commit mapping.

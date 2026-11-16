# AGENTS.md

## What this repo is
A collection of agent **skill** definitions (Markdown) shared by **Claude Code** (as a plugin marketplace) and **OpenCode**. There is no application, build, or codegen step and no `package.json` — the files are the product. CI only checks the skill files (see below).

## Layout
- `plugins/<plugin>/` — one folder per plugin, each submittable to the Claude plugin directory on its own: `.claude-plugin/plugin.json` (name, version, license, …), `.claude-plugin/icon.png` (1024x1024; the directory takes it only on the first submission), `README.md` (≥40 words, says what the skills run), `LICENSE` (a copy of the root one — symlinks aren't allowed) and `skills/<skill-name>/SKILL.md`, the single source of truth for both tools. Skills: `branch`, `changelog`, `code-history`, `codebase-tour`, `conventional-commit`, `cpp-linter`, `js-linter`, `pull-request`, `python-linter`, `refactor`, `release`, `review`, `tech-debt`.
- `.claude-plugin/marketplace.json` — Claude Code marketplace `skill-hive`. Each plugin entry uses `"source": "./plugins/<name>"`; skills are discovered from that folder's `skills/`. Never add a `.claude-plugin/plugin.json` at the repo root: it renames every plugin whose source is the root. Plugins:
  - `git-workflow`: branch, changelog, conventional-commit, pull-request, release, review
  - `code-quality`: cpp-linter, js-linter, python-linter, refactor, tech-debt
  - `code-insight`: code-history, codebase-tour
- `scripts/check-skills.py` — checks frontmatter (`name` = directory, kebab-case, unique, only `name`/`description`, description ≤1024), that every plugin folder has `plugin.json`/`README.md`/`LICENSE` and is in the marketplace with the same version, that all plugins share one version, and that the root and plugin READMEs and INSTALL.md list every skill.
- `scripts/test-changelog.sh` — extracts the `cliff.toml` from `plugins/git-workflow/skills/changelog/SKILL.md` and tests it with git-cliff on gitmoji commits and on this repo's history.
- `.github/workflows/validate.yml` — runs both scripts, `claude plugin validate --strict .` and `claude plugin validate --strict plugins/<name>` for each plugin on pushes to `main` and on PRs.
- `INSTALL.md` — step-by-step install guide written for an AI agent (Claude Code or OpenCode); the README tells users to point their agent at its raw `main` URL. Keep its plugin/skill tables, expected `claude plugin details` output and skill count in sync with the marketplace.
- `README.md` — skill table and install instructions for both tools. `assets/` — `banner.svg` (README banner, 1280x640) and the older `logo.png`. `LICENSE` — MIT.

## Adding / editing a skill
- Every `SKILL.md` starts with YAML frontmatter with only `name` + `description` (both tools read these; don't add tool-specific fields). `name` must equal the directory name: lowercase kebab-case, unique. `description` (max 1024 chars) is what both tools use to decide when to load the skill, so keep it keyword- and trigger-rich.
- Keep skill bodies tool-neutral: no OpenCode- or Claude-specific tool names. Refer to other skills by bare name ("the changelog skill"); in Claude Code they appear namespaced (`git-workflow:changelog`).
- When adding a skill: create it under a plugin's `skills/` folder (or a new `plugins/<name>/` with its own `plugin.json`, icon, README, LICENSE and marketplace entry), and add it to the root README table, the plugin's README table **and** INSTALL.md (plugin table, expected output, skill list, CLI tools).
- Before pushing, run what CI runs: `python3 scripts/check-skills.py`, `claude plugin validate --strict .`, and `scripts/test-changelog.sh` if you touched the changelog skill (needs `git-cliff`).
- Plugins are pinned with `version` in each `plugins/<name>/.claude-plugin/plugin.json` and its marketplace entry (all equal), so Claude Code users only get changes when it is bumped. When cutting a release (the release skill), bump `version` in every `plugin.json` and marketplace entry to the new semver in the same commit as the changelog, then tag `vX.Y.Z`. Title the GitHub Release `skill-hive vX.Y.Z` (e.g. `gh release create vX.Y.Z --title "skill-hive vX.Y.Z" ...`) to match the existing releases.
- OpenCode is registered through the `skills` array in `~/.config/opencode/opencode.jsonc` pointing at each plugin's `plugins/<name>/skills` directory; it loads `<root>/<name>/SKILL.md` directly, so the live skill set follows the checked-out branch.

## Git workflow
- `main` is the only long-lived branch and the one users install from. For every change, create a short-lived branch from `main` (`feat/…`, `fix/…`, `docs/…`; the branch skill does this), open a PR into `main`, and merge it once CI is green. Don't push directly to `main`.
- Commits use conventional commits **with a gitmoji prefix and a scope when applicable**: `✨ feat(refactor): add refactor skill`, `📝 docs(cpp-linter): add ...`. Follow the existing history.
- Skills wrap external CLIs the user must install: `git-cliff`, `gh`/`glab`, `ast-grep`, `clang-format`/`clang-tidy`/`cppcheck`, `ruff`/`mypy`, `eslint`/`prettier`, `rg`/`lizard`/`jscpd`, `scc`/`tokei` (`gitmoji-cli` is optional). Don't assume they're present; each skill should check for its tool and show install commands.
- Verify every command and flag a skill tells the agent to run (e.g. install the tool in a scratch dir and run it). Prefer non-interactive commands and `--body-file`/`-F` over inline quoted bodies.
- The changelog skill's `cliff.toml` strips the leading gitmoji before parsing; keep it in sync with the conventional-commit mapping.

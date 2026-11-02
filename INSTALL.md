# skill-hive — installation guide for AI agents

> **You are an AI coding agent (Claude Code, OpenCode, or similar) and the user asked you to install skill-hive.**
> Follow these steps in order. Run the commands yourself, but **ask the user before every step that changes their machine or config**, and show what you will change. Never use `sudo` without asking. At the end, report exactly what was installed and where.

skill-hive is a set of agent skills (`skills/<name>/SKILL.md`) that work in both **Claude Code** and **OpenCode**:

| Plugin (Claude Code) | Skills |
|----------------------|--------|
| `git-workflow` | `changelog`, `conventional-commit`, `pull-request`, `release`, `review` |
| `code-quality` | `cpp-linter`, `js-linter`, `python-linter`, `refactor` |

Repository: `https://github.com/halilibrahimonus/skill-hive`

---

## Step 1 — Detect the tools

Run:

```bash
claude --version
opencode --version
git --version
```

Tell the user which of Claude Code and OpenCode are installed, then ask:

1. **Install for which tool(s)?** Claude Code, OpenCode, or both (offer only the installed ones).
2. **Which plugins?** `git-workflow`, `code-quality`, or both (default: both). For OpenCode all skills come together; this choice only matters for Claude Code.

If neither tool is installed, stop and tell the user to install one first.

## Step 2 — Claude Code

Skip if the user didn't choose Claude Code.

1. Add the marketplace (safe to re-run; it reports "already on disk" if present):

   ```bash
   claude plugin marketplace add halilibrahimonus/skill-hive
   ```

2. Install each chosen plugin for the user (safe to re-run):

   ```bash
   claude plugin install git-workflow@skill-hive
   claude plugin install code-quality@skill-hive
   ```

   Default scope is `user` (all projects). If the user wants it only for the current project, add `--scope project`; this enables the plugin in the project's `.claude/settings.json`.

3. Verify — each must list its skills:

   ```bash
   claude plugin details git-workflow
   claude plugin details code-quality
   ```

   Expected: `Skills (5)  changelog, conventional-commit, pull-request, release, review` and `Skills (4)  cpp-linter, js-linter, python-linter, refactor`.

4. Tell the user to restart Claude Code (or run `/reload-plugins` in a session). Skills are namespaced: `/git-workflow:changelog`, `/code-quality:python-linter`, and Claude also picks them automatically from their descriptions.

> If you are running *inside* Claude Code and `claude` commands are unavailable, give the user these to type instead:
> `/plugin marketplace add halilibrahimonus/skill-hive`, then `/plugin install git-workflow@skill-hive` and `/plugin install code-quality@skill-hive`.

## Step 3 — OpenCode

Skip if the user didn't choose OpenCode.

OpenCode loads skills from directories listed in its config, so it needs a local clone.

1. **Pick a clone location.** Default: `~/.local/share/skill-hive` (ask the user if they prefer another). If that directory already contains a skill-hive clone, update it with `git -C <dir> pull --ff-only` instead of cloning again.

   ```bash
   git clone https://github.com/halilibrahimonus/skill-hive.git ~/.local/share/skill-hive
   ```

2. **Find the global config file**: `~/.config/opencode/opencode.jsonc`, or `~/.config/opencode/opencode.json` if that one exists instead. Create `opencode.jsonc` if neither exists. Read the file first.

3. **Add the skills directory** — the `skills` folder inside the clone, as an absolute path or starting with `~/`. Edit the file in place, keeping every existing setting and comment (it may be JSONC). Show the user the change before saving. Handle the existing shape:

   - No `skills` key → add `"skills": ["~/.local/share/skill-hive/skills"]`
   - `"skills": [ ... ]` (array) → append the path if it's not already there
   - `"skills": { "paths": [ ... ] }` (object) → append to `paths` if it's not already there

   Minimal resulting file when it was empty:

   ```jsonc
   {
     "$schema": "https://opencode.ai/config.json",
     "skills": ["~/.local/share/skill-hive/skills"]
   }
   ```

   Older setups may point at `<clone>/opencode` — that still works (it is a symlink to `skills/`); leave it or replace it with `<clone>/skills`, but don't list both.

4. **Verify.** OpenCode silently ignores a path that doesn't exist, so always check:

   ```bash
   opencode debug skill
   ```

   The output is JSON; it must contain entries whose `location` is under `<clone>/skills/` for all 9 skills: `changelog`, `conventional-commit`, `cpp-linter`, `js-linter`, `pull-request`, `python-linter`, `refactor`, `release`, `review`. If they are missing, re-check the path in the config.

5. Tell the user to restart OpenCode; config is loaded only at startup.

> **Don't** symlink skill-hive into `~/.claude/skills` when Claude Code has the plugins installed: OpenCode also reads `~/.claude/skills`, but Claude Code would then load every skill twice (once from the plugin, once as a personal skill).

## Step 4 — Optional CLI tools

The skills call external CLIs and check for them at run time, so nothing breaks if they are missing. Show the user this table, mark which tools are already on PATH (`command -v <tool>`), and offer to install the missing ones for the skills they care about. Ask before installing anything.

| Skill | Tools | Install |
|-------|-------|---------|
| changelog, release | `git-cliff` | `cargo install git-cliff` · `brew install git-cliff` · `pip install git-cliff` |
| pull-request, review, release | `gh` (GitHub) or `glab` (GitLab) | `brew install gh` · see https://cli.github.com |
| cpp-linter | `clang-format`, `clang-tidy`, `cppcheck` | `sudo apt install clang-format clang-tidy cppcheck` · `brew install clang-format llvm cppcheck` |
| python-linter | `ruff`, `mypy` | `pip install ruff mypy` · `uv tool install ruff` · `brew install ruff mypy` |
| js-linter | `eslint`, `prettier`, `tsc` | per project: `npm i -D eslint @eslint/js globals prettier typescript` |
| refactor | `ast-grep` | `cargo install ast-grep --locked` · `npm i -g @ast-grep/cli` · `brew install ast-grep` |

`conventional-commit` only needs `git`.

## Step 5 — Report

Summarize for the user:

- Claude Code: marketplace added (yes/no), plugins installed and their scope, result of `claude plugin details`
- OpenCode: clone location, config file and the line you added, number of skill-hive skills in `opencode debug skill`
- CLI tools installed or still missing
- What to restart

---

## Updating

- **Claude Code:** `claude plugin marketplace update skill-hive`, then `claude plugin update git-workflow@skill-hive` and `claude plugin update code-quality@skill-hive`; restart.
- **OpenCode:** `git -C ~/.local/share/skill-hive pull --ff-only`; restart.

## Uninstalling

- **Claude Code:** `claude plugin uninstall git-workflow@skill-hive`, `claude plugin uninstall code-quality@skill-hive`, then `claude plugin marketplace remove skill-hive`.
- **OpenCode:** remove the skill-hive path from `skills` in the config, then delete the clone (ask first).

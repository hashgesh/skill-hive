# skill-hive — installation guide for AI agents

> **You are an AI coding agent (Claude Code, OpenCode, or similar) and the user asked you to install skill-hive.**
> Follow these steps in order. Run the commands yourself, but **ask the user before every step that changes their machine or config**, and show what you will change. Never use `sudo` without asking. At the end, report exactly what was installed and where.

skill-hive is a set of agent skills (`plugins/<plugin>/skills/<name>/SKILL.md`) that work in both **Claude Code** and **OpenCode**:

| Plugin (Claude Code) | Skills |
|----------------------|--------|
| `git-workflow` | `branch`, `changelog`, `conventional-commit`, `pull-request`, `release`, `review` |
| `code-quality` | `cpp-linter`, `js-linter`, `python-linter`, `refactor`, `tech-debt` |
| `code-insight` | `code-history`, `codebase-tour` |

Repository: `https://github.com/hashgesh/skill-hive`

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
2. **Which plugins?** Any of `git-workflow`, `code-quality`, `code-insight` (default: all three). The same choice applies to Claude Code and OpenCode.

If neither tool is installed, stop and tell the user to install one first.

## Step 2 — Claude Code

Skip if the user didn't choose Claude Code.

1. Add the marketplace (safe to re-run; it reports "already on disk" if present):

   ```bash
   claude plugin marketplace add hashgesh/skill-hive
   ```

2. Install each chosen plugin for the user (safe to re-run):

   ```bash
   claude plugin install git-workflow@skill-hive
   claude plugin install code-quality@skill-hive
   claude plugin install code-insight@skill-hive
   ```

   Default scope is `user` (all projects). If the user wants it only for the current project, add `--scope project`; this enables the plugin in the project's `.claude/settings.json`.

3. Verify — each must list its skills:

   ```bash
   claude plugin details git-workflow
   claude plugin details code-quality
   claude plugin details code-insight
   ```

   Expected: `Skills (6)  branch, changelog, conventional-commit, pull-request, release, review` `Skills (5)  cpp-linter, js-linter, python-linter, refactor, tech-debt` and `Skills (2)  code-history, codebase-tour`.

4. Tell the user to restart Claude Code (or run `/reload-plugins` in a session). Skills are namespaced: `/git-workflow:changelog`, `/code-quality:python-linter`, `/code-insight:codebase-tour`, and Claude also picks them automatically from their descriptions.

> If you are running *inside* Claude Code and `claude` commands are unavailable, give the user these to type instead:
> `/plugin marketplace add hashgesh/skill-hive`, then `/plugin install git-workflow@skill-hive`, `/plugin install code-quality@skill-hive` and `/plugin install code-insight@skill-hive`.

## Step 3 — OpenCode

Skip if the user didn't choose OpenCode.

OpenCode loads skills from directories listed in its config, so it needs a local clone.

1. **Pick a clone location.** Default: `~/.local/share/skill-hive` (ask the user if they prefer another). If that directory already contains a skill-hive clone, update it with `git -C <dir> pull --ff-only` instead of cloning again.

   ```bash
   git clone https://github.com/hashgesh/skill-hive.git ~/.local/share/skill-hive
   ```

2. **Find the global config file**: `~/.config/opencode/opencode.jsonc`, or `~/.config/opencode/opencode.json` if that one exists instead. Create `opencode.jsonc` if neither exists. Read the file first.

3. **Add the skills directories** — `plugins/<plugin>/skills` inside the clone for each chosen plugin, as absolute paths or starting with `~/`. Edit the file in place, keeping every existing setting and comment (it may be JSONC). Show the user the change before saving. Handle the existing shape:

   - No `skills` key → add `"skills": [ ... ]` with the chosen paths
   - `"skills": [ ... ]` (array) → append each path that's not already there
   - `"skills": { "paths": [ ... ] }` (object) → append each path to `paths` that's not already there

   Minimal resulting file when it was empty:

   ```jsonc
   {
     "$schema": "https://opencode.ai/config.json",
     "skills": [
       "~/.local/share/skill-hive/plugins/git-workflow/skills",
       "~/.local/share/skill-hive/plugins/code-quality/skills",
       "~/.local/share/skill-hive/plugins/code-insight/skills"
     ]
   }
   ```

   Older setups may point at `<clone>/skills` (before v2.0.0) or `<clone>/opencode`; those paths no longer exist, so replace them with the `plugins/<plugin>/skills` paths above.

4. **Restart OpenCode.** Config is read only at startup. If a background server is running (`opencode serve --service`), restart it too: it keeps the config, and the environment (e.g. `OPENCODE_CONFIG`), it was started with.

5. **Verify.** OpenCode silently ignores a path that doesn't exist, so always check:

   ```bash
   opencode api GET /api/skill
   ```

   The output is JSON with the skills under `data`; every chosen plugin's skills must appear with a `data[].path` under `<clone>/plugins/` (all 13 when all three are chosen): `branch`, `changelog`, `code-history`, `codebase-tour`, `conventional-commit`, `cpp-linter`, `js-linter`, `pull-request`, `python-linter`, `refactor`, `release`, `review`, `tech-debt`. The top-level `location` is only the directory the query ran in.

   Right after a restart the first answer can come back before the skill scan finishes (`"data": []`, or only built-in skills): wait a few seconds and ask again before concluding anything. Don't add `--standalone`; it returns an empty list. Older OpenCode versions used `opencode debug skill` instead. If skill-hive skills are missing, re-check the paths in the config; if a same-named skill comes from another path, OpenCode may pick that copy, so remove the duplicate.

> **Don't** symlink skill-hive into `~/.claude/skills` when Claude Code has the plugins installed: OpenCode also reads `~/.claude/skills`, but Claude Code would then load every skill twice (once from the plugin, once as a personal skill).

## Step 4 — Optional CLI tools

The skills call external CLIs and check for them at run time, so nothing breaks if they are missing. Show the user this table, mark which tools are already on PATH (`command -v <tool>`), and offer to install the missing ones for the skills they care about. Ask before installing anything.

| Skill | Tools | Install |
|-------|-------|---------|
| changelog, release | `git-cliff` | `cargo install git-cliff` · `brew install git-cliff` · `pip install git-cliff` |
| pull-request, review, release, branch | `gh` (GitHub) or `glab` (GitLab) | `brew install gh` · see https://cli.github.com |
| cpp-linter | `clang-format`, `clang-tidy`, `cppcheck` | `sudo apt install clang-format clang-tidy cppcheck` · `brew install clang-format llvm cppcheck` |
| python-linter | `ruff`, `mypy` | `pip install ruff mypy` · `uv tool install ruff` · `brew install ruff mypy` |
| js-linter | `eslint`, `prettier`, `tsc` | per project: `npm i -D eslint @eslint/js globals prettier typescript` |
| refactor | `ast-grep` | `cargo install ast-grep --locked` · `npm i -g @ast-grep/cli` · `brew install ast-grep` |
| tech-debt | `rg` (required), `lizard`, `jscpd` | `apt install ripgrep` · `brew install ripgrep` · `pip install lizard` · `npm i -g jscpd` |
| codebase-tour | `rg`, `scc` or `tokei` (optional) | `brew install scc` · `go install github.com/boyter/scc/v3@latest` · `cargo install tokei` |
| code-history | `git`; `gh` for PRs and issues | see the `gh` row |

`conventional-commit` only needs `git`; `branch` needs only `git`, and uses `gh` to read and link issues when available.

## Step 5 — Report

Summarize for the user:

- Claude Code: marketplace added (yes/no), plugins installed and their scope, result of `claude plugin details`
- OpenCode: clone location, config file and the paths you added, number of skill-hive skills in `opencode api GET /api/skill` and the folder their `path` points to
- CLI tools installed or still missing
- What to restart

---

## Updating

- **Claude Code:** `claude plugin marketplace update skill-hive`, then `claude plugin update git-workflow@skill-hive`, `claude plugin update code-quality@skill-hive` and `claude plugin update code-insight@skill-hive`; restart.
- **OpenCode:** `git -C ~/.local/share/skill-hive pull --ff-only`; restart.

## Uninstalling

- **Claude Code:** `claude plugin uninstall git-workflow@skill-hive`, `claude plugin uninstall code-quality@skill-hive`, `claude plugin uninstall code-insight@skill-hive`, then `claude plugin marketplace remove skill-hive`.
- **OpenCode:** remove the skill-hive path from `skills` in the config, then delete the clone (ask first).

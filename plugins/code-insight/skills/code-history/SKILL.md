---
name: code-history
description: Answer "why is this code like this?" from version history - find the commit that introduced a line or function (git blame -w -C -C -M, peeling past moves and reformat commits), trace how a function or range evolved (git log -L, --follow), find when a string or call appeared or vanished (pickaxe -S/-G), then pull in the commit message, the GitHub PR and linked issues (gh api) and summarize the rationale with evidence. Use for code archaeology, why was this added, who changed this, history of a function, git blame, when did this break, find the PR that introduced.
---

# Code History Skill

Explain **why** code looks the way it does, using git history and the PRs/issues behind it. This skill reads; it doesn't change code. Every claim in the answer cites its evidence (commit SHA, PR or issue number), and stated reasons are kept apart from your inferences.

## When Invoked

1. **Pin down the target** - ask if unclear:
   - a line or range (`src/billing.py:40-55`)
   - a function or class (`price` in `src/billing.py`)
   - a string, call or config key ("when did we start calling `retry()`?")
   - a whole file
2. **Check the history is usable**: `git rev-parse --is-shallow-repository`. If `true`, history is cut off - ask before running `git fetch --unshallow`.
3. **Find the origin and the evolution** with the techniques below.
4. **Collect context** for the important commits: message, PR, review discussion, linked issues.
5. **Answer** with the Output format: short answer first, then the timeline with evidence.

## Techniques

### Who last touched these lines - and the real origin

```bash
git blame -w -C -C -M -L {start},{end} -- {file}
git blame -w -C -C -M -L {start},{end} --porcelain -- {file}   # machine-readable: sha, author-time, summary, filename
```

- `-w` ignores whitespace changes, `-M` follows lines moved within the file, `-C -C` follows lines moved or copied from other files (including the commit that created the file).
- If the repo has `.git-blame-ignore-revs` (bulk reformat commits), add `--ignore-revs-file .git-blame-ignore-revs`.
- **Peel** past commits that only moved, renamed or reformatted the line: blame again at that commit's parent, and repeat until you reach the commit that changed the meaning:

  ```bash
  git blame -w -C -C -M -L {start},{end} {sha}^ -- {path-at-that-commit}
  ```

  `--porcelain` prints `filename`, which is the path to use at the parent when the file was renamed.

### How a function or range evolved

```bash
git log -L :{funcname}:{file} --format='%h %ad %an %s' --date=short    # every change to that function, with diffs
git log -L {start},{end}:{file} --format='%h %ad %an %s' --date=short  # every change to a line range
git log -L :{funcname}:{file} -s --format='%h %ad %s' --date=short     # same, list only
```

`:{funcname}:` works with git's built-in function detection; for better results in some languages set a diff driver in `.gitattributes` (e.g. `*.py diff=python`).

### A whole file, across renames

```bash
git log --follow --format='%h %ad %an %s' --date=short -- {file}
```

### When something appeared or disappeared (pickaxe)

```bash
git log -S '{exact string}' --format='%h %ad %s' --date=short -- {paths}   # commits that changed the number of occurrences
git log -G '{regex}' --format='%h %ad %s' --date=short -- {paths}          # commits whose diff touches a matching line
```

`-S` finds introduction and removal; `-G` also finds edits to matching lines. Add `--all` to include other branches.

### Context for a commit

```bash
git show --stat --format='%H%n%an <%ae>%n%ad%n%n%B' {sha}   # full message and files touched
```

The PR that brought a commit in, and its discussion (GitHub; `{owner}` and `{repo}` are filled in by `gh api` from the current repo):

```bash
gh api 'repos/{owner}/{repo}/commits/{sha}/pulls' --jq '.[] | "#\(.number) \(.title) \(.html_url)"'
gh api 'repos/{owner}/{repo}/pulls/{n}' --jq '{title, user: .user.login, merged_at, body}'
gh api 'repos/{owner}/{repo}/pulls/{n}/comments' --jq '.[] | {path, line, user: .user.login, body}'   # review comments on code
gh api 'repos/{owner}/{repo}/issues/{n}/comments' --jq '.[] | {user: .user.login, body}'             # conversation
```

Linked issues: look for `Closes #N` / `Fixes #N` / `Resolves #N` in the PR body and commit messages, then:

```bash
gh api 'repos/{owner}/{repo}/issues/{N}' --jq '{title, state, body}'
```

Without `gh` or for other hosts, use the merge commit instead: `git log --merges --ancestry-path --format='%h %s' {sha}..HEAD | tail -1` usually names the PR or branch that brought `{sha}` in.

## Reading the evidence

- **Stated rationale** is what a commit message, PR description, review comment or issue says. Quote it briefly and cite it.
- **Inferred rationale** is your reading of the diff (e.g. "the check was added in the same commit as the null-token crash fix, so it is likely the guard for it"). Label it as inferred.
- Squash merges, imported code ("initial import", vendor drops) and huge refactors can hide the real origin; say so instead of guessing, and point to where the history stops.
- Authors are context, not blame: report who changed what only when it helps (e.g. who to ask).

## Output

```markdown
## Why does `price()` round to 2 decimals?

**Short answer:** Added in a1b2c3d (2024-03-12) to fix invoices that were off by a cent (#88); the PR discussion chose rounding at the end over Decimal everywhere to keep the change small (PR #91, review by @alice). *Stated.*

### Timeline
| Date | Commit | Change | Evidence |
|------|--------|--------|----------|
| 2023-01-10 | 3f2e1d0 | `price()` created, float arithmetic | initial billing module |
| 2024-03-12 | a1b2c3d | `round(total, 2)` added | PR #91 "Fix off-by-one-cent invoices", closes #88 |
| 2025-06-01 | 9c8b7a6 | moved to `billing/pricing.py` | rename only (peeled) |

### Still open
- The TODO "replace with decimal arithmetic" (2023-01-10) was never addressed; see the tech-debt skill to track it.
```

## Install

Only `git` is required. `gh` (GitHub CLI, authenticated with `gh auth login`) adds PRs, reviews and issues: `brew install gh` or see https://cli.github.com.

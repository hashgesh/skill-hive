---
name: branch
description: Create a correctly named git branch for new work - feat/, fix/, hotfix/, release/, docs/, refactor/ etc. - from the right base (develop or main), optionally from a GitHub issue number (gh issue develop links the branch to the issue). Follows the repo's existing prefix convention, slugifies the description, checks the name is valid and unused, and avoids tracking the base branch. Use for new branch, create branch, start feature, start bugfix, git switch -c, branch naming, work on issue.
---

# Branch Skill

Create a branch with a consistent name from the right base branch.

## When Invoked

1. **Check the working tree**: `git status --porcelain`. If there are uncommitted changes, ask: carry them to the new branch (the default with `git switch`), stash them (`git stash push -u -m "before {name}"`), or stop.
2. **Gather the input** - ask for whatever is missing:
   - **Type**: one of the prefixes below.
   - **Description**: a few words, or an **issue number**. With an issue and `gh` available, read it:
     `gh issue view {n} --json number,title,labels`
     and suggest the type from its labels (`bug` → `fix`, `enhancement`/`feature` → `feat`, `documentation` → `docs`).
3. **Follow the repo's convention**: look at existing branch prefixes and reuse them (e.g. `feature/` vs `feat/`, `bugfix/` vs `fix/`):
   `git fetch --prune origin && git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin | grep / | cut -d/ -f1 | sort | uniq -c | sort -rn`
   With no existing convention, use the short prefixes below.
4. **Build the name**: `{prefix}/{issue-}{slug}`, e.g. `feat/42-add-login-endpoint`, `fix/null-token-crash`.
   - Slug: lowercase ASCII, words joined with `-`, no other punctuation, max ~50 characters, drop filler words.
   - Transliterate non-ASCII letters (`ç→c ğ→g ı→i ö→o ş→s ü→u`, `ä→a ß→ss é→e` …) instead of dropping them.
   - Validate: `git check-ref-format --branch "{name}"` (non-zero exit = invalid).
   - Must not exist: `git show-ref --verify --quiet "refs/heads/{name}"` (exit 0 = exists locally) and `git ls-remote --exit-code --heads origin "{name}"` (exit 0 = exists on the remote, 2 = free). If taken, suggest a variant or offer to switch to the existing branch.
5. **Pick the base** (table below), confirm it with the user, then `git fetch origin {base}`.
6. **Show the plan and ask for confirmation**: name, base, and whether uncommitted changes come along.
7. **Create the branch**:
   - From an issue on GitHub, offer to link it (the branch then shows up on the issue and is created on the remote):
     `gh issue develop {n} --name "{name}" --base {base} --checkout`
   - Otherwise:
     `git switch -c "{name}" --no-track "origin/{base}"`

     `--no-track` matters: starting from `origin/{base}` would otherwise set the base as upstream, so a later `git pull`/`git push` would talk to `{base}`.
8. **Ask "Push now?"** If yes: `git push -u origin HEAD` (sets the correct upstream). Otherwise mention that the first push should use `-u`.
9. **Report**: branch name, base, upstream, and the next steps (commit with the conventional-commit skill, open a PR with the pull-request skill against `{base}`).

## Prefixes and Base Branches

| Prefix | Use for | Base with `develop` | Base without `develop` |
|--------|---------|---------------------|------------------------|
| `feat/` | New feature | `develop` | default branch |
| `fix/` | Bug fix | `develop` | default branch |
| `hotfix/` | Urgent production fix | `main` (merge back into `develop` later) | default branch |
| `release/` | Release preparation | `develop` | default branch |
| `docs/` | Documentation only | `develop` | default branch |
| `refactor/` | Refactoring, no behavior change | `develop` | default branch |
| `test/` | Tests only | `develop` | default branch |
| `chore/` | Tooling, config, dependencies | `develop` | default branch |

- "With `develop`" means `git ls-remote --exit-code --heads origin develop` succeeds.
- Default branch: `git symbolic-ref --short refs/remotes/origin/HEAD` (prints `origin/main`). If that fails, run `git remote set-head origin --auto` and retry, or use `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`.
- The user can always override the base.

## Example

```
User: Start a branch for issue 42
→ gh issue view 42 → "Add login endpoint" [enhancement]
→ Existing prefixes on origin: feat (12), fix (7) → using feat/
→ Name: feat/42-add-login-endpoint (valid, unused)
→ Base: develop (exists on origin)

Create feat/42-add-login-endpoint from origin/develop and link it to issue #42? (yes/no)
User: yes
→ gh issue develop 42 --name feat/42-add-login-endpoint --base develop --checkout
→ Switched to feat/42-add-login-endpoint

Next: commit with the conventional-commit skill, then open a PR against develop.
```

```
User: New branch: kullanıcı girişi hatasını düzelt
→ Type: fix · slug from "kullanıcı girişi hatası" → kullanici-girisi-hatasi
→ Name: fix/kullanici-girisi-hatasi · base: develop
→ git switch -c fix/kullanici-girisi-hatasi --no-track origin/develop
Push now? (yes/no)
```

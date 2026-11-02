---
name: pull-request
description: Open a GitHub pull request (gh) or GitLab merge request (glab) with an auto-generated title and summary from the commits and diff against the target branch. Groups conventional/gitmoji commits by type, fills the repo's PR template, pushes the branch if needed. Use for create PR, open MR, pull request description, PR summary.
---

# Pull Request Skill

Create a pull request (PR) or merge request (MR) with an auto-generated summary.

## When Invoked

1. **Detect source branch**: `git branch --show-current`. Stop if it is the target branch.
2. **Ask target branch**: main, develop, or custom. Suggest the default branch:
   `gh repo view --json defaultBranchRef -q .defaultBranchRef.name`
3. **Sync**: `git fetch origin {target}` and compare against `origin/{target}`, not the local branch, which may be stale.
4. **Analyze differences** (three dots = only changes made on the source branch since it diverged):
   - Commits: `git log origin/{target}..HEAD --oneline`
   - Changed files: `git diff origin/{target}...HEAD --stat`
   - Totals: `git diff origin/{target}...HEAD --shortstat`
   - Template: `.github/pull_request_template.md`, `.github/PULL_REQUEST_TEMPLATE/`, `docs/pull_request_template.md`, or `.gitlab/merge_request_templates/`
5. **Generate summary**:
   - Parse commit messages (strip a leading gitmoji, then read `type(scope)`)
   - Group by type; list changed files; count additions/deletions
   - If a template exists, fill its sections instead of the default format
6. **Show preview**: title, body, source → target
7. **Ask confirmation**: "Create PR?" (also offer draft)
8. **Push if needed**: if `git rev-parse --abbrev-ref @{u}` fails or the branch is ahead, run `git push -u origin HEAD`.
9. **Execute** - write the body to a temp file to avoid shell-quoting problems:
   - GitHub: `gh pr create --base {target} --head {source} --title "{title}" --body-file {file}` (add `--draft` if asked)
   - GitLab: `glab mr create --target-branch {target} --source-branch {source} --title "{title}" --description "$(cat {file})"`
   - Neither CLI: print the compare URL (`https://github.com/{owner}/{repo}/compare/{target}...{source}?expand=1`) and the body to paste
10. **Report** the PR/MR URL.

## Title

- One commit: use its subject.
- Several commits: derive from the branch name (`feat/auth-login` → `✨ feat(auth): login`) or summarize the dominant type.
- Keep the conventional/gitmoji format used in the repo.

## Summary Format

```
## Summary
- ✨ feat: {description} ({count} commits)
- 🐛 fix: {description} ({count} commits)
- 📝 docs: {description} ({count} commits)
- ♻️ refactor: {description} ({count} commits)
- other: {count} commits

## Changes
- +{additions} -{deletions} in {file count} files

## Files Changed
{file list with changes}
```

## Example

```
User: Create PR
Assistant: Which branch is the target? (main/develop/other)
User: main

→ git fetch origin main
→ Analyzing feat/auth → origin/main...
→ Found 3 commits: feat(auth), fix(api), docs(readme)

Title: ✨ feat(auth): add auth module

## Summary
- ✨ feat: add auth module (1)
- 🐛 fix: resolve api bug (1)
- 📝 docs: update readme (1)

## Changes
- +50 -10 in 4 files

Create PR? (yes/draft/no)
```

## Branch Naming Conventions

- Feature: `feature/` or `feat/`
- Bugfix: `bugfix/` or `fix/`
- Hotfix: `hotfix/`
- Release: `release/`

Extract the type from the branch name for the PR title if available.

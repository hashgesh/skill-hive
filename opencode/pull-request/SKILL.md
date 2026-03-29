---
name: pull-request
description: Create a pull/merge request with auto-generated summary based on target branch
---

# Pull Request Skill

Create a pull request (PR) or merge request (MR) with auto-generated summary.

## When Invoked

1. **Ask target branch**: "Which branch is the target?" (options: main, develop, or custom)
2. **Ask source branch**: Detect current branch automatically
3. **Analyze differences**:
   - Get commits: `git log {target}..{source} --oneline`
   - Get changed files: `git diff {target}..{source} --stat`
   - Get PR/MR template if exists
4. **Generate summary**:
   - Parse commit messages (extract type: feat, fix, docs, etc.)
   - List changed files with categories
   - Count additions/deletions
5. **Show preview** with:
   - Title (from branch name or commits)
   - Summary (bullet points from commits)
   - Changed files list
   - Target branch
6. **Ask confirmation**: "Create PR?"
7. **Execute**:
   - If `gh` CLI available: `gh pr create --base {target} --head {source} --title "..." --body "..."`
   - If not: Show link to create PR manually

## Summary Format

```
## Summary
- [feat]: {description} ({count} commits)
- [fix]: {description} ({count} commits)
- [docs]: {description} ({count} commits)
- [refactor]: {description} ({count} commits)
- [other]: {count} commits

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

→ Analyzing develop → main...
→ Found 3 commits: feat(auth), fix(api), docs(readme)

## Summary
- ✨ feat: add auth module (1)
- 🐛 fix: resolve api bug (1)
- 📝 docs: update readme (1)

## Changes
- +50 -10 in 4 files

Create PR? (yes/no)
```

## Branch Naming Conventions

- Feature: `feature/` or `feat/`
- Bugfix: `bugfix/` or `fix/`
- Hotfix: `hotfix/`
- Release: `release/`

Extract type from branch name for PR title if available.

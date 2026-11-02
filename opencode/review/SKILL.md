---
name: review
description: Review a GitHub pull request with gh - fetch the PR diff, commits and existing review state, analyze the changes (tests, breaking changes, size, C++ lint via cpp-linter), suggest approve / comment / request-changes, and post the review after confirmation. Use for code review, review PR, approve PR, request changes, LGTM.
---

# Review Skill

Analyze an existing GitHub pull request and post a review with `gh`.

## When Invoked

1. **Identify the PR**: ask "Which PR to review?" or detect it from the current branch with `gh pr view --json number -q .number`.
2. **Fetch PR data** (all from GitHub, not local branches):
   - Metadata: `gh pr view {n} --json number,title,author,baseRefName,headRefName,isDraft,additions,deletions,changedFiles,files,commits,reviewDecision,reviewRequests,reviews,comments`
   - Diff: `gh pr diff {n}`
   - Current user: `gh api user -q .login`
3. **Analyze** the diff with the Auto-Analysis Rules below, plus Language-Specific Checks.
4. **Suggest a review type** with the decision table, and show why.
5. **Show preview** of the review body and the suggested type; let the user confirm or change the type.
6. **Execute** - write the body to a temp file to avoid shell-quoting problems:
   `gh pr review {n} --{approve|comment|request-changes} --body-file {file}`
7. **Report** the result with the PR URL.

Never post a review, and especially never approve, without the user's explicit confirmation in step 5.

## Review Types

- `--approve` : Approve the PR
- `--comment` : Leave a comment
- `--request-changes` : Request changes

## Decision Table

Evaluate top to bottom; the first matching row wins.

| Condition | Suggested type |
|-----------|----------------|
| PR author is the current user | `--comment` (GitHub rejects approve **and** request-changes on your own PR) |
| Blocking issues found (bugs, breaking changes without notice, failing lint) | `--request-changes` |
| Open questions or non-blocking suggestions | `--comment` |
| No issues found | `--approve` |

## Auto-Analysis Rules

| Change Type | Finding |
|-------------|---------|
| docs only | No code impact - still read the diff for errors and broken links |
| feat + test | Check tests cover the new behavior |
| fix + test | Check a test reproduces the bug |
| feat / fix without test | Suggest: "Consider adding tests" |
| breaking change (`!` or `BREAKING CHANGE:`) | Check it is documented and intended |
| 100+ files or 1000+ changed lines | Suggest: "Consider splitting into smaller PRs" |
| Draft PR | Mention it is a draft; prefer `--comment` |

Also check the existing `reviews` and `comments`: don't repeat points already raised, and mention unresolved change requests from others.

## Review Body Format

```
## Code Review

### Summary
{what the PR does, from commits and diff}

### Changes
+{additions} -{deletions} in {changedFiles} files

### Analysis
- {findings, with file:line where possible}

### Recommendation
{LGTM / Needs changes / Suggestions}
```

## Example

```
User: Review PR 2

→ gh pr view 2 ... / gh pr diff 2
→ Author: alice (not you), 1 commit, +77 -0 in 1 file

## Code Review

### Summary
- 📝 docs: add pull request skill

### Changes
+77 -0 in 1 file

### Analysis
- Documentation-only change, no code impact
- No breaking changes
- Clean commit history

### Recommendation
LGTM! 👍

Suggested type: --approve (no issues found, not your PR)
Post this review? (approve/comment/request-changes/no)
User: approve

→ Approved PR #2: https://github.com/{owner}/{repo}/pull/2
```

## Language-Specific Checks

When C++ files are in the PR, run the cpp-linter skill's checks on the **changed files only**:

1. **Detect C++ files** in `files`: `.cpp`, `.cc`, `.cxx`, `.h`, `.hpp`
2. **Get the PR's code locally**: the working tree must be clean; then `gh pr checkout {n}` (ask first, and switch back afterwards)
3. **Run lint checks** (respect the repo's `.clang-format` / `.clang-tidy` if present):
   - `clang-format --style=file --dry-run --Werror {files}` (fallback `--style=Google`)
   - `clang-tidy {files} -p build` (or `-- -std=c++17`)
   - `cppcheck --enable=warning,style,performance,portability --suppress=missingIncludeSystem {files}`
4. **Include findings in review** under a "C++ Analysis" section; only report lines the PR touched.

### C++ Review Example

```
### C++ Analysis (cpp-linter)
- ⚠️ src/main.cpp:15 - code should be clang-formatted
- ⚠️ src/utils.cpp:42 - variable can be declared const
- ✅ No memory leaks detected

Recommendation: Fix formatting issues before merge.
```

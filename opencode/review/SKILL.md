---
name: review
description: Add review notes to a pull request with analysis output
---

# Review Skill

Add review notes to an existing pull request with code analysis.

## When Invoked

1. **Ask PR number**: "Which PR to review?" (or detect from current branch)
2. **Ask review type**: approve / comment / request-changes
3. **Generate review content**:
   - Get commits: `git log {target}..{source} --oneline`
   - Get changes: `git diff {target}..{source}`
   - Get code statistics
4. **Generate review body**:
   - Summary of changes
   - File analysis
   - Suggestions (optional)
5. **Show preview**
6. **Execute**: `gh pr review {pr_number} --{type} -b "{body}"`

## Review Types

- `--approve` : Approve the PR
- `--comment` : Leave a comment
- `--request-changes` : Request changes

## Review Body Format

```
## Code Review

### Summary
{commit summary}

### Changes
{files changed with stats}

### Analysis
- {auto-generated insights}

### Recommendation
{LGTM / Needs changes / Suggestions}
```

## Example

```
User: Review PR 2
Assistant: What type of review? (approve/comment/request-changes)
User: approve

→ Analyzing PR #2...

## Code Review

### Summary
- 📝 docs: add pull request skill (1)

### Changes
- +77 -0 in 1 file

### Analysis
- Documentation-only change
- No breaking changes
- Clean commit history

### Recommendation
LGTM! 👍

Add this review? (yes/no)
User: yes

→ Added review to PR #2
```

## Auto-Analysis Logic

### Step 1: Check for Review Requests
- Get PR review threads: `gh pr view {pr_number} --json reviews`
- Check if there are pending review requests or questions

### Step 2: Determine Review Type

| Condition | Action |
|-----------|--------|
| PR owner is self | `--comment` only (can't approve own PR) |
| Has pending change requests | `--request-changes` |
| Has questions in comments | `--comment` |
| No issues found + not own PR | `--approve` |

### Step 3: Generate Review Body

Based on analysis:
- **Approve**: "LGTM! 👍 Great work."
- **Comment**: "Looks good, but consider X"
- **Request Changes**: "Please address X before merging"

## Auto-Analysis Rules

| Change Type | Recommendation |
|-------------|----------------|
| docs only | LGTM |
| feat + test | LGTM |
| fix + test | LGTM |
| feat without test | Comment: "Consider adding tests" |
| breaking changes | Request changes: "Review breaking changes" |
| 100+ files | Comment: "Consider splitting into smaller PRs" |

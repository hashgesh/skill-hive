---
name: conventional-commit
description: Write and validate conventional commit messages following the conventional-commits specification with gitmoji. Use gitmoji-cli for commits.
---

# Conventional Commit Skill with Gitmoji

Guidelines for writing conventional commits following the [conventional-commits](https://www.conventionalcommits.org/) specification with gitmoji. Use the **gitmoji-cli** tool for commits.

## Install

```bash
npm i -g gitmoji-cli
```

## Commands

```bash
gitmoji -c    # Interactive commit (recommended)
gitmoji -l    # List all available gitmojis
gitmoji -s    # Search gitmojis
```

## Format

```
:<gitmoji>: <type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Always include a scope when applicable!** Examples: `auth`, `api`, `shared-ptr`, `unique-ptr`

## Gitmoji Mapping

| Gitmoji | Code | Type | Description |
|---------|------|------|-------------|
| ✨ | :sparkles: | feat | A new feature |
| 🐛 | :bug: | fix | A bug fix |
| 📝 | :memo: | docs | Documentation only changes |
| 💄 | :lipstick: | style | UI and style files |
| ♻️ | :recycle: | refactor | Refactor code |
| ⚡️ | :zap: | perf | Improve performance |
| ✅ | :white_check_mark: | test | Add or pass tests |
| 📦️ | :package: | build | Compiled files/packages |
| 👷 | :construction_worker: | ci | CI build system |
| 🔧 | :wrench: | chore | Configuration files |
| 🔨 | :hammer: | chore | Development scripts |
| 🚑️ | :ambulance: | fix | Critical hotfix |
| 🎨 | :art: | style | Code structure/format |
| 🔖 | :bookmark: | release | Release/version tags |
| ✏️ | :pencil2: | style | Fix typos |
| 💥 | :boom: | feat | Breaking changes |
| 🧪 | :test_tube: | test | Failing test |
| 👔 | :necktie: | feat | Business logic |
| 🌐 | :globe_with_meridians: | feat | Internationalization |
| ⬆️ | :arrow_up: | build | Upgrade dependencies |
| ⬇️ | :arrow_down: | build | Downgrade dependencies |

## Rules

### Subject Line
- Use imperative mood: "add feature" not "added feature"
- Keep subject line under 50 characters
- Do not end with a period
- Lowercase the first letter
- Always prefix with appropriate gitmoji

### Scope (Required when applicable)
- Use parentheses after type: `feat(auth):`, `fix(shared-ptr):`, `test(unique-ptr):`
- Use lowercase alphanumeric with single hyphens
- Include scope to identify what the change affects

### Body (Optional)
- Separate subject from body with a blank line
- Wrap body at 72 characters
- Explain what and why, not how

### Footer (Optional)
- Reference issues: `Closes #123`, `Fixes #456`
- Breaking changes: `BREAKING CHANGE: description`

## Examples

```
✨ feat(auth): add login endpoint

Implements OAuth2 login flow with JWT tokens.

Closes #123
```

```
🐛 fix(shared-ptr): resolve memory leak in release

Fixed release() not deleting object when ref_count reaches 0.

Fixes #456
```

```
📝 docs(agents): update agent guidelines

Added build commands and code style guidelines.

Closes #789
```

```
✅ test(shared-ptr): add tests for copy semantics

Added test cases for copy constructor and assignment operator.
```

```
♻️ refactor(unique-ptr): simplify release method

Removed redundant null check before deletion.
```

## Validation

When reviewing commit messages, verify:
1. Gitmoji is present and matches the type
2. Type is one of the defined types
3. **Scope is included when applicable** (e.g., `fix(shared-ptr):`, `feat(auth):`)
4. Subject is under 50 chars
5. Imperative mood is used
6. No trailing period in subject
7. Scope is in lowercase with hyphens
8. Breaking changes properly marked

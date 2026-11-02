---
name: conventional-commit
description: Write, commit and validate conventional commit messages with a gitmoji prefix and scope, e.g. "✨ feat(auth): add login endpoint". Maps gitmoji to types (feat, fix, docs, refactor, ...), marks breaking changes, checks subject rules. Use for commit, commit message, git commit, conventional commits, gitmoji, lint commit.
---

# Conventional Commit Skill with Gitmoji

Guidelines for writing conventional commits following the [conventional-commits](https://www.conventionalcommits.org/) specification with a [gitmoji](https://gitmoji.dev/) prefix.

## When Invoked

1. **Inspect changes**: `git status --short` and `git diff --staged` (if nothing is staged, ask what to stage).
2. **Pick type, gitmoji and scope** from the mapping below; take the scope from the touched module/directory.
3. **Draft the message** and check it against the Validation list.
4. **Show it and ask for confirmation**.
5. **Commit non-interactively**:
   - Subject only: `git commit -m "✨ feat(auth): add login endpoint"`
   - With body/footer: write the message to a temp file and run `git commit -F {file}`

Don't run `gitmoji -c` from an agent: it is an interactive prompt, and its default output (`:sparkles: (scope): title`) has no conventional type.

## Optional: gitmoji-cli

Useful for humans browsing emojis; not needed to commit.

```bash
npm i -g gitmoji-cli
gitmoji -l          # List all available gitmojis
gitmoji -s <query>  # Search gitmojis
```

## Format

```
<gitmoji> <type>(<scope>)[!]: <description>

[optional body]

[optional footer(s)]
```

Use the unicode emoji (`✨`), not the `:sparkles:` shortcode, so the message renders everywhere and matches the changelog skill.

**Always include a scope when applicable!** Examples: `auth`, `api`, `parser`, `ci`

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
| 💥 | :boom: | feat! | Breaking changes (add `!` and/or a `BREAKING CHANGE:` footer) |
| 🧪 | :test_tube: | test | Failing test |
| 👔 | :necktie: | feat | Business logic |
| 🌐 | :globe_with_meridians: | feat | Internationalization |
| ⬆️ | :arrow_up: | build | Upgrade dependencies |
| ⬇️ | :arrow_down: | build | Downgrade dependencies |

## Rules

### Subject Line
- Use imperative mood: "add feature" not "added feature"
- Keep the whole subject line (emoji, type, scope included) under 72 characters; aim for a description of about 50
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
- Breaking changes: `BREAKING CHANGE: description`, and add `!` after the type/scope: `💥 feat(api)!: remove v1 endpoints`

## Examples

```
✨ feat(auth): add login endpoint

Implements OAuth2 login flow with JWT tokens.

Closes #123
```

```
🐛 fix(parser): handle empty input without crashing

Return an empty AST instead of dereferencing a null token.

Fixes #456
```

```
📝 docs(readme): add installation steps
```

```
✅ test(parser): add tests for nested expressions
```

```
♻️ refactor(cache): extract eviction policy

Moved LRU logic into its own class so it can be swapped.
```

```
💥 feat(api)!: remove v1 endpoints

BREAKING CHANGE: /v1/* routes are gone; use /v2/*.
```

## Validation

When reviewing commit messages, verify:
1. Gitmoji is present and matches the type
2. Type is one of the defined types
3. **Scope is included when applicable** (e.g., `fix(shared-ptr):`, `feat(auth):`)
4. Subject line is under 72 chars
5. Imperative mood is used
6. No trailing period in subject
7. Scope is in lowercase with hyphens
8. Breaking changes properly marked

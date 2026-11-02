---
name: release
description: Cut a new release - pick a semver version, generate CHANGELOG.md with git-cliff (see changelog skill), commit it, create an annotated git tag, and optionally push and publish a GitHub release with gh. Use for release, version bump, tag, semver, ship, publish.
---

# Release Skill

Create a new release by generating the changelog and creating an annotated git tag. Uses the `changelog` skill's `cliff.toml`.

## Pre-flight Checks

Stop and report if any check fails:

1. `git cliff --version` and a `cliff.toml` exist (otherwise run the `changelog` skill first)
2. Working tree is clean: `git status --porcelain` is empty
3. On the release branch (usually `main`); ask if not
4. Branch is up to date: `git fetch origin && git status -sb` shows no `behind`

## When Invoked

1. **Pick version**: suggest one with `git cliff --bumped-version`, let the user confirm or change it. Keep the repo's tag style (e.g. `v1.0.0` if existing tags use `v`).
2. **Check tag**: `git rev-parse -q --verify "refs/tags/{version}"` - if it exists, ask for a different version.
3. **Generate changelog**: `git cliff --tag {version} -o CHANGELOG.md`
   (`-o` is required; without it git-cliff only prints to stdout)
4. **Preview**: show `git diff CHANGELOG.md` and ask for confirmation.
5. **Commit**: `git add CHANGELOG.md && git commit -m "🔖 release: {version}"`
6. **Tag**: `git tag -a {version} -m "Release {version}"`
7. **Ask "Push?"** (user decides): `git push origin HEAD && git push origin {version}`
8. **Optional GitHub release** (if `gh` is available and the user wants it):
   `gh release create {version} --title "{version}" --notes "$(git cliff --latest --strip header)"`

## Example

```
Release v1.0.0
- Checks: clean tree, on main, up to date
- Suggested version: v1.0.0 (git cliff --bumped-version)
- Writes CHANGELOG.md
- Commits with: 🔖 release: v1.0.0
- Creates tag: v1.0.0
- Push? (yes/no)
```

## Undo (before pushing)

```bash
git tag -d {version}
git reset --soft HEAD~1
```

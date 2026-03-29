---
name: release
description: Create a new release with changelog and tag. Triggers changelog skill.
---

# Release Skill

Create a new release by generating changelog and creating a git tag.

## When Invoked

1. Ask for version number (e.g., v1.0.0)
2. Check if tag already exists - if yes, ask for different version
3. Generate changelog with `git cliff --tag {version}`
4. Show preview and confirm
5. Commit changelog: `git add CHANGELOG.md && git commit -m "📝 docs(release): add changelog for {version}"`
6. Create annotated tag: `git tag -a {version} -m "Release {version}"`
7. Ask: "Push?" (user decides)

## Example

```
Release v1.0.0
- Generates CHANGELOG.md
- Commits with: 📝 docs(release): add changelog for v1.0.0
- Creates tag: v1.0.0
```

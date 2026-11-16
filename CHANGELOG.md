# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2026-11-16

### Refactor

- **marketplace:** Move each plugin into its own folder (**BREAKING**)

### Documentation

- **agents:** Document release title format
- **install:** Verify OpenCode skills with opencode api GET /api/skill

## [1.0.0] - 2026-11-16

### Documentation

- **readme:** Add badges, why section and example prompts

### Maintenance

- Add neon honeycomb SVG banner (#16)
- **marketplace:** Pin plugins to version 1.0.0

## [0.1.0] - 2026-11-09

### Features

- **review:** Add cpp-linter integration
- **refactor:** Add refactor skill
- **marketplace:** Add Claude Code plugin marketplace
- **python-linter:** Add Python lint skill with ruff and mypy
- **js-linter:** Add JS/TS lint skill with ESLint, Prettier and tsc
- **marketplace:** Add Python and JS/TS linters to code-quality
- **branch:** Add branch creation skill
- **marketplace:** Add branch skill to git-workflow
- **tech-debt:** Add technical debt audit skill
- **marketplace:** Add tech-debt skill to code-quality
- **codebase-tour:** Add guided repository tour skill
- **code-history:** Add code archaeology skill
- **marketplace:** Add code-insight plugin

### Bug Fixes

- **changelog:** Parse gitmoji-prefixed commits
- **release:** Write changelog to file before committing
- **cpp-linter:** Use valid clang-format and install commands
- **refactor:** Correct ast-grep install and commands
- **pr:** Diff against merge base of remote target
- **review:** Read PR data from GitHub and confirm before posting
- **conventional-commit:** Commit non-interactively
- **changelog:** Skip merge commits instead of reporting parse errors
- **changelog:** Skip every kind of merge commit

### Refactor

- **review:** Add auto-approve logic
- Move skills to tool-neutral skills/ directory

### Documentation

- **changelog:** Add changelog skill
- **conventional-commit:** Add conventional commit skill
- **release:** Add release skill
- **pr:** Add pull request skill
- **review:** Add review skill
- **review:** Add GitHub restriction note
- **cpp-linter:** Add C++ coding standard checker skill
- Update README with cpp-linter skill
- **agents:** Add AGENTS.md
- Add installation and requirements to README
- **install:** Add agent-driven install guide for Claude Code and OpenCode
- Rename GitHub user to hashgesh

### CI

- Validate skills, marketplace and changelog config
- Check INSTALL.md lists every plugin and skill

### Maintenance

- Add LICENSE
- Add logo and README
- Add network logo
- Make main the only long-lived branch
- Remove opencode symlink


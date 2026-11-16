# Privacy

skill-hive is a set of agent skills: Markdown instructions that your AI coding agent (Claude Code or OpenCode) reads. It has no server, no telemetry and no account. **skill-hive itself collects, stores and sends no data.**

What the skills do depends on the tools they ask your agent to run, on your machine and under your own accounts:

- **Local tools** read your files and git history and report what they find: `git`, `git-cliff`, `rg`, `clang-format`, `clang-tidy`, `cppcheck`, `ruff`, `mypy`, `eslint`, `prettier`, `tsc`, `ast-grep`, `lizard`, `jscpd`, `scc` and `tokei`. Files are changed only when you ask, for example when you apply a fix or save `TECH_DEBT.md` or `ONBOARDING.md`.
- **GitHub and GitLab** are reached through `gh` and `glab` with your own login. The skills use them to read issues and pull requests, and they open pull requests, post reviews, create issues or publish releases only after you confirm.
- **Package registries** (npm, PyPI, crates.io) are queried by the tech-debt skill's outdated-dependency check (`npm outdated`, `pip list --outdated`, `cargo outdated`).

Those services handle data under their own privacy policies. Your agent and model provider handle your conversation under theirs.

Questions: [open an issue](https://github.com/hashgesh/skill-hive/issues).

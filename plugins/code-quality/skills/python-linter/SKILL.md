---
name: python-linter
description: Lint, format-check and type-check Python code (.py, .pyi) with ruff (linter + formatter, replaces flake8/isort/black) and mypy. Respects the project's pyproject.toml / ruff.toml / mypy config and its own lint scripts. Use for Python lint, PEP 8, code style, unused imports, type errors, auto-format.
---

# Python Linter Skill

Check Python code for lint errors, formatting and type errors.

## When Invoked

1. **Prefer the project's own command**: if the repo defines one (e.g. a `lint` target in `Makefile`, `noxfile.py`, `tox.ini`, `pyproject.toml` scripts, or `.pre-commit-config.yaml`), offer to run that instead and stop here if the user agrees.
2. **Check tools**: `ruff --version`, `mypy --version`. Run them through the project's environment when there is one (`uv run ruff`, `poetry run ruff`, or the active virtualenv). Skip missing tools and show how to install them.
3. **Ask files/directory**: default to the files changed on the current branch, else the whole project:
   `git diff --name-only --diff-filter=d origin/main...HEAD -- '*.py' '*.pyi'`
4. **Use the project config**: ruff reads `[tool.ruff]` in `pyproject.toml` or `ruff.toml`; mypy reads `[tool.mypy]`, `mypy.ini` or `setup.cfg`. Don't pass rule flags when a config exists.
5. **Run checks**:
   - Lint: `ruff check --output-format=concise {files}`
   - Format: `ruff format --check --diff {files}`
   - Types (only if the project uses mypy or the user asks): `mypy {files}`
6. **Show results** grouped by: Lint, Formatting, Types - each with `file:line` and rule code.
7. **Auto-fix if requested** (show the diff afterwards):
   - Safe lint fixes: `ruff check --fix {files}`
   - Formatting: `ruff format {files}`
   - Type errors are never auto-fixed; propose edits instead.

## Rule Sets

Without a project config ruff uses its defaults. To ask for more, pass `--select`/`--extend-select` (or add them to `[tool.ruff.lint]` if the user wants it permanent):

| Code | Plugin | Catches |
|------|--------|---------|
| `E`, `W` | pycodestyle | PEP 8 style |
| `F` | Pyflakes | Unused imports/variables, undefined names |
| `I` | isort | Import order |
| `B` | flake8-bugbear | Likely bugs and design problems |
| `UP` | pyupgrade | Outdated syntax for the target Python version |
| `SIM` | flake8-simplify | Simplifiable code |
| `S` | flake8-bandit | Security issues |

Example: `ruff check --extend-select B,UP,SIM {files}`

## Example

```
User: Lint my Python code
→ No project lint script found
→ Files changed on this branch: app/api.py, app/models.py

→ ruff check --output-format=concise app/api.py app/models.py
→ ruff format --check --diff app/api.py app/models.py
→ mypy app/api.py app/models.py   (pyproject.toml has [tool.mypy])

## Results

### Lint
⚠️ app/api.py:1:8 - F401 `os` imported but unused [fixable]
⚠️ app/models.py:12:5 - B006 mutable default argument

### Formatting
⚠️ app/api.py - would be reformatted
✅ app/models.py - OK

### Types
⚠️ app/api.py:30 - Incompatible return value type (got "int", expected "str")

Auto-fix lint and formatting? (yes/no)
```

## Install

```bash
# ruff and mypy
pip install ruff mypy
# or
uv tool install ruff && uv tool install mypy
# or (macOS)
brew install ruff mypy
```

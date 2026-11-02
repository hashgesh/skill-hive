---
name: tech-debt
description: Inventory, measure and prioritize technical debt across a whole repository - aged TODO/FIXME/HACK markers (git blame), suppressed lint/type warnings, churn x complexity hotspots (git log + lizard), duplicated code (jscpd), outdated dependencies, untested modules. Writes and updates a TECH_DEBT.md register with impact, effort and priority, tracks the trend between runs, optionally files GitHub issues, and hands fixes to the refactor skill. Use for technical debt, tech debt audit, code health, debt register, hotspots, legacy code, what to clean up first.
---

# Technical Debt Skill

Find where the debt is, rank it by what it costs, and keep a register that shows whether it is shrinking. This skill **measures and plans**; it does not change code. Fixes go to the refactor skill (or the linter skills) one item at a time.

## When Invoked

1. **Scope**: ask which part of the repo to scan (default: the whole repo). Only tracked files count: `rg` and `jscpd` respect `.gitignore`. Also skip vendored, generated and lock files (`vendor/`, `third_party/`, `dist/`, `build/`, `*.min.js`, `*.lock`, `package-lock.json`).
2. **Check tools**: `git` and `rg` are required. `lizard`, `jscpd` and the package managers are optional: skip a scan whose tool is missing, say so in the report, and show its install command.
3. **Run the scans** below. Some tools exit 1 when they *find* something (`lizard -w`, `npm outdated`); that is a result, not an error.
4. **Score every finding** with the rules in Prioritizing.
5. **Write or update `TECH_DEBT.md`** (format below). Show the diff before saving. If the file exists, keep item IDs and statuses, mark items that are gone as `resolved`, and add a row to the trend table.
6. **Summarize** in chat: totals per category, the change since the last run, and the top 5 items to tackle first.
7. **Offer next steps**: fix one item now with the refactor skill, or file issues for the top items (see Issues). Ask before doing either.

## Scans

### 1. Markers (TODO / FIXME / HACK / XXX) and their age

```bash
rg -n --no-heading -e '\b(TODO|FIXME|HACK|XXX)\b' {paths}
```

Age of each marker, from the commit that last touched that line:

```bash
git blame -L {line},{line} --porcelain -- {file} | sed -n 's/^author-time //p'   # unix time
```

Report the date, and flag markers older than one year. `FIXME`/`HACK`/`XXX` weigh more than `TODO`.

### 2. Suppressed warnings

Each one is a known problem someone chose to silence.

```bash
rg -c --no-heading \
  -e 'eslint-disable' -e '@ts-(ignore|expect-error|nocheck)' \
  -e '# *noqa' -e 'type: *ignore' -e 'pylint: *disable' \
  -e 'NOLINT' -e '#pragma warning disable' -e '@SuppressWarnings' -e '//nolint' \
  {paths}
```

Blanket forms (`eslint-disable` at file top, bare `# noqa`, `@ts-nocheck`) weigh more than rule-specific ones.

### 3. Hotspots: churn x complexity

Debt costs most where code is both complicated **and** changed often.

Churn (commits per file in the last 12 months; widen the window for slow repos):

```bash
git log --since='12 months ago' --name-only --format= -- {paths} | grep -v '^$' | sort | uniq -c | sort -rn | head -30
```

Complexity per function with [lizard](https://github.com/terryyin/lizard) (C/C++, Python, JS/TS, Java, Go, Rust, C#, and more):

```bash
lizard -C 10 -L 60 -a 5 -w {paths}      # warnings only: CCN > 10, length > 60 lines, > 5 params
lizard --csv {paths}                    # all functions: nloc, ccn, tokens, params, length, location, file, name, ...
```

Thresholds are "greater than": a function with CCN exactly 10 is not reported by `-C 10`.

A **hotspot** is a file in the top churn list that also contains a function over the thresholds. List hotspots first in the register; they are where the refactor skill pays off most.

### 4. Duplicated code

```bash
npx jscpd --min-lines 5 --min-tokens 30 --reporters console --silent {paths}
npx jscpd --min-lines 5 --min-tokens 30 --reporters json --output .jscpd-report --silent {paths}   # .jscpd-report/jscpd-report.json
```

The default `--min-tokens 50` misses small but real copies; 30 is a good middle ground. Report the overall duplicated percentage and each clone pair (both locations, line count). Delete `.jscpd-report/` afterwards.

### 5. Outdated dependencies

Run only for the ecosystems the repo uses; most need dependencies installed first.

| Ecosystem | Command |
|-----------|---------|
| npm / pnpm / yarn | `npm outdated --json` · `pnpm outdated --format json` · `yarn outdated` |
| Python | `pip list --outdated --format=json` (inside the project's venv), `uv pip list --outdated` |
| Rust | `cargo outdated` (needs `cargo install cargo-outdated`) |
| Go | `go list -u -m -json all` (entries with an `Update` field) |

Count major-version gaps separately from minor/patch: a major gap is debt, a patch gap is routine.

### 6. Untested code

- If a coverage report already exists (`coverage.xml`, `lcov.info`, `coverage/coverage-final.json`), list the files with the lowest coverage. Don't run the test suite just for this unless the user asks.
- Otherwise, list source modules that no test file references, e.g. `src/billing.py` with no `tests/test_billing.py` and no import of `billing` under `tests/`.

## Prioritizing

Give each finding an **impact** and an **effort**, then a priority:

| Impact | When |
|--------|------|
| **High** | In a hotspot; a `FIXME`/`HACK` older than a year; a blanket suppression; a major-version dependency gap with known security fixes; an untested module that changes often |
| **Medium** | Complex but rarely changed code; duplicated blocks; old `TODO`s; rule-specific suppressions in active files |
| **Low** | Cosmetic, isolated, or in code that rarely changes |

| Effort | Meaning |
|--------|---------|
| **S** | Under an hour, one file |
| **M** | Up to a day, a few files |
| **L** | More than a day or needs design work |

Priority: **P1** = High impact and S/M effort (do first) · **P2** = High/L or Medium/S-M · **P3** = everything else.

Be honest about uncertainty: estimate effort from the code you read, and say when an estimate is a guess.

## TECH_DEBT.md Format

```markdown
# Technical Debt Register

Last scan: 2026-11-02 · scope: whole repo · tools: rg, git, lizard 1.25, jscpd 5 (missing: cargo-outdated)

## Trend

| Date | Markers | Suppressions | Hotspots | Duplication | Outdated (major) | Open items |
|------|---------|--------------|----------|-------------|------------------|------------|
| 2026-11-02 | 3 | 3 | 1 | 15.6% | 2 | 7 |

## Top priorities

1. TD-001 - src/billing.py `price()`: CCN 14, changed 5 times in 12 months
2. ...

## Items

| ID | Priority | Category | Location | Finding | Impact | Effort | Status |
|----|----------|----------|----------|---------|--------|--------|--------|
| TD-001 | P1 | hotspot | src/billing.py:2 | `price()` CCN 14, 5 changes / 12 mo | High | M | open |
| TD-002 | P2 | duplication | src/report.py:2, :10 | `report_a`/`report_b` identical (7 lines) | Medium | S | open |
| TD-003 | P2 | marker | src/billing.py:1 | TODO from 2023-01-10: replace with decimal arithmetic | Medium | M | open |
```

Rules for updates:

- IDs are stable: never renumber; new items get the next free number.
- Status is `open`, `in-progress`, `accepted` (a conscious decision to keep it - add a short reason), or `resolved` (no longer found; keep the row with the date).
- Don't remove the user's manual edits: notes, `accepted` decisions and owners stay as written.

## Issues (optional)

Only after the user picks which items to file:

1. Check for the label: `gh label list --search tech-debt`; if missing, ask, then `gh label create tech-debt --color BFD4F2 --description "Technical debt"`.
2. Write each body to a temp file (location, finding, why it matters, suggested fix, link back to the `TD-xxx` row) and run:
   `gh issue create --title "TD-001: simplify price() in billing.py" --body-file {file} --label tech-debt`
3. Put the issue number in the register row (e.g. `open (#42)`).

## Example

```
User: How much tech debt do we have?
→ Scope: whole repo · tools: rg, git, lizard (jscpd via npx, pip)

## Summary (vs. last scan 2026-08-01)
- Markers: 3 (oldest: TODO from 2023-01-10)          ▲ +1
- Suppressions: 3 (1 blanket)                         = 0
- Hotspots: 1 (src/billing.py: price() CCN 14, 5 changes)
- Duplication: 15.6% (src/report.py report_a/report_b)
- Outdated: 2 major gaps (eslint 9 → 10, @eslint/js 9 → 10)

## Start here
1. TD-001 P1 src/billing.py price() - split by product kind (Replace Conditional with Polymorphism)
2. TD-002 P2 src/report.py - extract shared formatter (Extract Method)
3. ...

Updated TECH_DEBT.md (3 new, 1 resolved). Fix TD-001 now with the refactor skill, or file issues for the top 3?
```

## Install

```bash
# ripgrep (required)
sudo apt install ripgrep        # or: brew install ripgrep
# lizard - complexity
pip install lizard              # or: pipx install lizard / uv tool install lizard
# jscpd - duplication (or run via npx without installing)
npm install -g jscpd
```

---
name: js-linter
description: Lint, format-check and type-check JavaScript and TypeScript (.js, .jsx, .mjs, .cjs, .ts, .tsx) with ESLint (flat config), Prettier and tsc. Uses the project's package manager, local binaries and own lint/format scripts. Use for JS lint, TS lint, eslint, prettier, code style, unused variables, type errors, auto-format.
---

# JS/TS Linter Skill

Check JavaScript and TypeScript code for lint errors, formatting and type errors.

## When Invoked

1. **Detect the package manager** from the lockfile: `pnpm-lock.yaml` → pnpm, `yarn.lock` → yarn, `bun.lock`/`bun.lockb` → bun, otherwise npm. Run tools through it (`npx`, `pnpm exec`, `yarn`, `bunx`) so the project's local versions are used.
2. **Prefer the project's own scripts**: if `package.json` has `lint`, `format:check`, `typecheck` or similar scripts, offer to run them (`npm run lint`) and stop here if the user agrees.
3. **Ask files/directory**: default to the files changed on the current branch, else the whole project:
   `git diff --name-only --diff-filter=d origin/main...HEAD -- '*.js' '*.jsx' '*.mjs' '*.cjs' '*.ts' '*.tsx'`
4. **Check configs**:
   - ESLint 9 needs a flat config (`eslint.config.js`/`.mjs`/`.cjs`/`.ts`) and fails without one. Legacy `.eslintrc*` only works with ESLint 8 or below. If there is no config, ask before adding the minimal one below.
   - Prettier uses `.prettierrc*` or the `prettier` key in `package.json`, and its defaults otherwise.
   - Type-check only if there is a `tsconfig.json`.
5. **Run checks**:
   - Lint: `npx eslint {files}`
   - Format: `npx prettier --check {files}`
   - Types: `npx tsc --noEmit -p tsconfig.json` (checks the whole project; filter the output to the selected files)
6. **Show results** grouped by: Lint, Formatting, Types - each with `file:line` and rule name.
7. **Auto-fix if requested** (show the diff afterwards):
   - Lint: `npx eslint --fix {files}` (preview with `--fix-dry-run`)
   - Formatting: `npx prettier --write {files}`
   - Type errors are never auto-fixed; propose edits instead.

## Minimal Flat Config

Only add this after the user agrees. Install: `npm i -D eslint @eslint/js globals`.

```js
// eslint.config.mjs
import js from "@eslint/js";
import globals from "globals";

export default [
  js.configs.recommended,
  { languageOptions: { globals: { ...globals.browser, ...globals.node } } },
];
```

For TypeScript, also install `typescript-eslint` and use:

```js
// eslint.config.mjs
import js from "@eslint/js";
import tseslint from "typescript-eslint";

export default tseslint.config(js.configs.recommended, tseslint.configs.recommended);
```

## Example

```
User: Lint my code
→ pnpm-lock.yaml found → using pnpm
→ package.json has "lint": "eslint ." → Run `pnpm run lint` instead? no
→ Files changed on this branch: src/api.ts, src/util.js

→ pnpm exec eslint src/api.ts src/util.js
→ pnpm exec prettier --check src/api.ts src/util.js
→ pnpm exec tsc --noEmit -p tsconfig.json

## Results

### Lint
⚠️ src/util.js:1:7 - 'unused' is assigned a value but never used (no-unused-vars)
⚠️ src/api.ts:22:5 - Unexpected any. Specify a different type (@typescript-eslint/no-explicit-any)

### Formatting
⚠️ src/util.js - code style issues found
✅ src/api.ts - OK

### Types
⚠️ src/api.ts:30:3 - TS2322: Type 'number' is not assignable to type 'string'

Auto-fix lint and formatting? (yes/no)
```

## Install

```bash
# per project (recommended, versions pinned in package.json)
npm i -D eslint @eslint/js globals prettier
# TypeScript projects
npm i -D typescript typescript-eslint
```

---
name: cpp-linter
description: Lint and format-check C/C++ code (.cpp, .cc, .cxx, .h, .hpp) for style guide compliance and bugs using clang-format, clang-tidy, and cppcheck. Supports Google, LLVM, Chromium, Mozilla, WebKit styles or a project .clang-format/.clang-tidy. Use for C++ lint, code style, static analysis, auto-format.
---

# C++ Linter Skill

Check C++ code for coding standards compliance and common bugs.

## When Invoked

1. **Check tools**: `clang-format --version`, `clang-tidy --version`, `cppcheck --version`. Skip any missing tool and tell the user how to install it.
2. **Ask files/directory**: which files to check? Expand globs to a file list, e.g.
   `git ls-files '*.cpp' '*.cc' '*.cxx' '*.h' '*.hpp'`
3. **Pick the style**:
   - If the repo has `.clang-format` / `.clang-tidy`, use them (`--style=file`) and don't ask.
   - Otherwise ask: Google, LLVM, Chromium, Mozilla, WebKit.
4. **Find compile flags** for clang-tidy:
   - If `compile_commands.json` exists (often in `build/`), pass `-p build`.
   - Otherwise pass flags after `--`, e.g. `-- -std=c++17 -Iinclude`.
5. **Run checks**:
   - `clang-format --style={style} --dry-run --Werror {files}`
   - `clang-tidy {files} -p build` (or `-- -std=c++17`), with `--checks=...` only if there is no `.clang-tidy`
   - `cppcheck --enable=warning,style,performance,portability --inline-suppr --suppress=missingIncludeSystem {files}`
6. **Show results** grouped by: Formatting, Style / static analysis, Bugs & security
7. **Auto-fix if requested**:
   - Formatting: `clang-format --style={style} -i {files}`
   - clang-tidy fixes: `clang-tidy {files} -p build --fix` (review the diff afterwards)

## Supported Styles

| `--style=` | Style |
|------------|-------|
| `Google` | Google C++ Style Guide |
| `LLVM` | LLVM/Clang style |
| `Chromium` | Chromium style |
| `Mozilla` | Mozilla style |
| `WebKit` | WebKit style |
| `file` | Project `.clang-format` |

The [C++ Core Guidelines](https://isocpp.github.io/CppCoreGuidelines/) are not a formatting style; check them with clang-tidy's `cppcoreguidelines-*` checks.

## Tools

- **clang-format**: formatting only (`--dry-run --Werror` to check, `-i` to fix)
- **clang-tidy**: static analysis and style; needs compile flags to be accurate
- **cppcheck**: memory leaks, undefined behavior, out-of-bounds

## Example

```
User: Check my code
Which files? src/*.cpp
No .clang-format found. Which style? Google

→ clang-format --style=Google --dry-run --Werror src/main.cpp src/utils.cpp
→ clang-tidy src/main.cpp src/utils.cpp -p build
→ cppcheck --enable=warning,style,performance,portability --suppress=missingIncludeSystem src/

## Results

### Formatting
⚠️ src/main.cpp:15:4 - code should be clang-formatted
✅ src/utils.cpp - OK

### Style
⚠️ src/main.cpp:42:10 - variable 'n' can be declared const [misc-const-correctness]
⚠️ src/main.cpp:55:3 - base class has non-virtual public destructor [cppcoreguidelines-virtual-class-destructor]

### Bugs & Security
✅ No issues found

Auto-fix formatting? (yes/no)
```

## Common clang-tidy Checks

| Check | Description |
|-------|-------------|
| `readability-*` | Readability rules |
| `performance-*` | Performance suggestions |
| `modernize-*` | Modern C++ idioms |
| `bugprone-*` | Bug detection |
| `cppcoreguidelines-*` | C++ Core Guidelines |
| `clang-analyzer-*` | Static analysis |
| `-*,misc-const-correctness` | Disable all, enable only const-correctness |

## Install

```bash
# Ubuntu / Debian
sudo apt install clang-format clang-tidy cppcheck

# macOS (clang-tidy ships with llvm)
brew install clang-format llvm cppcheck
# clang-tidy is then at "$(brew --prefix llvm)/bin/clang-tidy"
```

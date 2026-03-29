---
name: cpp-linter
description: Check C++ code for style guide compliance using clang-format, clang-tidy, and cppcheck
---

# C++ Linter Skill

Check C++ code for coding standards compliance.

## When Invoked

1. **Ask files/directory**: Which files to check?
2. **Ask standard**: Which style guide?
   - Google
   - LLVM
   - Chromium
   - WebKit
   - Custom
3. **Run checks**:
   - `clang-format --style={standard} --check {file}`
   - `clang-tidy {file} --checks={checks}`
   - `cppcheck --enable=all {file}`
4. **Show results**:
   - Formatting issues
   - Style violations
   - Security warnings
5. **Auto-fix if requested**: `clang-format -i {file}`

## Supported Standards

| Standard | Style |
|----------|-------|
| Google | Google C++ Style Guide |
| LLVM | LLVM/Clang style |
| Chromium | Chromium style |
| WebKit | WebKit style |
| C++ Core | C++ Core Guidelines |

## Tools

- **clang-format**: Code formatting
- **clang-tidy**: Static analysis & style
- **cppcheck**: Memory leaks, undefined behavior

## Example

```
User: Check my code
Which files? src/*.cpp

→ Running clang-format --style=google --check src/main.cpp
→ Running clang-tidy src/main.cpp
→ Running cppcheck src/main.cpp

## Results

### Formatting
⚠️ src/main.cpp:15:4 - Indentation incorrect
✅ src/utils.cpp - OK

### Style
⚠️ src/main.cpp:42:10 - use 'const' for read-only variables
⚠️ src/main.cpp:55:3 - add virtual destructor to base class

### Security
✅ No security issues found

Auto-fix formatting? (yes/no)
```

## Common Checks

| Check | Description |
|-------|-------------|
| readability-* | Readability rules |
| performance-* | Performance suggestions |
| modernize-* | Modern C++ idioms |
| bugprone-* | Bug detection |
| clang-analyzer-* | Static analysis |
| -*,readability-const* | Disable all, enable const |

## Install

```bash
# Ubuntu
sudo apt install clang-format clang-tidy cppcheck

# macOS
brew install clang-format clang-tidy cppcheck
```

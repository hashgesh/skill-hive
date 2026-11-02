#!/usr/bin/env bash
# Test the cliff.toml embedded in skills/changelog/SKILL.md against
# gitmoji-prefixed conventional commits, and against this repo's own history.
#
# Usage: scripts/test-changelog.sh   (needs git-cliff on PATH)
set -euo pipefail

root="$(cd "$(dirname "$0")/.." && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

config="$work/cliff.toml"
awk '/^```toml/{f=1;next} /^```/{f=0} f' "$root/skills/changelog/SKILL.md" > "$config"
[ -s "$config" ] || { echo "error: no toml block found in skills/changelog/SKILL.md" >&2; exit 1; }

fail=0
expect() { # expect <description> <needle> <haystack>
  if grep -qF -- "$2" <<<"$3"; then echo "ok:   $1"; else echo "FAIL: $1 (missing: $2)" >&2; fail=1; fi
}
reject() { # reject <description> <needle> <haystack>
  if grep -qF -- "$2" <<<"$3"; then echo "FAIL: $1 (unexpected: $2)" >&2; fail=1; else echo "ok:   $1"; fi
}

# 1. Synthetic repo covering the formats the conventional-commit skill produces
repo="$work/repo"
git init -q "$repo"
git -C "$repo" config user.name test
git -C "$repo" config user.email test@example.com
for msg in \
  "✨ feat(auth): add login endpoint" \
  ":bug: fix(parser): handle empty input" \
  "♻️ refactor(cache): extract eviction policy" \
  "⚡️ perf: speed up lookup" \
  "💥 feat(api)!: remove v1 endpoints" \
  "📝 docs: add install steps" \
  "🔖 release: v0.9.0" \
  "Merge pull request #1 from someone/feature" \
  "Merge 1a2b3c4 into 5d6e7f8" \
  "Merge tag 'v0.8.0'" \
  "random unconventional commit"; do
  git -C "$repo" commit -q --allow-empty -m "$msg"
done

out="$(cd "$repo" && git-cliff -c "$config" --tag v1.0.0 2>"$work/synthetic.log")"
expect "unicode gitmoji parsed"        "- **auth:** Add login endpoint" "$out"
expect "shortcode gitmoji parsed"      "- **parser:** Handle empty input" "$out"
expect "variation-selector emoji"      "- **cache:** Extract eviction policy" "$out"
expect "breaking change marked"        "Remove v1 endpoints (**BREAKING**)" "$out"
expect "groups ordered and named"      "### Features" "$out"
expect "release date formatted"        "## [1.0.0] - $(date +%Y-%m-%d)" "$out"
reject "group sort prefix stripped"    "<!--" "$out"
reject "release commit skipped"        "V0.9.0" "$out"
reject "unconventional commit dropped" "Random unconventional" "$out"
# only the deliberately unconventional commit may be reported as unparsable
expect "merge commit skipped, not a parse error" "1 commit(s) were skipped due to parse error" "$(cat "$work/synthetic.log")"

# 2. This repo's own history must parse without errors
if git -C "$root" rev-parse --is-shallow-repository | grep -q true; then
  echo "skip: repo history check (shallow clone)"
else
  log="$(cd "$root" && git-cliff -c "$config" --unreleased 2>&1 >/dev/null || true)"
  reject "repo history parses" "skipped due to parse error" "$log"
fi

exit "$fail"

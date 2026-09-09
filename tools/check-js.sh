#!/usr/bin/env bash
# Syntax-check every JavaScript file this site ships. The site has no build step for
# its JavaScript, so this is the only thing standing between a typo and a dead nav.
#
# There is exactly one script here — assets/site.js, a nav toggle — because no page
# on this site makes a network call or takes a credential. The sibling's equivalent
# also scans apps/*.html for inline <script> blocks; this site has no apps/ directory
# to scan, and tools/check_site.py fails the build if a script ever appears that
# references an origin or calls fetch().
set -euo pipefail
cd "$(dirname "$0")/.."
shopt -s nullglob
fail=0
found=0
for f in assets/*.js docs/assets/*.js; do
  found=$((found+1))
  node --check "$f" || fail=1
done
if [ "$found" = 0 ]; then
  echo "check-js: no scripts to check."
elif [ "$fail" = 0 ]; then
  echo "check-js: all $found script(s) parse."
fi
exit $fail

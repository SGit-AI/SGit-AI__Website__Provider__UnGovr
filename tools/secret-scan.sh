#!/usr/bin/env bash
# secret-scan.sh — the required check. This repository is public; the vault its
# content came from was not, so every safety property that material relied on is
# gone. A leaked key here would be the site's own headline.
#
# THE ONE THAT MATTERS HERE. This site reports on a vault, and whoever builds it is
# holding that vault's WRITE key. The write key must never enter this repository —
# not in a brief, not in a comment, not in a test fixture, not in docs/.
#
#   sgit_private_read_…   publishable. It is how a vault is shared, the same way
#                         sgit.ai/llms.txt shares one. Not matched below, on purpose.
#   sgit_private_vault_…  the write key. Never publishable.
#   <passphrase>:<uuid>   the other shape an sgit vault key takes.
#
# Runs over the working tree (or, with --staged, over what is about to be committed).
# Exits non-zero on the first match, and prints the file and line.
set -uo pipefail
cd "$(dirname "$0")/.."

PATTERNS=(
  'sgit_private_vault_[A-Za-z0-9]+'     # sgit vault WRITE key
  'sgit_private_write_[A-Za-z0-9]+'     # ditto, alternate spelling
  '[A-Za-z0-9_-]{20,}:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'  # passphrase:uuid
  # UnGovr Open Data API key. Free to register for, read-only, and still a
  # credential: it carries a per-key daily quota and it identifies whoever
  # registered it. It is issued to the project, never published.
  'ung_live_[A-Za-z0-9]{16,}'
  'ung_test_[A-Za-z0-9]{16,}'
  'sk_[A-Za-z0-9]{32,}'                 # ElevenLabs
  'sk-or-v1-[A-Za-z0-9]{16,}'           # OpenRouter
  'sk-[A-Za-z0-9]{32,}'                 # OpenAI-shaped
  'hf_[A-Za-z0-9]{20,}'                 # Hugging Face
  'AKIA[0-9A-Z]{16}'                    # AWS
  'ghp_[A-Za-z0-9]{36}'                 # GitHub PAT
  'github_pat_[A-Za-z0-9_]{22,}'        # GitHub fine-grained PAT
  'AIza[0-9A-Za-z_-]{35}'               # Google
  'xox[baprs]-[A-Za-z0-9-]{10,}'        # Slack
  '-----BEGIN [A-Z ]*PRIVATE KEY-----'
  # An UnGovr API key pasted into an example. The header name beside an empty
  # placeholder is documentation, not a leak, so the length qualifier matters.
  'X-API-Key:[[:space:]]*[A-Za-z0-9_-]{16,}'
)

status=0
for p in "${PATTERNS[@]}"; do
  # --exclude-dir keeps the scanner out of git internals; everything else,
  # including the built site under docs/, is in scope on purpose.
  if hits=$(grep -rInE --binary-files=without-match \
        --exclude-dir=.git --exclude="$(basename "$0")" \
        "$p" . 2>/dev/null); then
    echo "SECRET SCAN FAILED — pattern /$p/ matched:"
    echo "$hits" | head -20
    status=1
  fi
done

if [ "$status" = 0 ]; then
  echo "secret-scan: clean (${#PATTERNS[@]} patterns, whole tree including docs/)."
fi
exit $status

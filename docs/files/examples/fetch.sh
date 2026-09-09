#!/usr/bin/env sh
# fetch.sh — retrieve one UnGovr endpoint, write the raw bytes unmodified, hash
# those bytes, and print a retrieval-log row. Nothing is parsed before it is
# hashed: a node that cannot name the bytes it came from is an assertion, not a
# retrieval.
#
#   ./fetch.sh https://data.ungovr.org/v1/meta/last-updated.json data/raw/meta-last-updated.json
#
# Prints, tab-separated: UTC timestamp, method, HTTP status, sha256 of the bytes
# on disk, byte count, X-RateLimit-Remaining (blank when the endpoint sends none),
# and the URL.
set -eu
url="$1"; dest="$2"
mkdir -p "$(dirname "$dest")" "$(dirname "$dest")/../headers" 2>/dev/null || true
hdr="$(dirname "$dest")/../headers/$(basename "$dest").headers"
mkdir -p "$(dirname "$hdr")"
code=$(curl -sS --max-time 300 -D "$hdr" -o "$dest" -w '%{http_code}' \
        ${UNGOVR_API_KEY:+-H "X-API-Key: $UNGOVR_API_KEY"} "$url") || code=000
rem=$(grep -i '^x-ratelimit-remaining:' "$hdr" | tr -d '\r' | cut -d' ' -f2- || true)
printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
  "$(date -u +%Y-%m-%dT%H:%M:%SZ)" "GET" "$code" \
  "$(sha256sum "$dest" | cut -d' ' -f1)" "$(wc -c < "$dest" | tr -d ' ')" "${rem:-}" "$url"

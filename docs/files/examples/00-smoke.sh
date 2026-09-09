#!/usr/bin/env sh
# The smallest thing that runs: prove the API answers, with no credential at all.
# This is the whole of pattern 0 for UnGovr's open surface — there is no key to put
# anywhere, so there is nothing to leak.
set -eu
curl -sS -o /dev/null -w 'entities index   HTTP %{http_code}  %{size_download} bytes\n' \
  https://data.ungovr.org/v1/entities/index.json
curl -sS https://data.ungovr.org/v1/meta/last-updated.json
echo

#!/usr/bin/env sh
# The worked example's three retrievals, in order: resolve the county slug from the
# state slice, fetch its detail, fetch its boundary. Three calls, not a loop over
# the entity API — that is what the bulk files are for, and the entity tier is
# 100 requests a day per IP.
set -eu
B=https://data.ungovr.org/v1
./fetch.sh "$B/entities/us/ca.json"                                data/raw/entities-us-ca.json
./fetch.sh "$B/entities/detail/us--ca--santa-barbara.json"         data/raw/entity-detail-us--ca--santa-barbara.json
./fetch.sh "$B/entities/boundaries/us--ca--santa-barbara.geojson"  data/raw/boundary-us--ca--santa-barbara.geojson
# The county's records law is NOT on the entity. It is in a separate corpus, keyed
# by jurisdiction, and joining the two is the inference this whole report is about.
./fetch.sh "$B/laws/records/us--ca.json"                           data/raw/law-records-us--ca.json

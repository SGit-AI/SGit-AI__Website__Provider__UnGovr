#!/usr/bin/env python3
"""
inferred-join.py — Computation 2: how far would the join reach if it were inferred?

Computation 1 measured the edge UnGovr publishes: 0 of 49 sampled entities carry
`open_records.law`. This measures the edge we would have to INFER, and what it
would cost to be wrong.

THE RULE
    An entity slug is a path: us/ca/santa-barbara/spd/goleta-west-sanitary-district.
    A law in /v1/laws/records/index.json is keyed by a jurisdiction that is a path
    of the same shape: us, us/ca, ar/b, mx/baja-california. So for each entity,
    take the LONGEST law jurisdiction that is a prefix of its slug. That is the
    records law most likely to govern it.

WHAT THIS IS NOT
    It is not a claim UnGovr makes. They publish the entities and they publish the
    laws; they do not join them. Every edge this produces is `inferred`, and the
    vault renders it as inferred. Rendered as an assertion it would be a lie about
    the source.

WHAT WOULD MAKE IT WRONG
    Slug hierarchy is geography, and records law is jurisdiction. They coincide for
    general-purpose local government and they come apart for exactly the bodies a
    requester most often wants: federal facilities on state soil, interstate
    compacts, tribal nations, and special districts chartered under their own act.
    Those are counted separately below rather than folded into the headline.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"

laws = json.loads((RAW / "laws-records-index.json").read_text())["laws"]
juris = {l["jurisdiction"]: l for l in laws}

# Bodies whose governing records law is not reliably given by geography.
SUSPECT_PREFIXES = ("us/compact/", "us/fed/", "us/agency/", "us/tribal/")
SUSPECT_TYPES = {"interstate_compact", "federal_category", "tribal_nation", "agency",
                 "regulated_utility", "charter_school"}


def longest_prefix(slug):
    parts = slug.split("/")
    for i in range(len(parts), 0, -1):
        cand = "/".join(parts[:i])
        if cand in juris:
            return cand
    return None


def report(name, frame_file):
    d = json.loads((RAW / frame_file).read_text())
    rows = d["entities"] if isinstance(d, dict) else d
    hit = miss = suspect = 0
    by_law = {}
    for e in rows:
        j = longest_prefix(e["slug"])
        risky = e.get("type") in SUSPECT_TYPES or e["slug"].startswith(SUSPECT_PREFIXES)
        if j:
            hit += 1
            by_law[j] = by_law.get(j, 0) + 1
            if risky:
                suspect += 1
        else:
            miss += 1
    n = len(rows)
    print(f"\n{name}  (n={n}, frame={frame_file})")
    print(f"  a law jurisdiction is a prefix of the slug : {hit:>6}  {100*hit/n:5.1f}%")
    print(f"  no law in the corpus matches              : {miss:>6}  {100*miss/n:5.1f}%")
    print(f"  matched, but geography != jurisdiction    : {suspect:>6}  {100*suspect/n:5.1f}%  <- would need a human")
    top = sorted(by_law.items(), key=lambda kv: -kv[1])[:5]
    for j, c in top:
        print(f"      {c:>6}  ->  {j}  ({juris[j]['name']})")
    return {"frame": frame_file, "n": n, "matched": hit, "unmatched": miss,
            "matched_but_suspect": suspect}


print(__doc__)
print(f"law corpus: {len(laws)} laws over {len(juris)} jurisdictions "
      f"({sum(1 for j in juris if '/' in j)} sub-national)")
out = {
    "computation": "2 — reach of the inferred entity -> records-law edge",
    "rule": "longest law jurisdiction that is a path-prefix of the entity slug",
    "assertion_class": "inferred — UnGovr does not make this claim",
    "strata": [
        report("California, full depth", "entities-us-ca-all.json"),
        report("United States, top level", "entities-us.json"),
        report("United Kingdom, top level", "entities-gb.json"),
        report("France, top level", "entities-fr.json"),
        report("Germany, top level", "entities-de.json"),
    ],
}
(ROOT / "data" / "computation-2.json").write_text(json.dumps(out, indent=1) + "\n")
print("\n-> data/computation-2.json")

#!/usr/bin/env python3
"""
coverage-sample.py — Computation 1: how far can the entity -> records-law join reach?

THE QUESTION
    Of UnGovr's entities, how many carry a non-empty `open_records.law`?

WHY THIS IS A SAMPLE AND NOT A CENSUS
    `open_records` appears in exactly one place in the API: the per-entity detail
    document, /v1/entities/detail/{slug}.json — one HTTP request per entity. It is
    absent from every bulk surface. UnGovr's own OpenAPI description of the
    full-depth index says so: "a compact record ({slug, name, type, parent_slug?,
    population?})". So a census of 327,138 entities costs 327,138 requests, and the
    open tier allows 100 a day. This script therefore measures a stratified random
    sample and reports an interval, not a point.

WHAT A MISSING VALUE MEANS
    A missing law reference is not an error. It is an entity whose records law has
    not been mapped yet, and for much of the world it may not exist in a mappable
    form. The number measures how far the join can currently reach. It is not a
    defect count.

REPRODUCIBILITY
    The seed is fixed and the frames are the retrieved bytes in data/raw/, whose
    sha256s are in provenance/retrieval-log.md. Re-running against the same frames
    selects the same entities.

    python3 bin/coverage-sample.py --plan     # print the sample, fetch nothing
    python3 bin/coverage-sample.py --run      # fetch the details, write the result
"""
import json, random, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw"
SEED = 20260909

# stratum -> (frame file, how many to draw, what the stratum is)
STRATA = {
    "us-ca-full-depth": ("entities-us-ca-all.json", 25,
        "Every descendant of California: counties, cities, school and special districts"),
    "us-top-level":     ("entities-us.json",        12,
        "The 99 direct children of the United States: states, territories, federal categories"),
    "gb-top-level":     ("entities-gb.json",         6, "The direct children of the United Kingdom"),
    "fr-top-level":     ("entities-fr.json",         3, "The direct children of France"),
    "de-top-level":     ("entities-de.json",         3, "The direct children of Germany"),
}


def frame(path):
    d = json.loads((RAW / path).read_text())
    return d["entities"] if isinstance(d, dict) else d


def draw():
    """The sample. Deterministic: same seed, same frames, same entities."""
    out = []
    for name, (path, n, _desc) in STRATA.items():
        rows = frame(path)
        rng = random.Random(f"{SEED}:{name}")          # per-stratum stream
        for e in rng.sample(rows, min(n, len(rows))):
            out.append({"stratum": name, "slug": e["slug"], "type": e["type"]})
    return out


def detail_url(slug):
    return "https://data.ungovr.org/v1/entities/detail/" + slug.replace("/", "--") + ".json"


def wilson(k, n, z=1.96):
    """95% interval. With k=0 the normal approximation gives 0±0, which would
    report certainty this sample cannot support."""
    if n == 0:
        return (0.0, 1.0)
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return (max(0.0, c - h), min(1.0, c + h))


def main():
    sample = draw()
    if "--plan" in sys.argv or "--run" not in sys.argv:
        print(f"seed {SEED} · {len(sample)} entities across {len(STRATA)} strata")
        for s in sample:
            print(f"  {s['stratum']:18} {s['type']:22} {s['slug']}")
        print("\n--run to fetch the details (one request each) and write the result.")
        return 0

    outdir = RAW / "detail-sample"
    outdir.mkdir(parents=True, exist_ok=True)
    rows, log = [], []
    for i, s in enumerate(sample, 1):
        url = detail_url(s["slug"])
        dest = outdir / (s["slug"].replace("/", "--") + ".json")
        r = subprocess.run([str(ROOT / "fetch.sh"), url, str(dest)],
                           capture_output=True, text=True, cwd=ROOT)
        line = r.stdout.strip()
        log.append(line)
        code = line.split("\t")[2] if line else "000"
        if code == "402":
            print(f"HTTP 402 after {i - 1} requests — the free tier is spent. Stopping.",
                  file=sys.stderr)
            break
        if code != "200":
            print(f"  ! {code} {s['slug']}", file=sys.stderr)
            continue
        d = json.loads(dest.read_text())
        law = (d.get("open_records") or {}).get("law")
        rows.append({**s, "has_law": bool(law), "law": law,
                     "keys": sorted(d.keys())})
        print(f"  {i:>3}/{len(sample)}  {'LAW' if law else '  —'}  {s['slug']}")
        time.sleep(0.3)

    by = {}
    for r in rows:
        b = by.setdefault(r["stratum"], {"n": 0, "k": 0})
        b["n"] += 1
        b["k"] += r["has_law"]
    total_n, total_k = len(rows), sum(r["has_law"] for r in rows)
    lo, hi = wilson(total_k, total_n)

    result = {
        "computation": "1 — coverage of the entity -> records-law edge",
        "question": "Of UnGovr's entities, how many carry a non-empty open_records.law?",
        "method": "stratified random sample of per-entity detail documents",
        "why_sample": ("open_records appears only in /v1/entities/detail/{slug}.json, "
                       "one request per entity; it is absent from every bulk surface. "
                       "A census of 327,138 entities is 327,138 requests against a "
                       "100/day open tier."),
        "seed": SEED,
        "retrieved": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "n": total_n, "with_law": total_k,
        "coverage": (total_k / total_n) if total_n else None,
        "ci95_wilson": [round(lo, 4), round(hi, 4)],
        "by_stratum": {k: {**v, "coverage": v["k"] / v["n"] if v["n"] else None,
                           "description": STRATA[k][2]} for k, v in by.items()},
        "by_type": {},
        "not_a_defect_count": ("A missing law reference is not an error. It is an entity "
                               "whose records law has not been mapped yet, and for much of "
                               "the world it may not exist in a mappable form. The number "
                               "measures how far the join can currently reach."),
        "sample": rows,
    }
    for r in rows:
        t = result["by_type"].setdefault(r["type"], {"n": 0, "k": 0})
        t["n"] += 1
        t["k"] += r["has_law"]

    (ROOT / "data" / "computation-1.json").write_text(json.dumps(result, indent=1) + "\n")
    (ROOT / "data" / "computation-1-retrieval.tsv").write_text("\n".join(log) + "\n")
    print(f"\ncoverage {total_k}/{total_n} = {100 * total_k / total_n:.1f}%  "
          f"(95% CI {100 * lo:.1f}–{100 * hi:.1f}%)  -> data/computation-1.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

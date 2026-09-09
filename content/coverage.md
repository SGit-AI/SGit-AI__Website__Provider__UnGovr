---
title: The coverage measurement, and the query that produced it
description: "Computation 1: 0 of 49 sampled entities carry open_records.law. Computation 2: inferring the same edge by slug prefix reaches 96.6%. Both with their queries, seeds and retrieval dates."
lead: "A number without its query is an assertion, and this site exists to argue the opposite. So both computations are here with the exact question, the seed, the sampling frame, the byte hashes of the frames, and the date they were run."
order: 2
toc: true
provenance:
  vault: dkeclt5r
  date: 9 September 2026
  note: "Both computations were run in this session against bytes retrieved in this session."
---

## Computation 1 — the edge they publish

**The question.** Of UnGovr's entities, how many carry a non-empty `open_records.law`?

**Before the number, the framing, because the number is easy to misread.** A missing law reference is not an error. It is an entity whose records law has not been mapped yet, and for much of the world it may not exist in a mappable form. The result below measures how far the join can currently reach. It is **not a defect count**, and there is a build check that refuses to publish the figure on any page that omits this paragraph.

{{coverage}}

### Why this is a sample and not a census

`open_records` appears in exactly one place in the API: the per-entity detail document, one HTTP request per entity. It is absent from every bulk surface — UnGovr's own OpenAPI describes the full-depth index as *"a compact record ({slug, name, type, parent_slug?, population?})"*. {{claim:law-not-in-bulk}}

So a census of 327,138 entities is 327,138 requests, against a free tier of 100 a day: **about 9 years, or $327.14 metered.** {{claim:census-cost}} Nobody on the open tier can compute this number exactly, including us. What can be done honestly is a stratified random sample with a published seed and an interval — which is what is above.

### What would make this wrong

- **If UnGovr already publish this figure**, then computation 1 is not new and the honest response is to cite theirs and check it. No such figure was found on their published pages on 9 September 2026; if one exists, this section is the one to correct.
- **If the sample missed a populated stratum.** 49 draws across five strata cannot rule out pockets of coverage; the 95% interval says so — the true rate could be anything up to 7.3%. It cannot be *high*, which is the only thing this measurement needs to establish.
- **If `open_records` is populated on entity types not sampled.** Seventeen types were drawn, including states, counties, cities, school and special districts, utilities and ministries. A type not in that list is not covered by this claim.

## Computation 2 — the edge we would have to infer

The first computation measures how far the join falls short. This one measures **how far it would reach if we drew it ourselves** — and, more importantly, where drawing it would be wrong.

{{inferred}}

### The rule, in full

An entity slug is a path: `us/ca/santa-barbara/spd/goleta-west-sanitary-district`. A law in the records corpus is keyed by a jurisdiction that is a path of the same shape: `us`, `us/ca`, `ar/b`, `mx/baja-california`. So for each entity, take the **longest law jurisdiction that is a path-prefix of its slug**.

```
us/ca/santa-barbara/spd/goleta-west-sanitary-district
us/ca/santa-barbara
us/ca                 <- longest match: California Public Records Act
us                    (Freedom of Information Act — the shorter, wrong answer)
```

**This is not a claim UnGovr make.** They publish the entities and they publish the laws; they do not join them. Every edge the rule produces is `inferred`, and [the graph draws it that way](/join/) everywhere it appears. Rendered as an assertion it would be a lie about the source.

### Where the rule breaks, which is the point

Slug hierarchy is **geography**. Records law is **jurisdiction**. They coincide for general-purpose local government and they come apart for exactly the bodies a requester most often wants:

| Body | Why geography gives the wrong law |
|---|---|
| Interstate compacts | Governed by their compact and by member-state law, not by where they sit |
| Federal categories and agencies | Federal FOIA applies, whatever state the building is in |
| Tribal nations | Sovereign. Neither state nor federal records law simply applies |
| Regulated utilities | Often private bodies with statutory duties, not public agencies |
| Charter schools | Chartered under their own act, with varying records obligations |

That is the 20.5%. {{claim:inferred-suspect}} It is why the edge carries an assertion class rather than being silently added, and it is the whole reason the vault has assertion classes at all.

## Reproducing both

```bash
# the frames, hashed as they land — the raw bytes, unmodified
./fetch.sh https://data.ungovr.org/v1/entities/us/ca/all.json    data/raw/entities-us-ca-all.json
./fetch.sh https://data.ungovr.org/v1/laws/records/index.json    data/raw/laws-records-index.json

python3 bin/coverage-sample.py --plan   # print the sample, fetch nothing
python3 bin/coverage-sample.py --run    # 49 requests, writes data/computation-1.json
python3 bin/inferred-join.py            # local only, writes data/computation-2.json
```

Both scripts are [downloadable](/examples/) and both are the originals. The seed is `20260909` and the frames are pinned by sha256 in [the retrieval log](/retrievals/), so the same run selects the same entities — which is acceptance test 7, and the reason to build any of this.

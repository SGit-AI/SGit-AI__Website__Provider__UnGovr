---
title: The minimal working examples — as files
description: "The scripts that produced every number on this site, downloadable and runnable. Not illustrations of the method: the originals."
lead: "§6 of the contract asks for the smallest thing that runs, **as a file rather than a snippet**. These are those files, and they are the ones that were actually run — the retrieval log and both computations are their output."
order: 8
toc: false
---

{{examples}}

## Running them

```bash
# 1. prove the API answers, with no credential at all
./00-smoke.sh

# 2. the worked example's four retrievals, hashed as they land
./santa-barbara.sh

# 3. computation 1 — 49 requests, a fixed seed, an interval
python3 coverage-sample.py --plan     # print the sample, fetch nothing
python3 coverage-sample.py --run

# 4. computation 2 — local only, no requests
python3 inferred-join.py
```

`fetch.sh` is the one the others lean on, and it is four lines of actual work. Its whole discipline is the ordering: **write the raw bytes, hash those bytes, log the row, and only then let anything parse it.**

## What they will cost you

Nothing, if you stay inside the free tier. `00-smoke.sh` is 2 requests, `santa-barbara.sh` is 4, and `coverage-sample.py --run` is 49. The entity tier is **100 a day per IP**. {{claim:rate-limits}} The sampler stops itself on a `402` rather than spending anything, because a script that quietly starts billing is a bad script.

Everything they fetch is UnGovr's, and it is used under **CC BY 4.0** with attribution. {{claim:licence-ccby}}

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

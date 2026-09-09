---
title: Release history
description: "Every release of this site, what changed in it, and the date it shipped. One file owns the version and CI refuses to tag if anything disagrees with it."
lead: "`admin/build/version.txt` owns the version and `data/releases.json` owns the history. `bin/bump.py` moves both, and **every row links to that version's own page** — a reader who clicks `v0.1.7` wants to know what v0.1.7 was, not to land on a generic changelog. The release commit's subject repeats it, and **CI refuses to tag if the two disagree** — which is how a site avoids shipping two versions of itself."
order: 12
toc: false
---

{{releases}}

## The pipeline

**validate → tag → deploy**, in that order, a failure at any stage stopping the release.

| Stage | What it does |
|---|---|
| **validate** | The build is reproducible against `content/`; the version agrees everywhere; internal links resolve; every canonical is on the host in `CNAME`; **the key-shape scan is clean over the whole tree including `docs/`**; every claim is cited and dated; all nine sections are present and in order |
| **tag** | Reads `admin/build/version.txt`, finds the commit whose subject carries the same version, refuses if they disagree or if the bump was not the next minor, then tags it |
| **deploy** | Rebuilds from `content/` and publishes `docs/`. Never when validation failed, never from a pull request |

It also runs on pull requests, so branch work is gated before it reaches the release branch.

---
title: Release history
description: "Every release of this site, what changed in it, and the date it shipped. One file owns the version and CI refuses to tag if anything disagrees with it."
lead: "`admin/build/version.txt` owns the version and `data/releases.json` owns the history. `bin/bump.py` moves both, and **every row links to that version's own page** — a reader who clicks `v0.1.7` wants to know what v0.1.7 was, not to land on a generic changelog. The release commit's subject repeats it, and **CI refuses to tag if the two disagree** — which is how a site avoids shipping two versions of itself."
order: 12
toc: false
---

{{releases}}

## Why the newest release has no commit beside it yet

Every row above names the git commit it was built from, except the newest — and that is not an oversight, it is arithmetic. **A commit cannot contain its own hash.** Recording the sha and amending the release commit produces a *different* sha; recording that one and amending again produces another. It does not converge.

So the sha is written by the **following** commit, and two things stop "later" becoming "never": `check_version_agreement` requires a commit on every release but the newest, and `bin/bump.py` refuses to move to the next version while the current one is still blank.

This was found the honest way — by running the workflow, watching the recorded sha and `git rev-parse HEAD` disagree, and noticing that fixing it once would not fix it twice.

## The pipeline

**validate → tag → deploy**, in that order, a failure at any stage stopping the release.

| Stage | What it does |
|---|---|
| **validate** | The build is reproducible against `content/`; the version agrees everywhere; internal links resolve; every canonical is on the host in `CNAME`; **the key-shape scan is clean over the whole tree including `docs/`**; every claim is cited and dated; all nine sections are present and in order |
| **tag** | Reads `admin/build/version.txt`, finds the commit whose subject carries the same version, refuses if they disagree or if the bump was not the next minor, then tags it |
| **deploy** | Rebuilds from `content/` and publishes `docs/`. Never when validation failed, never from a pull request |

It also runs on pull requests, so branch work is gated before it reaches the release branch.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

# 05 — Verification: Both Deliverables

**version** v0.33.68
**date** 9 September 2026

[← 04 The Site](04__the-site.md) · [00 Start Here](00__START-HERE.md)

---

## The Rule

**Every claim carries a state, and the default is the weakest one.** It applies to this pack about itself: the status column below is what is true at the moment of writing, not what is hoped for.

---

## A · The Vault's Thirteen Tests

**These live in the vault at `pack/06__verification.md` and are its property, not this pack's.** Move their states; do not rewrite the tests.

| # | Test | Now | After the MVP |
|---|---|---|---|
| 1 | A named real entity resolves from its published slug and its boundary renders | `unevidenced` — blocked | **Should pass** |
| 2 | Every provision node carries the hash of its source bytes and a retrieval date | `unevidenced` | **Should pass** |
| 3 | The instrument's markdown rebuilds from the graph byte for byte | `unevidenced` | Depends on B3. **If the CPRA is HTML-only, say so rather than weakening the test** |
| 4 | A provision links to the page or byte range that produced it, and the viewer opens it | `unevidenced` | Out of MVP. Stays open |
| 5 | **Nodes derived from their data are visually distinct from nodes that are our model** | `unevidenced` | **Must pass. A partner checks it first** |
| 6 | Zoom into an entity, a law and a provision; each expands under identical rules | `unevidenced` | Out of MVP. Stays open |
| 7 | The same query returns the same nodes on a rerun | `unevidenced` | **Must pass. It is the reason to build any of this** |
| 8 | The vault opens read-only for a stranger and asks for nothing | `unevidenced` | **Must pass. The site links to it** |
| 9 | The demonstration is citable by version | `asserted` | **Should reach `verified`** once a third party opens a pinned link |
| 10 | The compiled table is one artefact rather than thousands of files | `unevidenced` | **Must pass** |
| 11 | Every computed number is shown beside the query that produced it, with the retrieval date | `unevidenced` | **Must pass for computation 1** |
| 12 | The compiled artefact is checkable against the retrieved JSON it came from | `unevidenced` | **Must pass** |
| 13 | The pack is in the vault as its first commit, readable before anything is built | **`programmatic-out-of-band` — passes** | Stays passing. **Do not disturb the history that proves it** |

**Seven of thirteen should pass after the MVP.** Four are honestly out of scope and one depends on a fact nobody has established. **A vault claiming thirteen of thirteen after one session has stopped measuring and started asserting.**

## B · The Site's Gate

**These are build failures, not review comments.** Copy them from the sibling rather than reimplementing.

| # | Check | Note |
|---|---|---|
| S1 | The build is reproducible — committed `docs/` matches the sources | |
| S2 | Version agreement across every page badge, the release history and both machine indexes | |
| S3 | Internal links resolve, and every canonical is on the host in `CNAME` | |
| S4 | No root-absolute internal URL | **The sibling shipped one and served unstyled for a day** |
| S5 | No bare `<https://…>` autolink | It reaches the browser as an unknown tag and the URL vanishes |
| S6 | **A key-shape scan over the whole tree, including `docs/`** | **The one that will bite you. You are holding a write key** |
| S7 | Every claim cited, every state dated; a claim on a page and not in the ledger fails the build | |
| S8 | The disclosure line present on every page | A disclosure found at the bottom does the opposite of its job |
| S9 | A markdown twin at every path | So an agent never parses HTML |
| S10 | `llms.txt` and `llms-full.txt` present and version-consistent | The hub syncs from these |
| S11 | **All nine contract sections present, in order** | *"A provider page that skips §9 is the thing this family exists not to be"* |
| S12 | Every vendor quote carries its **product**, URL and date read | The rule that has already caught somebody |

## C · What Would Make This Pack Wrong

**Stated in advance, because a specification that cannot be refuted is not one.** Five are inherited from the vault; five are new to this pack.

| If this turns out to be true | Then |
|---|---|
| **UnGovr already publishes the law-edge coverage number** | Computation 1 is not new. **Cite theirs and check it** rather than presenting it as a finding |
| Their `open_records.law` coverage is near-total and richly structured | The gap is smaller than claimed and the argument shrinks to the provision layer |
| The CPRA has no usable machine-readable source | Test 3 cannot pass. **Say so and pick a different instrument; do not weaken the test** |
| The four cross-references *are* exposed somewhere | The join is cheaper than described and part of the vault's model is over-engineered |
| DuckDB-WASM cannot carry a cold open | The recommendation is wrong. **Fall back to the proven SQLite path** |
| **The family's contract genuinely does not admit a data provider** | Then §1 of `04__the-site.md` is wrong, and this belongs somewhere other than `providers.sgit.ai` — **a decision for the project lead, not for you** |
| The sibling's `build.py` differs materially from what `02__the-house-pattern.md` infers | **Likely in places.** That file was written from the live sites, not the repository. **Correct it beside itself** |
| The default branch is `main` and the observed `dev` was a working branch, or the reverse | One question, asked before the first push, saves a release |
| **Your container is refused egress too** | Take the same decision as the previous session, log it the same way, and build what can be built. **Do not substitute a lossy path** |
| Publishing a `dev.*` vault link from a public site is unacceptable | The vault moves to production first. **A vault step, not a site change** |

## D · Handback: What A Human Must Decide Or Check

**Kept short enough to work through in one sitting**, in the sibling's own style. This becomes `HANDBACK.md` in the site repository.

| # | Item | Why it cannot be decided here |
|---|---|---|
| 1 | **The vault write key**, handed over out of band | It must never enter the repository, and the key-shape scan is a required check |
| 2 | **Is the UnGovr API key available to this session?** | Blocker B2. **The AI-laws answer unblocks 1,064 parked crosswalks** and is the highest-value unknown in the project |
| 3 | **Default branch: `dev` or `main`?** | Observed as `dev` with one commit; the sibling links under `main` |
| 4 | **May a `dev.send.sgraph.ai` vault be linked from a public site?** | Or does the vault move to production first |
| 5 | **When does `ungovr.providers.sgit.ai` get pointed?** | It answers 404 today. The site ships regardless, under the project path |
| 6 | **Does the hub's contract get a correction filed against it** for the open-data-provider extension? | It is a change to a shared contract, so it is the project lead's call |
| 7 | **Do we tell UnGovr before publishing?** | The licence permits it with attribution. **Asking is not required and is probably right** |
| 8 | **Who is the named owner on the acceptance node?** | Step 7 needs a real name, an interval and a revocation path. **An acceptance without an owner is a note** |

## E · Honest Tensions

| Tension | Note |
|---|---|
| Publishing a site about a nonprofit's data gap | It is the clearest possible argument, and it is a stranger telling them their model is short by one edge |
| Extending "provider" to admit a data publisher | It makes the comparison matrix richer, and it stretches a definition the family wrote deliberately narrow |
| Shipping a site whose ledger is mostly `docs` and `spec` | **The family has a state for exactly this**, and a site that waits for everything to be verified ships nothing |
| A site self-contained by CI rule, reporting on a vault that lives elsewhere | Static copy plus a link is the resolution, and the copy is stale the moment the vault moves |
| Building on a snapshot | Reproducible and dated, **and stale the moment they push** |
| Two claim vocabularies on one project | They answer different questions and merging them would lose both. **And two vocabularies is a thing a reader can get wrong** |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

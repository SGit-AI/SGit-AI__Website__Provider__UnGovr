# 06 — Verification: Acceptance Tests, Claim States, Blockers

**version** v0.33.67
**date** 8 September 2026

[← 05 The Workbench](05__the-workbench.md) · [Pack hub](README.md) · [00 README](00__README.md)

---

## The Rule This File Enforces

> **Every claim carries a state, and `unevidenced` is the default.**

Settled 4 September. **It applies to this pack about itself**, which is why the status column below is mostly `unevidenced` and why that is the correct reading rather than an embarrassing one. Nothing here is built. A pack that marked its own tests as passing before the work existed would fail the discipline it specifies.

---

## The Acceptance Tests

**Thirteen tests.** The dev brief lists twelve and numbers two of them `10`; the duplicate is recorded in the corrections section below rather than silently fixed, and the list is renumbered here to 13.

| # | Test | Why | Status |
|---|---|---|---|
| 1 | A named real entity resolves from its published slug and its boundary renders | The join is live rather than illustrated | `unevidenced` — **blocked**, see below |
| 2 | Every provision node carries the hash of its source bytes and a retrieval date | The provenance claim, checkable | `unevidenced` |
| 3 | The markdown of the instrument rebuilds from the graph byte for byte | The method site's own standard, applied here | `unevidenced` |
| 4 | A provision links to the page or byte range that produced it, and the viewer opens it | What makes test 2 more than an assertion | `unevidenced` |
| 5 | **Nodes derived from their data are visually distinct from nodes that are our model** | The two-edge discipline, and **the thing a partner will check first** | `unevidenced` |
| 6 | Zoom into an entity, a law and a provision, and each expands under identical rules | The fractal test | `unevidenced` |
| 7 | The same query returns the same nodes on a rerun | Deterministic, **which is the reason to build it at all** | `unevidenced` |
| 8 | The vault opens read-only for a stranger and asks for nothing | The shareable form, as the Risk Graph Explorer already does | `unevidenced` |
| 9 | The demonstration is citable by version | A release is the same objects rather than a copy that drifted | **`asserted`** — release channel configured at this commit; not yet exercised by a third party |
| 10 | The compiled table is one artefact rather than thousands of files | The write-amplification measurement of 7 September, applied | `unevidenced` |
| 11 | Every computed number is shown beside the query that produced it, and the retrieval date | **A number without its query is an assertion** | `unevidenced` |
| 12 | The compiled artefact is checkable against the retrieved JSON it came from | The provenance claim, end to end | `unevidenced` |
| 13 | **The pack is in the vault as its first commit and is readable before anything is built** | The method, demonstrated by the artefact | **`programmatic-out-of-band`** — this file is that commit. Verifiable from the vault's own history |

**Test 13 is the only one that passes today, and it passes by construction.** That is the intended state of a pack published before its implementation.

---

## Blockers, Recorded Rather Than Worked Around

### B1 — Egress policy refuses `data.ungovr.org`

**Status: open. It blocks tests 1, 2, 3, 4, 10 and 12.**

The session that would perform the retrieval cannot reach the host over its shell. The proxy's own log:

```
{
  "ts": "2026-09-08T22:13:06.108Z",
  "kind": "connect_rejected",
  "detail": "gateway answered 403 to CONNECT (policy denial or upstream failure)",
  "host": "data.ungovr.org:443"
}
```

**This is the same failure the research brief of 8 September records**, where an issued API key could not be used because the session's egress policy refused the authenticated host. **It is now confirmed to apply to the open endpoints too, not only the authenticated ones.** That is new information and it is worse than the earlier finding.

**One path is open and it was deliberately not taken.** A web-fetch tool can reach the host, and it returns *model-summarised text rather than raw bytes*. A retrieval through that path cannot carry a `response_sha256`, because there are no source bytes to hash — only a paraphrase of them. **Committing such a payload as if it were a retrieval would put a false provenance record at the root of a vault whose entire argument is provenance.**

**So nothing was fetched.** The pack ships with the retrieval specified and unrun.

| Resolution path | Cost | Preference |
|---|---|---|
| Run the fetch from an environment with unrestricted egress and commit the raw bytes | Low. It is four open endpoints and one bulk download | **Preferred** |
| Have the bulk JSON supplied directly and hash it on arrival | Low, and the provenance holds if the supplier records their own retrieval | Acceptable |
| Fetch through the summarising path and mark every node `method: transcribed-through-model`, with no content hash | Low effort, **high cost to the argument** | **Rejected** |

**The rejection is the finding.** A vault that argues for byte-level provenance and then ships transcribed data has refuted itself in its first commit.

### B2 — The two key-gated corpora remain unread

**Status: open, and it is the same blocker as B1 plus a key question.**

`/ai-laws/*` and `/cgj/reports/{id}.json` are gated behind `X-API-Key`. **These are the two most interesting endpoints to this work** and neither has been read.

The AI-laws corpus matters beyond this vault: **the conformance work of 4 September left 1,064 crosswalks with nothing to resolve into, blocked until another framework is published as a graph.** Whether UnGovr's AI-law corpus is a graph or only per-jurisdiction verdicts is **the single most valuable question to ask them**, because one answer unblocks a parked item.

### B3 — The instrument's source format is unknown

**Status: open. It gates test 3.**

The EU AI Act vault was tractable because Formex XML exists. **Whether the California Public Records Act has an Akoma Ntoso rendering, or a published XML source of comparable quality, has not been established.**

**If Californian statute is available only as HTML, the byte-for-byte rebuild claim is weaker and the decomposition is harder.** That must be stated in the vault rather than discovered by a reader. **Resolve this before writing any parser**, because it may change which provision — or which instrument — the worked example uses.

### B4 — The entity slug is not known

**Status: open, downstream of B1.**

The Santa Barbara County slug has deliberately **not been guessed**. It is resolved from `/entities/us/ca.json` and transcribed verbatim. A guessed slug in a vault about published identifier spaces would be the most embarrassing possible defect.

### B5 — Upstream: no collection roots for pinned releases

**Status: open, upstream, not fixable here.**

There are no collection roots yet, so when garbage collection is built, **pinned commits must become roots or a published release could be collected out from under a live link.** This vault's citation story depends on that being resolved upstream. It is recorded here so that a reader relying on a pinned link knows the dependency exists.

---

## Corrections Recorded Beside The Thing

**A correction is a proposal recorded beside the thing rather than an edit to it, and no file has two writers.** Two are open against the source briefs.

| # | Against | Correction |
|---|---|---|
| C1 | The dev brief's acceptance-test table | **Two rows are numbered `10`.** The tests themselves are distinct and both are kept. Renumbered to 13 above; the source is not edited |
| C2 | The research brief's finding on egress | It records that the *authenticated* host was refused. **The open host is refused too.** Recorded here rather than as an edit to that brief |

---

## What Would Make This Pack Wrong

**Stated in advance, because a specification that cannot be refuted is not one.**

| If this turns out to be true | Then |
|---|---|
| Their `open_records.law` coverage is near-total and richly structured | **The gap this vault exists to close is smaller than claimed**, and the argument shrinks to the provision layer alone |
| The CPRA has no usable machine-readable source | Test 3 cannot pass and the honest move is to say so and pick a different instrument, not to weaken the test |
| The cross-references to GeoNames, Wikidata, OCD and FIPS *are* exposed | The join is cheaper than described and part of [`02__the-model.md`](02__the-model.md) is over-engineered |
| DuckDB-WASM cannot carry the workload on a cold open | The recommendation in [`05__the-workbench.md`](05__the-workbench.md) is wrong and should be replaced with the proven SQLite path |
| UnGovr already publishes the coverage number | **Computation 1 is not new**, and the honest response is to cite theirs and check it rather than to present it as a finding |

---

## Honest Tensions

| Tension | Note |
|---|---|
| Showing a partner the gap in their data | It is the clearest possible argument, and it is a stranger telling them their model is short by one edge |
| Building on a snapshot | It is reproducible and dated, and **it is stale the moment they push** |
| One county, one law | Depth beats breadth for a demonstration, and **one instance proves nothing about coverage** |
| Our nodes on their graph | The attach-never-mutate rule makes it safe, and a viewer renders both as one dataset unless the classes are visibly distinct |
| The determinism claim | The strongest property here, and it holds only while both address schemes are stable |
| Building a corrections path before asking | It demonstrates the point, and it implies their data needs correcting. Ships empty |
| Doing this before the meeting | A built thing beats a slide, and **arriving with one can read as presumption rather than as effort** |

---

## Open Questions

| Question | Notes |
|---|---|
| Is the AI and crawling law corpus a graph, or only per-jurisdiction verdicts? | **The ask with the highest value.** It unblocks 1,064 parked crosswalks |
| Are the GeoNames, Wikidata, OCD and FIPS cross-references exposed in the API? | On the platform page, absent from the schema |
| Do we ask before publishing a vault built on their data? | The licence permits it with attribution. **Asking is not required and is probably right** |
| How does a snapshot stay honest as their data moves? | The retrieval date is the minimum. **A refresh cadence is the real answer** |
| Does the corrections offer go in the vault, or stay a conversation? | Built, and shipped empty, per [`04__the-vault.md`](04__the-vault.md) |
| Does this vault join the catalogue immediately? | Yes. Under a minute, and a graph vault absent from the index argues against its own method |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

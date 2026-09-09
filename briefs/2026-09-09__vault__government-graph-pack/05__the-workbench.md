# 05 — The Workbench: Pipeline, Artefacts, Database, Computations

**version** v0.33.67
**date** 8 September 2026

[← 04 The Vault](04__the-vault.md) · [Pack hub](README.md) · Next → [06 Verification](06__verification.md)

---

## Why This Changes The Vault's Character

**A demonstration argues. A workbench lets somebody check the argument themselves.**

Their open-data page offers complete datasets as JSON for offline analysis, research or integration. That single fact turns this from a thing shown at a meeting into a thing handed over after it — data, transformations and the application over them in one artefact that runs in a browser and travels as a link.

**The precedent is published**: one of the vaults on the demos index is an eleven-step risk-acceptance walk running SQLite in the browser.

---

## The Engineering Constraint That Decides The Shape

**This is the single most important paragraph in the pack, and getting it wrong is expensive rather than untidy.**

**Every write is a commit, and there is no host-side staging.** Writing one file into a folder produces a new blob, **a new tree object for that folder and for every ancestor up to the root**, a new commit and a ref write. A tree entry costs roughly 280 bytes.

| Files already in the folder | Tree rewritten per new file | To store a 200-byte record |
|---|---|---|
| 100 | ~28 KB | ~140× |
| 1,000 | ~280 KB | **~1,400×** |
| 10,000 | ~2.8 MB | **exceeds the request budget; commits start failing** |

**And nothing is reclaimed.** No deduplication — the same plaintext encrypted twice produces different ciphertext and therefore a different object. No delta compression, no packing, **no garbage collection**. Every version of every tree ever written is still there.

> **A vault holding 160,000 entity files is the worst version of that case.** It would not be slow. It would stop committing.

### So: compile, do not scatter

**Fetch the bulk files, transform once, commit a small number of large artefacts.**

**The 3 MB cap is on what an application may write from inside the browser, not on what the vault may hold.** So the compilation happens offline through the command line and **the browser only reads**.

### And a second cost, which decides commit count rather than file count

History walks truncate silently: ahead and behind counts stop at 100, ancestry at 200, common ancestor at 500. **These are wrong answers rather than errors.** A vault past a few hundred unreconciled commits reports divergence when it is merely behind. **Keep the commit count in the tens, not the thousands.**

Clone and cold open were measured at 202 seconds for 42 commits and 2,375 objects, at roughly 50 ms per object server-side, and **the fix is specified and has not shipped**. A workbench that takes three minutes to open is not a workbench.

---

## The Pipeline

**Load, Extract, Transform, Save** — the pattern documented in this corpus from February and never built.

```
   LOAD       their bulk JSON, per country and per state,
              each with its retrieval date and a hash of the bytes
                    |
   EXTRACT    entities, hierarchy, boundaries, law references
                    |
   TRANSFORM  to two artefacts: the graph, and a columnar table
                    |
   SAVE       committed once, versioned, citable by release
```

**The finality rule applies unchanged: a retrieval that has completed never needs reprocessing.** A dated snapshot is computed once and read forever. That is what makes the workbench cheap to open and what makes the citation honest.

---

## The Compiled Artefacts

| Artefact | Format | Why |
|---|---|---|
| `/data/raw/*.json` | **The retrieved bytes, unmodified**, one file per bulk download | So the compiled artefact is checkable against what it came from. **Acceptance test 12** |
| `/data/entities.parquet` | Parquet, columnar | Compresses far better than JSON and is what the recommended engine reads fastest |
| `/data/graph.json` | One file | The nodes and edges of the worked example |
| `/data/boundaries/` | GeoJSON, **only for the entities in the worked example** | Boundaries are large. 160,000 of them is not a vault, it is a tile server |
| `/provenance/retrieval-log.md` | Markdown | Every fetch: URL, timestamp, method, response hash |

**Ship the table as Parquet rather than JSON.** Columnar, far better compression, and the format the recommended engine reads fastest. **The JSON stays in the vault beside it as the retrieved original.**

**Count the files, not the bytes.** A handful of large artefacts is correct. A folder per country is not.

---

## The Browser Database

**Three candidates, and they are not equivalent for this workload.**

| Candidate | Why it might fit | What to check before committing to it |
|---|---|---|
| **DuckDB in WebAssembly** | **The recommendation.** Reads JSON and Parquet natively, and analytical aggregation over 160,000 rows is precisely what it is for | Bundle size, and **whether its spatial extension is usable in the browser build** |
| SQLite in WebAssembly | **Already proven in a published vault here**, so integration risk is known | Whether analytical queries over this row count stay responsive |
| Postgres in WebAssembly | Interesting because they run Postgres and PostGIS, so a query could be portable to them | **Whether the spatial functions their own queries use exist in the browser build at all** |

**The test that decides it**, and it should be run before any of the seven computations are written: load the compiled Parquet, run computation 1 below, and measure time to first result on a cold open. **If the answer is worse than a few seconds, the recommendation changes and the pack is wrong**, which is a fine outcome recorded honestly.

**And one constraint from the shareable form**: the engine must work on the read-only, static path with no key. Anything requiring a write or an owner-sealed secret disqualifies itself.

---

## The Seven Computations

**These are not decoration. Each answers a question their own site raises and does not answer.**

| # | Computation | Why it matters |
|---|---|---|
| 1 | **Coverage of the law edge**: how many of their entities carry an `open_records.law` reference, and how that varies by country and by entity type | **This is the argument, measured.** It sizes the gap this vault exists to close, from their own data, and it may not exist anywhere |
| 2 | Entity-type distribution, and the ratio of special districts to cities | Their claim is more than ten to one in California. **Reproduce it or correct it** |
| 3 | Coverage density by country and by state, drawn on their boundaries | Half the Atlas is one country, and a map says that better than a sentence |
| 4 | Hierarchy depth, and the entities with no parent and no children | **Orphans are where a graph is thin**, and they are cheap to find |
| 5 | The overlapping-jurisdiction stack for one address, drawn | **The thing only they can do**, rendered so it can be seen |
| 6 | **The address test, reproduced**: how many addresses naming a city fall outside its boundary | Their measurement was 40.7 per cent for Santa Barbara. **Repeating it independently is the strongest possible compliment** |
| 7 | Instrument coverage: which referenced laws exist as addressable provisions and which do not | The join, and its honest gaps |

**One and seven carry the meeting. Everything else is craft.**

### Computation 1, in more detail, because it is the argument

**The question**: of their ~320,000 entities, how many carry a non-empty `open_records.law`?

**The shape of the answer**: a single percentage, then the same percentage broken down by country and by entity type. **The breakdown is where it gets interesting**, because a low overall number caused by 205 countries at uneven maturity is a very different finding from a low number inside the United States, and only one of those is a gap worth closing.

**The honest framing**: a missing law reference is not an error. **It is an entity whose records law has not been mapped yet**, and for most of the world it may not exist in a mappable form. **The number is a measure of how far the join can currently reach, not a defect count**, and the page must say so in those words.

### The discipline that applies to all seven

**Each computation is a query the viewer can see, edit and rerun, with the result stated beside it and the retrieval date on the page.**

**A number without its query is an assertion, and this whole vault exists to argue the opposite.** That is acceptance test 11.

**Applied literally**: no computed figure appears anywhere in this vault — not in a heading, not in a summary, not in the catalogue entry — without the query that produced it being one click away.

---

## Rate Limits And What They Permit

| Data | Limit | Consequence for the workbench |
|---|---|---|
| Entity endpoints | 100/day per IP | **The workbench cannot be built from the per-entity API.** Bulk downloads are the only viable path, which is why they decide the design |
| Bulk downloads | Offered for offline analysis | The intended path. Use it |
| Grand jury indices | Unlimited | Free to explore |
| Grand jury report detail | 50/day per key | Enough for the worked example, not for a corpus |
| Over limit | **HTTP 402** with a payment challenge, $0.001/entity request | Real money, and a reason not to loop over an API in a browser |

**And a note worth carrying into the meeting rather than into the vault.** They have shipped a machine payments flow and an MCP server, both of which this corpus has only researched. **Whatever they have learned about wallets, refusals and agent retries at the 402 is worth an hour of the meeting on its own.**

---

## What The Workbench Does Not Do

| Not done | Why |
|---|---|
| Mirror their API | The vault holds a dated snapshot and points at the live source |
| Hold all 160,000 boundaries | That is a tile server, not a vault |
| Re-fetch on open | Finality: a completed retrieval is never reprocessed |
| Compute anything without showing the query | A number without its query is an assertion |
| Write from the browser | The compilation is a command-line job. The browser only reads |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

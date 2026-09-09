# 03 — Deliverable One: The Vault MVP

**version** v0.33.68
**date** 9 September 2026
**status** Specified. The vault holds the design; this file holds the build order.

[← 02 The House Pattern](02__the-house-pattern.md) · Next → [04 The Site](04__the-site.md)

---

## This Is The Work

**The site is a report on this.** If this is thin, the site's ledger is all `spec` and `unrun` and the family already has one of those. **Build the measurement first.**

---

## Step 0 — Confirm Egress Before Planning Anything

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://data.ungovr.org/v1/entities/index.json
curl -sS https://data.ungovr.org/v1/meta/last-updated.json
```

| Result | Do this |
|---|---|
| `200` | **Blocker B1 closes.** Proceed. Record the close in the retrieval log with the timestamp |
| `403`, `000`, or a proxy denial | **Stop.** Record it in `provenance/retrieval-log.md` exactly as the previous session did, with the proxy's own log line. **Do not substitute a summarising path.** Then build only what can be built without their bytes, and say so |

**And ask about the key.** Blocker B2 is the two key-gated corpora, `/ai-laws/*` and `/cgj/reports/{id}.json`. A key was issued to the project previously and could not be used. **Ask the project lead whether it is available to you before you plan around its absence** — the AI-laws answer unblocks 1,064 parked crosswalks elsewhere in the estate and is the single most valuable unknown in this work.

## Step 1 — Clone The Vault And Read Its Pack

```bash
pip3 install sgit-ai --break-system-packages
sgit --token aws clone <WRITE-KEY-HANDED-TO-YOU-OUT-OF-BAND> government-graph
cd government-graph
sgit remote add dev https://dev.send.sgraph.ai --default   # if not already configured
```

**Then read `pack/02__the-model.md` and `pack/03__the-worked-example.md` properly.** Everything below assumes you have.

**Commit discipline, from `pack/05__the-workbench.md` and it is not advisory.** Every write is a commit; a commit rewrites the tree of its folder and every ancestor at ~280 bytes per entry; nothing is ever reclaimed. **Compile, do not scatter. Keep the commit count in the tens.** Batch a whole phase into one commit rather than committing per file.

## Step 2 — Retrieve, And Hash As You Go

**Nine retrievals, listed in `provenance/retrieval-log.md` under "Still To Retrieve".** All but the last are open endpoints.

**The rule: write the raw response bytes to disk unmodified, hash those bytes, and log before you parse anything.**

```bash
fetch() {  # url, dest
  curl -sS --fail "$1" -o "$2"
  printf '%s  %s  %s\n' "$(date -u +%FT%TZ)" "$(sha256sum "$2" | cut -d' ' -f1)" "$1"
}
```

| # | Endpoint | Produces | Auth |
|---|---|---|---|
| 1 | `/v1/entities/us/ca.json` | **Resolves the Santa Barbara County slug. Closes B4** | Open |
| 2 | `/v1/entities/detail/{slug}.json` | The entity, its `open_records.law`, its hierarchy | Open |
| 3 | `/v1/entities/boundaries/{slug}.geojson` | The boundary, stored unmodified | Open |
| 4 | `/v1/laws/records/index.json` | The records-law corpus index | Open |
| 5 | `/v1/laws/records/{jurisdiction}.json` | The CPRA as they publish it. **Closes or refines B3** | Open |
| 6 | Bulk download, United States | **Computation 1. The argument** | Open |
| 7 | `/v1/meta/schema.json` | Re-confirm the schema at retrieval time | Open |
| 8 | `/v1/cgj/counties/{code}.json` | Santa Barbara grand jury index, for step 6 evidence | Open |
| 9 | `/v1/ai-laws/index.json` | **B2.** The most valuable unread corpus | **Key** |

**Rate limits, and they decide the plan**: entity endpoints **100/day per IP**; grand jury indices unlimited; report detail 50/day per key. **Over the limit the API answers HTTP 402 with a payment challenge** at $0.001 per entity request, Stripe wallet, $5 minimum. **Steps 1–3 are three calls. Do not loop over the entity API — that is what the bulk download is for.**

**Every retrieved file lands in `data/raw/` unmodified**, and every one gets a row in `provenance/retrieval-log.md`: URL, UTC timestamp, method, `response_sha256`, outcome.

**Commit the whole retrieval as one commit**, then cut the release `@2026-09-09-retrieval`.

## Step 3 — Computation 1: The Coverage Of Their Law Edge

**This is the highest-value thing in this pack and it may not exist anywhere.**

**The question**: of their entities, how many carry a non-empty `open_records.law`?

**The shape of the answer**: one percentage, then the same broken down by country and by entity type. **The breakdown is where it gets interesting** — a low overall number caused by 205 countries at uneven maturity is a very different finding from a low number inside the United States, and only one of those is a gap worth closing.

**The framing, which is not optional and must appear on the page in these words or close to them:**

> A missing law reference is not an error. It is an entity whose records law has not been mapped yet, and for much of the world it may not exist in a mappable form. **The number measures how far the join can currently reach. It is not a defect count.**

**And the discipline**: the query is shown beside the result, with the retrieval date. **A number without its query is an assertion**, and this vault exists to argue the opposite.

**Cross-check before you publish it.** If UnGovr already publishes this number, computation 1 is not new, and the honest response is to cite theirs and check it rather than to present it as a finding. That is listed in `pack/06__verification.md` under "What Would Make This Pack Wrong".

## Step 4 — Compile, Do Not Scatter

| Artefact | Format | Note |
|---|---|---|
| `data/raw/*.json` | **The retrieved bytes, unmodified** | So the compiled artefact is checkable against what it came from |
| `data/entities.parquet` | Parquet, columnar | Compresses far better than JSON; fastest for the recommended engine |
| `data/graph.json` | One file | The nodes and edges of the worked example |
| `data/boundaries/` | GeoJSON, **only the worked example's entities** | 160,000 boundaries is a tile server, not a vault |
| `provenance/retrieval-log.md` | Markdown, append-only | Including the failures |

**Count files, not bytes.** A handful of large artefacts is correct; a folder per country is not. **The 3 MB write cap applies to what an application writes from inside the browser, not to what the vault may hold** — so compile at the command line and let the browser only read.

## Step 5 — The Join, Seven Steps

**Follow `pack/03__the-worked-example.md` exactly.** Summarised here only so the build order is visible:

```
 1 ENTITY       real slug, boundary, published law reference   ung:
 2 INSTRUMENT   CPRA as addressable provisions, two hashes     akn:  ← THE JOIN
 3 PROVISION    one clause. The one that creates a duty        akn:
 4 OBLIGATION   what, of whom, within what interval            sg:   ← first node that is ours
 5 CONTROL      what would satisfy it                          sg:
 6 EVIDENCE     at a stated tier, unevidenced by default       sg:
 7 ACCEPTANCE   named owner, interval, revocation path         sg:
```

**Three rules that are the argument rather than decoration.**

**Attach, never mutate.** No `ung:` node is edited, corrected, enriched or re-typed. Transcribe with provenance and leave it alone.

**`sg:resolvesTo` is inferred, not asserted.** It is the only edge crossing from their data into ours and it is the most important claim in the demonstration. **UnGovr did not make this claim.** Rendered like an assertion, it is a lie about the source.

**Origin by shape, assertion class by colour.** Hue is already spent on asserted / inferred / possible, so the `ung:` / `akn:` / `sg:` distinction is carried by shape or border. **A partner checks this first.**

> **On step 3, do not trust the section number in the vault's pack.** It names Gov. Code § 7922.535 as a *candidate to verify*, written from prior knowledge and therefore `unevidenced` by the vault's own rule. **The provision that ships is whichever one the retrieved bytes carry.** If it differs, the pack is wrong and the bytes are right — and that correction is a good thing to publish, not an embarrassment.

## Step 6 — The Vault App, Cut To An MVP

**The vault's `pack/04__the-vault.md` specifies a graph viewer with seven configurable settings and three linked viewers. That is the target, not the MVP.**

**In the MVP:**

- The graph, rendered, with **origin visually distinct from assertion class**
- **Filter by node and edge type** — the one setting a partner will reach for first, because it is how you see `ung:` alone
- Expand and collapse one level
- A node detail panel that shows the provenance fields and **opens the retrieved JSON beside the node**
- Computation 1, with its query shown and the retrieval date on the page

**Out of the MVP, and say so on the page rather than leaving it to be noticed:**

- The full fractal zoom to sentence level (acceptance test 6)
- The document viewer opening a byte range in the instrument's own source (test 4)
- The remaining six computations
- The browser database. **Evaluate DuckDB-WASM against a cold-open load of `entities.parquet` before committing to it**; SQLite-WASM is already proven in a published vault here and is the fallback

**And the constraints that decide the app's shape**: it must open **read-only for a stranger and ask for nothing** (`app.json` requests no permissions), and **nothing on the demonstration path may depend on a model call**, because an owner-sealed LLM key cannot be decrypted on a read-only or static host. Build no app-side navigation — `hud` supplies back, forward, home, reload and a path bar.

## Step 7 — Release, Log, Catalogue

```bash
sgit commit "v0.33.68 — retrieval, coverage, and the worked example"
sgit --token aws push
```

Then, as the Librarian:

- Fill `.vault/releases.json` — the planned entries `2026-09-08-retrieval` and `demo-v1` are already stubbed there with their blockers named. **Re-date the retrieval release to the day you actually fetched.**
- Update `catalogue/entry.json`: `acceptance_tests_passing`, `blockers_open`, `head_commit`.
- Update `pack/06__verification.md` — **move test states, do not rewrite the tests.**
- Append every retrieval to `provenance/retrieval-log.md`, including failures.

**Do not pin the working branch.** A pinned view is read-only for everybody including the owner and refuses with `EPINNED`.

## The MVP Cut Line, In One Table

| In | Out |
|---|---|
| Egress confirmed, or the refusal logged | The seven-computation workbench |
| Nine retrievals with byte hashes | All 58 counties, all 398 laws, all 205 countries |
| **Computation 1, with its query and date** | The browser database, unless it evaluates cleanly |
| The seven-step join for one entity and one clause | Full fractal zoom to sentence level |
| A graph the viewer can filter by type | The document viewer opening byte ranges |
| Provenance visible on every node | The corrections path being used. It stays empty |
| A dated release and an updated ledger | Anything that widens the scope |

**One county. One law. One acceptance. And a refusal to widen it.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

---
title: The briefs, published raw
description: "Every brief this site and its vault were built from, published unedited, with a decision-by-decision account of what was accepted, modified and rejected."
lead: "A site arguing for published provenance that hides its own inputs has refuted itself. So both packs are here, raw and unedited — including the parts this session found to be wrong."
order: 11
toc: true
---

## The two packs

| Pack | What it is |
|---|---|
| [`2026-09-09__pack__ungovr-site-and-vault/`](/briefs/2026-09-09__pack__ungovr-site-and-vault/00__START-HERE.md) | The brief for this session: the two deliverables, the house pattern, the vault MVP, the site, and the acceptance tests for both |
| [`2026-09-09__vault__government-graph-pack/`](/briefs/2026-09-09__vault__government-graph-pack/00__README.md) | The vault's own specification, **published as the vault's first commit before any implementation existed** |

Both are CC BY 4.0. Neither has been edited to match what was built.

## What was accepted

- **The scope discipline.** One county, one law, one acceptance, and a refusal to widen it.
- **The two-edge rule** — nodes derived from their data visibly distinct from nodes that are our model, with origin and assertion class carried by different visual channels.
- **Retrieve, hash, log, then parse.** Every row of [the retrieval log](/retrievals/) follows it.
- **Ship the site at v0.1.0 with all nine sections**, several honestly thin, rather than waiting.
- **Do not substitute a lossy path.** Not needed — [egress worked](/retrievals/) — but the precedent was inherited and would have been followed.

## What was modified

**The framing of the finding.** The pack anticipated a low-but-nonzero coverage number and a gap to be described. The measurement is `0 of 49`, and a bare zero reads as an accusation. So the site leads with what the Atlas is, states the zero **with its interval and its framing sentence**, and pairs it immediately with the 96.6% that says the gap is one derivable hop. There is a build check that refuses to let the number appear on any page without the sentence that says it is **not a defect count**.

**The `spec`/`unrun` expectation.** The pack predicted a ledger that would be mostly `spec` and `unrun`, on the assumption that egress would stay blocked. Egress worked, so most of the ledger is `verified` and `measured` instead. The example files are `verified` rather than `unrun` because they are the scripts that produced the numbers, not illustrations of them.

## What was rejected, or found wrong

**These are corrections filed against the packs, beside them rather than as edits to them** — the house rule, and the third and fourth such corrections on this project.

| # | Against | Correction |
|---|---|---|
| **C3** | `03__vault-mvp.md`, step 3: *"fetch one country subset and compute the coverage of their `open_records.law` edge"* | **Not possible as described.** `open_records` is absent from every bulk surface — country subsets, state slices and full-depth indexes all carry a compact record without it. Coverage can only be **sampled**, one request per entity, and the pack's plan would have measured nothing. [The measurement was redesigned as a seeded stratified sample with an interval.](/coverage/) {{claim:law-not-in-bulk}} |
| **C4** | `04__the-site.md` §2, and the vault pack's model | **The records-law corpus is far richer than assumed.** It is sub-national — 254 of 398 rows — and the California record carries structured obligation data, not just a citation. The gap is not "no structure below the law"; it is **no addressable provision, and no edge from the entity**. That is a narrower and more defensible finding. {{claim:cpra-in-corpus}} |
| **C5** | `03__vault-mvp.md`, step 5: Akoma Ntoso for legislative text | **No Akoma Ntoso exists for the CPRA.** Both source URLs serve JSF-rendered HTML. The `akn:` identifier in the graph is therefore *minted by us following the naming convention*, not retrieved, and is marked `inferred` for exactly that reason. Acceptance test 3 is recorded as unpassable for this instrument rather than weakened. {{claim:cpra-no-akn}} |
| **C6** | `03__vault-mvp.md`, step 2, retrieval 8: `/v1/cgj/counties/{code}.json` with an entity slug | **Two identifier schemes in one API.** The CGJ corpus is keyed by bare county code (`santa-barbara`), the entity API by slug (`us--ca--santa-barbara`). The pack's URL 404s. Logged as a failure rather than silently corrected |
| **C7** | `01__what-is-already-built.md`, blocker B2 | **B2 closes by registering, not by paying.** An API key is free. The pack treats the gated corpora as a commercial unknown; they are a registration decision, and therefore [a relationship decision](/disclosures/). **Closed the same day**: a key was issued to the project mid-session |
| **C8** | `04__the-site.md` §2: *"the AI-law endpoints return a verdict, not provisions… a reader can neither check it nor disagree"* | **Wrong, and the corpus is much stronger than predicted.** It carries 2,915 instruments across 271 jurisdictions with citations, effective dates and statuses, a per-scenario `basis` naming controlling authority, and a `provenance` block with `as_of_date`, `confidence` and `stale`. **The prediction was made without a key and did not survive contact with one.** {{claim:ai-laws-is-instruments}} |
| **C9** | The whole pack, and `02__the-house-pattern.md` on licensing | **The API is not uniformly CC BY 4.0.** The OpenAPI document declares it so; the AI-law payloads carry their own, more restrictive licence. Nothing in either pack anticipated a per-corpus licence split, and it changes what may be republished {{claim:ai-laws-licence}} |
| **C12** | `01__what-is-already-built.md`, the Read URL row | **The URL form does not open the vault.** The brief gives `https://dev.vault.sgraph.ai/en-gb/#<read-key>:dkeclt5r`; the `/en-gb/` segment breaks the client-side fragment routing, and the working form is `https://dev.vault.sgraph.ai/#<read-key>:<id>`. Both return HTTP 200 — it is a single-page app, so the shell serves either way and only the browser can tell them apart, which is why this survived a `curl` check. **The brief is republished unedited**; the corrected form is on [the vault page](/vault/) and in the vault's catalogue entry {{claim:vault-url-form}} |
| **C11** | `04__the-site.md` §3: *"Do not iframe it… Link, do not embed."* | **Wrong, and the estate's real pattern is the opposite.** Every published vault on `sgit.ai/demos/vaults/` is embedded live through SG/Vault's embed protocol: a sandboxed frame, a `postMessage` handshake, and the read key posted to a pinned origin **after** the frame proves it is the right recipient. That is strictly safer than the link the brief prescribed, because **the key never enters a URL**. [The vault now runs on this site that way.](/vault/) {{claim:vault-embed-pattern}} |
| **C10** | `02__the-house-pattern.md` §3, the `patterns:` front-matter example | It shows inline flow mappings (`p0: { verdict: never, note: "…" }`). **The family's `build.py` YAML subset does not parse those** — the block form is required, which is what the sibling's real front-matter uses. The file was written from the live sites rather than the repository, and §5 of that file predicted exactly this class of error |

## What is still open

The handback list — what a human with access must decide, kept short enough for one sitting.

| # | Item |
|---|---|
| 1 | **The vault write key.** Handed over out of band. It must never enter this repository, and [the scan that enforces that is wired](/vault/) |
| 2 | ~~Register for a free UnGovr API key?~~ **Done.** A key was issued to the project mid-session and the corpus was read. What remains: **the key is not in this repository or the vault**, and a build check now refuses both it and the corpus it unlocks |
| 3 | **Default branch.** `dev`, confirmed from the sibling repository's `origin/HEAD`. CI deploys from it |
| 4 | **May a `dev.send.sgraph.ai` vault be linked from a public site?** Or does the vault move to production first — [the link ships on the dev host today](/vault/) |
| 5 | ~~When does `ungovr.providers.sgit.ai` get pointed?~~ **Done, mid-session.** It answered 404 at v0.1.0 and serves at v0.1.1; the project path now redirects to it {{claim:domain-pointed}} |
| 6 | **Does the hub's contract take the open-data-provider correction?** A change to a shared contract, so it is the project lead's call |
| 7 | **Do we tell UnGovr before publishing?** The licence permits it with attribution. Asking is not required and is probably right |
| 8 | **Who is the named owner on the acceptance node?** An acceptance without an owner is a note {{claim:acceptance-unowned}} |

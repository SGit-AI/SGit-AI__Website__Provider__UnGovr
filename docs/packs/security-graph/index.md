---
title: The security-standards graph — a dev pack
description: "Eight files specifying how UnGovr's 327,138 entities become the jurisdiction layer for the security and AI standards this family already holds as graphs. Specified, nothing built."
lead: "**Every security and AI standard tells you what good looks like. None of them tells you who has to do it, or where.** This pack specifies how to connect the two **without merging a single vocabulary** — and it is published before anything is built, so it can be checked against whatever gets built."
order: 14
toc: false
provenance:
  vault: dkeclt5r @ obj-cas-imm-4ae37acb099a
  date: 9 September 2026
  note: "The eight files below are served byte for byte from the vault. Their sha256 is recorded in data/packs-manifest.txt and check_site.py fails the build if a published byte differs."
---

<div class="openbar">
<a class="btn-open" href="/packs/security-graph/00__START-HERE/">Start here &rarr;</a>
<span>Each file opens in a reader with the rest of the pack beside it, and <b>the raw bytes one click away on every page</b>. <b>Read 04 if you only read one</b> &mdash; it is the deliverable: one control, one body, one jurisdiction, end to end.</span>
</div>

## The eight files

| # | File | What it holds | Bytes |
|---|---|---|---|
| — | [`README.md`](/packs/security-graph/readme/) | The pack's own index, as it appears in the vault | [raw](/packs/security-graph/README.md) |
| 00 | [`00__START-HERE.md`](/packs/security-graph/00__START-HERE/) | The argument, the strict order of work, what is already decided | [raw](/packs/security-graph/00__START-HERE.md) |
| 01 | [`01__the-anchor-node-thesis.md`](/packs/security-graph/01__the-anchor-node-thesis/) | Why bridging beats merging, in graphs.sgit.ai's own words | [raw](/packs/security-graph/01__the-anchor-node-thesis.md) |
| 02 | [`02__the-model.md`](/packs/security-graph/02__the-model/) | Five node classes, fifteen edges with named inverses, provenance fields | [raw](/packs/security-graph/02__the-model.md) |
| 03 | [`03__the-standards-map.md`](/packs/security-graph/03__the-standards-map/) | What exists as a graph and what does not — **with AIUC-1's thirteen frameworks counted, not guessed** | [raw](/packs/security-graph/03__the-standards-map.md) |
| 04 | [`04__the-worked-example.md`](/packs/security-graph/04__the-worked-example/) | **The deliverable.** One control, one body, one jurisdiction | [raw](/packs/security-graph/04__the-worked-example.md) |
| 05 | [`05__integration.md`](/packs/security-graph/05__integration/) | Licence to Operate, AIUC-1 conformance, Risk Mandate, the EU AI Act text | [raw](/packs/security-graph/05__integration.md) |
| 06 | [`06__verification.md`](/packs/security-graph/06__verification/) | Thirteen tests, five blockers — one closed — and what would make this wrong | [raw](/packs/security-graph/06__verification.md) |

**Pick a file on the left of any reader page. Raw is always there** — every rendered document names the file it came from, its sha256, and links the bytes, above the text rather than under it. {{claim:pack-reader}}

## What state it is actually in

**Specified, nothing built.** {{claim:pack-nothing-built}} Thirteen acceptance tests: **five pass and every one of the five is inherited** from work this vault had already done on the government side, one is `asserted`, and seven are `unevidenced`. Of the fifteen edges in the model, **five are marked proposed rather than existing**. Four blockers are open.

> **That count was wrong when the pack shipped, and the correction is in the document rather than around it.** File 06 said *"Two of twelve pass"*. The table had thirteen rows and five at `programmatic-inline` — a summary line that had drifted from its own table, because test 13 was added when a blocker closed and three rows were upgraded after the summary was written. It was caught by **parsing the rows with a script instead of reading them**, which is the only reason it was caught, and the old line is quoted in 06 rather than quietly swapped. {{claim:pack-count-corrected}} It is the same failure the pack itself warns about in file 03, where a framework's label had to be checked against its members.

> **A second correction, found while building the reader.** The gate that refuses domain-only links fired on the pack's own pages once they were rendered — so the links were deep-linked at source, and fetching the page one of them pointed at turned up something worse. File 02 said **eight** of graphs.sgit.ai's fifteen established edges were *reused unchanged*. Six came from there, and **four of the six had been quietly renamed** — `observed_on` given the inverse `observation_of` where the published set says `bears_observation`, and three more like it. **Renaming another vocabulary's inverses and calling it reuse is a fork**, which is the exact failure the pack's own rule 6 exists to prevent, committed by the file that states the rule. {{claim:pack-vocabulary-forked}} The four are now theirs, and the old paragraph is quoted in the file rather than swapped out.

## The one number that carries the argument

AIUC-1's conformance vault holds **1,126 crosswalks** from its controls out to 489 distinct control items across thirteen frameworks. **Ninety-five of those crosswalks point at law** — and **three of the four laws are sub-national United States jurisdictions.** {{claim:estate-aiuc-law-share}}

A crosswalk ending at *the Colorado AI Act* is a statement about a text, not about **which bodies in Colorado it binds**. UnGovr's Atlas is keyed on exactly that axis. **[The estate page](/estate/)** has the working, and the vaults it was counted from, running live.

## Why it is published raw

A pack is a source document: it is what somebody would have to disagree with in order to disagree with the work. Summarising it and keeping the real thing private lets the two drift, and the summary is always the flattering one — which is precisely what happened to the test count above.

So these are the vault's bytes, unedited, [with their hashes](/packs/). **The reader is an addition and never a replacement** — every `.md` URL still serves the file exactly as it always did, and the build refuses to ship if a rendered page and its raw file are not the same bytes.

The one thing the reader changes is links: inside a rendered page, `01__the-anchor-node-thesis.md` points at the rendered sibling and the vault-tree breadcrumbs resolve here, because otherwise they would 404 on this host. **The raw file keeps every link exactly as the vault wrote it.** Editing a document's navigation to suit a second home is the first small step towards editing its argument; rendering it with working links is not the same thing, and the bytes are there to check.

**The originals are in the vault**, beside the measurements they cite. [Open it](/vault/), or pick it from [the estate page](/estate/).

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

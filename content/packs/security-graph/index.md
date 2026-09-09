---
title: The security-standards graph — a dev pack
description: "Eight files specifying how UnGovr's 327,138 entities become the jurisdiction layer for the security and AI standards this family already holds as graphs. Specified, nothing built."
lead: "**Every security and AI standard tells you what good looks like. None of them tells you who has to do it, or where.** This pack specifies how to connect the two **without merging a single vocabulary** — and it is published before anything is built, so it can be checked against whatever gets built."
order: 14
toc: false
provenance:
  vault: dkeclt5r @ obj-cas-imm-739913cb1bb0
  date: 9 September 2026
  note: "The eight files below are served byte for byte from the vault. Their sha256 is recorded in data/packs-manifest.txt and check_site.py fails the build if a published byte differs."
---

<div class="openbar">
<a class="btn-open" href="/packs/security-graph/00__START-HERE.md">Start here &rarr;</a>
<span>Or take them in order below. <b>Read 04 if you only read one</b> &mdash; it is the deliverable: one control, one body, one jurisdiction, end to end.</span>
</div>

## The eight files

| # | File | What it holds |
|---|---|---|
| — | [`README.md`](/packs/security-graph/README.md) | The pack's own index, as it appears in the vault |
| 00 | [`00__START-HERE.md`](/packs/security-graph/00__START-HERE.md) | The argument, the strict order of work, what is already decided |
| 01 | [`01__the-anchor-node-thesis.md`](/packs/security-graph/01__the-anchor-node-thesis.md) | Why bridging beats merging, in graphs.sgit.ai's own words |
| 02 | [`02__the-model.md`](/packs/security-graph/02__the-model.md) | Five node classes, fifteen edges with named inverses, provenance fields |
| 03 | [`03__the-standards-map.md`](/packs/security-graph/03__the-standards-map.md) | What exists as a graph and what does not — **with AIUC-1's thirteen frameworks counted, not guessed** |
| 04 | [`04__the-worked-example.md`](/packs/security-graph/04__the-worked-example.md) | **The deliverable.** One control, one body, one jurisdiction |
| 05 | [`05__integration.md`](/packs/security-graph/05__integration.md) | Licence to Operate, AIUC-1 conformance, Risk Mandate, the EU AI Act text |
| 06 | [`06__verification.md`](/packs/security-graph/06__verification.md) | Thirteen tests, five blockers — one closed — and what would make this wrong |

## What state it is actually in

**Specified, nothing built.** {{claim:pack-nothing-built}} Thirteen acceptance tests: **five pass and every one of the five is inherited** from work this vault had already done on the government side, one is `asserted`, and seven are `unevidenced`. Of the fifteen edges in the model, **five are marked proposed rather than existing**. Four blockers are open.

> **That count was wrong when the pack shipped, and the correction is in the document rather than around it.** File 06 said *"Two of twelve pass"*. The table had thirteen rows and five at `programmatic-inline` — a summary line that had drifted from its own table, because test 13 was added when a blocker closed and three rows were upgraded after the summary was written. It was caught by **parsing the rows with a script instead of reading them**, which is the only reason it was caught, and the old line is quoted in 06 rather than quietly swapped. {{claim:pack-count-corrected}} It is the same failure the pack itself warns about in file 03, where a framework's label had to be checked against its members.

## The one number that carries the argument

AIUC-1's conformance vault holds **1,126 crosswalks** from its controls out to 489 distinct control items across thirteen frameworks. **Ninety-five of those crosswalks point at law** — and **three of the four laws are sub-national United States jurisdictions.** {{claim:estate-aiuc-law-share}}

A crosswalk ending at *the Colorado AI Act* is a statement about a text, not about **which bodies in Colorado it binds**. UnGovr's Atlas is keyed on exactly that axis. **[The estate page](/estate/)** has the working, and the vaults it was counted from, running live.

## Why it is published raw

A pack is a source document: it is what somebody would have to disagree with in order to disagree with the work. Summarising it and keeping the real thing private lets the two drift, and the summary is always the flattering one — which is precisely what happened to the test count above.

So these are the vault's bytes, unedited, [with their hashes](/packs/). One consequence: the breadcrumbs inside them (`../../README.md`) point at the **vault's** tree, not this site's. That is republication working as intended. Editing a document's navigation to suit a second home is the first small step towards editing its argument.

**The originals are in the vault**, beside the measurements they cite. [Open it](/vault/), or pick it from [the estate page](/estate/).

---
title: The seven-step join — one entity, one clause, one acceptance
description: "Santa Barbara County to the California Public Records Act and down to an unowned acceptance node, with the provenance of every node and the assertion class of every edge."
lead: "One county. One law. One acceptance. And a refusal to widen it — because one instrument modelled properly beats forty sketched, and a vault that tries to be a complete ontology of government ships nothing."
order: 4
toc: true
wide: true
provenance:
  vault: dkeclt5r
  date: 9 September 2026
  note: "The join was built in this session from bytes retrieved in this session."
---

## How to read it

Two things are being said about every node, and they are different questions:

- **Origin** — whose claim is this? `ung:` is transcribed from UnGovr and **never edited, corrected, enriched or re-typed**. `akn:` is the instrument. `sg:` is our model.
- **Assertion class** — how strongly is it held? `asserted` or `inferred`.

**Origin is carried by border and shape; assertion class by colour.** Hue is already spent on the second, so the first cannot also use it. Merging them would lose both, and a reader checking this work should check that separation first.

{{join}}

## The three rules that are the argument

**The county was resolved, not guessed.** `us/ca/santa-barbara` came out of `/v1/entities/us/ca.json` rather than out of anybody's memory, which is what closed blocker B4. {{claim:sb-slug}}

**Attach, never mutate.** No `ung:` node is edited. The entity above is exactly the bytes UnGovr served, and the things we have to say about it hang off it rather than being written into it. That is what makes the compiled artefact checkable against the retrieved JSON it came from.

**`sg:resolvesTo` is inferred, not asserted.** It is the only edge crossing from their data into our model and it is the most important claim in the demonstration. **UnGovr did not make it.** [The rule that produces it, and the 20.5% of cases where it would be wrong, are measured on the coverage page.](/coverage/)

**The default evidence tier is the weakest one.** The evidence node above is `unevidenced`, and it stays that way, because nobody has observed Santa Barbara County's determinations against the control. That is a statement about **our** observation, not about the county's compliance.

## Two vocabularies, and why they must not merge

This is the thing a reader is most likely to get wrong, so it is stated rather than left implicit.

| | The vault's states | This site's states |
|---|---|---|
| Answer the question | *How well is this subject's compliance observed?* | *How well does this site know what it says?* |
| Values | `unevidenced`, `asserted`, `documented`, `manually-checked`, `programmatic-out-of-band`, `programmatic-inline` | `verified`, `measured`, `docs`, `spec`, `unrun`, `projected` |
| Default | `unevidenced` | nothing ships without one |

**A vault node's evidence tier is never rendered as a site claim state.** If it were, a reader would see `unevidenced` on the evidence node and conclude that *this site does not know something*. It means **the county has not been observed**. The two vocabularies are [crosswalked in the brief](/briefs/), not merged.

## What is out of this MVP, said here rather than left to be noticed

- **The full fractal zoom** to sentence level — zoom into an entity, a law and a provision and have each expand under identical rules. Specified, not built. {{claim:vault-viewer-mvp}}
- **The document viewer opening a byte range** in the instrument's own source. Blocked by something real: [there is no machine-readable CPRA to open](/#9-what-went-wrong). {{claim:cpra-no-akn}}
- **The remaining six computations.** Two are done.
- **A named owner on the acceptance node.** It ships open. {{claim:acceptance-unowned}}

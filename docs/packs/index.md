---
title: The dev packs, published raw
description: "The design documents this work runs on, republished byte for byte from the vault they live in — with the sha256 of every file, so a copy that drifted would be visible."
lead: "A dev pack is how a piece of work is specified here before it is built: the argument, the model, a worked example, and a list of tests it has not passed yet. **They are published raw because a specification that only its author can read is not a specification.**"
order: 13
toc: false
provenance:
  vault: dkeclt5r @ obj-cas-imm-e23f0cecfccf
  date: 9 September 2026
  note: "Copied from packs/ in the vault. tools/check_site.py verifies every published file against a recorded sha256, so a copy that drifted from the vault would fail the build."
---

## What is here

| Pack | What it specifies | Files | State |
|---|---|---|---|
| [**The security-standards graph**](/packs/security-graph/) | How UnGovr's entities become the jurisdiction layer for the security and AI standards this family already holds as graphs | 8 | **Specified, nothing built.** Thirteen tests: 5 pass (all inherited), 1 asserted, 7 unevidenced |

## Why raw

The same reason [the briefs](/briefs/) are raw. A pack is a **source document**: it is what somebody would have to disagree with in order to disagree with the work. Summarising it here and keeping the real thing private would let the summary and the document drift, and the summary would always be the flattering one.

So the files are served exactly as they are in the vault — **byte for byte, with their sha256 recorded** — and where something in one of them is wrong, the correction is filed beside it rather than edited into it.

> **One consequence worth naming.** These documents were written to be read *inside the vault*, and their breadcrumbs still point there — a link like `../../README.md` resolves against the vault's tree, not this site's. That is republication working as intended rather than a broken link: editing the navigation out of a document to suit a second home is the first small step towards editing the argument.

## The pack files are also in the vault

Everything under `/packs/` is a copy. The originals are in `packs/` in the government-graph vault, where they sit beside the measurements they cite and move when the work does. **[Open the vault](/vault/)** — or pick it, and six others, from **[the estate page](/estate/)**.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

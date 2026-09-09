---
title: Four decks, from the vault
description: "What UnGovr is, what we built on it, how it composes with the rest of the estate, and what we plan to build next — 39 slides, each one a projection of a markdown file in the vault."
lead: "Four presentations, **39 slides**, written as ordinary markdown in the vault and rendered here. They read as documents in the vault browser, as slides in the vault's app, and as slides on this page — **and if the three ever disagree, the markdown is right.**"
order: 15
toc: false
provenance:
  vault: dkeclt5r @ obj-cas-imm-a6f0269b0967
  date: 9 September 2026
  note: "Republished byte for byte from decks/ in the vault; check_site.py verifies every file against a recorded sha256, so a copy that drifted would fail the build."
---

| # | Deck | What it covers | Slides |
|---|---|---|---|
| 01 | [**What we learned about UnGovr**](/decks/what-we-learned/) | Eight findings from 76 hashed requests: the 0-of-49, why nobody can census it, the 96.6% that is one hop away, and the licence split | 10 |
| 02 | [**What we built on the site**](/decks/what-we-built/) | The provider report, the argument for admitting an open-data provider at all, and the checks that make its promises enforceable | 9 |
| 03 | [**How this composes**](/decks/how-it-composes/) | What this vault contributes to Risk Mandate, Licence to Operate and the AIUC-1 conformance layer — and what it took from them | 10 |
| 04 | [**What we plan to build**](/decks/what-we-plan/) | The security-standards dev pack: the 95 crosswalks that point at law, the vocabulary we forked by accident, and the blocker that would kill the thesis | 10 |

**Start with 01 if you have never met the data, and 04 if you have.** {{claim:decks-four}}

## How to read them

Every slide is stacked on the page, numbered, with its speaker notes visible — **it is a document first.** `Present` shows one slide at a time with `←` and `→`, `Esc` leaves. `Hide notes` strips the notes for a cleaner read or a cleaner print. A link to `#s7` opens that slide.

None of it needs JavaScript to read: the enhancement is present mode and the toggle, and everything else is in the HTML.

## Why these are rendered rather than read live

sgit.ai's [decks-from-a-vault brief](https://sgit.ai/briefs/vault-decks-on-a-site.html) describes a **live** viewer: the host fetches deck sources from the vault with a read key, runs them in a sandboxed opaque-origin frame, and renders the slide markup in a second frame with scripting off entirely.

**This site does it differently, and the reason is its own contract.** Every page here is static and contacts nothing, with exactly two named exceptions. A live deck viewer would have made every deck page a third, and would have needed a vault reader and two sandboxed frames to do safely what a build step does for free. {{claim:decks-static-not-live}}

What that costs is **liveness**. When the vault moves ahead of this site, **this site is behind** — and says so rather than guessing. The live decks are one click away: they are the Decks view of the vault's own app, which runs on [the vault page](/vault/) and on [the estate page](/estate/), and they move the moment the vault does.

What carries over from that brief unchanged is the part that matters most: **the raw markdown is always available for every deck**, the viewer is an addition rather than a replacement, and every rendered slide is one click from the file it was rendered from — [01](/decks/01__what-we-learned.md) · [02](/decks/02__what-we-built.md) · [03](/decks/03__how-it-composes.md) · [04](/decks/04__what-we-plan.md).

## Markdown is the source, and that is the whole point

A slide is an `##` heading and everything under it, split on a `---` rule. A blockquote opening `**Notes.**` is speaker notes. Front matter carries the title, subtitle and date. That is the entire format.

The site's parser is a **port of the vault app's**, so both render the same slides from the same bytes. It is the same reason the estate's book is generated from its site's markdown rather than authored twice: **a presentation that is a projection of a document cannot drift from it.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

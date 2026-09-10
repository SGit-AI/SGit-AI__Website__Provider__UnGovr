---
title: Six decks, from the vault
description: "What UnGovr is, what we built on it, how it composes, what we plan next, how this site publishes and what its build refuses — 60 slides, each one a projection of a markdown file in the vault."
lead: "Six presentations, **60 slides**, written as ordinary markdown in the vault and rendered here as real 16:9 slides — **and as PDFs you can send to somebody.** They read as documents in the vault browser, as slides in the vault's app, and as slides here; if they ever disagree, the markdown is right."
order: 15
toc: false
provenance:
  vault: dkeclt5r @ obj-cas-imm-ca05faec37fd
  date: 9 September 2026
  note: "Republished byte for byte from decks/ in the vault; check_site.py verifies every file against a recorded sha256, so a copy that drifted would fail the build."
---

| # | Deck | What it covers | Slides | PDF |
|---|---|---|---|---|
| 01 | [**What we learned about UnGovr**](/decks/what-we-learned/) | Eight findings from 76 hashed requests: the 0-of-49, why nobody can census it, the 96.6% that is one hop away, and the licence split | 10 | [**⇓ 1521 KB**](/files/decks/what-we-learned.pdf) |
| 02 | [**What we built on the site**](/decks/what-we-built/) | The provider report, the argument for admitting an open-data provider at all, and the checks that make its promises enforceable | 9 | [**⇓ 1552 KB**](/files/decks/what-we-built.pdf) |
| 03 | [**How this composes**](/decks/how-it-composes/) | What this vault contributes to Risk Mandate, Licence to Operate and the AIUC-1 conformance layer — and what it took from them | 10 | [**⇓ 1139 KB**](/files/decks/how-it-composes.pdf) |
| 04 | [**What we plan to build**](/decks/what-we-plan/) | The security-standards dev pack: the 95 crosswalks that point at law, the vocabulary we forked by accident, and the blocker that would kill the thesis | 10 | [**⇓ 1079 KB**](/files/decks/what-we-plan.pdf) |
| 05 | [**How this site publishes**](/decks/how-this-publishes/) | **The machinery.** The pack reader, the deck viewer, the PDFs and the version convention — and the three defects found while building them | 11 | [**⇓ 2569 KB**](/files/decks/how-this-publishes.pdf) |
| 06 | [**What the build refuses**](/decks/what-the-build-refuses/) | **The gates.** Thirty-two checks and the defect behind each, with the build actually refusing them on screen | 10 | [**⇓ 1798 KB**](/files/decks/what-the-build-refuses.pdf) |

**Start with 01 if you have never met the data, and 04 if you have. 05 and 06 are about the site itself** — how it publishes, and what it refuses to publish. {{claim:decks-six}} {{claim:decks-four}}

## The PDFs are the point

Each deck prints to a **16:9 PDF at the estate's deck geometry** — 1200×675, one slide per page, no cropping and no second page for a stray footer. {{claim:deck-pdfs}} They are generated from **the same markup the page renders**, so a slide cannot look one way here and another in the file somebody forwards.

**Every screenshot in them is of this site**, captured from a real build rather than mocked — including, in deck 06, **the build itself refusing a bad change**, photographed by breaking the tree on purpose and putting it back — and **every slide that has one carries a link back to the page it shows** — absolute, so they resolve wherever the PDF is opened. {{claim:deck-shots}} That is what makes them worth sending: a reader who never visits the site still sees what it does, and a reader who wants more has the URL in front of them.

The screenshots and the links are **the site's addition, not the vault's**. The words on every slide are the vault's, republished byte for byte. `data/deck-extras.json` holds the mapping and says so at the top of the file.

## How to read them

Every slide is stacked on the page, numbered, with its speaker notes visible — **it is a document first.** `Present` shows one slide at a time with `←` and `→`, `Esc` leaves. `Hide notes` strips the notes for a cleaner read or a cleaner print. A link to `#s7` opens that slide.

None of it needs JavaScript to read: the enhancement is present mode and the toggle, and everything else is in the HTML.

## Why these are rendered rather than read live

sgit.ai's [decks-from-a-vault brief](https://sgit.ai/briefs/vault-decks-on-a-site.html) describes a **live** viewer: the host fetches deck sources from the vault with a read key, runs them in a sandboxed opaque-origin frame, and renders the slide markup in a second frame with scripting off entirely.

**This site does it differently, and the reason is its own contract.** Every page here is static and contacts nothing, with exactly two named exceptions. A live deck viewer would have made every deck page a third, and would have needed a vault reader and two sandboxed frames to do safely what a build step does for free. {{claim:decks-static-not-live}}

What that costs is **liveness**. When the vault moves ahead of this site, **this site is behind** — and says so rather than guessing. The live decks are one click away: they are the Decks view of the vault's own app, which runs on [the vault page](/vault/) and on [the estate page](/estate/), and they move the moment the vault does.

What carries over from that brief unchanged is the part that matters most: **the raw markdown is always available for every deck**, the viewer is an addition rather than a replacement, and every rendered slide is one click from the file it was rendered from — [01](/decks/01__what-we-learned.md) · [02](/decks/02__what-we-built.md) · [03](/decks/03__how-it-composes.md) · [04](/decks/04__what-we-plan.md) · [05](/decks/05__how-this-publishes.md) · [06](/decks/06__what-the-build-refuses.md).

## Markdown is the source, and that is the whole point

A slide is an `##` heading and everything under it, split on a `---` rule. A blockquote opening `**Notes.**` is speaker notes. Front matter carries the title, subtitle and date. That is the entire format.

The site's parser is a **port of the vault app's**, so both render the same slides from the same bytes. It is the same reason the estate's book is generated from its site's markdown rather than authored twice: **a presentation that is a projection of a document cannot drift from it.**

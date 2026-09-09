# Decks

**Markdown is the source of truth. The app's Decks view is a projection of it.**

[🏠 Vault index](../README.md) › **Decks**

---

Four decks — 39 slides — written as ordinary markdown so they read as documents in the vault browser and as
slides in the app. If the two ever disagree, **the markdown is right** — `app/build_appdata.py`
parses these files at build time and the app renders what it finds.

| Deck | What it covers |
|---|---|
| [01 — What we learned about UnGovr](01__what-we-learned.md) | Eight findings from 76 hashed requests: the 0-of-49, why nobody can census it, the 96.6% that is one hop away, and the licence split |
| [02 — What we built on the site](02__what-we-built.md) | The provider report, the argument for admitting an open-data provider, and the checks that make its promises enforceable |
| [03 — How this composes](03__how-it-composes.md) | What this vault contributes to Risk Mandate, Licence to Operate and the AIUC-1 conformance layer, and what it took from them |
| [04 — What we plan to build](04__what-we-plan.md) | The security-standards dev pack: the gap, the 95 crosswalks that point at law, the vocabulary we forked by accident, and the blocker that would kill the whole thesis |

## The format

A slide is an `##` heading and everything under it, separated by a `---` rule. A blockquote
beginning `**Notes.**` is speaker notes: shown in the app behind the **notes** toggle, and simply
part of the document when read as markdown.

Front matter carries the deck title, its subtitle and an accent. Nothing else is required.

## Why markdown rather than a slide format

The same reason the estate's own book is generated from its site's markdown rather than authored
twice: **a presentation that is a projection of a document cannot drift from it.** These files are
readable, diffable, greppable, and survive the app being rewritten.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

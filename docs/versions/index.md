---
title: Release history
description: "Every release of this site, what changed in it, and the date it shipped. One file owns the version and CI refuses to tag if anything disagrees with it."
lead: "`admin/build/version.txt` owns the version. `bin/bump.py` moves it and adds the row below. The release commit's subject repeats it, and **CI refuses to tag if the two disagree** — which is how a site avoids shipping two versions of itself."
order: 12
toc: false
---

<div class="tablewrap"><table class="releases">
<thead><tr><th>Version</th><th>Date</th><th>What changed</th></tr></thead>
<tbody>
<!-- releases -->
    <tr><td class="vnum">v0.1.15</td><td>2026-09-09</td><td>A vault document could run script on this origin, through the pack and deck readers. Confirmed in a browser, closed, and gated — plus link schemes restricted and a literal entity caught.</td></tr>
    <tr><td class="vnum">v0.1.14</td><td>2026-09-09</td><td>A fourth deck — what we plan to build — and all four on the site at /decks/: stacked and printable by default, present mode and deep links on top, markdown one click away.</td></tr>
    <tr><td class="vnum">v0.1.13</td><td>2026-09-09</td><td>What you get when you reach a law: JSON only, no instrument text, no graph — and 254 of the 398 records laws, every sub-national one, with no reachable detail document.</td></tr>
    <tr><td class="vnum">v0.1.12</td><td>2026-09-09</td><td>The vault app names its own release in its header, and the pill opens a table of what each one changed — the same pattern as this nav, reaching a view instead of a page.</td></tr>
    <tr><td class="vnum">v0.1.11</td><td>2026-09-09</td><td>A reader for the pack files: the rest of the pack beside every document and the raw bytes one click above it. Two corrections it surfaced, one of them the pack forking a vocabulary it said it reused.</td></tr>
    <tr><td class="vnum">v0.1.10</td><td>2026-09-09</td><td>The security-standards dev pack, published raw at /packs/ — byte for byte from the vault, hash-checked on every build. Its test count was wrong in both numbers and is corrected.</td></tr>
    <tr><td class="vnum">v0.1.9</td><td>2026-09-09</td><td>The estate page: seven published vaults from across the family, each opening in the page from its own published read key, one at a time and nothing fetched until asked.</td></tr>
    <tr><td class="vnum">v0.1.8</td><td>2026-09-09</td><td>Three markdown-sourced slide decks in the vault: what we learned, what we built, and how it composes with the other vaults.</td></tr>
    <tr><td class="vnum">v0.1.7</td><td>2026-09-09</td><td>The vault link drops the /en-gb/ segment, which broke the fragment routing; a check now refuses it.</td></tr>
    <tr><td class="vnum">v0.1.6</td><td>2026-09-09</td><td>The vault leads the vault page, with an open-in-a-new-tab button; the release channel is withdrawn and test 9 regressed with it; the embed is verified.</td></tr>
    <tr><td class="vnum">v0.1.5</td><td>2026-09-09</td><td>The vault's entry is now a real HTML app with five views; the site says so, and two of its computations exist only there.</td></tr>
    <tr><td class="vnum">v0.1.4</td><td>2026-09-09</td><td>The vault is pushed: 9 of 13 acceptance tests pass, release @2026-09-09-retrieval pinned, and the site names the commit it reports on.</td></tr>
    <tr><td class="vnum">v0.1.3</td><td>2026-09-09</td><td>The vault runs live on the site, embedded through SG/Vault's own embed protocol from the published read key.</td></tr>
    <tr><td class="vnum">v0.1.2</td><td>2026-09-09</td><td>The domain was pointed mid-session: 404 at v0.1.0, serving at v0.1.1. Both states recorded.</td></tr>
    <tr><td class="vnum">v0.1.1</td><td>2026-09-09</td><td>The AI-law corpus, read under a key: 2,915 instruments, and a per-corpus licence that is not CC BY 4.0. Blocker B2 closed.</td></tr>
    <tr><td class="vnum">v0.1.0</td><td>2026-09-09</td><td>First release. All nine contract sections; the coverage measurement and the inferred-join computation with their queries; the seven-step join; the retrieval log; the vault linked by read key.</td></tr>
</tbody>
</table></div>

## The pipeline

**validate → tag → deploy**, in that order, a failure at any stage stopping the release.

| Stage | What it does |
|---|---|
| **validate** | The build is reproducible against `content/`; the version agrees everywhere; internal links resolve; every canonical is on the host in `CNAME`; **the key-shape scan is clean over the whole tree including `docs/`**; every claim is cited and dated; all nine sections are present and in order |
| **tag** | Reads `admin/build/version.txt`, finds the commit whose subject carries the same version, refuses if they disagree or if the bump was not the next minor, then tags it |
| **deploy** | Rebuilds from `content/` and publishes `docs/`. Never when validation failed, never from a pull request |

It also runs on pull requests, so branch work is gated before it reaches the release branch.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

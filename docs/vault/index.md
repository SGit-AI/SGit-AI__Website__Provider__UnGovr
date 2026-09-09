---
title: The government-graph vault — open it read-only
description: "The vault this report is a report on: what it holds, how to open it with nothing but a read key, and why the read key is publishable when the write key never is."
lead: "It is running below, live, decrypted in your browser from the read key on this page. **Nothing on this site holds a copy of it** — a push to the vault changes what you see here with no rebuild and no deploy."
order: 5
toc: false
wide: true
provenance:
  vault: dkeclt5r @ obj-cas-imm-760fee6127a2
  date: 9 September 2026
  note: "The vault's own pack is published raw under /briefs/."
---

<div class="openbar">
<a class="btn-open" href="https://dev.vault.sgraph.ai/#sgit_private_read_d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d:dkeclt5r" rel="noopener" target="_blank">Open the vault in a new tab &#8599;</a>
<span>Five views and a graph canvas &mdash; <b>it has far more room in its own tab</b> than in the frame below.</span>
</div>

<div class="sgv-uiembed" data-vault="dkeclt5r" data-readkey="d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d" data-app="1"></div>

<script>
/* Contract-compliant loader: no `<script src>` anywhere on this site, because every
   page must survive being served from inside a vault, where declarative refs cannot
   be answered. Fetch + eval, the estate's own pattern. The component is vendored
   into this site's assets/ rather than pulled from another origin. */
(function () {
  var root = document.documentElement.getAttribute('data-root') || '';
  fetch(root + 'assets/vault-ui-embed.js')
    .then(function (r) { if (!r.ok) throw new Error(r.status); return r.text(); })
    .then(function (t) { (0, eval)(t); })
    .catch(function (e) { console.error('[vault] embed component failed to load:', e); });
}());
</script>

**Two surfaces open above.** App Mode boots the vault's own `index.html` — six views: the seven-step join, filterable by origin and with the provenance of every node; the coverage measurement; the inferred edge; the shape of the corpus; every retrieval with its hash; and **three slide decks**. **Two of its computations exist only there** — the shape of the 398-law corpus, and what the 16,071 Californian bodies are. {{claim:vault-app}} Under it, the vault browser, with the FILES / SGIT / SETTINGS rail and an explicit **Read-only** badge in the chrome.

**It requests no permissions, makes no network call, and reads exactly one vault file.** That file is deliberately *not* inlined into the page: sgit objects are content-addressed and immutable, so the 33 KB of measurements stay their own object and the vault client caches them — releasing a new version of the app does not re-download the numbers.

> **It ships `verified` rather than `unrun`, and only because somebody watched it.** This page went out badged *written, not yet watched working*: the container that built it cannot open a browser TLS tunnel to the vault host, so the frame could never boot here. The project lead then opened it and the vault came up in App Mode — read-only chrome, five views, the join drawing. {{claim:vault-embed-runs}} **That is the only thing that moves a claim off `unrun`**, and it is why the state existed in the first place.

> **How the key gets there.** The frame is loaded with `?embed=1&parent=<origin>`; the page waits for the frame to announce itself, then posts `{sg:'vault-open', key, mode}` with the target origin pinned. **The key never appears in a URL** and the frame keeps it in memory only. {{claim:vault-embed-pattern}}

> **This vault is on a development host.** `dev.vault.sgraph.ai` is not the production browser, and publishing a `dev.*` URL from a public site is a decision rather than a detail. It ships because the read key is the whole point of §7 and a vault nobody can open is worse than one on the wrong host — but **moving to production is [handback item 4](/briefs/)**, and this page changes when it moves.

## Three decks, and the markdown they come from

The vault carries three presentations — **what we learned about UnGovr**, **what we built on the site**, and **how this vault composes** with Risk Mandate, Licence to Operate and the AIUC-1 conformance layer. Twenty-nine slides, with speaker notes, a present mode and print-to-PDF. {{claim:vault-decks}}

**They are written as ordinary markdown**, in `decks/*.md`, and the app's Decks view is a *projection* of those files, parsed at build time. So they read as documents in the vault browser and as slides in App Mode, and **if the two ever disagree the markdown is right**.

That is the same reason the estate's own book is generated from its site's markdown rather than authored twice: **a presentation that is a projection of a document cannot drift from it.**

The third deck is the one worth reading if you only read one. It is not a summary — it names what this vault contributes to the others (a jurisdiction layer, and a deadline set by statute rather than by an attestation's expiry), what it took from them (the two-edge rule, `unevidenced` as a default, the grant/mandate/delta shape), and it closes on a *what this does not prove* slide borrowed from the conformance layer's own field of that name.

> **The app says which release it is.** A version pill sits in its header, exactly as one sits in this site's nav, and clicking it opens the Provenance view at a table of seven releases with what each one changed — including the three that moved *this site* around the vault rather than the vault itself. {{claim:vault-app-version}} It is a button rather than a link because **a vault app must never assign `location.hash`**, and an internal fragment href lands on the host's broken-link overlay.

## The security-standards dev pack

The vault carries a dev pack under `packs/security-graph/` — **eight files proposing how UnGovr's entities become the jurisdiction layer for the security and AI standards already graphed elsewhere in this family.** {{claim:vault-security-pack}} It is a design document with tests, not an implementation: thirteen acceptance tests, of which **five pass and all five were inherited** from work this vault had already done, one is `asserted`, and seven are `unevidenced`.

Its central move is borrowed rather than invented: *don't merge vocabularies — keep them intact and bridge them through anchor nodes.* Two anchors are proposed, `ung:entity` and `ung:jurisdiction`, and fifteen edges, each with a distinct inverse and five of them marked **proposed** rather than existing.

**One of its files was written twice.** The first draft implied the estate had not applied the anchor pattern. Opening the AIUC-1 conformance vault and counting showed it had — 489 `anchors_to` edges — so the file was corrected to propose a different *axis* of anchor instead of the mechanism. **[The estate page](/estate/) carries that measurement and the vaults it came from**, running live.

## The vault is the experiment; this site is the report

The division is deliberate. **New data processing and visualisation happen in the vault**, where a push changes what a reader sees with no rebuild and no deploy. This site reports on what the vault establishes, and carries the claim ledger that says how well each thing is known.

That is why two of the app's computations are not on this site at all. They are experiments on UnGovr's corpus rather than findings about their API, and the vault is where experiments belong.

## Open it from the command line

```bash
pip3 install sgit-ai --break-system-packages
sgit clone sgit_private_read_d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d:dkeclt5r government-graph
```

## Why publishing this key is safe, and which key it is

**Two keys exist and only one of them is here.**

| | What it does | Publishable |
|---|---|---|
| **Read key** `sgit_private_read_…` | Decrypts and reads. Cannot commit, cannot push, cannot delete | **Yes.** It is how this estate shares a vault — the same way `sgit.ai/llms.txt` does |
| **Write key** `sgit_private_vault_…` | Everything. Rewrites history | **Never** |

The write key for this vault was handed over out of band and **is not in this repository, in any form**. That is not a promise, it is a check: `tools/secret-scan.sh` runs over the whole tree *including the built output in `docs/`*, on every push and every pull request, and refuses the release on a match. It deliberately does not match `sgit_private_read_…`, and `tools/check_site.py` carries the same tripwire a second time against the `passphrase:uuid` shape an sgit key can also take.

**This is the check the brief singled out as the one most likely to bite whoever built this site.** It is wired first, before any content, for that reason.

## What the vault holds

```
  pack/          the specification — 7 files, published as the FIRST commit,
                 before any implementation existed. That ordering is the
                 vault's own acceptance test 13, and the only one that
                 passed before this session
  team/          four agentic roles and the single-writer rule
  data/raw/      the retrieved bytes, unmodified, so the compiled artefacts
                 are checkable against what they came from
  data/          the compiled artefacts: the graph, both computations
  provenance/    the retrieval log, including the failures
  catalogue/     the catalogue submission
  corrections/   ships empty, on purpose
  review/        ships empty
```

**The pack was published before the work, and the history proves it.** That is the strongest demonstration the method has: a design that could be checked against the thing it specified, before the thing existed. This session's commits sit on top of it and do not disturb it.

The pack is also [published raw on this site](/briefs/), because a site arguing for published provenance that hides its own inputs has refuted itself.

## What this site copies, and what it links

**Copied.** The compiled artefacts — `graph.json`, `computation-1.json`, `computation-2.json`, the retrieval log — are copied into this repository at build time and rendered as part of the site. Every table on [the coverage page](/coverage/) and [the join page](/join/) is static HTML built from them. **No page here fetches anything**, which is a build rule, not a preference.

**Linked, never embedded.** The vault itself is a link. An iframe pulling another host into the page is exactly what the no-third-party rule exists to prevent, and it would break the site with JavaScript off. `tools/check_site.py` refuses an `<iframe>` anywhere in the built output.

**The copy is stale the moment the vault moves ahead.** The page says which vault commit it reports on rather than guessing, and that is the honest resolution rather than a fixed one.

## The thirteen acceptance tests

They live in the vault, at `pack/06__verification.md`, and they are its property rather than this site's — this session moved their states and did not rewrite the tests.

| | |
|---|---|
| Passing before this session | **1 of 13** — the pack was in the vault as its first commit |
| **Passing now** | **9 of 13** — 1, 2, 5, 7, 8, 10, 11, 12, 13 |
| Honestly out of MVP scope | **4** — fractal zoom, byte-range document viewer, and two others |
| Cannot pass as written | **1** — test 3, rebuild the instrument byte for byte. [There is no machine-readable CPRA to rebuild from.](/#9-what-went-wrong) Recorded as unpassable rather than weakened {{claim:cpra-no-akn}} |
| **Regressed on purpose** | **1** — test 9, *the demonstration is citable by version*. Two releases were cut and **withdrawn**: the vault settings UI rendered each one's commit as `obj-cas-im`, a 10-character prefix of a 24-character id. A release channel that cannot show which commit it pins does not make anything citable, so the honest state is the weak one until it is fixed {{claim:release-withdrawn}} |

**A vault claiming thirteen of thirteen after one session has stopped measuring and started asserting.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

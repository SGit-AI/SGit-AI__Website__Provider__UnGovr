---
title: The government-graph vault — open it read-only
description: "The vault this report is a report on: what it holds, how to open it with nothing but a read key, and why the read key is publishable when the write key never is."
lead: "The vault is the workload in [§7](/#7-what-we-use-it-for). It holds the retrieved bytes, their hashes, the compiled artefacts, the seven-step join and the specification that was published **before** any of it was built. You can open it read-only, right now, and it will ask you for nothing."
order: 5
toc: true
wide: true
provenance:
  vault: dkeclt5r @ obj-cas-imm-b9c2cddb51e8
  date: 9 September 2026
  note: "The vault's own pack is published raw under /briefs/."
---

## Open it, here

The vault is running below, live, decrypted in your browser from the published read key on this page. **Nothing on this site holds a copy of it** — a push to the vault changes what you see here with no rebuild and no deploy.

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

**Two surfaces open above**: App Mode, which renders the vault's own `_page.json`, and the vault browser under it, with the FILES / SGIT / SETTINGS rail and an explicit **R1 W0 · Read-only** badge in the chrome. The second one is where you can read the retrieval log, open `data/graph.json`, and check the commit history that proves the pack was published before the work.

**How the key gets there.** The frame is loaded with `?embed=1&parent=<origin>`; the page waits for the frame to announce itself, then posts `{sg:'vault-open', key, mode}` with the target origin pinned. **The key never appears in a URL** and the frame keeps it in memory only. `vault-ready` / `vault-error` come back as structured events.

> **Written, and not yet watched working.** The component is the estate's own, vendored unmodified — byte-identical below its provenance header — and the markup and the published read key are checked against it. {{claim:vault-embed-pattern}} **But nobody has seen this frame render.** The container that built this site cannot open a browser TLS tunnel to the vault host: `curl` gets 200 and no frame-blocking headers, Chromium gets `ERR_CONNECTION_RESET`. {{claim:vault-embed-unrun}} So the embed above ships in the state the family has a chip for — **read it, then open it and find out.** If it is blank, the fallback link below opens the same vault in a new tab.

> **This is the one page on this site that opens a network connection**, and it opens exactly one, to `dev.vault.sgraph.ai`. Every other page here fetches nothing at all — [the ledger](/ledger/) says which. The trade is deliberate: an embed that reads the real vault is worth more than a screenshot of one, and it is the estate's own published pattern.

<div class="card-open">
<p class="small dim">SG/Send vault &middot; read-only &middot; asks for no permissions</p>
<h3>government-graph <code>dkeclt5r</code></h3>
<p>Prefer a new tab, or a vault that is having a bad day? The same key, the same vault.</p>
<p class="mono breakall"><a href="https://dev.vault.sgraph.ai/en-gb/#sgit_private_read_d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d:dkeclt5r" rel="noopener" target="_blank">open it read-only in a new tab &rarr;</a></p>
</div>

> **This vault is on a development host.** `dev.vault.sgraph.ai` is not the production browser, and publishing a `dev.*` URL from a public site is a decision rather than a detail. It ships because the read key is the whole point of §7 and a vault nobody can open is worse than one on the wrong host — but **moving to production is [handback item 4](/briefs/)**, and this page changes when it moves.

Or with the CLI:

```bash
pip3 install sgit-ai --break-system-packages
sgit clone sgit_private_read_d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d:dkeclt5r government-graph
```

> **This link is on a development host.** `dev.vault.sgraph.ai` is not the production browser, and publishing a `dev.*` URL from a public site is a decision rather than a detail. It ships here because the read key is the whole point of §7 and a link nobody can open is worse than a link on the wrong host — but **moving the vault to production is [handback item 4](/briefs/)**, and this page changes when it moves.

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
| **Passing now** | **9 of 13** — 1, 2, 5, 7, 8, 10, 11, 12, 13. Pinned by release `@2026-09-09-retrieval` |
| Honestly out of MVP scope | **4** — fractal zoom, byte-range document viewer, and two others |
| Cannot pass as written | **1** — test 3, rebuild the instrument byte for byte. [There is no machine-readable CPRA to rebuild from.](/#9-what-went-wrong) Recorded as unpassable rather than weakened {{claim:cpra-no-akn}} |

**A vault claiming thirteen of thirteen after one session has stopped measuring and started asserting.**

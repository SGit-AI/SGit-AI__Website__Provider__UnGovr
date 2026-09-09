---
title: The government-graph vault — open it read-only
description: "The vault this report is a report on: what it holds, how to open it with nothing but a read key, and why the read key is publishable when the write key never is."
lead: "The vault is the workload in [§7](/#7-what-we-use-it-for). It holds the retrieved bytes, their hashes, the compiled artefacts, the seven-step join and the specification that was published **before** any of it was built. You can open it read-only, right now, and it will ask you for nothing."
order: 5
toc: true
provenance:
  vault: dkeclt5r
  date: 9 September 2026
  note: "The vault's own pack is published raw under /briefs/."
---

## Open it

<div class="card-open">
<p class="small dim">SG/Send vault &middot; read-only &middot; asks for no permissions</p>
<h3>government-graph <code>dkeclt5r</code></h3>
<p>Opens in the SG/Send browser with the read key already in the URL fragment. Nothing to install, nothing to sign in to, nothing to accept.</p>
<p class="mono breakall"><a href="https://dev.vault.sgraph.ai/en-gb/#sgit_private_read_d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d:dkeclt5r" rel="noopener">dev.vault.sgraph.ai/en-gb/#sgit_private_read_&hellip;:dkeclt5r</a></p>
</div>

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
| Should pass after this MVP | **7 of 13** |
| Honestly out of MVP scope | **4** — fractal zoom, byte-range document viewer, and two others |
| Cannot pass as written | **1** — test 3, rebuild the instrument byte for byte. [There is no machine-readable CPRA to rebuild from.](/#9-what-went-wrong) Recorded as unpassable rather than weakened {{claim:cpra-no-akn}} |

**A vault claiming thirteen of thirteen after one session has stopped measuring and started asserting.**

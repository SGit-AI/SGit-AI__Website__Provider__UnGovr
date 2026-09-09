# 01 — What Is Already Built

**version** v0.33.68
**date** 9 September 2026

[← 00 Start Here](00__START-HERE.md) · Next → [02 The House Pattern](02__the-house-pattern.md)

---

## The Vault

**It exists, it is pushed, and it contains a specification and no implementation.**

| | |
|---|---|
| Vault ID | `dkeclt5r` |
| Remote | `https://dev.send.sgraph.ai` |
| Remote token | `aws` — pass as `sgit --token aws <command>`; it persists to `.sg_vault/token` after first use |
| **Write key** | **Handed to you out of band. It is not in this pack and must never enter the site repository** |
| Read key | `sgit_private_read_d5220d6ada858319cf31f4a4e1a3bd04fe97d647285c16c869adef651db5208d` |
| Read URL | `https://dev.vault.sgraph.ai/en-gb/#<read-key>:dkeclt5r` |
| Commits | 4, including init |
| Release | `@pack-v0.33.67`, pinning `obj-cas-imm-87e6f3cf0b56` |
| sgit build used | `sgit-ai` v0.16.0 from PyPI (`pip3 install sgit-ai --break-system-packages`) |

**You continue this vault.** Same key, same history. The history is part of the argument: it shows the specification was published before the implementation, which is acceptance test 13 and the only one currently passing.

### What is in it

```
  _page.json                    root page layout, renders on open
  README.md                     markdown fallback index
  .vault/app.json               chrome config, entry, permissions: []
  .vault/releases.json          release channel, sg-releases/v1
  pack/README.md                the pack hub
  pack/00__README.md            the argument, scope, what not to rebuild
  pack/01__what-exists.md       assembly inventory, both sides
  pack/02__the-model.md         THE ONTOLOGY. Nodes, edges, two hashes, provenance
  pack/03__the-worked-example.md  THE DELIVERABLE. Seven steps, Santa Barbara, CPRA
  pack/04__the-vault.md         team, viewers, graph settings, releases, corrections
  pack/05__the-workbench.md     pipeline, artefacts, browser database, seven computations
  pack/06__verification.md      13 acceptance tests, 5 blockers, what would make it wrong
  team/README.md                the four roles and the single-writer rule
  team/cartographer.md          lead role. Graph and viewer
  team/librarian.md             provenance, attribution, catalogue
  team/architect.md             schema and model
  team/reviewer.md              commissioned to contradict
  provenance/retrieval-log.md   every fetch, INCLUDING THE FAILURES
  catalogue/entry.json          catalogue submission, read key, commit ids
  corrections/README.md         ships empty, on purpose
  review/README.md              ships empty
```

**Read `pack/02__the-model.md` and `pack/03__the-worked-example.md` properly before you write code.** They are not background; they are the specification you are implementing, and they were written to be read first.

## What The Previous Session Refused To Do, And Why It Matters To You

**It did not fetch any UnGovr data.** The container's proxy answered 403 to CONNECT on `data.ungovr.org:443` — the open endpoints, not only the authenticated ones. That is recorded in `provenance/retrieval-log.md` with the proxy's own log line, and as blocker B1 in `pack/06__verification.md`.

**A summarising fetch path was available and was declined.** A tool could reach the host but returned model-summarised text rather than raw bytes. A node retrieved that way cannot carry a `response_sha256`, because there are no source bytes to hash.

**This matters to you for three reasons.**

**One: it is the precedent you inherit.** If your own container turns out to have the same limit, take the same decision, and record it the same way. **The refusal is logged as an entry rather than left as an absence**, so a reader can see that a shortcut existed and was declined.

**Two: the sibling site has the same scar.** The ElevenLabs provider site's ledger opens with "almost everything written about this API here was written by a machine that could not reach the API", and every one of its examples is badged `unrun`. **The family already knows this failure mode and has a state for it.** You do not need to invent one.

**Three: if your egress works, you close five blockers in an afternoon**, and that is the single most valuable thing in this pack.

## Blockers Recorded In The Vault, And Who Closes Them

| # | Blocker | Closes when |
|---|---|---|
| **B1** | Egress refuses `data.ungovr.org` | **You confirm your container can reach it.** Gates six acceptance tests |
| **B2** | The two key-gated corpora are unread: `/ai-laws/*` and `/cgj/reports/{id}.json` | A working `X-API-Key` reaches them. **Ask the project lead whether the issued key is available to you** |
| **B3** | The CPRA's machine-readable source format is unknown | You establish whether Akoma Ntoso or comparable XML exists. **Resolve before writing a parser** |
| **B4** | The Santa Barbara County slug is not known | Resolved from `/v1/entities/us/ca.json`. **Deliberately not guessed** |
| **B5** | Upstream: no collection roots, so a pinned release could be garbage-collected later | Not yours. Recorded so a reader relying on a pinned link knows the dependency exists |

## Two Corrections Already Filed

Recorded beside the source rather than as edits to it, per the house rule that a correction is a proposal recorded beside the thing.

| # | Against | Correction |
|---|---|---|
| C1 | The original dev brief's acceptance-test table | Two rows are numbered `10`. Both tests are distinct and kept; renumbered to 13 in the vault |
| C2 | The original research brief's egress finding | It records the *authenticated* host being refused. **The open host is refused too** |

**Keep filing them the same way.** If this pack is wrong about the house pattern — and §5 of `02__the-house-pattern.md` lists exactly where it is most likely to be — the correction goes beside it.

## The Site Repository

| | |
|---|---|
| Repository | `github.com/SGit-AI/SGit-AI__Website__Provider__UnGovr` |
| Description | "repo for ungovr.providers.sgit.ai" |
| Contents | `.gitignore`, `LICENSE`, `README.md`. **One commit** |
| Branch observed | `dev`. **The sibling repo links its own files under `main`.** Confirm which is the default and which CI deploys from before your first push |
| Target host | `ungovr.providers.sgit.ai` — **answers 404 today, measured 9 September 2026.** Not pointed yet |
| Parent hub | `providers.sgit.ai` — live |
| Sibling | `elevenlabs.providers.sgit.ai` — live, v0.3.0, and **the template you copy** |

> **One naming inconsistency, unresolved, worth one question rather than a guess.** The sibling repository's description says `elevenlabs.provider.sgit.ai` (singular) while its own `CNAME` file and every canonical URL on the site say `elevenlabs.providers.sgit.ai` (plural). The UnGovr repository's description says `ungovr.providers.sgit.ai` (plural). **Plural is what serves.** Write `ungovr.providers.sgit.ai` in `CNAME` and every canonical, and do not copy the description's spelling.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

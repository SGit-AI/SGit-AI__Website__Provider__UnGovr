# 04 — Deliverable Two: ungovr.providers.sgit.ai

**version** v0.33.68
**date** 9 September 2026
**target** `github.com/SGit-AI/SGit-AI__Website__Provider__UnGovr` → GitHub Pages → `ungovr.providers.sgit.ai`

[← 03 Vault MVP](03__vault-mvp.md) · Next → [05 Verification](05__verification.md)

---

## 1 · Read This Before You Write A Line Of Site Content

**The family defines "provider" narrowly, and UnGovr does not fit the definition.**

The sibling site says so in its own words:

> "**'Provider' here means one thing only: a service that serves models over an API** — the sense this estate's own code uses, where a constant of that name holds an entry per model service."

**UnGovr serves data, not models.** They are a nonpartisan nonprofit publishing a public good under CC BY 4.0. If you write the nine sections as though they were a model vendor, you will produce nine sections that answer the wrong questions well.

### The resolution, and it makes the site better rather than weaker

**The family's actual question is not "which model service is this". It is: *where does the credential live, and what bounds it*.** UnGovr answers that question — and answers it in a way no model provider in the family can.

| Section | A model provider's answer | **UnGovr's answer** |
|---|---|---|
| 3 · Which pattern | Pattern 0 is a mistake; pattern 3 is the goal | **Most of this API needs no credential at all.** Pattern 0 is not a hazard here, it is the intended mode. **That is a genuinely new row in the comparison matrix** |
| 5 · The bounding primitive | A key scope, or a plan quota | **A rate limit per IP, and then HTTP 402 with a payment challenge.** The bound is a *payment protocol*, not a property of a key |
| 8 · What it cost | Dollars on a named workload | **Nothing, inside 100 requests a day.** Then $0.001 per entity request, $0.01 per report, $5 minimum wallet, Stripe |

**So: UnGovr is the family's first open-data provider, and the extension is deliberate, stated, and argued.** Say it on the page, in §1 or immediately after it. Do not quietly widen the word and hope nobody notices.

**And file it as a correction against the hub's contract** — beside it, not as an edit. The contract's own closing rule applies: *"If adding the second provider requires template surgery, the contract is wrong and the fix belongs in the contract rather than in the page."* The same logic covers a definition that a legitimate new member does not fit.

> **One thing this site is emphatically not.** UnGovr have shipped a machine-payments flow and an MCP server that this estate has only researched, and they have a firsthand measurement — 40.7 per cent of addresses written "Santa Barbara, CA" fall outside the city limits — of exactly the kind this estate holds itself to. **The site reports on an API and admires the work.** A page that reads as a nonprofit being audited by a stranger has failed.

## 2 · The Nine Sections, Answered For UnGovr

**All nine at v0.1.0.** Several honestly thin. **A section answered `spec` is fine; a section filled with something plausible because the section exists is the failure.**

| # | Section | What goes in it | Likely state |
|---|---|---|---|
| 1 | **Disclosure** | **None.** No relationship, no funding, no agreement, with the date checked. **Ships before there is anything to disclose**, so its existence is not evidence of one. Add: no conversation with UnGovr has happened, so **every statement about what they need is inference from what they publish** | `verified` |
| 2 | **What it grants** | Capability tuples for a data API: `read × entity × world`, `read × boundary × world`, `read × records-law × world`, `read × grand-jury-report × tenant` (key-gated), `spend × wallet × tenant` (the 402 path). **Reversibility marked; nothing here writes**, which is itself the interesting row | `docs` mostly, `verified` where you called it |
| 3 | **Which pattern, per product** | **Per product, never per vendor.** Open entity/law/CGJ-index endpoints: no credential, so the pattern question dissolves. Key-gated AI-laws and CGJ detail: pattern 0 with a real bound, pattern 1 unknown, pattern 2 unknown, pattern 3 `spec`. **The `patterns:` front-matter block is what the hub syncs — get it right** | mixed |
| 4 | **Where the key goes** | `X-API-Key` header. **Quote the product, the URL, the date read.** And where it goes in our estate: owner-sealed under the vault's write key, never in the repository | `docs` |
| 5 | **The bounding primitive** | Rate limit per IP for entity data, per key for report detail. **Then 402 with a payment challenge.** And what it does *not* cap: nothing stops a key burning a wallet; the MCP server signals the same condition as JSON-RPC `-32042` | `docs`, `verified` if you hit a limit |
| 6 | **Minimal working example** | **As files, not snippets.** The nine retrievals from `03__vault-mvp.md` as runnable scripts, each with the invocation beside it | `verified` if run, else `unrun` |
| 7 | **What we use it for** | **The government graph vault.** One county, one law, one acceptance — the named workload, with the vault linked | `verified` |
| 8 | **What it cost** | **Nothing, inside the free tier.** State the request count, the date, the limits, and the price above them. **This section stales fastest** | `measured` |
| 9 | **What went wrong** | **See below. This section is the strongest thing this site will have** | mixed |

### §9, which is the section nobody else writes

**Do not soften these, and do not present them as failings.** Each is a specific, dated, checkable observation, and several are things they would want to know.

| Finding | Note |
|---|---|
| **The law edge stops short** | An entity carries `open_records.law` and nothing addressable below it. **The core finding, and it is one hop, not a chasm** |
| **The AI-law endpoints return a verdict, not provisions** | A verdict is a summary judgement. **A reader can neither check it nor disagree at the level where disagreement is useful** |
| **The entity count disagrees with itself** | 330,000, 321,000 and 320,000 on three pages. Ordinary for a live dataset. **Report it as an observation, not a gotcha** — and the research brief's own instruction is that pointing at it is not the conversation |
| **The cross-references are described and not exposed** | GeoNames, Wikidata, OCD and FIPS are on the platform page and absent from `/meta/schema.json`. **If exposed, joining their entities to anything else becomes free.** The cheapest possible improvement to their surface |
| **No public repository, so no corrections path** | No clone, no fork, no pull request. **Their own argument makes this awkward**, because they object to reaching your government becoming a rental metered by whoever owns the index, and an API on one domain is a single point of dependency however good the licence |
| **Half the Atlas is one country** | 159,926 of ~320,000 are United States. **Their own explanation is honest and structural** and should be quoted, not paraphrased |
| **Egress** | If your container was refused, that is a §9 finding about *our* environment, not theirs. **Say which** |

## 3 · Where The Vault Goes On The Site

**The vault is the centrepiece of §7 and it is what makes this site different from a page about an API.**

**Two surfaces, and the CI gate decides which is primary.**

**Primary — a static rendering built into the site.** At build time, copy the vault's compiled artefacts into `data/`, and render the graph and computation 1 **as part of the site itself**. Self-contained, no external fetch, passes the no-third-party rule, works with JavaScript disabled for the tables. **This is the one that must exist.**

**Secondary — a link to the live vault by read key.** A prominent card: *open the vault itself, read-only, in the SG/Send browser.* It carries the read key in the URL fragment.

> **Three constraints on the live link, and one of them is a question for the project lead.**
>
> **The read key is publishable; the write key never is.** The CI key-shape scan runs over the whole tree including `docs/`. Put only the read key in the repository.
>
> **Do not iframe it.** *"No third-party anything"* is a build rule. An embedded frame pulling a different host into the page is exactly what that rule exists to prevent, and it would also break the site with JavaScript off. **Link, do not embed.**
>
> **The vault currently lives on `dev.send.sgraph.ai`, and its browse URL is on `dev.vault.sgraph.ai`.** Publishing a `dev.*` link from a public site is a decision, not a detail. **Ask before shipping it**, and if the answer is to move the vault to production first, that is a step in `03__vault-mvp.md`, not a site change.

## 4 · The Repository, Concretely

**The repository exists with three files and one commit.** Do not create it; fill it.

**Confirm the default branch before your first push.** The repository was observed with one commit on `dev`; the sibling links its own files under `main`. **Whichever CI deploys from is the answer**, and guessing wastes a release.

**Copy the sibling's skeleton rather than writing one.** `build.py`, `assets/site.css`, `assets/site.js`, the workflow, the gate scripts and the templates are the same files across the family, by design.

```
  .github/workflows/     validate → tag → deploy
  admin/build/version.txt   v0.1.0
  assets/                site.css, site.js, favicon.svg  ← copied, not written
  bin/                   gate scripts
  briefs/                THIS PACK, published raw
  content/               the markdown sources
  data/                  the vault's compiled artefacts, copied at build time
  docs/                  built output. GitHub Pages serves this. COMMITTED
  files/                 the example scripts from §6, downloadable
  CNAME                  ungovr.providers.sgit.ai
  HANDBACK.md            what a human with a key must check
  build.py               copied
  README.md  LICENSE  .gitignore
```

**`briefs/` is not optional.** The sibling publishes every brief it was built from, raw, with a decision-by-decision account of what was accepted, modified and rejected. **This pack goes there**, and so does the vault's own `/pack/`. A site arguing for published provenance that hides its own inputs has refuted itself.

## 5 · The Two Claim Vocabularies, And The Crosswalk

**Do not merge them.** They answer different questions.

| | The vault's states | The site's states |
|---|---|---|
| Answers | *How well is this subject's compliance observed?* | *How well does this site know what it says?* |
| Values | `unevidenced`, `asserted`, `documented`, `manually-checked`, `programmatic-out-of-band`, `programmatic-inline` | `verified`, `measured`, `docs`, `spec`, `unrun`, `projected` |
| Default | `unevidenced` | Nothing ships without one |

**The crosswalk, for site claims *about the vault*:**

| Site claim | State |
|---|---|
| We fetched this endpoint and hashed the bytes on this date | `verified` |
| Coverage of the law edge is N per cent on their bulk snapshot | `measured` |
| The rate limit is 100/day per IP | `docs` — read on their page, unless you hit it |
| The graph viewer will do the full fractal zoom | `spec` |
| The example scripts | `verified` if run, `unrun` otherwise |
| Cost above the free tier for a workload of size X | `projected`, workings shown |

**And one rule that spans both**: a vault node's evidence tier is *never* rendered as a site claim state, or a reader will think "unevidenced" means the site does not know. It means the county has not been observed.

## 6 · The Release, And The Domain

**v0.1.0.** `admin/build/version.txt` owns it; the release commit's subject repeats it; **CI refuses to tag if the two disagree.** Validate → tag → deploy, in that order.

**`ungovr.providers.sgit.ai` answers 404 today**, measured 9 September 2026. **Ship anyway.** The canonical says the intended host; internal links stay relative so the site serves correctly under the GitHub Pages project path; the page says which host it is measured to be serving on. **The sibling shipped in exactly this state and documented it**, and the hub's `bin/sync-providers.py` picks the site up automatically once the domain answers.

**Then**: a `patterns:` block in the report's front-matter, and a row in the hub's `data/providers.yml` **added by running `bin/sync-providers.py`, not typed.**

## 7 · What This Site Must Not Do

| Not this | Because |
|---|---|
| Read as an audit of a nonprofit | They publish a public good under CC BY 4.0 and they work from the outside, which is this estate's own position in their words |
| Lead with the gap | **Lead with what the Atlas is**, then the one edge, then what was built on it |
| Pitch encryption for the Atlas | **Openness is the product.** The vault story is for private instances that reference it, never for the library |
| Claim the semantic layer is shipped | The method site says of itself that it is designed rather than shipped |
| Describe them as AI governance | They are civic infrastructure and the confusion is easy to make |
| Present the entity-count discrepancy as a finding | Ordinary for a live dataset. An observation, not a conversation |
| Assert what they want | No conversation has happened. **Everything about their intentions is inference from published pages** |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

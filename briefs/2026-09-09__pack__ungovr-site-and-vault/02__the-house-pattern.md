# 02 — The House Pattern: Stack, Workflow, Styles, Contract

**version** v0.33.68
**date** 9 September 2026

[← 01 What Is Already Built](01__what-is-already-built.md) · Next → [03 Vault MVP](03__vault-mvp.md)

---

## How This File Was Produced, And What That Means For You

**Everything below was read on 9 September 2026 from the live sites and their published markdown twins**, not recalled and not read from the repositories. The session that wrote this pack could reach `providers.sgit.ai`, `elevenlabs.providers.sgit.ai`, `graphs.sgit.ai` and `standards.sgit.ai` over HTTPS, and **could not read the GitHub repositories** — the API refused with 403 and clone required credentials it did not have.

**So this file is accurate about what the sites publish and inferential about how they are built.** Where it describes `build.py`, the workflow file, or a check, that is derived from the sites' own prose about themselves and from the shape of the output.

> **Your first act on the site deliverable is to read the sibling repository directly** and correct anything below. **File the correction beside this file rather than editing it**, per the house rule. `01__what-is-already-built.md` records two such corrections already.

## 1 · The Stack

| | |
|---|---|
| Build | **`build.py`**, Python 3.11+, **no external dependencies** |
| Source | **Markdown with YAML front-matter**, in `content/` |
| Output | Static HTML in **`docs/`**, served by **GitHub Pages from that directory** |
| Version | **`admin/build/version.txt`** owns it. One file, everywhere else derived |
| Release | **validate → tag → deploy**, in that order, a failure at any stage stopping the release |
| JS | One file, `assets/site.js`, **436 bytes**, and its entire job is a nav toggle |
| CSS | One file, `assets/site.css`, ~22 KB, hand-written |
| Third party | **None. No CDN, no web fonts, no analytics, no cookies** |
| Licence split | Content **CC BY 4.0**; build code (`build.py`, `assets/`, `apps/`, `tools/`) **Apache-2.0** |

### The repository layout, as the sibling has it

```
  .github/workflows/     the validate → tag → deploy pipeline
  admin/build/           version.txt and build configuration
  apps/                  browser labs, if the site has any
  assets/                site.css, site.js, favicon.svg
  bin/                   scripts. The hub's own sync-providers.py lives here
  briefs/                every brief the site was built from, published raw
  content/               the markdown sources with front-matter
  data/                  structured inputs the build reads
  docs/                  THE BUILT OUTPUT. GitHub Pages serves this
  files/                 downloadable artefacts
  tools/                 development tooling
  .gitignore
  HANDBACK.md            what a human with access must check. Kept short
  LICENSE
  README.md
  build.py
```

**`docs/` is committed.** The build is reproducible and CI checks that the committed output matches the sources — a stale build publishes prose nobody wrote.

## 2 · What Every Page Emits

Verified by fetching them.

| Artefact | Path | Note |
|---|---|---|
| The page | `<path>/index.html` | |
| **Its markdown twin** | **`<path>/index.md`** | **At every path.** So an agent never has to parse HTML and never leaves the markdown surface |
| Alternate link | `<link rel="alternate" type="text/markdown" href="index.md">` | In every `<head>` |
| Canonical | `<link rel="canonical" href="https://<host>/<path>">` | On the CNAME host |
| Agent index | `/llms.txt` | Site version, description, claim-state note, licence, then a `## Pages` list with description per page |
| Whole site | `/llms-full.txt` | **167 KB on the sibling.** Every page's front-matter and body, `PAGE /path — title` banners between them |
| Sitemap | `/sitemap.xml` | Every canonical URL |
| Robots | `/robots.txt` | `Allow: /` plus the sitemap line |
| Domain | `/CNAME` | One line. `ungovr.providers.sgit.ai` |

## 3 · The Front-Matter Shape

From the sibling's `index.md`, read live:

```yaml
---
title: ElevenLabs — text to speech with character-level timestamps
description: "One sentence. Used in <meta>, og:description and llms.txt"
lead: "The opening paragraph, with **markdown emphasis** in it"
order: 1          # sort position within its section
toc: true
wide: false
provenance:
  commit: 7d1916aca5f3
  date: 7 September 2026
  note: "Where the prose came from"
platform_grants:  # verb × object class × reach, reversibility marked, per product
  - verb: send
    object: text
    reach: endpoint
    reversible: true
    product: Text to speech
    note: the words you send leave for the model
grants:           # what OUR scoped key grants, same tuple shape
  - verb: spend
    object: characters
    reach: tenant
    reversible: true
    bounded_by: the plan's monthly quota only — there is no per-key spend limit
not_granted: [voice cloning, dubbing, agents]
patterns:         # THE BLOCK THE HUB SYNCS. One entry per product
  - provider: ElevenLabs
    product: Text to speech (REST)
    server: "Yes — ours, until sg.tts ships"
    p0: { verdict: never, note: "CORS allows it; the account quota is the only bound" }
    p1: { verdict: no,    note: "no per-key spend limit exists" }
    p2: { verdict: yes,   note: "only with a server we run" }
    p3: { verdict: spec,  note: "sg.tts specified; terms file in the vault" }
---
```

**`provenance.commit` is the vault commit the prose came from.** The hub's own pages carry it and say plainly: *"When the vault moves ahead, this page is behind — and says so rather than guessing."* **Your site's provenance commit is the government-graph vault's commit**, which is a nice property: the site can name exactly which state of the vault it reports on.

**Verdict values seen in the wild**: `never`, `no`, `yes`, `spec`, `na`.

## 4 · Template Placeholders

The build substitutes these in markdown bodies. Observed in the published twins:

| Placeholder | Renders |
|---|---|
| `{{badge:verified}}` `{{badge:measured}}` `{{badge:docs}}` `{{badge:spec}}` `{{badge:unrun}}` `{{badge:projected}}` | A claim-state chip, linking to `/ledger/` |
| `{{claim:some-id}}` | A citation chip joined to the ledger **at build time** |
| `{{ledger}}` | The full claim table |
| `{{evidence}}` | The six-state table, or the family roll-up |
| `{{grants}}` | The capability tuples from front-matter, as a table |
| `{{examples}}` | The example-file list |
| `{{family}}` | The list of sites in the family |

**The join is the enforcement.** *"A claim that appears on a page and not in that site's ledger fails the build."*

## 5 · The Six Claim States

**Verbatim from `providers.sgit.ai/evidence/`. Do not invent a seventh.**

| Chip | Means | What a reader may do with it |
|---|---|---|
| `verified` | Somebody ran it and watched it work, on that date, in a named place | Treat as fact for that date and that setup |
| `measured` | Our own pipeline produced this number on a named workload | Treat as fact about *our* workload; yours will differ |
| `docs` | Read in the vendor's documentation on that date; never executed by us | Check it against the vendor before relying on it |
| `spec` | A written specification for something that does not exist | **Never plan around it. Future tense only** |
| `unrun` | Code we wrote and have never executed | Read it, then run it and find out. Expect it to be wrong somewhere |
| `projected` | Arithmetic, with its workings shown | Re-do the arithmetic with your own numbers |

**And the reading discipline the family states about its own states**: read `docs` as the honest debt, `unrun` as the invitation, and **read `verified` narrowly** — it means somebody watched it work once, in one place, on one account tier.

> **Note the mapping you will need.** The vault uses the conformance ladder — `unevidenced`, `asserted`, `documented`, `manually-checked`, `programmatic-out-of-band`, `programmatic-inline`. **The site uses these six.** They are different vocabularies for different jobs and **must not be merged**: the vault's states describe how well a *subject's compliance* is observed, the site's describe how well *this site knows what it says*. `04__the-site.md` §5 gives the crosswalk.

## 6 · The Nine Sections, Fixed

**From `providers.sgit.ai/contract/`. Not added to, not reordered, not merged.**

| # | Section | For |
|---|---|---|
| 1 | **Disclosure** | One line: commercial relationship, or none, with the date checked |
| 2 | **What it grants** | Capability tuples — verb × object class × reach, reversibility marked — in two layers: what the platform grants per product, and what *your* scoped key grants |
| 3 | **Which pattern** | Which of the four the provider supports and which it forbids, **per product** |
| 4 | **Where the key goes** | The exact mechanism, quoted with the product it belongs to, the URL and the date read |
| 5 | **The bounding primitive** | What caps the blast radius — and what it does **not** cap |
| 6 | **The minimal working example** | The smallest thing that runs, **as a file rather than a snippet** |
| 7 | **What we use it for** | Named workloads, so the page is a report rather than a tutorial |
| 8 | **What it cost** | Date, workload size, model, request count, price |
| 9 | **What went wrong** | The failures, the limits hit, the surprises. **The section nobody else writes** |

**Sections 8 and 9 get the visual weight.** *"If a reader takes one screenshot from a provider site, it should be §9."*

**And the rule that has already caught somebody**: credential rules are stated **per product, never per vendor**, and every quote carries the product, the URL and the date it was read.

### The four credential patterns

| | |
|---|---|
| **Pattern 0** | Key in the page |
| **Pattern 1** | Bounded key in the page |
| **Pattern 2** | Short-lived token, from a minter |
| **Pattern 3** | **The host holds the key** and enforces the terms. The app never sees it |

## 7 · Build Failures, Not Review Comments

**Each is enforced by a check.** Copy the list; it is the gate.

| Check | Why it exists |
|---|---|
| **The build is reproducible** — committed output matches sources | Markdown is the source of truth; a stale build publishes prose nobody wrote |
| **Version agreement** across every page badge, the release history and both machine indexes | A blanket bump that misses a page ships two versions of one site |
| **Internal links resolve**, and every canonical is on the host in `CNAME` | The two ways a static site quietly breaks |
| **No root-absolute internal URL** | The first site shipped one and served unstyled under a project path for a day |
| **No bare `<https://…>` autolink** | It reaches the browser as an unknown tag and the URL vanishes |
| **A key-shape scan over the whole tree, including `docs/`** | **These repositories are public; the vaults they came from were not** |
| **Every claim cited, every state dated** | The contract, enforced instead of promised |
| **The disclosure line present on every page** | A disclosure found at the bottom does the opposite of its job |

> **The key-shape scan is the one that will bite you.** You will be holding a vault **write** key. It must never enter this repository — not in a brief, not in a comment, not in a test fixture, not in `docs/`. **The read key is publishable and is the one the site uses.**

## 8 · The Styles

**Copy `assets/site.css` from the sibling rather than writing one.** The tokens, read from the live file:

```css
--bg:#faf9f5        --panel:#ffffff     --panel2:#f2f0e9
--line:#e5e1d5      --line2:#d5d0c2
--fg:#1c1d21        --dim:#5c5f66       --dim2:#8a8d94      --ink:#34363c
--accent:#0f766e    --accent-dk:#115e59
--yellow:#a16207    --warm:#b45309      --green:#15803d
--blue:#0369a1      --red:#b91c1c
--term-bg:#0d1117   --term-green:#3fb950  --term-red:#f85149
--term-cyan:#58a6ff --term-yellow:#d29922 --term-dim:#8b949e
--sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif
--serif:ui-serif,Georgia,"Times New Roman",serif
--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,"Liberation Mono",monospace
--measure:960px     --wide:1360px
--shadow:0 1px 2px rgba(28,29,33,.05),0 4px 14px rgba(28,29,33,.04)
```

**Warm off-white ground, teal accent, system font stacks only.** No web fonts — that is a CI rule, not a preference.

### The nav, which is the house signature

Structure read from the sibling's rendered HTML:

```html
<nav class="site"><div class="row">
  <a class="brand" href="index.html">ungovr<span>.providers.sgit.ai</span></a>
  <a class="parent" href="https://sgit.ai/…" rel="noopener" title="…">&#8599; part of <b>sgit.ai</b></a>
  <span class="stage-pill">provider report</span>
  <a class="ver" href="versions/index.html" title="Site release history">v0.1.0</a>
  <button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>
  <div class="nav-items">
    <div class="ni"><a class="nl here" href="index.html">The report</a></div>
    <div class="ni ni-has"><a class="nl" href="…">Section<span class="caret">&#9662;</span></a>
      <div class="sub"><a class="sl" href="…">Sub-page</a></div></div>
  </div>
</div></nav>
```

**The brand splits**: bare name in the anchor, the domain suffix in a `<span>`. **The parent link is `↗ part of sgit.ai` and points at a page, never at a domain** — a domain link is a referral rather than a composition, and the family records that as its one defect.

Other observed classes worth reusing rather than reinventing: `.note` for the how-to-read-this callout, `.fails > .fail.open` for the open-items list on the ledger page.

## 9 · Composition Rules

- **A cross-link points at the page that answers the question**, never at a domain.
- **Every page is served as markdown at the same path.**
- **Machine-readable where it is cheap**: `llms.txt`, `llms-full.txt`, and a claim index the hub syncs.
- **The canonical URL is the intent, the link is the reality.** A link goes wherever that site is *measured* to be serving — the canonical host once it answers, the project path before it does — **and the page says which.** The hub's `bin/sync-providers.py` fetches each site's published index from its canonical host and a build check fails if a link disagrees.

> **This rule applies to you immediately.** `ungovr.providers.sgit.ai` **answers 404 today.** Until it points, cross-links to your site resolve to the GitHub Pages project path, and your own canonical says the intended host. The sibling shipped in exactly this state and documented it; **do the same rather than waiting for DNS.**

## 10 · Joining The Family

From `providers.sgit.ai/sites/`, three steps and no template surgery:

1. **A repository, from the same template** — the build system, the gate and the release pipeline are the same files.
2. **A `patterns:` block** in the report's front-matter, per product. **That is what the hub syncs.**
3. **A row in `data/providers.yml`**, added by running `bin/sync-providers.py` **rather than typed.**

**No edit to the comparison page.** *"If adding the second provider requires either, the contract is wrong and the fix belongs in the contract rather than in the page."*

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

---
title: UnGovr — the open-data provider, and the one edge that stops short
description: "An independent report on the UnGovr Open Data API: 327,138 government entities, 398 open-records laws, free under CC BY 4.0 — and a join between them that is one derivable hop away."
lead: "UnGovr publish an Atlas of **327,138 government entities** and a corpus of **398 open-records laws**, free, under CC BY 4.0, with no credential needed for most of it. This is a report on that API, written to the nine sections of the [providers contract](https://providers.sgit.ai/contract/). It is the family's **first open-data provider**, and admitting one required arguing with the family's own definition of the word — [§3](#3-which-pattern-per-product) does that. The finding it exists to report is in [§9](#9-what-went-wrong), and it is one edge long."
order: 1
toc: true
provenance:
  vault: dkeclt5r
  date: 9 September 2026
  note: "The retrievals, the two computations and the seven-step join were produced in this session against the live API."
platform_grants:
  - verb: read
    object: entity
    reach: world
    reversible: true
    product: Open Data API — entities
    note: 327,138 entities across 205 countries. **No credential at all**
  - verb: read
    object: boundary
    reach: world
    reversible: true
    product: Open Data API — boundaries
    note: 161,603 GeoJSON boundaries, one per entity that has one
  - verb: read
    object: records-law
    reach: world
    reversible: true
    product: Open Data API — laws
    note: 398 open-records laws, 254 of them sub-national
  - verb: read
    object: grand-jury-report
    reach: tenant
    reversible: true
    product: Open Data API — CGJ report detail
    note: key-gated, 50/day per key. The indices are ungated and unlimited
  - verb: read
    object: ai-law-verdict
    reach: tenant
    reversible: true
    product: Open Data API — AI and crawling law
    note: key-gated, and **read** — 2,915 instruments. Its own licence, not CC BY 4.0
  - verb: spend
    object: wallet
    reach: tenant
    reversible: false
    product: Machine Payments Protocol
    note: the 402 path. **The only irreversible verb on the whole surface**
grants:
  - verb: read
    object: entity
    reach: world
    reversible: true
    bounded_by: 100 requests a day per **IP address** — there is no key to scope, because we hold none
  - verb: read
    object: records-law
    reach: world
    reversible: true
    bounded_by: the same IP budget. Nothing here writes, and nothing here spends
not_granted: [write, delete, spend, ai-laws, grand jury report detail]
patterns:
  - provider: UnGovr
    product: Open Data API — entities, boundaries, laws, CGJ indices
    server: "No — there is no credential to hold"
    p0:
      verdict: na
      note: "no credential exists for this surface, so the question dissolves"
    p1:
      verdict: na
      note: "the bound is per IP, not per key"
    p2:
      verdict: na
      note: "nothing to mint a token for"
    p3:
      verdict: na
      note: "nothing for a host to hold"
  - provider: UnGovr
    product: Open Data API — AI-laws and CGJ report detail (key-gated)
    server: "Yes for pattern 3 — but the key is free and read-only"
    p0:
      verdict: yes
      note: "a free, read-only key with a per-key daily cap. The first yes here that is not a warning"
    p1:
      verdict: spec
      note: "no per-key scoping is documented; the daily cap is the only bound"
    p2:
      verdict: no
      note: "no token minter is offered"
    p3:
      verdict: spec
      note: "possible, and unnecessary at this risk level"
  - provider: UnGovr
    product: Machine Payments Protocol (the 402 path)
    server: "Yes — a funded wallet must never reach a browser"
    p0:
      verdict: never
      note: "a wallet credential in a page is spendable by anyone who reads it"
    p1:
      verdict: spec
      note: "a per-request price exists; a per-key spend cap is not documented"
    p2:
      verdict: spec
      note: "the natural shape for this, and not offered today"
    p3:
      verdict: spec
      note: "what we would build before spending a cent from a browser"
---

<div class="tiles">
<div class="tile tile-big"><b>0 of 49</b><span>sampled entities carrying <code>open_records.law</code></span></div>
<div class="tile"><b>96.6%</b><span>reachable if the edge is <em>inferred</em></span></div>
<div class="tile"><b>$0.00</b><span>what this whole report cost</span></div>
<div class="tile"><b>2 of 2</b><span>gated corpora now read &mdash; blocker B2 closed</span></div>
</div>

**Read the first number with the second.** A missing law reference is not an error. It is an entity whose records law has not been mapped yet, and for much of the world it may not exist in a mappable form. The number measures how far the join can currently reach. It is **not a defect count**. {{claim:coverage-zero}}

## What the Atlas is, before anything else

UnGovr are a nonpartisan nonprofit. They publish the Atlas — every government entity they can identify, from national governments down to a reclamation district in Sutter County — with boundaries, hierarchy, websites and domains, and they publish it **free, under CC BY 4.0, mostly without asking for a credential**. {{claim:licence-ccby}} Alongside it they publish a corpus of 398 open-records laws, and **254 of those are sub-national**: not just "the United States has FOIA" but California, Idaho, Chaco, Baja California Sur. {{claim:cpra-in-corpus}}

That corpus is better than this report expected to find. The California record is not a citation and a link — it carries `initial_response_days: 10`, `extension_days: 14`, `private_right_of_action: true`, per-page copy rates, submission methods, and a structured list of what a valid request must contain. Somebody read the statute and modelled it.

**Their stated purpose is helping a person reach their government**, and for that purpose the data is shaped exactly right. This report is about what happens when you want to do the next thing with it.

## 1 · Disclosure

**None.** No commercial relationship with UnGovr — no funding, no agreement, no credits, no programme. **No conversation of any kind has taken place**, which matters more than the absence of money: every statement on this site about what UnGovr intend, need, or would want is *inference from what they publish*, and is marked as such. {{claim:no-conversation}}

This page ships before there is anything to disclose, so that its existence is never evidence that something appeared later.

UnGovr's data is used here under **CC BY 4.0**, which is the licence they chose. This report is published under the same one.

## 2 · What it grants

Capability tuples — verb × object class × reach, reversibility marked — in two layers: what the platform can grant per product, and what *our* access actually reaches.

**The interesting row is the one that is missing.** Across the entire open surface there is no `write`, no `delete`, and no `spend`. Every verb is `read` and every one is reversible. The single irreversible verb on the platform is `spend × wallet`, and it lives behind the 402 path that we never touched.

{{grants}}

## 3 · Which pattern, per product

**First, the definitional problem, because it changes the answers.** This family defines *provider* narrowly — the sibling site states it plainly:

<blockquote class="vendor">
<p>&ldquo;Provider&rdquo; here means one thing only: a service that serves models over an API — the sense this estate's own code uses, where a constant of that name holds an entry per model service.</p>
<cite><a href="https://elevenlabs.providers.sgit.ai/#what-this-site-is-and-is-not" rel="noopener">elevenlabs.providers.sgit.ai &sect; What this site is, and is not</a>, read 9 September 2026</cite>
</blockquote>

**UnGovr serve data, not models.** By that definition they do not belong here. Written as though they were a model vendor, the nine sections would answer the wrong questions well.

**The resolution, and it makes the contract better rather than weaker.** The family's real question was never *which model service is this*. It is: **where does the credential live, and what bounds it?** UnGovr answer that question — and answer it in a way no model provider in this family can, because for most of their surface **the answer is that there is no credential**. Pattern 0 is not a hazard here; it is the intended mode, and it is the first row in this matrix where `pattern 0` is not a warning. {{claim:api-key-free}}

**So UnGovr is this family's first open-data provider, and the extension is deliberate.** It is [filed as a correction against the hub's contract](/briefs/) rather than as an edit to it, per the house rule — and per the contract's own closing rule, that if admitting a legitimate new member requires template surgery, the fix belongs in the contract.

{{comparison}}

**Note the three products are bounded by three different things**, which is exactly why this section is per product and never per vendor: the open surface by an IP budget, the gated surface by a free key's daily cap, and the payment path by a wallet balance.

## 4 · Where the key goes

**For most of this API: nowhere. There is no key.** That is the honest answer for entities, boundaries, records laws and the CGJ indices, and it is the reason this provider is worth adding to the comparison.

For the two gated corpora — AI-laws, and CGJ report *detail* — the API advertises **two different mechanisms in the same 401 response**: {{claim:ai-laws-gated}}

```
HTTP/2 401
www-authenticate: Bearer resource_metadata="https://data.ungovr.org/.well-known/oauth-protected-resource", scope="opendata:read"

{"error":"API key required. Include X-API-Key header.",
 "register":"https://www.ungovr.org/open-data/api-keys"}
```

The body says `X-API-Key`. The header offers OAuth 2.0 Protected Resource Metadata — the discovery document an MCP client follows. **Product: Open Data API, AI-laws endpoints. Read at `https://data.ungovr.org/v1/ai-laws/index.json` on 9 September 2026.**

**Only one of the two works, and we have now run both.** The same valid key returns `200` as `X-API-Key` and `401` as `Authorization: Bearer` — byte-identical to the anonymous refusal. {{claim:authorization-ignored}} Their key page says so plainly: *"The Open Data API does not read `Authorization`, so a bearer token is ignored and the request is answered as an anonymous one."* The 401's own header does not say so, and a client that trusts the header over the docs fails open into anonymity.

<blockquote class="vendor">
<p>The Open Data API does not read <code>Authorization</code>, so a bearer token is ignored and the request is answered as an anonymous one.</p>
<cite><a href="https://www.ungovr.org/open-data/api-keys" rel="noopener">ungovr.org/open-data/api-keys</a> &mdash; product: Open Data API, API keys &mdash; read 9 September 2026</cite>
</blockquote>

**Where it goes in our estate**, if we ever hold one: owner-sealed under the vault's write key, never in this repository. The key-shape scan in `tools/secret-scan.sh` runs over the whole tree including the built output, and it deliberately does **not** match `sgit_private_read_…`, because a read key is publishable and is how this estate shares a vault — the same way `sgit.ai/llms.txt` does. [The vault page](/vault/) carries one.

## 5 · The bounding primitive

**What caps the blast radius here is not a property of a key. It is a property of the network path, and then a payment protocol.** {{claim:rate-limits}}

| Resource | Free tier | Bounded by |
|---|---|---|
| Entity data | **100/day per IP** | your IP address |
| CGJ indices and county listings | **unlimited** | nothing |
| CGJ report detail | 50/day per key | the key |
| Conditional revalidation (`304`) | free, 5,000/day per key | the key, then `429` + `Retry-After` |

Past the free tier the API answers **HTTP 402 with a Machine Payments Protocol challenge**, payable per request from a Stripe-funded wallet: $0.001 per entity request, $0.01 per report, $5.00 minimum top-up. {{claim:machine-payments}}

**And what it does not cap.** Nothing scopes a *wallet*. The rate limit protects UnGovr from a client; the wallet balance is the only thing protecting a client from itself, and a runaway agent with a funded wallet has no per-key spend ceiling documented anywhere. That is the same finding this family recorded against a model vendor's per-key quota, arrived at from the opposite direction.

**One practical gap.** `X-RateLimit-Remaining` and `X-Quota-Remaining` are advertised in the API's CORS `Access-Control-Expose-Headers`, but were not emitted on any of the 70 responses taken here — so a client cannot see how much budget is left until it is gone. {{claim:no-ratelimit-headers}}

**And one design choice worth knowing before you plan around it.** Several keys on one account **share a single daily allowance**: *"connecting a second client does not buy a second free tier."* {{claim:shared-quota}} So a key here is a **revocation handle, not a budget** — issuing one per machine limits what you have to rotate when one leaks, without raising throughput. That is the right trade, and it is the opposite of the assumption most per-key quota systems train you into.

## 6 · The minimal working example

**As files, not snippets** — and these are not illustrations. **They are the scripts that produced every number on this site.** {{claim:examples-run}}

{{examples}}

The discipline they encode: write the raw response bytes to disk unmodified, hash *those* bytes, and log before parsing anything. A node that cannot name the bytes it came from is an assertion, not a retrieval. [Every row of the log is published](/retrievals/), including the failures.

## 7 · What we use it for

**The government-graph vault** — one county, one law, one acceptance, and a refusal to widen it. {{claim:vault-viewer-mvp}}

The named workload is a seven-step join: **entity → instrument → provision → obligation → control → evidence → acceptance**, for Santa Barbara County and the California Public Records Act. [The whole join is on one page](/join/), with the provenance of every node and the state of every claim.

The one thing worth knowing before you read it: **only one edge crosses from their data into our model**, and UnGovr did not make that claim. It is drawn `inferred` everywhere it appears, because rendered as an assertion it would be a lie about the source.

**[The vault runs live on this site](/vault/)**, decrypted in your browser from a published read key — not a screenshot of one, and not a copy. It is the one page here that opens a network connection.

## 8 · What it cost

**Nothing. $0.00.** {{claim:requests-used}}

| | |
|---|---|
| Date | 9 September 2026 |
| Workload | 70 requests: 21 named retrievals + 49 entity-detail documents for the coverage sample |
| Free tier | 100 entity requests per day, per IP |
| Spent | **$0.00.** No 402 was ever returned |
| Above the tier | $0.001 per entity request, $0.01 per report, $5.00 minimum wallet |

**This section stales fastest**, and the honest version of it is the arithmetic rather than the invoice. A *census* of the law edge — one detail request per entity, because there is no bulk surface carrying it — is 327,138 requests: **about 9 years free, or $327.14 metered.** {{claim:census-cost}} That number is why [the measurement on this site is a sample](/coverage/) and says so.

## 9 · What went wrong

**The section nobody else writes.** None of these is a failing, and several are things we would want to know if the data were ours. They are dated, checkable observations, in descending order of how much they matter.

### The law edge stops one hop short

An entity carries no addressable path to the law that governs it. `open_records` **is** in the published schema, as an optional object with one string member — the join point is designed. {{claim:schema-declares-law}} It was present on **0 of 49** entities sampled, including six US states whose records laws are in UnGovr's own corpus, and including Santa Barbara County and California itself. {{claim:sb-detail-no-law}} **It is not a defect count** — it is the measurement of how far the join reaches today.

**And it is one derivable hop.** [Inferring it by slug prefix reaches 96.6%](/coverage/) of California's 16,071 entities, with a two-line rule, over data UnGovr already publish. {{claim:inferred-reach}} The reason it must be *inferred* and not merged is the other 20.5%: geography and jurisdiction come apart for interstate compacts, tribal nations, federal categories and specially-chartered districts — exactly the bodies a requester most often wants. {{claim:inferred-suspect}}

### The edge is not in any bulk surface, so nobody can measure it

`open_records` exists only in the per-entity detail document — one HTTP request each. Their own OpenAPI says the full-depth index is *"a compact record ({slug, name, type, parent_slug?, population?})"*. {{claim:law-not-in-bulk}} **The consequence is that the coverage of this field is not knowable to anyone on the open tier**, ourselves included, which is why the number above is a sample with an interval rather than a census with a total. Putting `open_records` into the bulk files would be the single cheapest improvement to this API's surface.

### Below the law, there is nothing addressable

The CPRA record cites `Gov. Code § 7922.535(a)` — which is exactly right, and confirms a section number the vault's own pack had only guessed at. {{claim:provision-confirmed}} But it is **prose inside a free-text field**. {{claim:provision-not-addressable}} There is no provision array, no clause identifier, no byte range. You can cite the Act; you cannot cite the clause, and so you cannot attach evidence to the clause. Everything downstream of a duty — a control, an observation, an acceptance — needs to hang on something smaller than a statute.

### The gated corpus is stronger than expected — and is not open data

The AI-law corpus was the highest-value unread thing in this project, and a key for it arrived while this report was being written. **It is much better than the brief predicted.** The brief expected a bare verdict — a summary judgement a reader could neither check nor usefully disagree with. What `ungovr.ai-laws/2` actually carries is **2,915 instruments across 271 jurisdictions**, each with a citation, a URL, a status and an effective date; a per-scenario `basis` naming the controlling authority — Van Buren, hiQ v LinkedIn, Ziff Davis v OpenAI; and a `provenance` block with `as_of_date`, `confidence` and `stale`. {{claim:ai-laws-is-instruments}} **It is checkable, and it is disagreeable-with at the level where that is useful.** The prediction was wrong and the correction is filed.

**But it is not CC BY 4.0, and nothing on the API's front door says so.** The OpenAPI document declares the whole Open Data API CC BY 4.0. The AI-law payloads carry their own `license` block — *"UnGovr Data License (non-exclusive, by agreement)"* — whose grant field reads **"No license is conveyed by receipt of this file."** {{claim:ai-laws-licence}}

The specific term governs, so **this site and its vault describe and measure that corpus and redistribute none of it**, and there is a build check that refuses to let the payload into either tree. This is the single most consequential thing in this report for anyone building on the API: **a consumer who reads the OpenAPI licence, sees CC BY 4.0, and redistributes what they fetched would be wrong**, and would have had to open a payload to find out.

### The cross-references are described and not exposed

GeoNames, Wikidata, OCD and FIPS identifiers appear on the platform pages and in **none** of the published schema definitions. If they were exposed, joining the Atlas to anything else in the world would become free. It is the cheapest possible improvement after the one above.

### Small, specific, and probably worth a fix

- **Two source URLs that disagree.** The CPRA record's `law_url` points at the current codification (Division 10, Title 1) and its `primary_source_url` at the one the Act occupied before the 2023 recodification. One is stale. {{claim:source-url-mismatch}}
- **No machine-readable statute anywhere.** Both URLs serve JSF-rendered HTML. There is no Akoma Ntoso and no XML, which closes a blocker and **makes one of the vault's own acceptance tests unpassable for this instrument** — recorded as unpassable rather than weakened. {{claim:cpra-no-akn}}
- **`products` is returned by every entity and documented by none.** 49 of 49. The schema is behind the API here and ahead of it on `open_records`. {{claim:products-undocumented}}
- **`HEAD` returns 405** where `GET` returns 200, so a client cannot size a file before fetching it. The strong `ETag` on `GET` is the better tool anyway. {{claim:head-405}}
- **The entity total moves**: 327,138 today against three other figures published elsewhere. Ordinary for a live dataset that rebuilds nightly. **An observation, not a conversation.** {{claim:entity-count-drift}}

### No public repository, so no corrections path

There is no clone, no fork, no pull request. Everything above had to be written *here*, on a stranger's website, rather than filed where it belongs. Their own argument makes this awkward: they object to reaching your government becoming a rental metered by whoever owns the index, and an API on one domain is a single point of dependency however good the licence and however good the intentions.

### And one that was ours, not theirs

The previous session on this project could not reach `data.ungovr.org` at all — its container's proxy refused CONNECT on the open endpoints, not only the authenticated ones — and it correctly declined a summarising fetch path rather than commit a retrieval it could not hash. **That was our environment, not their API.** This session's container reaches the host fine. {{claim:egress-open}} It is recorded here because the sibling site's ledger opens with the same scar, and because the refusal is worth more as a logged entry than as an absence.

---

## What this report does not claim

- It does not claim the semantic layer this estate builds on top is shipped. [It is designed](/join/), and one MVP of it is built.
- It does not claim any of the above is a mistake on UnGovr's part. **They built for a person reaching their government, and for that the data is shaped right.** The gap only appears when you want to reach the clause underneath.
- It does not claim to know what they want. [No conversation has happened.](#1-disclosure)
- It does not claim the coverage number is a census. [It is a sample of 49, with an interval, and the query is published beside it.](/coverage/)

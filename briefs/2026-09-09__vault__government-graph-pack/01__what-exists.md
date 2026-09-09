# 01 — What Exists: The Assembly Inventory

**version** v0.33.67
**date** 8 September 2026

[← 00 README](00__README.md) · [Pack hub](README.md) · Next → [02 The Model](02__the-model.md)

---

## Why This File Exists First

**Because the size of the work is decided by what is already published, not by what the argument needs.** Six of the twenty-six vaults on the demos index are graph vaults, and three of them are precisely the thing UnGovr does not have. Two live sites already ship the addressing scheme and the provenance discipline this pack inherits. **So the pack is assembly plus one new join**, and any plan that treats it as a build has mis-sized it by an order of magnitude.

---

## Part A: What Is Published On This Side

### The six graph vaults

| Vault | What it is | Why it matters here |
|---|---|---|
| **Standards Atlas (GDPR)** | GDPR as a semantic graph, with writes scoped to a feedback folder | A law as a graph, **with a contribution path**. The corrections shape |
| **Regulation Graph** | The EU AI Act parsed from Formex into an evidence graph, article by article | A law parsed **from its official XML** into a graph, article by article |
| **AIUC-1 conformance layer** | The AIUC-1 standard as a graph, plus a layer computing insurability over it | The layer that turns a graph of requirements into a judgement about a subject |
| **Risk Graph Explorer** | A fact-to-risk graph explorer, built to be public: its `app.json` requests nothing | **The shareable form.** A public graph app that asks for no permissions |
| **Agentic Browser Isolation** | A living risk graph, rendered per stakeholder | The same graph per audience without changing the facts |
| **Scaling Threat Modeling** | Eleven linked threat models across 51 nodes and 179 threats | Linked graphs at a countable scale |

**And the catalogue itself is the recursion argument**: an index of published vaults that is itself a vault and lists itself.

### standards.sgit.ai, at v0.1.4

Honestly labelled a proof of concept. The EU AI Act ships as **1,523 nodes and 1,944 edges** including a 2026 amendment. Provisions are addressed by **two hashes**, one for hierarchical position and one for current text. Each carries a **SHA-256 of the source bytes** and provenance recording the retrieval source, timestamp and method. Akoma Ntoso is in its covered set.

**Its own summary of its state is the sentence to keep**: one instrument is modelled properly. One.

### graphs.sgit.ai

The stronger discipline, and the standard this vault inherits:

- Documents decomposed so that **section, block, sentence and word each become a node with stable identity**
- **The markdown rebuilds from the graph byte for byte**
- Quotes verified byte by byte on every build
- The frozen edition hashed so the build fails if a byte changes

**And its own honest label**: the semantic layer is *designed* rather than *shipped*. That distinction must survive into anything shown to a third party.

---

## Part B: What Is Published On Their Side

*Fetched from UnGovr's own site and live open API on 8 September 2026. Re-check anything you are about to depend on: their data moves, and their marketing pages already disagree with each other by a few thousand entities.*

### The Atlas

| | |
|---|---|
| Entities | ~320,000. The site quotes 330,000, 321,000 and 320,000 on three different pages |
| Countries | **205**, confirmed live from the index endpoint |
| Boundaries | 160,000 |
| United States | **159,926 entities. Half the Atlas is one country** |
| France | 35,235 |
| Italy | 15,968 |

**Their definition of an entity is by obligation, and it is a good one.** An organisation qualifies if it **independently handles public records requests** and has designated leadership with decision-making authority. A place with staff but no independent governance is a *facility*, not an entity. That is a definition by accountability, which is the same instinct that makes this estate insist a mandate names an owner.

**Their depth claim**: in California, special districts outnumber cities by more than ten to one, and that layer below city hall is what nobody else maps.

**Their measurement**: 40.7 per cent of addresses written "Santa Barbara, CA" fall outside the city limits. **A measured claim with a named method that changes what a system should do.** It is the reason Santa Barbara is the county in [`03__the-worked-example.md`](03__the-worked-example.md).

### The API surface

Base URL `data.ungovr.org/v1`, HTTPS, **most of it open with no authentication**. Auth header `X-API-Key`.

| Endpoint | Auth | Returns |
|---|---|---|
| `/entities/index.json` | Open | Countries with entity counts |
| `/entities/{cc}.json` | Open | First-tier entities for a country |
| `/entities/{cc}/{state}.json` | Open | Entities within a state or province |
| `/entities/detail/{id}.json` | Open | Full detail for one entity |
| `/entities/children/{id}.json` | Open | Child entities of a parent |
| `/entities/boundaries/{id}.geojson` | Open | GeoJSON boundary |
| `/laws/records/index.json` | Open | Records-law corpus, compact index |
| `/laws/records/{jurisdiction}.json` | Open | One records law in full |
| `/laws/transparency/index.json` | Open | Transparency laws across five domains |
| `/cgj/index.json`, `/cgj/counties.json`, `/cgj/counties/{code}.json` | Open | Grand jury collection, 58 counties |
| `/cgj/reports/{id}.json` | **Key** | Full report with findings |
| `/ai-laws/index.json`, `/ai-laws/{jurisdiction}.json`, `/ai-laws/vocab.json` | **Key** | AI and crawling law, verdict per jurisdiction, plus vocabulary |
| `/meta/countries.json`, `/meta/schema.json`, `/meta/openapi.yaml`, `/meta/last-updated.json` | Open | Registry, JSON Schema, OpenAPI 3.1, refresh timestamp |

**Rate limits**: entity data 100/day per IP; grand jury indices unlimited; report detail 50/day per key. Over the limit the API answers **HTTP 402** with a payment challenge and the MCP server answers JSON-RPC `-32042`. Entity data $0.001/request, report detail $0.01/request, $5.00 minimum wallet, Stripe.

**MCP server** at `mcp.ungovr.org/mcp`, five tools: `list_countries`, `search_entities`, `get_entity`, `search_cgj_reports`, `get_cgj_report`.

**A published JSON Schema and an OpenAPI 3.1 specification.** That is a level of machine-readability most public bodies never reach, and it is what makes the join cheap.

### The schema, and the edge that stops short

From `/meta/schema.json`, JSON Schema Draft 2020-12.

`entity_detail` requires `slug`, `name`, `type`, `country`, `children_count`, `geography`, `url`, and also carries `state`, `parent` (an object with `slug` and `name`), `children_url`, `domains`, `memberships`, `geography` (with `has_boundary` and `boundary_url`), `population`, `website`, and:

> **`open_records`, an object with `law`. This is the edge that stops short.**

```
   THEIR GRAPH                                     WHERE IT STOPS

   place --spatially--> entity --> parent
                          |    --> children
                          |    --> boundary (GeoJSON)
                          |    --> domains
                          |    --> memberships
                          |
                          +----> open_records.law  --------->  X
                                 "which law applies"
                                                          no provision
                                                          no obligation
                                                          no requirement
                                                          nothing to point at
```

**The consequence is concrete.** A claim built on their data today can say *this water district is governed by the California Public Records Act*. It cannot say *this water district must respond within ten days under section such-and-such, and here is the byte range that says so, retrieved on this date*. **The first is a fact about a jurisdiction. The second is an obligation, and only the second can carry a risk, a control, or an acceptance.**

**And the same gap is visible in their newest work.** The AI and crawling law endpoints return a **verdict** per jurisdiction with a vocabulary defining what the verdict values mean. A verdict is a summary judgement; the provisions it summarises are not addressable, so a reader can neither check it nor disagree with it at the level where disagreement is useful.

### What is a graph here, and what is not

**It earns the name for structure.** Real edges: entity→parent, entity→children, entity→boundary, entity→domain, entity→membership, entity→open-records law. **And the spatial join is the part nobody else has**: given a location they resolve every entity that serves it, and a single address may fall under a city, a county, a school district, a water district and a fire district at once. That is a many-to-many relation computed from geometry rather than declared.

**What makes it less than a semantic graph is that the vocabulary is not published as one.** There is a JSON Schema, which types payloads. There is no ontology: no formal classes, no declared predicates, no equivalence statements to the identifier systems they cross-reference.

**And one open question worth asking them.** Their platform page says Atlas IDs are cross-referenced to **GeoNames, Wikidata, OCD and FIPS**. Those cross-references **do not appear in the schema definitions**. If they are exposed somewhere, joining their entities to anything else becomes free. If they are not, that is the cheapest possible improvement to their surface.

### Licence and publishing

**CC BY 4.0 with attribution to UnGovr**, per their open-data page, with **bulk downloads as JSON** for offline analysis, research or integration. That is the same licence this corpus releases its own briefs under, and it removes the main blocker on building this vault.

**There is no public repository of theirs.** Their technology page lists GitHub as their own source control with no repository linked, and a search of the public index found nothing. **So there is no clone, no fork, no pull request, and no corrections path for an outsider.** See [`04__the-vault.md`](04__the-vault.md) for the corrections offer that follows from this, which is a thing to build rather than a criticism to level.

---

## Part C: The Ledger

**What exists, what is new, and the ratio that should govern the plan.**

| Component of the worked example | State |
|---|---|
| Step 1 — entity resolved from a published slug, with boundary | **New.** Nobody has joined their slugs to an instrument graph |
| Step 2 — instrument rendered as addressable provisions | **Done twice.** GDPR and the EU AI Act. Reuse the method |
| Step 3 — provision as a node with two-hash addressing | Shipped at standards.sgit.ai |
| Step 4 — obligation | Shipped in the conformance work |
| Step 5 — control | Shipped |
| Step 6 — evidence tier, unevidenced as default | Shipped, 4 September conformance layer |
| Step 7 — acceptance with owner, interval, revocation | Shipped, and already carried in a published vault |
| The coverage measurement of their law edge | **New, and it may not exist anywhere** |
| The graph viewer with configurable settings | Documented on the method site |
| The agentic team coordinating through files | House model, in use |
| Release channels for citation by version | Shipped 3 August |

**Two new things. Nine reused.** Plan accordingly.

---

## Sources

- The published vaults index on sgit.ai, read 8 September 2026, for the twenty-six vaults and the six graph vaults. https://sgit.ai/demos/vaults/index.html
- graphs.sgit.ai, read 8 September 2026, for the decomposition rules, the byte-for-byte rebuild, the byte-verified quotes, the hashed frozen edition, and the statement that the semantic layer is designed rather than shipped. https://graphs.sgit.ai
- standards.sgit.ai at v0.1.4, read 8 September 2026, for two-hash addressing, the SHA-256 of source bytes, the provenance fields, the shipped EU AI Act at 1,523 nodes and 1,944 edges, the covered instruments including Akoma Ntoso, and the one-instrument statement. https://standards.sgit.ai
- UnGovr homepage, platform, architecture, entities, agents, vision, tech and open-data pages, read 8 September 2026. https://www.ungovr.org/
- UnGovr Open Data API and MCP pages, read 8 September 2026. https://www.ungovr.org/open-data/api and https://www.ungovr.org/open-data/mcp
- The live schema and country index endpoints, called 8 September 2026. https://data.ungovr.org/v1/meta/schema.json and https://data.ungovr.org/v1/entities/index.json

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

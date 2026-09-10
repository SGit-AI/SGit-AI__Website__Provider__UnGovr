---
title: What you get when you reach a law
description: "Follow the evidence to an instrument and this is what UnGovr hands you: a structured summary in JSON, a link to the publisher — and, for 254 of the 398 records laws, no detail document at all."
lead: "The rabbit hole works right up to the law. **Entity → jurisdiction → instrument all resolve.** Then it stops: there is no text, no PDF, no markdown, no graph — and for **every sub-national jurisdiction**, no detail document that can be addressed at all."
order: 7
toc: true
provenance:
  vault: dkeclt5r @ obj-cas-imm-ca05faec37fd
  date: 9 September 2026
  note: "Every row below was fetched in this session and hashed; the requests are in the retrieval log. Nothing here is read from their documentation."
---

## The short answer

| You want | UnGovr gives you | State |
|---|---|---|
| The law's **text** — md, html, txt, pdf, docx | **Nothing.** No format carries the instrument itself | absent |
| A **structured summary** of it | **31–34 JSON fields**: deadlines, residency, fees, exemptions, appeals, penalties | rich |
| A link to the **actual source** | `law_url` + `primary_source_url` + typed `secondary_sources[]` | **good** |
| **Provision-level** identifiers you could cite as nodes | Only inside `exemptions[].code` — and only on some of them | partial |
| A **semantic graph** — nodes, edges, ontology | **Nothing.** The only "graph" in their whole OpenAPI is *GeoJSON* | absent |
| The same for a **sub-national** jurisdiction | **404.** 254 of 398 laws have no reachable detail document | **broken** |

## JSON, and only JSON

Every response is `application/json`. There is no other representation and **asking for one changes nothing**: {{claim:law-json-only}}

```
GET /v1/laws/records/ad.md      404       GET /v1/laws/records/ad.jsonld  404
GET /v1/laws/records/ad.pdf     404       GET /v1/laws/records/ad.ttl     404
```

Content negotiation is not ignored quietly — it is ignored *identically*. `Accept: text/markdown`, `Accept: application/ld+json` and no `Accept` header at all return the same document with **the same sha256, `b06492bfb34b9572…`, 6,749 bytes**. That is not a header saying JSON; that is the same bytes three times.

## What the summary actually holds — and it is a lot

Andorra's Law 33/2021 comes back as **34 top-level fields**. Not the statute: a research summary of it, with real structure. {{claim:law-no-text}}

`exemptions[]` — 14 entries, each with a code, a name, a description and whether it is discretionary. `appeal_process[]` — the tiers, the body, the deadline in days, a contact URL. `submission_methods[]`, `required_elements[]`, `fee_structure{}`, `penalties{}` split three ways, `response_deadline_notes`, `residency_required`, `private_right_of_action`.

**This is genuinely good data**, and it is the part worth saying plainly: somebody read 398 statutes in dozens of languages and normalised them. The gap below is not a complaint about that work.

## The provenance link is there, and it works

This is the half of the question that has a happy answer. **392 of the 398 laws carry a URL to the instrument at its official publisher** — `portaljuridicandorra.ad`, `boe.es`, `lexfind.ch`, `saij.gob.ar` — across **339 distinct hosts**. {{claim:law-source-links}}

`secondary_sources[]` adds typed extras (`government`, `reference`, …) and `rti_rating_url` links the external rating that scored it. So the hop *out* to the real source exists and is well made. **What does not exist is the hop back *in*** — you leave for a PDF on a government site and the graph ends there.

## Provision-level identifiers: one field, some of the time

`exemptions[].code` carries values like `art11-a` … `art11-m`, `art12`. That is a real article-and-subparagraph anchor — the raw material of a provision node.

But it is the only field that does it, and it does not always. Across a deterministic sample of ten jurisdictions, **58 exemptions carried 34 article-shaped codes — 59%.** {{claim:law-provision-ids}} Everywhere else, article references live in prose: *"Article 15 provides that consultation of public information is free."* Readable by a person, not addressable by a graph.

## The sub-national half is unreachable

This is the finding that matters most for anything jurisdictional. **254 of the 398 records laws are sub-national**, and their `jurisdiction` values carry a slash — `us/ms`, `br/minas-gerais`, `au/nt`, `pk/sindh`. The detail route is a single path segment, so none of them can be addressed.

| Sample | Detail endpoint |
|---|---|
| 26 national jurisdictions (`ad`, `ca`, `fi`, `bj`, `vu`, …) | **26 of 26 returned 200** |
| 24 sub-national jurisdictions (`us/ms`, `au/nt`, `ar/v`, …) | **24 of 24 returned 404** |

Raw, percent-encoded and dash-substituted forms all 404. {{claim:law-subnational-404}} They are not missing from the corpus — **they are in the index**, with name, citation, source URL, response days and RTI rating. It is the 30-odd-field document that cannot be reached.

> **Why this is the expensive one.** Sub-national is where the jurisdictional variation lives, and it is exactly what a standards graph needs. The dev pack's whole argument turns on Colorado, California and New York City being addressable bodies in named places. Their AI-law crosswalks point at those three; their records-law detail does not resolve for any of them.

## Ontology: a controlled vocabulary, not a graph

The closest thing in the whole API is the AI-law corpus's `vocab.json`: **4 verdicts, 6 contexts, 6 crawl-policy fields, 22 field definitions and 17 enums**, with a JSON Schema at `ungovr.ai-laws/2`. {{claim:ai-vocab-not-graph}}

That is a real controlled vocabulary — every enum value defined in prose, which is more than most publishers manage. **It is not an ontology and not a graph**: no classes, no properties with domains and ranges, no relations between terms, no SKOS, no OWL, no RDF, no JSON-LD. A flat dictionary of fields and their permitted values.

The schema document is public; **the data behind it is not** — it is key-gated and its licence states *"No license is conveyed by receipt of this file."* Which is why this site describes its shape and stores none of it.

## So: could we help? Yes, and this is the shape of it

**They have done the expensive half.** Finding, reading and normalising 398 records laws across 205 countries and 2,915 AI-law instruments is the part that does not automate. Nobody else has that corpus.

**What is missing is the part this estate has already built twice.** The Regulation Graph parsed the EU AI Act from official Formex XML into 1,523 nodes hash-verified to source bytes. The EU AI Act current text carries **a sha256 per provision**, rolling to a root hash. Both are the same operation this corpus needs and does not have: *instrument → provisions → citable nodes.*

| They supply | We supply | The result |
|---|---|---|
| The instrument, found and summarised, with its publisher URL | Parsing it into provisions with a hash each | A provision you can cite as a node |
| 254 sub-national jurisdictions, identified and slugged | The anchor node that binds a body to a place | An obligation with a subject |
| A controlled vocabulary of 22 fields and 17 enums | Edges with named inverses | A vocabulary you can traverse |

None of this needs their corpus to be redistributed, which matters because part of it cannot be. **The graph can carry the anchor, the hash and the link, and leave the text where its licence requires it to stay.**

The design is written down: **[the security-standards dev pack](/packs/security-graph/)**, and specifically [file 03](/packs/security-graph/03__the-standards-map/), which now has this page's findings as its evidence rather than an assumption.

## What this page does not claim

**Nothing here is a defect report.** The API does exactly what its OpenAPI says it does; none of the gaps above is a broken promise, and the sub-national 404 is the only one that looks like an oversight rather than a scope decision.

**It is one snapshot.** Every figure was fetched on 9 September 2026 and hashed; the corpus rebuilds nightly. The [retrieval log](/retrievals/) carries every request, including the 404s, because a probe that failed is the evidence for half of this page.

**We have not asked them.** All of this is read off the live API. Whether provision-level structure or a sub-national detail route is planned, refused or simply not yet built is a conversation nobody has had — and [handback item 5](/briefs/) is that somebody should.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

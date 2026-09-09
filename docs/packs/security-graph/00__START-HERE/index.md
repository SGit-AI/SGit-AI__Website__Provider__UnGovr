# 00 — Start Here: The Security-Standards Graph

**version** v0.1 · **9 September 2026** · **status: specified, nothing built**

[🏠 Vault index](../../README.md) › [Packs](../README.md) › **Security graph**

---

## The one-sentence argument

**Every security and AI standard tells you what good looks like. None of them tells you who
has to do it, or where.** UnGovr publish 327,138 identified bodies and 398 jurisdiction-keyed
laws — **the anchor nodes our standards graphs are missing** — and this pack specifies how to
connect them without merging a single vocabulary.

## Why this pack exists

The estate already holds standards as graphs. AIUC-1 is 53 controls, 144 requirements and
**1,126 crosswalks** to thirteen other frameworks. GDPR is a navigable semantic graph. The EU AI
Act exists twice — once parsed from Formex into 1,523 nodes, and once as a **derived current text
where every provision carries its own sha256**, rolling up to a root hash.

**What none of them has is a subject.** A control says *maintain an audit log*. It does not say
*Santa Barbara County must, under Gov. Code § 7922.535(a), within 10 calendar days*. The obligated
party and the jurisdiction that binds it are the two node classes every one of these graphs
gestures at and none of them identifies.

That is exactly the gap this vault has already measured on the government side — and the same
missing edge, seen from the other direction.

## Read in order

| # | File | Holds |
|---|---|---|
| 00 | Start Here (this file) | The argument, the order, and what is already decided |
| 01 | [The anchor-node thesis](01__the-anchor-node-thesis.md) | **Read this before you model anything.** Why bridging beats merging, in graphs.sgit.ai's own words |
| 02 | [The model](02__the-model.md) | Node classes, the edge vocabulary and its inverses, provenance fields, the two-edge rule |
| 03 | [The standards map](03__the-standards-map.md) | **What exists as a graph, what does not, and the honest state of each** |
| 04 | [The worked example](04__the-worked-example.md) | **The deliverable.** One control, one body, one jurisdiction, end to end |
| 05 | [Integration](05__integration.md) | RiskMandate, Licence to Operate, the AIUC-1 conformance layer — concretely |
| 06 | [Verification](06__verification.md) | Acceptance tests, blockers, and what would make this pack wrong |

## What is already decided

Do not relitigate these. Each is settled, and each is inherited from work that is published and
checkable rather than from an opinion formed here.

| Decision | Where it comes from |
|---|---|
| **Vocabularies are never merged.** Standards keep their own terms and are bridged through anchor nodes | [graphs.sgit.ai, thesis sentence 6](https://graphs.sgit.ai/v1/depth/index.html) |
| **Every edge is a verb with a distinct inverse.** The generic association edge is banned | graphs.sgit.ai, the grammar |
| **Never render the whole graph — render the result of a query** | graphs.sgit.ai, thesis sentence 8 |
| **Classification is a query, not a judgment** | graphs.sgit.ai, thesis sentence 3 |
| Origin and assertion class are **two channels, never merged** | This vault's `pack/02__the-model.md`, and the AIUC-1 two-edge rule |
| **`unevidenced` is the default state**, and an absent row is never read as compliance | The AIUC-1 conformance layer |
| A crosswalk the standard body did not publish is **`inferred`**, always | This vault, `sg:resolvesTo` |
| Scope is **one control, one body, one jurisdiction**. Widening it weakens it | This vault's `pack/00__README.md` |

## The order is strict

**Anchors first, then one standard, then the crosswalk.** Not the other way round.

A crosswalk built before the anchors exist is a mapping between two vocabularies with nothing
underneath it — which is the thing sentence 5 of the thesis warns about, and the reason the
Semantic Web's promise stayed a promise.

## The one thing to check first

```bash
curl -sS https://eu-ai-act.standards.riskmandate.ai/provisions/index.json | head -40
```

**If that returns per-provision ids with sha256 hashes, the instrument layer is already solved for
one major standard** and this pack's step 2 is a join rather than a parse. It did on 9 September
2026; confirm rather than assume, because it is a live site.

## What this pack is not

**It is not a proposal to build a compliance product.** It specifies a graph that makes one
question answerable — *which obligations bind this body, in this jurisdiction, and what is the
state of the evidence* — and it states plainly which parts of that are inferred.

**And it is not a claim that UnGovr endorse any of it.** No conversation has taken place. Their
data is used under CC BY 4.0 with attribution, and every edge drawn from it into our model is
marked `inferred` for exactly that reason.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

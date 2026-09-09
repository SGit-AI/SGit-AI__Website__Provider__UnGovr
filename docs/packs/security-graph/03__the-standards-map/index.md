# 03 — The Standards Map

**version** v0.1 · 9 September 2026

[← 02 The model](02__the-model.md) · Next → [04 The worked example](04__the-worked-example.md)

---

## How to read this file

**Two columns matter more than the rest: what state the corpus is in, and who says so.**

Rows marked **`in the estate`** were read from that vault's or site's own published page on
9 September 2026 and the figures are quoted from it. Rows marked **`candidate`** are named from
general knowledge and **nothing about their structure has been checked** — they are a work list,
not an inventory, and treating them as one would be the exact failure this estate keeps a claim
ledger to prevent.

## What already exists as a graph, in this estate

| Standard | Where | Shape, as its own page states it | State |
|---|---|---|---|
| **AIUC-1** (agent standard) | [aiuc-1-graph](https://sgit.ai/demos/vaults/aiuc-1-graph/index.md) vault `2wzct4k7` | **53 controls, 144 requirements, 1,126 crosswalks, 1,238 nodes, 3,526 edges** over five releases; every field names the page or commit it was read from with the sha256 of the retrieved bytes | **the richest thing we have** |
| **AIUC-1 conformance** | [aiuc-1-conformance](https://sgit.ai/demos/vaults/aiuc-1-conformance/index.md) `2wzct4k7` | A fork adding one directory: `attested_by` kept permanently apart from `evidenced_by`, 53 conformance rows, insurability as a query | **the layer everything else should imitate** |
| **EU AI Act** — as parsed law | [regulation-graph](https://sgit.ai/demos/vaults/regulation-graph/index.md) `73heuprz` | Regulation (EU) 2024/1689 parsed from **official Formex XML**, hash-verified to source bytes, **1,523 nodes and 1,944 edges** across eleven views | **the model for instrument parsing** |
| **EU AI Act** — as current text | [eu-ai-act.standards.riskmandate.ai](https://eu-ai-act.standards.riskmandate.ai/articles.md) | The composed current text with the Digital Omnibus applied by a gated parser. **Per-provision ids, statuses and sha256**, rolling to a root hash; `.md` and `.llm.json` on every slug; JSON-LD and Turtle exports | **the instrument layer, solved** |
| **GDPR** | [standards-atlas-gdpr](https://sgit.ai/demos/vaults/standards-atlas-gdpr/index.md) `4zv4bvmu` | GDPR as a navigable semantic graph, with **CJEU rulings, regulator guidance and per-country variation as first-class nodes** layered over the articles they bend | **the model for jurisdictional variation** |

**Read that table as the answer to "can this be done".** Two regulations and one standard are
already graphs with byte-level provenance. **The method is proven; what is missing is breadth and
an anchor.**

## AIUC-1's thirteen, read from its own graph

**Blocker S1 is closed.** The pack said this was the cheapest thing to check and it was: the
crosswalk targets are in `graph/edges.json` of vault `2wzct4k7`, opened with its published read
key. **1,126 crosswalks across exactly thirteen frameworks**, counted from the edges themselves:

| Framework | `in_framework` | crosswalks | Kind |
|---|---|---|---|
| CSA AI Controls Matrix | 360 | 320 | control set |
| IBM AI Risk Atlas | 138 | 145 | risk taxonomy |
| ISO/IEC 42001 | 124 | 105 | management system |
| NIST AI RMF | 110 | 152 | framework |
| Cisco AI Security Framework | 80 | 135 | vendor framework |
| **EU AI Act** | 54 | 62 | **law** |
| MITRE ATLAS | 34 | 32 | threat taxonomy |
| OWASP Top 10 **(for LLM Applications)** | 20 | 60 | threat list |
| OWASP Agentic Top 10 | 20 | 55 | threat list |
| OWASP AIVSS | 20 | 27 | scoring |
| **NYC Local Law 144** | 8 | 6 | **law** |
| **Colorado AI Act** | 6 | 18 | **law** |
| **California SB 53** | 4 | 9 | **law** |

**One row needs its label read carefully.** `framework:owasp-top-10` is labelled *"OWASP Top 10"*,
which reads as the web application list. Its members are not: they are `LLM01:25 - Prompt Injection`
through `LLM10:25 - Unbounded Consumption` — the **OWASP Top 10 for LLM Applications (2025)**.
Checked by listing the ten `in_framework` members rather than trusting the label, which is the
only reason the AI-specific finding below survives. **A shorthand label that collides with a
different, better-known standard is the kind of thing an anchor node exists to disambiguate**, and
it is worth reporting upstream rather than silently working around.

**Two findings, and the second is the important one.**

### One: the coverage is AI-specific, not general security

**Not one general security control set is in that list.** No NIST CSF, no NIST SP 800-53, no
ISO/IEC 27001 or 27002, no SOC 2, no CIS Controls, no PCI DSS, no HIPAA, no FedRAMP.

That is not a gap in AIUC-1 — it is an agent standard and it crosswalks to the AI corpus, which is
the right scope for it. **But it means the general-security half of the map is genuinely absent
from this estate**, and anyone assuming "AIUC-1 covers the crosswalks" would be wrong about
exactly the frameworks most enterprises are actually assessed against.

### Two: four of the thirteen are laws, and three are sub-national US laws

`eu-ai-act`, `co-ai-act`, `ca-sb-53`, `nyc-ll-144`.

**Colorado. California. New York City.** Those are not abstractions — they are jurisdictions with
UnGovr entity slugs: `us/co`, `us/ca`, `us/ny/…`. A crosswalk from an AIUC-1 control to the
Colorado AI Act currently floats free of any statement about **who in Colorado it binds**.

**This is the join, and it is already half-built by somebody else.** AIUC-1 supplies the control →
law edge. UnGovr supplies the body → jurisdiction anchor. Nobody has connected them, and the
connection is one edge.

### And they already use anchor nodes

The crosswalk edges do not point at frameworks. They point at **`anchor:` nodes** —
`anchor:co-ai-act:6-1-1702-developer-duties` — reached by an `anchors_to` edge, of which there are
489.

**So the anchor pattern is established in this estate and this pack is not proposing it.** What it
proposes is a *different axis of anchor*: theirs anchor **provisions across standards**; ours
would anchor **obligations to the body and the place**. The two compose; neither replaces the
other. [File 01](01__the-anchor-node-thesis.md) is right about the principle and was wrong to
imply the estate had not applied it.

## The candidate list — named, not inventoried

**Nothing in this table has been checked.** No structure, no licence, no machine-readable source,
no count. Every cell would start `unevidenced`.

| Family | Candidates | Why it matters here |
|---|---|---|
| **General security control sets** | NIST CSF 2.0 · NIST SP 800-53 · ISO/IEC 27001 & 27002 · SOC 2 TSC · CIS Controls | **The real gap.** Confirmed absent from AIUC-1's thirteen, and the set most enterprises are assessed against |
| **Sectoral** | PCI DSS · HIPAA Security Rule · FedRAMP · DORA | Scope is defined by what the body *does* — the entity anchor's `type` field carries part of this |
| **EU regulatory, beyond the AI Act** | NIS2 · the Cyber Resilience Act | **Where the jurisdiction anchor earns its place**: scope clauses keyed to entity type and member state |
| **Already covered by AIUC-1** | CSA AICM · ISO 42001 · NIST AI RMF · MITRE ATLAS · OWASP · EU AI Act · CO · CA · NYC | **Do not redraw.** Fork the crosswalks byte for byte, as the conformance layer forked the catalogue |

**The licence question comes before the parse, every time.** This vault learned that the expensive
way: UnGovr's AI-law corpus reads as part of a CC BY 4.0 API and carries its own licence saying
*"No license is conveyed by receipt of this file."* Several standards bodies charge for the text.
A graph of ids, structure and crosswalks **without** the text is still useful — but that has to be
a decision made before the work.

## What the anchor changes, per family

The point of the map is not the list. It is what a jurisdiction anchor does to it:

| Question, today | Question, with the anchor |
|---|---|
| *Which controls does ISO 27001 A.5.15 map to?* | unchanged — a crosswalk, and AIUC-1 already answers this shape |
| *Does NIS2 apply to us?* | **a query over `governed_by`**, not a lawyer's reading of a scope clause |
| *Which obligations bind this specific body?* | **answerable**, and currently not expressible at all |
| *What is the evidence state of each?* | **answerable, with `unevidenced` as the honest default** |
| *Two bodies, same standard — comparable?* | **yes, because the subject is a node rather than a string** |

**Only the first row works today.** The other four are what the anchor is for.

## The order of work, and it is not the obvious one

1. **The anchors.** UnGovr entity + jurisdiction, with the `governed_by` edge **marked inferred**
   and its 96.6% / 20.5% measured. *This vault has already done this for one jurisdiction.*
2. **One instrument, already solved.** The EU AI Act current text — per-provision ids and hashes
   exist, so this is a join and not a parse. **Do not re-parse what RiskMandate has parsed.**
3. **One standard, already graphed.** AIUC-1. Do not re-transcribe it; fork it the way the
   conformance layer forked it, byte for byte.
4. **One crosswalk edge**, `std:control --addresses--> sg:obligation`, drawn once, by hand,
   for one control, and **marked inferred**.
5. **Only then** widen — and widening means another anchor, not another standard.

**A crosswalk built before step 1 is a mapping between two vocabularies with nothing underneath
it.** That is the failure mode thesis sentence 5 names, and it is why this order is strict.

## What would make this file wrong

| If this turns out to be true | Then |
|---|---|
| ~~AIUC-1's thirteen already include most of the candidate list~~ | **Checked, and no.** They are AI-specific; the general-security half is genuinely missing. Four of the thirteen are laws, three of them sub-national US, which is where the anchor pays off first |
| A standards body publishes machine-readable jurisdiction scope | Their binding beats our inference. Cite it and delete our edge |
| The estate's existing graphs disagree on the EU AI Act's structure | Two independent parses of one law disagreeing is a **finding worth publishing**, not a defect to hide |
| Most candidates forbid redistribution | The graph carries ids, structure and crosswalks and **not the text** — and says so on its face |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

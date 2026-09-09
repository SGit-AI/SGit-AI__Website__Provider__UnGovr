# 04 — The Worked Example

**version** v0.1 · 9 September 2026 · **status: specified, not built**

[← 03 The standards map](03__the-standards-map.md) · Next → [05 Integration](05__integration.md)

---

## This is the deliverable

**One control. One body. One jurisdiction. End to end, with every node carrying either a hash or
an honest note saying it is ours.**

Not a survey of standards. Not a crosswalk matrix. **One path that reads as a sentence and can be
checked byte for byte at every hop.**

## The path

```
  ung:us/ca/santa-barbara          ENTITY        UnGovr, sha256, CC BY 4.0
        |
        | governed_by                            <- INFERRED. UnGovr do not draw this
        v
  ung:jurisdiction/us-ca           JURISDICTION  UnGovr, sha256
        |
        | governs -> instrument
        v
  akn:cpra                         INSTRUMENT    Cal. Gov. Code 7920-7931
        |
        | has_provision
        v
  akn:cpra#7922.535(a)             PROVISION     cited in prose, NOT addressable  <- the gap
        |
        | creates_obligation
        v
  sg:obl/determine-and-notify-10d  OBLIGATION    ours. 10 calendar days, +14
        ^
        | addresses                              <- INFERRED. AIUC-1 do not draw this
        |
  std:aiuc-1/A001                  CONTROL       AIUC-1, sha256, forked byte for byte
        |
        | has_requirement
        v
  std:aiuc-1/A001-R1               REQUIREMENT   AIUC-1
        |
        | attested_by                            <- the conformance layer's edge
        v
  sg:attestation/none              (absent)      unevidenced. THE DEFAULT
        |
        | accepted_by
        v
  sg:acceptance/unassigned         ACCEPTANCE    no owner. Ships open
```

**Two edges are inferred and both are marked.** `governed_by`, because UnGovr publish entities and
laws and do not join them. `addresses`, because AIUC-1 publish controls and crosswalks to other
standards and do not map to statutory obligations. **Neither body made the claim we are making,
and drawing either solid would be a lie about the source.**

## Why this pair, specifically

**Because the two ends are as unlike each other as the graph will ever have to handle.**

One end is a **statutory** obligation: a legislature wrote it, the deadline is in calendar days,
and nobody negotiates it. The other is a **standard's** control: a private body wrote it, its
requirements carry tiers, and conformance is attested rather than adjudicated.

If the model survives that pair it survives ISO-to-NIST, which is two control sets of the same
kind. **Prove the hard join first.**

## The seven steps

| # | Step | Cost | Where the bytes come from |
|---|---|---|---|
| 1 | Transcribe the entity | **done** in this vault | `/v1/entities/detail/us--ca--santa-barbara.json`, sha256 `8d5e6db9…` |
| 2 | Transcribe the jurisdiction and instrument | **done** | `/v1/laws/records/us--ca.json`, sha256 `ce8bc474…` |
| 3 | Draw `governed_by`, marked inferred, with its measured reach | **done** — 96.6%, of which 20.5% need a human | `bin/inferred-join.py` |
| 4 | Mint the provision node | **done, and it is the finding** | The clause is prose in `response_deadline_notes`. **No addressable id exists to point at** |
| 5 | Fork AIUC-1's control byte for byte | **not started** | Vault `2wzct4k7`, published read key |
| 6 | Draw `addresses`, marked inferred | **not started** | One edge, drawn by hand, once |
| 7 | Leave `attested_by` absent and the acceptance unowned | **done** | Both are the default and both stay |

**Five of seven already exist in this vault.** The pack is mostly a specification for steps 5 and
6, which is deliberate: the expensive parts are done and the remaining work is one fork and one
edge.

## The asymmetry that makes the point

Compare the two instrument layers at step 4:

| | CPRA (UnGovr) | EU AI Act (RiskMandate) |
|---|---|---|
| Provision addressable? | **No.** `§ 7922.535(a)` is prose inside a notes field | **Yes.** Per-provision id |
| Provision hashed? | No | **Yes**, sha256 per provision, rolling to a root hash |
| Machine-readable source? | **No.** JSF-rendered HTML both URLs | **Yes.** `.llm.json`, JSON-LD, Turtle |
| Can you cite the clause? | **No** | **Yes** |

**Same layer of the same graph, two sources, and one of them can carry evidence and the other
cannot.** That contrast is the strongest argument in this pack for what an instrument layer needs
to look like — and it costs nothing to make, because both artefacts already exist.

**It is also the fair reading of UnGovr's position.** They built a records-law corpus for people
filing records requests, and for that purpose a citation in prose is entirely adequate. The
addressable-provision requirement comes from *our* use, not from a defect in theirs.

## Acceptance, and the thing it must not do

The path ends on `sg:acceptance/unassigned` — **no named owner, no review interval, no revocation
path** — and it stays that way.

An acceptance is the only node in this graph that a human must sign. **Generating one because the
schema has a slot for it would make every downstream number meaningless**, and it is precisely
what the AIUC-1 layer means by *"unevidenced is a state, and it is the default."*

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

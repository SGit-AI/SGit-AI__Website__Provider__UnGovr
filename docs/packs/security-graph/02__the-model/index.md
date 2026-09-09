# 02 — The Model

**version** v0.1 · 9 September 2026

[← 01 The anchor-node thesis](01__the-anchor-node-thesis.md) · Next → [03 The standards map](03__the-standards-map.md)

---

## Five node classes, and the prefix says whose claim it is

**Origin is carried by the prefix and never by the colour.** This is the two-edge rule this vault
already ships, extended by one class.

| Prefix | Class | Who asserts it | Editable by us |
|---|---|---|---|
| `ung:` | **Anchor** — entity, jurisdiction | UnGovr | **Never.** Transcribed with provenance and left alone |
| `akn:` | **Instrument** — act, provision | The publisher of the law | Never. Anchored to a published citation |
| `std:` | **Standard** — framework, control, requirement | The standards body | Never. Transcribed from their published corpus |
| `sg:` | **Our model** — obligation, control-instance, evidence, acceptance | **Us** | Yes. This is the only layer we own |
| `x:` | **Crosswalk** — a claimed correspondence | Whoever published it, **or us** | Yes, and always carries who |

**Four of the five are somebody else's.** That ratio is the point: the value is in the connective
tissue, not in re-typing corpora that already exist.

## The edge vocabulary

Every edge is a verb with a **distinct, meaningfully-named inverse** — not the same edge walked
backwards. The generic association edge is banned.

**Six** come from [graphs.sgit.ai's fifteen established edges](https://graphs.sgit.ai/v1/grammar/edge-set.html),
reused with **their** inverse names. **Four** come from the AIUC-1 conformance layer. **Five** are
proposed here and marked as proposed, exactly as that site marks its own.

> **This paragraph said *eight … reused unchanged*, and four of the six were not unchanged.**
> `observed_on` had been given the inverse `observation_of` where the published set says
> `bears_observation`; `backed_by`→`backs` for `evidences`; `accepted_by`→`accepts` for `accepted`;
> `conditional_on`→`condition_for` for `conditions`. Renaming another vocabulary's inverses and
> calling it reuse is a **fork**, and it is the exact failure this pack's own rule 6 exists to
> prevent — committed by the file that states the rule. Caught by fetching the published edge set
> and comparing row by row, not by rereading this table. **The four are now theirs.**

| Edge | Inverse | Domain → range | Status |
|---|---|---|---|
| `located_in` | `contains` | entity → entity | **proposed here** |
| `governed_by` | `governs` | entity → jurisdiction | **proposed here** |
| `has_provision` | `provision_of` | instrument → provision | **proposed here** |
| `creates_obligation` | `arises_from` | provision → obligation | **proposed here** |
| `addresses` | `addressed_by` | std:control → obligation | **proposed here** |
| `maps_to` | `mapped_from` | std:control → std:control | established (AIUC-1 uses it) |
| `has_requirement` | `requirement_of` | std:control → requirement | established (AIUC-1) |
| `evidenced_by` | `evidences` | anything → evidence | **established.** Do not redefine |
| `attested_by` | `attests` | control-instance → attestation | **established.** Never traversed with `evidenced_by` unnamed |
| `observed_on` | `bears_observation` | evidence → date | established |
| `backed_by` | `evidences` | claim → source bytes | established |
| `accepted_by` | `accepted` | evidence → acceptance | established |
| `owned_by` | `owns` | acceptance → named person | established |
| `conditional_on` | `conditions` | obligation → condition | established |
| `underwritten_by` | `underwrites` | acceptance → policy | established |

**Rule for extending this set**, quoted from the grammar: *a new edge needs a sentence, its inverse
needs a different sentence, both need a stated domain and range.* The five proposed above each do.

## The rule that keeps `evidenced_by` and `attested_by` apart

Taken whole from the AIUC-1 conformance layer, because it is already load-bearing there:

| Edge | Answers | Absent means |
|---|---|---|
| `evidenced_by` | does the **standard** say this? | a build defect |
| `attested_by` | does **this subject** do this? | the control is **unevidenced — which is the finding** |

**A query may traverse both, and must name which it used.** The conformance layer enforces this
with a test that goes red if a layer edge reaches a source observation. This pack inherits the
rule and the test.

## Provenance, on every node that claims a source

Seven fields, unchanged from this vault's existing model:

```json
{
  "source_url":       "https://data.ungovr.org/v1/entities/detail/us--ca--santa-barbara.json",
  "response_sha256":  "8d5e6db9e4056b2f68fcd66da7c18e6797340bf516dc5c4446f0e8267e0fcd7d",
  "retrieved":        "2026-09-09T01:49Z",
  "method":           "HTTPS GET, raw bytes hashed before parsing",
  "licence":          "CC BY 4.0",
  "assertion":        "asserted | inferred",
  "note":             "for nodes that are ours, instead of a hash they have not earned"
}
```

**A node that is our model carries the note and no hash.** Writing a plausible-looking hash on a
node nobody retrieved is the exact failure the whole method exists to prevent.

## The crosswalk rule

**A crosswalk edge always names who drew it**, and there are only two answers:

| `x:source` | Meaning | Assertion |
|---|---|---|
| the standards body | They published this mapping | `asserted` |
| **us** | We drew it | **`inferred`, always, with no exceptions** |

AIUC-1's 1,126 crosswalks are the first kind and can be transcribed. **Anything we add between two
standards is the second kind**, and rendering it like the first would be a lie about the source —
the same lie `sg:resolvesTo` would be if it were drawn solid.

## Rendering

**Never render the whole graph. Render the result of a query.** Mermaid is unreadable past ~50
nodes; a rendered graph past ~300–400. A standards graph is tens of thousands of nodes, so
*whole-graph* is not a view, it is a failure mode.

**Two visual channels, never merged**, as this vault's app already does:

- **Origin** (`ung:` / `akn:` / `std:` / `sg:` / `x:`) → **shape and border**
- **Assertion class** (`asserted` / `inferred`) → **colour**

Hue is spent on the second, so the first cannot also use it. **A reader checking this work checks
that separation first.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

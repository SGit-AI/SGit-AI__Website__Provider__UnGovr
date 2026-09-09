# 01 — The Anchor-Node Thesis

**version** v0.1 · 9 September 2026

[← 00 Start Here](00__START-HERE.md) · Next → [02 The Model](02__the-model.md)

---

## The rule this whole pack rests on

From [graphs.sgit.ai, thesis sentence 6](https://graphs.sgit.ai/v1/depth/index.html), quoted rather than paraphrased:

> **So don't merge vocabularies — merging erases the disagreement. Keep them intact and bridge
> them through anchor nodes.**

**Everything below is a consequence of taking that literally.**

## The temptation, and why it fails

The obvious move with a dozen security standards is to build one super-ontology: normalise NIST's
subcategories, ISO's controls, SOC 2's criteria and AIUC-1's requirements into a single control
vocabulary, then map everything to it.

**This fails at the first real disagreement.** NIST CSF's `PR.AA-05` and ISO 27001's `A.5.15` are
*about* the same thing and are not the same thing: different scopes, different evidence
expectations, different assessor traditions. A merged vocabulary has to pick one, and the moment it
picks, **the disagreement — which is the information a practitioner actually needs — is gone.**

The estate has already recorded what that costs. AIUC-1 publishes **1,126 crosswalks** and the
conformance layer keeps `evidenced_by` and `attested_by` in *separate graphs*, with a test that goes
red if a query traverses both without naming which it used. That is the same instinct: **keep the
vocabularies, make the bridge explicit and inspectable.**

## What an anchor node is

An anchor node is a node **both vocabularies can point at without either giving anything up.** It
has three properties:

| Property | Why it matters |
|---|---|
| **Stable identifier** | Two graphs built a year apart must reach the same node |
| **Published by a third party** | If we mint it, we are back to a house ontology with extra steps |
| **Independently meaningful** | It must denote something in the world, not a bucket we invented |

**UnGovr supply two node classes that satisfy all three, and nothing else in this estate does.**

## The two anchors

### `ung:entity` — the obligated party

**327,138 identified bodies**, each with a stable slug (`us/ca/santa-barbara`), a hierarchy, a
boundary, and domains. Published under CC BY 4.0.

Every standards graph in this estate describes obligations **in the abstract**. A control says
*maintain an audit log*; it never says *who*. The subject is supplied at use time, ad hoc, usually
as a free-text customer name — which is why conformance results cannot be compared across two
assessments, let alone aggregated.

**With a stable entity id, "who" stops being a string and becomes a node.**

### `ung:jurisdiction` — the law that binds

**398 records laws, 254 of them sub-national**, keyed by a path (`us/ca`, `mx/baja-california`)
that is a prefix of the entity slug — plus an AI-and-crawling-law corpus covering **271
jurisdictions with 2,915 instruments**, which is key-gated and **not CC BY 4.0**.

Standards do not apply uniformly. The EU AI Act binds a provider placing a model on the EU market;
the CPRA binds a Californian public agency; NIS2 binds essential entities in member states.
**Today "does this apply to me" is answered by a human reading a scope clause.**

**With a jurisdiction anchor it becomes a query** — which is thesis sentence 3, applied:
*classification is a query, not a judgment.*

## What this buys, stated as sentences a path can read

The grammar's own test is that a path must read as a sentence. These do:

```
  santa-barbara-county  --located_in-->        us/ca
  us/ca                 --governed_by-->       cpra
  cpra                  --has_provision-->     gov-7922.535(a)
  gov-7922.535(a)       --creates_obligation--> determine-and-notify-10d
  aiuc-1:A001           --addresses-->         determine-and-notify-10d
  determine-and-notify  --evidenced_by-->      (nothing yet)   <- the finding
```

**Read the last two lines together.** A standard's control and a statutory obligation meeting over
the same anchor is the thing none of these graphs can currently express — and it is one join, not
a new ontology.

## The honest part

**The `located_in` and `governed_by` edges are the weak links, and they must stay marked.**

This vault has already measured them. Of 49 sampled entities, **0 carry a published
`open_records.law`** — a missing law reference is not an error, it is an entity whose records law
has not been mapped yet, and **it is not a defect count**. Inferring the edge by slug prefix
reaches **96.6%** of California's 16,071 bodies, and **20.5% of those matches would need a human**,
because slug hierarchy is geography and records law is jurisdiction.

So the anchor layer is real, and **the edge into it is inferred**. Both facts ship together or the
graph is a lie about its own sources.

## What would make this thesis wrong

| If this turns out to be true | Then |
|---|---|
| A standards body publishes its own jurisdiction bindings, machine-readable | The anchor is theirs, not ours, and we cite rather than infer. **Strictly better** |
| The entity ids churn between releases | The anchor is not stable and the whole thesis fails. **Check this before building** |
| Practitioners want the merged vocabulary anyway | They may — but then the disagreement belongs in a layer above, not erased below |
| Two standards genuinely mean the same thing | Then a crosswalk is an identity, and saying so is cheap. The rule costs nothing when it is easy |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

---
deck: How this composes
subtitle: With Risk Mandate, Licence to Operate, and the sgit vault family
date: September 2026
accent: blue
---

# How this composes

> **Deck 3 of 4.** What this vault contributes to the estate's other vaults, and what it takes
> from them. Every claim about another vault here is read from **that vault's own published
> page**, and linked, rather than recalled.
>
> This is the markdown source; the **Decks** view is a projection of it.

---

## The shape **everything shares**

Four vaults, one chain, different segments of it:

```
  AIUC-1        standard -> control -> requirement -> attestation -> conformance -> insurability
  LICENCE       grant -> mandate -> DELTA -> policy -> covered / not covered
  THIS VAULT    entity -> instrument -> provision -> obligation -> control -> evidence -> acceptance
```

**They overlap at `control`, `evidence` and `acceptance`.** That is not a coincidence — it is the
same risk-acceptance grammar applied to three different sources of obligation: a standard, a
mandate, and a statute.

**This vault supplies the third one, which none of the others had.**

---

## What we take: the two-edge rule

The AIUC-1 conformance vault keeps two edges *"never traversed in one query without the query
naming which it used"*:

| Edge | Answers | Absent means |
|---|---|---|
| `evidenced_by` | does the **standard** say this? | a build defect |
| `attested_by` | does **this subject** do this? | the control is **unevidenced — which is the finding** |

**We do the same thing on a different axis.** `ung:` is what UnGovr publish; `sg:` is our model;
exactly one edge crosses between them and it is drawn `inferred`.

Their rule is enforced by a test that goes red if a layer edge reaches a `source_observation`.
Ours is enforced by a build check that fails if any page names `sg:resolvesTo` without marking it
inferred.

---

## What we take: unevidenced is a state

From the same vault: *"Every control in scope gets a row whether or not anyone has looked at it,
so an absent row is never quietly read as compliance."*

Their first build of one subject across 53 controls: **2 evidenced, 48 unevidenced, 3
contradicted** — *"the designed answer, not a failure to finish."*

**Our evidence node ships `unevidenced` and our acceptance node ships with no owner.** Both are
the default, both stay, and both mean *nobody has looked* rather than *nothing is wrong*.

---

## What we contribute: a **jurisdiction layer**

**327,138 entities. 398 records laws. 254 of them sub-national.**

A `policy/v1` that covers an agent acting for a public body has to know **which body, and which
law binds it**. Neither the Licence to Operate vault nor the conformance layer carries that, and
neither should have to build it.

This vault is that lookup — with the honest caveat attached, which is that the entity-to-law edge
is **inferred**, reaches 96.6%, and hands 20.5% of matches to a human.

> **Notes.** The caveat is the contribution as much as the data is. A jurisdiction layer that
> silently guessed would be worse than none.

---

## What we contribute: a clock **nobody negotiates**

The conformance layer's headline mechanism is that **time breaks the policy**: move the date to
2027-01-15, *"with nothing edited by anybody"*, and one condition becomes **53 exclusions** —
because the attestations behind them expire.

**Our obligations expire on a different clock, and it is not ours.**

`Gov. Code § 7922.535(a)`: the agency shall determine and notify **within 10 calendar days**,
extendable by 14 in unusual circumstances. Calendar days — office closures do not toll it.

An attestation expiry is a policy parameter somebody chose. **A statutory deadline is a fact
about the world.** A conformance model that can carry both is strictly better than one that can
only carry the first.

---

## The delta, at **zero**

Licence to Operate's argument, made countable:

| | | In their demo |
|---|---|---|
| **CAN DO** — the grant | what the agent can technically reach | **12 capabilities** |
| **MAY DO** — the mandate | what is actually expected, and all the policy insures | **4** |
| **THE DELTA** | inside reach, outside authority. **Nothing covers these** | **8** |

**This vault's app declares `"permissions": []`.**

CAN DO equals MAY DO. **The delta is zero** — not managed down, absent. It is the smallest
possible instance of their argument, and it is why a stranger can open this vault read-only and
be asked for nothing.

---

## Where the three meet: an **unowned acceptance**

Our chain ends on `sg:acceptance/unassigned` — **no named owner, no review interval, no
revocation path.**

Read through the conformance layer's vocabulary, that is not a gap in the diagram. It is a
**conformance state**, and it is `unevidenced`.

Read through Licence to Operate's, it is not a condition on a policy. **It is an exclusion** —
and the exclusion carries its reason in the control's own words: *an acceptance without an owner
is a note.*

**Three vaults, three vocabularies, one unfilled field, and all three agree on what it means.**
That is the strongest evidence so far that the grammar is real rather than a house style.

---

## What we took from the family, concretely

| From | What we used |
|---|---|
| **Risk Graph Explorer** | `PUBLIC.md`'s three rules for a vault whose read key is published. We added a fourth: nothing whose licence forbids republication |
| **Regulation Graph** | law-as-a-citable-graph, hash-verified to source bytes — the closest analogue to this work |
| **AIUC-1 conformance** | the two-edge rule, and `unevidenced` as a default rather than an absence |
| **Licence to Operate** | grant / mandate / delta, and the `policy/v1` shape |
| **Risk Mandate** | that a real application ships *as* a vault, with a release history |
| **sgit.ai** | the embed protocol — the read key posted to a pinned origin after a handshake, never in a URL |

---

## The one thing to **build next**

**Make the obligation layer a `policy/v1` producer.**

This vault already has the pieces: an entity, an instrument, an addressable-enough provision, a
statutory deadline as a scalar, a control, and an acceptance with a named hole in it.

The missing step is emitting the conformance row — **one obligation, one control, one state, one
`valid_until` driven by the statute rather than by an attestation** — in the shape the
conformance layer already reads.

Then a policy could say: *this agent may file a records request on behalf of this body, in this
jurisdiction, under this law, with this deadline* — and say what it does **not** prove.

> **Notes.** Scope discipline still applies. One county, one law, one acceptance. The point of
> this slide is the interface, not a second vault.

---

## What this **does not** prove

Borrowed deliberately from the conformance layer's own `does_not_prove` field:

- It does **not** prove Santa Barbara County complies with anything. The evidence node is
  `unevidenced` because **nobody has observed the county**.
- It does **not** prove UnGovr intend any of this. **No conversation has taken place**; every
  statement about their intentions is inference from what they publish.
- It does **not** prove the inferred edge is right for any particular entity. It reaches 96.6%
  and hands 20.5% of those to a human.
- It does **not** make anything citable by version. That release channel was **withdrawn**, and
  acceptance test 9 regressed to `unevidenced` rather than being left looking satisfied.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

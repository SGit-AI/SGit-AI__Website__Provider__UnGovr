# 02 — The Model: Nodes, Edges, Addressing, Provenance

**version** v0.33.67
**date** 8 September 2026

[← 01 What Exists](01__what-exists.md) · [Pack hub](README.md) · Next → [03 The Worked Example](03__the-worked-example.md)

---

## The One Rule Everything Else Serves

> **Their nodes are theirs. Our nodes attach without altering them.**

This is the attach-never-mutate rule of 9 August, applied. **No node derived from UnGovr's data is ever edited, corrected, enriched or re-typed in this vault.** It is transcribed with its provenance and left alone. Everything this estate adds hangs off it as a new node with a new edge.

**Two reasons, and the second is the operational one.** First, it is their data under their licence and modifying it while attributing it is dishonest. Second, **a snapshot that has been improved cannot be diffed against the live source**, so the moment we mutate we lose the ability to say what changed when they push.

---

## Namespaces, Which Are Also The Visual Classes

Three prefixes, and **they are never mixed in one node identifier**.

| Prefix | Origin | Rendered as | Meaning |
|---|---|---|---|
| `ung:` | **Derived** from UnGovr data | One visual class, labelled with attribution | Transcribed from their API. Never our judgement |
| `akn:` | **Anchored** to a published external identifier | A second visual class | Addressed in Akoma Ntoso terms, pointing at legislative text somebody else published |
| `sg:` | **Our model** | A third visual class | Asserted by this estate. Everything below the provision |

**Acceptance test 5 is the check on this**, and a partner will run it first: open the graph and it must be impossible to confuse a `ung:` node with a `sg:` node without reading the label. Colour alone is not enough — colour is already spent on the assertion classes below, so **the origin distinction must be carried by shape or border, not by hue.**

### And separately, the three assertion classes from the method site

Never mixed, and orthogonal to origin:

| Class | Means | Failure it prevents |
|---|---|---|
| **Asserted** | Someone stated it, and the bytes are cited | — |
| **Inferred** | Derived by a transformation this vault can name and rerun | An inference read as a fact |
| **Possible** | A hypothesis. Drawn, and drawn differently | **A hypothesis drawn like a fact, which is the failure this whole estate exists to prevent** |

---

## Node Types

### Derived from UnGovr (`ung:`)

| Type | Identifier | Carries |
|---|---|---|
| `ung:Entity` | Their published slug, verbatim | `name`, `type`, `country`, `state`, `population`, `website`, `children_count` |
| `ung:Boundary` | Entity slug + `#boundary` | GeoJSON as retrieved, unmodified |
| `ung:Domain` | The domain string | Verbatim |
| `ung:Membership` | The membership string | Verbatim |
| `ung:LawReference` | Entity slug + `#open_records.law` | **The law name exactly as they publish it.** Not normalised, not matched, not resolved |

**Note the last one.** `ung:LawReference` is a *string they published*, not a law. It is the near side of the join. Resolving it to an instrument is our inference and is modelled as such.

### Anchored to published identifiers (`akn:`)

| Type | Identifier | Carries |
|---|---|---|
| `akn:Instrument` | Akoma Ntoso FRBR work URI | Title, jurisdiction, enactment date, the retrieval that produced the text |
| `akn:Provision` | Two hashes (below) | Position, text, source byte range |

**Akoma Ntoso is the anchor, and this is settled before anything is minted.** It is the published standard for legislative text, it is in the standards site's covered set, and the August rule is to anchor to published identifiers rather than mint. **If a jurisdiction's law has no Akoma Ntoso rendering, that is recorded as an open item rather than solved by inventing an identifier scheme.**

### Our model (`sg:`)

| Type | Carries | Notes |
|---|---|---|
| `sg:Obligation` | What is required, of whom, within what interval, with what trigger | The first node that is entirely our judgement |
| `sg:Control` | What would satisfy the obligation | Descriptive, not prescriptive |
| `sg:Evidence` | A tier, a subject, an observation, a date | **Default state is `unevidenced`** |
| `sg:Acceptance` | A named owner, an interval, a revocation path | Carried in the vault and versioned |
| `sg:Retrieval` | Source URL, timestamp, method, response hash | Attached to every derived node |
| `sg:Inference` | The transformation that produced an edge, named and rerunnable | Attached to every inferred edge |

---

## Edge Types

```
   ung:Entity ──ung:parent──────────> ung:Entity
   ung:Entity ──ung:child───────────> ung:Entity
   ung:Entity ──ung:boundary────────> ung:Boundary
   ung:Entity ──ung:domain──────────> ung:Domain
   ung:Entity ──ung:membership──────> ung:Membership
   ung:Entity ──ung:openRecordsLaw──> ung:LawReference     ← their graph ends here
   ─────────────────────────────────────────────────────────────────────────────
   ung:LawReference ──sg:resolvesTo─> akn:Instrument       ← THE JOIN. Inferred
   akn:Instrument ──akn:hasProvision> akn:Provision
   akn:Provision ──sg:creates───────> sg:Obligation
   sg:Obligation ──sg:satisfiedBy───> sg:Control
   sg:Control ──sg:evidencedBy──────> sg:Evidence
   sg:Evidence ──sg:accepted────────> sg:Acceptance
   * ──sg:retrievedBy───────────────> sg:Retrieval         ← on every derived node
   * ──sg:inferredBy────────────────> sg:Inference         ← on every inferred edge
```

**One edge carries the whole argument and it is `sg:resolvesTo`.** It is the only edge in the diagram that crosses from their data into ours, it is **inferred rather than asserted**, and it must be rendered in the inferred class. A reader who thinks UnGovr asserted that resolution has been misled by the drawing.

---

## The Address Scheme: Two Hashes

Inherited unchanged from standards.sgit.ai. **A provision has two addresses because it has two kinds of identity, and conflating them is how citations rot.**

| Hash | Over | Answers | Changes when |
|---|---|---|---|
| **Position hash** | The canonical hierarchical path, normalised | *Which slot in the instrument is this?* | The instrument is restructured |
| **Content hash** | **The raw source bytes of the provision, unnormalised** | *Is this the same text I read before?* | A single byte of the text changes |

```
   akn:Provision
     position_hash  sha256( "akn:us-ca/act/cpra/sec-7922.535/(a)" )
     content_hash   sha256( <the exact bytes of that subsection as retrieved> )
```

**Why both.** An amendment that rewords a subsection leaves the position and changes the content, so a citation to the position still resolves and a claim resting on the wording is correctly invalidated. A renumbering does the reverse. **A single identifier cannot express that difference**, and a system with one hash silently picks which kind of change it is blind to.

**Normalisation rule, and it is asymmetric on purpose.** The position path is normalised — case folded, whitespace collapsed, numbering canonicalised — because it is a name. **The content bytes are never normalised**, because the hash's whole job is to be a hash of what was published. Normalising before hashing would mean the artefact cannot be checked against the source it claims to come from.

---

## Provenance Fields

**Every derived node and every quoted span carries all seven.** A node missing any of them fails verification rather than degrading quietly.

| Field | Example | Why |
|---|---|---|
| `source_url` | `https://data.ungovr.org/v1/entities/detail/{slug}.json` | Where to check it |
| `retrieved_at` | `2026-09-08T14:22:11Z` | **The minimum honesty on a snapshot of live data** |
| `method` | `HTTPS GET, no auth` | So a failed or degraded retrieval is visible as one |
| `response_sha256` | `sha256` of the raw response bytes | The artefact is checkable against the bytes it came from |
| `byte_range` | `[10412, 10598]` | Which part of the source produced this node |
| `licence` | `CC BY 4.0, UnGovr` | Attribution travels with the node, not with a page footer |
| `snapshot_release` | `@2026-09-08` | The release channel that pins this retrieval |

**The `method` field is doing real work and is not boilerplate.** A retrieval that went through a summariser, a transcription, or any lossy path records that here — and a node whose method is not a direct byte-preserving fetch **cannot carry a content hash**, because there are no source bytes to hash. See [`06__verification.md`](06__verification.md), where exactly this situation is recorded as the current blocker.

---

## The Two-Edge Rule, Applied

**Settled 4 September. Every node in this vault carries two mandatory edges before it carries anything interesting:**

1. **An origin edge** — who asserted this: UnGovr, a published standard, or us
2. **A provenance edge** — `sg:retrievedBy` for derived nodes, `sg:inferredBy` for inferred ones

**A node that cannot carry both is not added to the graph.** That is the constraint that makes the honest-label requirement mechanical rather than editorial: the model refuses to hold an unattributed node, so nobody has to remember to write the footnote.

**And the rendering follows from it**, which is the part a partner will check. Origin decides shape. Assertion class decides colour. Provenance decides what the node's detail panel opens.

---

## Claim States

**Every claim carries a state, and `unevidenced` is the default.** Settled in the 4 September conformance layer, applied here without modification.

| State | Means |
|---|---|
| `unevidenced` | **The default.** Nothing has been observed about this subject |
| `asserted` | Someone said so |
| `documented` | There is a document |
| `manually-checked` | A person looked |
| `programmatic-out-of-band` | Observed by a system that is not in the path of the thing observed |
| `programmatic-inline` | Observed by something in the request path |

**One limit stated plainly, because the temptation runs the other way.** This estate is out of band and can *evidence* any rung including the last. **It can never be the inline control that makes the last rung true.** A control bounds a grant only if it is enforced by something the grant does not include, and an out-of-band party is never that enforcer. A page that blurs those two is claiming the one thing the architecture rules out.

---

## What This Model Deliberately Does Not Do

| Not done | Why |
|---|---|
| Mint an identifier for a jurisdiction | Their slugs are the anchor. That is the entire reason this vault is worth building |
| Normalise their law reference strings | It is their published value. Normalisation is an inference and is modelled as one |
| Publish a formal OWL/RDF ontology | The method site says its semantic layer is designed rather than shipped, and that honesty survives here |
| Model more than one instrument | One properly beats forty sketched |
| Assert anything about a subject's compliance | The conformance layer holds what a standard says apart from what a subject does |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

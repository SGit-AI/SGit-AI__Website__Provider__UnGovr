# 03 — The Worked Example: One County, One Law, One Acceptance

**version** v0.33.67
**date** 8 September 2026
**status** Specified, not built. Every value marked *pending retrieval* is a slot, not a claim.

[← 02 The Model](02__the-model.md) · [Pack hub](README.md) · Next → [04 The Vault](04__the-vault.md)

---

## This Is The Deliverable

**Everything else in this pack exists to make this one path defensible.** If you read one file, read this one.

The path runs from a real government entity, resolved from a slug somebody else publishes, to a named person who accepted a residual risk — and at every step you can see the bytes it came from and the date they were retrieved.

---

## The Choice, And Why

| Slot | Choice | Why this one |
|---|---|---|
| **County** | **Santa Barbara County, California** | It is the city behind **their own published measurement**: 40.7 per cent of addresses written "Santa Barbara, CA" fall outside the city limits. The example lands on ground they have already done fieldwork on, which makes it a compliment rather than a probe |
| **Instrument** | **The California Public Records Act** | It is the records law their `open_records.law` edge points at for Californian bodies, so the join is against a reference they actually publish rather than one we chose |
| **Acceptance** | One, named, with an interval and a revocation path | Because an acceptance without an owner is a note |

**And a secondary reason for California that matters for step 1.** Their own depth claim is that Californian special districts outnumber cities by more than ten to one, and that layer below city hall is what nobody else maps. **The overlapping-jurisdiction stack for a Santa Barbara address is therefore the richest available demonstration of the one thing only they can do.**

**Refuse to widen it.** Not all 58 counties. Not all 398 records laws. Not the transparency corpus as well. One.

---

## The Seven Steps

```
   1  ENTITY        a real UnGovr slug, fetched live, with its boundary
                    and its published law reference
                          |
   2  INSTRUMENT    that records law, rendered as addressable provisions:
                    two-hash addressing, source bytes hashed,
                    retrieval source and timestamp recorded
                          |
   3  PROVISION     one clause. The one that creates a duty
                          |
   4  OBLIGATION    what it requires, of whom, within what interval
                          |
   5  CONTROL       what would satisfy it
                          |
   6  EVIDENCE      at a stated tier, with unevidenced as the default
                          |
   7  ACCEPTANCE    a named owner, an interval, a revocation path,
                    carried in the vault and versioned
```

**Steps 1 and 2 are the join that does not exist today. Steps 3 to 7 are the chain this estate already has.**

---

### Step 1 — Entity

**Produces**: one `ung:Entity`, one `ung:Boundary`, one `ung:LawReference`, one `sg:Retrieval`.

| | |
|---|---|
| Source | `GET /v1/entities/us/ca.json`, then `GET /v1/entities/detail/{slug}.json` |
| Slug | **Pending retrieval.** Do not guess it. Resolve it from their index and transcribe it verbatim |
| Boundary | `GET /v1/entities/boundaries/{slug}.geojson`, stored unmodified |
| Law reference | `open_records.law`, **transcribed as the exact string they publish** |
| Rate limit | 100/day per IP on entity data. The whole of step 1 is three calls |

**The discipline here is the whole vault in miniature.** The slug is not normalised. The GeoJSON is not simplified. The law string is not matched to anything yet. Three files land in the vault with their retrieval metadata and nothing else happens to them.

**Acceptance test 1** is satisfied when the named entity resolves from its published slug and its boundary renders.

---

### Step 2 — Instrument

**Produces**: one `akn:Instrument`, N `akn:Provision` nodes, one `sg:Retrieval`, and **one `sg:Inference` for the resolution edge**.

This is the join. It has two halves and they must not be confused with each other.

**Half one, the resolution.** `ung:LawReference` → `akn:Instrument`, via `sg:resolvesTo`. **This edge is inferred, not asserted**, and it carries the transformation that produced it — a documented, rerunnable match from their published string to an Akoma Ntoso work URI. **UnGovr did not make this claim and the graph must not draw it as if they did.**

**Half two, the rendering.** The instrument's text is decomposed into addressable provisions by the method already used twice, for GDPR and for the EU AI Act. Section, block, sentence. Two hashes per provision. SHA-256 of the source bytes. Retrieval source, timestamp and method on each.

| Requirement | From |
|---|---|
| Two-hash addressing | standards.sgit.ai, unchanged |
| SHA-256 of source bytes | standards.sgit.ai, unchanged |
| **The markdown rebuilds from the graph byte for byte** | graphs.sgit.ai. **This is acceptance test 3 and it is not optional** |
| Quotes verified byte by byte on build | graphs.sgit.ai |

**One open item to settle before building**, and settling it is cheap: whether the CPRA has an Akoma Ntoso rendering, or a published XML source of comparable quality. The EU AI Act had Formex, which is why that vault was tractable. **If Californian statute is only available as HTML, the decomposition is harder and the byte-hash claim is weaker, and that must be said in the vault rather than discovered by a reader.** Record the answer in `06__verification.md` before writing any parser.

---

### Step 3 — Provision

**Produces**: one `akn:Provision` promoted to the spine of the example.

**One clause. The one that creates a duty.** The candidate is the CPRA's response-interval provision — the ten-day determination requirement, at **Gov. Code § 7922.535** in the 2023 recodification, formerly § 6253(c).

> **Pending retrieval.** That citation is written here from prior knowledge and is therefore `unevidenced` under this vault's own rule. It is a *candidate to verify*, not a fact to publish. The provision that ships is whichever one the retrieved bytes actually carry, and if the section number differs the pack is wrong and the bytes are right.

**Why an interval clause is the right choice.** It creates a duty with a measurable trigger and a measurable deadline, which means step 6 can distinguish evidence tiers meaningfully instead of collapsing into "there is a policy document".

---

### Step 4 — Obligation

**Produces**: one `sg:Obligation`. **The first node that is entirely our judgement**, and the graph must say so.

| Field | Content |
|---|---|
| Requires | A determination on whether the request seeks disclosable records |
| Of whom | The agency named at step 1 |
| Within | The interval the provision states |
| Triggered by | Receipt of a request |
| Derived from | The `akn:Provision` at step 3, by `sg:creates` |

**The honest label lives on this node**, not in a footnote at the bottom of a page. Everything from here down is our model applied to their data. That is acceptance test 5, and it is the thing a partner checks first.

---

### Step 5 — Control

**Produces**: one `sg:Control`.

What would satisfy the obligation: a logged intake with a timestamp, a determination recorded against it, and a clock that can be measured. **Descriptive, not prescriptive.** The vault says what would satisfy the duty; it does not tell a county what to buy.

---

### Step 6 — Evidence

**Produces**: one `sg:Evidence` node, **whose state is `unevidenced` unless something was actually observed.**

| Tier | What it would mean here |
|---|---|
| `unevidenced` | **The default, and the honest state for this example unless a real observation exists** |
| `asserted` | The agency says it responds in time |
| `documented` | There is a published policy |
| `manually-checked` | Someone read a sample of responses |
| `programmatic-out-of-band` | A system that is not in the path measured the interval |
| `programmatic-inline` | Something in the request path measured it |

**Two disciplines apply and both are load-bearing.**

The first: **this estate can evidence any rung and can never be the inline control that makes the last rung true.** An out-of-band party establishes whether an enforcer exists, at what tier, and with what left unobserved. It is not the enforcer.

The second: **the grand jury corpus is an evidence source already structured for this.** Findings and recommendations arrive as objects with a number, the text and a **page number** — provenance to the page, which is stronger than most compliance tooling manages. A Santa Barbara County grand jury finding about records handling would attach here at `documented` or `manually-checked`, under the evidence-pack rule of 9 August: **a pack attaches, adds nodes and edges, and never alters what it attaches to.**

> **Note the constraint.** `/cgj/reports/{id}.json` is key-gated at 50/day. The county index is open and unlimited. See [`06__verification.md`](06__verification.md) for the access status, which is currently unresolved.

---

### Step 7 — Acceptance

**Produces**: one `sg:Acceptance`, carried in the vault and versioned.

| Field | Why it is mandatory |
|---|---|
| **A named owner** | An acceptance without a name is a note |
| **An interval** | An acceptance without an expiry is a permanent decision taken casually |
| **A revocation path** | An acceptance nobody can withdraw is not a decision |
| The residual it accepts | Stated as the gap between the control and the obligation |
| The commit it was made at | Because the acceptance is only meaningful against a stated version of the facts |

**This is the node that only a vault can carry properly**, and it is the reason the demonstration is a vault rather than a slide. It is versioned, it is addressable by release, and the state of the world it was made against is pinned to a commit rather than remembered.

---

## The Two Properties That Must Hold Visibly

**They are the argument. They are not decoration.**

**One — every node traces to bytes somebody else published, with the retrieval date.** Not "sourced from UnGovr". A URL, a timestamp, a method, a byte range, a hash.

**Two — the whole path is deterministic.** Given the entity slug and the instrument, the same nodes come back, **because the addressing is by content hash rather than by position in a list that may be reordered.** That is acceptance test 7, and it is the reason to build any of this.

**And the determinism claim has a stated limit**, which belongs in the vault rather than in a defence of it: it holds only while both address schemes are stable. Theirs is a slug they maintain; ours is a hash of bytes. If they re-slug, the join breaks loudly, which is the correct failure mode.

---

## What Ships At The End Of This

| Artefact | Form |
|---|---|
| The seven nodes above, with their edges | A graph the viewer opens |
| Three retrieved JSON files, unmodified, with hashes | The bytes, checkable |
| The instrument's provisions, addressable | Reusable beyond this example |
| A page stating the path in prose, with every number beside its query | Because a number without its query is an assertion |
| A release pinning the whole thing to a date | So it can be cited |

**One county. One law. One acceptance. And a refusal to widen it.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

# 05 — Integration

**version** v0.1 · 9 September 2026

[← 04 The worked example](04__the-worked-example.md) · Next → [06 Verification](06__verification.md)

---

## What each existing thing gains, and what it gives

**Every row is read from that vault's or site's own published page**, linked, and quoted rather
than recalled.

## Licence to Operate — `posrhzp3`

**What it is.** An agent's grant, its mandate, and the delta between them, priced. **12
capabilities can do, 4 may do, 8 in the delta** — *"inside the agent's reach, outside its
authority. No policy covers these."*

**What it gains from the anchor.** A `policy/v1` covering an agent acting **for a body, in a
jurisdiction** currently has no way to name either. With the anchors, the mandate stops being
*"answer a customer's question"* and becomes *"answer a records request on behalf of
`ung:us/ca/santa-barbara`, under `us/ca`, within the statutory 10 days"* — **a mandate with a
deadline that came from a legislature rather than from a product decision.**

**What it gives back.** The delta. Our graph has no way to express *the agent could reach this
obligation's evidence and is not authorised to*, and that is the sharpest thing in their model.

## The AIUC-1 conformance layer — `2wzct4k7`

**What it is.** 53 conformance rows for a named subject where `unevidenced` is the default, and
**insurability computed as a query** — 1 condition met, 52 exclusions at build, **53 exclusions
when the date moves to 2027-01-15 with nothing edited by anybody**.

**What it gains.** *Subjects*, with stable ids. Today a conformance run names its subject as a
string, so two runs cannot be compared and none can be aggregated. **With `ung:entity` the subject
is a node**, and *"how many bodies in this jurisdiction have an unevidenced control here"* becomes
a query rather than a spreadsheet.

**What it gives back — and this is the one to steal.** Their `valid_until` mechanism, where **time
alone turns conditions into exclusions.** We contribute a second clock: theirs expires because an
*attestation* lapsed, ours because a *statute* says 10 calendar days. **An attestation expiry is a
parameter somebody chose. A statutory deadline is a fact about the world.** A model carrying both
is strictly better than one carrying either.

## Risk Mandate — `4zf6pf2z`

**What it is.** A working application delivered as a vault — 124 files, 98 commits, eight entry
points, pinned releases — that **calls an LLM without ever holding the API key.**

**What it gains.** A register assembled for a *named body in a named jurisdiction* rather than for
a scenario. The eight questions stay; what changes is that the answers hang off an anchor and can
be compared with somebody else's.

**What it gives back.** The delivery pattern, and the honest one: an app in a vault, offline once
cached, with `takeaway.html` rebuilding a saved register from the link alone. **This vault already
copied that shape** — index.html, data as its own cached immutable object, no permissions.

## eu-ai-act.standards.riskmandate.ai

**What it is.** The composed current text of Regulation (EU) 2024/1689 with the Digital Omnibus
applied by a deterministic gated parser, **published so it can be checked**: per-provision ids and
sha256 rolling to a root hash, `.md` and `.llm.json` on every slug, JSON-LD and Turtle exports,
and a manifest hashing every file. It states plainly that it is **derived and not authentic law.**

**What it gains.** Almost nothing — and that is the point. **It is the layer this pack needs and
does not have to build.** Step 2 of the work order is a join, not a parse.

**What it gives.** The standard every other instrument in this graph should be held to. Set beside
the CPRA — where the operative clause is prose in a notes field — it is the clearest possible
statement of what *addressable* means, and it is why [the worked example](04__the-worked-example.md)
puts the two side by side.

**And the honesty to copy.** It says on its own front page that only the Official Journal is
authentic, and it publishes a root hash so a reader knows exactly which version they read. **Our
inferred edges deserve the same treatment, and get it.**

## The graph family — `graphs.sgit.ai`

**What it is.** The grammar this pack obeys: nine sentences, five rules, fifteen edges with named
inverses, and the instruction to bridge rather than merge.

**What it gains.** A worked instance of anchor nodes with a **measured** bridge — 96.6% reach,
20.5% needing a human. The site argues that confidence is computable; this is a case where
somebody computed it and published the part that does not work.

## The composite question this makes answerable

None of the vaults above can answer this today. Together, with the anchors, they can:

> *For this body, in this jurisdiction: which obligations bind it, which standard controls address
> each, what is the evidence state of each, what would an insurer exclude — and which of those
> links did we infer rather than read?*

**Every clause of that question maps to one layer**, and the last clause is the one that keeps it
honest.

## What integration must not do

| Not this | Because |
|---|---|
| Merge the vocabularies into one control set | Merging erases the disagreement. **Bridge through anchors** |
| Import UnGovr's AI-law corpus into any of these vaults | **It is not CC BY 4.0.** Its own licence conveys none |
| Draw a crosswalk and leave who drew it implicit | A crosswalk without an author is an assertion nobody owns |
| Generate an acceptance owner to make a demo look finished | An acceptance without an owner is a note, and a generated one is worse |
| Treat 96.6% as 100% because it rounds nicely | The 20.5% that needs a human is the whole reason the edge is inferred |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

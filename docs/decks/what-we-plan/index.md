---
deck: What we plan to build
subtitle: The security-standards graph — specified, nothing built, and honest about which
date: September 2026
accent: teal
---

# What we plan to build

> **Deck 4 of 6.** The dev pack, in ten slides: the gap, the design, and the four things that
> could still make it wrong.
>
> The pack itself is eight files in `packs/security-graph/`, republished on the site at
> `/packs/security-graph/`. This is the markdown source of the deck; the **Decks** view is a
> projection of it, and if the two disagree this one is right.

---

## Every standard says what good looks like. **None says who has to do it.**

A control says *maintain an audit log*. It does not say **Santa Barbara County must, under
Gov. Code § 7922.535(a), within 10 calendar days.**

The obligated party and the jurisdiction that binds it are the two node classes every standards
graph gestures at, and none of them identifies.

UnGovr publish **327,138 identified bodies** and **398 jurisdiction-keyed laws**. Those are the
anchor nodes our graphs are missing.

> **Notes.** This is the entire pitch in three sentences. If you say nothing else, say this. The
> gap is not in their data and not in the standards — it is between them, and it is one edge.

---

## The number that carries the argument

AIUC-1's conformance vault holds **1,126 crosswalks** from its controls out to **489 distinct
control items across thirteen frameworks.**

**Ninety-five of those crosswalks point at law** — EU AI Act 62, Colorado AI Act 18,
California SB 53 9, NYC Local Law 144 6.

**Three of the four laws are sub-national United States jurisdictions.**

> **Notes.** Counted from graph/edges.json in vault 2wzct4k7, not read from its prose. A
> crosswalk ending at "the Colorado AI Act" is a statement about a text, not about which bodies
> in Colorado it binds. UnGovr's Atlas is keyed on exactly that axis.

---

## Two findings from opening their vault, and the second changed the pack

**One: all thirteen frameworks are AI-specific.** No NIST CSF, no 800-53, no ISO 27001 or 27002,
no SOC 2, no CIS, no PCI DSS. That is the right scope for an agent standard — and it means the
general-security half of the map is **absent from this estate**.

**Two: they already use `anchor:` nodes**, reached by an `anchors_to` edge, 489 of them.

> **Notes.** The second finding forced a rewrite. File 01 had implied the estate had not applied
> the anchor pattern. It had. So the pack proposes a different AXIS of anchor — theirs anchor
> provisions across standards, ours would anchor obligations to the body and the place — rather
> than proposing the mechanism. Two anchor axes compose; they do not compete.

---

## One label had to be read rather than trusted

One of the thirteen is labelled **"OWASP Top 10"**, which reads as the web application list —
a general security artefact. If it were one, the finding above would be wrong.

Its members are `LLM01:25 Prompt Injection` through `LLM10:25 Unbounded Consumption`: the
**OWASP Top 10 for LLM Applications.**

**The finding survives only because the members were listed instead of the label believed.**

> **Notes.** A shorthand that collides with a different, better-known standard is exactly what an
> anchor node exists to disambiguate. Worth reporting upstream rather than working around.

---

## Where the rabbit hole actually stops

Follow the evidence to a law and UnGovr hands you a **structured summary in JSON** — 31 to 34
fields — and **a link to the official publisher**, on 392 of 398 laws across 339 hosts.

What it does not hand you: **the text**, in any format. `.md` `.html` `.txt` `.pdf` `.jsonld`
`.ttl` all 404, and `Accept:` headers return **byte-identical** responses.

**And 254 of the 398 laws — every sub-national one — have no reachable detail document at all.**

> **Notes.** 24 of 24 sub-national slugs returned 404 against 26 of 26 national ones at 200. The
> jurisdiction carries a slash and the route is a single path segment. Sub-national is where the
> variation lives, and it is exactly the half the crosswalks point at.

---

## The rule the whole design rests on

> **Don't merge vocabularies — merging erases the disagreement. Keep them intact and bridge them
> through anchor nodes.**

*graphs.sgit.ai, thesis sentence 6*

Merging UnGovr's entity vocabulary into a standards vocabulary would destroy both. Bridging them
costs **one node class and one edge**.

> **Notes.** This is inherited, not invented, and it is why the pack proposes two anchors —
> ung:entity and ung:jurisdiction — rather than a schema everyone must adopt.

---

## Fifteen edges, and the four that caught us out

Every edge is a verb with a **distinct inverse**. Six come from graphs.sgit.ai's established set,
four from the AIUC-1 conformance layer, **five are proposed here and marked as proposed**.

The pack originally said eight were *reused unchanged*. **Four of the six had been quietly
renamed** — `observed_on` given the inverse `observation_of` where the published set says
`bears_observation`.

**Renaming another vocabulary's inverses and calling it reuse is a fork.**

> **Notes.** Caught by fetching the published edge set and comparing row by row, not by rereading
> our own table. It is the exact failure rule 6 exists to prevent, committed by the file that
> states the rule. The four are now theirs.

---

## What we would supply, and what we would not

| They supply | We supply |
|---|---|
| The instrument, found and summarised, with its publisher URL | Parsing it into provisions, each with a hash |
| 254 sub-national jurisdictions, identified and slugged | The anchor binding a body to a place |
| A controlled vocabulary — 22 fields, 17 enums | Edges with named inverses |

**None of it requires their corpus to be redistributed**, which matters because part of it
cannot be.

> **Notes.** The AI-law corpus licence says "No license is conveyed by receipt of this file". The
> graph can carry the anchor, the hash and the link, and leave the text where its licence
> requires it to stay. We have built the parsing half twice already — Regulation Graph from
> Formex, and the EU AI Act current text with a sha256 per provision.

---

## The state of it: nothing is built, and the tests say so

**Thirteen acceptance tests. Five pass — and all five are inherited** from work this vault had
already done. One is `asserted`. **Seven are `unevidenced`.**

Four blockers are open. One, S1, closed on the day it was written by doing what the pack said to
do first.

> **Notes.** This slide is the point of the deck. A specification published before its
> implementation, with the count of what it has not earned, is checkable against whatever gets
> built. The count itself was wrong first time — it said "two of twelve" — and was caught by
> parsing the table with a script rather than reading it.

---

## What would make this wrong

**S3 is the one that kills it.** If UnGovr's entity ids churn between releases, the anchor thesis
fails and nothing else in the pack survives. **It is unmeasured.** Two snapshots, compared, is
the next cheapest thing to do.

**S4:** if a standards body already publishes machine-readable jurisdiction scope, their binding
replaces our inference and should.

**S5 is not closeable by us:** the AI-law corpus cannot be redistributed.

> **Notes.** End here rather than on a roadmap. The pack's own rule is that every claim carries a
> state and the default is the weakest one — that applies to the pack about itself. Nobody should
> leave this deck thinking any of it is built.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

# 00 — README: The Government Graph Pack

**version** v0.33.67
**date** 8 September 2026
**status** PROPOSED. Nothing described in this pack is built. This pack is the first commit in the vault, published before the work it specifies, which is the point.

[Pack hub](README.md) · Next → [01 — What Exists](01__what-exists.md)

---

## The Argument, In One Paragraph

UnGovr publishes an excellent graph of government: roughly 320,000 entities across 205 countries, with hierarchy, boundaries, and a spatial join that resolves an address into every overlapping jurisdiction. Each entity carries one edge to the open-records law that governs it, **and then stops.** A consumer can learn *which law applies* and can never point at *the clause that requires anything*. So a claim built on their data can be about a jurisdiction and never about an obligation — and an obligation is the only thing that can carry a risk, a control or an acceptance. **This vault closes that gap for one worked example**, one county and one law and one acceptance, and shows what the data would need in order to be usable at scale.

**This is not a criticism.** That edge is exactly right for their stated purpose, which is helping a person reach their government. It is one hop short of the purpose everybody downstream has.

## Reading Order

| # | File | Read it for |
|---|---|---|
| 00 | `00__README.md` | This file. The argument, the scope, what not to rebuild |
| 01 | [`01__what-exists.md`](01__what-exists.md) | The assembly inventory. What is already published on both sides |
| 02 | [`02__the-model.md`](02__the-model.md) | The ontology: node types, edge types, addressing, provenance, the two-edge rule |
| 03 | [`03__the-worked-example.md`](03__the-worked-example.md) | Santa Barbara County, the CPRA, one acceptance. The seven steps |
| 04 | [`04__the-vault.md`](04__the-vault.md) | The vault's own shape: the team, the viewers, the graph settings, the release channel |
| 05 | [`05__the-workbench.md`](05__the-workbench.md) | The bulk pipeline, the compiled artefacts, the browser database, the seven computations |
| 06 | [`06__verification.md`](06__verification.md) | The acceptance tests, the claim-state rule, and the blockers recorded honestly |

**If you read one file, read 03.** It is the deliverable. Everything else exists to make it defensible.

## What Is Already Built And Must Not Be Rebuilt

This is the finding that should set the size of the work. **The demonstration is assembly plus one new join, not a build.**

| Already published | Where | Do not rebuild |
|---|---|---|
| A law rendered as a semantic graph with a contribution path | Standards Atlas (GDPR) vault | The pattern for law-as-graph |
| A law parsed from official XML into an evidence graph, article by article | Regulation Graph (EU AI Act) vault | The parse-to-provision pipeline |
| A conformance layer computing a judgement over a graph of requirements | AIUC-1 vault | The requirement → subject → evidence separation |
| A public graph app whose `app.json` requests no permissions | Risk Graph Explorer vault | The shareable read-only form |
| SQLite in the browser over an eleven-step acceptance walk | The published risk-acceptance vault | The in-browser query pattern |
| An instrument at 1,523 nodes and 1,944 edges with two-hash addressing | standards.sgit.ai v0.1.4 | The addressing scheme |
| Byte-for-byte rebuild of source from graph, quotes verified on every build | graphs.sgit.ai | The provenance discipline |

**What is new is exactly two things**: the entity-to-instrument join (steps 1→2 of the worked example), and the coverage measurement of UnGovr's own law edge. Everything below step 2 has been done twice for other instruments.

## The Success Criterion

**One sentence.** A stranger opens a link, sees a named real government entity resolved from a published slug, follows it to a clause of an actual law, sees the obligation that clause creates, sees what would satisfy it, sees at what evidence tier, sees who accepted the residual risk — and at every node can see the bytes it came from and the date they were retrieved.

**And the negative criterion, which is the one that will be checked first.** At no point can a reader confuse a node that came from UnGovr's data with a node that is our model. See [`02__the-model.md`](02__the-model.md), the two-edge rule.

## Scope: One County, One Law, One Acceptance

**Santa Barbara County, California. The California Public Records Act. One acceptance.**

Santa Barbara because it is the city behind UnGovr's own published measurement — that 40.7 per cent of addresses written "Santa Barbara, CA" fall outside the city limits — so the example lands on ground they have already done fieldwork on. The CPRA because it is the records law their entity edge points at for Californian bodies.

**Refuse to widen it.** Every reader of this pack will want to model all 398 records laws, or all 205 countries, or the whole entity graph. **One instrument modelled properly beats forty sketched**, which is the standards site's own conclusion about itself after a year of work. A pack that tries to be a complete ontology of government ships nothing.

## What This Pack Does Not Cover

| Not covered | Why |
|---|---|
| A complete ontology of government | One county, one law, one acceptance, and a refusal to widen it |
| Modelling their domain better than they do | They know government structure. The contribution is the layer below the law reference |
| A replacement for their API | The vault holds a dated snapshot and points at the live source |
| A graph database pitch | The method site says of itself that its semantic layer is designed rather than shipped. That honesty survives into this vault |
| A partnership, or any claim about what UnGovr wants | No conversation has happened. Every statement about their needs is inference from what they publish |
| The insurance chain | Three steps down from anything they do, and it is not the conversation |

## Tone

**This vault may be shown to the organisation whose data it uses.** Write everything in it as a contribution offered, not a gap exposed. The missing edge is right for their purpose and short for ours, and both halves of that sentence must survive into every file.

**And do not overclaim the semantic layer**, in either direction. What is shipped is shipped; what is designed is labelled designed.

## Attribution

Entity data, slugs, boundaries and law references originate with **UnGovr** and are used under **CC BY 4.0** with attribution. This vault holds a dated snapshot and is not a replacement for their live source at `data.ungovr.org/v1`.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

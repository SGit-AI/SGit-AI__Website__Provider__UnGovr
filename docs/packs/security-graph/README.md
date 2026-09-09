# The Security-Standards Graph — a dev pack

**version** v0.1 · 9 September 2026 · **status: specified, nothing built**

[🏠 Vault index](../../README.md) › [Packs](../README.md) › **Security graph**

---

**Every security and AI standard tells you what good looks like. None tells you who has to do it,
or where.** UnGovr publish 327,138 identified bodies and 398 jurisdiction-keyed laws — the anchor
nodes our standards graphs are missing. This pack specifies how to connect them **without merging
a single vocabulary.**

| # | File | Holds |
|---|---|---|
| 00 | [Start Here](00__START-HERE.md) | The argument, the strict order, what is already decided |
| 01 | [The anchor-node thesis](01__the-anchor-node-thesis.md) | Why bridging beats merging, in graphs.sgit.ai's own words |
| 02 | [The model](02__the-model.md) | Five node classes, fifteen edges with named inverses, provenance fields |
| 03 | [The standards map](03__the-standards-map.md) | What exists as a graph, what does not, and the honest state of each |
| 04 | [The worked example](04__the-worked-example.md) | **The deliverable.** One control, one body, one jurisdiction |
| 05 | [Integration](05__integration.md) | Licence to Operate, AIUC-1 conformance, Risk Mandate, the EU AI Act text |
| 06 | [Verification](06__verification.md) | Thirteen tests, five blockers — one closed — and what would make this wrong |

## The cheapest thing to do first — done, 9 September

This said: **open AIUC-1's vault and read which thirteen frameworks its 1,126 crosswalks point
at.** It was done the same day, and it changed the pack rather than confirming it. All thirteen
are AI-specific — **no general security control set among them** — four are laws, three of those
sub-national US, and the estate already uses `anchor:` nodes (489 `anchors_to` edges), so file 01
was corrected to propose a different *axis* rather than the mechanism. Blocker S1 is closed and
[03](03__the-standards-map.md) carries the working.

**The next cheapest thing** is S3: compare two UnGovr snapshots and measure whether entity ids are
stable. If they churn, the anchor thesis fails, and no amount of the rest of this pack survives it.

## Published before the work

Nothing here is built. **Five of thirteen acceptance tests pass and all five are inherited** from
what this vault already did on the government side — one more is `asserted` and seven are
`unevidenced`. The pack ships first so it can be checked against
whatever gets built, which is the method this estate argues for, applied to itself.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

# 06 — Verification

**version** v0.1 · 9 September 2026

[← 05 Integration](05__integration.md) · [00 Start Here](00__START-HERE.md)

---

## The rule this file enforces

**Every claim carries a state, and the default is the weakest one.** That applies to this pack
about itself: **nothing it specifies is built**, and the status column below says so.

## The acceptance tests

| # | Test | Why it exists | State |
|---|---|---|---|
| 1 | A named body resolves from its published slug, and the jurisdiction it is `governed_by` resolves too | The anchor is real rather than illustrated | **`programmatic-inline`** — inherited. Done in this vault |
| 2 | The `governed_by` edge is drawn `inferred` everywhere, and its measured reach and its needs-a-human share ship beside it | **UnGovr do not make this claim** | **`programmatic-inline`** — inherited. 96.6% / 20.5% |
| 3 | A standard's control is forked **byte for byte**, and a test proves the fork is identical to its source | The AIUC-1 layer's own discipline, applied to us | `unevidenced` |
| 4 | The `addresses` edge names who drew it, and ours are `inferred` | A crosswalk without an author is an assertion nobody owns | `unevidenced` |
| 5 | A query traversing `evidenced_by` and `attested_by` **names which it used**, and a test goes red if a layer edge reaches a source observation | Taken whole from the conformance layer | `unevidenced` |
| 6 | `unevidenced` is emitted for every control in scope, whether or not anyone looked | **An absent row must never read as compliance** | `unevidenced` |
| 7 | Origin is carried by shape and assertion class by colour, and neither borrows the other's channel | The thing a reader checks first | **`programmatic-inline`** — inherited. The app does this |
| 8 | Every node claiming a retrieved source carries `response_sha256` and a retrieval date; every node that is ours carries a note instead | A hash nobody earned is worse than no hash | **`programmatic-inline`** — inherited |
| 9 | No whole-graph render exists anywhere in the app | *Never render the whole graph — render the result of a query* | `unevidenced` |
| 10 | Every proposed edge has a sentence, an inverse with a **different** sentence, a domain and a range | The grammar's own rule for extending the set | **`asserted`** — the five proposed in [02](02__the-model.md) each do; not yet tested |
| 11 | No standard's text is redistributed where its licence forbids it, and the check runs over the whole tree | **This vault learned this the expensive way** | **`programmatic-inline`** — inherited. `check_no_restricted_corpus` |
| 12 | The composite query in [05](05__integration.md) returns an answer, and the answer names which links were inferred | The reason to build any of this | `unevidenced` |
| 13 | The estate's existing anchor pattern (`anchors_to`, 489 edges in AIUC-1) is **reused rather than reinvented** | Discovered while closing S1. Two anchor axes must compose, not compete | `unevidenced` |

**Five of thirteen pass, and all five are inherited** from work already done in this vault rather
than earned by this pack. One more (10) is `asserted`; the remaining seven are `unevidenced`. That
is the honest state of a specification published before its implementation.

> **This line said *two of twelve* until 9 September.** Both numbers were wrong: test 13 was added
> when S1 closed and the total was never moved, and three rows had been marked
> `programmatic-inline — inherited` after the count was written. It was caught by counting the
> table with a script rather than reading it, which is the only reason it was caught at all — and
> it is the same failure mode this pack warns about in [03](03__the-standards-map.md), where a
> framework's label had to be checked against its members. **A summary of a table drifts from the
> table.** The count is now derived by parsing the rows.

## Blockers

| # | Blocker | Closes when |
|---|---|---|
| ~~**S1**~~ | ~~AIUC-1's thirteen crosswalk targets are not known here~~ | **CLOSED, 9 Sep**, by doing what this pack said to do first. They are AI-specific — **no general security control set among them** — and four are laws, three of those sub-national US. Counted from `graph/edges.json` in vault `2wzct4k7`. See [03](03__the-standards-map.md) |
| **S2** | The licence position of every candidate standard is unknown | Each is checked **before** its text is parsed, never after |
| **S3** | Entity id stability across UnGovr releases is unmeasured | Two snapshots are compared. **If ids churn, the anchor thesis fails** |
| **S4** | No standards body is known to publish machine-readable jurisdiction scope | Somebody looks. If one does, their binding replaces our inference |
| **S5** | The AI-law corpus, which carries jurisdiction-level AI-law verdicts, **cannot be redistributed** | Not closeable by us. It is described and measured, never stored |

## What would make this pack wrong

**Stated in advance, because a specification that cannot be refuted is not one.**

| If this turns out to be true | Then |
|---|---|
| ~~AIUC-1 already crosswalks most of the candidate list~~ | **Checked and false.** The general-security half is absent. But a second prediction *did* land: AIUC-1 already uses `anchor:` nodes and an `anchors_to` edge, so this pack does not introduce the pattern — it proposes a different axis for it, and [01](01__the-anchor-node-thesis.md) says so |
| UnGovr entity ids are not stable between rebuilds | **The anchor thesis fails outright.** Everything here depends on it |
| A standards body publishes its own jurisdiction bindings | Ours are deleted in favour of theirs, and the pack is better for it |
| Practitioners need the merged control vocabulary after all | Then merging belongs in a layer *above* the bridge, and the bridge still has to exist first |
| The `addresses` edge turns out to be many-to-many and unstable | Likely. **It is why exactly one is drawn by hand in the worked example** before any of it is automated |
| The two EU AI Act graphs in this estate disagree | **Publish the disagreement.** Two independent parses of one law diverging is a finding |

## Honest tensions

| Tension | Note |
|---|---|
| A graph that spans regulation and standards invites being read as compliance advice | It is not. Every layer states what it does **not** prove, borrowed from the conformance layer's own field |
| The anchor is somebody else's data, and it can move | It is a dated snapshot with a hash, and the live source is named. **Stale and honest beats fresh and unattributed** |
| Inferring `governed_by` at 96.6% is useful and 20.5% of it needs a human | Both numbers ship together, always |
| This pack cites five vaults and two sites it did not build | Which is the argument. **The value is the connective tissue, not re-typing corpora that exist** |
| Nothing here is built | **And the pack is published before the work anyway**, which is the method this estate argues for, demonstrated on itself |

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

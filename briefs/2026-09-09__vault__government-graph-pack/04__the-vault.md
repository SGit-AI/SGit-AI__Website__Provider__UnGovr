# 04 — The Vault: Team, Viewers, Settings, Releases

**version** v0.33.67
**date** 8 September 2026

[← 03 The Worked Example](03__the-worked-example.md) · [Pack hub](README.md) · Next → [05 The Workbench](05__the-workbench.md)

---

## Why The Vault's Own Shape Is Part Of The Argument

**A vault demonstrating how to operate a graph must be operable in the way it describes.** If the team is real, the viewers work, and the demonstration can be cited by version, then the method is shown rather than asserted. If any of those is a diagram in a document, the vault is a slide deck with a URL.

---

## The Agentic Team

**The house model, unchanged: agents never address each other and coordinate through file artefacts.** An issue is a *contract between roles* rather than a to-do item. A session finishes by writing a handoff and exiting; the next role starts fresh and picks it up.

**Four roles, and no more.** Their instructions live in the vault as ordinary files at [`/team/`](../team/README.md), so a clone carries the team.

| Role | Owns | Writes to | Reads |
|---|---|---|---|
| **Cartographer** | The graph. Node and edge construction, the join, the viewer | `/graph/`, `/app/` | Everything |
| **Librarian** | Provenance, retrieval log, attribution, the catalogue entry | `/provenance/`, `/catalogue/` | Everything |
| **Architect** | The schema and the model. Owns [`02__the-model.md`](02__the-model.md) | `/pack/02__*`, `/schema/` | Everything |
| **Reviewer** | Contradiction. **Commissioned to contradict, not instructed to be critical** | `/review/` | Everything |

**The cartographer leads on this vault.** The role exists in the house model and has previously been a reviewer; here it is the lead, which is a first and worth noting when the handoffs are read later.

### The single-writer rule

**No file has two writers.** Generated files flow one way, contributed files the other. **A correction is recorded beside the thing rather than as an edit to it.**

**A path with a single writer and defined readers is an interface between two agents**, and the set of such paths *is* the architecture of this vault. Adding a participant means granting a path, not changing anybody's code.

### Why the reviewer's framing matters

"Be critical" produces a reviewer who agrees with well-written work. **"Contradict this" produces a reviewer with a job.** The reviewer's output goes to `/review/` as its own artefact and is never merged into the thing it reviews — which is the same rule as the corrections path below, applied internally.

---

## The Viewers

**The rule: a source sits beside the node it produced.** Three viewers, and the third is the one that makes the provenance claim checkable rather than stated.

| Viewer | Shows | Requirement |
|---|---|---|
| **Graph viewer** | The nodes and edges, with settings | See below |
| **JSON viewer** | The retrieved payload behind a `ung:` node | Unmodified, beside the node |
| **Document viewer** | The instrument's own PDF or XML | **A provision node links to the exact page or byte range that produced it, and the viewer opens it there** |

**Acceptance test 4 is the document viewer test**, and it is what turns "we recorded the provenance" into something a stranger can check in one click.

---

## The Graph Viewer, And Why The Settings Are The Point

**A graph nobody can re-lay-out is a picture.** The configurable surface is what turns it into an instrument.

| Setting | Why it earns its place |
|---|---|
| Filter by node and edge type | The only way to see `ung:` alone, which is what a partner will want first |
| Collapse and expand a subtree | 159,926 US entities do not fit on a screen and never will |
| Change what a node is coloured and sized by | Colour is spent on assertion class by default; the ability to rebind it is what makes the view an argument rather than a decoration |
| Pin a node and walk outward by degree | The natural motion of checking a claim |
| Switch coarse and fine over the same data | Entity level and sentence level are the same graph |
| **Export the current view with its settings** | **So somebody else sees the same thing.** A screenshot of a graph is not evidence of a graph |

### The fractal test, which is the acceptance criterion

**Zoom into any node and it expands into a graph obeying identical rules.**

| Zoom into | Expands into |
|---|---|
| An entity | Its children |
| A law | Its provisions |
| A provision | Its sentences |

**Same interaction, same address scheme, same three assertion classes.** That is acceptance test 6.

### And the discipline carried from the method site

**Three visual classes that are never mixed: asserted, inferred, possible.** With origin — `ung:` / `akn:` / `sg:` — carried by shape or border rather than by hue, because hue is already spent.

**A hypothesis drawn like a fact is the failure this whole estate exists to prevent.** In this vault the specific instance is `sg:resolvesTo`, the edge from their law string to an instrument. It is our inference. Drawn like their assertion, it is a lie about the source of the most important claim in the demonstration.

---

## The Shareable Form

**The vault opens read-only for a stranger and asks for nothing.** That is acceptance test 8, and the Risk Graph Explorer vault already demonstrates it: its `app.json` requests no permissions.

| Requirement | Consequence |
|---|---|
| No permission prompts on open | Any capability the app requests must be optional |
| No model calls on the read-only path | **A vault app's model calls fail on a static host when the key is owner-sealed**, because the seal derives from the write key. So nothing on the demonstration path may depend on an LLM |
| No writes on the read-only path | Every write is refused as read-only off-site |
| The corrections path is separate and explicitly entered | See below |

**Read keys yes, write keys never.** The read key is published by definition. **And escrow the write key before publishing, not after**, because a vault whose write key is lost is frozen: readable forever, never correctable.

---

## Releases: The Citation Mechanism

`.vault/releases.json`, schema `sg-releases/v1`. **Use releases from the first artefact, not retrofitted.**

**Two properties matter here and both are load-bearing for a demonstration built on somebody else's data.**

**A release is the same content-addressed objects, not a copy that might have drifted**, so a dated snapshot is exact rather than approximately exact. **And publishing new work does not change what an existing link holder sees**, so a link handed over at a meeting keeps showing what was shown at the meeting.

**Two traps, recorded so nobody hits them.** A pinned view is **read-only for everybody including the owner**, refusing with `EPINNED` — so do not pin the working branch. And there are **no collection roots yet**, so when garbage collection is built, pinned commits must become roots or a published release could be collected out from under a live link. That is an upstream dependency, not a thing this vault can fix, and it belongs in the risk register rather than in a footnote.

### The release plan for this vault

| Release | Pins |
|---|---|
| `@pack-v0.33.67` | **This pack, as the first commit, before anything is built** |
| `@2026-09-08` | The retrieval snapshot of UnGovr data, when it happens |
| `@demo-v1` | The worked example, complete, as shown |

**A link pins with `#key|@v1-2`.** Resolution runs url, then stored choice, then default, then live.

---

## The Catalogue Entry

**Yes, immediately.** The submission-queue design says so and it takes under a minute. The catalogue is an index of published vaults that is itself a vault and lists itself, and a graph vault that is not in it is arguing against its own method.

The entry lives at [`/catalogue/entry.json`](../catalogue/entry.json) and names the read key, the default release, the one-line description, and the attribution to UnGovr.

---

## The Corrections Offer

**A public dataset of 320,000 entities will contain errors, and there is no visible mechanism for an outsider to propose a fix.** No repository, no fork, no pull request.

**The GDPR vault already demonstrates the shape**: writes scoped to a feedback folder. And the rule was settled on 31 July: **a correction is a proposal recorded beside the thing rather than an edit to it, and no file has two writers.**

**So this vault carries `/corrections/`**, a folder where a reader may record a proposed correction to a derived node without touching the node. Each correction names the node, the retrieval it disagrees with, and the evidence for the disagreement.

**Three reasons this is built rather than discussed.**

It demonstrates the point in a way a slide cannot. It costs almost nothing, since the mechanism is shipped and published elsewhere. **And it pre-empts a decision that is theirs**: nothing here proposes that UnGovr adopt anything. A correction sitting in a stranger's vault is a suggestion they may ignore, which is the correct power relationship for a first meeting.

> **Honest tension, recorded rather than resolved.** Building a corrections path for somebody else's data before asking them is a stranger implying their data needs correcting. The mitigation is that the folder ships empty, with the mechanism visible and no corrections filed.

---

## Host Chrome

**`app.json` configures the chrome through `hud`** — modes full, minimal, hidden and none — and it supplies back, forward, home, reload and a path bar.

**Do not build app-side navigation.** A vault app that draws its own back button is fighting the host and will drift from it.

**And a homepage** comes from `.vault/app.json` naming an `entry` with `present: true` and `auto_open`, or from a root `_page.json` which renders immediately on open. **This vault uses both**, because the second works in the plain browse view and the first works in the app host.

**A menu to sub-sections is a `cards` component whose items link to relative paths.** The `navigation` field is in-page anchors only, and the declarative folder-narrative manifest was proposed in March and never built.

**One markdown limitation that shapes every file in this pack**: markdown here **does not render task lists and does not support nested lists.** A checklist must be part of a page layout or an application. Every file in this pack uses tables and flat lists for exactly that reason.

---

## Where State Goes

| Kind of state | Where | Travels with the vault? |
|---|---|---|
| A per-device preference: theme, panel size, a dismissal | `sg.state.*`, 64 KiB per key, no grant needed | No |
| Anything whose loss would be a bug | `sg.fs.write('.app-state/...')`, a real commit | Yes |

**The rule verbatim from the guide**: if losing it when the user switches browsers would be fine, use device state; **if losing it would be a bug, write it into the vault.**

**Applied here**: graph viewer layout and filter settings are device state. **An exported view, a correction, and an acceptance are commits.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

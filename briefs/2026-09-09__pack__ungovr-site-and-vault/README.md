# Handover: The MVP And Its Provider Site

**version** v0.33.68 · **9 September 2026**

[🏠 Vault index](../README.md) › **Handover**

---

**This is the brief pack for the session that builds what [`/pack/`](../pack/README.md) specifies.**

It is carried in the vault rather than sent as an attachment, for the same reason the specification was: **a design published before it is built is the strongest demonstration of the method this vault argues for**, and a handover that lives beside the work can be checked against it later.

## Read In Order

| # | File | Holds |
|---|---|---|
| 00 | [Start Here](00__START-HERE.md) | The two deliverables, the strict order between them, and what was already decided |
| 01 | [What Is Already Built](01__what-is-already-built.md) | This vault as it stands, the five blockers, and **what the previous session refused to do** |
| 02 | [The House Pattern](02__the-house-pattern.md) | The `*.sgit.ai` stack, workflow, styles and providers contract, read from the live sites |
| 03 | [Vault MVP](03__vault-mvp.md) | **Deliverable one. This is the work** |
| 04 | [The Site](04__the-site.md) | Deliverable two, and the definitional problem to resolve before writing site content |
| 05 | [Verification](05__verification.md) | Acceptance tests for both, what would make this pack wrong, and the handback list |

## The Order Is Strict

**Vault MVP first. The site is a report on it.** A site written before the vault has anything measured has a ledger that is entirely `spec` and `unrun`.

## The One Thing To Do First

```bash
curl -sS -o /dev/null -w '%{http_code}\n' https://data.ungovr.org/v1/entities/index.json
```

**If that returns 200, blocker B1 closes and five acceptance tests become reachable in an afternoon.** If it does not, take the same decision the previous session took, log it in [`/provenance/retrieval-log.md`](../provenance/retrieval-log.md) the same way, and **do not substitute a lossy path**.

## What Is Not In This Pack

**The vault write key.** It is handed over out of band and must never enter the site repository — the family's CI runs a key-shape scan over the whole tree, including the built output. **The read key is publishable and is the one the site uses.**

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

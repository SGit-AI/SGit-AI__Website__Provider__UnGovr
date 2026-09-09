# Start Here: The UnGovr Vault MVP And Its Provider Site

**version** v0.33.68
**date** 9 September 2026
**for** a Claude Code session with network egress and repository access
**status** The vault exists and holds a specification. **Nothing it specifies is built.** The site repository exists and holds three files.

---

## Copy This To Brief The Session

> You are picking up a project with two deliverables and a strict order between them.
>
> **First**, build the MVP of an existing sgit vault that demonstrates semantic graphs and ontologies over open
> government data, using UnGovr's Atlas as the source. The vault already contains its own specification,
> published as its first commit before any implementation. Your job is the implementation.
>
> **Second**, build `github.com/SGit-AI/SGit-AI__Website__Provider__UnGovr` — a GitHub Pages site for
> `ungovr.providers.sgit.ai`, using the same build system, CI gate, release discipline and styles as every
> other `*.sgit.ai` site, and obeying the providers contract at `https://providers.sgit.ai/contract/`.
> The vault is the centrepiece of that site, embedded by its read key.
>
> **Read these in order, all of them, before writing anything:**
>
> 1. `00__START-HERE.md` (this file)
> 2. `01__what-is-already-built.md` — the vault as it stands, and what the previous session refused to do
> 3. `02__the-house-pattern.md` — the tech stack, workflow, styles and contract, read from the live sites
> 4. `03__vault-mvp.md` — **deliverable one. This is the work**
> 5. `04__the-site.md` — deliverable two, and the definitional problem you must resolve before writing a word of it
> 6. `05__verification.md` — the acceptance tests for both, and what would make this pack wrong
>
> **Then clone the vault before you clone the repository.** The vault carries a seven-file specification pack
> at `/pack/`, four agentic team role files at `/team/`, and a retrieval log recording a blocked fetch.
> Read the vault's own `/pack/03__the-worked-example.md` before you fetch anything.

---

## What Happened Yesterday, In One Paragraph

A previous session was given a brief pack and asked to create the vault. **It created the vault and wrote the specification, and it fetched no UnGovr data**, because its container's egress policy answered 403 to CONNECT on `data.ungovr.org` — the open endpoints, not only the authenticated ones. A summarising fetch path was available and was declined, on the grounds that a node retrieved that way cannot carry a hash of its source bytes, and committing one as a retrieval would put a false provenance record at the root of a vault whose entire argument is provenance.

**You are the session that unblocks it.** Everything the vault specifies about retrieval assumes a container that can reach the host. **Confirm that yours can before you plan anything**, because the answer changes the shape of both deliverables.

## The Order, And Why It Is Strict

**The vault MVP is first and the site is second.** Not because the site is less important, but because the site is *a report on the vault*. Its ledger states what was verified, on what date, with what left unrun. **A site written before the vault has anything measured is a site whose ledger is entirely `spec` and `unrun`**, and the family already has one of those; the honest thing is to build the measurement first and let the site report it.

**Ship the site anyway, at v0.1.0, with the sections it can honestly fill.** See `04__the-site.md`. What is forbidden is filling a section with something plausible because the section exists.

## What Is Already Decided

Do not relitigate these. Each was settled and is recorded in the vault or in this pack.

| Decision | Where |
|---|---|
| **You continue the existing vault.** Same write key, same history | This pack, and the project lead, 9 September |
| Scope is one county, one law, one acceptance. Widening it weakens it | Vault `/pack/00__README.md` |
| **Santa Barbara County, California; the California Public Records Act** | Vault `/pack/03__the-worked-example.md` |
| Nodes derived from their data must be visibly distinct from nodes that are our model | Vault `/pack/02__the-model.md`, the two-edge rule |
| Bulk data is compiled to a few large artefacts, never scattered into files | Vault `/pack/05__the-workbench.md` |
| Anchor to published identifiers rather than minting. **Akoma Ntoso for legislative text** | Vault `/pack/02__the-model.md` |
| Every claim carries a state, and the default is the weakest one | Both the vault and the providers contract |
| **The site carries all nine contract sections at v0.1.0**, several answered `spec` or `unrun` | This pack, and the project lead, 9 September |
| The site is GitHub Pages from `docs/`, built by `build.py`, no third-party anything | The house pattern, read from the live sites |
| `ungovr.providers.sgit.ai` is **not yet pointed**. It answers 404 today | Measured 9 September 2026 |

## What To Do First, In Order

1. **Confirm egress.** `curl https://data.ungovr.org/v1/entities/index.json`. If it fails, stop and say so; do not substitute a lossy path.
2. **Clone the vault** and read its pack. It is the specification you are implementing, and it was written to be read before the work.
3. **Fetch one country subset and compute the coverage of their `open_records.law` edge.** That single number is the argument, measured from their own data, **and it may not exist anywhere.** It is the highest-value thing in this entire pack.
4. **Then** build the join: entity → instrument → provision → obligation → control → evidence → acceptance.
5. **Then** the site, reporting what steps 3 and 4 actually produced.

## The Two Things That Will Go Wrong

**Scope.** Every reader wants to model all 398 records laws, or all 205 countries, or the whole entity graph. **One instrument modelled properly beats forty sketched.** If the vault tries to be a complete ontology of government it will ship nothing.

**The word "provider".** The family this site joins uses that word in one specific sense, and UnGovr does not fit it. **Read `04__the-site.md` §1 before you write a line of site content.** Getting this wrong means writing nine sections that answer the wrong questions well.

## Tone And Claims

**This vault and this site may be shown to UnGovr.** Neither is a critique of their work. The missing edge is exactly right for their stated purpose, which is helping a person reach their government, and it is one hop short of what everybody downstream needs. Write it that way.

**And do not overclaim.** The method site says of itself that its semantic layer is designed rather than shipped. That honesty survives into both deliverables.

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

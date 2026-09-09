---
title: The claim ledger — every claim, with the state it earned
description: "Every factual claim this site makes, once, with its verification state, the date it earned it, and where it is said. A claim on a page and not in this table fails the build."
lead: "Six states, and the default is the weakest one. **The join is the enforcement**: a claim that appears on a page and not in this table fails the build, and a `docs` claim whose source is not a URL fails it too."
order: 9
toc: true
wide: true
---

{{ledger}}

## How to read the states

| Chip | Means | What you may do with it |
|---|---|---|
| `verified` | Somebody ran it and watched it work, on that date, in a named place | Treat as fact **for that date and that setup**. Read it narrowly |
| `measured` | Our own pipeline produced this number on a named workload | Treat as fact about *our* workload; yours will differ |
| `docs` | Read in the vendor's documentation on that date; never executed by us | The honest debt. Check it against the vendor before relying on it |
| `spec` | A written specification for something that does not exist | **Never plan around it. Future tense only** |
| `unrun` | Code we wrote and have never executed | The invitation. Run it and find out |
| `projected` | Arithmetic, with its workings shown | Re-do it with your own numbers |

**Read `verified` narrowly.** On this site it mostly means *one container, one afternoon, one IP address, on 9 September 2026*. The API is live and rebuilds nightly; several of these claims have a shelf life measured in weeks.

**The one state this site never uses about UnGovr's compliance with anything** is any of the vault's six. [Those are a different vocabulary answering a different question](/join/), and merging them would lose both.

## What is honestly thin

- **`docs` claims about the payment path.** No `402` was ever returned here, so everything about the wallet, the price and the challenge headers is read rather than run. It is the largest block of unexercised claims on the site.
- **One gated corpus is still unread.** CGJ *report detail* needs the same key and was not fetched; only the indices were. Blocker B2 is otherwise closed.
- **One number is a sample, not a census**, and [says so with an interval](/coverage/).

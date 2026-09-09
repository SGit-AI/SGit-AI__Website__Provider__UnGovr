---
title: The four credential patterns, and why an open-data provider is a new row
description: "Pattern 0 is a mistake for a model vendor and the intended mode for an open-data API. Adding UnGovr to this family required arguing with the family's own definition, and the argument is here."
lead: "The four patterns are about one question: **where does the credential live, and what bounds it?** UnGovr answer it in a way no model provider in this family can — for most of their surface, by not having one."
order: 6
toc: true
---

## The four patterns

| | | For UnGovr |
|---|---|---|
| **Pattern 0** | Key in the page | **Not applicable to the open surface — there is no key.** For the gated corpora, a free read-only key with a daily cap: the first `yes` in this matrix that is not a warning |
| **Pattern 1** | Bounded key in the page | The bound on the open surface is **per IP, not per key**. No per-key scoping is documented for the gated one |
| **Pattern 2** | Short-lived token, from a minter | No minter offered |
| **Pattern 3** | **The host holds the key** and enforces the terms. The app never sees it | Unnecessary for reads at this risk level. **Necessary before anything spends from the wallet** |

## Why this needed an argument

This family defines *provider* as a service that serves models over an API. UnGovr serve data. **By the letter of that definition they do not belong here**, and writing the nine sections as though they were a model vendor would have produced nine sections answering the wrong questions well.

The resolution is that the definition was a proxy for the real question. The family's actual question is *where does the credential live and what bounds it*, and a provider that answers **"there is no credential, and the bound is your IP address"** is not an exception to that question — it is the most informative possible answer to it.

**Three rows in the comparison matrix are genuinely new because of it:**

| Section | A model provider's answer | UnGovr's |
|---|---|---|
| Which pattern | Pattern 0 is a mistake; pattern 3 is the goal | **Pattern 0 is the intended mode.** There is nothing to leak |
| The bounding primitive | A key scope, or a plan quota | **A rate limit per IP, then HTTP 402 with a payment challenge.** The bound is a *payment protocol*, not a property of a key |
| What it cost | Dollars on a named workload | **Nothing**, inside 100 requests a day |

**So the extension is deliberate, stated, and argued rather than quietly assumed.** It is [filed as a correction against the hub's contract](/briefs/) — beside it, not as an edit to it. The contract's own closing rule is that if adding a member requires template surgery then the contract is wrong and the fix belongs in the contract; the same logic covers a definition that a legitimate new member does not fit.

**Whether the contract takes that correction is not this site's decision.** It is a change to a shared contract, so it is [handback item 6](/briefs/).

## What pattern three would be for, here

Not for reads. Reading the Atlas needs no credential, and building a key-holding host in front of an open endpoint would add a dependency and remove nothing.

**It is for the wallet.** The Machine Payments path is the one place on this surface with an irreversible verb, and the only documented bound on it is the balance. A funded wallet reaching a browser is pattern 0 applied to money. {{claim:machine-payments}} If this estate ever pays UnGovr per request, the credential goes behind a host that enforces a per-workload ceiling — because the platform does not document one.

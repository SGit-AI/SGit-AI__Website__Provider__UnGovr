---
title: The comparison matrix
description: "Which of the four credential patterns each provider supports and which it forbids, per product. Generated from the patterns: front-matter of every provider page in this family."
lead: "Generated at build time from the `patterns:` block on each provider page. Adding a provider is one markdown file; this table follows. That is the contract's own test of itself."
order: 7
toc: false
wide: true
---

{{comparison}}

## Reading it

**Per product, never per vendor.** A vendor with three products can support three different patterns, and stating a credential rule at vendor level is how a reader ends up putting a spendable key somewhere a read-only one belonged. UnGovr's three rows are bounded by three different things: an IP budget, a free key's daily cap, and a wallet balance.

**`na` is not `no`.** On UnGovr's open surface the pattern question dissolves rather than being answered negatively — there is no credential for a pattern to be about. That is a different fact from "this provider does not support pattern 2", and the matrix distinguishes them.

**This site contributes one row shape the family did not have**: a provider where pattern 0 is correct. [The argument for admitting it is on the patterns page.](/patterns/)

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

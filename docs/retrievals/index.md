---
title: The retrieval log — every fetch, including the failures
description: "Twenty-one named retrievals plus a 49-request sample, each with the sha256 of the response bytes, the UTC timestamp and the outcome. The refusals are rows, not absences."
lead: "The rule: write the raw response bytes to disk unmodified, hash **those** bytes, and log before parsing anything. A node that cannot name the bytes it came from is an assertion, not a retrieval."
order: 3
toc: false
wide: true
---

Every number on this site derives from these bytes. Nothing on any page here is fetched at read time — the site makes no network call at all — so this log is the only thing standing between a published figure and an unsupported one.

{{retrievals}}

## The failures, and why they are rows

Three responses here are not `200`, and they are the useful ones.

| Row | What it means |
|---|---|
| `404` on `/v1/laws/records/us/ca.json` | The path separator in the law corpus is `--`, not `/` — the same convention the entity detail endpoint uses. A guess, logged as a guess, then corrected to `us--ca.json` |
| `404` on `/v1/cgj/counties/us--ca--santa-barbara.json` | The CGJ corpus is keyed by bare county code (`santa-barbara`), not by entity slug. Two identifier schemes for the same county, in one API |
| `401` on `/v1/ai-laws/index.json` | Blocker **B2**, still open. The corpus needs a key, and [the key is free](/#4-where-the-key-goes) — so this closes by registering, not by paying {{claim:ai-laws-gated}} |

Recording a refusal as an entry rather than leaving it as an absence is the point: a reader can see what was tried, what was declined, and that a shortcut existed and was not taken.

## The 49-request sample

The coverage sample's per-request log is not inlined above — 49 near-identical detail fetches would drown the page — but it is complete and downloadable:

- [`computation-1-sample-retrievals.tsv`](/files/computation-1-sample-retrievals.tsv) — timestamp, status, sha256 and URL for all 49

## What is not here

**The one retrieval this session declined to make.** UnGovr's `/v1/ai-laws/*` corpus is the highest-value unread thing in this project, and it is gated by a key that is free to register for. No key was registered, because registering one is a relationship with a nonprofit that [nobody has spoken to yet](/disclosures/), and that is a decision for a human rather than a build step. It is [handback item 2](/briefs/).

---

This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0).

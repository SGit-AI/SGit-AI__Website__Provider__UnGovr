# Handback — what a human with access must decide or check

Kept short enough to work through in one sitting. Eight items; **items 1 and 2 are the
ones that block anything.**

---

## 1 · The vault write key

The government-graph vault `dkeclt5r` was **not pushed by this session**, because the write
key is handed over out of band and was not available here. Everything the next version of
the vault needs is built and staged; it needs one `sgit push` from somebody holding the key.

**The key must never enter this repository.** `tools/secret-scan.sh` enforces that over the
whole tree including `docs/`, and it is wired into CI before any content was written.

## 2 · Register for a free UnGovr API key?

**Blocker B2, and the highest-value unknown in this project.** The `/v1/ai-laws/*` corpus is
unread. A key is **free** — this session confirmed that on their own page — so this closes by
registering, not by paying.

It is a handback item rather than a build step because registering is a **relationship with a
nonprofit nobody has spoken to** (see item 7), and that is a human decision.

## 3 · Default branch — settled

`dev`, confirmed from the sibling repository's `origin/HEAD`. CI deploys from it. The
workflow's `tag-release` job is conditioned on `refs/heads/dev` only, matching the estate.
**No action needed** unless that is wrong.

## 4 · May a `dev.send.sgraph.ai` vault be linked from a public site?

**The site currently ships this link**, on `/vault/`, because the read key is the whole point
of §7 and a link nobody can open is worse than a link on the wrong host. The page says
plainly that it is a development host.

**If the answer is no, the vault moves to production first** — that is a vault step, not a
site change, and then one URL on `content/vault.md` changes.

## 5 · When does `ungovr.providers.sgit.ai` get pointed?

It answers **404**, measured 9 September 2026. The site ships regardless, under the project
path. Nothing breaks when the domain lands: canonicals already name it, links are relative,
and the hub's `bin/sync-providers.py` picks the site up automatically once it answers.

## 6 · Does the hub's contract take the open-data-provider correction?

UnGovr do not fit the family's definition of *provider* — "a service that serves models over
an API". The site argues the definition was a proxy for the real question (*where does the
credential live, and what bounds it*), and that an answer of "there is no credential" is the
most informative possible answer rather than an exception.

**Filed as a correction beside the contract, not as an edit to it.** Whether the contract
takes it is a change to a shared document, so it is the project lead's call.

## 7 · Do we tell UnGovr before publishing?

**No conversation of any kind has taken place.** The CC BY 4.0 licence permits all of this
with attribution, and asking is not required.

Asking is probably right. The report contains several small, specific, checkable things they
would likely want — a stale `primary_source_url` on the CPRA record, `products` shipping
undocumented, rate-limit headers advertised in CORS but never emitted — and there is no
public repository to file any of them against.

## 8 · Who is the named owner on the acceptance node?

The seven-step join ends on `sg:acceptance/unassigned`, which ships **open**: no owner, no
review interval, no revocation path. An acceptance without an owner is a note, and writing a
plausible name because the field exists is the exact failure the vault argues against.

Needs a real name, an interval, and a revocation path.

---

## Verified before handback

| | |
|---|---|
| The full gate passes | `admin/build/validate.sh` — build reproducible, 12 pages, 29 claims, secret scan clean over 14 patterns |
| `docs/` matches `content/` | `python3 build.py --check` |
| No write key anywhere | secret scan + a second tripwire in `check_site.py` |
| The read key **is** present, on purpose | `/vault/`, and it is excluded from the scan deliberately |
| No page makes a network call | enforced by `check_site.py`, not just claimed |
| All nine contract sections, in order | enforced by `check_site.py` |
| Every claim cited and dated | enforced by `check_site.py`; a `docs` claim without a URL fails |
| `admin/build/` is not swallowed by `.gitignore` | the Python template's `build/` rule already broke a sibling release |

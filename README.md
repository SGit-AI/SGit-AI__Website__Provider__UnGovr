# SGit-AI__Website__Provider__UnGovr

The source for **[ungovr.providers.sgit.ai](https://ungovr.providers.sgit.ai/)** — an
independent report on the UnGovr Open Data API, written to the nine sections of the
[providers contract](https://providers.sgit.ai/contract/).

> **The domain does not resolve yet.** Measured 404 on 9 September 2026. The site ships
> anyway, under the GitHub Pages project path: every canonical URL states the intended
> host and every internal link is relative, so it serves correctly from either.

## What it reports

UnGovr publish an Atlas of 327,138 government entities and a corpus of 398 open-records
laws, free, under CC BY 4.0, with no credential needed for most of it. This report
measures one thing: **how far the join from an entity to the records law that governs it
can currently reach.**

| | |
|---|---|
| Entities sampled carrying `open_records.law` | **0 of 49** (95% CI 0.0–7.3%) |
| The same edge, inferred by slug prefix | **96.6%** of California's 16,071 entities |
| …of which would need a human | **20.5%** — geography and jurisdiction come apart |
| What the whole report cost | **$0.00**, 70 requests inside a free tier of 100 |

A missing law reference is **not a defect count**. It is an entity whose records law has
not been mapped yet. The number measures how far the join can reach.

## Layout

```
  .github/workflows/   validate → tag → deploy
  admin/build/         version.txt (owns the version) and validate.sh (the gate)
  assets/              site.css, site.js, favicon.svg — no web fonts, no CDN
  bin/                 bump.py — the only thing that moves the version
  briefs/              every brief this site was built from, published raw
  content/             the markdown sources, with YAML front-matter
  data/                claims.yml, and the vault's compiled artefacts
  docs/                THE BUILT OUTPUT. GitHub Pages serves this. COMMITTED
  files/               the example scripts, downloadable
  tools/               check_site.py, secret-scan.sh, check-js.sh
  build.py             the whole build system. No dependencies
```

## Build

```bash
python3 build.py              # build docs/
python3 build.py --check      # build to a temp dir and diff against docs/ (CI)
admin/build/validate.sh       # the full pre-release gate
```

Python 3.11+, **no external dependencies**. A site that argues for provenance should not
ask a reader to trust forty transitive packages.

## Release

```bash
bin/bump.py "what changed in this release"
python3 build.py
admin/build/validate.sh
git commit -am "site v0.1.1: what changed in this release"
git push -u origin dev
```

`admin/build/version.txt` owns the version, `bin/bump.py` moves it, the release commit's
subject repeats it, and **CI refuses to tag if the two disagree.** `dev` is the release
branch and the default.

## The check that matters most here

This repository is public. The vault it reports on is not, and whoever builds it holds
that vault's **write key**.

`tools/secret-scan.sh` runs over the whole tree **including the built output in `docs/`**,
on every push and every pull request, and refuses the release on a match.
`tools/check_site.py` carries the same tripwire a second time against the `passphrase:uuid`
shape an sgit key can also take.

It deliberately does **not** match `sgit_private_read_…`. A read key is publishable — it is
how this estate shares a vault, the same way `sgit.ai/llms.txt` does — and the
[vault page](https://ungovr.providers.sgit.ai/vault/) carries one on purpose.

## Licences

- **Content** (`content/`, `briefs/`, `docs/`) — CC BY 4.0
- **Build code** (`build.py`, `assets/`, `bin/`, `tools/`) — Apache-2.0
- **UnGovr's data**, from which every number here derives — CC BY 4.0, © UnGovr

Independent work by SGit-AI. Not affiliated with, endorsed by, or sponsored by UnGovr.

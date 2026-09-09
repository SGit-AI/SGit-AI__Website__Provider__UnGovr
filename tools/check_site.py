#!/usr/bin/env python3
"""
check_site.py — the pre-release gate: the acceptance checklist as assertions over
the built site.

The first four are the house gate, inherited from the sibling sites in this estate
unchanged in intent — version agreement, internal links, canonical host, key-leak
tripwire. The rest are this site's own promises, which are worth no more than the
checks that enforce them.

Two of them exist because of what this particular site is. It reports on a
nonprofit that publishes a public good, so `check_tone` refuses the words that
would turn a report into an audit. And it reports on a number that is easy to
misread, so `check_not_a_defect_count` refuses to publish the coverage figure
anywhere the framing sentence does not also appear.

Everything here is something a human would otherwise have to re-read the whole site
to confirm. Run after `python3 build.py`; `admin/build/validate.sh` runs both.

    python3 tools/check_site.py
"""

import hashlib
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs"
DOMAIN = "ungovr.providers.sgit.ai"

# Every number on this site was computed at the command line and compiled in, and
# no page fetches anything to render itself. ONE page is a deliberate exception:
# /vault/ embeds the live vault through SG/Vault's own embed protocol, which is the
# estate's published pattern for this and is worth more than a screenshot of a
# vault. So exactly one origin is allowed, it is reached only from the vendored
# embed component, and check_network_pages below pins the exception to that page.
VAULT_ORIGIN = "https://dev.vault.sgraph.ai"
ALLOWED_JS_ORIGINS = {
    VAULT_ORIGIN,
    # An XML namespace is an identifier, never fetched.
    "http://www.w3.org",
}
# The only files permitted to open a connection at all.
NETWORK_CAPABLE = {"assets/vault-ui-embed.js"}
# The only page permitted to load one.
# /estate/ is the second, and it is stricter than the first: it opens nothing at
# all until the reader picks a vault, and mounts exactly one at a time.
NETWORK_PAGES = {"vault/index.html", "estate/index.html"}

NON_AFFILIATION = "Not affiliated with, endorsed by, or sponsored by UnGovr"

# The framing sentence that must accompany the coverage number wherever it appears.
# A coverage figure without it reads as a defect count, which is the one reading
# this site exists not to produce.
NOT_A_DEFECT = "not a defect count"
COVERAGE_FIGURE = re.compile(r"\b0\s*(?:of|/)\s*49\b")

# Words that would make this page an audit of a nonprofit rather than a report on
# an API. The estate's own rule, and the brief's: a page that reads as a stranger
# auditing a public good has failed regardless of whether its facts are right.
FORBIDDEN_TONE = [
    (r"\bpartner\w*\b", "'partner' is never used about a vendor in this estate"),
    (r"\bfail(?:ure|ing|s)? to (?:provide|expose|publish|map)\b", "reads as an audit finding"),
    (r"\bnegligen\w+\b", "reads as an audit finding"),
    # "should have published", "should have mapped" — retrospective criticism of a
    # vendor, which is the thing this rule exists to catch. But "neither should
    # have TO build it" is an obligation, not a finding, and the broad pattern
    # flagged exactly that sentence in a vault deck. Narrowed rather than the
    # sentence rewritten, because the sentence was right.
    (r"\bshould have\b(?!\s+to\b)", "reads as an audit finding"),
]

failures = []
notes = []


def fail(msg):
    failures.append(msg)


def pages():
    return sorted(OUT.rglob("index.html"))


def check_non_affiliation():
    for p in pages():
        if NON_AFFILIATION not in p.read_text():
            fail(f"non-affiliation line missing from {p.relative_to(OUT)}")


def check_tone():
    """This site reports on an API and admires the work. These are the phrasings
    that would quietly turn it into something else.

    Scoped to this site's OWN prose. `/briefs/` is excluded because the briefs are
    republished verbatim — editing a source document to pass our own style gate
    would defeat the reason for publishing it raw, and the corrections against
    those documents are filed beside them instead."""
    for p in list(pages()) + list(OUT.rglob("*.md")):
        if "briefs/" in str(p.relative_to(OUT)).replace(os.sep, "/"):
            continue
        text = p.read_text()
        for n, line in enumerate(text.split("\n"), 1):
            if "check_site" in line or "FORBIDDEN_TONE" in line:
                continue
            for pattern, why in FORBIDDEN_TONE:
                if re.search(pattern, line, re.I):
                    fail(f"{p.relative_to(OUT)}:{n}: {why} — {re.search(pattern, line, re.I).group(0)!r}")


def check_not_a_defect_count():
    """The coverage number and its framing travel together or not at all."""
    for p in list(pages()) + list(OUT.rglob("*.md")):
        text = p.read_text()
        if COVERAGE_FIGURE.search(text) and NOT_A_DEFECT not in text:
            fail(f"{p.relative_to(OUT)}: states the coverage figure without the "
                 f"{NOT_A_DEFECT!r} framing")


def check_inferred_edge_is_marked():
    """`sg:resolvesTo` is the only edge crossing from their data into ours, and
    UnGovr did not make that claim. Any page that names it must say so on the same
    page. Rendered like an assertion it is a lie about the source."""
    for p in pages():
        text = p.read_text()
        if "resolvesTo" in text and "inferred" not in text.lower():
            fail(f"{p.relative_to(OUT)}: names sg:resolvesTo without marking it inferred")


def check_vendor_quotes_dated():
    """The rule that has already caught somebody in this family: a quote from a
    vendor carries the product it belongs to, the URL, and the date it was read.
    Enforced structurally — every <blockquote class="vendor"> needs a cite."""
    for p in pages():
        for m in re.finditer(r'<blockquote class="vendor"[^>]*>(.*?)</blockquote>',
                             p.read_text(), re.S):
            block = m.group(1)
            if "cite" not in block or not re.search(r"\b\d{1,2} \w+ 202\d\b", block):
                fail(f"{p.relative_to(OUT)}: a vendor quote carries no source URL and date")


def resource_loads(html):
    """Everything the browser fetches without the reader asking."""
    out = []
    out += re.findall(r'<script[^>]+src=["\']([^"\']+)', html)
    out += re.findall(r'<link[^>]+href=["\']([^"\']+)', html)
    out += re.findall(r'<img[^>]+src=["\']([^"\']+)', html)
    out += re.findall(r'@import\s+["\']([^"\']+)', html)
    out += re.findall(r'url\((https?://[^)]+)\)', html)
    return out


def check_no_third_party():
    """No declarative resource from another origin: no `<script src>`, no
    `<link href>`, no `<img src>`, no `@import`, no `url()`. The vault embed does
    not breach this — it declares nothing; the vendored component creates its frame
    at runtime, which check_network_pages governs instead."""
    for p in pages():
        for url in resource_loads(p.read_text()):
            if url.startswith(("http://", "https://", "//")) and DOMAIN not in url:
                fail(f"third-party resource loaded by {p.relative_to(OUT)}: {url}")
    for css in OUT.rglob("*.css"):
        text = css.read_text()
        for url in (re.findall(r'url\((https?://[^)]+)\)', text)
                    + re.findall(r'@import\s+["\']([^"\']+)', text)):
            fail(f"third-party resource in {css.relative_to(OUT)}: {url}")


def check_no_iframes():
    """No hand-written iframe anywhere, including on the vault page.

    The vault embed IS an iframe, but the page never writes one: the vendored
    component creates it, loads it with `?embed=1&parent=<origin>`, waits for the
    frame to announce itself, and only then posts the key with the target origin
    pinned. A hand-rolled `<iframe src=…#key>` would put the credential in a URL,
    which is exactly what that handshake exists to avoid — so a literal iframe tag
    in the markup means somebody has bypassed the protocol."""
    for p in pages():
        if re.search(r"<iframe", p.read_text(), re.I):
            fail(f"{p.relative_to(OUT)}: hand-written iframe — the vault embed must go "
                 f"through the embed protocol, which never puts the key in a URL")


def check_network_pages():
    """The site's claim is that it fetches nothing, with one named exception. This
    check is what makes that a fact rather than a sentence: no page may open a
    connection except /vault/, and no file may contain the code to do it except the
    vendored embed component."""
    for p in pages():
        rel = str(p.relative_to(OUT)).replace(os.sep, "/")
        text = p.read_text()
        opens = re.search(r"\bfetch\s*\(|XMLHttpRequest|navigator\.sendBeacon|new WebSocket", text)
        if opens and rel not in NETWORK_PAGES:
            fail(f"{rel}: opens a network connection ({opens.group(0)}) — only "
                 f"{sorted(NETWORK_PAGES)} may, and only to the vault origin")
    for js in OUT.rglob("*.js"):
        rel = str(js.relative_to(OUT)).replace(os.sep, "/")
        opens = re.search(r"\bfetch\s*\(|XMLHttpRequest|navigator\.sendBeacon|new WebSocket",
                          js.read_text())
        if opens and rel not in NETWORK_CAPABLE:
            fail(f"{rel}: opens a network connection ({opens.group(0)}) — only "
                 f"{sorted(NETWORK_CAPABLE)} may")


def check_read_key_only():
    """The embed is handed a credential in the page source, on purpose. This check
    is that it is the READ key and never anything else: a 64-hex read key, matching
    the one the vault page publishes, and no other credential shape in the attribute."""
    for p in pages():
        for m in re.finditer(r'data-readkey="([^"]*)"', p.read_text()):
            if not re.fullmatch(r"[0-9a-f]{64}", m.group(1)):
                fail(f"{p.relative_to(OUT)}: data-readkey is not a bare 64-hex read key")


def check_js_origins():
    """The claim on every page: this site contacts nothing. You can check it."""
    for js in list(OUT.rglob("*.js")) + list(OUT.rglob("index.html")):
        text = js.read_text()
        if js.suffix == ".html":
            text = "\n".join(re.findall(r"<script[^>]*>(.*?)</script>", text, re.S))
        for url in set(re.findall(r'["\'](https?://[^"\'\s]+)', text)):
            origin = "/".join(url.split("/")[:3])
            if origin not in ALLOWED_JS_ORIGINS:
                fail(f"script in {js.relative_to(OUT)} references {origin}")


def check_shortcodes():
    for p in pages():
        for m in re.findall(r"\{\{[a-z:|.\- ]+\}\}", p.read_text()):
            fail(f"unexpanded shortcode {m} in {p.relative_to(OUT)}")


def check_links():
    built = {str(p.relative_to(OUT)) for p in OUT.rglob("*") if p.is_file()}
    for p in pages():
        base = p.parent.relative_to(OUT)
        for href in re.findall(r'href=["\']([^"\'#?]+)', p.read_text()):
            if href.startswith(("http://", "https://", "mailto:", "//")):
                continue
            target = (Path(href.lstrip("/")) if href.startswith("/") else base / href)
            target = Path(os.path.normpath(str(target)))
            candidates = {str(target), str(target / "index.html")}
            if not candidates & built:
                where = p.relative_to(OUT) if p != OUT / "index.html" else "index.html"
                fail(f"dead internal link in {where}: {href}")


def check_relative_urls():
    """The site must work wherever it is served: the custom domain, a GitHub Pages
    project path, a local directory, a vault frame. A root-absolute internal URL
    works in exactly one of those, and shipping one left a sibling's first deploy
    unstyled for a day — so it is a build failure now, not a review item.

    It matters more here than usual: ungovr.providers.sgit.ai does not resolve yet,
    so every reader of v0.1.0 arrives under the project path."""
    for p in pages():
        for m in re.finditer(r'\b(?:href|src)="(/[^"]*)"', p.read_text()):
            fail(f"{p.relative_to(OUT)}: root-absolute URL {m.group(1)} — must be relative to the page")


def check_no_swallowed_urls():
    """A bare <https://…> in markdown reaches the browser as an unknown tag and the
    URL vanishes. It is invisible in the source and invisible on the page, which is
    the worst combination, so the build refuses it."""
    for p in pages():
        for m in re.finditer(r"<https?:[^>]*>", p.read_text()):
            fail(f"{p.relative_to(OUT)}: a bare URL is being parsed as a tag: {m.group(0)[:60]}")


def check_composition_links():
    """The family's recorded defect: a domain link is a referral, not a composition.
    An anchor into the estate must land on the page that answers the question its
    text promises. Canonical and og:url are exempt — they are identity, not links."""
    for p in pages():
        for m in re.finditer(r'<a [^>]*href="(https?://[^"]+)"', p.read_text()):
            url = m.group(1)
            path = url.split("://", 1)[1]
            if "/" not in path.rstrip("/") and DOMAIN not in url:
                fail(f"{p.relative_to(OUT)}: domain-only link {url} — link the page that answers the question")


def check_licence_stamp():
    """The estate publishes its sites under CC BY 4.0, stamped where a reader or an
    agent will actually meet it: the footer, every raw markdown document, and both
    machine-readable indexes. A stamp that drifts is worse than none."""
    stamp = "Creative Commons Attribution 4.0 International licence (CC BY 4.0)"
    for p in pages():
        if stamp not in p.read_text():
            fail(f"{p.relative_to(OUT)}: no licence stamp in the footer")
    for md in OUT.rglob("index.md"):
        if stamp not in md.read_text():
            fail(f"{md.relative_to(OUT)}: markdown twin carries no licence stamp")
    for name in ("llms.txt", "llms-full.txt"):
        if stamp not in (OUT / name).read_text():
            fail(f"{name} carries no licence stamp")
    for raw, what in ((OUT / "briefs", "brief"), (OUT / "packs", "pack file")):
        if raw.exists():
            for b in raw.rglob("*.md"):
                if "CC BY 4.0" not in b.read_text():
                    fail(f"{b.relative_to(OUT)}: published {what} carries no CC BY 4.0 stamp")


def check_attribution():
    """UnGovr publish the Atlas under CC BY 4.0. Using it obliges attribution, and
    the obligation is the same one this estate asks of its own readers."""
    for p in pages():
        text = p.read_text()
        if "data.ungovr.org" in text and "CC BY 4.0" not in text:
            fail(f"{p.relative_to(OUT)}: uses UnGovr data without the CC BY 4.0 attribution")


def check_nine_sections():
    text = (OUT / "index.html").read_text()
    wanted = ["1 · Disclosure", "2 · What it grants", "3 · Which pattern", "4 · Where the key goes",
              "5 · The bounding primitive", "6 · The minimal working example", "7 · What we use it for",
              "8 · What it cost", "9 · What went wrong"]
    pos = -1
    for w in wanted:
        i = text.find(w)
        if i < 0:
            fail(f"the report is missing section: {w}")
        elif i < pos:
            fail(f"the report's sections are out of order at: {w}")
        else:
            pos = i


def check_every_claim_cited():
    sys.path.insert(0, str(ROOT))
    import build  # noqa: E402
    claims = build.yaml_load((ROOT / "data" / "claims.yml").read_text())
    html = "\n".join(p.read_text() for p in pages())
    for c in claims:
        if f"claim-{c['id']}" not in html:
            fail(f"claim {c['id']!r} is in the ledger but cited by no page")
        if c["state"] not in build.STATES:
            fail(f"claim {c['id']!r} has an unknown state {c['state']!r}")
        if c["state"] in ("verified", "measured", "docs", "projected") and not c.get("date"):
            fail(f"claim {c['id']!r} is {c['state']} but carries no date")
        if c["state"] == "docs" and not c.get("source", "").startswith("http"):
            fail(f"claim {c['id']!r} is `docs` but its source is not a URL to read it at")


def check_version_agreement():
    """House check 1. One file owns the version; everything else is rendered from
    it. A blanket bump that misses a page ships two versions of one site."""
    version = (ROOT / "admin" / "build" / "version.txt").read_text().strip()
    if not re.fullmatch(r"v\d+\.\d+\.\d+", version):
        fail(f"admin/build/version.txt does not carry a vX.Y.Z version: {version!r}")
        return
    for p in pages():
        for badge in re.findall(r'class="ver"[^>]*>(v\d+\.\d+\.\d+)<', p.read_text()):
            if badge != version:
                fail(f"{p.relative_to(OUT)}: version badge {badge} != {version}")
    for name in ("llms.txt", "llms-full.txt"):
        if version not in (OUT / name).read_text():
            fail(f"{name} does not mention {version}")
    history = (OUT / "versions" / "index.html").read_text()
    # The row's version is inside a link now — every row goes to that version's own
    # page rather than the table being the only place it is described.
    rows = re.findall(r'class="vnum"[^>]*>(?:<a [^>]*>)?(v\d+\.\d+\.\d+)<', history)
    if version not in rows:
        fail(f"the release history has no row for {version}")
    for v in rows:
        if rows.count(v) > 1:
            fail(f"the release history lists {v} more than once")

    # The data behind the history, the file that owns the version, and the page for
    # this release must all agree — and the nav pill must reach that page.
    rel = json.loads((ROOT / "data" / "releases.json").read_text())
    if rel["current"] != version:
        fail(f"data/releases.json says current is {rel['current']}, version.txt says {version}")
    listed = [r["version"] for r in rel["releases"]]
    if listed != rows:
        fail("the rendered release history and data/releases.json disagree on the list "
             f"of releases ({rows[:3]}… vs {listed[:3]}…)")
    # Every release names the commit it was built from — except, necessarily, the
    # newest. A commit cannot contain its own hash: recording the sha and amending
    # produces a different sha, and doing it again produces another. So the current
    # release's commit is filled in by the FOLLOWING commit, and bin/bump.py refuses
    # to move to the next version while it is still blank. That closes the loop
    # without pretending a file can know the hash of the commit that carries it.
    for r in rel["releases"]:
        if r["version"] == rel["current"]:
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", r.get("commit", "")):
            fail(f"{r['version']} names no git commit — a version that cannot be traced "
                 f"to a commit cannot be verified later")
        if not (OUT / "versions" / r["version"] / "index.html").exists():
            fail(f"{r['version']} has no page of its own at /versions/{r['version']}/")
    for p in pages():
        for href in re.findall(r'class="ver" href="([^"]+)"', p.read_text()):
            if version not in href:
                fail(f"{p.relative_to(OUT)}: the version pill links to {href!r}, which is not "
                     f"{version}'s own page — see sgit.ai/docs/guidance on versions")
            break


def check_canonical_host():
    """House check 3. Every canonical and og:url is on the host in CNAME, and every
    page declares one — a copy-pasted canonical is how a static site quietly
    de-indexes itself."""
    host = (OUT / "CNAME").read_text().strip()
    for p in pages():
        text = p.read_text()
        claimed = re.findall(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', text)
        claimed += re.findall(r'<meta[^>]+property="og:url"[^>]+content="([^"]+)"', text)
        if not claimed:
            fail(f"{p.relative_to(OUT)}: no canonical link")
        for url in claimed:
            if not url.startswith(f"https://{host}/") and url != f"https://{host}":
                fail(f"{p.relative_to(OUT)}: canonical/og:url is not on {host} -> {url}")


def check_write_key_tripwire():
    """House check 4, as a belt to tools/secret-scan.sh's braces, and the check the
    brief singles out as the one that will bite whoever builds this: an sgit vault
    WRITE key is <passphrase>:<uuid>, or sgit_private_vault_…, and it unlocks
    everything the vault holds.

    The READ key is deliberately not matched. It is publishable — sharing a vault by
    its read key is how this estate shares vaults, the same way sgit.ai/llms.txt
    does — and this site's whole §7 depends on carrying one."""
    shapes = [
        re.compile(r"[A-Za-z0-9_-]{20,}:[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}"),
        re.compile(r"sgit_private_(?:vault|write)_[A-Za-z0-9]+"),
        # The UnGovr API key issued to this project. Free to obtain and read-only,
        # which is not the same as publishable: it carries a per-key quota and it
        # identifies whoever registered it.
        re.compile(r"ung_(?:live|test)_[A-Za-z0-9]{16,}"),
    ]
    for f in ROOT.rglob("*"):
        if not f.is_file() or ".git/" in str(f) or f.suffix in {
                ".png", ".jpg", ".webp", ".ico", ".woff2", ".zip", ".pdf", ".parquet"}:
            continue
        try:
            text = f.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        for shape in shapes:
            if shape.search(text):
                fail(f"{f.relative_to(ROOT)}: contains a credential-shaped string")


def check_no_restricted_corpus():
    """UnGovr's Open Data API declares CC BY 4.0 at the OpenAPI level, but the
    AI-law payloads carry their OWN licence block — "UnGovr Data License
    (non-exclusive, by agreement)", whose grant field reads "No license is
    conveyed by receipt of this file."

    The specific, more restrictive term governs. So that corpus may be described,
    measured and reported on, and may NOT be redistributed here. This repository is
    public and the vault it feeds is shared by a read key, so the only safe rule is
    that the payload never enters either tree.

    Two things are deliberately NOT matched, because matching them would block the
    report rather than the payload:

      * the licence sentence itself. Quoting one sentence of a licence in order to
        report what it says is the finding, not the redistribution.
      * the 401 error body, which is the evidence that the endpoint is gated at all.

    So the markers are the payload's own schema identifier and a set of field names
    that occur in the corpus and in nothing else.
    """
    markers = [
        '"ungovr.ai-laws/2"',
        "'ungovr.ai-laws/2'",
    ]
    # A file carrying several corpus-only field names is the payload even if the
    # schema line was stripped.
    corpus_fields = ("access_matrix", "tdm_optout_mechanism", "robots_txt_legal_weight",
                     "after_technical_circumvention", "authorization_test")
    for f in ROOT.rglob("*"):
        if not f.is_file() or ".git/" in str(f) or f.suffix in {
                ".png", ".jpg", ".webp", ".ico", ".woff2", ".zip", ".pdf", ".parquet"}:
            continue
        try:
            text = f.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        if "check_site" in f.name:
            continue
        hit = next((m for m in markers if m in text), None)
        if hit is None and sum(c in text for c in corpus_fields) >= 3:
            hit = "three or more corpus-only field names"
        if hit:
            fail(f"{f.relative_to(ROOT)}: contains UnGovr's restricted AI-law corpus "
                 f"({hit}) — that corpus is not CC BY 4.0 and must not be redistributed")


def check_decks_verbatim():
    """The decks are republished from the same vault under the same rule as the packs:
    byte for byte, with the sha256 of every file recorded in data/decks-manifest.txt.

    The rendered slides on /decks/<id>/ are the site's; the markdown is the vault's,
    and the twin beside each rendered deck IS that file rather than a re-rendering of
    it. Both paths are checked. A correction to a deck belongs in the vault, where the
    vault app renders the same bytes into the same slides."""
    _verbatim("decks", ROOT / "data" / "decks-manifest.txt", flat=True)


def check_packs_verbatim():
    """The packs are republished from the vault byte for byte, and this is what makes
    that a fact rather than a sentence.

    `data/packs-manifest.txt` records the sha256 of every pack file. If a published
    byte differs — an editor tidying a line, a stray trailing newline, a well-meant
    correction made here instead of in the vault — the build fails and names the file.
    A correction belongs in the vault where the original lives; making it here would
    leave two documents that disagree and no way to tell which is the source.

    The manifest is regenerated by copying the vault's packs/ over this repo's, so it
    cannot be updated without the bytes it describes."""
    _verbatim("packs", ROOT / "data" / "packs-manifest.txt", flat=False)


def _verbatim(top, manifest, flat):
    """Shared by both. `flat` says the manifest keys are bare filenames (decks/) rather
    than <collection>/<name> (packs/), which changes only how a rendered page's twin is
    matched back to the file it renders."""
    if not manifest.exists():
        fail(f"{manifest.name} is missing — {top}/ cannot be checked")
        return
    recorded = {}
    for line in manifest.read_text().split("\n"):
        if line.strip():
            digest, rel = line.split("  ", 1)
            recorded[rel.strip()] = digest.strip()
    # Two paths carry each file: the raw copy, and the markdown twin beside its
    # rendered page — which IS that file rather than a second rendering of it. Both
    # are checked, so a reader cannot drift from the bytes it claims to render.
    def slug_of(name):
        stem = name[:-3] if name.endswith(".md") else name
        if stem.upper() == "README":
            return "readme"
        return stem.split("__", 1)[-1] if flat else stem

    # A rendered page's twin lives at <top>/<slug>/index.md for a flat manifest, and
    # at <top>/<collection>/<slug>/index.md otherwise.
    by_slug, depth = {}, (2 if flat else 3)
    for rel in recorded:
        if flat:
            if rel == "README.md":
                continue                 # the collection's own index, which has no reader
            by_slug[(slug_of(rel),)] = rel
        elif "/" in rel:
            coll, name = rel.split("/", 1)
            by_slug[(coll, slug_of(name))] = rel

    published, twins = {}, 0
    for f in (OUT / top).rglob("*.md"):
        rel = str(f.relative_to(OUT / top)).replace(os.sep, "/")
        digest = hashlib.sha256(f.read_bytes()).hexdigest()
        if f.name == "index.md":
            parts = rel.split("/")
            if len(parts) != depth:
                continue                 # a real site page's own twin, not a republished file
            key = tuple(parts[:-1])
            if key not in by_slug:
                fail(f"{top}/{rel}: a rendered page whose twin matches no republished file")
                continue
            raw_rel = by_slug[key]
            twins += 1
            if digest != recorded[raw_rel]:
                fail(f"{top}/{raw_rel}: the reader's twin at {rel} is not the same bytes as "
                     f"the raw file — the reader has drifted from what it renders")
            continue
        published[rel] = digest
    if twins != len(by_slug):
        fail(f"{len(by_slug)} files under {top}/ but {twins} rendered pages — every one "
             f"must get a reader, and a reader must render one")

    for rel, digest in recorded.items():
        if rel not in published:
            fail(f"{top}/{rel} is in the manifest but was not published")
        elif published[rel] != digest:
            fail(f"{top}/{rel} differs from the vault — a correction belongs in the vault, "
                 f"not here (recorded {digest[:16]}, published {published[rel][:16]})")
    for rel in published:
        if rel not in recorded:
            fail(f"{top}/{rel} was published but is not in {manifest.name}")


def check_no_double_escaped_entities():
    """An HTML entity written into markdown ships as literal text.

    `inline()` escapes `&` before anything else, so `&mdash;` in a page's prose or
    front matter reaches the browser as `&amp;mdash;` and the reader sees the six
    characters rather than a dash. It shipped on /decks/ in v0.1.14 and was spotted
    in a screenshot, not by a check — the build was perfectly happy.

    The fix in the content is to type the character. This is what stops the next one:
    a literal entity anywhere in a built page fails the build and names it."""
    for p in pages():
        for m in re.finditer(r"&amp;[a-zA-Z][a-zA-Z0-9]{1,8};", p.read_text()):
            fail(f"{p.relative_to(OUT)}: {m.group(0)!r} ships as literal text — "
                 f"markdown escapes the ampersand, so type the character itself")


def check_deck_pdfs():
    """Every deck ships a PDF, and the PDF is not allowed to go stale.

    The PDFs are generated by a browser (tools/make-pdfs.js) and committed, because
    CI has no browser and a deck nobody can download is not the point. That makes
    staleness the risk: edit a deck, rebuild the site, and the page would happily
    offer a PDF of the previous words.

    So data/deck-pdfs.json records the sha256 of the DECK each PDF was built from.
    If a deck's bytes have moved, the PDF must be regenerated before the build
    passes — which is the whole reason the record is of the source, not the output."""
    reg = json.loads((ROOT / "data" / "deck-pdfs.json").read_text())
    decks = {}
    for line in (ROOT / "data" / "decks-manifest.txt").read_text().split("\n"):
        if line.strip():
            digest, name = line.split("  ", 1)
            decks[name.strip()] = digest.strip()
    expect = {n for n in decks if n != "README.md"}
    if {v["deck"] for v in reg.values()} != expect:
        fail(f"data/deck-pdfs.json covers {sorted(v['deck'] for v in reg.values())}, "
             f"but the decks are {sorted(expect)}")
    for slug, rec in reg.items():
        current = decks.get(rec["deck"])
        if current != rec["deck_sha256"]:
            fail(f"{rec['deck']} has changed since {slug}.pdf was built "
                 f"(deck is {str(current)[:16]}, the PDF was printed from "
                 f"{rec['deck_sha256'][:16]}) — rerun tools/make-pdfs.js")
        pdf = OUT / "files" / "decks" / f"{slug}.pdf"
        if not pdf.exists():
            fail(f"files/decks/{slug}.pdf was not published")
            continue
        got = hashlib.sha256(pdf.read_bytes()).hexdigest()
        if got != rec["pdf_sha256"]:
            fail(f"files/decks/{slug}.pdf is not the file data/deck-pdfs.json records "
                 f"({got[:16]} vs {rec['pdf_sha256'][:16]})")


def check_no_vault_markup():
    """Republished vault content must never become live markup on this origin.

    sgit.ai's site-pages brief states the rule this enforces: on a *.sgit.ai page
    there is no host — YOU are the host — and the bytes you render were written by
    whoever holds the vault's write key. **A vault must be able to change what is
    shown, and never what the page does.**

    It was not true here. A `<script>` in a pack file reached the rendered page as a
    real script tag and executed; so did `<img src=x onerror=…>`. Both were confirmed
    running in Chromium before build.py's renderer was given an `untrusted` mode that
    escapes rather than passes through. This check is what keeps it fixed, and it
    reads the built pages rather than trusting the flag was set."""
    for p in pages():
        rel = str(p.relative_to(OUT)).replace(os.sep, "/")
        if not (rel.startswith("packs/") or rel.startswith("decks/")):
            continue
        body = p.read_text()
        # The page's own chrome is ours; the reader's article is the vault's.
        for region in re.findall(r'<article class="packdoc">(.*?)</article>', body, re.S) + \
                      re.findall(r'<div class="deckbody" id="deck">(.*?)</div>\s*</div>', body, re.S):
            # Every pattern requires a REAL `<` or a real attribute. Escaped text is
            # inert and must not fire: `&lt;img src=x onerror=…&gt;` is the renderer
            # working, and an early version of this check flagged it, which would have
            # taught the next person to loosen the escaping to quiet the gate.
            for pattern, why in (
                (r"<script\b", "a script tag"),
                (r"<iframe\b", "an iframe"),
                (r"<form\b", "a form"),
                (r"<object\b|<embed\b", "an object or embed"),
                (r"<[a-z][^>]*\son[a-z]+\s*=", "an inline event handler"),
                (r'(?:href|src)\s*=\s*["\']\s*(?:javascript|data|vbscript):', "a script-bearing URL"),
            ):
                m = re.search(pattern, region, re.I)
                if m:
                    fail(f"{rel}: republished vault content rendered {why} ({m.group(0)!r}) — "
                         f"a vault may change what is shown, never what the page does")


def check_vault_url_form():
    """The vault opens at https://dev.vault.sgraph.ai/#<read-key>:<vault-id>.

    The `/en-gb/` form the handover brief carries does NOT work: the segment
    breaks the client-side fragment routing. Both forms return HTTP 200, because
    the shell of a single-page app is served either way — so this cannot be caught
    by checking a status code, and was not. It is caught here instead.

    `/briefs/` is exempt: those documents are republished verbatim and the bad URL
    in one of them is corrected beside it (C12), not edited out of it."""
    for p in list(pages()) + list(OUT.rglob("*.md")):
        rel = str(p.relative_to(OUT)).replace(os.sep, "/")
        if rel.startswith("briefs/"):
            continue
        for m in re.finditer(r"dev\.vault\.sgraph\.ai/(?!#)([a-z-]+)/#", p.read_text()):
            fail(f"{rel}: vault URL carries a /{m.group(1)}/ segment — it must be "
                 f"dev.vault.sgraph.ai/#<read-key>:<vault-id> or the fragment does not route")

def check_cname():
    cname = (OUT / "CNAME").read_text().strip()
    if cname != DOMAIN:
        fail(f"CNAME is {cname!r}, expected {DOMAIN!r}")


def check_markdown_twins():
    for p in pages():
        if not (p.parent / "index.md").exists():
            fail(f"no markdown twin beside {p.relative_to(OUT)}")


def check_disclosure_strip():
    """A disclosure found at the bottom does the opposite of its job."""
    for p in pages():
        text = p.read_text()
        i = text.find("disclosure-strip")
        j = text.find("<main")
        if i < 0:
            fail(f"{p.relative_to(OUT)}: no disclosure strip")
        elif j >= 0 and i > j:
            fail(f"{p.relative_to(OUT)}: the disclosure strip is below the fold")


def main():
    if not OUT.exists():
        print("docs/ not built — run python3 build.py first", file=sys.stderr)
        sys.exit(2)
    for fn in [check_version_agreement, check_links, check_relative_urls, check_canonical_host,
               check_write_key_tripwire, check_non_affiliation, check_tone,
               check_not_a_defect_count, check_inferred_edge_is_marked, check_vendor_quotes_dated,
               check_no_third_party, check_no_iframes, check_network_pages,
               check_read_key_only, check_js_origins, check_shortcodes,
               check_no_swallowed_urls, check_composition_links, check_licence_stamp,
               check_attribution, check_no_restricted_corpus, check_nine_sections,
               check_every_claim_cited,
               check_cname, check_markdown_twins, check_disclosure_strip,
               check_vault_url_form, check_packs_verbatim,
               check_decks_verbatim, check_no_vault_markup,
               check_no_double_escaped_entities, check_deck_pdfs]:
        fn()
    if failures:
        print(f"check_site: {len(failures)} problem(s)\n", file=sys.stderr)
        for f in failures:
            print("  ✗ " + f, file=sys.stderr)
        sys.exit(1)
    print(f"check_site: {len(list(pages()))} pages pass every acceptance assertion.")
    for n in notes:
        print("  · " + n)


if __name__ == "__main__":
    main()

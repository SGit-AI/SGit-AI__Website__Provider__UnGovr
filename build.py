#!/usr/bin/env python3
"""
build.py — the whole build system for ungovr.providers.sgit.ai.

Markdown in `content/` is the source of truth; this script renders it to static
HTML in `docs/`. No dependencies, no framework, no CDN: a site that argues for
provenance should not ask a reader to trust forty transitive packages.

    python3 build.py            build docs/
    python3 build.py --check    build to a temp dir and diff against docs/ (CI)

Generated, not hand-written:
  * the comparison matrix          — from `patterns:` front-matter on provider pages
  * the ledger of claims           — from data/claims.yml, joined to every {{claim:id}}
  * the coverage tables            — from data/computation-1.json and -2.json, which
                                     are the compiled output of the vault's own
                                     scripts, copied in rather than recomputed here
  * the retrieval log              — from data/retrieval-log.tsv, byte hashes and all
  * the seven-step join            — from data/graph.json
  * each page's markdown twin      — docs/<path>/index.md, the house convention

The rule that shapes all of it: every number on this site was computed at the
command line, against bytes whose sha256 is published, and compiled in. No page
here fetches anything.
"""

import html
import json
import os
import re
import shutil
import sys
import tempfile
import filecmp
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
ASSETS = ROOT / "assets"
FILES = ROOT / "files"
DATA = ROOT / "data"
BRIEFS = ROOT / "briefs"
# The dev packs, republished byte for byte from the vault they live in.
PACKS = ROOT / "packs"
# The decks, republished from the same vault under the same rule as the packs.
DECKS = ROOT / "decks"
OUT = ROOT / "docs"

# The estate convention: one file owns the version, `bin/bump.py` moves it, the
# release commit's subject repeats it, and CI refuses to tag if the two disagree.
VERSION = (ROOT / "admin" / "build" / "version.txt").read_text().strip()
# The host is owned by docs/CNAME's source of truth, here, and every canonical URL
# on the site is checked against it before a release. It does not resolve yet —
# measured 404 on 9 September 2026 — so the canonical states the intent and every
# internal link stays relative so the site serves correctly under the project path.
DOMAIN = "ungovr.providers.sgit.ai"

SITE = {
    "domain": DOMAIN,
    "base": f"https://{DOMAIN}",
    "title": "UnGovr, reported on",
    # The government-graph vault this site reports on. When the vault moves ahead,
    # this page is behind — and says so rather than guessing.
    "vault_id": "dkeclt5r",
    "vault_commit": "obj-cas-imm-e23f0cecfccf",
    "version": VERSION,
}

# Two levels, as on the sibling sites: every group label is itself a link to a real
# page, so nothing is reachable only by opening a menu.
NAV = [
    ("The report", "/", []),
    ("The finding", "/coverage/", [
        ("The coverage measurement", "/coverage/"),
        ("The seven-step join", "/join/"),
        ("Reaching a law", "/instruments/"),
        ("The retrieval log", "/retrievals/"),
    ]),
    ("The vault", "/vault/", [
        ("The government-graph vault", "/vault/"),
        ("The estate it joins", "/estate/"),
    ]),
    ("Patterns", "/patterns/", [
        ("The four patterns", "/patterns/"),
        ("Comparison matrix", "/comparison/"),
    ]),
    ("Try it", "/examples/", []),
    ("Evidence", "/ledger/", [
        ("The claim ledger", "/ledger/"),
        ("The briefs, published raw", "/briefs/"),
        ("Disclosures", "/disclosures/"),
        ("The four decks", "/decks/"),
        ("The dev packs, published raw", "/packs/"),
        ("Release history", "/versions/"),
    ]),
]

LICENCE_STAMP = (
    "This document is released under the Creative Commons Attribution 4.0 International licence (CC BY 4.0)."
)

NON_AFFILIATION = (
    "Independent work by SGit-AI. Not affiliated with, endorsed by, or sponsored by "
    "UnGovr. &ldquo;UnGovr&rdquo; identifies the open-data API this page reports on; all "
    "trademarks belong to their owners. UnGovr&rsquo;s data is used under CC BY 4.0."
)

# ---------------------------------------------------------------- tiny YAML ---
# A deliberate subset: mappings, sequences, sequences of mappings, inline lists,
# quoted scalars. Anything hairier belongs in prose, not in front-matter.


def yaml_load(text):
    lines = []
    for raw in text.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        lines.append((indent, raw.strip()))
    val, _ = _yaml_block(lines, 0, 0)
    return val


def _scalar(s):
    s = s.strip()
    if not s:
        return ""
    if s[0] in "\"'" and s[-1] == s[0] and len(s) > 1:
        body = s[1:-1]
        if s[0] == '"':                       # only double quotes take escapes
            body = body.replace('\\"', '"').replace("\\n", "\n").replace("\\\\", "\\")
        return body
    if s.startswith("[") and s.endswith("]"):
        inner = s[1:-1].strip()
        return [_scalar(x) for x in _split_commas(inner)] if inner else []
    if s == "true":
        return True
    if s == "false":
        return False
    if re.fullmatch(r"-?\d+", s):
        return int(s)
    if re.fullmatch(r"-?\d*\.\d+", s):
        return float(s)
    return s


def _split_commas(s):
    out, depth, cur, quote = [], 0, "", None
    for ch in s:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
            continue
        if ch in "\"'":
            quote, cur = ch, cur + ch
        elif ch in "[{":
            depth, cur = depth + 1, cur + ch
        elif ch in "]}":
            depth, cur = depth - 1, cur + ch
        elif ch == "," and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur)
    return [x.strip() for x in out]


def _yaml_block(lines, i, indent):
    if i >= len(lines):
        return {}, i
    if lines[i][1].startswith("- "):
        return _yaml_seq(lines, i, indent)
    return _yaml_map(lines, i, indent)


def _yaml_map(lines, i, indent):
    out = {}
    while i < len(lines):
        ind, text = lines[i]
        if ind < indent:
            break
        if ind > indent:  # defensive: a stray deeper line
            i += 1
            continue
        key, _, rest = text.partition(":")
        key, rest = key.strip(), rest.strip()
        if rest:
            out[key] = _scalar(rest)
            i += 1
        else:
            i += 1
            if i < len(lines) and lines[i][0] > ind:
                out[key], i = _yaml_block(lines, i, lines[i][0])
            else:
                out[key] = None
    return out, i


def _yaml_seq(lines, i, indent):
    out = []
    while i < len(lines):
        ind, text = lines[i]
        if ind < indent or not text.startswith("- "):
            break
        body = text[2:].strip()
        if ":" in body and not body.startswith(("\"", "'")):
            # a mapping whose first pair is on the dash line
            sub_lines = [(0, body)]
            j = i + 1
            while j < len(lines) and lines[j][0] > ind:
                sub_lines.append((lines[j][0] - (ind + 2), lines[j][1]))
                j += 1
            item, _ = _yaml_map(sub_lines, 0, 0)
            out.append(item)
            i = j
        else:
            out.append(_scalar(body))
            i += 1
    return out, i


# ------------------------------------------------------------- markdown ------
# A subset of GFM: headings, paragraphs, lists, tables, fenced code, block
# quotes, rules, inline emphasis/code/links. Enough for a report; small enough
# to read in one sitting.

INLINE_CODE = re.compile(r"`([^`]+)`")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"([^\"]*)\")?\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
EM = re.compile(r"(?<![\w*])\*([^*\n]+)\*(?![\w*])")
STRIKE = re.compile(r"~~([^~]+)~~")


def slugify(text):
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "section"


def inline(text, ctx):
    """Inline markdown → HTML. Code spans are extracted first so nothing
    inside them is interpreted."""
    spans = []

    def stash(m):
        spans.append(m.group(1))
        return f"\x00{len(spans) - 1}\x00"

    # Vault content is a third party's bytes. On this surface there is no host: we
    # are the host, and a document must be able to change what is SHOWN and never
    # what the page DOES. So for republished vault files the escaper takes
    # everything — no raw tags survive, and no shortcode runs, because a vault
    # file must not be able to mint a claim chip on this site either.
    untrusted = ctx.get("untrusted")
    text = INLINE_CODE.sub(stash, text)
    if not untrusted:
        text = shortcodes_inline(text, ctx)
    # GFM autolinks. Without this, <https://example.com/x> reaches the browser as an
    # unknown tag and the URL disappears from the page entirely — which is how §4's
    # vendor citation shipped with its URL invisible. Every quote there is supposed to
    # carry the product, the URL and the date read; two of the three were arriving.
    if not untrusted:
        text = re.sub(
            r"<(https?://[^>\s]+)>",
            lambda m: f'<a href="{m.group(1)}" rel="noopener">{m.group(1)}</a>',
            text,
        )
    placeholders = {}

    def stash_html(fragment):
        placeholders[f"\x01{len(placeholders)}\x01"] = fragment
        return list(placeholders)[-1]

    # keep raw <chip …> etc. produced by shortcodes out of the escaper
    if untrusted:
        text = html.escape(text, quote=False)
    else:
        parts = re.split(r"(<[^>]+>)", text)
        text = "".join(stash_html(p) if p.startswith("<") and p.endswith(">") else html.escape(p, quote=False) for p in parts)

    text = LINK.sub(lambda m: _link(m, ctx), text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = EM.sub(r"<em>\1</em>", text)
    text = STRIKE.sub(r"<s>\1</s>", text)
    text = text.replace("--", "&ndash;") if False else text
    for k, v in placeholders.items():
        text = text.replace(k, v)
    for i, code in enumerate(spans):
        text = text.replace(f"\x00{i}\x00", f"<code>{html.escape(code, quote=False)}</code>")
    return text


# Schemes a link in REPUBLISHED VAULT CONTENT may use. "A link is a place a vault
# author can send your visitor" — sgit.ai's site-pages brief. A markdown link is
# enough to mint one: `[click](javascript:…)` produced a live javascript: href here,
# and `[x](data:text/html,…)` a live data: document, both confirmed in the built page
# before this list existed. Relative links and fragments are fine; everything else
# must name a scheme on this list or it is not rendered as a link at all.
SAFE_SCHEMES = ("http://", "https://", "mailto:", "/", "#", ".")


def _link(m, ctx):
    label, href, title = m.group(1), m.group(2), m.group(3)
    if ctx.get("untrusted") and not href.startswith(SAFE_SCHEMES):
        # Keep the words, drop the destination, and say so rather than silently
        # swallowing it — a reader can still see what the document meant to link.
        return (f'{label} <span class="deadlink" title="A link in republished vault '
                f'content may only use http, https or mailto">[link removed: '
                f'{html.escape(href.split(":", 1)[0])}:]</span>')
    ext = href.startswith("http") and SITE["domain"] not in href
    attrs = f' title="{html.escape(title)}"' if title else ""
    if ext:
        attrs += ' rel="noopener"'
        ctx["external_links"].add(href)
    return f'<a href="{html.escape(href)}"{attrs}>{label}</a>'


def render_markdown(md, ctx):
    lines = md.split("\n")
    out, i = [], 0
    last, spins = -1, 0
    while i < len(lines):
        if i == last:                      # every branch must consume at least one line
            spins += 1
            if spins > 1:
                raise SystemExit(f"build: parser stuck at line {i + 1}: {lines[i]!r}")
        else:
            last, spins = i, 0
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith("```"):
            lang = stripped[3:].strip()
            body, i = [], i + 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                body.append(lines[i])
                i += 1
            i += 1
            cls = "shell" if lang in ("bash", "sh", "console", "shell") else (f"lang-{lang}" if lang else "")
            out.append(f'<pre class="{cls}">{html.escape(chr(10).join(body))}</pre>')
            continue

        # a block shortcode on a line of its own: {{app}}, {{ledger}}, {{comparison}}…
        if re.fullmatch(r"\{\{[a-z-]+\}\}", stripped):
            out.append(shortcodes_block(stripped, ctx))
            i += 1
            continue

        # <script> and <style> are consumed to their closing tag and emitted
        # VERBATIM, blank lines and all.
        #
        # They used to fall through to the raw-html branch below, which stops at the
        # first blank line — so a script with a blank line in it was cut in half and
        # the remainder rendered as markdown: `<p>` tags injected mid-function and
        # `i < all.length` escaped to `i &lt; all.length`. That ships a syntax error
        # into the page. It happened, on /estate/, and nothing caught it: tools/
        # check-js.sh only read assets/*.js and never the inline blocks. Both were
        # fixed together — this, and the check that would have found it.
        if re.match(r"<(script|style)\b", stripped, re.I) and not ctx.get("untrusted"):
            tag = re.match(r"<(script|style)\b", stripped, re.I).group(1).lower()
            block, close = [], f"</{tag}>"
            while i < len(lines):
                block.append(lines[i])
                done = close in lines[i].lower()
                i += 1
                if done:
                    break
            else:
                raise SystemExit(f"build: unclosed <{tag}> block")
            if close not in "\n".join(block).lower():
                raise SystemExit(f"build: unclosed <{tag}> block")
            out.append("\n".join(block))
            continue

        # raw html block (an <aside>, a stat-tile row, the app slot).
        # Never for republished vault content: there a block opening with `<` is a
        # paragraph that happens to start with an angle bracket, and it is escaped
        # like any other text. A vault file that shipped a <script> would otherwise
        # become a live script on this origin — which it did, until this line.
        if stripped.startswith("<") and not stripped.startswith("<http") and not ctx.get("untrusted"):
            block = []
            while i < len(lines) and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append(shortcodes_block("\n".join(block), ctx))
            continue

        # heading
        m = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if m:
            level, text = len(m.group(1)), m.group(2).strip()
            anchor = slugify(text)
            rendered = inline(text, ctx)
            if level >= 2:
                ctx["toc"].append((level, anchor, re.sub(r"<[^>]+>", "", rendered)))
            out.append(f'<h{level} id="{anchor}">{rendered}</h{level}>')
            i += 1
            continue

        # horizontal rule
        if re.fullmatch(r"(-{3,}|\*{3,})", stripped):
            out.append("<hr>")
            i += 1
            continue

        # table
        if "|" in stripped and i + 1 < len(lines) and re.fullmatch(r"\|?[\s:|-]+\|[\s:|-]*", lines[i + 1].strip()):
            head = _row(lines[i])
            aligns = [_align(c) for c in _row(lines[i + 1])]
            i += 2
            body = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                body.append(_row(lines[i]))
                i += 1
            th = "".join(f"<th{_style(a)}>{inline(c, ctx)}</th>" for c, a in zip(head, aligns + [None] * len(head)))
            trs = []
            for r in body:
                tds = "".join(f"<td{_style(a)}>{inline(c, ctx)}</td>" for c, a in zip(r, aligns + [None] * len(r)))
                trs.append(f"<tr>{tds}</tr>")
            out.append(
                '<div class="tablewrap"><table><thead><tr>' + th + "</tr></thead><tbody>" + "".join(trs) + "</tbody></table></div>"
            )
            continue

        # blockquote
        if stripped.startswith(">"):
            body = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                body.append(lines[i].strip()[1:].strip())
                i += 1
            out.append("<blockquote>" + render_markdown("\n".join(body), ctx) + "</blockquote>")
            continue

        # lists
        if re.match(r"^\s*([-*]|\d+\.)\s+", line):
            block, base = [], len(line) - len(line.lstrip(" "))
            while i < len(lines) and (
                re.match(r"^\s*([-*]|\d+\.)\s+", lines[i]) or (lines[i].strip() and (len(lines[i]) - len(lines[i].lstrip(" "))) > base)
            ):
                block.append(lines[i])
                i += 1
            out.append(_list(block, base, ctx))
            continue

        # paragraph
        para = [lines[i].strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not _breaks_paragraph(lines, i):
            para.append(lines[i].strip())
            i += 1
        out.append("<p>" + inline(" ".join(para), ctx) + "</p>")
    return "\n".join(out)


def _breaks_paragraph(lines, i):
    """A paragraph ends at whatever starts another block. Note the space required
    after a bullet: `**bold at the start of a line**` is not a list item."""
    line = lines[i]
    if re.match(r"^\s*([-*]\s+|\d+\.\s+|#{1,6}\s|>|```)", line):
        return True
    if line.strip().startswith("<") and not line.strip().startswith("<http"):
        return True
    if "|" in line and i + 1 < len(lines) and re.fullmatch(r"\|?[\s:|-]+\|[\s:|-]*", lines[i + 1].strip()):
        return True
    return False


def _row(line):
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    cells, cur, esc = [], "", False
    for ch in line:
        if esc:
            cur, esc = cur + ch, False
        elif ch == "\\":
            esc = True
        elif ch == "|":
            cells.append(cur.strip())
            cur = ""
        else:
            cur += ch
    cells.append(cur.strip())
    return cells


def _align(cell):
    cell = cell.strip()
    if cell.startswith(":") and cell.endswith(":"):
        return "center"
    if cell.endswith(":"):
        return "right"
    return None


def _style(a):
    return f' style="text-align:{a}"' if a else ""


def _list(block, base, ctx):
    ordered = bool(re.match(r"^\s*\d+\.\s+", block[0]))
    items, cur = [], None
    for line in block:
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        indent = len(line) - len(line.lstrip(" "))
        if m and indent == base:
            if cur is not None:
                items.append(cur)
            cur = [m.group(3)]
        elif cur is not None:
            cur.append(line[base:] if len(line) > base else line.strip())
    if cur is not None:
        items.append(cur)
    lis = []
    for item in items:
        first, rest = item[0], [x for x in item[1:] if x.strip()]
        body = inline(first, ctx)
        if rest:
            sub_base = min(len(x) - len(x.lstrip(" ")) for x in rest)
            body += render_markdown("\n".join(x[sub_base:] if len(x) > sub_base else x for x in rest), ctx)
        lis.append(f"<li>{body}</li>")
    tag = "ol" if ordered else "ul"
    return f"<{tag}>" + "".join(lis) + f"</{tag}>"


# ------------------------------------------------------------- shortcodes ----

STATES = {
    "verified": ("verified", "st-v", "Verified by execution on this date, by us."),
    "measured": ("measured", "st-m", "Measured by our own pipeline on a named workload and date."),
    "docs": ("vendor docs", "st-d", "Read from the vendor's documentation on this date. Never executed by us."),
    "spec": ("specified, not shipped", "st-s", "A specification. It does not exist yet."),
    "unrun": ("written, not run", "st-u", "Code we wrote and have never executed."),
    "projected": ("projected", "st-p", "Arithmetic, not an invoice. The workings are shown."),
}


def chip(state, date=None, claim_id=None, label=None):
    text, cls, why = STATES.get(state, ("unknown", "st-u", ""))
    body = label or text
    if date:
        body += f" {date}"
    title = html.escape(why)
    if claim_id:
        return f'<a class="chip {cls}" href="/ledger/#claim-{claim_id}" title="{title}">{html.escape(body)}</a>'
    return f'<span class="chip {cls}" title="{title}">{html.escape(body)}</span>'


def shortcodes_inline(text, ctx):
    def claim_ref(m):
        cid = m.group(1)
        c = ctx["claims_by_id"].get(cid)
        if not c:
            raise SystemExit(f"build: unknown claim id {cid!r} referenced by {ctx['page']}")
        ctx["claim_uses"].setdefault(cid, set()).add(ctx["page"])
        return chip(c["state"], c.get("date_label"), cid)

    text = re.sub(r"\{\{claim:([a-z0-9-]+)\}\}", claim_ref, text)
    text = re.sub(
        r"\{\{badge:([a-z]+)(?:\|([^}]+))?\}\}",
        lambda m: chip(m.group(1), m.group(2)),
        text,
    )
    return text


def shortcodes_block(block, ctx):
    m = re.fullmatch(r"\s*\{\{([a-z-]+)\}\}\s*", block)
    if not m:
        # a hand-written HTML block: inline shortcodes still expand inside it, so a
        # claim chip can sit in a stat tile without going through the escaper.
        return shortcodes_inline(block, ctx)
    name = m.group(1)
    fn = BLOCKS.get(name)
    if not fn:
        raise SystemExit(f"build: unknown block shortcode {{{{{name}}}}} on {ctx['page']}")
    return fn(ctx)


# ------------------------------------------------------- generated blocks ----

PATTERN_NAMES = {
    "0": "0 &middot; key in the page",
    "1": "1 &middot; bounded key in the page",
    "2": "2 &middot; short-lived token",
    "3": "3 &middot; host holds the key",
}
VERDICT_MARK = {
    "yes": ('<span class="v v-yes">&check;</span>', "available"),
    "no": ('<span class="v v-no">&times;</span>', "unavailable"),
    "never": ('<span class="v v-never">&#9888;</span>', "available and never acceptable"),
    "spec": ('<span class="v v-spec">&#9686;</span>', "specified here, not shipped"),
    "na": ('<span class="v v-na">&mdash;</span>', "not applicable"),
}


def block_comparison(ctx):
    rows = []
    for page in ctx["pages"]:
        fm = page["fm"]
        if not fm.get("patterns"):
            continue
        for entry in fm["patterns"]:
            cells = []
            for p in ("0", "1", "2", "3"):
                v = entry.get(f"p{p}") or {}
                verdict = v.get("verdict", "na")
                verdict = {True: "yes", False: "no"}.get(verdict, str(verdict).lower())
                if verdict not in VERDICT_MARK:
                    raise SystemExit(f"build: unknown pattern verdict {verdict!r} on {page['path']}")
                mark, meaning = VERDICT_MARK[verdict]
                note = html.escape(str(v.get("note", "")))
                cells.append(f'<td title="{meaning}">{mark}<span class="vnote">{note}</span></td>')
            rows.append(
                f'<tr><th scope="row"><a href="{page["url"]}">{html.escape(entry.get("provider", fm["title"]))}</a></th>'
                f'<td>{html.escape(str(entry.get("product", "")))}</td>'
                + "".join(cells)
                + f'<td>{html.escape(str(entry.get("server", "")))}</td></tr>'
            )
    head = "".join(f"<th>{n}</th>" for n in PATTERN_NAMES.values())
    legend = " &middot; ".join(f"{VERDICT_MARK[k][0]} {v}" for k, v in [(k, VERDICT_MARK[k][1]) for k in VERDICT_MARK])
    return (
        '<div class="tablewrap"><table class="cmp"><thead><tr><th>Provider</th><th>Product</th>'
        + head
        + "<th>Needs a server for the safe pattern</th></tr></thead><tbody>"
        + "".join(rows)
        + "</tbody></table></div>"
        + f'<p class="small dim legend">{legend}</p>'
        + '<p class="small dim">Generated at build time from the <code>patterns:</code> front-matter of every provider page. '
        "Adding a provider is one Markdown file; this table follows.</p>"
    )


def _grant_rows(grants):
    rows = []
    for g in grants:
        rows.append(
            "<tr><td><code>{v}</code></td><td><code>{o}</code></td><td><code>{r}</code></td>"
            "<td>{rev}</td><td>{b}</td></tr>".format(
                v=html.escape(str(g.get("verb", ""))),
                o=html.escape(str(g.get("object", ""))),
                r=html.escape(str(g.get("reach", ""))),
                rev="reversible" if g.get("reversible") else "<b>irreversible</b>",
                b=html.escape(str(g.get("bounded_by", g.get("note", "")))),
            )
        )
    return "".join(rows)


def block_grants(ctx):
    """Two layers, because they answer different questions: what an agent gains by
    connecting this provider at all, and what the key we actually use can reach."""
    fm = ctx["fm"]
    platform = fm.get("platform_grants") or []
    rows = _grant_rows(fm.get("grants") or [])
    not_granted = fm.get("not_granted") or []
    ng = ", ".join(f"<code>{html.escape(str(x))}</code>" for x in not_granted)
    plat = ""
    if platform:
        prows = []
        for g in platform:
            prows.append(
                "<tr><td><code>{v}</code></td><td><code>{o}</code></td><td><code>{r}</code></td>"
                "<td>{rev}</td><td>{p}</td><td>{n}</td></tr>".format(
                    v=html.escape(str(g.get("verb", ""))),
                    o=html.escape(str(g.get("object", ""))),
                    r=html.escape(str(g.get("reach", ""))),
                    rev="reversible" if g.get("reversible") else '<b class="irrev">irreversible</b>',
                    p=html.escape(str(g.get("product", ""))),
                    n=inline(str(g.get("note", "")), ctx),
                )
            )
        plat = (
            '<h4>What the platform can grant, per product</h4>'
            '<div class="tablewrap"><table class="grants"><thead><tr><th>verb</th><th>object class</th>'
            "<th>reach</th><th>reversibility</th><th>product</th><th>note</th></tr></thead><tbody>"
            + "".join(prows)
            + "</tbody></table></div>"
            + '<h4>What <em>our</em> key grants — scoped to text to speech and voices-read</h4>'
        )
    return (
        plat
        + '<div class="tablewrap"><table class="grants"><thead><tr><th>verb</th><th>object class</th><th>reach</th>'
        "<th>reversibility</th><th>bounded by</th></tr></thead><tbody>"
        + rows
        + "</tbody></table></div>"
        + (f'<p class="small"><b>Not granted</b> by a key scoped this way, and it should stay that way: {ng}.</p>' if ng else "")
        + '<p class="small dim">The same rows are emitted as front-matter in this page&rsquo;s '
        f'<a href="{ctx["page_url"]}index.md">markdown source</a>, so a capability index can join across '
        "providers without parsing English.</p>"
    )


def short_label(url):
    """A ledger row lists several pages; their full titles would each be a
    paragraph. The last path segment is what a reader recognises."""
    parts = [p for p in url.strip("/").split("/") if p]
    return html.escape(parts[-1] if parts else "the report")


def block_ledger(ctx):
    groups = {}
    for c in ctx["claims"]:
        groups.setdefault(c.get("group", "Other"), []).append(c)
    out = []
    for group, items in groups.items():
        out.append(f'<h3 id="{slugify(group)}">{html.escape(group)}</h3>')
        rows = []
        for c in items:
            used = sorted(ctx["claim_uses"].get(c["id"], set()), key=lambda u: ctx["page_urls"][u])
            links = ", ".join(
                f'<a href="{ctx["page_urls"][u]}" title="{html.escape(ctx["page_titles"][u])}">{short_label(ctx["page_urls"][u])}</a>'
                for u in used
            ) or '<span class="dim">&mdash;</span>'
            rows.append(
                f'<tr id="claim-{c["id"]}"><td>{inline(c["claim"], ctx)}</td>'
                f'<td>{chip(c["state"], c.get("date_label"))}</td>'
                f'<td class="small">{html.escape(str(c.get("source", "")))}</td>'
                f'<td class="small">{links}</td></tr>'
            )
        out.append(
            '<div class="tablewrap"><table class="ledger"><thead><tr><th>Claim</th><th>State</th>'
            "<th>How we know</th><th>Where it is said</th></tr></thead><tbody>" + "".join(rows) + "</tbody></table></div>"
        )
    counts = {}
    for c in ctx["claims"]:
        counts[c["state"]] = counts.get(c["state"], 0) + 1
    tiles = "".join(
        f'<div class="tile"><b>{counts.get(k, 0)}</b><span>{STATES[k][0]}</span></div>' for k in STATES if counts.get(k)
    )
    return f'<div class="tiles tiles-sm">{tiles}</div>' + "\n".join(out)


def _pct(x):
    return "&mdash;" if x is None else f"{100 * x:.1f}%"


def block_coverage(ctx):
    """Computation 1, with its query beside it. A number without its query is an
    assertion, and this site exists to argue the opposite."""
    c = json.loads((DATA / "computation-1.json").read_text())
    lo, hi = c["ci95_wilson"]
    rows = "".join(
        f'<tr><th scope="row">{html.escape(k)}</th><td class="num">{v["n"]}</td>'
        f'<td class="num">{v["k"]}</td><td class="num">{_pct(v["coverage"])}</td>'
        f'<td class="small">{html.escape(v["description"])}</td></tr>'
        for k, v in c["by_stratum"].items()
    )
    types = "".join(
        f'<tr><th scope="row"><code>{html.escape(t)}</code></th>'
        f'<td class="num">{v["n"]}</td><td class="num">{v["k"]}</td></tr>'
        for t, v in sorted(c["by_type"].items(), key=lambda kv: -kv[1]["n"])
    )
    return (
        '<div class="tiles">'
        f'<div class="tile tile-big"><b>{c["with_law"]} of {c["n"]}</b>'
        '<span>entities carrying <code>open_records.law</code></span></div>'
        f'<div class="tile"><b>{_pct(c["coverage"])}</b><span>coverage</span></div>'
        f'<div class="tile"><b>{100 * lo:.1f}&ndash;{100 * hi:.1f}%</b>'
        '<span>95% interval (Wilson)</span></div>'
        f'<div class="tile"><b>{len(c["by_type"])}</b><span>entity types sampled</span></div>'
        "</div>"
        f'<p class="note"><b>What this number is not.</b> {html.escape(c["not_a_defect_count"])}</p>'
        '<h4>By stratum</h4>'
        '<div class="tablewrap"><table><thead><tr><th>Stratum</th><th>sampled</th>'
        '<th>with law</th><th>coverage</th><th>what it is</th></tr></thead><tbody>'
        + rows + "</tbody></table></div>"
        '<h4>By entity type</h4>'
        '<div class="tablewrap"><table><thead><tr><th>type</th><th>sampled</th>'
        "<th>with law</th></tr></thead><tbody>" + types + "</tbody></table></div>"
        '<h4>The query that produced it</h4>'
        f'<pre class="q"><code>{html.escape(c["question"])}\n\n'
        f'method   {html.escape(c["method"])}\n'
        f'seed     {c["seed"]}\n'
        f'frames   the retrieved bytes in data/raw/, sha256 in the retrieval log\n'
        f'run      {html.escape(c["retrieved"])}</code></pre>'
        f'<p class="small dim">{html.escape(c["why_sample"])}</p>'
    )


def block_inferred(ctx):
    """Computation 2. The constructive half: not how short the join falls, but how
    far it would reach if it were inferred, and where inferring it would be wrong."""
    c = json.loads((DATA / "computation-2.json").read_text())
    rows = ""
    for st in c["strata"]:
        n, m, sus = st["n"], st["matched"], st["matched_but_suspect"]
        rows += (
            f'<tr><th scope="row">{html.escape(st["frame"])}</th>'
            f'<td class="num">{n:,}</td>'
            f'<td class="num">{m:,}</td><td class="num">{100 * m / n:.1f}%</td>'
            f'<td class="num">{st["unmatched"]:,}</td>'
            f'<td class="num warn">{sus:,}</td><td class="num warn">{100 * sus / n:.1f}%</td></tr>'
        )
    return (
        f'<p class="note"><b>Assertion class: {html.escape(c["assertion_class"])}.</b> '
        "Every edge in this table is one we would have to draw ourselves. It is the "
        "only edge in the demonstration that crosses from their data into our model, "
        "and it is drawn as <code>inferred</code> everywhere it appears.</p>"
        f'<p><b>The rule.</b> {html.escape(c["rule"])}.</p>'
        '<div class="tablewrap"><table><thead><tr><th>Frame</th><th>entities</th>'
        '<th>a law matches</th><th></th><th>none matches</th>'
        '<th>matched, needs a human</th><th></th></tr></thead><tbody>'
        + rows + "</tbody></table></div>"
        '<p class="small dim">&ldquo;Needs a human&rdquo; counts the bodies whose governing '
        "records law is not reliably given by geography: interstate compacts, federal "
        "categories, tribal nations, regulated utilities and charter schools. They are "
        "counted separately rather than folded into the headline, because they are "
        "exactly the bodies a requester most often wants.</p>"
    )


def block_retrievals(ctx):
    """Every fetch, including the failures. The log is the argument."""
    rows = ""
    for line in (DATA / "retrieval-log.tsv").read_text().strip().split("\n"):
        if not line or line.startswith("#"):
            continue
        ts, method, code, sha, size, rem, url = (line.split("\t") + [""] * 7)[:7]
        cls = "ok" if code == "200" else ("warn" if code in ("401", "402") else "bad")
        rows += (
            f'<tr><td class="small mono">{html.escape(ts)}</td>'
            f'<td class="mono">{html.escape(method)}</td>'
            f'<td class="mono st-{cls}">{html.escape(code)}</td>'
            f'<td class="small mono trunc" title="{html.escape(sha)}">{html.escape(sha[:16])}&hellip;</td>'
            f'<td class="num small">{html.escape(size)}</td>'
            f'<td class="small mono breakall">{html.escape(url)}</td></tr>'
        )
    return (
        '<div class="tablewrap"><table class="retr"><thead><tr><th>UTC</th><th>method</th>'
        '<th>status</th><th>sha256 of the bytes</th><th>bytes</th><th>URL</th>'
        "</tr></thead><tbody>" + rows + "</tbody></table></div>"
        '<p class="small dim">The raw response bytes were written to disk unmodified and '
        "hashed before anything parsed them. A node that cannot name the bytes it came "
        "from is an assertion, not a retrieval. The failures are rows here rather than "
        "absences, so a reader can see what was tried and refused.</p>"
    )


def block_join(ctx):
    """The seven-step join, rendered from the same graph.json the vault holds.
    Origin is carried by shape and border, assertion class by colour — hue is
    already spent on asserted/inferred, so the ung:/akn:/sg: distinction cannot
    also use it. A reader checks this first."""
    g = json.loads((DATA / "graph.json").read_text())
    steps = ""
    for i, n in enumerate(g["nodes"], 1):
        prov = n.get("provenance", {})
        src = ""
        if prov.get("source_url"):
            src = (f'<div class="prov"><span>retrieved</span> {html.escape(prov.get("retrieved", ""))}'
                   f'<br><span>sha256</span> <code class="trunc">{html.escape(str(prov.get("response_sha256", ""))[:24])}&hellip;</code>'
                   f'<br><span>source</span> <a href="{html.escape(prov["source_url"])}" rel="noopener nofollow">'
                   f'{html.escape(prov["source_url"][:64])}&hellip;</a></div>')
        elif prov.get("note"):
            src = f'<div class="prov"><span>note</span> {html.escape(prov["note"])}</div>'
        steps += (
            f'<li class="step o-{n["origin"]} a-{n.get("assertion", "asserted")}">'
            f'<div class="stepno">{i}</div>'
            f'<div class="stepbody"><div class="steptype"><code>{html.escape(n["id"])}</code>'
            f'<span class="oc">{html.escape(n["origin"])}</span>'
            f'<span class="ac">{html.escape(n.get("assertion", "asserted"))}</span></div>'
            f'<h4>{html.escape(n["label"])}</h4>'
            f'<p>{inline(n.get("note", ""), ctx)}</p>{src}</div></li>'
        )
    edges = "".join(
        f'<tr><td class="mono">{html.escape(e["from"])}</td>'
        f'<td class="mono edge a-{e.get("assertion", "asserted")}">{html.escape(e["type"])}</td>'
        f'<td class="mono">{html.escape(e["to"])}</td>'
        f'<td>{html.escape(e.get("assertion", "asserted"))}</td>'
        f'<td class="small">{inline(e.get("note", ""), ctx)}</td></tr>'
        for e in g["edges"]
    )
    return (
        '<div class="legend-box"><b>How to read this.</b> '
        '<span class="key o-ung"></span> <code>ung:</code> transcribed from UnGovr, never edited &middot; '
        '<span class="key o-akn"></span> <code>akn:</code> the instrument, anchored to its published citation &middot; '
        '<span class="key o-sg"></span> <code>sg:</code> our model. '
        'Origin is carried by border and shape; assertion class by colour. '
        'They are two different questions and merging them would lose both.</div>'
        f'<ol class="steps">{steps}</ol>'
        '<h4>The edges</h4>'
        '<div class="tablewrap"><table><thead><tr><th>from</th><th>edge</th><th>to</th>'
        "<th>class</th><th>note</th></tr></thead><tbody>" + edges + "</tbody></table></div>"
    )


def block_examples(ctx):
    rows = []
    for f in sorted((FILES / "examples").iterdir()):
        first = ""
        for line in f.read_text().split("\n"):
            if line.startswith("#") and not line.startswith("#!"):
                first = line.lstrip("# ").strip()
                break
            if line.startswith("//"):
                first = line.lstrip("/ ").strip()
                break
        state = "verified" if f.name in (ctx.get("ran") or set()) else "unrun"
        rows.append(
            f'<tr><td><a href="/files/examples/{f.name}" download><code>{f.name}</code></a></td>'
            f'<td class="small">{html.escape(first)}</td><td>{chip(state)}</td></tr>'
        )
    return (
        '<div class="tablewrap"><table><thead><tr><th>File</th><th>What it does</th><th>State</th></tr></thead>'
        "<tbody>" + "".join(rows) + "</tbody></table></div>"
    )


BLOCKS = {
    "comparison": block_comparison,
    "ledger": block_ledger,
    "examples": block_examples,
    "grants": block_grants,
    "coverage": block_coverage,
    "inferred": block_inferred,
    "retrievals": block_retrievals,
    "join": block_join,
}


# ------------------------------------------------------------------ shell ----


def rel_prefix(url):
    """How far a page sits below the site root: "" at /, "../" at /bench/."""
    depth = len([x for x in url.strip("/").split("/") if x])
    return "../" * depth


def relativise(doc, prefix):
    """Rewrite every root-absolute internal URL to one relative to this page.

    The site has to work wherever it is served from — the custom domain, a
    GitHub Pages project path (/<repo>/), a local directory, or inside a vault
    app frame, which has no origin at all. Root-absolute URLs work in exactly
    one of those, and the site spent its first deploy unstyled because of it.
    Directory URLs become explicit index.html so file:// works too.
    """

    def one(m):
        attr, target = m.group(1), m.group(2)
        path, _, frag = target.partition("#")
        path = path.lstrip("/")
        if path == "" or path.endswith("/"):
            path += "index.html"
        return f'{attr}="{prefix}{path}{"#" + frag if frag else ""}"'

    return re.sub(r'\b(href|src)="(/[^"]*)"', one, doc)


# ---------------------------------------------------------------- packs ----
# A document viewer for the republished pack files, built to the contract in
# sgit.ai/briefs/markdown-and-file-viewers: raw is always available for every
# file, the reader is an ADDITION and never a replacement, and the tree comes
# from a manifest generated at build time rather than a walk at runtime.
#
# That brief's ladder stops at rung 3 — "a viewer on your website" — for content
# that has to live outside a vault host, which is this. It is rendered HERE, at
# build time, rather than fetched and parsed in the browser, for one reason: this
# site's whole claim is that its pages contact nothing, and exactly two are
# allowed to (/vault/ and /estate/). A client-side reader would have made every
# pack file a third. A static render costs nothing at read time and keeps that
# claim true.
#
# The rendered view is the SITE'S; the bytes are the vault's. So intra-pack links
# are rewritten here so they resolve on this host — and the raw file beside every
# page is untouched, hash-checked against the vault, and one click away.

PACK_ORDER = ["README.md", "00__START-HERE.md", "01__the-anchor-node-thesis.md",
              "02__the-model.md", "03__the-standards-map.md", "04__the-worked-example.md",
              "05__integration.md", "06__verification.md"]


def pack_manifest():
    """The file tree, read from the manifest the build wrote — never from a walk.
    Returns {pack: [(filename, sha256)]} in PACK_ORDER, then anything else."""
    src = (DATA / "packs-manifest.txt").read_text()
    packs = {}
    for line in src.split("\n"):
        if not line.strip():
            continue
        digest, rel = line.split("  ", 1)
        rel = rel.strip()
        if "/" not in rel:
            continue                      # packs/README.md — the index, not a pack file
        pack, name = rel.split("/", 1)
        packs.setdefault(pack, []).append((name, digest.strip()))
    for pack, files in packs.items():
        files.sort(key=lambda f: (PACK_ORDER.index(f[0]) if f[0] in PACK_ORDER else 99, f[0]))
    return packs


def pack_slug(name):
    """06__verification.md -> 06__verification ; README.md -> readme"""
    stem = name[:-3] if name.endswith(".md") else name
    return "readme" if stem.upper() == "README" else stem


def pack_rail(pack, files, current):
    """The folder viewer. Every file on every page, so a reader is never one
    back-button away from the rest of the pack."""
    rows = []
    for name, digest in files:
        slug = pack_slug(name)
        here = " here" if name == current else ""
        rows.append(
            f'<a class="prow{here}" href="/packs/{pack}/{slug}/">'
            f'<span class="pname">{html.escape(name)}</span>'
            f'<span class="phash">sha256 {digest[:12]}</span></a>'
        )
    return ('<nav class="prail" aria-label="Files in this pack">'
            f'<div class="prailhead">{html.escape(pack)}/ &mdash; {len(files)} files</div>'
            + "".join(rows) +
            '<p class="prailfoot">Every file is one click from its own bytes. '
            'The hash beside each name is the sha256 this site checks on every build.</p>'
            "</nav>")


def pack_body(text, pack, files, ctx_shared):
    """Render one pack file, rewriting intra-pack links so they resolve here.

    The rewrite is the VIEW's, not the document's: `01__the-anchor-node-thesis.md`
    becomes the rendered sibling, and the vault-tree breadcrumbs `../../README.md`
    and `../README.md` become this site's equivalents. The raw file served beside
    this page keeps every one of them exactly as the vault wrote it."""
    names = {n for n, _ in files}
    ctx = dict(ctx_shared)
    ctx.update({"page": f"packs/{pack}", "page_url": f"/packs/{pack}/", "fm": {}, "toc": [],
                "untrusted": True})
    # The document's own leading `# Title` becomes this page's <h1>, so rendering it
    # again inside the article would print the title twice. Dropped from the VIEW
    # only — the raw file, and the twin beside it, still open on their own heading.
    body = render_markdown(re.sub(r"\A\s*#\s+[^\n]*\n", "", text), ctx)

    def one(m):
        attr, href = m.group(1), m.group(2)
        if href in names:
            return f'{attr}="/packs/{pack}/{pack_slug(href)}/"'
        if href == "../../README.md":
            return f'{attr}="/packs/"'
        if href == "../README.md":
            return f'{attr}="/packs/{pack}/"'
        return m.group(0)

    return re.sub(r'\b(href)="([^"]+)"', one, body), ctx


def pack_pages(out_dir, ctx_shared):
    """One page per pack file: the rail, the rendered document, and the raw bytes
    named and linked at the top and the bottom. Returns {url: title} for the
    sitemap and the machine indexes."""
    made = {}
    for pack, files in pack_manifest().items():
        order = [n for n, _ in files]
        for i, (name, digest) in enumerate(files):
            raw = (PACKS / pack / name).read_text()
            body, ctx = pack_body(raw, pack, files, ctx_shared)
            title = raw.lstrip().split("\n", 1)[0].lstrip("# ").strip() or name
            slug = pack_slug(name)
            url = f"/packs/{pack}/{slug}/"
            prev_ = f'<a href="/packs/{pack}/{pack_slug(order[i-1])}/">&larr; {html.escape(order[i-1])}</a>' if i else ""
            next_ = f'<a href="/packs/{pack}/{pack_slug(order[i+1])}/">{html.escape(order[i+1])} &rarr;</a>' if i + 1 < len(files) else ""
            rawurl = f"/packs/{pack}/{name}"
            page = {
                "fm": {"title": title, "wide": True,
                       "description": f"{name} from the {pack} dev pack, rendered — with the "
                                      f"raw bytes beside it, byte for byte from the vault."},
                "url": url,
                "crumb": f' / <a href="/packs/">packs</a> / <a href="/packs/{pack}/">{html.escape(pack)}</a> / {html.escape(name)}',
                "nav_match": "/packs/",
                "src_md": raw,
            }
            doc = (
                '<div class="rawbar">'
                f'<a class="btn-open" href="{rawurl}">View the raw file &darr;</a>'
                f'<span><b>{html.escape(name)}</b> &mdash; rendered here, and served '
                f'unrendered at <code>{html.escape(rawurl)}</code>. '
                f'sha256 <code>{digest[:16]}</code>, checked against the vault on every build. '
                '<b>The reader is an addition; the bytes are the document.</b> '
                "The rendering drops the document's own title line, because this page already "
                'carries it as its heading, and rewrites intra-pack links so they resolve here.</span>'
                "</div>"
                f'<div class="packwrap">{pack_rail(pack, files, name)}'
                f'<article class="packdoc">{body}</article></div>'
                + (f'<p class="packnav">{prev_}{next_}</p>' if (prev_ or next_) else "")
                + '<p class="packfoot">This is the site\'s rendering of a vault document. '
                  'Intra-pack links are rewritten so they resolve on this host; '
                  f'<a href="{rawurl}">the raw file</a> keeps every link exactly as the vault '
                  'wrote it, including the breadcrumbs that point into the vault\'s own tree.</p>'
            )
            target = out_dir / url.strip("/") / "index.html"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(page_html(page, ctx, doc))
            # The markdown twin IS the pack file. Two paths, the same bytes, both
            # checked — rather than a second rendering of it.
            (target.parent / "index.md").write_text(raw)
            made[url] = title
    return made


# ----------------------------------------------------------------- decks ----
# The vault's four decks, on this site.
#
# sgit.ai's "decks from a vault, on a site" brief describes a LIVE viewer: the
# host fetches deck sources out of the vault with a read key, runs them in a
# sandboxed opaque-origin frame, and renders the slide markup in a second frame
# with scripting off. That architecture exists because the vault's bytes are
# untrusted input to the host page, and because a push to the vault should change
# the site with no rebuild.
#
# THIS SITE DOES IT DIFFERENTLY, AND THE REASON IS ITS OWN CONTRACT. Every page
# here is static and contacts nothing; exactly two are allowed to open a
# connection, and both are named in check_network_pages. A live deck viewer would
# have made every deck page a third, and would have needed a vault reader and two
# frames to do safely what a build step does for free.
#
# So the decks are republished byte for byte, hash-checked against the vault on
# every build, and rendered here — the same rule already applied to packs/. What
# that costs is liveness: when the vault moves ahead of this site, THIS SITE IS
# BEHIND, and says so rather than guessing. The live decks are one click away in
# the vault's own app, which /vault/ and /estate/ both run.
#
# The brief's contract that DOES carry over, unchanged: the raw markdown is always
# available for every deck, the viewer is an addition rather than a replacement,
# and every rendered slide is one click from the file it was rendered from.

def parse_deck(text):
    """The site's parser is a port of the vault's app/build_appdata.py, so both
    render the same slides from the same file. A slide is an `##` heading and
    everything under it, split on `---`; a blockquote opening `**Notes.**` is
    speaker notes."""
    meta = {}
    if text.startswith("---\n"):
        fm, _, text = text[4:].partition("\n---\n")
        for line in fm.split("\n"):
            if ":" in line:
                k, _, v = line.partition(":")
                meta[k.strip()] = v.strip()
    slides, intro = [], ""
    for chunk in text.split("\n---\n"):
        chunk = chunk.strip()
        if not chunk:
            continue
        if chunk.startswith("## "):
            head, _, rest = chunk.partition("\n")
            notes, keep = "", []
            for para in rest.strip().split("\n\n"):
                if para.lstrip().startswith("> **Notes.**"):
                    notes = " ".join(l.lstrip("> ").strip() for l in para.split("\n"))
                    notes = notes.replace("**Notes.**", "").strip()
                else:
                    keep.append(para)
            slides.append({"title": head[3:].strip(), "body": "\n\n".join(keep).strip(),
                           "notes": notes})
        elif chunk.startswith("# ") and not intro:
            intro = chunk
    return {"title": meta.get("deck", ""), "subtitle": meta.get("subtitle", ""),
            "date": meta.get("date", ""), "intro": intro, "slides": slides}


def deck_manifest():
    """Decks in file order, from the manifest the build wrote — never a walk."""
    out = []
    for line in (DATA / "decks-manifest.txt").read_text().split("\n"):
        if not line.strip():
            continue
        digest, name = line.split("  ", 1)
        name = name.strip()
        if name != "README.md":
            out.append((name, digest.strip()))
    return out


def deck_slug(name):
    return name[:-3].split("__", 1)[-1] if name.endswith(".md") else name


def deck_pages(out_dir, ctx_shared):
    made = {}
    entries = deck_manifest()
    for name, digest in entries:
        raw = (DECKS / name).read_text()
        d = parse_deck(raw)
        slug = deck_slug(name)
        url = f"/decks/{slug}/"
        ctx = dict(ctx_shared)
        ctx.update({"page": f"decks/{name}", "page_url": url, "fm": {}, "toc": [],
                    "untrusted": True})

        rail = "".join(
            f'<a class="drow{" here" if n == name else ""}" href="/decks/{deck_slug(n)}/">'
            f'<span class="dnum">{i:02d}</span>'
            f'<span class="dname">{html.escape(parse_deck((DECKS / n).read_text())["title"])}</span></a>'
            for i, (n, _h) in enumerate(entries, 1)
        )

        slides = []
        for i, s in enumerate(d["slides"], 1):
            notes = (f'<div class="notes"><b>Notes.</b> {inline(s["notes"], ctx)}</div>'
                     if s["notes"] else "")
            slides.append(
                f'<section class="slide" id="s{i}" data-n="{i}">'
                f'<div class="sn">{i} / {len(d["slides"])}</div>'
                f'<h2>{inline(s["title"], ctx)}</h2>'
                f'{render_markdown(s["body"], ctx)}{notes}</section>'
            )

        rawurl = f"/decks/{name}"
        page = {
            "fm": {"title": d["title"] or slug, "wide": True,
                   "description": (d["subtitle"] or f"A deck from the government-graph vault, "
                                   f"{len(d['slides'])} slides.")},
            "url": url,
            "crumb": f' / <a href="/decks/">decks</a> / {html.escape(d["title"] or slug)}',
            "nav_match": "/decks/",
            "src_md": raw,
        }
        body = (
            f'<p class="dsub">{inline(d["subtitle"], ctx)} &middot; '
            f'<b>{len(d["slides"])} slides</b> &middot; {html.escape(d["date"])}</p>'
            '<div class="dbar">'
            '<button type="button" class="btn-present" id="present">&#9654; Present</button>'
            '<button type="button" class="btn-notes" id="ntoggle">Hide notes</button>'
            f'<a class="btn-raw" href="{rawurl}">The markdown &darr;</a>'
            f'<span class="dhash">sha256 <code>{digest[:16]}</code> &mdash; checked against the '
            'vault on every build</span>'
            "</div>"
            f'<div class="deckwrap"><nav class="drail" aria-label="Decks">{rail}'
            '<p class="drailfoot">Every deck is a projection of a markdown file. '
            'If the slides and the file ever disagree, <b>the file is right</b>.</p></nav>'
            f'<div class="deckbody" id="deck">{"".join(slides)}</div></div>'
            f'<p class="packfoot">These slides are rendered from <a href="{rawurl}">'
            f'<code>{html.escape(name)}</code></a>, republished byte for byte from the vault. '
            'The <b>live</b> decks — the same file, parsed by the vault\'s own app — are in the '
            'Decks view of <a href="/vault/">the vault</a>, which moves the moment the vault does. '
            'This page moves when the site rebuilds.</p>'
        )
        target = out_dir / url.strip("/") / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_html(page, ctx, body + DECK_JS))
        (target.parent / "index.md").write_text(raw)
        made[url] = d["title"] or slug
    return made


DECK_JS = """
<script>
/* Present mode and the notes toggle. Everything above renders without this: the
   slides are stacked, numbered and printable with JavaScript off, which is why
   the enhancement can be this small. No network call — see check_network_pages,
   which allows exactly two pages to make one and this is not either of them. */
(function () {
  var deck = document.getElementById('deck');
  if (!deck) return;
  var slides = [].slice.call(deck.querySelectorAll('.slide'));
  if (!slides.length) return;
  var at = 0, on = false;

  function paint() {
    for (var i = 0; i < slides.length; i++) slides[i].classList.toggle('off', on && i !== at);
    document.body.classList.toggle('presenting', on);
  }
  function go(n) {
    at = Math.max(0, Math.min(slides.length - 1, n));
    paint();
    if (on) slides[at].scrollIntoView({ block: 'start' });
  }

  var pbtn = document.getElementById('present');
  pbtn.addEventListener('click', function () {
    on = !on;
    pbtn.innerHTML = on ? '\u25a0 Leave present mode' : '\u25b6 Present';
    // Enter on whichever slide the reader has scrolled to, not back at the top.
    if (on) {
      var best = 0, top = 1e9;
      for (var i = 0; i < slides.length; i++) {
        var d = Math.abs(slides[i].getBoundingClientRect().top - 80);
        if (d < top) { top = d; best = i; }
      }
      at = best;
    }
    go(at);
  });

  var nbtn = document.getElementById('ntoggle');
  nbtn.addEventListener('click', function () {
    var hidden = document.body.classList.toggle('nonotes');
    nbtn.textContent = hidden ? 'Show notes' : 'Hide notes';
  });

  document.addEventListener('keydown', function (e) {
    if (e.target && /^(INPUT|TEXTAREA)$/.test(e.target.tagName)) return;
    if (e.key === 'ArrowRight' || e.key === 'PageDown') { if (on) { go(at + 1); e.preventDefault(); } }
    else if (e.key === 'ArrowLeft' || e.key === 'PageUp') { if (on) { go(at - 1); e.preventDefault(); } }
    else if (e.key === 'Escape' && on) { pbtn.click(); }
  });

  // A deep link to #s7 opens that slide. Reading the fragment is fine here; it is
  // the VAULT app that must never assign one.
  var m = /^#s(\d+)$/.exec(location.hash || '');
  if (m) {
    var n = parseInt(m[1], 10) - 1;
    if (n >= 0 && n < slides.length) { at = n; slides[n].scrollIntoView({ block: 'start' }); }
  }
}());
</script>
"""


def nav_html(current):
    items = []
    for label, href, subs in NAV:
        here = href == current or any(s_href == current for _, s_href in subs)
        cls = "nl here" if here else "nl"
        if not subs:
            items.append(f'<div class="ni"><a class="{cls}" href="{href}">{html.escape(label)}</a></div>')
            continue
        sub = "".join(
            f'<a class="sl{" here" if s_href == current else ""}" href="{s_href}">{html.escape(s_label)}</a>'
            for s_label, s_href in subs
        )
        items.append(
            f'<div class="ni ni-has"><a class="{cls}" href="{href}">{html.escape(label)}'
            '<span class="caret">&#9662;</span></a>'
            f'<div class="sub">{sub}</div></div>'
        )
    # The parent link points at a page, never at a domain: a domain link is a
    # referral rather than a composition, and the family records that as its one
    # defect. check_composition_links enforces it.
    return (
        '<nav class="site"><div class="row">'
        '<a class="brand" href="/">ungovr<span>.providers.sgit.ai</span></a>'
        '<a class="parent" href="https://providers.sgit.ai/contract/" rel="noopener" '
        'title="The providers contract on providers.sgit.ai — the nine sections this report is written to">'
        '&#8599; part of <b>sgit.ai</b></a>'
        '<span class="stage-pill">provider report</span>'
        f'<a class="ver" href="/versions/" title="Site release history">{SITE["version"]}</a>'
        '<button class="nav-toggle" type="button" aria-expanded="false" aria-label="Menu">Menu</button>'
        '<div class="nav-items">' + "".join(items) + "</div>"
        '<a class="gh" href="https://github.com/SGit-AI/SGit-AI__Website__Provider__UnGovr" rel="noopener">&#9733; Source</a>'
        "</div></nav>"
    )


def footer_html():
    return f"""<footer class="site"><div class="cols">
  <div>
    <div class="brandline">ungovr<span>.providers.sgit.ai</span></div>
    <p class="nonaff"><b>{NON_AFFILIATION}</b></p>
    <p>An independent report on the UnGovr Open Data API: what it grants, what bounds it, what it cost,
       and the one edge that stops short of what everybody downstream needs. The first open-data provider
       in the <code>*.providers.sgit.ai</code> family. Source material: the government-graph vault
       <code>{SITE['vault_id']}</code>.</p>
    <p class="licence">{LICENCE_STAMP} The code that builds it is Apache-2.0.
       UnGovr&rsquo;s Atlas is used under CC BY 4.0.</p>
    <p class="verline">site <a href="/versions/">{SITE['version']}</a> &middot; <a href="/ledger/">the ledger</a> &middot; <a href="/disclosures/">disclosures</a> &middot; <a href="index.md" title="The same page as plain markdown">this page as markdown</a></p>
  </div>
  <div>
    <h4>The report</h4>
    <a href="/">UnGovr, nine sections</a>
    <a href="/#5-the-bounding-primitive">&sect;5 The bounding primitive</a>
    <a href="/#8-what-it-cost">&sect;8 What it cost</a>
    <a href="/#9-what-went-wrong">&sect;9 What went wrong</a>
  </div>
  <div>
    <h4>The finding</h4>
    <a href="/coverage/">The coverage measurement</a>
    <a href="/join/">The seven-step join</a>
    <a href="/retrievals/">The retrieval log</a>
    <a href="/examples/">Example files</a>
  </div>
  <div>
    <h4>The vault</h4>
    <a href="/vault/">What the vault holds</a>
    <a href="/join/">Entity to acceptance</a>
    <a href="/coverage/">Computation 1</a>
  </div>
  <div>
    <h4>The argument</h4>
    <a href="/patterns/">The four patterns</a>
    <a href="/comparison/">Comparison matrix</a>
    <a href="/ledger/">Claim ledger</a>
    <a href="/briefs/">The briefs, published raw</a>
    <a href="/disclosures/">Disclosures</a>
  </div>
</div>
<div class="footnote"><p>No analytics. No cookies. No third-party fonts, scripts or CDN &mdash; every byte of this site
is served from this domain. Every number was computed at the command line against bytes whose sha256 is published in
<a href="/retrievals/">the retrieval log</a>, and compiled in. <b>Exactly one page opens a network connection</b> &mdash;
<a href="/vault/">the vault page</a>, to <code>dev.vault.sgraph.ai</code>, to run the vault live from its published read
key. Every other page fetches nothing, and a build check holds that line.</p></div>
</footer>"""


def page_html(page, ctx, body):
    fm = page["fm"]
    desc = fm.get("description", "")
    prov = fm.get("provenance", {}) or {}
    toc = ""
    if fm.get("toc") and len(ctx["toc"]) > 2:
        links = "".join(
            f'<a class="lv{lv}" href="#{anchor}">{html.escape(text)}</a>' for lv, anchor, text in ctx["toc"] if lv == 2
        )
        toc = f'<aside class="toc"><b>On this page</b>{links}</aside>'
    provline = ""
    if prov:
        provline = (
            f'<p class="prov">Prose from the government-graph vault <code>{html.escape(str(prov.get("vault", SITE["vault_id"])))}</code>, '
            f'{html.escape(str(prov.get("date", "")))}. '
            f'{html.escape(str(prov.get("note", "")))} '
            f'When the vault moves ahead, this page is behind &mdash; and says so rather than guessing.</p>'
        )
    prefix = rel_prefix(page["url"])
    return relativise(f"""<!doctype html>
<html lang="en" data-root="{prefix}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(fm['title'])} &mdash; {html.escape(SITE['title'])}</title>
<meta name="description" content="{html.escape(desc)}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{SITE['base']}{page['url']}">
<meta property="og:type" content="{'website' if page['url'] == '/' else 'article'}">
<meta property="og:site_name" content="{SITE['domain']}">
<meta property="og:url" content="{SITE['base']}{page['url']}">
<meta property="og:title" content="{html.escape(fm['title'])}">
<meta property="og:description" content="{html.escape(desc)}">
<meta name="twitter:card" content="summary">
<link rel="alternate" type="text/markdown" href="index.md" title="This page as markdown">
<link rel="stylesheet" href="/assets/site.css">
<link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">
<script src="/assets/site.js" defer></script>
</head>
<body>
{nav_html(page['nav_match'])}
<div class="disclosure-strip"><div class="row"><b>Independent.</b> No commercial relationship with UnGovr
&mdash; no funding, no agreement, no conversation of any kind &mdash; checked 9 September 2026.
<a href="/disclosures/">Disclosures</a> &middot; <a href="/ledger/">how every claim here is evidenced</a></div></div>
<main class="doc{' doc-wide' if fm.get('wide') else ''}">
<p class="crumb"><a href="/">ungovr.providers.sgit.ai</a>{page['crumb']}</p>
<h1>{html.escape(fm['title'])}</h1>
{f'<p class="lead">{inline(fm["lead"], ctx)}</p>' if fm.get('lead') else ''}
{provline}
{toc}
{body}
<p class="pagenav"><a href="/ledger/">Every claim on this site, with its state &rarr;</a>
<a href="/disclosures/">Disclosures &rarr;</a></p>
</main>
{footer_html()}
</body>
</html>
""", prefix)


# ------------------------------------------------------------------ build ----


def read_page(path):
    text = path.read_text()
    if not text.startswith("---"):
        raise SystemExit(f"build: {path} has no front-matter")
    _, fm_text, body = text.split("---", 2)
    fm = yaml_load(fm_text)
    rel = path.relative_to(CONTENT)
    slug = str(rel.with_suffix("")).replace("index", "").strip("/")
    url = "/" + (slug + "/" if slug else "")
    return {"path": path, "fm": fm, "body": body.lstrip("\n"), "url": url, "src_md": text}


def build(out_dir):
    out_dir = Path(out_dir)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)

    claims = yaml_load((DATA / "claims.yml").read_text())
    for c in claims:
        c["date_label"] = c.get("date", "")
    claims_by_id = {c["id"]: c for c in claims}

    pages = sorted((read_page(p) for p in CONTENT.rglob("*.md")), key=lambda p: (p["fm"].get("order", 500), p["url"]))
    page_urls = {p["path"].name: p["url"] for p in pages}
    page_urls = {str(p["path"]): p["url"] for p in pages}
    page_titles = {str(p["path"]): p["fm"]["title"] for p in pages}

    ctx_shared = {
        "claims": claims,
        "claims_by_id": claims_by_id,
        "claim_uses": {},
        "pages": pages,
        "page_urls": page_urls,
        "page_titles": page_titles,
        "external_links": set(),
    }

    # two passes: the first collects claim usage so the ledger can join on it.
    for _ in range(2):
        rendered = {}
        for page in pages:
            fm = page["fm"]
            crumbs = ""
            if page["url"] != "/":
                parts = [x for x in page["url"].strip("/").split("/") if x]
                parent = "/" + parts[0] + "/"
                if len(parts) > 1 and any(q["url"] == parent for q in pages):
                    crumbs = ' / <a href="' + parent + '">' + parts[0] + "</a>"
                elif len(parts) > 1:
                    crumbs = " / " + parts[0]
                crumbs += f" / {html.escape(fm['title'])}"
            page["crumb"] = crumbs
            page["nav_match"] = "/" + (page["url"].strip("/").split("/")[0] + "/" if page["url"] != "/" else "")
            ctx = dict(ctx_shared)
            ctx.update({"page": str(page["path"]), "page_url": page["url"], "fm": fm, "toc": []})
            body = render_markdown(page["body"], ctx)
            rendered[page["url"]] = (page, ctx, body)

    for url, (page, ctx, body) in rendered.items():
        target = out_dir / url.strip("/") / "index.html" if url != "/" else out_dir / "index.html"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(page_html(page, ctx, body))
        twin = page["src_md"].rstrip("\n")
        if LICENCE_STAMP not in twin:
            twin += f"\n\n---\n\n{LICENCE_STAMP}\n"
        (target.parent / "index.md").write_text(twin)

    # static assets, verbatim
    shutil.copytree(ASSETS, out_dir / "assets")
    shutil.copytree(FILES, out_dir / "files")
    # the briefs this site was built from, raw, at /briefs/ — the estate's shape.
    # Copied after the pages so the generated /briefs/index.html is not clobbered.
    for src in sorted(BRIEFS.rglob("*")):
        if src.is_file():
            dst = out_dir / "briefs" / src.relative_to(BRIEFS)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    # the dev packs, raw, at /packs/ — same rule as the briefs: byte for byte from
    # the vault, corrections filed beside rather than edited in. Copied after the
    # pages so the generated /packs/**/index.html are not clobbered.
    for src in sorted(PACKS.rglob("*")):
        if src.is_file():
            dst = out_dir / "packs" / src.relative_to(PACKS)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    # the rendered reader over those files, built from the manifest just copied
    pack_urls = pack_pages(out_dir, ctx_shared)
    for src in sorted(DECKS.rglob("*")):
        if src.is_file():
            dst = out_dir / "decks" / src.relative_to(DECKS)
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
    pack_urls.update(deck_pages(out_dir, ctx_shared))
    (out_dir / "CNAME").write_text(SITE["domain"] + "\n")
    (out_dir / ".nojekyll").write_text("")
    (out_dir / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE['base']}/sitemap.xml\n")
    urls = "".join(f"<url><loc>{SITE['base']}{u}</loc></url>"
                   for u in sorted(set(rendered) | set(pack_urls)))
    (out_dir / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + urls + "</urlset>\n"
    )
    (out_dir / "assets" / "site-index.json").write_text(site_index(rendered, claims))
    (out_dir / "llms.txt").write_text(llms_txt(rendered))
    (out_dir / "llms-full.txt").write_text(llms_full(rendered))
    print(f"build: {len(rendered)} pages, {len(claims)} claims → {out_dir}")
    unused = [c["id"] for c in claims if c["id"] not in ctx_shared["claim_uses"]]
    if unused:
        print("build: claims in the ledger that no page cites: " + ", ".join(unused))
    return rendered


def site_index(rendered, claims):
    """A machine-readable index of the site, beside llms.txt: what each page is,
    and every claim with the state it earned. The hub syncs from these."""
    pages = []
    for url, (page, ctx, body) in sorted(rendered.items()):
        fm = page["fm"]
        headings = [text for lv, _a, text in ctx["toc"]]
        pages.append({
            "url": url,
            "title": fm["title"],
            "description": fm.get("description", ""),
            "lead": re.sub(r"<[^>]+>", "", inline(fm.get("lead", ""), ctx)),
            "headings": headings,
            "kind": fm.get("kind", "page"),
        })
    return json.dumps({
        "version": SITE["version"],
        "domain": SITE["domain"],
        "vault": SITE["vault_id"],
        "licence": "CC BY 4.0",
        "pages": pages,
        "claims": [
            {"id": c["id"], "state": c["state"], "date": c.get("date", ""),
             "claim": re.sub(r"[*`]", "", c["claim"])}
            for c in claims
        ],
    }, indent=1)


def llms_txt(rendered):
    lines = [
        f"# {SITE['domain']}",
        f"> site {SITE['version']}",
        "",
        "> An independent report on the UnGovr Open Data API — 327,138 government entities and 398",
        "> open-records laws, published free under CC BY 4.0. This report measures one thing: how far",
        "> the join from an entity to the records law that governs it can currently reach.",
        "> Not affiliated with, endorsed by, or sponsored by UnGovr.",
        "",
        "The headline measurement: `open_records.law` is declared in UnGovr's published schema as an",
        "optional property of the entity-detail document, and it was present on 0 of 49 entities in a",
        "seeded random sample across 5 strata and 3 countries on 9 September 2026. A missing law",
        "reference is not an error — it is an entity whose records law has not been mapped yet. The",
        "number measures how far the join can reach. It is not a defect count.",
        "",
        "Every factual claim on this site carries one of six states: verified, measured, vendor docs,",
        "specified-not-shipped, written-not-run, projected. The full list is at /ledger/.",
        "Every page is also served as markdown at <page>/index.md.",
        "Every number was computed at the command line against bytes whose sha256 is published at",
        "/retrievals/. Exactly one page opens a network connection: /vault/ embeds the live vault from",
        "its published read key, against dev.vault.sgraph.ai. Every other page fetches nothing.",
        f"Licence: {LICENCE_STAMP}",
        "",
        "## Pages",
    ]
    for url, (page, _ctx, _body) in sorted(rendered.items()):
        lines.append(f"- [{page['fm']['title']}]({SITE['base']}{url}): {page['fm'].get('description', '')}")
    return "\n".join(lines) + "\n"


def llms_full(rendered):
    """The whole site as one markdown document. The estate ships one of these
    beside llms.txt so an agent can read the site without crawling it — and here it
    costs nothing, because markdown is already the source of truth."""
    parts = [
        f"# {SITE['domain']} — the whole site as markdown",
        f"site {SITE['version']} · source: the government-graph vault {SITE['vault_id']} · "
        "every claim's verification state is at /ledger/",
        "",
        "Independent work by SGit-AI. Not affiliated with, endorsed by, or sponsored by "
        "UnGovr. \"UnGovr\" identifies the open-data API this site reports on; all trademarks "
        "belong to their owners. UnGovr's Atlas is used under CC BY 4.0.",
        "",
        LICENCE_STAMP,
        "",
    ]
    for url, (page, _ctx, _body) in sorted(rendered.items()):
        parts += [
            "\n" + "=" * 78,
            f"PAGE {url}  —  {page['fm']['title']}",
            "=" * 78 + "\n",
            page["src_md"].strip(),
        ]
    return "\n".join(parts) + "\n"


def main():
    if "--check" in sys.argv:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "docs"
            build(target)
            diff = dircmp_report(target, OUT)
            if diff:
                print("build --check: docs/ is stale. Run `python3 build.py` and commit.", file=sys.stderr)
                for d in diff[:40]:
                    print("  " + d, file=sys.stderr)
                sys.exit(1)
            print("build --check: docs/ matches the sources.")
        return
    build(OUT)


def dircmp_report(a, b, prefix=""):
    out = []
    cmp = filecmp.dircmp(str(a), str(b))
    out += [f"only in build: {prefix}{x}" for x in cmp.left_only]
    out += [f"only in docs/: {prefix}{x}" for x in cmp.right_only]
    out += [f"differs: {prefix}{x}" for x in cmp.diff_files]
    for sub in cmp.common_dirs:
        out += dircmp_report(Path(a) / sub, Path(b) / sub, prefix + sub + "/")
    return out


if __name__ == "__main__":
    main()

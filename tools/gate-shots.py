#!/usr/bin/env python3
"""Render captured gate output as terminal images for the decks.

The text in these images is REAL output, captured by running the gate against a
deliberately broken tree and then restoring it — not typed to look convincing.
tools/shots.js photographs the site; this photographs the build refusing it.
"""
import html
import pathlib
import sys

TERM = """<!doctype html><meta charset="utf-8"><style>
  body{{margin:0;background:#0d1117;font:21px/1.6 ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}}
  .win{{width:1240px;padding:0 0 1rem}}
  .bar{{display:flex;gap:.5rem;align-items:center;padding:.7rem 1rem;background:#161b22;
    border-bottom:1px solid #21262d;color:#8b949e;font-size:17px}}
  .dot{{width:14px;height:14px;border-radius:50%}}
  pre{{margin:0;padding:1rem 1.2rem;color:#c9d1d9;white-space:pre-wrap;word-break:break-word}}
  .cmd{{color:#3fb950}} .bad{{color:#f85149}} .ok{{color:#3fb950}} .dim{{color:#8b949e}}
</style><div class="win">
<div class="bar"><span class="dot" style="background:#ff5f57"></span>
<span class="dot" style="background:#febc2e"></span>
<span class="dot" style="background:#28c840"></span>
<span style="margin-left:.6rem">{title}</span></div>
<pre>{body}</pre></div>"""


def render(text, cmd):
    out = [f'<span class="cmd">$ {html.escape(cmd)}</span>']
    for line in text.strip().split("\n"):
        e = html.escape(line)
        if line.lstrip().startswith("✗"):
            e = f'<span class="bad">{e}</span>'
        elif "pass every acceptance" in line or line.startswith("validate: OK"):
            e = f'<span class="ok">{e}</span>'
        elif line.startswith("check_site:") or line.startswith("secret-scan"):
            e = f'<span class="dim">{e}</span>'
        out.append(e)
    return "\n".join(out)


def main(argv):
    src, out_dir = pathlib.Path(argv[1]), pathlib.Path(argv[2])
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    for spec in argv[3:]:
        name, cmd, title = spec.split("|", 2)
        text = (src / f"{name}.txt").read_text()
        f = out_dir / f"{name}.html"
        f.write_text(TERM.format(title=html.escape(title), body=render(text, cmd)))
        made.append(str(f))
    print("\n".join(made))


if __name__ == "__main__":
    main(sys.argv)

#!/usr/bin/env python3
"""Publish one day's morning brief to the GitHub Pages site.

Usage: python3 build.py YYYY-MM-DD path/to/brief_fragment.html

The fragment is the inner HTML of the brief (sections only, no <html>/<body>).
Follows CONVENTIONS.md (Grok and Claude both publish):
- writes Claude's brief to briefs/YYYY-MM-DD-claude.html (never touches -grok files)
- index.html becomes a short landing page linking to today's Grok and Claude briefs
- archive.html lists every brief file, labeled by source (Grok / Claude).
"""
import sys, re, datetime, pathlib, html
from zoneinfo import ZoneInfo

ROOT = pathlib.Path(__file__).resolve().parent
BRIEFS = ROOT / "briefs"

CSS = """
:root{--ink:#1d1d1f;--muted:#6b6b70;--line:#e3e1dc;--bg:#faf8f4;--card:#fff;--accent:#8a3b26}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Georgia,"DejaVu Serif",serif}
.wrap{max-width:680px;margin:0 auto;padding:28px 18px 60px}
header{border-bottom:2px solid var(--ink);padding-bottom:10px;margin-bottom:22px}
header .kicker{font:600 12px/1 system-ui,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
header h1{margin:6px 0 0;font-size:30px}
nav{font:14px system-ui,sans-serif;margin-top:8px}
nav a{color:var(--muted);margin-right:14px}
section{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 18px;margin:0 0 16px}
section h2{font:700 13px/1.2 system-ui,sans-serif;letter-spacing:.08em;text-transform:uppercase;color:var(--accent);margin:0 0 8px}
table{border-collapse:collapse;width:100%}
td{padding:3px 6px 3px 0;vertical-align:top}
.sources{font:12px/1.5 system-ui,sans-serif;color:var(--muted);word-break:break-word}
ul.archive{list-style:none;padding:0}
ul.archive li{padding:8px 0;border-bottom:1px solid var(--line)}
a{color:var(--accent)}
footer{font:12px/1.5 system-ui,sans-serif;color:var(--muted);text-align:center;margin-top:24px;padding-top:12px;border-top:1px solid var(--line)}
"""

def page(title, kicker, body, footer=""):
    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{html.escape(title)}</title><style>{CSS}</style></head>
<body><div class="wrap">
<header><div class="kicker">{html.escape(kicker)}</div><h1>{html.escape(title)}</h1>
<nav><a href="{{root}}index.html">Today</a><a href="{{root}}archive.html">Archive</a></nav></header>
{body}
{footer}
</div></body></html>
"""

def published_stamp():
    now = datetime.datetime.now(ZoneInfo("America/Toronto"))
    return now.strftime("%A, %B %-d, %Y at %-I:%M %p ") + now.tzname()

def nice(d):
    return d.strftime("%A, %B %-d, %Y")

SOURCES = [("grok", "Grok version"), ("claude", "Claude version")]
FNAME = re.compile(r"^(\d{4}-\d{2}-\d{2})(?:-(grok|claude))?$")

def scan():
    """{date: {source: filename}} for every brief file; plain YYYY-MM-DD.html = older brief."""
    out = {}
    for p in BRIEFS.glob("*.html"):
        m = FNAME.match(p.stem)
        if m:
            d = datetime.date.fromisoformat(m.group(1))
            out.setdefault(d, {})[m.group(2) or "plain"] = p.name
    return out

def main():
    date = datetime.date.fromisoformat(sys.argv[1])
    frag = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    frag = re.sub(r"(?is)</?(html|body|head)[^>]*>", "", frag)
    BRIEFS.mkdir(exist_ok=True)
    stamp = html.escape(published_stamp())
    doc = page("Morning brief", nice(date) + " · Claude", frag, f"<footer>Published {stamp}</footer>")
    (BRIEFS / f"{date}-claude.html").write_text(doc.replace("{root}", "../"), encoding="utf-8")

    files = scan()
    today = max(files)
    links = []
    for src, label in SOURCES:
        f = files[today].get(src)
        links.append(f'<li><a href="briefs/{f}">{label}</a></li>' if f
                     else f'<li>{label} — <i>not yet published</i></li>')
    if "plain" in files[today]:
        links.append(f'<li><a href="briefs/{files[today]["plain"]}">Earlier brief</a></li>')
    landing = "<section><h2>Today's briefs</h2><ul class=\"archive\">\n" + "\n".join(links) + "\n</ul></section>"
    idx = page("Morning brief", nice(today), landing, f"<footer>Updated {stamp}</footer>")
    (ROOT / "index.html").write_text(idx.replace("{root}", ""), encoding="utf-8")

    rows = []
    for d in sorted(files, reverse=True):
        parts = [f'<a href="briefs/{files[d][s]}">{lab.split()[0]}</a>' for s, lab in SOURCES if s in files[d]]
        if "plain" in files[d]:
            parts.append(f'<a href="briefs/{files[d]["plain"]}">Brief</a>')
        rows.append(f"<li>{nice(d)} — " + " · ".join(parts) + "</li>")
    arch = page("Archive", "Past morning briefs", "<section><ul class=\"archive\">\n" + "\n".join(rows) + "\n</ul></section>",
               f"<footer>Last updated {stamp}</footer>")
    (ROOT / "archive.html").write_text(arch.replace("{root}", ""), encoding="utf-8")
    print(f"published {date} (claude); index links: " + ", ".join(s for s, _ in SOURCES if s in files[today]) + f"; {len(files)} day(s) in archive")

if __name__ == "__main__":
    main()

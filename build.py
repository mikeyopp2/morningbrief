#!/usr/bin/env python3
"""Publish one day's morning brief to the GitHub Pages site.

Usage: python3 build.py YYYY-MM-DD path/to/brief_fragment.html

The fragment is the inner HTML of the brief (sections only, no <html>/<body>).
Writes briefs/YYYY-MM-DD.html, makes index.html a copy of the newest brief,
and rebuilds archive.html from everything in briefs/.
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

def main():
    date = datetime.date.fromisoformat(sys.argv[1])
    frag = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
    frag = re.sub(r"(?is)</?(html|body|head)[^>]*>", "", frag)
    BRIEFS.mkdir(exist_ok=True)
    stamp = html.escape(published_stamp())
    doc = page("Morning brief", nice(date), frag, f"<footer>Published {stamp}</footer>")
    (BRIEFS / f"{date}.html").write_text(doc.replace("{root}", "../"), encoding="utf-8")

    dates = sorted((datetime.date.fromisoformat(p.stem) for p in BRIEFS.glob("*.html")), reverse=True)
    newest = dates[0]
    newest_doc = (BRIEFS / f"{newest}.html").read_text(encoding="utf-8").replace('href="../', 'href="')
    (ROOT / "index.html").write_text(newest_doc, encoding="utf-8")

    items = "\n".join(f'<li><a href="briefs/{d}.html">{nice(d)}</a></li>' for d in dates)
    arch = page("Archive", "Past morning briefs", f'<section><ul class="archive">\n{items}\n</ul></section>',
               f"<footer>Last updated {stamp}</footer>")
    (ROOT / "archive.html").write_text(arch.replace("{root}", ""), encoding="utf-8")
    print(f"published {date}; {len(dates)} brief(s) in archive")

if __name__ == "__main__":
    main()

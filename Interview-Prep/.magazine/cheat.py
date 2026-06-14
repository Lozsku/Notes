# -*- coding: utf-8 -*-
"""Builds CHEATSHEET.pdf in the premium magazine style (replaces the old LibreOffice build)."""
import re, html, subprocess
import mag

ROOT = mag.ROOT
SRC = (ROOT / "CHEATSHEET.md").read_text(encoding="utf-8")

# topic -> accent (matches the magazine series)
PAL = {1:"#6366f1",2:"#10b981",3:"#3b82f6",4:"#06b6d4",5:"#8b5cf6",6:"#f59e0b",
       7:"#f43f5e",8:"#0d9488",9:"#f97316",10:"#ef4444",11:"#a855f7"}
BASE = "#6366f1"
b = mag.shades(BASE)
ACC_CSS = (f":root{{--acc:{BASE};--acc2:#8b5cf6;--acc-bg:{b['bg']};--acc-z:{b['z']};"
           f"--acc-bd:{b['bd']};--acc-tx:{b['tx']};--acc-d:{b['d']};}}")

EXTRA_CSS = r"""
.hero{padding:9mm 0 4mm;}
.cards{column-count:2;column-gap:12px;}
.tcard{break-inside:avoid;border:1px solid var(--cbd);border-radius:13px;margin:0 0 12px;overflow:hidden;
  box-shadow:0 2px 7px #0b10200d;display:inline-block;width:100%;}
.tcard .th{display:flex;align-items:center;gap:9px;padding:8px 12px;color:#fff;
  background:linear-gradient(135deg,var(--cd),var(--c));}
.tcard .th .num{font-family:'Space Grotesk';font-weight:700;font-size:14px;opacity:.92;}
.tcard .th .nm{font-family:'Space Grotesk';font-weight:700;font-size:10.4px;line-height:1.05;}
.tcard .tbody{padding:9px 13px 4px;background:#fff;}
.tcard ul{margin:0;padding-left:15px;list-style:none;}
.tcard li{font-size:8.6px;margin:4px 0;line-height:1.42;color:#2b3450;position:relative;padding-left:3px;}
.tcard li::marker{content:"";}
.tcard li::before{content:"";position:absolute;left:-11px;top:5px;width:5px;height:5px;border-radius:50%;background:var(--c);}
.tcard li ul{margin:3px 0 3px 4px;}
.tcard b{color:#10182f;} .tcard em{color:var(--cd);font-style:normal;font-weight:600;}
.kbd{font-family:'JetBrains Mono';font-size:7.8px;background:var(--acc-z);border:1px solid var(--acc-bd);
  border-radius:5px;padding:1px 4px;color:var(--acc-d);}
.tcard .kbd{background:var(--cbg);border-color:var(--cbd);color:var(--cd);}
.hl-y{background:linear-gradient(transparent 55%,#ffe08a 55%);padding:0 1px;font-weight:600;color:#1c2540;}
.rank{counter-reset:r;column-count:2;column-gap:18px;}
.rank .ri{display:flex;gap:10px;align-items:center;padding:6px 0;border-bottom:1px solid var(--acc-bd);break-inside:avoid;}
.rank .ri .rn{counter-increment:r;font-family:'Space Grotesk';font-weight:700;font-size:13px;color:var(--acc);width:22px;}
.rank .ri .rn::before{content:counter(r,decimal-leading-zero);}
.rank .ri .rt{font-size:9px;font-weight:600;color:#1c2540;}
.chips{display:flex;flex-wrap:wrap;gap:6px;margin-top:24px;}
.chip{display:flex;align-items:center;gap:6px;font-size:8px;font-weight:600;color:#cfd6f3;
  background:#ffffff10;border:1px solid #ffffff1a;border-radius:20px;padding:4px 10px 4px 7px;}
.chip i{width:9px;height:9px;border-radius:50%;display:block;}
/* compact card-themed tables (e.g. the isolation-levels matrix) */
.tcard table{font-size:6.4px;margin:6px 0;border-radius:7px;box-shadow:0 0 0 1px var(--cbd);width:100%;}
.tcard thead th{background:linear-gradient(135deg,var(--cd),var(--c));color:#fff;padding:3.5px 5px;
  font-family:'Space Grotesk';font-weight:600;font-size:6.2px;text-align:left;}
.tcard tbody td{padding:3px 5px;border-top:1px solid var(--cbd);vertical-align:top;line-height:1.3;}
.tcard tbody tr:nth-child(even) td{background:var(--cbg);}
.tcard table code{font-size:6px;}
"""

def parse():
    title = re.sub(r"[^\x00-\x7f]", "", re.search(r"^#\s+(.*)$", SRC, re.M).group(1)).strip()
    txt = re.sub(r"\n## Table of Contents\n.*?(?=\n## )", "\n", SRC, flags=re.DOTALL)
    parts = re.split(r"\n## (?=\S)", txt)
    intro = re.search(r"\n>\s+(.*)", parts[0])
    intro = intro.group(1) if intro else ""
    secs = []
    for p in parts[1:]:
        line, _, body = p.partition("\n")
        secs.append((line.strip(), body.strip()))
    return title, intro, secs

def topic_card(n, name, body):
    inner = mag.md.markdown(body, extensions=["sane_lists", "tables"])
    s = mag.shades(PAL[n])
    style = f"--c:{PAL[n]};--cd:{s['d']};--cbd:{s['bd']};--cbg:{s['bg']}"
    return (f'<div class="tcard" style="{style}"><div class="th"><span class="num">{n:02d}</span>'
            f'<span class="nm">{html.escape(name)}</span></div><div class="tbody">{inner}</div></div>')

def leaderboard(body):
    items = re.findall(r"^\d+\.\s+(.*)$", body, re.M)
    ris = "".join(f'<div class="ri"><span class="rn"></span><span class="rt">{mag.md.markdown(it)[3:-4]}</span></div>'
                  for it in items)
    return f'<div class="rank">{ris}</div>'

def build():
    title, intro, secs = parse()
    pages = []
    # chips
    chips = "".join(f'<span class="chip"><i style="background:{PAL[i]}"></i>{i:02d}</span>' for i in range(1, 12))
    pages.append(f"""<section class="page cover"><div class="grid"></div>
      <div class="blob" style="width:240px;height:240px;background:#6366f1;top:-40px;right:-30px;opacity:.5;"></div>
      <div class="blob" style="width:200px;height:200px;background:#8b5cf6;bottom:120px;left:-50px;opacity:.4;"></div>
      <div class="blob" style="width:150px;height:150px;background:#22d3ee;bottom:-30px;right:50px;opacity:.28;"></div>
      <div class="cover-in">
        <div class="kicker"><span class="pill">Engineering Essentials</span><span>FAANG Interview Master Series</span></div>
        <h1 style="margin-top:auto">The Master <span class="g">Cheat Sheet</span></h1>
        <div class="sub">All eleven domains, compressed for the morning of the interview — every primitive,
          formula, mnemonic and trade-off on a few dense, scannable pages.</div>
        <div class="chips">{chips}</div>
        <div class="cover-meta" style="margin-top:auto">
          <div class="m">Night-Before Edition<b>11 domains · 1 sitting</b></div>
          <div class="m" style="text-align:center">Read time<b>~20 minutes</b></div>
          <div class="m" style="text-align:right">Level<b>SWE → Staff</b></div>
        </div>
      </div></section>""")

    # topic cards
    cards, special = [], []
    for tl, body in secs:
        m = re.match(r"(\d+)\.\s+(.*)", tl)
        if m:
            cards.append(topic_card(int(m.group(1)), m.group(2).strip(), body))
        else:
            special.append((tl, body))

    pages.append(f"""<section class="page"><div class="body">
      <div class="hero"><div class="eyebrow">The 11 Domains · At a Glance</div>
      <div class="shead"><div><div class="tt" style="font-size:25px">Core Recall</div></div></div></div>
      <div class="cards">{''.join(cards)}</div></div></section>""")

    # specials: cross-topic table + leaderboard + golden rule
    blocks = ""
    for tl, body in special:
        clean = re.sub(r"^[^\x00-\x7f]+\s*", "", tl).strip()
        if "Highest-Frequency" in tl or "Highest" in tl:
            blocks += f'<div class="eyebrow">Priorities</div><h3 class="csub">{html.escape(clean)}</h3>{leaderboard(body)}'
        else:
            inner = mag.convert_section_body(body)
            blocks += f'<div class="eyebrow">Connections</div><h3 class="csub">{html.escape(clean)}</h3>{inner}'
    pages.append(f"""<section class="page"><div class="body">{blocks}</div></section>""")

    extra = EXTRA_CSS + "\n.csub{font-family:'Space Grotesk';font-size:15px;font-weight:700;color:#0f1730;margin:2px 0 8px;}"
    return ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><style>"
            + mag.FONTS + ACC_CSS + mag.SHARED_CSS + extra + "</style></head><body>" + "".join(pages) + "</body></html>")

def render():
    out_html = mag.HERE / "_cheat.html"
    out_html.write_text(build(), encoding="utf-8")
    out_pdf = ROOT / "CHEATSHEET.pdf"
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}","--virtual-time-budget=25000","--run-all-compositor-stages-before-draw",
        str(out_html)], check=True, capture_output=True)
    out_html.unlink()
    info = subprocess.run(["pdfinfo", str(out_pdf)], capture_output=True, text=True).stdout
    print("CHEATSHEET.pdf:", re.search(r"Pages:\s+(\d+)", info).group(1), "pages ·", out_pdf.stat().st_size//1024, "KB")

if __name__ == "__main__":
    import sys
    if "--html" in sys.argv:
        sys.stdout.write(build())
    else:
        render()

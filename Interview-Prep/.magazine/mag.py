# -*- coding: utf-8 -*-
"""Generic markdown -> premium magazine PDF converter (fonts embedded, flow-safe pages).
Renders ASCII-art code fences as framed DIAGRAM cards, real code as highlighted code cards,
blockquotes as typed callouts, and all tables in a styled treatment."""
import re, html, pathlib, sys, subprocess, hashlib, importlib.util
import markdown as md

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
FONTS = (HERE / "fonts_embedded.css").read_text()

# ----------------------------- color helpers (derive theme shades) -----------------------------
def _rgb(h): h = h.lstrip("#"); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def _hex(t): return "#%02x%02x%02x" % t
def mix(c1, c2, t): a, b = _rgb(c1), _rgb(c2); return _hex(tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3)))
def shades(acc):
    W, K = "#ffffff", "#0b1020"
    return dict(bg=mix(acc, W, .93), z=mix(acc, W, .965), bd=mix(acc, W, .68),
                tx=mix(acc, K, .34), d=mix(acc, K, .30))

# ----------------------------- syntax highlighter -----------------------------
KW = set("""public private protected static final void class new return if else while for try catch finally
synchronized volatile transient import package throws throw extends implements interface abstract enum
int long short byte boolean char float double true false null this super var def with as global nonlocal
lambda async await yield from in is and or not None True False pass raise except elif del self print func
const auto using namespace template struct typename std include define operator nullptr bool unsigned
do switch case break continue default goto sizeof type range len append map filter""".split())
TOK = re.compile(r"""(?P<comment>//[^\n]*|\#[^\n]*)|(?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[^`]*`)
|(?P<anno>@\w+)|(?P<num>\b\d+\.?\d*[LlFfUu]*\b)|(?P<ident>[A-Za-z_]\w*)""", re.VERBOSE)

def hl(code):
    out, pos = [], 0
    for m in TOK.finditer(code):
        if m.start() > pos: out.append(html.escape(code[pos:m.start()]))
        kind = m.lastgroup; txt = html.escape(m.group())
        if kind == "ident":
            raw = m.group()
            cls = "k" if raw in KW else ("t" if raw[0].isupper() else
                  ("fn" if code[m.end():m.end()+1] == "(" else None))
            out.append(f'<span class="{cls}">{txt}</span>' if cls else txt)
        else:
            out.append(f'<span class="{kind[0]}">{txt}</span>')
        pos = m.end()
    out.append(html.escape(code[pos:]))
    return "".join(out)

DIAG_CHARS = set("─│┌┐└┘├┤┬┴┼━┃┏┓┗┛╔╗╚╝║═╠╣╦╩╬▲▼◄►◀▶↑↓→←↔⟶⟵⇄⇆⇒�`·•◆◇○●□■┄┈╎╌")
def is_diagram(code):
    chars = set(code)
    if chars & DIAG_CHARS: return True
    arrows = code.count("->") + code.count("=>") + code.count("──") + code.count("│")
    return arrows >= 3 and ("{" not in code and ";" not in code)

_OV = {}   # per-topic hand-built diagram overrides: {ascii-hash: html}
def dia_key(code): return hashlib.md5(code.strip("\n").strip().encode()).hexdigest()[:12]
def load_overrides(n):
    p = HERE / "diagrams" / f"d{n:02d}.py"
    if not p.exists(): return {}
    spec = importlib.util.spec_from_file_location(f"d{n}", p)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return getattr(m, "D", {})

def render_code(code, lang):
    code = code.strip("\n")
    # In these notes, real code is always language-tagged; untagged fences are diagrams/ASCII art.
    if not lang:
        ov = _OV.get(dia_key(code))
        if ov: return ov
        cap = "Pseudocode" if ((";" in code or "==" in code) and not (set(code) & set("┌│─►▼└├"))) else "Diagram"
        return (f'<div class="dia"><div class="cap"><span class="ddot"></span>{cap}</div>'
                f'<pre class="ascii">{html.escape(code)}</pre></div>')
    barlang = f'<span class="lang">{html.escape(lang)}</span>' if lang else ''
    dots = '<span class="dots"><i></i><i></i><i></i></span>'
    return (f'<div class="code"><div class="codebar">{dots}{barlang}</div><pre>{hl(code)}</pre></div>')

# ----------------------------- callout typing -----------------------------
def callout_class(text):
    t = text.lower()
    if any(w in t for w in ["takeaway","remember this","key insight","pro tip","interview tip"]): return "c-take","★ Takeaway"
    if any(w in t for w in ["trap","mistake","pitfall","warning","gotcha","never ","don't","beware"]): return "c-warn","▲ Watch out"
    if any(w in t for w in ["analogy","think of","like a ","imagine"]): return "c-ana","⟡ Analogy"
    if any(w in t for w in ["mental model","rule of thumb"]): return "c-model","◈ Mental model"
    return "c-key","◆ Key idea"

# ----------------------------- markdown -> styled html -----------------------------
def convert_section_body(body):
    # pull fenced code first
    blocks = {}
    def stash(m):
        lang = (m.group(1) or "").strip()
        key = f"@@CODE{len(blocks)}@@"
        blocks[key] = render_code(m.group(2), lang)
        return "\n\n" + key + "\n\n"
    body = re.sub(r"```([\w+-]*)\n(.*?)```", stash, body, flags=re.DOTALL)
    h = md.markdown(body, extensions=["tables", "sane_lists"])
    # blockquotes -> callouts
    def cobq(m):
        inner = m.group(1)
        txt = re.sub("<[^>]+>", " ", inner)
        cls, lab = callout_class(txt)
        return f'<div class="callout {cls}"><div class="ch">{lab}</div>{inner}</div>'
    h = re.sub(r"<blockquote>(.*?)</blockquote>", cobq, h, flags=re.DOTALL)
    # restore code/diagram blocks (un-wrap stray <p> around placeholder)
    for k, v in blocks.items():
        h = h.replace(f"<p>{k}</p>", v).replace(k, v)
    return h

def split_sections(text):
    # drop auto TOC block
    text = re.sub(r"\n## Table of Contents\n.*?(?=\n## )", "\n", text, flags=re.DOTALL)
    parts = re.split(r"\n## (?=\S)", text)
    secs = []
    for p in parts[1:]:
        line, _, rest = p.partition("\n")
        title = re.sub(r"\s*\{#.*\}", "", line).strip()
        if title.lower().startswith("table of contents"): continue
        # strip leading separators
        rest = re.sub(r"^\s*(-{3,}\s*)+", "", rest)
        rest = rest.rsplit("\n---", 1)[0] if rest.strip().endswith("---") else rest
        secs.append((title, rest))
    return secs

# ----------------------------- shared CSS -----------------------------
SHARED_CSS = r"""
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
@page{size:A4;margin:15mm 15mm 14mm;}
@page cover{margin:0;}
html,body{margin:0;padding:0;}
:root{--ink:#0b1020;--paper:#fff;--mist:#f5f7fb;--text:#1e2538;--muted:#5b6478;--line:#e6e9f2;
  --gold:#f59e0b;--teal:#0ea5a4;--coral:#f43f5e;--violet:#8b5cf6;}
body{font-family:'Inter',system-ui,sans-serif;color:var(--text);font-size:10.2px;line-height:1.5;}
.page{position:relative;break-after:page;}
.page:last-child{break-after:auto;}
.pad{display:block;}
.body{display:block;}
h1,h2,h3,h4{font-family:'Space Grotesk','Inter',sans-serif;letter-spacing:-.01em;}
b,strong{font-weight:700;color:#0f1730;} em{font-style:italic;color:#33405f;}
.mono{font-family:'JetBrains Mono',monospace;}
.foot{margin-top:24px;padding-top:8px;border-top:1px solid var(--line);display:flex;justify-content:space-between;
  font-size:7.6px;letter-spacing:.14em;text-transform:uppercase;color:#9aa3b7;font-weight:600;break-inside:avoid;}
.foot .pn{font-family:'Space Grotesk';color:var(--acc);}

/* cover */
.cover{page:cover;position:relative;overflow:hidden;break-after:page;color:#fff;
  background:radial-gradient(120% 90% at 80% -10%,#222a48 0%,#0b1020 55%),
  radial-gradient(90% 70% at 8% 112%,#1c2342 0%,rgba(11,16,32,0) 60%),var(--ink);}
.cover:last-child{break-after:auto;}
.cover .grid{position:absolute;inset:0;background-image:linear-gradient(#ffffff0a 1px,transparent 1px),
  linear-gradient(90deg,#ffffff0a 1px,transparent 1px);background-size:26px 26px;mask:linear-gradient(180deg,#000,transparent 75%);}
.blob{position:absolute;border-radius:50%;filter:blur(9px);}
.cover-in{position:relative;padding:24mm 20mm;min-height:297mm;display:flex;flex-direction:column;}
.kicker{display:inline-flex;align-items:center;gap:8px;font-family:'Space Grotesk';font-weight:600;
  font-size:9px;letter-spacing:.3em;text-transform:uppercase;color:#aeb8e6;}
.kicker .pill{padding:4px 11px;border:1px solid #ffffff2e;border-radius:30px;background:#ffffff0d;color:#dde3ff;letter-spacing:.2em;}
.cover h1{font-size:52px;line-height:1;font-weight:700;margin:auto 0 0;letter-spacing:-.025em;max-width:170mm;}
.cover h1 .g{color:var(--acc);filter:brightness(1.32) saturate(1.05);}
.cover .sub{font-size:14px;color:#c4cce4;max-width:150mm;margin-top:15px;line-height:1.5;}
.cover-meta{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid #ffffff1f;padding-top:14px;}
.cover-meta .m{font-size:8.2px;letter-spacing:.16em;text-transform:uppercase;color:#8b96b8;font-weight:600;}
.cover-meta .m b{display:block;color:#eef1ff;font-family:'Space Grotesk';font-size:11px;letter-spacing:.04em;margin-top:3px;}
.tagrow{display:flex;gap:7px;flex-wrap:wrap;margin-top:20px;}
.tag{font-size:8.2px;font-weight:600;letter-spacing:.05em;padding:5px 10px;border-radius:7px;background:#ffffff12;color:#cfd6f3;border:1px solid #ffffff1a;}
.lanes{display:grid;gap:7px;margin-top:26px;}
.lane{display:flex;gap:5px;align-items:center;}
.lane .lab{width:46px;font-family:'JetBrains Mono';font-size:8px;color:#7e8ab5;}
.seg{height:11px;border-radius:3px;}

/* section header */
.eyebrow{font-family:'Space Grotesk';font-weight:600;font-size:8.4px;letter-spacing:.26em;
  text-transform:uppercase;color:var(--acc);margin-bottom:4px;}
.shead{display:flex;align-items:flex-start;gap:14px;margin-bottom:13px;}
.snum{flex:none;font-family:'Space Grotesk';font-weight:700;font-size:13px;color:#fff;width:34px;height:34px;border-radius:10px;
  display:flex;align-items:center;justify-content:center;background:linear-gradient(135deg,var(--acc),var(--acc2));}
.shead .tt{font-size:22px;font-weight:700;line-height:1.06;color:#0f1730;}

/* body typography */
.body h3{font-size:13px;font-weight:700;color:#0f1730;margin:15px 0 6px;padding-left:11px;border-left:4px solid var(--acc);}
.body h4{font-size:11px;font-weight:700;color:#28324d;margin:11px 0 4px;}
.body p{margin:6px 0;}
.body ul,.body ol{margin:6px 0 6px 17px;padding:0;}
.body li{margin:3px 0;}
.body a{color:var(--acc);text-decoration:none;}
.body hr{display:none;}
.body img{max-width:100%;}

/* tables */
table{width:100%;border-collapse:separate;border-spacing:0;margin:11px 0;font-size:8.8px;border-radius:11px;overflow:hidden;
  box-shadow:0 0 0 1px var(--line);break-inside:avoid;}
thead th{background:linear-gradient(135deg,var(--acc-d),var(--acc));color:#fff;text-align:left;padding:8px 10px;
  font-family:'Space Grotesk';font-weight:600;font-size:8.4px;}
table{box-shadow:0 0 0 1px var(--acc-bd);}
tbody td{padding:7px 10px;border-top:1px solid var(--acc-bd);vertical-align:top;}
tbody tr:nth-child(even){background:var(--acc-z);} td b{color:#16204a;}

/* callouts */
.callout{border-radius:12px;padding:11px 13px 11px 14px;margin:11px 0;position:relative;border:1px solid var(--line);break-inside:avoid;}
.callout .ch{font-family:'Space Grotesk';font-weight:700;font-size:9px;letter-spacing:.1em;text-transform:uppercase;margin-bottom:3px;}
.callout p{margin:2px 0;font-size:9.6px;} .callout ul{margin:4px 0 2px 16px;} .callout li{font-size:9.4px;}
.callout::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;border-radius:12px 0 0 12px;}
.c-key{background:#f3f5ff;border-color:#e3e7ff;}.c-key::before{background:var(--acc);}.c-key .ch{color:var(--acc);}
.c-take{background:#fff7e8;border-color:#ffe9bf;}.c-take::before{background:var(--gold);}.c-take .ch{color:#b9770a;}
.c-ana{background:#e9faf8;border-color:#cdeeea;}.c-ana::before{background:var(--teal);}.c-ana .ch{color:#0a7d7c;}
.c-warn{background:#fff0f2;border-color:#ffd7dd;}.c-warn::before{background:var(--coral);}.c-warn .ch{color:#c81e3c;}
.c-model{background:#f6f0ff;border-color:#e7d9ff;}.c-model::before{background:var(--violet);}.c-model .ch{color:#7c3aed;}

/* code + diagram */
.code{border-radius:11px;overflow:hidden;margin:10px 0;box-shadow:0 6px 18px #0b102014;break-inside:avoid;}
.codebar{background:#10162b;display:flex;align-items:center;gap:9px;padding:6px 12px;}
.codebar .dots{display:flex;gap:5px;} .codebar .dots i{width:8px;height:8px;border-radius:50%;display:block;}
.dots i:nth-child(1){background:#ff5f57;}.dots i:nth-child(2){background:#febc2e;}.dots i:nth-child(3){background:#28c840;}
.codebar .lang{margin-left:auto;font-family:'Space Grotesk';font-size:7.6px;letter-spacing:.16em;text-transform:uppercase;color:#7c89b5;}
.code pre{margin:0;background:#0d1326;color:#cdd6f4;padding:11px 13px;font-family:'JetBrains Mono';font-size:8.2px;line-height:1.6;white-space:pre;overflow:hidden;}
.code .c{color:#6b7699;font-style:italic;}.code .s{color:#9ece6a;}.code .k{color:#c4a3ff;}
.code .t{color:#7dcfff;}.code .fn{color:#7aa2f7;}.code .n{color:#ff9e64;}.code .a{color:#e0af68;}
.dia{border:1px solid var(--acc-bd);border-radius:12px;padding:11px 14px 12px;background:var(--acc-bg);
  margin:11px 0;break-inside:avoid;box-shadow:inset 3px 0 0 var(--acc);}
.dia .cap{font-family:'Space Grotesk';font-weight:700;font-size:8px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--acc-d);margin-bottom:8px;display:flex;align-items:center;gap:7px;}
.dia .cap .ddot{width:8px;height:8px;border-radius:50%;background:var(--acc);display:inline-block;
  box-shadow:0 0 0 3px var(--acc-bd);}
.dia pre.ascii{margin:0;font-family:'JetBrains Mono';font-size:8px;line-height:1.5;color:var(--acc-tx);
  font-weight:500;white-space:pre;overflow:hidden;}

/* ============ REAL DIAGRAM TOOLKIT (hand-built figures) ============ */
.fig{border:1px solid var(--acc-bd);border-radius:13px;padding:14px 15px 15px;margin:12px 0;
  background:linear-gradient(180deg,#ffffff,var(--acc-bg));break-inside:avoid;}
.fig .figcap{font-family:'Space Grotesk';font-weight:700;font-size:8px;letter-spacing:.16em;text-transform:uppercase;
  color:var(--acc-d);margin-bottom:12px;display:flex;align-items:center;gap:8px;}
.fig .figcap::before{content:"";width:8px;height:8px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 3px var(--acc-bd);}
.fig .fignote{font-size:8.2px;color:var(--muted);margin-top:10px;text-align:center;}
.frow{display:flex;align-items:center;gap:9px;justify-content:center;flex-wrap:wrap;}
.frow.sb{justify-content:space-between;}
.fcol{display:flex;flex-direction:column;gap:8px;}
.node{border:1px solid var(--acc-bd);border-radius:10px;background:#fff;padding:8px 12px;text-align:center;
  box-shadow:0 1px 3px #0b102010;min-width:54px;}
.node .nt{font-family:'Space Grotesk';font-weight:700;font-size:9.5px;color:#10182f;line-height:1.1;}
.node .ns{font-size:7.6px;color:var(--muted);margin-top:2px;}
.node.acc{background:linear-gradient(135deg,var(--acc),var(--acc2));border:none;}
.node.acc .nt{color:#fff;} .node.acc .ns{color:#ffffffd6;}
.node.soft{background:var(--acc-bg);}
.ar{color:var(--acc);font-weight:800;font-size:16px;line-height:1;}
.ar-d{color:var(--acc);font-weight:800;font-size:15px;text-align:center;line-height:1;}
.chip{display:inline-block;font-family:'JetBrains Mono';font-size:7.6px;font-weight:600;padding:2px 7px;border-radius:20px;
  background:var(--acc-bg);border:1px solid var(--acc-bd);color:var(--acc-d);}

/* sequence / handshake */
.seq{position:relative;padding:2px 6px 4px;}
.seq::before,.seq::after{content:"";position:absolute;top:26px;bottom:8px;border-left:1.4px dashed var(--acc-bd);}
.seq::before{left:24%;} .seq::after{right:24%;}
.seqhead{display:flex;justify-content:space-between;padding:0 6px 8px;}
.seqhead span{font-family:'Space Grotesk';font-weight:700;font-size:9.6px;color:#fff;background:var(--acc);
  padding:4px 12px;border-radius:7px;}
.seqmsg{position:relative;height:15px;margin:11px 0;}
.seqmsg .t{position:absolute;left:50%;transform:translateX(-50%);top:-8px;font-family:'JetBrains Mono';font-size:7.6px;
  color:var(--acc-tx);background:var(--acc-bg);padding:1px 7px;border-radius:4px;white-space:nowrap;z-index:2;}
.seqmsg::before{content:"";position:absolute;left:24%;right:24%;top:8px;border-top:1.6px solid var(--acc);}
.seqmsg.dash::before{border-top-style:dashed;opacity:.8;}
.seqmsg.r::after,.seqmsg.l::after{content:"";position:absolute;top:3.5px;width:0;height:0;
  border-top:5px solid transparent;border-bottom:5px solid transparent;}
.seqmsg.r::after{right:24%;border-left:8px solid var(--acc);transform:translateX(1px);}
.seqmsg.l::after{left:24%;border-right:8px solid var(--acc);transform:translateX(-1px);}
.seqmsg.note .t{color:var(--muted);background:#fff;border:1px dashed var(--acc-bd);}
.seqmsg.note::before{display:none;}

/* layered stack */
.stack{display:flex;flex-direction:column;gap:5px;}
.stk{display:flex;align-items:center;gap:11px;border-radius:9px;padding:8px 12px;background:#fff;
  border:1px solid var(--acc-bd);box-shadow:0 1px 2px #0b10200a;}
.stk .si{font-family:'Space Grotesk';font-weight:700;font-size:8.4px;color:#fff;background:var(--acc);
  width:18px;height:18px;border-radius:6px;display:flex;align-items:center;justify-content:center;flex:none;}
.stk .sn{font-family:'Space Grotesk';font-weight:700;font-size:9.2px;color:#10182f;min-width:78px;}
.stk .sd{font-size:8.2px;color:var(--muted);}
.stk.hl{background:linear-gradient(135deg,var(--acc-bg),#fff);}

/* tier / architecture columns */
.tiers{display:flex;align-items:stretch;gap:9px;}
.tier{flex:1;border:1px dashed var(--acc-bd);border-radius:11px;padding:9px;background:var(--acc-bg);}
.tier .th{font-family:'Space Grotesk';font-weight:700;font-size:8.2px;letter-spacing:.06em;text-transform:uppercase;
  color:var(--acc-d);text-align:center;margin-bottom:7px;}
.tier .fcol{gap:6px;}
/* timeline / gantt / proportional bars */
.gantt{display:flex;flex-direction:column;gap:6px;}
.gantt .gr{display:flex;align-items:center;gap:9px;}
.gantt .gl{width:52px;font-family:'Space Grotesk';font-weight:700;font-size:8.2px;color:#10182f;flex:none;}
.track{flex:1;height:17px;border-radius:7px;background:var(--acc-bg);display:flex;overflow:hidden;border:1px solid var(--acc-bd);}
.gseg{height:100%;display:flex;align-items:center;justify-content:center;font-family:'JetBrains Mono';font-size:7px;
  color:#fff;border-right:1.5px solid #ffffff66;}
.gseg.a{background:var(--acc);} .gseg.b{background:var(--acc2);} .gseg.m{background:var(--acc-bd);color:var(--acc-d);}
/* inline svg figures auto-center & theme via currentColor */
.fig svg{display:block;margin:2px auto 0;max-width:100%;height:auto;color:var(--acc);}
.matrix{display:grid;gap:5px;}
.cell{border:1px solid var(--acc-bd);border-radius:7px;padding:6px 8px;text-align:center;background:#fff;font-size:8px;}
.cell.on{background:var(--acc);color:#fff;border-color:transparent;} .cell.hd{background:var(--acc-bg);font-weight:700;color:var(--acc-d);}

/* contents */
.toc{counter-reset:t;}
.toc .ti{display:flex;align-items:baseline;gap:12px;padding:7.5px 0;border-bottom:1px solid var(--line);}
.toc .ti .tn{counter-increment:t;font-family:'Space Grotesk';font-weight:700;font-size:13px;color:var(--acc);width:28px;}
.toc .ti .tn::before{content:counter(t,decimal-leading-zero);}
.toc .ti .tx{font-family:'Space Grotesk';font-weight:600;font-size:11.5px;color:#0f1730;}
"""

# ----------------------------- page assembly -----------------------------
def build_html(cfg):
    global _OV
    _OV = load_overrides(cfg["n"])
    src = (ROOT / cfg["file"]).read_text(encoding="utf-8")
    h1 = re.search(r"^#\s+(.*)$", src, re.M).group(1)
    title_full = re.sub(r"\s*—.*$", "", h1).strip()
    intro = ""
    bq = re.search(r"\n>\s+(.*)", src)
    secs = split_sections(src)

    s = shades(cfg["acc"])
    accent_css = (f":root{{--acc:{cfg['acc']};--acc2:{cfg['acc2']};--acc-bg:{s['bg']};"
                  f"--acc-z:{s['z']};--acc-bd:{s['bd']};--acc-tx:{s['tx']};--acc-d:{s['d']};}}")
    foot_txt = title_full + "  ·  Interview Edition"
    page_css = (
        '@page{@bottom-left{content:"' + foot_txt + '";font-family:Inter,sans-serif;font-size:7px;'
        'letter-spacing:.1em;color:#9aa3b7;}@bottom-right{content:counter(page);'
        'font-family:"Space Grotesk",sans-serif;font-weight:600;font-size:8.5px;color:' + cfg["acc"] + ';}}'
        '@page cover{@bottom-left{content:none;}@bottom-right{content:none;}}')
    pages = []

    # lanes graphic
    import random; random.seed(cfg["n"])
    lanes = ""
    for r in range(4):
        cells = ""
        for _ in range(7):
            w = random.choice([12,16,20,22,14,18]); g = random.random() < .25
            col = "background:#ffffff14" if g else f"background:linear-gradient(90deg,{cfg['acc']},{cfg['acc2']})"
            cells += f'<div class="seg" style="width:{w}%;{col}"></div>'
        lanes += f'<div class="lane"><div class="lab">lane {r}</div>{cells}</div>'

    tags = "".join(f'<span class="tag">{t}</span>' for t in cfg["tags"])
    title_html = cfg.get("title_html") or f'{title_full}'
    pages.append(f"""<section class="page cover"><div class="grid"></div>
      <div class="blob" style="width:240px;height:240px;background:{cfg['acc']};top:-40px;right:-30px;opacity:.5;"></div>
      <div class="blob" style="width:200px;height:200px;background:{cfg['acc2']};bottom:120px;left:-50px;opacity:.4;"></div>
      <div class="blob" style="width:150px;height:150px;background:{cfg['acc']};bottom:-30px;right:50px;opacity:.28;"></div>
      <div class="cover-in">
        <div class="kicker"><span class="pill">Engineering Essentials</span><span>FAANG Interview Master Series</span></div>
        <h1>{title_html}</h1>
        <div class="sub">{cfg['sub']}</div>
        <div class="lanes">{lanes}</div>
        <div class="tagrow">{tags}</div>
        <div class="cover-meta">
          <div class="m">Volume {cfg['n']:02d}<b>The {title_full} Issue</b></div>
          <div class="m" style="text-align:center">Comprehensive<b>Deep dive + revision</b></div>
          <div class="m" style="text-align:right">Level<b>SWE → Staff</b></div>
        </div>
      </div></section>""")

    # contents
    toc = "".join(f'<div class="ti"><span class="tn"></span><span class="tx">{html.escape(t)}</span></div>'
                  for t, _ in secs)
    pages.append(f"""<section class="page"><div class="pad"><div class="body">
      <div class="eyebrow">In This Issue</div>
      <div class="shead"><div><div class="tt" style="font-size:27px">Contents</div></div></div>
      <div class="toc">{toc}</div></div>
    </div></section>""")

    # sections
    pnum = 3
    for i, (title, body) in enumerate(secs, 1):
        inner = convert_section_body(body)
        pages.append(f"""<section class="page"><div class="pad"><div class="body">
          <div class="eyebrow">Section {i:02d}</div>
          <div class="shead"><div class="snum">{i:02d}</div><div><div class="tt">{html.escape(title)}</div></div></div>
          {inner}</div>
        </div></section>""")
        pnum += 1

    # back cover
    pages.append(f"""<section class="page cover"><div class="grid"></div>
      <div class="blob" style="width:220px;height:220px;background:{cfg['acc']};bottom:-50px;left:-30px;opacity:.4;"></div>
      <div class="blob" style="width:170px;height:170px;background:{cfg['acc2']};top:80px;right:-40px;opacity:.28;"></div>
      <div class="cover-in" style="justify-content:center;text-align:center;align-items:center">
        <div class="kicker" style="justify-content:center"><span class="pill">Engineering Essentials</span></div>
        <h1 style="font-size:38px;margin:22px 0 0;text-align:center">Master the <span class="g">fundamentals.</span></h1>
        <div class="sub" style="text-align:center;margin:16px auto 0">Understand the <b>why</b> before the <b>how</b>.
          Connect every concept to a real system, an analogy, and a trade-off you can defend.</div>
        <div class="tagrow" style="justify-content:center;margin-top:24px">
          <span class="tag">Vol. {cfg['n']:02d} — {html.escape(title_full)}</span>
          <span class="tag">FAANG Interview Master Series</span></div>
      </div></section>""")

    return ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'><style>"
            + FONTS + accent_css + SHARED_CSS + page_css + "</style></head><body>" + "".join(pages) + "</body></html>")

def build(cfg):
    htmldoc = build_html(cfg)
    out_html = HERE / f"_tmp_{cfg['n']:02d}.html"
    out_html.write_text(htmldoc, encoding="utf-8")
    out_pdf = ROOT / cfg["out"]
    subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--no-pdf-header-footer",
        f"--print-to-pdf={out_pdf}","--virtual-time-budget=25000","--run-all-compositor-stages-before-draw",
        str(out_html)], check=True, capture_output=True)
    out_html.unlink()
    return out_pdf

def cfg_by_n(n):
    for c in CONFIGS:
        if c["n"] == int(n): return c
    raise KeyError(n)

# ----------------------------- per-topic configs -----------------------------
CONFIGS = [
 dict(n=2, file="02-operating-systems.md", out="OS-Magazine.pdf", acc="#10b981", acc2="#14b8a6",
   sub="Processes, scheduling, virtual memory &amp; the great illusion that every program runs alone.",
   title_html="Operating <span class='g'>Systems</span>",
   tags=["Process vs Thread","Scheduling","Virtual Memory","Paging","Context Switch","Deadlock","File Systems"]),
 dict(n=3, file="03-computer-networks.md", out="Networks-Magazine.pdf", acc="#3b82f6", acc2="#06b6d4",
   sub="From the TCP handshake to TLS, DNS, gRPC and HTTP/3 — what really happens when you type a URL.",
   title_html="Computer <span class='g'>Networks</span>",
   tags=["TCP vs UDP","TLS / SSL","DNS","HTTP/2 &amp; 3","REST vs gRPC","WebSockets","Load Balancing"]),
 dict(n=4, file="04-cloud-infrastructure.md", out="Cloud-Magazine.pdf", acc="#06b6d4", acc2="#3b82f6",
   sub="Containers, Kubernetes, service mesh, CI/CD and the three pillars of observability.",
   title_html="Cloud &amp; <span class='g'>Infrastructure</span>",
   tags=["Docker","Kubernetes","Service Mesh","CI/CD","IaC","Observability","SLI / SLO"]),
 dict(n=5, file="05-system-design.md", out="System-Design-Magazine.pdf", acc="#8b5cf6", acc2="#6366f1",
   sub="The framework, the building blocks and the trade-offs that win senior design rounds.",
   title_html="System <span class='g'>Design</span>",
   tags=["Scalability","Caching","Sharding","Replication","CAP","Message Queues","Microservices"]),
 dict(n=6, file="06-low-level-design.md", out="LLD-Magazine.pdf", acc="#f59e0b", acc2="#f97316",
   sub="OOP, SOLID and the design patterns that turn requirements into extensible, clean code.",
   title_html="Low-Level <span class='g'>Design</span>",
   tags=["OOP","SOLID","Design Patterns","UML","Clean Code","Extensibility"]),
 dict(n=7, file="07-distributed-systems.md", out="Distributed-Systems-Magazine.pdf", acc="#f43f5e", acc2="#ec4899",
   sub="CAP, consensus, consistent hashing and Raft — making many computers behave like one.",
   title_html="Distributed <span class='g'>Systems</span>",
   tags=["CAP","Consistent Hashing","Raft","Consensus","Quorum","Kafka","Service Discovery"]),
 dict(n=8, file="08-databases.md", out="Databases-Magazine.pdf", acc="#0d9488", acc2="#10b981",
   sub="SQL internals, indexing, ACID, isolation levels and the NoSQL families — when and why.",
   title_html="<span class='g'>Databases</span>",
   tags=["SQL &amp; Joins","Indexing","ACID","Isolation Levels","Locking","Replication","NoSQL"]),
 dict(n=9, file="09-performance-engineering.md", out="Performance-Magazine.pdf", acc="#f97316", acc2="#f59e0b",
   sub="Profiling, tail latency, Amdahl &amp; Little's laws — measure, find the bottleneck, then fix.",
   title_html="Performance <span class='g'>Engineering</span>",
   tags=["Profiling","Tail Latency","p99","USE / RED","Caching","Throughput","Memory Leaks"]),
 dict(n=10, file="10-security-fundamentals.md", out="Security-Magazine.pdf", acc="#ef4444", acc2="#f43f5e",
   sub="AuthN vs AuthZ, OAuth, JWT, encryption and the OWASP Top 10 — defense in depth.",
   title_html="Security <span class='g'>Fundamentals</span>",
   tags=["Auth","OAuth 2.0","JWT","Encryption","Hashing","OWASP Top 10","Secrets"]),
 dict(n=11, file="11-behavioral-leadership.md", out="Behavioral-Magazine.pdf", acc="#a855f7", acc2="#ec4899",
   sub="STAR stories, Amazon's leadership principles and the signals that pass the bar raiser.",
   title_html="Behavioral &amp; <span class='g'>Leadership</span>",
   tags=["STAR Method","Ownership","Conflict","Ambiguity","Leadership Principles","Impact"]),
]

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "--html":
        sys.stdout.write(build_html(cfg_by_n(sys.argv[2])))
        sys.exit(0)
    only = sys.argv[1:] if len(sys.argv) > 1 else None
    for cfg in CONFIGS:
        if only and str(cfg["n"]) not in only: continue
        p = build(cfg)
        size = p.stat().st_size // 1024
        info = subprocess.run(["pdfinfo", str(p)], capture_output=True, text=True).stdout
        pages = re.search(r"Pages:\s+(\d+)", info)
        print(f"  ✓ {cfg['out']:38} {pages.group(1) if pages else '?':>3} pages · {size} KB")

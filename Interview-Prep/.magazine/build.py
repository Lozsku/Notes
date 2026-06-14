# -*- coding: utf-8 -*-
"""Builds a premium magazine-style HTML for the Concurrency notes, fonts embedded."""
import re, html, pathlib

HERE = pathlib.Path(__file__).parent
_local = HERE / "fonts_embedded.css"
FONTS = (_local if _local.exists() else pathlib.Path("/tmp/fonts_embedded.css")).read_text()

# ---------- lightweight syntax highlighter ----------
KW = set("""public private protected static final void class new return if else while for try catch finally
synchronized volatile transient import package throws throw extends implements interface abstract enum
int long short byte boolean char float double true false null this super var def with as global nonlocal
lambda async await yield from in is and or not None True False pass raise except elif del print
const auto using namespace template struct typename std include define operator nullptr bool unsigned
do switch case break continue default goto sizeof""".split())

TOK = re.compile(r"""
   (?P<comment>//[^\n]*|\#[^\n]*)
 | (?P<string>"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*')
 | (?P<anno>@\w+)
 | (?P<num>\b\d+\.?\d*[LlFfUu]*\b)
 | (?P<ident>[A-Za-z_]\w*)
""", re.VERBOSE)

def hl(code, lang=""):
    code = code.strip("\n")
    out, pos = [], 0
    for m in TOK.finditer(code):
        if m.start() > pos:
            out.append(html.escape(code[pos:m.start()]))
        kind = m.lastgroup
        txt = html.escape(m.group())
        if kind == "ident":
            raw = m.group()
            if raw in KW:
                cls = "k"
            elif raw[0].isupper():
                cls = "t"
            elif re.match(r"^[a-z_]\w*$", raw) and code[m.end():m.end()+1] == "(":
                cls = "fn"
            else:
                cls = None
            out.append(f'<span class="{cls}">{txt}</span>' if cls else txt)
        else:
            out.append(f'<span class="{kind[0]}">{txt}</span>')
        pos = m.end()
    out.append(html.escape(code[pos:]))
    label = f'<span class="lang">{lang}</span>' if lang else ""
    dots = '<span class="dots"><i></i><i></i><i></i></span>'
    return (f'<div class="code"><div class="codebar">{dots}{label}</div>'
            f'<pre>{"".join(out)}</pre></div>')

CSS = r"""
*{box-sizing:border-box;-webkit-print-color-adjust:exact;print-color-adjust:exact;}
@page{size:A4;margin:0;}
html,body{margin:0;padding:0;}
:root{
  --ink:#0b1020; --ink2:#141a2e; --paper:#ffffff; --mist:#f5f7fb;
  --indigo:#6366f1; --indigo2:#818cf8; --violet:#8b5cf6; --teal:#0ea5a4;
  --gold:#f59e0b; --coral:#f43f5e; --rose:#fb7185; --green:#10b981;
  --text:#1e2538; --muted:#5b6478; --line:#e6e9f2;
}
body{font-family:'Inter',system-ui,sans-serif;color:var(--text);font-size:10.2px;line-height:1.5;}
.page{position:relative;width:210mm;min-height:297mm;overflow:hidden;page-break-after:always;
  background:var(--paper);display:flex;flex-direction:column;}
.page:last-child{page-break-after:auto;}
.pad{padding:15mm 15mm 11mm;flex:1;display:flex;flex-direction:column;}
h1,h2,h3,h4,.dh{font-family:'Space Grotesk','Inter',sans-serif;letter-spacing:-.01em;}
b,strong{font-weight:700;color:#0f1730;}
em{color:var(--indigo);font-style:normal;font-weight:600;}
.mono{font-family:'JetBrains Mono',monospace;}

/* footer + page number */
.foot{margin-top:auto;padding-top:9mm;display:flex;justify-content:space-between;
  font-size:7.6px;letter-spacing:.14em;text-transform:uppercase;color:#9aa3b7;font-weight:600;}
.foot .pn{font-family:'Space Grotesk';color:var(--indigo);}

/* ============ COVER ============ */
.cover{background:radial-gradient(120% 90% at 80% -10%,#243056 0%,#0b1020 55%),
  radial-gradient(90% 70% at 10% 110%,#2a1f4d 0%,rgba(11,16,32,0) 60%),var(--ink);color:#fff;}
.cover .grid{position:absolute;inset:0;background-image:linear-gradient(#ffffff0a 1px,transparent 1px),
  linear-gradient(90deg,#ffffff0a 1px,transparent 1px);background-size:26px 26px;mask:linear-gradient(180deg,#000,transparent 75%);}
.blob{position:absolute;border-radius:50%;filter:blur(8px);opacity:.5;}
.cover-in{position:relative;padding:22mm 18mm;min-height:297mm;flex:1;display:flex;flex-direction:column;}
.kicker{display:inline-flex;align-items:center;gap:8px;font-family:'Space Grotesk';font-weight:600;
  font-size:9px;letter-spacing:.32em;text-transform:uppercase;color:#a9b4ff;}
.kicker .pill{padding:4px 11px;border:1px solid #ffffff2e;border-radius:30px;background:#ffffff0d;color:#cdd5ff;letter-spacing:.22em;}
.cover h1{font-size:56px;line-height:.98;font-weight:700;margin:auto 0 0;letter-spacing:-.025em;}
.cover h1 .amp{color:#a5b4fc;}
.cover .sub{font-size:15px;color:#c4cce4;max-width:115mm;margin-top:16px;line-height:1.5;font-weight:400;}
.lane-wrap{margin-top:30px;}
.cover-meta{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;border-top:1px solid #ffffff1f;padding-top:14px;}
.cover-meta .m{font-size:8.4px;letter-spacing:.16em;text-transform:uppercase;color:#8b96b8;font-weight:600;}
.cover-meta .m b{display:block;color:#eef1ff;font-family:'Space Grotesk';font-size:11px;letter-spacing:.04em;margin-top:3px;}
.tagrow{display:flex;gap:7px;flex-wrap:wrap;margin-top:22px;}
.tag{font-size:8.2px;font-weight:600;letter-spacing:.06em;padding:5px 10px;border-radius:7px;background:#ffffff12;color:#c9d2f3;border:1px solid #ffffff1a;}

/* lanes graphic (interleaving threads) */
.lanes{display:grid;gap:7px;}
.lane{display:flex;gap:5px;align-items:center;}
.lane .lab{width:42px;font-family:'JetBrains Mono';font-size:8px;color:#7e8ab5;}
.seg{height:11px;border-radius:3px;}
.seg.i{background:linear-gradient(90deg,#6366f1,#818cf8);}
.seg.v{background:linear-gradient(90deg,#8b5cf6,#a78bfa);}
.seg.t{background:linear-gradient(90deg,#0ea5a4,#2dd4bf);}
.seg.g{background:#ffffff14;}

/* ============ section header ============ */
.shead{display:flex;align-items:flex-start;gap:14px;margin-bottom:14px;}
.snum{flex:none;font-family:'Space Grotesk';font-weight:700;font-size:13px;color:#fff;
  width:34px;height:34px;border-radius:10px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,var(--indigo),var(--violet));box-shadow:0 6px 16px #6366f140;}
.shead .tt{font-size:23px;font-weight:700;line-height:1.05;color:#0f1730;margin:1px 0 3px;}
.shead .st{font-size:10px;color:var(--muted);font-weight:500;max-width:150mm;}
.eyebrow{font-family:'Space Grotesk';font-weight:600;font-size:8.4px;letter-spacing:.28em;
  text-transform:uppercase;color:var(--indigo);margin-bottom:4px;}
.rule{height:3px;width:46px;border-radius:3px;background:linear-gradient(90deg,var(--indigo),var(--violet));margin:2px 0 0;}

h3.sub{font-size:13px;font-weight:700;color:#0f1730;margin:16px 0 7px;display:flex;align-items:center;gap:8px;}
h3.sub .ic{font-size:14px;}
p{margin:6px 0;}
.lead{font-size:11.5px;color:#39425c;line-height:1.55;}
.dropcap::first-letter{font-family:'Space Grotesk';font-weight:700;font-size:42px;float:left;line-height:.82;
  padding:3px 9px 0 0;color:var(--indigo);}

/* ============ callouts ============ */
.callout{border-radius:12px;padding:12px 14px 12px 15px;margin:11px 0;position:relative;border:1px solid var(--line);
  break-inside:avoid;}
.callout .ch{font-family:'Space Grotesk';font-weight:700;font-size:9px;letter-spacing:.12em;text-transform:uppercase;
  display:flex;align-items:center;gap:7px;margin-bottom:4px;}
.callout p{margin:2px 0;font-size:9.8px;}
.callout::before{content:"";position:absolute;left:0;top:0;bottom:0;width:4px;border-radius:12px 0 0 12px;}
.c-key{background:#eef0ff;border-color:#dfe3ff;} .c-key::before{background:var(--indigo);} .c-key .ch{color:var(--indigo);}
.c-take{background:#fff7e8;border-color:#ffe9bf;} .c-take::before{background:var(--gold);} .c-take .ch{color:#b9770a;}
.c-ana{background:#e9faf8;border-color:#cdeeea;} .c-ana::before{background:var(--teal);} .c-ana .ch{color:#0a7d7c;}
.c-warn{background:#fff0f2;border-color:#ffd7dd;} .c-warn::before{background:var(--coral);} .c-warn .ch{color:#c81e3c;}
.c-model{background:#f6f0ff;border-color:#e7d9ff;} .c-model::before{background:var(--violet);} .c-model .ch{color:#7c3aed;}

/* ============ tables ============ */
table{width:100%;border-collapse:separate;border-spacing:0;margin:11px 0;font-size:9px;border-radius:11px;overflow:hidden;
  box-shadow:0 0 0 1px var(--line);break-inside:avoid;}
thead th{background:linear-gradient(135deg,#4338ca,var(--indigo));color:#fff;text-align:left;padding:8px 10px;
  font-family:'Space Grotesk';font-weight:600;font-size:8.6px;letter-spacing:.04em;}
tbody td{padding:7px 10px;border-top:1px solid var(--line);vertical-align:top;}
tbody tr:nth-child(even){background:var(--mist);}
td b{color:#16204a;}

/* ============ card grids ============ */
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:11px;}
.grid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;}
.grid4{display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:9px;}
.card{border:1px solid var(--line);border-radius:12px;padding:12px;background:#fff;break-inside:avoid;}
.card .hd{font-family:'Space Grotesk';font-weight:700;font-size:10.5px;color:#0f1730;margin-bottom:3px;}
.card p{font-size:9px;color:#48516a;margin:3px 0 0;}

/* coffman letter cards */
.coff{border-radius:13px;padding:13px 12px;color:#fff;position:relative;overflow:hidden;break-inside:avoid;}
.coff .L{font-family:'Space Grotesk';font-weight:700;font-size:30px;line-height:1;opacity:.9;}
.coff .nm{font-weight:700;font-size:10px;margin-top:6px;font-family:'Space Grotesk';}
.coff .ds{font-size:8.3px;opacity:.92;margin-top:4px;line-height:1.4;}
.coff .fx{font-size:8px;margin-top:7px;padding-top:6px;border-top:1px solid #ffffff33;}
.coff .fx b{color:#fff;}

/* stat cards */
.stat{border:1px solid var(--line);border-radius:12px;padding:13px;background:linear-gradient(180deg,#fff,#fafbff);break-inside:avoid;}
.stat .big{font-family:'Space Grotesk';font-weight:700;font-size:24px;color:var(--indigo);line-height:1;}
.stat .lab{font-size:8.4px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:600;margin-top:5px;}
.stat .fm{font-family:'JetBrains Mono';font-size:9px;color:#33405f;margin-top:6px;background:var(--mist);padding:5px 7px;border-radius:6px;}

/* generic diagram frame */
.dia{border:1px solid var(--line);border-radius:12px;padding:13px;background:#fbfcff;margin:11px 0;break-inside:avoid;}
.dia .cap{font-family:'Space Grotesk';font-weight:600;font-size:8.4px;letter-spacing:.12em;text-transform:uppercase;
  color:var(--muted);margin-bottom:9px;display:flex;align-items:center;gap:7px;}
.dia .cap .dot{width:7px;height:7px;border-radius:2px;background:var(--indigo);}

/* concurrency vs parallelism panels */
.panel{border:1px solid var(--line);border-radius:11px;padding:11px;background:#fff;}
.panel .pt{font-family:'Space Grotesk';font-weight:700;font-size:10px;margin-bottom:8px;color:#0f1730;}
.core{display:flex;align-items:center;gap:5px;margin:4px 0;}
.core .cl{width:40px;font-family:'JetBrains Mono';font-size:7.6px;color:var(--muted);}
.blk{height:13px;border-radius:3px;display:flex;align-items:center;justify-content:center;color:#fff;font-size:7px;font-family:'JetBrains Mono';}
.b1{background:linear-gradient(90deg,#6366f1,#818cf8);} .b2{background:linear-gradient(90deg,#0ea5a4,#2dd4bf);}

/* sync cost ladder */
.ladder{display:flex;align-items:flex-end;gap:8px;margin:12px 0 4px;}
.rung{flex:1;text-align:center;}
.rung .bar{border-radius:7px 7px 0 0;background:linear-gradient(180deg,var(--indigo2),var(--indigo));}
.rung .nm{font-family:'Space Grotesk';font-weight:600;font-size:8.4px;margin-top:6px;color:#0f1730;}
.rung .ns{font-family:'JetBrains Mono';font-size:7.6px;color:var(--muted);}

/* memory model boxes */
.mm{display:flex;align-items:center;gap:9px;}
.mmbox{flex:1;border:1px dashed #c7cdde;border-radius:10px;padding:9px;text-align:center;background:#fff;}
.mmbox .t{font-family:'Space Grotesk';font-weight:600;font-size:8.4px;color:var(--muted);}
.mmbox .v{font-family:'JetBrains Mono';font-weight:700;font-size:13px;margin-top:3px;}
.v-hot{color:var(--coral);} .v-stale{color:var(--gold);} .v-ram{color:var(--muted);}

/* flow boxes */
.flow{display:flex;align-items:center;gap:6px;flex-wrap:wrap;}
.fbox{border:1px solid var(--line);border-radius:9px;padding:8px 10px;background:#fff;font-size:8.6px;text-align:center;flex:none;}
.fbox .ft{font-family:'Space Grotesk';font-weight:700;font-size:8.8px;color:#0f1730;}
.fbox .fs{font-size:7.6px;color:var(--muted);}
.arr{color:var(--indigo);font-weight:700;font-size:13px;}
.slots{display:flex;gap:4px;}
.slot{width:17px;height:21px;border-radius:5px;border:1px solid #cfd5e6;display:flex;align-items:center;
  justify-content:center;font-family:'JetBrains Mono';font-size:8px;color:#0f1730;background:#fff;}
.slot.full{background:linear-gradient(180deg,#818cf8,#6366f1);color:#fff;border-color:transparent;}

/* code */
.code{border-radius:11px;overflow:hidden;margin:10px 0;box-shadow:0 6px 20px #0b102014;break-inside:avoid;}
.codebar{background:#10162b;display:flex;align-items:center;gap:9px;padding:7px 12px;}
.codebar .dots{display:flex;gap:5px;} .codebar .dots i{width:8px;height:8px;border-radius:50%;display:block;}
.codebar .dots i:nth-child(1){background:#ff5f57;} .dots i:nth-child(2){background:#febc2e;} .dots i:nth-child(3){background:#28c840;}
.codebar .lang{margin-left:auto;font-family:'Space Grotesk';font-size:8px;letter-spacing:.16em;text-transform:uppercase;color:#7c89b5;}
.code pre{margin:0;background:#0d1326;color:#cdd6f4;padding:11px 13px;font-family:'JetBrains Mono';
  font-size:8.5px;line-height:1.62;white-space:pre;overflow:hidden;}
.code .c{color:#6b7699;font-style:italic;} .code .s{color:#9ece6a;} .code .k{color:#c4a3ff;}
.code .t{color:#7dcfff;} .code .fn{color:#7aa2f7;} .code .n{color:#ff9e64;} .code .a{color:#e0af68;}

/* analogy gallery */
.ana-grid{display:grid;grid-template-columns:1fr 1fr;gap:9px;}
.ana{display:flex;gap:10px;align-items:flex-start;border:1px solid var(--line);border-radius:11px;padding:10px 11px;background:#fff;break-inside:avoid;}
.ana .em{font-size:17px;flex:none;line-height:1;}
.ana .ax b{font-family:'Space Grotesk';font-size:9.6px;color:#0f1730;}
.ana .ax p{font-size:8.6px;color:#525c75;margin:2px 0 0;}

/* mnemonic cards */
.mn{border-radius:12px;padding:12px;background:linear-gradient(135deg,#161d36,#241a44);color:#fff;break-inside:avoid;}
.mn .word{font-family:'Space Grotesk';font-weight:700;font-size:18px;letter-spacing:.04em;color:#bcc6ff;}
.mn .sub{font-size:8.4px;color:#aab3d6;margin:2px 0 7px;}
.mn ul{margin:0;padding-left:0;list-style:none;}
.mn li{font-size:8.6px;margin:3px 0;color:#dce1f4;}
.mn li b{color:#fff;font-family:'JetBrains Mono';}

/* Q&A */
.qa{border:1px solid var(--line);border-radius:12px;padding:12px 13px;margin:10px 0;break-inside:avoid;background:#fff;}
.qa .q{font-family:'Space Grotesk';font-weight:700;font-size:10.6px;color:#0f1730;display:flex;gap:9px;align-items:flex-start;}
.qa .q .qb{flex:none;background:var(--indigo);color:#fff;font-size:8.4px;width:18px;height:18px;border-radius:6px;
  display:flex;align-items:center;justify-content:center;margin-top:1px;}
.qa .a{font-size:9px;color:#414b63;margin-top:6px;padding-left:27px;}
.qa .fu{font-size:8.3px;color:var(--muted);margin-top:6px;padding-left:27px;border-top:1px dashed var(--line);padding-top:6px;}
.qa .fu b{color:#7c3aed;}

/* good vs great */
.gg th:first-child{background:linear-gradient(135deg,#3a3550,#4a4060);}
.gg th:last-child{background:linear-gradient(135deg,#6d28d9,#4338ca);}
.gg td:last-child{background:#f6f2ff;}

/* connections chips */
.conn{display:grid;grid-template-columns:1fr 1fr;gap:9px;}
.conn .c2{border:1px solid var(--line);border-radius:11px;padding:10px 11px;background:#fff;break-inside:avoid;}
.conn .c2 .h{font-family:'Space Grotesk';font-weight:700;font-size:9.6px;color:var(--indigo);display:flex;gap:7px;align-items:center;}
.conn .c2 p{font-size:8.4px;color:#4d5670;margin:5px 0 0;}

/* ranked list */
.rank{counter-reset:r;}
.rank .ri{display:flex;gap:11px;align-items:center;padding:7px 0;border-bottom:1px solid var(--line);}
.rank .ri .rn{counter-increment:r;font-family:'Space Grotesk';font-weight:700;font-size:13px;color:var(--indigo);width:22px;}
.rank .ri .rn::before{content:counter(r,decimal-leading-zero);}
.rank .ri .rt{font-size:9.4px;font-weight:600;color:#1c2540;}
.rank .ri .rb{margin-left:auto;font-size:7.6px;letter-spacing:.08em;text-transform:uppercase;color:#fff;
  background:var(--violet);padding:3px 8px;border-radius:20px;font-weight:600;}

/* contents */
.toc{counter-reset:t;}
.toc .ti{display:flex;align-items:baseline;gap:12px;padding:8.5px 0;border-bottom:1px solid var(--line);}
.toc .ti .tn{counter-increment:t;font-family:'Space Grotesk';font-weight:700;font-size:14px;color:var(--indigo2);width:30px;}
.toc .ti .tn::before{content:counter(t,decimal-leading-zero);}
.toc .ti .tx{font-family:'Space Grotesk';font-weight:600;font-size:12px;color:#0f1730;}
.toc .ti .td{font-size:8.6px;color:var(--muted);margin-left:auto;text-align:right;max-width:78mm;}

.note{font-size:8.6px;color:var(--muted);font-style:italic;margin-top:4px;}
.kbd{font-family:'JetBrains Mono';font-size:8.4px;background:var(--mist);border:1px solid var(--line);
  border-radius:5px;padding:1px 5px;color:#33405f;}
.hl-y{background:linear-gradient(transparent 55%,#ffe08a 55%);padding:0 1px;font-weight:600;color:#1c2540;}
"""

def foot(n, total=11):
    return (f'<div class="foot"><span>Concurrency &amp; Multithreading · Interview Edition</span>'
            f'<span class="pn">{n:02d} / {total}</span></div>')

PAGES = []

# ============================== COVER ==============================
lanes = ""
pat = ["i v i v i v g i", "v g t i v t i v", "t i v g t i v i", "i v t i g v t v"]
for k,row in enumerate(pat):
    cells=""
    widths=[14,22,10,18,12,20,16,15]
    for j,c in enumerate(row.split()):
        cells+=f'<div class="seg {c}" style="width:{widths[j%len(widths)]}%"></div>'
    lanes+=f'<div class="lane"><div class="lab">core {k}</div>{cells}</div>'

PAGES.append(f"""
<section class="page cover">
  <div class="grid"></div>
  <div class="blob" style="width:240px;height:240px;background:#6366f1;top:-40px;right:-30px;"></div>
  <div class="blob" style="width:200px;height:200px;background:#8b5cf6;bottom:120px;left:-50px;opacity:.4;"></div>
  <div class="blob" style="width:160px;height:160px;background:#22d3ee;bottom:-40px;right:40px;opacity:.3;"></div>
  <div class="cover-in">
    <div class="kicker"><span class="pill">Engineering Essentials</span> <span>FAANG Interview Master Series</span></div>
    <h1>Concurrency<br><span class="amp">&amp;</span> Multithreading</h1>
    <div class="sub">From first principles to staff-level mastery — threads, locks, lock-free atomics,
      deadlocks and the mental models that win interviews at Google, Meta, Amazon, Apple &amp; beyond.</div>
    <div class="lane-wrap"><div class="lanes">{lanes}</div></div>
    <div class="tagrow">
      <span class="tag">Mutex &amp; Semaphore</span><span class="tag">Deadlock · MHNC</span>
      <span class="tag">Race Conditions</span><span class="tag">CAS &amp; Lock-Free</span>
      <span class="tag">Producer–Consumer</span><span class="tag">Thread Pools</span>
      <span class="tag">Memory Model</span><span class="tag">Python GIL</span>
    </div>
    <div class="cover-meta">
      <div class="m">Volume 01<b>The Concurrency Issue</b></div>
      <div class="m" style="text-align:center">Deep read ≈ 3–4 hrs<b>Revision ≈ 10 min</b></div>
      <div class="m" style="text-align:right">Level<b>SWE → Staff</b></div>
    </div>
  </div>
</section>""")

# ============================== CONTENTS + EDITORIAL ==============================
toc_items = [
  ("The Big Picture","Why concurrency exists — the power wall &amp; the latency wall"),
  ("Foundations","Concurrency vs parallelism · threads vs processes"),
  ("Synchronization &amp; Locks","Race conditions, mutex vs semaphore, when to spin"),
  ("Deadlock","The four Coffman conditions &amp; how to break them"),
  ("Classic Problems","Producer–consumer &amp; reader–writer, solved"),
  ("Going Lock-Free &amp; Fast","CAS, ABA, memory visibility, false sharing, the GIL"),
  ("Analogies &amp; Mnemonics","Memory hooks that survive interview pressure"),
  ("The Interview Room","Top questions, follow-ups &amp; good-vs-great answers"),
  ("Cheat Sheet","Ten-minute revision &amp; the ranked must-knows"),
]
toc_html=""
for t,d in toc_items:
    toc_html+=f'<div class="ti"><span class="tn"></span><span class="tx">{t}</span><span class="td">{d}</span></div>'

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">In This Issue</div>
  <div class="shead"><div><div class="tt" style="font-size:27px">Contents</div>
  <div class="rule"></div></div></div>
  <div class="toc">{toc_html}</div>

  <div class="callout c-key" style="margin-top:16px">
    <div class="ch">◆ Editor's Note — How to read this</div>
    <p>Read cover-to-cover for genuine understanding, or jump straight to <b>The Interview Room</b> and the
    <b>Cheat Sheet</b> for last-minute revision. Every concept is paired with a <b>real-world system</b>,
    an <b>analogy</b>, and the <b>exact follow-up</b> an interviewer will ask next.</p>
  </div>

  <h3 class="sub"><span class="ic">🧭</span> The One Idea That Ties It All Together</h3>
  <p class="lead dropcap">Concurrency is the art of making progress on many things at once. Parallelism is the
  luxury of <em>actually</em> doing them at the same instant. The first is a property of your <b>design</b>;
  the second is a property of your <b>hardware</b>. Almost every bug, primitive and interview question in this
  issue flows from one uncomfortable truth — <span class="hl-y">shared mutable state accessed without coordination
  is undefined behavior waiting to happen.</span></p>

  <div class="grid3" style="margin-top:12px">
    <div class="stat"><div class="big">2004</div><div class="lab">The Power Wall</div>
      <div class="fm">clock speeds stalled → cores multiplied</div></div>
    <div class="stat"><div class="big">10⁴–10⁶×</div><div class="lab">I/O vs CPU latency</div>
      <div class="fm">overlap waiting → throughput soars</div></div>
    <div class="stat"><div class="big">20×</div><div class="lab">Amdahl ceiling @ 5% serial</div>
      <div class="fm">speedup = 1 / (S + (1−S)/N)</div></div>
  </div>
  {foot(2)}
</div></section>""")

# ============================== FOUNDATIONS ==============================
cvp = ""
for lab,cls,blocks in [("Core 0","b1",[("T1",14),("T2",13),("T1",14),("T2",13),("T1",14)])]:
    pass
def core_row(label, segs):
    s=f'<div class="core"><span class="cl">{label}</span>'
    for txt,w,cls in segs:
        s+=f'<div class="blk {cls}" style="width:{w}%">{txt}</div>'
    return s+'</div>'

conc_panel = ('<div class="panel"><div class="pt">⟳ Concurrency · 1 core</div>'
  + core_row("core 0",[("T1",18,"b1"),("T2",17,"b2"),("T1",18,"b1"),("T2",17,"b2"),("T1",16,"b1")])
  + '<div class="note">interleaved — one at a time, switched fast</div></div>')
par_panel = ('<div class="panel"><div class="pt">⇉ Parallelism · 2 cores</div>'
  + core_row("core 0",[("T1",55,"b1"),("",0,"")][:1])
  + core_row("core 1",[("T2",55,"b2")])
  + '<div class="note">truly simultaneous — needs ≥2 cores</div></div>')

mutex_code = hl("""import threading
counter = 0
lock = threading.Lock()

def increment():
    global counter
    with lock:            # acquire on enter, release on exit
        counter += 1      # critical section: one thread at a time
# after 1000 threads -> counter == 1000, guaranteed""","python")

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 02 · Foundations</div>
  <div class="shead"><div class="snum">02</div><div>
    <div class="tt">Concurrency vs Parallelism</div>
    <div class="st">The single most-confused distinction in systems interviews — get it crisp in one sentence.</div>
  </div></div>

  <div class="grid2">{conc_panel}{par_panel}</div>

  <table><thead><tr><th>Dimension</th><th>Concurrency</th><th>Parallelism</th></tr></thead><tbody>
    <tr><td><b>Goal</b></td><td>Structure &amp; responsiveness</td><td>Speed &amp; throughput</td></tr>
    <tr><td><b>Requires</b></td><td>A scheduler &amp; context switching</td><td>Multiple physical CPU cores</td></tr>
    <tr><td><b>Example</b></td><td>Single-threaded event loop</td><td>Matrix multiply across 8 cores</td></tr>
    <tr><td><b>Risk</b></td><td>Races, deadlocks</td><td>False sharing, sync overhead</td></tr>
  </tbody></table>

  <div class="callout c-model"><div class="ch">◈ Mental Model</div>
    <p>Concurrency is about <b>design</b>; parallelism is about <b>execution</b>. A single-core machine can be
    concurrent but <b>never</b> parallel. Say exactly this in the interview.</p></div>

  <h3 class="sub"><span class="ic">🧵</span> Threads vs Processes</h3>
  <p>A <b>thread</b> is the smallest unit of CPU scheduling — it shares the process's heap, code and file
  descriptors but owns its <b>stack, registers and program counter</b>. A <b>process</b> is an isolated address space.</p>

  <div class="dia"><div class="cap"><span class="dot"></span>Process memory — what's shared vs private</div>
    <div class="flow" style="gap:8px">
      <div class="fbox" style="background:#eef0ff;border-color:#dfe3ff"><div class="ft">SHARED</div>
        <div class="fs">Heap · Code · Globals · File descriptors</div></div>
      <span class="arr">→</span>
      <div class="fbox"><div class="ft">Thread 1</div><div class="fs">stack · regs · PC</div></div>
      <div class="fbox"><div class="ft">Thread 2</div><div class="fs">stack · regs · PC</div></div>
      <div class="fbox"><div class="ft">Thread 3</div><div class="fs">stack · regs · PC</div></div>
    </div></div>

  <div class="grid2">
    <div class="card"><div class="hd">⚡ Use threads when…</div>
      <p>Shared state &amp; speed matter, or you're overlapping I/O within one task. Context switch ≈ <b>100 ns</b>.
      Communication via shared memory — fast but dangerous.</p></div>
    <div class="card"><div class="hd">🛡️ Use processes when…</div>
      <p>You need isolation (a crash mustn't kill the parent), security boundaries, or different runtimes.
      Switch costs more; comms need IPC. <span class="kbd">nginx</span> worker processes.</p></div>
  </div>

  <div class="callout c-ana"><div class="ch">⟡ Analogy</div>
    <p><b>Thread</b> = a line cook at a station: shares the kitchen, keeps their own tickets and prep.
    <b>Process</b> = a separate restaurant: its own kitchen and pantry, reachable only by phone order (IPC).</p></div>
  {foot(3)}
</div></section>""")

# ============================== SYNCHRONIZATION + LOCKS ==============================
ladder = ""
rungs=[("Atomic / CAS","~1 ns",26),("Spinlock","~10 ns",42),("Mutex","~25 ns",60),
       ("Semaphore","~50 ns",80),("Monitor","~100 ns",104)]
for nm,ns,h in rungs:
    ladder+=f'<div class="rung"><div class="bar" style="height:{h}px"></div><div class="nm">{nm}</div><div class="ns">{ns}</div></div>'

race_code = hl("""// Lost update — a textbook race condition
T1: READ counter (=0)
T2: READ counter (=0)        // both read 0
T1: counter = 0+1 -> WRITE 1
T2: counter = 0+1 -> WRITE 1 // T1's update vanishes
// result = 1, expected = 2""","race")

sem_code = hl("""Semaphore pool = new Semaphore(10);  // 10 DB connections

void queryDB() {
    pool.acquire();        // blocks if 10 already in use
    try { /* use connection */ }
    finally { pool.release(); }   // ANY thread may release
}""","java")

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 03 · Synchronization</div>
  <div class="shead"><div class="snum">03</div><div>
    <div class="tt">The Cost of Being Correct</div>
    <div class="st">Coordination isn't free — pick the cheapest primitive that still guarantees safety.</div>
  </div></div>

  <p>A <b>race condition</b> exists whenever correctness depends on thread scheduling. It needs exactly three
  ingredients: <em>shared mutable state</em>, <em>at least one writer</em>, and <em>no synchronization</em>.
  Remove any one and the race disappears.</p>
  {race_code}

  <div class="dia"><div class="cap"><span class="dot"></span>Synchronization cost ladder — cheap → expensive</div>
    <div class="ladder">{ladder}</div>
    <div class="note">Rule of thumb: spin only when the critical section is shorter than a context switch (~1 µs).</div>
  </div>

  <h3 class="sub"><span class="ic">🔐</span> Mutex vs Semaphore vs Monitor</h3>
  <div class="grid3">
    <div class="card"><div class="hd" style="color:var(--indigo)">Mutex</div>
      <p><b>Binary lock with ownership.</b> Only the acquiring thread may release. Waiters sleep. The default
      tool for mutual exclusion. Re-locking yourself → deadlock.</p></div>
    <div class="card"><div class="hd" style="color:var(--teal)">Semaphore</div>
      <p><b>A counter (0…N), no ownership.</b> Any thread can signal. Perfect for resource pools and
      producer→consumer signalling.</p></div>
    <div class="card"><div class="hd" style="color:var(--violet)">Monitor</div>
      <p><b>Mutex + condition variables</b> bundled with data. Java's <span class="kbd">synchronized</span> is a
      monitor. One thread inside; others <span class="kbd">wait()</span> / <span class="kbd">notify()</span>.</p></div>
  </div>
  {sem_code}

  <div class="grid2">
    <div class="callout c-warn" style="margin:8px 0 0"><div class="ch">▲ Interview Trap</div>
      <p>Forget to release a mutex (an exception mid-critical-section) and every other thread blocks forever.
      <b>Always</b> use RAII / <span class="kbd">try-finally</span> / <span class="kbd">with lock:</span>.</p></div>
    <div class="callout c-take" style="margin:8px 0 0"><div class="ch">★ Interview Takeaway</div>
      <p>"Mutex has <b>ownership</b>, a semaphore is just a <b>counter</b>." You can build a mutex from a binary
      semaphore — but you lose priority inheritance &amp; ownership checks.</p></div>
  </div>
  {foot(4)}
</div></section>""")

# ============================== DEADLOCK ==============================
coff = [
  ("M","Mutual Exclusion","A resource can't be shared — one holder at a time.","Prefer shareable / read-only data","#6366f1","#4f46e5"),
  ("H","Hold &amp; Wait","Hold one resource while blocking on another.","Acquire all locks atomically, up front","#8b5cf6","#7c3aed"),
  ("N","No Preemption","A held resource can't be forcibly reclaimed.","Allow rollback &amp; retry (DBs do this)","#0ea5a4","#0d9488"),
  ("C","Circular Wait","A cycle of threads each waiting on the next.","<b>Impose a global lock order</b> — the practical fix","#f43f5e","#e11d48"),
]
coff_html=""
for L,nm,ds,fx,c1,c2 in coff:
    coff_html+=(f'<div class="coff" style="background:linear-gradient(135deg,{c1},{c2})">'
                f'<div class="L">{L}</div><div class="nm">{nm}</div><div class="ds">{ds}</div>'
                f'<div class="fx">Break it → {fx}</div></div>')

dl_code = hl("""// Lock order fixes everything: always A before B
lockA.lock();
lockB.lock();
//   ... use both resources ...
lockB.unlock();
lockA.unlock();
// No circular wait can ever form -> no deadlock""","java")

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 04 · Deadlock</div>
  <div class="shead"><div class="snum">04</div><div>
    <div class="tt">The Four Conditions — <span style="color:var(--indigo)">MHNC</span></div>
    <div class="st">All four must hold simultaneously. Break <b>any single one</b> and deadlock becomes impossible.</div>
  </div></div>

  <div class="grid4">{coff_html}</div>

  <div class="dia" style="margin-top:13px"><div class="cap"><span class="dot"></span>Circular wait — the cycle to hunt for</div>
    <div class="flow" style="justify-content:center;gap:10px">
      <div class="fbox" style="background:#eef0ff;border-color:#dfe3ff"><div class="ft">Thread 1</div><div class="fs">holds A · wants B</div></div>
      <span class="arr">⇄</span>
      <div class="fbox" style="background:#fff0f2;border-color:#ffd7dd"><div class="ft">Thread 2</div><div class="fs">holds B · wants A</div></div>
      <span class="arr" style="color:var(--coral)">⟲ both block forever</span>
    </div>
  </div>

  <div class="grid2">
    <div>
      <h3 class="sub" style="margin-top:10px"><span class="ic">🛠️</span> Breaking it in practice</h3>
      <div class="card" style="margin-bottom:8px"><div class="hd">1 · Lock ordering</div>
        <p>Acquire locks in one global order everywhere. Kills <b>circular wait</b>. The most common real-world fix.</p></div>
      <div class="card" style="margin-bottom:8px"><div class="hd">2 · Lock timeouts</div>
        <p><span class="kbd">tryLock(timeout)</span> — give up, back off, retry. Breaks <b>no-preemption</b>.</p></div>
      <div class="card"><div class="hd">3 · Detection</div>
        <p>Build a <b>wait-for graph</b>; find cycles. Java thread dumps &amp; DB lock monitors do this; DBs kill a victim.</p></div>
    </div>
    <div>{dl_code}
      <div class="callout c-ana" style="margin-top:9px"><div class="ch">⟡ Analogy</div>
        <p>Cook A grips the only pan and waits for the oven; Cook B owns the oven and waits for the pan. Both freeze —
        until one kitchen rule (always grab the pan <i>before</i> the oven = <b>lock ordering</b>) makes the standoff impossible.</p></div>
    </div>
  </div>

  <div class="grid2" style="margin-top:4px">
    <div class="callout c-key" style="margin:6px 0 0"><div class="ch">◆ Livelock</div>
      <p>Threads stay <b>active</b> but make no progress — two cooks in the doorway side-stepping the same way forever.
      Fix with <b>randomized backoff</b> (exactly what Ethernet CSMA/CD does).</p></div>
    <div class="callout c-key" style="margin:6px 0 0"><div class="ch">◆ Starvation</div>
      <p>One thread is perpetually skipped while others progress. Not deadlock. Fix with <b>fair FIFO</b>
      queuing — <span class="kbd">new ReentrantLock(true)</span>.</p></div>
  </div>
  {foot(5)}
</div></section>""")

# ============================== CLASSIC PROBLEMS ==============================
slots = '<div class="slots">' + ''.join(
    f'<div class="slot {"full" if i<3 else ""}">{"●" if i<3 else ""}</div>' for i in range(5)) + '</div>'

pc_code = hl("""empty = Semaphore(CAPACITY)   # free slots
full  = Semaphore(0)          # items ready
mutex = Semaphore(1)          # buffer guard

def producer(item):
    empty.acquire()           # 1) wait for a slot
    mutex.acquire()           # 2) THEN enter critical section
    buffer.append(item)
    mutex.release()
    full.release()            # signal: one more item

def consumer():
    full.acquire()
    mutex.acquire()
    item = buffer.pop(0)
    mutex.release()
    empty.release()           # signal: one more slot""","python")

rw_code = hl("""ReadWriteLock rw = new ReentrantReadWriteLock();
Lock r = rw.readLock(), w = rw.writeLock();

void read()  { r.lock();  try { /* many at once */ } finally { r.unlock(); } }
void write() { w.lock();  try { /* exclusive */    } finally { w.unlock(); } }""","java")

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 05 · Classic Problems</div>
  <div class="shead"><div class="snum">05</div><div>
    <div class="tt">Producer–Consumer &amp; Reader–Writer</div>
    <div class="st">The two synchronization set-pieces every interviewer keeps in their back pocket.</div>
  </div></div>

  <div class="dia"><div class="cap"><span class="dot"></span>Bounded buffer — two semaphores guard the counts, one mutex guards the data</div>
    <div class="flow" style="justify-content:space-between">
      <div class="fbox" style="background:#eef0ff;border-color:#dfe3ff"><div class="ft">Producer</div><div class="fs">empty.acquire → add</div></div>
      <span class="arr">→</span>
      <div style="text-align:center">{slots}<div class="note" style="text-align:center">buffer · cap 5</div></div>
      <span class="arr">→</span>
      <div class="fbox" style="background:#e9faf8;border-color:#cdeeea"><div class="ft">Consumer</div><div class="fs">full.acquire → remove</div></div>
    </div>
  </div>
  {pc_code}
  <div class="callout c-warn"><div class="ch">▲ The #1 mistake</div>
    <p>Order matters: acquire the <b>resource</b> semaphore (<span class="kbd">empty</span>/<span class="kbd">full</span>)
    <b>before</b> the <span class="kbd">mutex</span> — never after. Reverse it and a full buffer deadlocks instantly.</p></div>

  <h3 class="sub"><span class="ic">📚</span> Reader–Writer — many readers <i>or</i> one writer</h3>
  <div class="flow" style="margin:6px 0 9px">
    <div class="fbox" style="background:#e9faf8;border-color:#cdeeea"><div class="ft">READING</div><div class="fs">N readers share</div></div>
    <span class="arr">⇄</span>
    <div class="fbox"><div class="ft">UNLOCKED</div><div class="fs">idle</div></div>
    <span class="arr">⇄</span>
    <div class="fbox" style="background:#fff0f2;border-color:#ffd7dd"><div class="ft">WRITING</div><div class="fs">1 writer, exclusive</div></div>
  </div>
  {rw_code}
  <div class="callout c-take"><div class="ch">★ Senior Insight</div>
    <p>A <span class="kbd">ReadWriteLock</span> only wins when reads dominate (&gt;90%). Under heavy writes, the
    bookkeeping makes it <b>slower</b> than a plain mutex. <span class="kbd">StampedLock</span> adds optimistic
    reads for even better throughput when conflicts are rare.</p></div>
  {foot(6)}
</div></section>""")

# ============================== LOCK-FREE + MEMORY ==============================
cas_code = hl("""AtomicInteger counter = new AtomicInteger(0);
int cur, next;
do {
    cur  = counter.get();
    next = cur + 1;
} while (!counter.compareAndSet(cur, next));  // retry if it changed""","java")

mm = """<div class="mm">
  <div class="mmbox"><div class="t">Core 0 · L1$</div><div class="v v-hot">x = 1</div><div class="note">dirty, not flushed</div></div>
  <div class="arr">⇡⇣</div>
  <div class="mmbox"><div class="t">Core 1 · L1$</div><div class="v v-stale">x = 0</div><div class="note">reads stale value</div></div>
  <div class="arr">⇡⇣</div>
  <div class="mmbox"><div class="t">L3 / RAM</div><div class="v v-ram">x = 0</div><div class="note">source of truth</div></div>
</div>"""

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 06 · Going Lock-Free &amp; Fast</div>
  <div class="shead"><div class="snum">06</div><div>
    <div class="tt">CAS, ABA &amp; the Memory Model</div>
    <div class="st">Where senior and staff interviews actually live — no locks, just hardware guarantees.</div>
  </div></div>

  <div class="grid2">
    <div>
      <p><b>Compare-And-Swap</b> is the atom of lock-free code: read a value, compare to expected, write the new
      value <em>only</em> if it still matches — all in one uninterruptible instruction (<span class="kbd">CMPXCHG</span>).</p>
      {cas_code}
    </div>
    <div>
      <div class="callout c-warn" style="margin-top:0"><div class="ch">▲ The ABA Problem</div>
        <p>CAS sees <b>A</b>, succeeds — but in between another thread did A→B→A. Nothing "changed" by value, yet
        the world moved. Classic in lock-free lists (node freed &amp; reallocated at the same address).</p>
        <p style="margin-top:5px">Fix: attach a version stamp — <span class="kbd">AtomicStampedReference</span>.</p></div>
      <div class="callout c-model"><div class="ch">◈ Lock-free vs wait-free</div>
        <p><b>Lock-free:</b> <i>some</i> thread always progresses. <b>Wait-free:</b> <i>every</i> thread progresses
        in bounded steps — a stronger, harder guarantee.</p></div>
    </div>
  </div>

  <h3 class="sub"><span class="ic">🧠</span> Memory Visibility — the bug locks don't obviously fix</h3>
  <p>Each core caches independently. A write on Core 0 may be invisible to Core 1 for a while — a
  <b>visibility</b> problem, distinct from a race. <span class="kbd">volatile</span> (Java) forces a flush on write
  and a fresh read, plus ordering (happens-before). But it is <b>not</b> atomic — <span class="kbd">count++</span>
  still needs an atomic or a lock.</p>
  <div class="dia">{mm}</div>

  <div class="grid3">
    <div class="card"><div class="hd">⬛ False Sharing</div>
      <p>Two threads write different variables in the <b>same 64-byte cache line</b> → constant invalidation.
      Fix: <b>pad to 64 bytes</b> (LMAX Disruptor's whole design).</p></div>
    <div class="card"><div class="hd">🐍 Python GIL</div>
      <p>One thread runs Python bytecode at a time. Threads help <b>I/O</b>, not CPU. For CPU parallelism use
      <span class="kbd">multiprocessing</span> or C extensions (NumPy).</p></div>
    <div class="card"><div class="hd">⚙️ Thread Pools</div>
      <p>Reuse N workers off a queue. Size: <b>CPU-bound → cores+1</b>; <b>I/O-bound → cores×(1+wait/compute)</b>.
      Bound the queue or risk a memory leak.</p></div>
  </div>

  <div class="grid2" style="margin-top:3px">
    <div class="stat"><div class="big">cores + 1</div><div class="lab">CPU-bound pool size</div>
      <div class="fm"># threads ≈ cores + 1</div></div>
    <div class="stat"><div class="big">cores × (1+W/C)</div><div class="lab">I/O-bound pool size</div>
      <div class="fm">8 cores, 90% wait → 8×(1+9) = 80</div></div>
  </div>
  {foot(7)}
</div></section>""")

# ============================== ANALOGIES + MNEMONICS ==============================
analogies = [
  ("🔪","Mutex","The single razor-sharp chef's knife — only one cook holds it; the rest wait their turn to chop."),
  ("🔥","Semaphore","The stove's 4 burners — at most 4 dishes cook at once; free a burner and the next cook claims it."),
  ("🍳","Deadlock","Cook A holds the only pan and wants the oven; Cook B holds the oven and wants the pan — both freeze."),
  ("🚪","Livelock","Two cooks in the narrow doorway keep stepping the same way to yield — polite, but nobody passes."),
  ("🥚","Race Condition","Two cooks grab the last egg for different orders — one ticket goes out wrong."),
  ("🔔","Condition Var","The expo bell — cooks rest until 'order up!' rings, then wake and plate."),
  ("🎟️","CAS","'Is table 5's ticket still unclaimed?' — check the rail before grabbing; if taken, try the next."),
  ("👨‍🍳","Thread Pool","A fixed brigade pulling tickets off the rail — idle cooks wait, finished cooks grab the next."),
  ("🥕","False Sharing","Two cooks elbow over one cutting board for different veg — both slow, without truly sharing."),
  ("🍽️","Python GIL","A tiny kitchen with one stove — hire ten cooks, but only one can actually cook at a time."),
]
ana_html=""
for em,nm,tx in analogies:
    ana_html+=f'<div class="ana"><div class="em">{em}</div><div class="ax"><b>{nm}</b><p>{tx}</p></div></div>'

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 07 · Make It Stick</div>
  <div class="shead"><div class="snum">07</div><div>
    <div class="tt">Analogies &amp; Mnemonics</div>
    <div class="st">Under pressure you won't recall definitions — you'll recall pictures. Here are the ones that work.</div>
  </div></div>

  <div class="ana-grid">{ana_html}</div>

  <h3 class="sub" style="margin-top:14px"><span class="ic">🎯</span> The Mnemonics Worth Memorizing</h3>
  <div class="grid3">
    <div class="mn"><div class="word">MHNC</div><div class="sub">Deadlock's four conditions · "Make Him Never Circulate"</div>
      <ul><li><b>M</b> · Mutual exclusion</li><li><b>H</b> · Hold &amp; wait</li>
      <li><b>N</b> · No preemption</li><li><b>C</b> · Circular wait</li></ul></div>
    <div class="mn"><div class="word">SLVJ</div><div class="sub">Java happens-before edges</div>
      <ul><li><b>S</b> · thread Start</li><li><b>L</b> · Lock release→acquire</li>
      <li><b>V</b> · Volatile write→read</li><li><b>J</b> · thread Join</li></ul></div>
    <div class="mn"><div class="word">P / V</div><div class="sub">Semaphore ops</div>
      <ul><li><b>P</b> · acquire — wait in the <i>Post</i> queue</li>
      <li><b>V</b> · release — <i>Vacate</i>, next!</li>
      <li style="margin-top:6px;color:#aab3d6">CAS for counters · Lock for compounds</li></ul></div>
  </div>

  <div class="callout c-take" style="margin-top:13px"><div class="ch">★ One-liners to deploy verbatim</div>
    <p>• "<b>volatile</b> = visibility + ordering, <b>not</b> atomicity." &nbsp; • "Acquire the resource semaphore
    <b>before</b> the mutex." &nbsp; • "Always <span class="kbd">while</span>, never <span class="kbd">if</span>,
    around a wait." &nbsp; • "<b>Pad to 64</b> to kill false sharing."</p></div>
  {foot(8)}
</div></section>""")

# ============================== INTERVIEW ROOM ==============================
qas = [
 ("Q","What is a race condition — and how do you prevent it?",
  "Output depends on thread scheduling. Needs shared mutable state, ≥1 writer, no sync. Prevent by protecting the critical section (mutex), using lock-free atomics, or eliminating sharing (immutability / thread-local).",
  "Can you race on a single CPU? → <b>Yes</b> — a context switch can land mid read-modify-write."),
 ("Q","Explain the four deadlock conditions and how to break each.",
  "MHNC. Break circular wait via global lock ordering (the practical one), hold-and-wait by acquiring all locks at once, no-preemption via tryLock+timeout.",
  "How does a database detect deadlock? → Wait-for graph cycle detection, then kills the youngest/cheapest victim."),
 ("Q","Mutex vs semaphore?",
  "Mutex: binary, has ownership (acquirer must release), for mutual exclusion. Semaphore: counter 0–N, no ownership (any thread signals), for resource counting &amp; signalling.",
  "Build a mutex from a semaphore? → Yes, a binary semaphore by convention — but you lose ownership checks &amp; priority inheritance."),
 ("Q","Why volatile in a double-checked-locking singleton?",
  "Without it, a thread can observe a <i>partially constructed</i> object — the constructor's writes can be reordered after the reference write. Volatile's happens-before forbids that.",
  "When is volatile enough? → Single-variable publish/flag. Never for <span class='kbd'>count++</span> — use AtomicInteger."),
]
qa_html=""
for _,q,a,fu in qas:
    qa_html+=(f'<div class="qa"><div class="q"><span class="qb">Q</span><span>{q}</span></div>'
              f'<div class="a">{a}</div><div class="fu"><b>Follow-up →</b> {fu}</div></div>')

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 08 · The Interview Room</div>
  <div class="shead"><div class="snum">08</div><div>
    <div class="tt">Questions, Follow-ups &amp; What Separates Great</div>
    <div class="st">The exact prompts FAANG panels reuse — with the next question they'll fire.</div>
  </div></div>

  {qa_html}

  <h3 class="sub" style="margin-top:6px"><span class="ic">⬆️</span> Good vs Great</h3>
  <table class="gg"><thead><tr><th>A good answer says…</th><th>A great answer says…</th></tr></thead><tbody>
    <tr><td>"Use a mutex."</td><td>"Mutex here — but if reads dominate, a ReadWriteLock lifts throughput."</td></tr>
    <tr><td>"volatile makes it thread-safe."</td><td>"volatile gives visibility &amp; ordering, not compound atomicity."</td></tr>
    <tr><td>"Threads run concurrently."</td><td>"On N cores, up to N run in parallel; the rest context-switch."</td></tr>
    <tr><td>"Use a thread pool."</td><td>"I/O-bound → cores×(1+wait/compute); CPU-bound → cores+1."</td></tr>
    <tr><td>"Deadlock is two threads waiting."</td><td>"Four Coffman conditions; break circular wait with lock ordering."</td></tr>
  </tbody></table>

  <div class="callout c-key"><div class="ch">◆ How concurrency connects to the rest of your loop</div>
    <p><b>OS:</b> futexes, scheduling, copy-on-write fork. &nbsp; <b>System Design:</b> connection pools = semaphores,
    Kafka = distributed producer–consumer, Redis <span class="kbd">SET NX</span> = distributed mutex.
    &nbsp; <b>Databases:</b> <span class="kbd">SELECT FOR UPDATE</span> = pessimistic lock, version columns = CAS,
    MVCC = the reader–writer solution. &nbsp; <b>Distributed:</b> Raft/Paxos = a distributed condition variable.</p></div>
  {foot(9)}
</div></section>""")

# ============================== CHEAT SHEET ==============================
rows = [
 ("Mutex","Binary lock with ownership","lock()…unlock()","Forgetting release = deadlock"),
 ("Semaphore","Counter lock, any thread signals","wait()…signal()","Acquire resource sem before mutex"),
 ("Condition Var","Sleep &amp; release lock atomically","while(!cond) wait()","Use while, not if"),
 ("volatile","Visibility + ordering, no atomicity","volatile boolean ready","Not enough for count++"),
 ("CAS / Atomic","HW read-modify-write","compareAndSet(old,new)","The ABA problem"),
 ("Spinlock","Busy-wait loop","while(test_and_set()){}","Burns CPU; &lt;1 µs only"),
 ("Deadlock","Circular wait for resources","conditions: MHNC","Prevent via lock ordering"),
 ("Thread Pool","Pre-made workers + queue","cores+1 / cores×10","Unbounded queue = leak"),
 ("False Sharing","Diff vars, same cache line","pad to 64 bytes","Needs perf tools to spot"),
 ("Python GIL","One bytecode thread at a time","multiprocessing for CPU","I/O threads still help"),
 ("Producer–Consumer","Bounded-buffer sync","empty+full sems + mutex","Order: sem → mutex"),
 ("async/await","Cooperative coroutines","await gather(*tasks)","Sync code blocks the loop"),
]
rows_html=""
for c,d,k,g in rows:
    rows_html+=f'<tr><td><b>{c}</b></td><td>{d}</td><td class="mono" style="font-size:8px">{k}</td><td style="color:var(--coral)">{g}</td></tr>'

ranked = [("Race condition: define + example + fix","Everywhere"),
 ("Deadlock — MHNC + prevention","Senior+"),
 ("Producer–consumer implementation","Amazon · Google"),
 ("volatile vs synchronized vs atomic","Java shops"),
 ("Thread-pool sizing","Sys-design"),
 ("Mutex vs semaphore","Universal"),
 ("False sharing","Perf-heavy"),
 ("Condition var + while-loop","Depth signal"),
 ("Python GIL","Python shops"),
 ("CAS &amp; the ABA problem","Staff / lock-free")]
rank_html=""
for t,b in ranked:
    rank_html+=f'<div class="ri"><span class="rn"></span><span class="rt">{t}</span><span class="rb">{b}</span></div>'

PAGES.append(f"""
<section class="page"><div class="pad">
  <div class="eyebrow">Section 09 · Ten-Minute Revision</div>
  <div class="shead"><div class="snum">09</div><div>
    <div class="tt">The Cheat Sheet</div>
    <div class="st">Everything in this issue, compressed for the morning of the interview.</div>
  </div></div>

  <div class="grid3" style="margin-bottom:4px">
    <div class="callout c-warn" style="margin:0"><div class="ch">① Race conditions</div>
      <p>Shared mutable state + no sync → lock or atomics, or remove sharing.</p></div>
    <div class="callout c-model" style="margin:0"><div class="ch">② Deadlocks</div>
      <p>MHNC conditions → break circular wait with <b>lock ordering</b>.</p></div>
    <div class="callout c-key" style="margin:0"><div class="ch">③ Visibility</div>
      <p>CPU caches lie → volatile for flags, atomic/lock for compounds.</p></div>
  </div>

  <table><thead><tr><th style="width:17%">Concept</th><th style="width:30%">One-liner</th><th style="width:27%">Key code / formula</th><th style="width:26%">Gotcha</th></tr></thead>
  <tbody>{rows_html}</tbody></table>

  <div class="grid2">
    <div>
      <h3 class="sub"><span class="ic">🏆</span> Most-asked, ranked</h3>
      <div class="rank">{rank_html}</div>
    </div>
    <div>
      <h3 class="sub"><span class="ic">⏱️</span> If you have 60 seconds</h3>
      <div class="callout c-take" style="margin-top:6px"><div class="ch">★ Say these five things</div>
        <p>1 · Concurrency = design, parallelism = execution.<br>
        2 · A race needs shared state + a writer + no sync.<br>
        3 · Deadlock = MHNC; fix with lock ordering.<br>
        4 · Mutex owns; semaphore counts.<br>
        5 · volatile ≠ atomic; CAS for counters, locks for compounds.</p></div>
      <div class="callout c-ana" style="margin-top:8px"><div class="ch">⟡ Language quick-facts</div>
        <p><b>Java:</b> synchronized = monitor; Atomic* = CAS; virtual threads (21).<br>
        <b>Python:</b> GIL → multiprocessing for CPU.<br>
        <b>Go:</b> prefer channels; goroutines ≈ 2 KB stacks; <span class="kbd">go test -race</span>.</p></div>
    </div>
  </div>
  {foot(10)}
</div></section>""")

# ============================== BACK COVER ==============================
PAGES.append(f"""
<section class="page cover">
  <div class="grid"></div>
  <div class="blob" style="width:220px;height:220px;background:#6366f1;bottom:-50px;left:-30px;opacity:.4;"></div>
  <div class="blob" style="width:180px;height:180px;background:#22d3ee;top:80px;right:-40px;opacity:.28;"></div>
  <div class="cover-in" style="justify-content:center;text-align:center;align-items:center">
    <div class="kicker" style="justify-content:center"><span class="pill">Engineering Essentials</span></div>
    <h1 style="font-size:40px;margin:22px 0 0">Now go break<br>the <span class="amp">circular wait.</span></h1>
    <div class="sub" style="text-align:center;margin:18px auto 0">Master one primitive at a time. Understand the
      hardware beneath it. Always reach for the <b>cheapest</b> tool that's still correct.</div>
    <div class="tagrow" style="justify-content:center;margin-top:26px">
      <span class="tag">Vol. 01 — Concurrency &amp; Multithreading</span>
      <span class="tag">FAANG Interview Master Series</span>
    </div>
    <div class="note" style="color:#7e8ab5;margin-top:30px">Designed for deep study &amp; 10-minute revision · A4 · Self-contained</div>
  </div>
</section>""")

HTML = ("<!DOCTYPE html><html lang='en'><head><meta charset='utf-8'>"
        "<style>" + FONTS + CSS + "</style></head><body>" + "".join(PAGES) + "</body></html>")
import sys
if "--html" in sys.argv:
    sys.stdout.write(HTML)
else:
    out = HERE / "concurrency_magazine.html"
    out.write_text(HTML, encoding="utf-8")
    print("HTML written:", len(HTML)//1024, "KB ·", len(PAGES), "pages")

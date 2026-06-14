# -*- coding: utf-8 -*-
"""Live preview server for the interview magazines.

Run:   python3 serve.py        (then open http://localhost:8000 )

Edit any source file — a diagram override in diagrams/dNN.py, the CSS/layout in
mag.py, or the markdown notes — hit save, and the browser tab auto-reloads with
the freshly rendered magazine. Click "Export PDF" to write the final PDF.
"""
import sys, subprocess, pathlib, urllib.parse, os, html, json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = pathlib.Path(__file__).parent
ROOT = HERE.parent
PORT = int(os.environ.get("PORT", "8000"))
sys.path.insert(0, str(HERE))
import mag  # for CONFIGS / cfg lookup

# id -> (display title, accent, html-command, pdf-filename, [source files to watch])
def _md(n): return ROOT / mag.cfg_by_n(n)["file"]
ITEMS = {}
ITEMS["1"] = ("Concurrency & Multithreading", "#6366f1",
              [sys.executable, "build.py", "--html"], "Concurrency-Multithreading-Magazine.pdf",
              [HERE / "build.py"])
for c in mag.CONFIGS:
    n = str(c["n"])
    ITEMS[n] = (c["title_html"].replace("<span class='g'>", "").replace("</span>", ""), c["acc"],
                [sys.executable, "mag.py", "--html", n], c["out"],
                [HERE / "mag.py", HERE / "diagrams" / f"d{int(n):02d}.py", _md(c["n"])])
ITEMS["cheat"] = ("The Master Cheat Sheet", "#6366f1",
                  [sys.executable, "cheat.py", "--html"], "CHEATSHEET.pdf",
                  [HERE / "cheat.py", HERE / "mag.py", ROOT / "CHEATSHEET.md"])

ORDER = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11",
         "12", "13", "14", "15", "16", "17",
         "18", "19", "20", "21", "22", "23", "cheat"]

def mtime(id):
    files = ITEMS[id][4]
    return str(max((f.stat().st_mtime for f in files if f.exists()), default=0))

def edit_files(id):
    """(label, abspath) source files you can edit in the browser for this edition."""
    out = []
    if id == "1":
        out = [("build.py — flagship layout &amp; content", HERE / "build.py")]
    elif id == "cheat":
        out = [("CHEATSHEET.md — source", ROOT / "CHEATSHEET.md"),
               ("cheat.py — layout", HERE / "cheat.py")]
    else:
        c = mag.cfg_by_n(int(id))
        out.append((c["file"] + " — notes source (wording, sections, tables)", ROOT / c["file"]))
        d = HERE / "diagrams" / f"d{int(id):02d}.py"
        if d.exists():
            out.append((f"diagrams/d{int(id):02d}.py — hand-built figures (HTML/SVG)", d))
    out.append(("mag.py — ⚠ shared styling &amp; CONFIGS (affects ALL editions)", HERE / "mag.py"))
    return out

def _safe(p):
    p = pathlib.Path(p).resolve()
    return p if str(p).startswith(str(ROOT.resolve())) else None

def render_html(id, embed=False):
    title, acc, cmd, pdf, _ = ITEMS[id]
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        return (f"<pre style='font:12px monospace;color:#f87171;white-space:pre-wrap;padding:24px;"
                f"background:#0b1020'>⚠ Build error in {id}:\n\n{html.escape(r.stderr or r.stdout)}</pre>")
    return inject(r.stdout, id, title, embed)

PREVIEW_CSS = """
<style>
@media screen{
  html,body{background:#4b5563;}
  body{padding:46px 0 30px;}
  .page{width:210mm;min-height:297mm;margin:0 auto 20px;box-shadow:0 8px 34px #0009;
        overflow:hidden;position:relative;}
  .page:not(.cover){background:#fff;padding:15mm 15mm 14mm;}
}
</style>"""

def inject(htmldoc, id, title, embed=False):
    script = ("<script>let last=null;async function poll(){try{let r=await fetch('/mtime?id=__ID__&_='+Date.now());"
              "let t=await r.text();if(last!==null&&t!==last){var s=document.getElementById('__st');"
              "if(s)s.textContent='reloading…';location.reload();}last=t;}catch(e){}}setInterval(poll,1000);poll();"
              "</script>").replace("__ID__", id)
    htmldoc = htmldoc.replace("</head>", PREVIEW_CSS + "</head>", 1)
    if embed:
        return htmldoc.replace("<body>", "<body>" + script, 1)
    bar = ("<div style=\"position:fixed;top:0;left:0;right:0;z-index:99999;background:#0b1020;color:#cdd6f4;"
           "font:600 12px Inter,system-ui,sans-serif;padding:8px 16px;display:flex;gap:16px;align-items:center;"
           "box-shadow:0 2px 12px #0007\"><b style=\"color:#818cf8;letter-spacing:.1em\">● LIVE</b>"
           f"<span style=\"color:#9aa3b7\">{title}</span><span id=__st style=\"color:#6b7699\">watching for changes…</span>"
           "<a href=/ style=\"color:#a5b4fc;margin-left:auto;text-decoration:none\">← all editions</a>"
           f"<a href=/studio/{id} style=\"color:#fbbf24;text-decoration:none\">✦ Edit &amp; Render</a>"
           f"<a href=/pdf/{id} style=\"color:#fff;background:#6366f1;padding:5px 14px;border-radius:7px;"
           "text-decoration:none\">⬇ Export PDF</a></div><div style=height:38px></div>")
    return htmldoc.replace("<body>", "<body>" + bar + script, 1)

GROUPS = [("Core Topics", [str(i) for i in range(1, 12)]),
          ("Practice Packs · DSA · System Design · LLD", [str(i) for i in range(12, 18)]),
          ("AI / ML", [str(i) for i in range(18, 24)]),
          ("Cheat Sheet", ["cheat"])]

def index():
    def card(id):
        title, acc, _, pdf, _ = ITEMS[id]
        flag = " ★" if id in ("1",) else ""
        return (f"<div class=card style=\"--a:{acc}\"><div class=dot></div>"
                f"<div class=ct>{title}{flag}</div>"
                f"<div class=links><a href=/studio/{id}>✦ Studio</a>"
                f"<a href=/view/{id} target=_blank>▶ View</a>"
                f"<a href=/{pdf} target=_blank>📄 PDF</a></div></div>")
    sections = ""
    for name, ids in GROUPS:
        ids = [i for i in ids if i in ITEMS]
        if not ids: continue
        sections += f"<h2>{name}</h2><div class=grid>" + "".join(card(i) for i in ids) + "</div>"
    return f"""<!doctype html><html><head><meta charset=utf-8><title>Magazine Studio</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,system-ui,sans-serif;background:#0b1020;color:#e8ecf8;
  padding:42px 40px 60px;background-image:radial-gradient(60% 50% at 80% 0%,#1c2342 0%,#0b1020 60%)}}
h1{{font-family:'Space Grotesk',sans-serif;font-size:30px;margin:0 0 4px}}
h2{{font-family:'Space Grotesk',sans-serif;font-size:14px;color:#818cf8;letter-spacing:.06em;text-transform:uppercase;
  margin:30px 0 12px;border-bottom:1px solid #ffffff14;padding-bottom:7px}}
.sub{{color:#9aa3b7;margin:0;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));gap:13px;max-width:1180px}}
.card{{background:#141a2e;border:1px solid #ffffff14;border-radius:13px;padding:15px;transition:.15s}}
.card:hover{{border-color:var(--a)}}
.dot{{width:28px;height:28px;border-radius:8px;background:var(--a);margin-bottom:10px}}
.ct{{font-family:'Space Grotesk';font-weight:700;font-size:13.5px;min-height:34px}}
.links{{display:flex;gap:7px;margin-top:11px}}
.links a{{flex:1;text-align:center;text-decoration:none;font-size:11px;font-weight:600;padding:6px 4px;border-radius:7px;
  color:#cdd6f4;background:#ffffff10;border:1px solid #ffffff14}}
.links a:hover{{background:var(--a);color:#fff;border-color:var(--a)}}
code{{background:#ffffff14;padding:2px 6px;border-radius:5px;font-size:12px}}
.tip{{margin-top:34px;color:#9aa3b7;font-size:12.5px;line-height:1.7;max-width:820px}}
</style></head><body>
<h1>📖 Magazine Studio</h1>
<p class=sub><b>✦ Studio</b> = edit + live render side-by-side (Overleaf-style) · <b>▶ View</b> = full-screen render · <b>📄 PDF</b> = the exported file.</p>
{sections}
<div class=tip><b style="color:#a5b4fc">Editing from here:</b> click <b>✏️ Edit</b> on any edition → change the notes <code>.md</code> or the diagram file (<code>diagrams/dNN.py</code>) → <b>💾 Save</b> (or Ctrl/⌘+S). Any open <b>▶ Preview</b> tab auto-reloads within a second. Hit <b>⬇ Export PDF</b> in the preview bar to write the final PDF. Page breaks &amp; margins are finalized in the exported PDF.</div>
</body></html>"""

def editor(id):
    title = ITEMS[id][0]
    panels = ""
    for i, (label, p) in enumerate(edit_files(id)):
        content = html.escape(p.read_text(encoding="utf-8")) if p.exists() else ""
        panels += (f'<div class=panel><div class=phead><span class=lbl>{label}</span>'
                   f'<code class=path>{html.escape(str(p))}</code>'
                   f'<button class=save onclick="save({i})">💾 Save</button>'
                   f'<span class=st id=st{i}></span></div>'
                   f'<textarea id=ta{i} spellcheck=false data-path="{html.escape(str(p))}">{content}</textarea></div>')
    return f"""<!doctype html><html><head><meta charset=utf-8><title>Edit · {html.escape(title)}</title><style>
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,system-ui,sans-serif;background:#0b1020;color:#e8ecf8}}
.top{{position:sticky;top:0;background:#0b1020;border-bottom:1px solid #ffffff14;padding:11px 18px;display:flex;
  gap:16px;align-items:center;z-index:5}}
.top b{{font-family:'Space Grotesk'}} .top a{{color:#a5b4fc;text-decoration:none;font-size:13px}}
.top .pv{{color:#fff;background:#6366f1;padding:6px 14px;border-radius:7px;margin-left:auto}}
.wrap{{padding:18px;max-width:1000px;margin:0 auto}}
.panel{{background:#141a2e;border:1px solid #ffffff14;border-radius:11px;margin:0 0 16px;overflow:hidden}}
.phead{{display:flex;gap:12px;align-items:center;padding:10px 14px;background:#10162b;border-bottom:1px solid #ffffff10}}
.lbl{{font-weight:600;font-size:13px}} .path{{color:#6b7699;font-size:11px}}
.save{{margin-left:auto;background:#6366f1;color:#fff;border:0;border-radius:7px;padding:6px 14px;font-weight:600;
  cursor:pointer;font-size:12px}} .save:hover{{background:#818cf8}}
.st{{font-size:12px;min-width:64px}}
textarea{{width:100%;min-height:340px;max-height:70vh;border:0;background:#0d1326;color:#cdd6f4;
  font-family:'JetBrains Mono',monospace;font-size:12px;line-height:1.5;padding:14px;resize:vertical;display:block}}
</style></head><body>
<div class=top><b>✏️ Editing — {html.escape(title)}</b>
  <span style="color:#6b7699;font-size:12px">Ctrl/⌘+S saves the focused box · the preview tab auto-reloads</span>
  <a href=/ >← all editions</a>
  <a class=pv href=/view/{id} target=_blank>↗ Open live preview</a></div>
<div class=wrap>{panels}</div>
<script>
async function save(i){{
  const ta=document.getElementById('ta'+i), st=document.getElementById('st'+i);
  st.textContent='saving…'; st.style.color='#9aa3b7';
  try{{
    const r=await fetch('/save',{{method:'POST',headers:{{'Content-Type':'application/json'}},
      body:JSON.stringify({{path:ta.dataset.path,content:ta.value}})}});
    const j=await r.json();
    st.textContent=j.ok?'saved ✓':('⚠ '+j.error); st.style.color=j.ok?'#34d399':'#f87171';
  }}catch(e){{st.textContent='⚠ '+e; st.style.color='#f87171';}}
}}
document.addEventListener('keydown',e=>{{
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){{e.preventDefault();
    const ta=document.activeElement; if(ta&&ta.tagName==='TEXTAREA') save(ta.id.replace('ta',''));}}
}});
</script></body></html>"""

def studio(id):
    title = ITEMS[id][0]
    files = edit_files(id)
    meta_js = json.dumps([{"path": str(p)} for _, p in files])
    opts = "".join(f'<option value="{i}">{html.escape(l)}</option>' for i, (l, p) in enumerate(files))
    return f"""<!doctype html><html><head><meta charset=utf-8><title>Studio · {html.escape(title)}</title><style>
*{{box-sizing:border-box}} html,body{{height:100%;margin:0}}
body{{display:flex;flex-direction:column;font-family:Inter,system-ui,sans-serif;background:#0b1020;color:#e8ecf8}}
.bar{{display:flex;gap:11px;align-items:center;padding:8px 14px;border-bottom:1px solid #ffffff14;flex:none}}
.bar b{{font-family:'Space Grotesk'}} .bar a{{color:#a5b4fc;text-decoration:none;font-size:13px}}
select{{background:#141a2e;color:#e8ecf8;border:1px solid #ffffff1a;border-radius:7px;padding:6px 9px;font-size:12px;max-width:330px}}
.btn{{border:0;border-radius:7px;padding:7px 14px;font-weight:600;font-size:12px;cursor:pointer;color:#fff}}
.save{{background:#6366f1}} .save:hover{{background:#818cf8}} .exp{{background:#10b981;text-decoration:none}}
.st{{font-size:12px;color:#6b7699;min-width:120px}}
.auto{{font-size:12px;color:#9aa3b7;display:flex;gap:5px;align-items:center;cursor:pointer}}
.split{{flex:1;display:flex;min-height:0}}
.left{{width:46%;display:flex;flex-direction:column;min-width:240px}}
textarea{{flex:1;width:100%;border:0;background:#0d1326;color:#cdd6f4;font-family:'JetBrains Mono',monospace;
  font-size:12px;line-height:1.55;padding:14px;resize:none;outline:none;tab-size:2}}
.gut{{width:6px;background:#1c2342;cursor:col-resize;flex:none}} .gut:hover{{background:#6366f1}}
.right{{flex:1;min-width:280px}} iframe{{width:100%;height:100%;border:0;background:#4b5563}}
</style></head><body>
<div class=bar><b>✦ {html.escape(title)}</b>
  <select id=fsel onchange=switchFile()>{opts}</select>
  <button class="btn save" onclick=save()>💾 Save</button>
  <label class=auto><input type=checkbox id=auto checked> auto-render</label>
  <span class=st id=st></span>
  <a class="btn exp" href=/pdf/{id} target=_blank style="margin-left:auto">⬇ Export PDF</a>
  <a href=/ >← all</a></div>
<div class=split>
  <div class=left id=left><textarea id=ta spellcheck=false placeholder="loading…"></textarea></div>
  <div class=gut id=gut></div>
  <div class=right><iframe id=pv src="/view/{id}?embed=1"></iframe></div>
</div>
<script>
const FILES={meta_js}; let cur=0, dirty=false, tmr=null;
const ta=document.getElementById('ta'), st=document.getElementById('st');
async function load(i){{const r=await fetch('/file?path='+encodeURIComponent(FILES[i].path));
  ta.value=await r.text(); cur=i; dirty=false; st.textContent=FILES[i].path.split('/').pop();}}
async function save(){{if(!dirty){{st.textContent='no changes';return;}} st.textContent='saving…';
  const r=await fetch('/save',{{method:'POST',headers:{{'Content-Type':'application/json'}},
    body:JSON.stringify({{path:FILES[cur].path,content:ta.value}})}});
  const j=await r.json(); if(j.ok){{dirty=false;st.textContent='saved ✓ rendering…';rerender();}}
  else{{st.textContent='⚠ '+j.error;}}}}
function rerender(){{const pv=document.getElementById('pv');try{{pv.contentWindow.location.reload();}}catch(e){{pv.src=pv.src;}}}}
async function switchFile(){{const i=+document.getElementById('fsel').value; if(dirty) await save(); load(i);}}
ta.addEventListener('input',()=>{{dirty=true;st.textContent='● unsaved';
  if(document.getElementById('auto').checked){{clearTimeout(tmr);tmr=setTimeout(save,1400);}}}});
document.addEventListener('keydown',e=>{{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){{e.preventDefault();save();}}}});
const gut=document.getElementById('gut'),left=document.getElementById('left');let drag=false;
gut.onmousedown=()=>{{drag=true;document.body.style.userSelect='none';}};
document.onmouseup=()=>{{drag=false;document.body.style.userSelect='';}};
document.onmousemove=e=>{{if(drag){{let w=e.clientX/window.innerWidth*100;if(w>20&&w<80)left.style.width=w+'%';}}}};
load(0);
</script></body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def do_POST(self):
        if urllib.parse.urlparse(self.path).path != "/save":
            return self._send('{"ok":false,"error":"unknown"}', "application/json", 404)
        try:
            n = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(n) or b"{}")
            p = _safe(data.get("path", ""))
            if not p:
                return self._send('{"ok":false,"error":"path not allowed"}', "application/json", 403)
            p.write_text(data.get("content", ""), encoding="utf-8")
            return self._send('{"ok":true}', "application/json")
        except Exception as e:
            return self._send(json.dumps({"ok": False, "error": str(e)}), "application/json", 500)
    def _send(self, body, ctype="text/html; charset=utf-8", code=200):
        if isinstance(body, str): body = body.encode("utf-8")
        self.send_response(code); self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store"); self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        u = urllib.parse.urlparse(self.path); path = u.path
        q = urllib.parse.parse_qs(u.query)
        if path == "/" or path == "":
            return self._send(index())
        if path == "/mtime":
            id = q.get("id", ["1"])[0]
            return self._send(mtime(id) if id in ITEMS else "0", "text/plain")
        if path.startswith("/view/"):
            id = path[6:]
            if id not in ITEMS: return self._send("unknown id", "text/plain", 404)
            return self._send(render_html(id, q.get("embed", ["0"])[0] == "1"))
        if path.startswith("/studio/"):
            id = path[8:]
            if id not in ITEMS: return self._send("unknown id", "text/plain", 404)
            return self._send(studio(id))
        if path.startswith("/edit/"):
            id = path[6:]
            if id not in ITEMS: return self._send("unknown id", "text/plain", 404)
            return self._send(editor(id))
        if path == "/file":
            p = _safe(q.get("path", [""])[0])
            if not p or not p.exists(): return self._send("", "text/plain", 404)
            return self._send(p.read_text(encoding="utf-8"), "text/plain")
        if path.startswith("/pdf/"):
            id = path[5:]
            if id not in ITEMS: return self._send("unknown id", "text/plain", 404)
            self._build_pdf(id)
            self.send_response(302); self.send_header("Location", f"/{ITEMS[id][3]}"); self.end_headers(); return
        if path.endswith(".pdf"):
            f = ROOT / path.lstrip("/")
            if f.exists(): return self._send(f.read_bytes(), "application/pdf")
            return self._send("not found", "text/plain", 404)
        self._send("not found", "text/plain", 404)
    def _build_pdf(self, id):
        if id == "1":
            subprocess.run([sys.executable, "build.py"], cwd=HERE, capture_output=True)
            subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--no-pdf-header-footer",
                f"--print-to-pdf={ROOT/ITEMS['1'][3]}","--virtual-time-budget=20000",
                "--run-all-compositor-stages-before-draw","concurrency_magazine.html"], cwd=HERE, capture_output=True)
            (HERE / "concurrency_magazine.html").unlink(missing_ok=True)
        elif id == "cheat":
            subprocess.run([sys.executable, "cheat.py"], cwd=HERE, capture_output=True)
        else:
            subprocess.run([sys.executable, "mag.py", id], cwd=HERE, capture_output=True)

if __name__ == "__main__":
    print(f"\n  📖  Magazine Studio  →  http://localhost:{PORT}\n  (Ctrl-C to stop)\n")
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()

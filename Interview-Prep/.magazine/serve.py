# -*- coding: utf-8 -*-
"""Live preview server for the interview magazines.

Run:   python3 serve.py        (then open http://localhost:8000 )

Edit any source file — a diagram override in diagrams/dNN.py, the CSS/layout in
mag.py, or the markdown notes — hit save, and the browser tab auto-reloads with
the freshly rendered magazine. Click "Export PDF" to write the final PDF.
"""
import sys, subprocess, pathlib, urllib.parse, os
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
         "12", "13", "14", "15", "16", "17", "cheat"]

def mtime(id):
    files = ITEMS[id][4]
    return str(max((f.stat().st_mtime for f in files if f.exists()), default=0))

def render_html(id):
    title, acc, cmd, pdf, _ = ITEMS[id]
    r = subprocess.run(cmd, cwd=HERE, capture_output=True, text=True)
    if r.returncode != 0:
        return (f"<pre style='font:13px monospace;color:#c00;white-space:pre-wrap;padding:24px'>"
                f"Build error in {id}:\n\n{r.stderr or r.stdout}</pre>")
    return inject(r.stdout, id, title)

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

def inject(htmldoc, id, title):
    bar = ("<div style=\"position:fixed;top:0;left:0;right:0;z-index:99999;background:#0b1020;color:#cdd6f4;"
           "font:600 12px Inter,system-ui,sans-serif;padding:8px 16px;display:flex;gap:16px;align-items:center;"
           "box-shadow:0 2px 12px #0007\"><b style=\"color:#818cf8;letter-spacing:.1em\">● LIVE</b>"
           f"<span style=\"color:#9aa3b7\">{title}</span><span id=__st style=\"color:#6b7699\">watching for changes…</span>"
           "<a href=/ style=\"color:#a5b4fc;margin-left:auto;text-decoration:none\">← all editions</a>"
           f"<a href=/pdf/{id} style=\"color:#fff;background:#6366f1;padding:5px 14px;border-radius:7px;"
           "text-decoration:none\">⬇ Export PDF</a></div><div style=height:38px></div>")
    script = ("<script>let last=null;async function poll(){try{let r=await fetch('/mtime?id=__ID__&_='+Date.now());"
              "let t=await r.text();if(last!==null&&t!==last){document.getElementById('__st').textContent='reloading…';"
              "location.reload();}last=t;}catch(e){}}setInterval(poll,1000);poll();</script>").replace("__ID__", id)
    htmldoc = htmldoc.replace("</head>", PREVIEW_CSS + "</head>", 1)
    htmldoc = htmldoc.replace("<body>", "<body>" + bar + script, 1)
    return htmldoc

def index():
    cards = ""
    for id in ORDER:
        title, acc, _, pdf, _ = ITEMS[id]
        flag = " ★" if id == "1" else ""
        cards += (f"<a class=card href=/view/{id} style=\"--a:{acc}\">"
                  f"<div class=dot></div><div class=ct>{title}{flag}</div>"
                  f"<div class=cl>open live preview →</div></a>")
    return f"""<!doctype html><html><head><meta charset=utf-8><title>Magazine Studio</title>
<style>
*{{box-sizing:border-box}} body{{margin:0;font-family:Inter,system-ui,sans-serif;background:#0b1020;color:#e8ecf8;
  padding:48px 40px;background-image:radial-gradient(60% 50% at 80% 0%,#1c2342 0%,#0b1020 60%)}}
h1{{font-family:'Space Grotesk',sans-serif;font-size:30px;margin:0 0 4px}}
.sub{{color:#9aa3b7;margin:0 0 28px;font-size:14px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px;max-width:1100px}}
.card{{display:block;text-decoration:none;color:#e8ecf8;background:#141a2e;border:1px solid #ffffff14;
  border-radius:13px;padding:16px;position:relative;transition:.15s}}
.card:hover{{border-color:var(--a);transform:translateY(-2px)}}
.dot{{width:30px;height:30px;border-radius:8px;background:var(--a);margin-bottom:11px}}
.ct{{font-family:'Space Grotesk';font-weight:700;font-size:14px}}
.cl{{color:#6b7699;font-size:11px;margin-top:5px}}
code{{background:#ffffff14;padding:2px 6px;border-radius:5px;font-size:12px}}
.tip{{margin-top:30px;color:#9aa3b7;font-size:12.5px;line-height:1.7;max-width:760px}}
</style></head><body>
<h1>📖 Magazine Studio <span style="color:#6b7699;font-size:15px">· live preview</span></h1>
<p class=sub>Edit a source file → save → the open tab auto-refreshes. Click a card to start.</p>
<div class=grid>{cards}</div>
<div class=tip><b style="color:#a5b4fc">How to make small changes yourself:</b><br>
• <b>A diagram</b>: edit <code>.magazine/diagrams/dNN.py</code> (HTML/SVG keyed by hash). Run <code>python3 extract.py N</code> to list a topic's diagrams + keys.<br>
• <b>Colors / layout / fonts</b>: edit the CSS in <code>.magazine/mag.py</code> (the flagship is <code>build.py</code>).<br>
• <b>Wording / content</b>: edit the topic's <code>NN-*.md</code> in the parent folder.<br>
• The on-screen preview stacks content into A4-width pages; exact page breaks &amp; margins are finalized in the exported PDF.</div>
</body></html>"""

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
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
            return self._send(render_html(id))
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

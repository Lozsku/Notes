#!/usr/bin/env python3
"""
Resumable LaTeX build pipeline for the Interview-Prep notes.

  markdown  --pandoc-->  styled .tex  --tectonic-->  PDF

State is tracked in manifest.json so the job can be stopped and resumed
across sessions: each source's content hash is recorded, and a target is
rebuilt only when its source (or the shared style/template) changes.

Usage:
  python3 build.py            # build everything that is stale
  python3 build.py --force    # rebuild all
  python3 build.py --only 01  # build docs whose key contains "01"
  python3 build.py --status   # print manifest status table
"""
import argparse, hashlib, json, os, re, subprocess, sys, time
from pathlib import Path

ROOT     = Path(__file__).resolve().parent          # .../Notes/Latex
NOTES    = ROOT.parent                               # .../Notes
SRC      = NOTES / "Interview-Prep"
ASSETS   = ROOT / "assets"
TEXDIR   = ROOT / "tex"
PDFDIR   = ROOT / "pdf"
FIGDIR   = ROOT / "figures"
MANIFEST = ROOT / "manifest.json"
LOCALBIN = Path.home() / ".local" / "bin"

PANDOC   = str(LOCALBIN / "pandoc")
TECTONIC = str(LOCALBIN / "tectonic")
TEMPLATE = ASSETS / "template.tex"

# ----------------------------------------------------------------------
# Topic registry: source -> output key, title, kicker, big number, colors
# colors are (accent, accent2) hex without '#'
# ----------------------------------------------------------------------
REG = [
  # key,            src (rel to SRC),                              title,                                  kicker,                  num,  acc,      acc2
  ("00-index",      "00-INDEX.md",                                 "Master Index",                         "Study Roadmap",         "",   "6366f1","8b5cf6"),
  ("01-concurrency","01-concurrency-multithreading.md",            "Concurrency \\& Multithreading",       "Systems Track",         "01", "6366f1","8b5cf6"),
  ("02-os",         "02-operating-systems.md",                     "Operating Systems",                    "Systems Track",         "02", "0ea5a4","22d3ee"),
  ("03-networks",   "03-computer-networks.md",                     "Computer Networks",                    "Systems Track",         "03", "2563eb","60a5fa"),
  ("04-cloud",      "04-cloud-infrastructure.md",                  "Cloud \\& Infrastructure",             "Platform Track",        "04", "7c3aed","a78bfa"),
  ("05-system-design","05-system-design.md",                       "System Design",                        "Design Track",          "05", "db2777","f472b6"),
  ("06-lld",        "06-low-level-design.md",                      "Low-Level Design",                     "Design Track",          "06", "ea580c","fb923c"),
  ("12-oop",        "12-oop-concepts.md",                          "Object-Oriented Programming",          "Design Track",          "",   "0d9488","2dd4bf"),
  ("07-distributed","07-distributed-systems.md",                   "Distributed Systems",                  "Systems Track",         "07", "0891b2","22d3ee"),
  ("08-databases",  "08-databases.md",                             "Databases",                            "Data Track",            "08", "059669","34d399"),
  ("09-performance","09-performance-engineering.md",               "Performance Engineering",              "Systems Track",         "09", "d97706","fbbf24"),
  ("10-security",   "10-security-fundamentals.md",                 "Security Fundamentals",                "Platform Track",        "10", "dc2626","f87171"),
  ("11-behavioral", "11-behavioral-leadership.md",                 "Behavioral \\& Leadership",            "Soft-Skills Track",     "11", "9333ea","c084fc"),
  ("cheatsheet",    "CHEATSHEET.md",                               "The Grand Cheat Sheet",                "Last-Minute Revision",  "",   "111827","6366f1"),
  # DSA
  ("dsa-00-index",  "DSA/00-INDEX.md",                             "DSA — Index",                          "DSA Track",             "",   "be123c","fb7185"),
  ("dsa-01-patterns","DSA/01-patterns-and-templates.md",           "DSA Patterns \\& Templates",           "DSA Track",             "01", "be123c","fb7185"),
  ("dsa-02-ds",     "DSA/02-data-structures.md",                   "Data Structures",                      "DSA Track",             "02", "be123c","fb7185"),
  ("dsa-03-algos",  "DSA/03-algorithms-and-complexity.md",         "Algorithms \\& Complexity",            "DSA Track",             "03", "be123c","fb7185"),
  # AI-ML
  ("aiml-00-index", "AI-ML/00-INDEX.md",                           "AI / ML — Index",                      "AI/ML Track",           "",   "7c3aed","a78bfa"),
  ("aiml-01-fund",  "AI-ML/01-ml-fundamentals.md",                 "ML Fundamentals",                      "AI/ML Track",           "01", "7c3aed","a78bfa"),
  ("aiml-02-classic","AI-ML/02-classic-ml-algorithms.md",          "Classic ML Algorithms",                "AI/ML Track",           "02", "7c3aed","a78bfa"),
  ("aiml-03-dl",    "AI-ML/03-deep-learning.md",                   "Deep Learning",                        "AI/ML Track",           "03", "7c3aed","a78bfa"),
  ("aiml-04-tf",    "AI-ML/04-transformers-and-llms.md",           "Transformers \\& LLMs",                "AI/ML Track",           "04", "7c3aed","a78bfa"),
  ("aiml-05-genai", "AI-ML/05-llm-applications-genai.md",          "LLM Applications \\& GenAI",           "AI/ML Track",           "05", "7c3aed","a78bfa"),
  ("aiml-06-mlops", "AI-ML/06-mlops-and-ml-system-design.md",      "MLOps \\& ML System Design",           "AI/ML Track",           "06", "7c3aed","a78bfa"),
  # System Design Problems
  ("sdp-1",         "System-Design-Problems/part1-foundational.md","System Design Problems — Foundational","Design Track",          "I",  "db2777","f472b6"),
  ("sdp-2",         "System-Design-Problems/part2-advanced.md",    "System Design Problems — Advanced",     "Design Track",          "II", "db2777","f472b6"),
  # LLD Problems
  ("lld-coded",     "LLD-Problems/coded-solutions.md",             "LLD Problems — Coded Solutions",        "Design Track",          "",   "ea580c","fb923c"),
  # ---- new editions ----
  ("design-patterns","13-design-patterns.md",                      "Design Patterns",                      "Design Track",          "",   "0284c7","38bdf8"),
  ("api-design",    "14-api-design.md",                            "API Design",                           "Design Track",          "",   "4f46e5","818cf8"),
  ("caching",       "15-caching.md",                               "Caching",                              "Design Track",          "",   "c2410c","fb923c"),
  ("message-queues","16-message-queues.md",                        "Message Queues \\& Streaming",         "Design Track",          "",   "7c3aed","a78bfa"),
  ("testing",       "17-testing.md",                               "Testing \\& Code Quality",             "Quality Track",         "",   "16a34a","4ade80"),
  ("observability", "18-observability.md",                         "Observability",                        "Platform Track",        "",   "0891b2","22d3ee"),
  ("git",           "19-git-version-control.md",                   "Git \\& Dev Workflow",                 "Quality Track",         "",   "ea580c","fb923c"),
  ("linux",         "20-linux-cli.md",                             "Linux \\& the Command Line",           "Platform Track",        "",   "334155","64748b"),
  ("vector-databases","21-vector-databases.md",                    "Vector Databases \\& Embeddings",      "Data Track",            "",   "0d9488","2dd4bf"),
  ("ai-agents",     "AI-ML/07-ai-agents.md",                       "AI Agents \\& Tool Use",               "AI/ML Track",           "07", "7c3aed","a78bfa"),
  # Project: Kite Algo Trader
  ("ticker-prep",   "tickerAlgo/INTERVIEW_PREP.md",                "Kite Algo Trader — Interview Prep",    "Project Track",         "",   "0d9488","2dd4bf"),
  ("ticker-detailed","tickerAlgo/interview_detailed.md",           "Kite Algo Trader — Detailed Prep",     "Project Track",         "",   "0d9488","2dd4bf"),
]

# ----------------------------------------------------------------------
# Output folder per edition — keeps tex/ and pdf/ organised by concept.
# Every folder is exactly ONE level deep (figures referenced as ../../figures/).
# ----------------------------------------------------------------------
FOLDER = {
  "00-index": "_collection", "cheatsheet": "_collection",
  # foundations
  "12-oop": "foundations", "design-patterns": "foundations",
  # systems
  "01-concurrency": "systems", "02-os": "systems", "03-networks": "systems",
  "07-distributed": "systems", "09-performance": "systems",
  # infrastructure / ops
  "04-cloud": "infrastructure", "10-security": "infrastructure",
  "observability": "infrastructure", "linux": "infrastructure",
  # system design
  "05-system-design": "system-design", "06-lld": "system-design",
  "api-design": "system-design", "caching": "system-design",
  "message-queues": "system-design", "sdp-1": "system-design",
  "sdp-2": "system-design", "lld-coded": "system-design",
  # data
  "08-databases": "data", "vector-databases": "data",
  # dev practices
  "testing": "dev-practices", "git": "dev-practices",
  # behavioral
  "11-behavioral": "behavioral",
  # dsa
  "dsa-00-index": "dsa", "dsa-01-patterns": "dsa", "dsa-02-ds": "dsa", "dsa-03-algos": "dsa",
  # ai / ml
  "aiml-00-index": "ai-ml", "aiml-01-fund": "ai-ml", "aiml-02-classic": "ai-ml",
  "aiml-03-dl": "ai-ml", "aiml-04-tf": "ai-ml", "aiml-05-genai": "ai-ml",
  "aiml-06-mlops": "ai-ml", "ai-agents": "ai-ml",
  # project
  "ticker-prep": "tickerAlgo", "ticker-detailed": "tickerAlgo",
}
def folder_of(key): return FOLDER.get(key, "misc")
def texdir_for(key):
    d = TEXDIR / folder_of(key); d.mkdir(parents=True, exist_ok=True); return d
def pdfdir_for(key):
    d = PDFDIR / folder_of(key); d.mkdir(parents=True, exist_ok=True); return d

def sha(p: Path) -> str:
    return hashlib.sha1(p.read_bytes()).hexdigest()[:12]

def style_hash() -> str:
    h = hashlib.sha1()
    for f in [ASSETS/"interviewstyle.sty", TEMPLATE, ASSETS/"tablewidths.lua",
              ASSETS/"codelang.lua", FIGDIR/"figures.json", Path(__file__)]:
        if f.exists(): h.update(f.read_bytes())
    return h.hexdigest()[:12]

def load_manifest():
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text())
    return {"style": "", "docs": {}}

def save_manifest(m):
    MANIFEST.write_text(json.dumps(m, indent=2))

# ---- unicode -> LaTeX math (body serif lacks these glyphs; XeTeX has no
#      auto-fallback). Applied ONLY outside code, where DejaVu Mono renders
#      the originals fine. tex_math_dollars lets pandoc parse the $...$. ----
SYM = {
 "→":r"$\rightarrow$","←":r"$\leftarrow$","↔":r"$\leftrightarrow$","↑":r"$\uparrow$",
 "↓":r"$\downarrow$","⇒":r"$\Rightarrow$","⇐":r"$\Leftarrow$","⇔":r"$\Leftrightarrow$",
 "≤":r"$\leq$","≥":r"$\geq$","≈":r"$\approx$","≠":r"$\neq$","≡":r"$\equiv$",
 "∞":r"$\infty$","√":r"$\surd$","−":r"$-$","±":r"$\pm$","×":r"$\times$","÷":r"$\div$",
 "·":r"$\cdot$","∝":r"$\propto$","∈":r"$\in$","∉":r"$\notin$","∀":r"$\forall$",
 "∃":r"$\exists$","∇":r"$\nabla$","∂":r"$\partial$","∑":r"$\sum$","∏":r"$\prod$",
 "∫":r"$\int$","∩":r"$\cap$","∪":r"$\cup$","∅":r"$\varnothing$","⊆":r"$\subseteq$",
 "⊂":r"$\subset$","⊕":r"$\oplus$","⊗":r"$\otimes$","∘":r"$\circ$",
 "ℝ":r"$\mathbb{R}$","ℕ":r"$\mathbb{N}$","ℤ":r"$\mathbb{Z}$","ℚ":r"$\mathbb{Q}$","ℂ":r"$\mathbb{C}$",
 "α":r"$\alpha$","β":r"$\beta$","γ":r"$\gamma$","δ":r"$\delta$","ε":r"$\varepsilon$",
 "ζ":r"$\zeta$","η":r"$\eta$","θ":r"$\theta$","ι":r"$\iota$","κ":r"$\kappa$","λ":r"$\lambda$",
 "μ":r"$\mu$","ν":r"$\nu$","ξ":r"$\xi$","π":r"$\pi$","ρ":r"$\rho$","σ":r"$\sigma$","τ":r"$\tau$",
 "υ":r"$\upsilon$","φ":r"$\varphi$","χ":r"$\chi$","ψ":r"$\psi$","ω":r"$\omega$",
 "Γ":r"$\Gamma$","Δ":r"$\Delta$","Θ":r"$\Theta$","Λ":r"$\Lambda$","Ξ":r"$\Xi$","Π":r"$\Pi$",
 "Σ":r"$\Sigma$","Φ":r"$\Phi$","Ψ":r"$\Psi$","Ω":r"$\Omega$",
 "ᵢ":r"$_i$","ⱼ":r"$_j$","ₙ":r"$_n$","ₖ":r"$_k$","ₜ":r"$_t$","₀":r"$_0$","₁":r"$_1$",
 "₂":r"$_2$","₃":r"$_3$","ⁿ":r"$^n$","ᵀ":r"$^{\mathsf{T}}$","²":r"$^2$","³":r"$^3$",
 "⁴":r"$^4$","⁵":r"$^5$","⁶":r"$^6$","⁷":r"$^7$",
 "✓":r"$\checkmark$","✅":r"$\checkmark$","✔":r"$\checkmark$","✗":r"$\times$","✘":r"$\times$",
 "❌":r"$\times$","★":r"$\star$","⭐":r"$\star$","◆":r"$\blacklozenge$","◇":r"$\lozenge$",
 "◁":r"$\triangleleft$","◀":r"$\blacktriangleleft$","▶":r"$\blacktriangleright$",
 "─":"-","│":"|","├":"|","└":"|","┌":"|","┐":"|","┘":"|","•":r"$\bullet$",
 "①":"(1)","②":"(2)","③":"(3)","④":"(4)","⑤":"(5)","⑥":"(6)","⑦":"(7)","⑧":"(8)",
 "⑨":"(9)","⑩":"(10)","❶":"(1)","❷":"(2)","❸":"(3)","❹":"(4)","❺":"(5)",
}
def _strip_emoji(s: str) -> str:
    out = []
    for ch in s:
        o = ord(ch)
        if (0x1F000 <= o <= 0x1FAFF or 0x2600 <= o <= 0x27BF
                or 0x2B00 <= o <= 0x2BFF or 0xFE00 <= o <= 0xFE0F
                or 0x2300 <= o <= 0x23FF or o == 0x200D):
            continue
        out.append(ch)
    return "".join(out)
def latexify(text: str) -> str:
    text = _strip_emoji(text)
    for k, v in SYM.items():
        if k in text:
            text = text.replace(k, v)
    return text
def _code_aware(md: str) -> str:
    # split keeping fenced blocks and inline code spans intact (odd indices)
    parts = re.split(r"(```.*?```|`[^`\n]+`)", md, flags=re.DOTALL)
    return "".join(p if i % 2 else latexify(p) for i, p in enumerate(parts))

# untagged ``` fences that are clearly code (not ASCII diagrams) get a language
# so they are syntax-highlighted instead of rendered as plain verbatim. These
# notes are Python-dominant, so unknown code defaults to python.
_DIAGRAM_CHARS = set("─│┌┐└┘├┤┬┴┼╔╗╚╝═║▲▶◀▼↑↓←→╴╵┃━┏┓┗┛")
# strict: require actual code structure so prose/workflow lists aren't mis-tagged
_CODE_HINT = re.compile(
    r"(\bdef\s+\w+\s*\(|\bclass\s+\w+|\bimport\s+\w|#\s*include|\bstd::|::|->|=>|"
    r"\bself\.|\bprint\s*\(|\bprintln|\bcout\b|\bSystem\.|\bpublic\s+\w|\bvoid\s+\w|"
    r"\b\w+\s*=\s*[\w'\"\[{(]|[{};]|==|!=|<=|>=|\+=|-=|\breturn\s+\w+\s*[\[(.])",
    re.MULTILINE)

def _guess_lang(body: str) -> str:
    """Guess the language of an untagged code block from content signatures."""
    b = body
    low = b.lower()
    # SQL (keyword-led, case-insensitive)
    if re.search(r"(?im)^\s*(select|insert\s+into|update\s+\w+\s+set|delete\s+from|"
                 r"create\s+(table|index|database)|alter\s+table|with\s+\w+\s+as)\b", b):
        return "sql"
    if "#include" in b or "std::" in b or re.search(r"\b(cout|cin|endl|nullptr|template\s*<|vector<)\b", b):
        return "cpp"
    if re.search(r"\b(public\s+(class|static)|System\.out|void\s+main|import\s+java)\b", b):
        return "java"
    if re.search(r"\b(func\s+\w+|package\s+main|fmt\.\w+|:=)\b", b):
        return "go"
    if re.search(r"(\bconst\s+\w+\s*=|\blet\s+\w+\s*=|=>|console\.log|function\s+\w*\()", b):
        return "javascript"
    if re.search(r"(^#!.*\b(bash|sh)\b|\becho\s|\bapt-get\b|\bsudo\b|\$\(|\bgrep\b|\bcurl\b)", b, re.M):
        return "bash"
    if re.search(r"(?m)^\s*(def\s+\w+|class\s+\w+|import\s+\w+|from\s+\w+\s+import|"
                 r"print\(|if\s+__name__)", b) or "self." in b or "elif " in b:
        return "python"
    return "python"   # python-dominant corpus default

def _autolang(md: str) -> str:
    def repl(m):
        info, body = m.group(1), m.group(2)
        if info.strip():                       # already has a language tag
            return m.group(0)
        if any(ch in _DIAGRAM_CHARS for ch in body):   # ASCII diagram -> leave plain
            return m.group(0)
        if _CODE_HINT.search(body):            # looks like code -> guess + tag
            return "```" + _guess_lang(body) + "\n" + body + "```"
        return m.group(0)                      # prose / output -> leave plain
    return re.sub(r"```([^\n]*)\n(.*?)```", repl, md, flags=re.DOTALL)

# ---- markdown preprocessing: drop the hand-written "Table of Contents"
#      block (we generate our own), keep everything else intact ----
def preprocess(md: str) -> str:
    # remove a "## Table of Contents" section up to the next "---" or "## "
    md = re.sub(r"\n##+\s*Table of Contents.*?\n(?=\n(?:---|\#\# ))",
                "\n", md, flags=re.DOTALL | re.IGNORECASE)
    # drop standalone horizontal rules ("---"/"***") used as section dividers:
    # our section styling already separates topics, so these are visual clutter.
    md = re.sub(r"(?m)^[ \t]*(?:-{3,}|\*{3,}|_{3,})[ \t]*$", "", md)
    # tag untagged code fences so they get syntax-highlighted (before latexify)
    md = _autolang(md)
    # unicode symbols -> LaTeX math (outside code only)
    md = _code_aware(md)
    return md

def build_one(key, srcrel, title, kicker, num, acc, acc2, m, force=False):
    src = SRC / srcrel
    if not src.exists():
        print(f"  !! missing source: {src}"); return False
    texd, pdfd = texdir_for(key), pdfdir_for(key)
    tex = texd / (key + ".tex")
    pdf = pdfd / (key + ".pdf")
    cur = sha(src)
    rec = m["docs"].get(key, {})
    up_to_date = (not force and rec.get("src") == cur
                  and rec.get("style") == m["style"]
                  and pdf.exists() and rec.get("pdf_ok"))
    if up_to_date:
        print(f"  == {key:18s} up-to-date"); return True

    print(f"  ++ {key:18s} building…")
    # make the style package discoverable next to the .tex (in this subfolder)
    (texd / "interviewstyle.sty").write_bytes((ASSETS/"interviewstyle.sty").read_bytes())
    md = preprocess(src.read_text())
    md = place_figures(md, key)          # insert inline figure tokens at anchors
    tmp_md = texd / (key + ".pre.md")
    tmp_md.write_text(md)

    # 1) pandoc -> tex
    cmd = [PANDOC, str(tmp_md),
           "--from", "gfm+tex_math_dollars",
           "--to", "latex",
           "--template", str(TEMPLATE),
           "--lua-filter", str(ASSETS / "tablewidths.lua"),
           "--lua-filter", str(ASSETS / "codelang.lua"),
           "--highlight-style", "breezedark",
           "--shift-heading-level-by=-1",   # h1 title->meta; h2->section, h3->subsection
           "--columns", "78",
           "--wrap", "preserve",
           "-V", f"themename={title}",
           "-V", f"themekicker={kicker}",
           "-V", f"themenumber={num}",
           "-V", f"accent={acc}",
           "-V", f"accent2={acc2}",
           "-o", str(tex)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  !! pandoc failed for {key}:\n{r.stderr[:1200]}")
        rec.update(src=cur, style=m["style"], pdf_ok=False, error="pandoc:"+r.stderr[:300])
        m["docs"][key] = rec; return False

    postprocess_tex(tex, key)

    # 2) tectonic -> pdf  (delete any stale pdf first so "exists" == fresh)
    pdf.unlink(missing_ok=True)
    t0 = time.time()
    r = subprocess.run([TECTONIC, "-X", "compile", str(tex),
                        "--outdir", str(pdfd), "--keep-logs"],
                       capture_output=True, text=True)
    ok = (pdf.exists() and r.returncode == 0)
    dt = time.time() - t0
    if not ok:
        # tectonic sometimes returns nonzero on warnings; check pdf presence
        if pdf.exists():
            ok = True
        else:
            tail = (r.stderr or r.stdout)[-1500:]
            print(f"  !! tectonic failed for {key} ({dt:.1f}s):\n{tail}")
            rec.update(src=cur, style=m["style"], pdf_ok=False, error="tectonic")
            m["docs"][key] = rec; return False
    print(f"  ok {key:18s} -> {pdf.name}  ({dt:.1f}s, {pdf.stat().st_size//1024} KB)")
    rec.update(src=cur, style=m["style"], pdf_ok=True, error="", built=time.strftime("%Y-%m-%d %H:%M"))
    m["docs"][key] = rec
    tmp_md.unlink(missing_ok=True)
    return True

# ---- post-pandoc .tex fixups: table striping + clickable cross-refs ----
def _style_tables(s: str) -> str:
    out, in_lt, after_head, header_pending, row = [], False, False, False, 0
    for line in s.split("\n"):
        if "\\begin{longtable}" in line:
            in_lt, after_head, header_pending, row = True, False, True, 0
            out.append(line); continue
        if in_lt and "\\end{longtable}" in line:
            in_lt = False; out.append(line); continue
        if in_lt:
            if header_pending and "\\toprule" in line:
                out.append(line); out.append("\\rowcolor{acc!16}")
                header_pending = False; continue
            if "\\endhead" in line:
                after_head = True; out.append(line); continue
            if after_head and line.rstrip().endswith("\\\\"):
                row += 1
                if row % 2 == 0:
                    out.append("\\rowcolor{zebra}")
                out.append(line); continue
        out.append(line)
    return "\n".join(out)

def postprocess_tex(tex: Path, key: str = ""):
    s = tex.read_text()
    s = _style_tables(s)
    # inline figures: @@VFIGn@@ -> \visualfigure{path}{caption}
    figs = load_figures().get(key, [])
    def figrepl(m):
        i = int(m.group(1))
        if i < len(figs):
            fn, cap = figs[i][0], figs[i][1]
            return r"\visualfigure{../../figures/%s/%s}{%s}" % (key, fn, latexify(cap))
        return ""
    s = re.sub(r"@@VFIG(\d+)@@", figrepl, s)
    # clickable in-document section references: "§9" -> jump to section 9
    s = re.sub(r"§\s*(\d+)", r"\\hyperlink{section.\1}{\\textcolor{acc}{§\1}}", s)
    tex.write_text(s)

# ---- figures placed inline where each topic is discussed (see ANCHORS) ----
def load_figures():
    fj = FIGDIR / "figures.json"
    if fj.exists():
        try: return json.loads(fj.read_text())
        except Exception: return {}
    return {}

def _anchor_pat(anchor: str) -> str:
    # dash- and whitespace-flexible: "Bias-Variance" matches "Bias–Variance"
    toks = [re.escape(t).replace(r"\-", "[-‐-―]") for t in anchor.split()]
    return r"\s+".join(toks)

def place_figures(md: str, key: str) -> str:
    figs = load_figures().get(key)
    if not figs:
        return md
    for i, entry in enumerate(figs):
        anchor = entry[2] if len(entry) > 2 else ""
        mode = entry[3] if len(entry) > 3 else "after"
        token = f"\n\n@@VFIG{i}@@\n\n"
        placed = False
        if mode == "replace" and anchor:
            # swap the ASCII block that contains the signature for the figure
            for fm in re.finditer(r"```[^\n]*\n.*?```", md, flags=re.DOTALL):
                if anchor in fm.group(0):
                    md = md[:fm.start()] + token.strip() + md[fm.end():]
                    placed = True
                    break
        if not placed and anchor:
            p = _anchor_pat(anchor)
            # 1) right after a heading line that mentions the anchor
            mh = re.search(r"(?im)^#{2,4}[^\n]*" + p + r"[^\n]*$", md)
            if mh:
                md = md[:mh.end()] + token + md[mh.end():]; placed = True
            else:
                # 2) after the first line that mentions it (TOC already stripped)
                ml = re.search(r"(?im)^.*" + p + r".*\n", md)
                if ml:
                    md = md[:ml.end()] + token + md[ml.end():]; placed = True
        if not placed:
            md = md.rstrip() + token       # fallback: end of document
    return md

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only", default=None, help="substring filter on key")
    ap.add_argument("--status", action="store_true")
    args = ap.parse_args()

    m = load_manifest()
    cur_style = style_hash()
    if m.get("style") != cur_style:
        print(f"** style/template changed ({m.get('style')} -> {cur_style}); "
              f"affected docs will rebuild")
        m["style"] = cur_style

    if args.status:
        print(f"{'KEY':20s} {'PDF':5s} {'SRC':14s} BUILT")
        for key, *_ in REG:
            r = m["docs"].get(key, {})
            print(f"{key:20s} {'OK' if r.get('pdf_ok') else '--':5s} "
                  f"{r.get('src','-'):14s} {r.get('built','-')}")
        done = sum(1 for k,*_ in REG if m['docs'].get(k,{}).get('pdf_ok'))
        print(f"\n{done}/{len(REG)} PDFs built.")
        return

    todo = [row for row in REG if (args.only is None or args.only in row[0])]
    ok = fail = 0
    for (key, srcrel, title, kicker, num, acc, acc2) in todo:
        try:
            if build_one(key, srcrel, title, kicker, num, acc, acc2, m, force=args.force):
                ok += 1
            else:
                fail += 1
        except Exception as e:
            print(f"  !! exception for {key}: {e}"); fail += 1
        save_manifest(m)   # checkpoint after every doc (resumable)
    print(f"\nDONE: {ok} ok, {fail} failed, {len(todo)} attempted.")
    print(f"PDFs in {PDFDIR}")

if __name__ == "__main__":
    main()

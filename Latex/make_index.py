#!/usr/bin/env python3
"""
Build the collection front-matter:
  * pdf/00-Collection-Index.pdf  — a professional cover + catalog of all editions
  * pdf/Complete-Collection.pdf  — every edition merged into one book

Run after build.py has produced the per-topic PDFs.
"""
import subprocess, time
from pathlib import Path
import pypdfium2 as pdfium
from build import REG, ASSETS, TEXDIR, PDFDIR, TECTONIC

CATALOG_KEY = "00-Collection-Index"

def pagecount(p: Path) -> int:
    try:
        return len(pdfium.PdfDocument(str(p)))
    except Exception:
        return 0

def esc(s: str) -> str:
    # titles in REG already contain LaTeX-safe escaping (\&); pass through
    return s

def build_catalog():
    # group editions by track (kicker), preserving REG order
    groups, order = {}, []
    rows = []
    for key, srcrel, title, kicker, num, acc, acc2 in REG:
        if key == "00-index":
            continue  # the per-doc roadmap; catalog supersedes it on the cover
        pdf = PDFDIR / f"{key}.pdf"
        pc = pagecount(pdf) if pdf.exists() else 0
        if kicker not in groups:
            groups[kicker] = []; order.append(kicker)
        groups[kicker].append((num, title, pc, acc))
    total_pages = sum(pagecount(PDFDIR / f"{k}.pdf") for k, *_ in REG if (PDFDIR / f"{k}.pdf").exists())
    total_docs = sum(1 for k, *_ in REG if (PDFDIR / f"{k}.pdf").exists())

    body = []
    for kicker in order:
        body.append(r"\catalogsection{%s}" % kicker)
        body.append(r"\begin{catalogtbl}")
        for num, title, pc, acc in groups[kicker]:
            tag = num if num else "\\textbullet"
            body.append(r"\catalogrow{%s}{%s}{%d}" % (tag, title, pc))
        body.append(r"\end{catalogtbl}")
    body = "\n".join(body)

    tex = TEXDIR / f"{CATALOG_KEY}.tex"
    (TEXDIR / "interviewstyle.sty").write_bytes((ASSETS / "interviewstyle.sty").read_bytes())
    tex.write_text(TEMPLATE_TEX.replace("<<TOTALDOCS>>", str(total_docs))
                               .replace("<<TOTALPAGES>>", str(total_pages))
                               .replace("<<BODY>>", body)
                               .replace("<<DATE>>", time.strftime("%B %Y")))
    out = PDFDIR / f"{CATALOG_KEY}.pdf"
    out.unlink(missing_ok=True)
    r = subprocess.run([TECTONIC, "-X", "compile", str(tex), "--outdir", str(PDFDIR)],
                       capture_output=True, text=True)
    if out.exists():
        print(f"  ok  {CATALOG_KEY}.pdf  ({pagecount(out)} pp, {out.stat().st_size//1024} KB)")
        return out
    print("  !! catalog failed:\n", (r.stderr or r.stdout)[-1500:])
    return None

def _plain(title: str) -> str:
    return title.replace("\\&", "&").replace("\\", "").strip()

def merge_all(catalog: Path):
    # pypdf preserves each edition's internal section bookmarks and nests them
    # under a per-edition outline entry -> a fully navigable ~750-page book.
    from pypdf import PdfWriter
    w = PdfWriter()
    n_ed = 0
    if catalog and catalog.exists():
        w.append(str(catalog), outline_item="Cover & Catalogue")
    last_track = None
    for key, srcrel, title, kicker, num, acc, acc2 in REG:
        if key == "00-index":
            continue
        p = PDFDIR / f"{key}.pdf"
        if not p.exists():
            continue
        w.append(str(p), outline_item=_plain(title))
        n_ed += 1
    outp = PDFDIR / "Complete-Collection.pdf"
    with open(outp, "wb") as f:
        w.write(f)
    w.close()
    pages = pagecount(outp)
    print(f"  ok  Complete-Collection.pdf  ({pages} pp, {outp.stat().st_size//1024} KB, "
          f"{n_ed} editions, bookmarked)")

TEMPLATE_TEX = r"""\documentclass[11pt]{article}
\newcommand{\ThemeName}{The Complete Collection}
\newcommand{\ThemeKicker}{Interview Mastery Library}
\newcommand{\ThemeNumber}{}
\usepackage{interviewstyle}
\setthemecolor{6366f1}{8b5cf6}
\providecommand{\tightlist}{}

\newcommand{\catalogsection}[1]{%
  \par\addvspace{14pt}\needspace{6\baselineskip}%
  {\headingfont\large\bfseries\color{acc}#1}\par
  {\color{acc}\rule{\linewidth}{1.4pt}}\par\addvspace{4pt}}
\newenvironment{catalogtbl}{%
  \begin{list}{}{\setlength{\leftmargin}{0pt}\setlength{\itemsep}{2pt}}}{\end{list}}
\newcommand{\catalogrow}[3]{%
  \item[]\makebox[2.4em][l]{\headingfont\bfseries\color{acc2}#1}%
  {\headingfont\color{ink}#2}\hfill{\color{ink2}\small#3 pp}%
  \par\vspace{1pt}{\color{rule}\rule{\linewidth}{0.4pt}}}

\begin{document}
\makecoverpage

% ---- stats band on its own intro page ----
\thispagestyle{empty}
\vspace*{2.2cm}
\begin{center}
{\headingfont\Huge\bfseries\color{ink} Interview Mastery Library}\\[6pt]
{\headingfont\large\color{ink2} A professionally typeset, end-to-end preparation series}\\[26pt]
\begin{tcolorbox}[enhanced,width=0.82\linewidth,colback=acc!6,colframe=acc,
  boxrule=0pt,leftrule=4pt,arc=3pt,left=16pt,right=16pt,top=12pt,bottom=12pt]
{\headingfont\large\color{ink}\bfseries This edition contains}\\[8pt]
{\Large\color{acc}\bfseries <<TOTALDOCS>>}~{\color{ink2}professionally typeset editions}\\[4pt]
{\Large\color{acc}\bfseries <<TOTALPAGES>>}~{\color{ink2}pages of curated interview material}\\[4pt]
{\color{ink2} Systems \textbullet\ Design \textbullet\ Data \textbullet\ DSA \textbullet\ AI/ML \textbullet\ Behavioral}
\end{tcolorbox}
\end{center}
\vfill
\begin{center}{\color{ink2}\small Compiled <<DATE>> \quad\textbullet\quad Rendered with \LaTeX\ (XeTeX / Tectonic)}\end{center}
\clearpage

% ---- catalog ----
\vspace*{2pt}
{\headingfont\LARGE\bfseries\color{ink}Catalogue of Editions}\par\vspace{4pt}
{\color{acc}\rule{\linewidth}{2pt}}\par\vspace{12pt}
<<BODY>>

\end{document}
"""

if __name__ == "__main__":
    cat = build_catalog()
    merge_all(cat)

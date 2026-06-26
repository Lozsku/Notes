# Interview-Prep — LaTeX Edition

Professional, book-quality LaTeX typesetting of every note in `../Interview-Prep`,
with compiled PDFs. Each markdown topic becomes one styled `.tex` source and one PDF.

## What's here

```
Latex/
├── assets/
│   ├── interviewstyle.sty   # the shared professional style package (the "design")
│   ├── template.tex         # pandoc → LaTeX template (cover, TOC, body)
│   └── tablewidths.lua      # pandoc filter: proportional table column widths
├── build.py                 # resumable driver: markdown → .tex → PDF
├── make_index.py            # builds the collection index + merged "Complete-Collection.pdf"
├── manifest.json            # build state (content hashes) — enables resume
├── tex/<concept>/           # generated LaTeX sources, grouped by concept folder
├── pdf/<concept>/           # compiled PDFs, grouped by concept folder
├── make_anki.py             # flashcard decks (anki/*.tsv)
├── make_flashcards_ui.py    # flashcards.html study app
├── flashcards.html          # self-contained flashcard web app
└── figures/                 # generated diagrams (matplotlib/TikZ)
```

`tex/` and `pdf/` are organised into **concept folders** (the `FOLDER` map in `build.py`):
`foundations` (oop, design-patterns), `systems`, `infrastructure`, `system-design`, `data`,
`dev-practices`, `dsa`, `ai-ml`, `behavioral`, and `_collection` (index + merged book).

Key outputs in `pdf/`:
- One PDF per topic, e.g. `pdf/foundations/design-patterns.pdf`, `pdf/system-design/caching.pdf` — **38 editions**.
- `_collection/00-Collection-Index.pdf` — cover + catalogue of all editions.
- `_collection/Complete-Collection.pdf` — every edition merged into one ~880-page book, with a
  full **PDF bookmark tree** (per-edition entries + nested sections) for navigation.

And `anki/` holds **flashcards** auto-generated from the Q&A sections — `ALL-flashcards.tsv`
plus one `.tsv` per topic, importable straight into Anki (see `anki/README.md`).

## Toolchain (no root / no system install required)

- **pandoc** (`~/.local/bin/pandoc`) — markdown → LaTeX.
- **Tectonic** (`~/.local/bin/tectonic`) — self-contained XeTeX engine; fetches and
  caches only the LaTeX packages it needs (no multi-GB TeX Live install).
- **matplotlib / pypdfium2** (already in the user's Python) — diagrams & PDF merge.
- Fonts: premium set installed to `~/.fonts` — body **IBM Plex Serif**, headings **Inter**,
  code **JetBrains Mono** (covers box-drawing glyphs for ASCII diagrams). Falls back to
  Liberation/Ubuntu/DejaVu if those aren't present.
- **pypdf** (merged-book bookmarks) — `pip install pypdf` if missing.

## Adding a new edition (step by step)

> **You never hand-write `.tex` or PDF.** You write **one Markdown file**, register it in
> two small places, and the scripts generate the styled `.tex`, the PDF, the merged book,
> the flashcards, and the index links for you.

This walkthrough adds a fictional edition called **GraphQL** end-to-end. Substitute your own
topic. Everything runs from the `Latex/` directory:

```bash
export PATH="$HOME/.local/bin:$PATH"   # so pandoc + tectonic are on PATH
cd /home/harsha/kite_algo_trader/Notes/Latex
```

### Step 1 — Write the Markdown note

Create the source file under `../Interview-Prep/` (the `Interview-Prep/` folder is the build's
source root, called `SRC`). Any sub-folder is fine. **Easiest start: copy an existing note and
edit it** so you inherit the exact section structure:

```bash
cp ../Interview-Prep/15-caching.md ../Interview-Prep/22-graphql.md
# now edit 22-graphql.md — change the title and content
```

The build expects this shape (it's what every edition uses; `(BT)` below means a literal
triple-backtick ` ``` ` — shown this way so the example itself doesn't break):

````text
# GraphQL                          ← H1 = the cover title (exactly ONE, at the very top)

> **How to use this file:** …      ← short intro blockquote (optional)

## Table of Contents               ← optional; the PDF builds its own clickable TOC
- …

## Overview — What It Is           ## headings -> numbered sections in the PDF
…
### A sub-topic                    ### headings -> numbered sub-sections (1.1, 1.2 …)

(BT)java                           code fences: TAG with a language (java/python/sql/
   …  your code …                  bash/json/…) to get IDE-style syntax highlighting
(BT)

(BT)                               an UNTAGGED fence = rendered as an ASCII-diagram card
   ┌────┐   ───►  ┌────┐
(BT)

## Common Interview Questions
### Q1: <the question>             ← `### Qn:` blocks are auto-extracted into FLASHCARDS
**Model answer:** …
**Follow-ups:**
- …

## Revision Cheat Sheet
…
````

Rules that matter: exactly **one `# H1`** (the cover title), use `##`/`###` for everything
else, language-tag code fences you want highlighted, and write questions as `### Qn:` +
`**Model answer:**` if you want flashcards from them.

### Step 2 — Register it in `build.py` (`REG`)

Open `build.py`, find the `REG = [ … ]` list near the top, and add **one row**. Columns are:
`key`, `source path (relative to Interview-Prep/)`, `title`, `track`, `number`, `accent`, `accent2`.

```python
REG = [
  …
  ("caching",  "15-caching.md", "Caching", "Design Track", "", "c2410c","fb923c"),
  ("graphql",  "22-graphql.md", "GraphQL", "Design Track", "", "e535ab","f0a6d6"),   # ← ADD THIS
  …
]
```

- **`key`** (`"graphql"`) = the output filename → `graphql.tex` / `graphql.pdf`. Keep it
  unique, lowercase, no spaces.
- **`title`** = what prints big on the cover. Escape `&` as `\\&` (e.g. `"Testing \\& Code Quality"`).
- **`track`** = the group it's filed under in the catalogue (e.g. `"Design Track"`, or a new one).
- **`number`** = the big faded number on the cover (use `""` for none).
- **`accent`/`accent2`** = two hex colours **without `#`** for the theme (cover, headings, code bar).

### Step 3 — Put it in a folder (`FOLDER`)

Still in `build.py`, find the `FOLDER = { … }` map and add the key → which concept sub-folder
its `.tex`/`.pdf` go into:

```python
FOLDER = {
  …
  "caching": "system-design",
  "graphql": "system-design",      # ← ADD THIS  → tex/system-design/ + pdf/system-design/
  …
}
```

Reuse an existing folder (`foundations`, `systems`, `infrastructure`, `system-design`, `data`,
`dev-practices`, `dsa`, `ai-ml`, `behavioral`). **Only if you invent a NEW folder**, also add it
to `FOLDER_META` in `make_readmes.py` (with a display label) so it appears in the index READMEs:

```python
FOLDER_META = [
  …
  ("system-design", "🏗️ System Design"),
  ("my-new-folder", "🆕 My New Folder"),   # ← only when adding a brand-new folder
]
```

### Step 4 — Build it → generates the `.tex` and PDF

```bash
python3 build.py --only graphql
```

**Expected output:**

```
  ++ graphql            building…
  ok graphql            -> graphql.pdf  (7.4s, 210 KB)

DONE: 1 ok, 0 failed, 1 attempted.
```

> `--only graphql` builds just this one (matches any key containing the text). Run
> `python3 build.py` alone to build everything that changed; add `--force` to rebuild ignoring
> the cache. If you only edited the `.md`, plain `build.py` rebuilds just that doc.

**Verify the files were generated:**

```bash
ls pdf/system-design/graphql.pdf tex/system-design/graphql.tex
# → pdf/system-design/graphql.pdf   tex/system-design/graphql.tex
```

Open `pdf/system-design/graphql.pdf` to eyeball it.

### Step 5 — Refresh the aggregate outputs

These pull your new edition into the merged book, flashcards, and index pages:

```bash
python3 make_index.py          # merged bookmarked collection + catalogue
python3 make_anki.py           # Anki decks from ### Qn: blocks
python3 make_flashcards_ui.py  # flashcards.html study app
python3 make_readmes.py        # pdf/README.md + tex/README.md index links
```

**Expected output (counts grow by your edition):**

```
# make_index.py
  ok  00-Collection-Index.pdf  (5 pp, 46 KB)
  ok  Complete-Collection.pdf  (1255 pp, 12104 KB, 40 editions, bookmarked)
# make_anki.py
  ok  254 flashcards across 31 topics -> …/Latex/anki
# make_flashcards_ui.py
  ok  254 cards across 31 decks -> …/Latex/flashcards.html
# make_readmes.py
  ok  pdf/README.md  (41 editions linked)
  ok  tex/README.md  (41 editions linked)
```

Done — your topic is now a styled PDF, in the merged book, in the flashcards, and linked from
`pdf/README.md`. **No LaTeX written by hand.**

### Editing an existing edition

Just edit its `.md` and re-run the build (it rebuilds only what changed) + the refreshers:

```bash
python3 build.py                # detects the changed source via manifest.json, rebuilds it
python3 make_index.py && python3 make_anki.py && python3 make_flashcards_ui.py && python3 make_readmes.py
```

### Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| `!! missing source: …` | the `source` path in `REG` is wrong (it's relative to `Interview-Prep/`). |
| Doc lands in a `misc/` folder | you added the `REG` row but forgot the `FOLDER` entry for that key. |
| New folder's PDFs aren't in `pdf/README.md` | add the folder to `FOLDER_META` in `make_readmes.py`. |
| `pandoc: command not found` | run `export PATH="$HOME/.local/bin:$PATH"` first. |
| `!! pandoc failed …` | a Markdown issue — usually a malformed table or an unclosed ``` code fence. |
| PDF built but a figure/section looks off | check for one stray `#` H1 in the body (only the first line should be H1). |
| Cover title shows a literal `\&` | in the `REG` title use `\\&` for an ampersand. |

## Rebuild / resume

```bash
export PATH="$HOME/.local/bin:$PATH"
cd Latex
python3 build.py            # build everything stale (skips up-to-date docs)
python3 build.py --force    # rebuild all
python3 build.py --only 04  # only docs whose key contains "04"
python3 build.py --status   # progress table
python3 make_index.py       # rebuild the index + bookmarked merged collection
python3 make_anki.py        # regenerate the Anki flashcard decks
python3 make_flashcards_ui.py   # regenerate flashcards.html (browser study app)
python3 make_readmes.py     # refresh the pdf/ + tex/ index READMEs (links to every edition)
```

**Flashcards UI:** `flashcards.html` is a self-contained study app (open in any browser, no
server) — deck picker, click/Space to reveal, ←/→ to navigate, shuffle, and "mastered"
progress saved in the browser. Built from the same Q&A as the Anki decks.

The build is **resumable**: `manifest.json` records each source's content hash and
whether its PDF compiled. Re-running rebuilds only what changed (source edits, or any
change to the style/template/filter). It checkpoints after every document, so an
interrupted run continues from where it stopped.

## Design notes

- The look is defined entirely in `assets/interviewstyle.sty`: per-topic accent color,
  colored section bars, **macOS-terminal-style code cards** (dark window with red/yellow/
  green traffic-light dots, syntax highlighting, and the **language shown top-right** via
  `assets/codelang.lua`), callout boxes for blockquotes, proportional booktabs tables, a
  TikZ cover page, and running headers.
- Headings are shifted up one level (`--shift-heading-level-by=-1`): the H1 doc title
  (already on the cover) is dropped, H2→numbered section, H3→subsection, so the TOC
  (`tocdepth=2`) shows full `1.1 / 1.2` detail.
- Untagged ` ``` ` code fences that are clearly code (not ASCII diagrams) are auto-tagged
  with a **guessed language** (`_guess_lang`/`_autolang` in `build.py`) so they get
  IDE-style highlighting instead of plain verbatim; box-drawing diagrams stay in the light
  card. Long code lines **wrap** (via `fvextra`) and carry a faint **line-number gutter**.
- Tables get a **tinted header row** + **zebra striping** (`_style_tables` in `build.py`),
  and inline `§N` references become **clickable** links to that section.
- The merged `Complete-Collection.pdf` is assembled with **pypdf** (`make_index.py`), which
  preserves each edition's internal bookmarks and nests them under a per-edition entry.
- **57 hand-crafted diagrams** (`diagrams.py` → vector PDFs in `figures/`), each placed
  **inline in the section that discusses it** (not in a bottom gallery). Two placement modes
  in `build.py` (`place_figures`): `ANCHORS` (insert after a matching heading) and `REPLACE`
  (swap a specific ASCII block for the bespoke figure in place). Architecture/box diagrams,
  sequence diagrams (TLS/TCP/DNS), class diagrams, state machines, heatmaps, neural-net &
  CNN schematics, flame graph, consistent-hashing ring, decision trees, plots, … — each
  themed to its edition's accent.
- To add a figure: write a function in `diagrams.py`, `_save(...)` it, and add either an
  `ANCHORS` entry (heading substring → placed after it) or a `REPLACE` entry (a signature
  inside an ASCII block → that block is replaced by the figure).
- Unicode in prose (arrows, Greek, math operators, ✓/✗) is converted to real LaTeX math
  during preprocessing (see `SYM` in `build.py`), because the body serif has no glyphs
  for them and XeTeX does no automatic font fallback. Inside code/diagram blocks the
  original characters are kept (DejaVu Mono renders them).
- ASCII diagrams render inside a light monospace "diagram card". Topics where a real
  plot is clearer can get matplotlib/TikZ figures under `figures/` (see `diagrams.py`).

## Per-topic accent / theme

Themes (title, track, number, colors) are defined in the `REG` table at the top of
`build.py`. Edit there to change a topic's title, ordering, or color.

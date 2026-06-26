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

**You never hand-write `.tex` or PDF — they are generated from Markdown.** To add a new note:

1. **Write the note in Markdown** under `Interview-Prep/` (any sub-folder is fine), following
   the same section format as the others (`# Title`, then `## Overview — What It Is`, … ,
   `## Common Interview Questions` with `### Qn:` blocks, … , `## Revision Cheat Sheet`).
   *Tip: copy an existing file as a skeleton.*

2. **Register it** — add one row to the `REG` list near the top of `build.py`:
   ```python
   # key,        source (rel. to Interview-Prep/),  title,                 track,           num, accent,  accent2
   ("caching",   "15-caching.md",                   "Caching",             "Design Track",  "",  "c2410c","fb923c"),
   ```
   `key` is the output filename; `accent`/`accent2` are hex colours (no `#`) for the theme.

3. **Put it in a folder** — add the `key` to the `FOLDER` map in `build.py` (which concept
   sub-folder its `.tex`/`.pdf` land in). Use an existing folder or a new one:
   ```python
   "caching": "system-design",      # → tex/system-design/ and pdf/system-design/
   ```
   (If you add a brand-new folder, also add it to `FOLDER_META` in `make_readmes.py` so it
   shows up in the index READMEs.)

4. **Build it:**
   ```bash
   python3 build.py --only caching      # builds just this one (or run build.py for all)
   ```
   This auto-generates `tex/<folder>/caching.tex` and `pdf/<folder>/caching.pdf`.

5. **Refresh the aggregate outputs:**
   ```bash
   python3 make_index.py          # adds it to the merged bookmarked collection + catalogue
   python3 make_anki.py           # flashcards from its ### Qn: blocks
   python3 make_flashcards_ui.py  # updates flashcards.html
   python3 make_readmes.py        # adds it to pdf/README.md + tex/README.md
   ```

That's it — no LaTeX by hand. Editing an existing note? Just edit its `.md` and re-run
`python3 build.py` (it rebuilds only what changed) plus the refresh scripts above.

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

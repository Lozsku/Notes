# 📖 Magazine Studio — live preview & editing

A small local tool to edit the magazines and see changes instantly, then export PDFs.

## Start it
```bash
cd Interview-Prep/.magazine
python3 serve.py          # then open http://localhost:8000
```
(Use a different port with `PORT=9000 python3 serve.py`.)

## Workflow
1. Open **http://localhost:8000** → click any edition to open its **live preview**.
2. Edit a source file in your editor and **save**.
3. The preview tab **auto-refreshes** with the new render (it polls every second).
4. Happy? Click **⬇ Export PDF** in the top bar to write the final PDF.

## What to edit for small changes
| Want to change… | Edit this |
|---|---|
| A **diagram** | `diagrams/dNN.py` — HTML/SVG keyed by the ASCII block's hash. Run `python3 extract.py N` to list a topic's diagrams + their keys + original ASCII. See `TOOLKIT.md` for the component classes (`.fig`, `.seq`, `.stack`, `.tiers`, `.gantt`, `.matrix`, `.node`, inline `<svg>` …). |
| **Colors / fonts / layout / callouts / tables** | the CSS string `SHARED_CSS` (and per-topic accent in `CONFIGS`) inside `mag.py`. The flagship Concurrency edition is styled in `build.py`. |
| **Wording / content / sections** | the topic's markdown in the parent folder, e.g. `../04-cloud-infrastructure.md`. |
| **Cover title / subtitle / tags** | the topic's entry in `CONFIGS` inside `mag.py`. |
| **Cheat sheet** | `cheat.py` (+ `../CHEATSHEET.md`). |

## Notes
- The on-screen preview stacks content into **A4-width pages**; exact page breaks and margins are finalized in the **exported PDF** (use Export PDF to verify pagination).
- Diagram overrides are matched by a content hash, so they survive edits to *other* parts of the notes. If you change the ASCII of a block that has an override, re-run `extract.py N` to get its new hash.
- Build everything from the CLI too: `python3 mag.py` (all topics) · `python3 mag.py 4` (one) · `python3 cheat.py` · `python3 build.py && <chrome render>` (flagship).

## Files
- `serve.py` — the preview server
- `mag.py` — generic builder (topics 2–11) + `CONFIGS` + `SHARED_CSS` + diagram toolkit
- `build.py` — flagship Concurrency edition
- `cheat.py` — cheat sheet
- `diagrams/dNN.py` — hand-built diagram figures per topic
- `extract.py` — list a topic's ASCII diagrams + hash keys
- `TOOLKIT.md` — diagram component reference
- `fonts_embedded.css` — base64 fonts (self-contained PDFs)

# Diagram Toolkit Reference (for building real HTML figures)

You are replacing ASCII-art diagrams in the magazine PDFs with real, good-looking HTML figures.
Use ONLY the CSS classes below (they auto-theme to each topic's accent via CSS variables — **never hardcode colors**;
if you need the theme color in inline SVG use `var(--acc)`, `var(--acc2)`, `var(--acc-bg)`, `var(--acc-bd)`, `var(--acc-d)`, `var(--acc-tx)`).

Every figure is wrapped:
```html
<div class="fig">
  <div class="figcap">SHORT TITLE</div>
  ...figure body...
  <div class="fignote">one-line caption / takeaway (optional)</div>
</div>
```

## Building blocks

**Nodes & flow**
- `<div class="node"><div class="nt">Title</div><div class="ns">subtitle</div></div>` — a box. Variants: `node acc` (filled gradient), `node soft` (tinted).
- `<div class="frow">…</div>` horizontal centered row; add `sb` for space-between; add inline `style="flex-wrap:nowrap"` to force one line.
- `<div class="fcol">…</div>` vertical stack.
- `<span class="ar">→</span>` accent arrow; `<div class="ar-d">↓ label ↓</div>` down arrow.
- `<span class="chip">label</span>` small pill (mono).

**Sequence / handshake** (exactly TWO actors)
```html
<div class="seq">
  <div class="seqhead"><span>Client</span><span>Server</span></div>
  <div class="seqmsg r"><span class="t">message left→right</span></div>
  <div class="seqmsg l"><span class="t">message right→left</span></div>
  <div class="seqmsg l dash"><span class="t">dashed = encrypted/optional</span></div>
</div>
```
Put summary chips AFTER the seq: `<div class="frow"><span class="chip">✓ established</span></div>`.

**Layered stack** (OSI, memory layout, network stack, protocol layers)
```html
<div class="stack">
  <div class="stk hl"><span class="si">7</span><span class="sn">Name</span><span class="sd">detail</span></div>
  <div class="stk"><span class="si">6</span><span class="sn">Name</span><span class="sd">detail</span></div>
</div>
```
`si` (index badge) is optional; `hl` highlights a row.

**Tiers / architecture columns** (client→LB→app→db, control plane, pipelines)
```html
<div class="tiers">
  <div class="tier"><div class="th">EDGE</div><div class="fcol"><div class="node">…</div></div></div>
  <div class="tier"><div class="th">APP</div><div class="fcol">…</div></div>
</div>
```

**Timeline / Gantt / proportional bars** (scheduling, latency budgets, percentages)
```html
<div class="gantt">
  <div class="gr"><span class="gl">CPU</span>
    <div class="track"><div class="gseg a" style="width:30%">P1</div><div class="gseg b" style="width:50%">P2</div></div></div>
</div>
```
Segment classes: `a` (accent), `b` (accent2), `m` (muted).

**Matrix / grid** (isolation levels, comparison cells, truth tables)
```html
<div class="matrix" style="grid-template-columns:repeat(4,1fr)">
  <div class="cell hd">Header</div> <div class="cell on">✓</div> <div class="cell">✗</div> …
</div>
```
`hd` = header cell, `on` = filled/accent cell.

**Comparison split** — just use two `node`/`fcol` side by side in a `frow sb`, or a 2-col `tiers`.

**Trees, rings, graphs** (B-trees, consistent-hashing rings, DAGs): use **inline `<svg>`**.
- Center with the `.fig svg` rule (automatic). Use `stroke="var(--acc)"`, `fill="var(--acc-bg)"`, text `fill="var(--acc-tx)"`, font-family `'JetBrains Mono'` or `'Space Grotesk'`, small font-size (8–10).
- Keep viewBox width ~ 520, height to fit; the svg scales to column width.

**Callouts** (if a "diagram" is really a note): `<div class="callout c-key"><div class="ch">◆ Title</div><p>…</p></div>`
(types: `c-key` accent, `c-take` gold, `c-ana` teal, `c-warn` coral, `c-model` violet).

## Rules
- Keep each figure compact enough to fit comfortably on a page (avoid very tall figures; split if needed).
- Match the *content* of the original ASCII faithfully (same labels/values), just rendered beautifully.
- Use `&amp;` `&lt;` `&gt;` for literal & < > inside text.
- Output Python file `diagrams/dNN.py` with: `D = { "<hash>": r'''<figure html>''', ... }`
- A complete reference example is **`diagrams/d03.py`** (computer networks) — read it first.

#!/usr/bin/env python3
"""
Generate Anki-importable flashcards from the Q&A sections of the notes.

Produces, under Latex/anki/ :
  <topic>.tsv          one deck per edition  (Front <TAB> Back <TAB> Tags)
  ALL-flashcards.tsv   every card, combined
  README.md            import instructions

The notes use a consistent  '### Qn: <question>'  +  '**Model answer:** ...'
layout; behavioral uses  '**Q: "<question>"**'.  Both are parsed.

Run:  python3 make_anki.py
"""
import re, html
from pathlib import Path
from build import REG, SRC, ROOT

ANKI = ROOT / "anki"

# ---- markdown -> light HTML suitable for an Anki card back ----
def md_to_html(text: str) -> str:
    text = text.strip()
    # fenced code -> <pre>
    def code_repl(m):
        body = html.escape(m.group(2))
        return f"<pre style='background:#0f1426;color:#e7ecf6;padding:8px;" \
               f"border-radius:6px;overflow:auto'>{body}</pre>"
    text = re.sub(r"```([^\n]*)\n(.*?)```", code_repl, text, flags=re.DOTALL)
    out_lines = []
    for ln in text.split("\n"):
        if re.match(r"^\s*-\s+", ln):
            ln = "• " + re.sub(r"^\s*-\s+", "", ln)
        out_lines.append(ln)
    text = "\n".join(out_lines)
    text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"^\s*#{1,6}\s*", "", text, flags=re.MULTILINE)
    text = text.replace("\n\n", "<br><br>").replace("\n", "<br>")
    # TSV-safe: no raw tabs/newlines
    return text.replace("\t", "    ").replace("\r", "").strip()

def clean_q(q: str) -> str:
    q = q.strip().strip('"').strip()
    q = re.sub(r"\*\*", "", q)
    return q.replace("\t", " ").strip()

def parse_cards(md: str):
    cards = []
    # split into blocks on headings/dividers, keep the heading
    # 1) "### Qn: question"  blocks
    pattern = re.compile(r"(?m)^###\s*Q\d*\s*[:.]?\s*(.+?)\s*$")
    matches = list(pattern.finditer(md))
    for i, m in enumerate(matches):
        q = clean_q(m.group(1))
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(md)
        block = md[start:end]
        # stop the answer at the next ## (section) or horizontal rule run
        block = re.split(r"(?m)^##\s", block)[0]
        block = re.sub(r"(?m)^---\s*$", "", block).strip()
        if q and block:
            cards.append((q, md_to_html(block)))
    # 2) behavioral-style  **Q: "..."**  with following paragraph(s)
    for m in re.finditer(r'(?m)^\*\*Q:\s*"?(.+?)"?\*\*\s*$', md):
        q = clean_q(m.group(1))
        start = m.end()
        nxt = re.search(r'(?m)^(\*\*Q:|##\s|###\s)', md[start:])
        block = md[start:start + (nxt.start() if nxt else 400)]
        block = re.sub(r"(?m)^---\s*$", "", block).strip()
        if q and block:
            cards.append((q, md_to_html(block)))
    return cards

def main():
    ANKI.mkdir(exist_ok=True)
    combined, per_topic_counts = [], []
    for key, srcrel, title, kicker, num, acc, acc2 in REG:
        src = SRC / srcrel
        if not src.exists():
            continue
        cards = parse_cards(src.read_text())
        if not cards:
            continue
        tag = "InterviewPrep::" + re.sub(r"[^A-Za-z0-9]+", "_", title.replace("\\&", "and")).strip("_")
        lines = [f"{q}\t{a}\t{tag}" for q, a in cards]
        (ANKI / f"{key}.tsv").write_text("\n".join(lines) + "\n")
        combined += lines
        per_topic_counts.append((title.replace("\\&", "&"), len(cards)))
    (ANKI / "ALL-flashcards.tsv").write_text("\n".join(combined) + "\n")

    readme = ["# Anki flashcards\n",
              f"Auto-generated from the Q&A sections of the notes — **{len(combined)} cards**.\n",
              "## Import into Anki",
              "1. Anki → File → Import → choose `ALL-flashcards.tsv` (or a single topic's `.tsv`).",
              "2. Type: **Basic**. Field separator: **Tab**.",
              "3. Map: Field 1 → Front, Field 2 → Back, Field 3 → Tags.",
              "4. Tick *Allow HTML in fields* so formatting/code renders.\n",
              "## Decks (cards each)\n"]
    for t, n in per_topic_counts:
        readme.append(f"- {t}: {n}")
    (ANKI / "README.md").write_text("\n".join(readme) + "\n")
    print(f"  ok  {len(combined)} flashcards across {len(per_topic_counts)} topics -> {ANKI}")

if __name__ == "__main__":
    main()

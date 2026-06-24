# 🎯 FAANG Interview Prep — Master Notes

A comprehensive, first-principles, interview-focused knowledge base for SDE / Senior-SDE
and AI/ML interviews — written as deep, scenario-driven notes and typeset into a
professional, book-quality PDF library with auto-generated flashcards.

> **38 editions · 1,200+ pages · 240+ flashcards** — every topic follows the same structure:
> *Overview → Why it exists → Why FAANG cares → Core concepts → deep topic sections →
> Architecture/diagrams → Real-world examples → Analogies → Interview Q&A → Senior
> discussion → Common mistakes → Cheat sheet.*

---

## 🚀 Start here

| I want to… | Go to |
|------------|-------|
| **Read everything as one book** | [`Complete-Collection.pdf`](Latex/pdf/_collection/Complete-Collection.pdf) — 1,207 pages, fully bookmarked |
| **Browse individual PDFs** | [`Latex/pdf/README.md`](Latex/pdf/README.md) — direct links to every edition |
| **Study with flashcards** | open [`Latex/flashcards.html`](Latex/flashcards.html) in any browser (240+ cards) |
| **Cram the night before** | [`CHEATSHEET.md`](Interview-Prep/CHEATSHEET.md) — all topics condensed |
| **See the topic roadmap** | [`Interview-Prep/00-INDEX.md`](Interview-Prep/00-INDEX.md) |
| **Read the source notes** | the `.md` files in [`Interview-Prep/`](Interview-Prep/) |

---

## 📚 What's inside

**Core systems & design**
- Concurrency & Multithreading · Operating Systems · Computer Networks · Distributed Systems
- System Design · Low-Level Design · **Object-Oriented Programming** · **Design Patterns**
- **API Design** · **Caching** · **Message Queues & Streaming** · Databases
- Performance Engineering · **Observability**

**Platform, practices & tooling**
- Cloud & Infrastructure · Security Fundamentals · **Linux & the Command Line**
- **Testing & Code Quality** · **Git & Dev Workflow**

**DSA** — Patterns & Templates · Data Structures · Algorithms & Complexity

**AI / ML** — ML Fundamentals · Classic ML · Deep Learning · Transformers & LLMs · LLM
Applications & GenAI · MLOps & ML System Design · **AI Agents & Tool Use** ·
**Vector Databases & Embeddings**

**Applied practice packs** — System Design Problems (I & II) · LLD machine-coding solutions

Each edition is a deep, standalone note (many are **30–50 pages**) with mechanism-level
explanations, code, diagrams, worked examples, trade-offs, and 10–12 interview Q&As.

---

## 📦 Repository structure

```
Notes/
├── Interview-Prep/             # the source notes (Markdown)
│   ├── 00-INDEX.md             # topic roadmap
│   ├── 01..21-*.md             # core topics
│   ├── CHEATSHEET.md
│   ├── DSA/                    # DSA pack
│   ├── AI-ML/                  # AI/ML series (+ its own 00-INDEX)
│   ├── System-Design-Problems/ # applied SD problems
│   └── LLD-Problems/           # machine-coding solutions
│
└── Latex/                      # the PDF + flashcard build pipeline
    ├── pdf/<concept>/          # compiled PDFs, grouped by concept  → see pdf/README.md
    ├── tex/<concept>/          # generated LaTeX sources            → see tex/README.md
    ├── figures/                # hand-crafted vector diagrams
    ├── anki/                   # flashcard decks (.tsv) for Anki
    ├── flashcards.html         # self-contained flashcard study app
    ├── build.py                # markdown → styled .tex → PDF (resumable)
    ├── make_index.py           # builds the merged, bookmarked collection
    ├── make_anki.py            # generates flashcard decks
    ├── make_flashcards_ui.py   # builds flashcards.html
    ├── make_readmes.py         # regenerates pdf/ + tex/ index READMEs
    └── README.md               # full pipeline docs
```

---

## 🛠️ The build pipeline (short version)

Notes are authored in Markdown and rendered to professional PDFs via
**pandoc → Tectonic (XeLaTeX)** — no system LaTeX install needed. Highlights:

- Per-topic accent themes, macOS-style code cards with syntax highlighting + line numbers,
  proportional tables with tinted headers, a multi-level clickable TOC.
- **Hand-crafted vector diagrams** placed inline where each topic is discussed.
- A single **bookmarked** `Complete-Collection.pdf` plus per-topic PDFs.
- **Flashcards** auto-extracted from each note's interview Q&A → Anki decks + a browser app.

Full details and commands: [`Latex/README.md`](Latex/README.md).

```bash
cd Latex
python3 build.py                # build/refresh all PDFs (resumable)
python3 make_index.py           # merged collection + catalogue
python3 make_anki.py            # flashcard decks
python3 make_flashcards_ui.py   # flashcards.html
python3 make_readmes.py         # refresh the pdf/ + tex/ index READMEs
```

---

*Authored for interview preparation. Browse the PDFs via
[`Latex/pdf/README.md`](Latex/pdf/README.md), or read the source in
[`Interview-Prep/`](Interview-Prep/).*

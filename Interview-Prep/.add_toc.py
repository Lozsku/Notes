#!/usr/bin/env python3
"""Insert a GitHub-compatible Table of Contents into each content markdown file.
Idempotent (skips files that already have one). Ignores headings inside code fences."""
import re, glob, os

BASE = os.path.dirname(os.path.abspath(__file__))
# Skip pure navigation indexes (they ARE tables of contents already)
SKIP = {"00-INDEX.md"}

def gh_slug(text, seen):
    s = text.strip().lower()
    s = re.sub(r'[`*_]+', '', s)            # strip markdown emphasis markers
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)  # md links -> text
    s = re.sub(r'[^\w\s-]', '', s)          # drop emoji & punctuation (keep word chars/space/hyphen)
    # NOTE: do NOT strip here — GitHub keeps the leading hyphen left by a removed leading emoji
    s = re.sub(r'\s', '-', s)               # spaces -> hyphens (no collapse: matches GitHub)
    base = s
    n = seen.get(base, 0)
    seen[base] = n + 1
    return base if n == 0 else f"{base}-{n}"

def process(path):
    rel = os.path.relpath(path, BASE)
    lines = open(path, encoding="utf-8").read().split("\n")
    if any(l.strip().lower() == "## table of contents" for l in lines):
        return rel, "already has TOC — skipped"

    in_fence = False
    headings = []          # (level, text, lineidx)
    first_h2_idx = None
    for i, l in enumerate(lines):
        if re.match(r'^\s*```', l):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = re.match(r'^(##)\s+(.*\S)\s*$', l)   # H2 only (## , not ### because \s+ after exactly ##)
        if m and not l.startswith('###'):
            if first_h2_idx is None:
                first_h2_idx = i
            headings.append(m.group(2))

    if first_h2_idx is None or len(headings) < 2:
        return rel, f"only {len(headings)} H2 — skipped"

    seen = {}
    toc = ["## Table of Contents", ""]
    for h in headings:
        anchor = gh_slug(h, seen)
        label = re.sub(r'[`*]+', '', h).strip()
        toc.append(f"- [{label}](#{anchor})")
    toc += ["", "---", ""]

    new_lines = lines[:first_h2_idx] + toc + lines[first_h2_idx:]
    open(path, "w", encoding="utf-8").write("\n".join(new_lines))
    return rel, f"added TOC ({len(headings)} entries)"

files = sorted(glob.glob(os.path.join(BASE, "**", "*.md"), recursive=True))
for f in files:
    if os.path.basename(f) in SKIP:
        print(f"{os.path.relpath(f, BASE):55} skip (index)")
        continue
    rel, msg = process(f)
    print(f"{rel:55} {msg}")

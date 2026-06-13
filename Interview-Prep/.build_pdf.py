#!/usr/bin/env python3
import markdown, sys, pathlib

src = pathlib.Path("CHEATSHEET.md").read_text(encoding="utf-8")
body = markdown.markdown(
    src,
    extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"],
)

css = """
@page { size: A4; margin: 1.2cm; }
* { box-sizing: border-box; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 8.4px;
       line-height: 1.35; color: #1a1a1a; max-width: 100%; }
h1 { font-size: 17px; border-bottom: 2px solid #333; padding-bottom: 3px;
     margin: 6px 0 8px; }
h2 { font-size: 12px; background: #2d3748; color: #fff; padding: 3px 6px;
     margin: 10px 0 5px; border-radius: 3px; }
h3 { font-size: 9.5px; margin: 6px 0 3px; color: #2b6cb0; }
p { margin: 3px 0; }
ul, ol { margin: 3px 0 3px 16px; padding: 0; }
li { margin: 1.5px 0; }
strong { color: #1a202c; }
code { font-family: 'DejaVu Sans Mono', monospace; font-size: 7.6px;
       background: #f0f0f0; padding: 0 2px; border-radius: 2px; }
pre { background: #f6f8fa; border: 1px solid #ddd; border-radius: 3px;
      padding: 5px; overflow-x: auto; font-size: 7.4px; }
pre code { background: none; }
table { border-collapse: collapse; width: 100%; margin: 5px 0; font-size: 7.8px; }
th, td { border: 1px solid #bbb; padding: 2.5px 5px; text-align: left; vertical-align: top; }
th { background: #e2e8f0; font-weight: bold; }
tr:nth-child(even) td { background: #f7fafc; }
blockquote { border-left: 3px solid #4299e1; margin: 5px 0; padding: 2px 8px;
             background: #ebf8ff; color: #2c5282; }
hr { border: none; border-top: 1px solid #ccc; margin: 8px 0; }
"""

html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<style>{css}</style></head><body>{body}</body></html>"""

pathlib.Path("CHEATSHEET.html").write_text(html, encoding="utf-8")
print("HTML written:", len(html), "bytes")

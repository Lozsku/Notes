#!/usr/bin/env python3
"""
Build a self-contained flashcard web app (Latex/flashcards.html) from the Q&A
sections of the notes. No server needed — just open the file in a browser.

Reuses the same parser/formatter as make_anki.py so the cards match the decks.

Run:  python3 make_flashcards_ui.py   ->  open Latex/flashcards.html
"""
import json
from pathlib import Path
from build import REG, SRC, ROOT
from make_anki import parse_cards, md_to_html

OUT = ROOT / "flashcards.html"

def main():
    topics, cards = [], []
    for key, srcrel, title, kicker, num, acc, acc2 in REG:
        src = SRC / srcrel
        if not src.exists():
            continue
        parsed = parse_cards(src.read_text())
        if not parsed:
            continue
        name = title.replace("\\&", "&")
        ti = len(topics)
        topics.append({"name": name, "track": kicker, "accent": "#" + acc})
        for q, a in parsed:
            cards.append({"q": q, "a": a, "t": ti})

    data = {"topics": topics, "cards": cards}
    blob = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    html = TEMPLATE.replace("/*DATA*/", blob).replace("__N__", str(len(cards)))
    OUT.write_text(html, encoding="utf-8")
    print(f"  ok  {len(cards)} cards across {len(topics)} decks -> {OUT}")
    print(f"      open it:  xdg-open {OUT}")

TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Interview Flashcards</title>
<style>
  :root{
    --ink:#12172a; --ink2:#4b5468; --line:#e2e6ef; --bg:#eef1f8; --paper:#fff;
    --acc:#6366f1;
  }
  *{box-sizing:border-box}
  html,body{margin:0;height:100%}
  body{font-family:'Inter',system-ui,-apple-system,Segoe UI,Roboto,sans-serif;
    color:var(--ink);background:linear-gradient(180deg,#f6f8fc,#e9edf7);min-height:100%}
  code,pre{font-family:ui-monospace,'JetBrains Mono',Menlo,Consolas,monospace}
  .wrap{max-width:820px;margin:0 auto;padding:18px 16px 60px}
  header{display:flex;align-items:center;gap:12px;flex-wrap:wrap;margin:6px 0 14px}
  header h1{font-size:20px;margin:0;font-weight:800;letter-spacing:-.3px}
  header .sub{color:var(--ink2);font-size:13px}
  .controls{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:14px}
  select,button{font:inherit}
  select{padding:9px 12px;border:1px solid var(--line);border-radius:10px;background:#fff;
    color:var(--ink);font-weight:600;max-width:100%}
  .btn{padding:9px 14px;border:1px solid var(--line);border-radius:10px;background:#fff;
    cursor:pointer;font-weight:600;color:var(--ink);transition:.15s}
  .btn:hover{border-color:var(--acc);color:var(--acc)}
  .btn.primary{background:var(--acc);color:#fff;border-color:var(--acc)}
  .btn.primary:hover{filter:brightness(1.08);color:#fff}
  .toggle{display:flex;align-items:center;gap:7px;color:var(--ink2);font-size:13px;font-weight:600}
  .meta{display:flex;justify-content:space-between;align-items:center;color:var(--ink2);
    font-size:13px;margin:2px 2px 8px;font-weight:600}
  .bar{height:6px;border-radius:6px;background:#dfe5f1;overflow:hidden;margin:8px 2px 16px}
  .bar > i{display:block;height:100%;width:0;background:var(--acc);transition:width .25s}
  .card{background:var(--paper);border:1px solid var(--line);border-top:5px solid var(--acc);
    border-radius:18px;box-shadow:0 10px 30px rgba(20,30,60,.08);padding:26px 26px 22px;
    min-height:230px;cursor:pointer;position:relative}
  .pill{display:inline-block;font-size:11px;font-weight:700;color:#fff;background:var(--acc);
    padding:3px 10px;border-radius:999px;letter-spacing:.2px}
  .qlabel,.alabel{font-size:11px;font-weight:800;letter-spacing:1px;color:var(--acc);margin:14px 0 6px}
  .q{font-size:21px;line-height:1.35;font-weight:700}
  .divider{height:1px;background:var(--line);margin:18px 0 4px}
  .answer{font-size:15px;line-height:1.6;color:#1d2440}
  .answer b{color:var(--ink)}
  .answer code{background:#eef1f8;padding:1px 5px;border-radius:5px;font-size:.9em}
  .answer pre{font-size:12.5px;line-height:1.45}
  .hint{color:var(--ink2);font-size:13px;text-align:center;margin-top:14px}
  .hidden{display:none}
  .nav{display:flex;gap:10px;justify-content:center;margin-top:16px;flex-wrap:wrap}
  .known-badge{position:absolute;top:16px;right:18px;font-size:12px;font-weight:800;
    color:#059669;display:none}
  .card.known .known-badge{display:block}
  kbd{background:#fff;border:1px solid var(--line);border-bottom-width:2px;border-radius:6px;
    padding:1px 6px;font-size:11px;font-family:inherit;color:var(--ink2)}
  @media(max-width:560px){.q{font-size:18px}.card{padding:20px 18px}}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>📇 Interview Flashcards</h1>
    <span class="sub">__N__ cards from your notes' Q&amp;A — click a card to reveal the answer</span>
  </header>

  <div class="controls">
    <select id="deck"></select>
    <button class="btn" id="shuffle">⤮ Shuffle</button>
    <label class="toggle"><input type="checkbox" id="onlyNew"> study only unmastered</label>
    <button class="btn" id="reset" title="clear mastered marks">↺ Reset progress</button>
  </div>

  <div class="meta">
    <span id="pos">–</span>
    <span id="mastered">–</span>
  </div>
  <div class="bar"><i id="fill"></i></div>

  <div class="card" id="card">
    <span class="known-badge">✓ MASTERED</span>
    <span class="pill" id="topic">Topic</span>
    <div class="qlabel">QUESTION</div>
    <div class="q" id="q">…</div>
    <div id="aWrap" class="hidden">
      <div class="divider"></div>
      <div class="alabel">ANSWER</div>
      <div class="answer" id="a">…</div>
    </div>
    <div class="hint" id="hint">click / <kbd>Space</kbd> to reveal</div>
  </div>

  <div class="nav">
    <button class="btn" id="prev">← Prev</button>
    <button class="btn primary" id="flip">Show answer</button>
    <button class="btn" id="next">Next →</button>
    <button class="btn" id="mark">✓ Mastered</button>
  </div>
  <p class="hint" style="margin-top:18px">
    Keys: <kbd>←</kbd>/<kbd>→</kbd> navigate · <kbd>Space</kbd> flip · <kbd>M</kbd> mastered · <kbd>S</kbd> shuffle
  </p>
</div>

<script>
const DATA = /*DATA*/;
const LS = "flashcards.v1";
const store = JSON.parse(localStorage.getItem(LS) || "{}");
store.mastered = store.mastered || {};                 // {cardHash:true}
function save(){ localStorage.setItem(LS, JSON.stringify(store)); }
function hash(s){ let h=0; for(let i=0;i<s.length;i++){h=(h*31+s.charCodeAt(i))|0;} return h+""; }

// build deck options
const deck = document.getElementById('deck');
deck.add(new Option(`All decks (${DATA.cards.length})`, "-1"));
DATA.topics.forEach((t,i)=>{
  const n = DATA.cards.filter(c=>c.t===i).length;
  deck.add(new Option(`${t.name} (${n})`, i+""));
});
deck.value = (store.deck!=null? store.deck : "-1");

let order=[], idx=0, revealed=false;

function activeCards(){
  let cs = DATA.cards.map((c,i)=>({...c,i}));
  const d = +deck.value;
  if(d>=0) cs = cs.filter(c=>c.t===d);
  if(document.getElementById('onlyNew').checked)
    cs = cs.filter(c=>!store.mastered[hash(c.q)]);
  return cs;
}
function rebuild(keepPos){
  const cs = activeCards();
  order = cs.map((_,i)=>i);
  if(store.shuffle) shuffleArr(order);
  pool = cs;
  if(!keepPos) idx=0;
  if(idx>=order.length) idx=0;
  render();
}
function shuffleArr(a){ for(let i=a.length-1;i>0;i--){const j=Math.random()*(i+1)|0;[a[i],a[j]]=[a[j],a[i]];} }

let pool=[];
function cur(){ return pool[order[idx]]; }
function setAccent(hex){ document.documentElement.style.setProperty('--acc',hex); }

function render(){
  const card=document.getElementById('card');
  if(!pool.length){
    document.getElementById('q').textContent="🎉 Nothing left here — all mastered (or empty deck).";
    document.getElementById('topic').textContent="Done";
    document.getElementById('aWrap').classList.add('hidden');
    document.getElementById('pos').textContent="0 / 0";
    document.getElementById('fill').style.width="100%";
    return;
  }
  const c=cur(), t=DATA.topics[c.t];
  setAccent(t.accent);
  document.getElementById('topic').textContent=t.name;
  document.getElementById('q').innerHTML=c.q;
  document.getElementById('a').innerHTML=c.a;
  revealed=false;
  document.getElementById('aWrap').classList.add('hidden');
  document.getElementById('hint').classList.remove('hidden');
  document.getElementById('flip').textContent="Show answer";
  card.classList.toggle('known', !!store.mastered[hash(c.q)]);
  const masteredN = pool.filter(c=>store.mastered[hash(c.q)]).length;
  document.getElementById('pos').textContent=`Card ${idx+1} / ${pool.length}`;
  document.getElementById('mastered').textContent=`${masteredN} mastered in this deck`;
  document.getElementById('fill').style.width=((idx+1)/pool.length*100)+"%";
}
function flip(){
  if(!pool.length) return;
  revealed=!revealed;
  document.getElementById('aWrap').classList.toggle('hidden',!revealed);
  document.getElementById('hint').classList.toggle('hidden',revealed);
  document.getElementById('flip').textContent=revealed?"Hide answer":"Show answer";
}
function go(d){ if(!pool.length)return; idx=(idx+d+pool.length)%pool.length; render(); }
function mark(){
  if(!pool.length)return;
  const h=hash(cur().q);
  store.mastered[h]=!store.mastered[h]; save();
  document.getElementById('card').classList.toggle('known',!!store.mastered[h]);
  render();
}

document.getElementById('card').onclick=flip;
document.getElementById('flip').onclick=(e)=>{e.stopPropagation();flip();};
document.getElementById('next').onclick=()=>go(1);
document.getElementById('prev').onclick=()=>go(-1);
document.getElementById('mark').onclick=(e)=>{e.stopPropagation();mark();};
document.getElementById('shuffle').onclick=()=>{store.shuffle=true;save();rebuild();};
deck.onchange=()=>{store.deck=deck.value;save();rebuild();};
document.getElementById('onlyNew').onchange=rebuild;
document.getElementById('reset').onclick=()=>{
  if(confirm("Clear all 'mastered' marks?")){store.mastered={};save();render();}
};
document.addEventListener('keydown',e=>{
  if(e.target.tagName==='SELECT')return;
  if(e.key==='ArrowRight')go(1);
  else if(e.key==='ArrowLeft')go(-1);
  else if(e.key===' '){e.preventDefault();flip();}
  else if(e.key.toLowerCase()==='m')mark();
  else if(e.key.toLowerCase()==='s'){store.shuffle=true;save();rebuild();}
});
rebuild();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()

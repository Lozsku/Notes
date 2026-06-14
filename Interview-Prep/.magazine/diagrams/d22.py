# Hand-built HTML diagrams for 05-llm-applications-genai.md  (key = md5(ascii)[:12])
D = {}

# ---- RAG Full Pipeline (Ingest + Query) ----
D["6bc3f088d238"] = r'''
<div class="fig"><div class="figcap">RAG Pipeline · Ingest &amp; Query phases</div>
<div class="tiers">
  <div class="tier">
    <div class="th">INGEST PHASE</div>
    <div class="fcol">
      <div class="frow" style="flex-wrap:nowrap;align-items:center">
        <div class="node soft"><div class="nt">Raw Docs</div><div class="ns">PDF · HTML · DOCX · MD · CSV · code</div></div>
        <span class="ar">→</span>
        <div class="node"><div class="nt">Parser</div><div class="ns">text extract</div></div>
        <span class="ar">→</span>
        <div class="node"><div class="nt">Cleaner</div><div class="ns">normalize · tables</div></div>
        <span class="ar">→</span>
        <div class="node"><div class="nt">Chunker</div><div class="ns">256–512 tok + overlap</div></div>
        <span class="ar">→</span>
        <div class="node"><div class="nt">Embedder</div><div class="ns">e5 / bge · 768 dims</div></div>
        <span class="ar">→</span>
        <div class="node acc"><div class="nt">Vector DB</div><div class="ns">FAISS / Pinecone / pgvector</div></div>
      </div>
    </div>
  </div>
</div>
<div class="ar-d" style="margin:6px 0">↓ &nbsp; query time &nbsp; ↓</div>
<div class="tiers">
  <div class="tier">
    <div class="th">QUERY PHASE</div>
    <div class="fcol">
      <div class="frow" style="flex-wrap:nowrap;align-items:center">
        <div class="node soft"><div class="nt">User Query</div></div>
        <span class="ar">→</span>
        <div class="node"><div class="nt">Embed Query</div><div class="ns">same model!</div></div>
      </div>
      <div class="frow" style="flex-wrap:nowrap;align-items:flex-start;margin-top:8px">
        <div class="fcol" style="flex:1">
          <div class="frow" style="flex-wrap:nowrap;align-items:center">
            <span class="chip">semantic</span>
            <span class="ar">→</span>
            <div class="node"><div class="nt">ANN Search</div><div class="ns">Vector DB top-20</div></div>
          </div>
        </div>
        <div class="fcol" style="flex:1">
          <div class="frow" style="flex-wrap:nowrap;align-items:center">
            <span class="chip">keyword</span>
            <span class="ar">→</span>
            <div class="node"><div class="nt">BM25</div><div class="ns">Sparse index top-20</div></div>
          </div>
        </div>
      </div>
      <div class="ar-d">↓ RRF Fusion (Reciprocal Rank) ↓</div>
      <div class="frow" style="flex-wrap:nowrap;align-items:center">
        <div class="node"><div class="nt">Rerank</div><div class="ns">cross-encoder · top 3–5</div></div>
        <span class="ar">→</span>
        <div class="node"><div class="nt">Inject Prompt</div><div class="ns">context + query</div></div>
        <span class="ar">→</span>
        <div class="node acc"><div class="nt">LLM</div><div class="ns">generates answer</div></div>
        <span class="ar">→</span>
        <div class="node soft"><div class="nt">Post-process</div><div class="ns">citations · PII filter</div></div>
      </div>
    </div>
  </div>
</div>
<div class="fignote">Same embedding model used in both phases — ensures query &amp; chunk vectors live in the same space.</div></div>
'''

# ---- RAG Query Pipeline (detailed) ----
D["db5ca298505b"] = r'''
<div class="fig"><div class="figcap">RAG · Query Pipeline (detailed)</div>
<div class="fcol" style="align-items:center;gap:4px">
  <div class="node soft"><div class="nt">User Query</div></div>
  <div class="ar-d">↓</div>
  <div class="node"><div class="nt">Query Preprocessing</div><div class="ns">spell-correct · expand abbreviations · classify intent</div></div>
  <div class="ar-d">↓</div>
  <div class="node"><div class="nt">Embed Query</div><div class="ns">same model as ingest — query_vec = embed("How do I reset password?")</div></div>
  <div class="ar-d">↓</div>
  <div class="frow" style="flex-wrap:nowrap;align-items:center;gap:12px">
    <div class="node"><div class="nt">Vector ANN Search</div><div class="ns">top_k=20 semantic</div></div>
    <span style="font-size:1.2em;opacity:.6">+</span>
    <div class="node"><div class="nt">BM25 Keyword</div><div class="ns">top_k=20 sparse</div></div>
  </div>
  <div class="ar-d">↓ Hybrid Fusion (RRF) ↓</div>
  <div class="node"><div class="nt">Rerank</div><div class="ns">Cross-encoder re-scores top-K → picks best 3–5 for context</div></div>
  <div class="ar-d">↓</div>
  <div class="node"><div class="nt">Context Injection</div><div class="ns">build prompt with retrieved chunks</div></div>
  <div class="ar-d">↓</div>
  <div class="node acc"><div class="nt">LLM Generation</div><div class="ns">answer grounded in retrieved context</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">Post-Process</div><div class="ns">add citations · filter PII · validate format</div></div>
</div>
<div class="fignote">Hybrid retrieval (semantic + keyword) then cross-encoder reranking maximises both recall and precision.</div></div>
'''

# ---- ReAct Agent Loop ----
D["6b4beb0d6432"] = r'''
<div class="fig"><div class="figcap">ReAct Agent Loop · Thought → Action → Observation</div>
<svg viewBox="0 0 520 340" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="11">
  <!-- Goal box -->
  <rect x="160" y="10" width="200" height="40" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="260" y="28" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">USER GOAL</text>
  <text x="260" y="43" text-anchor="middle" fill="var(--acc-tx)" font-size="9">"Book me the cheapest flight NYC→SF"</text>
  <!-- arrow down to THOUGHT -->
  <line x1="260" y1="50" x2="260" y2="76" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- THOUGHT box -->
  <rect x="130" y="76" width="260" height="48" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="260" y="94" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">THOUGHT (LLM reasons)</text>
  <text x="260" y="113" text-anchor="middle" fill="var(--acc-tx)" font-size="9">"I need to search for flights first…"</text>
  <!-- arrow THOUGHT → ACTION -->
  <line x1="260" y1="124" x2="260" y2="150" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- ACTION box -->
  <rect x="130" y="150" width="260" height="48" rx="8" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.5"/>
  <text x="260" y="168" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">ACTION (structured tool call)</text>
  <text x="260" y="187" text-anchor="middle" fill="var(--acc-tx)" font-size="9">search_flights(origin="JFK", date="2024-01-16")</text>
  <!-- arrow ACTION → OBSERVATION -->
  <line x1="260" y1="198" x2="260" y2="224" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- OBSERVATION box -->
  <rect x="130" y="224" width="260" height="48" rx="8" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="260" y="242" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">OBSERVATION (tool result)</text>
  <text x="260" y="261" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Found 12 flights. Cheapest: UA234 $287 06:00</text>
  <!-- decision fork -->
  <line x1="260" y1="272" x2="260" y2="290" stroke="var(--acc)" stroke-width="1.5"/>
  <!-- left: continue loop back up -->
  <line x1="100" y1="290" x2="420" y2="290" stroke="var(--acc)" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="180" y="305" text-anchor="middle" fill="var(--acc-tx)" font-size="10">more steps?</text>
  <text x="380" y="305" text-anchor="middle" fill="var(--acc-tx)" font-size="10">done?</text>
  <!-- loop back arrow (left side) -->
  <line x1="100" y1="290" x2="100" y2="100" stroke="var(--acc)" stroke-width="1.2" stroke-dasharray="4,3" marker-end="url(#ah)"/>
  <line x1="100" y1="100" x2="130" y2="100" stroke="var(--acc)" stroke-width="1.2" stroke-dasharray="4,3"/>
  <!-- final answer (right) -->
  <rect x="360" y="310" width="140" height="24" rx="6" fill="var(--acc)" />
  <text x="430" y="326" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="11">FINAL ANSWER</text>
  <line x1="420" y1="290" x2="420" y2="310" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <defs>
    <marker id="ah" markerWidth="7" markerHeight="7" refX="5" refY="3.5" orient="auto">
      <polygon points="0 0, 7 3.5, 0 7" fill="var(--acc)"/>
    </marker>
  </defs>
</svg>
<div class="fignote">The Thought/Action/Observation loop repeats until the LLM is confident enough to emit a Final Answer.</div></div>
'''

# ---- Vector / ANN search — HNSW layers ----
D["fe5b70274d6a"] = r'''
<div class="fig"><div class="figcap">ANN Search · HNSW Hierarchical Layers</div>
<svg viewBox="0 0 520 260" style="display:block;margin:0 auto" font-family="'JetBrains Mono',monospace" font-size="10">
  <defs>
    <marker id="ah2" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
      <polygon points="0 0,6 3,0 6" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- layer labels -->
  <text x="8" y="50" fill="var(--acc-tx)" font-size="9" font-weight="700">Layer 2</text>
  <text x="8" y="52" dy="10" fill="var(--acc-tx)" font-size="8">(sparse)</text>
  <text x="8" y="130" fill="var(--acc-tx)" font-size="9" font-weight="700">Layer 1</text>
  <text x="8" y="132" dy="10" fill="var(--acc-tx)" font-size="8">(medium)</text>
  <text x="8" y="210" fill="var(--acc-tx)" font-size="9" font-weight="700">Layer 0</text>
  <text x="8" y="212" dy="10" fill="var(--acc-tx)" font-size="8">(dense)</text>

  <!-- Layer 2: N1 and N8 connected -->
  <line x1="110" y1="50" x2="410" y2="50" stroke="var(--acc2)" stroke-width="1.4"/>
  <circle cx="110" cy="50" r="14" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="110" y="54" text-anchor="middle" fill="var(--acc-tx)">N1</text>
  <circle cx="410" cy="50" r="14" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="410" y="54" text-anchor="middle" fill="var(--acc-tx)">N8</text>

  <!-- Layer 1: N1 N3 N5 N7 N8 -->
  <line x1="110" y1="130" x2="210" y2="130" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <line x1="210" y1="130" x2="310" y2="130" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <line x1="310" y1="130" x2="360" y2="130" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <line x1="360" y1="130" x2="410" y2="130" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <circle cx="110" cy="130" r="13" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="110" y="134" text-anchor="middle" fill="var(--acc-tx)">N1</text>
  <circle cx="210" cy="130" r="13" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="210" y="134" text-anchor="middle" fill="var(--acc-tx)">N3</text>
  <circle cx="310" cy="130" r="13" fill="var(--acc)" stroke="var(--acc)" stroke-width="2"/>
  <text x="310" y="134" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">N5</text>
  <circle cx="360" cy="130" r="13" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="360" y="134" text-anchor="middle" fill="var(--acc-tx)">N7</text>
  <circle cx="410" cy="130" r="13" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="410" y="134" text-anchor="middle" fill="var(--acc-tx)">N8</text>

  <!-- Layer 0: N1-N9 -->
  <line x1="85" y1="210" x2="460" y2="210" stroke="var(--acc-bd)" stroke-width="1"/>
  <circle cx="85"  cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="85"  y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N1</text>
  <circle cx="135" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="135" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N2</text>
  <circle cx="185" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="185" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N3</text>
  <circle cx="235" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="235" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N4</text>
  <!-- N5 highlighted as nearest -->
  <circle cx="285" cy="210" r="13" fill="var(--acc)" stroke="var(--acc)" stroke-width="2"/>
  <text x="285" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="700">N5</text>
  <circle cx="335" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="335" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N6</text>
  <circle cx="385" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="385" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N7</text>
  <circle cx="435" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="435" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N8</text>
  <circle cx="485" cy="210" r="11" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="485" y="214" text-anchor="middle" fill="var(--acc-tx)" font-size="9">N9</text>

  <!-- query vector star -->
  <polygon points="310,5 315,18 328,18 318,26 322,39 310,31 298,39 302,26 292,18 305,18"
           fill="var(--acc2)" stroke="var(--acc2)" stroke-width="1" opacity=".85"/>
  <text x="340" y="18" fill="var(--acc-tx)" font-size="9" font-weight="700">query q</text>

  <!-- descent arrows -->
  <line x1="310" y1="36" x2="310" y2="116" stroke="var(--acc2)" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#ah2)"/>
  <line x1="310" y1="143" x2="285" y2="197" stroke="var(--acc2)" stroke-width="1.5" stroke-dasharray="4,3" marker-end="url(#ah2)"/>

  <!-- search steps legend -->
  <text x="10" y="240" fill="var(--acc-tx)" font-size="8">1. Enter at Layer 2, greedy move to N8</text>
  <text x="10" y="252" fill="var(--acc-tx)" font-size="8">2. Descend → Layer 1, refine → N5</text>
  <text x="280" y="240" fill="var(--acc-tx)" font-size="8">3. Descend → Layer 0, scan neighbors</text>
  <text x="280" y="252" fill="var(--acc-tx)" font-size="8">4. Return top-K ≈ O(log N)</text>
</svg>
<div class="fignote">HNSW: long-range links in upper layers enable fast coarse navigation; dense lower layer gives precise top-K.</div></div>
'''

# ---- Function Calling / Tool Use ----
D["820377eed78c"] = r'''
<div class="fig"><div class="figcap">Function Calling · Tool Use Flow</div>
<div class="fcol" style="align-items:center;gap:4px">
  <div class="node soft"><div class="nt">User</div><div class="ns">"What's the weather in Tokyo?"</div></div>
  <div class="ar-d">↓</div>
  <div class="node"><div class="nt">LLM Processes Request</div><div class="ns">sees available tools: [get_weather] — decides to call it</div></div>
  <div class="ar-d">↓ LLM output is <em>structured JSON</em>, not text ↓</div>
  <div class="node acc"><div class="nt">Tool Call (JSON)</div><div class="ns">{ "name": "get_weather", "arguments": { "location": "Tokyo, Japan" } }</div></div>
  <div class="ar-d">↓ your code executes ↓</div>
  <div class="node"><div class="nt">Tool Execution</div><div class="ns">result = get_weather("Tokyo, Japan") → { "temp": 22, "condition": "Sunny" }</div></div>
  <div class="ar-d">↓ result appended as tool message ↓</div>
  <div class="node"><div class="nt">Feed Result Back to LLM</div><div class="ns">messages.append({ "role": "tool", "content": '{"temp":22,"condition":"Sunny"}' })</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">LLM Final Response (text)</div><div class="ns">"The weather in Tokyo is 22°C and sunny."</div></div>
</div>
<div class="fignote">The LLM never directly runs code — it outputs a <em>call spec</em>; your runtime executes and feeds results back.</div></div>
'''

# ---- Prompting vs RAG vs Fine-tune Decision Tree ----
D["6723b331fe9c"] = r'''
<div class="fig"><div class="figcap">Prompting vs RAG vs Fine-tune · Decision Tree</div>
<svg viewBox="0 0 520 320" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="10">
  <defs>
    <marker id="ah3" markerWidth="6" markerHeight="6" refX="4" refY="3" orient="auto">
      <polygon points="0 0,6 3,0 6" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- START -->
  <rect x="185" y="4" width="150" height="28" rx="14" fill="var(--acc)" />
  <text x="260" y="23" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="11">START: what's wrong?</text>

  <!-- Q1 -->
  <line x1="260" y1="32" x2="260" y2="55" stroke="var(--acc)" stroke-width="1.4" marker-end="url(#ah3)"/>
  <rect x="100" y="55" width="320" height="28" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="260" y="73" text-anchor="middle" fill="var(--acc-tx)">Model doesn't know your private data?</text>

  <!-- YES branch Q1 → Q1a -->
  <line x1="180" y1="83" x2="130" y2="105" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <text x="145" y="99" fill="var(--acc-tx)" font-size="9" font-style="italic">YES</text>
  <rect x="30" y="105" width="200" height="26" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="130" y="122" text-anchor="middle" fill="var(--acc-tx)">Fits in context window?</text>
  <!-- YES sub-branch → Prompting -->
  <line x1="80" y1="131" x2="60" y2="155" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <text x="58" y="149" fill="var(--acc-tx)" font-size="9" font-style="italic">YES</text>
  <rect x="4" y="155" width="120" height="26" rx="6" fill="var(--acc2)" stroke="var(--acc2)" stroke-width="1"/>
  <text x="64" y="172" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">Stuff in context</text>
  <!-- NO sub-branch → RAG -->
  <line x1="180" y1="131" x2="200" y2="155" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <text x="198" y="149" fill="var(--acc-tx)" font-size="9" font-style="italic">NO</text>
  <rect x="140" y="155" width="100" height="26" rx="6" fill="var(--acc)" stroke="var(--acc)" stroke-width="1"/>
  <text x="190" y="172" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">Use RAG</text>

  <!-- NO branch Q1 → Q2 -->
  <line x1="340" y1="83" x2="380" y2="105" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <text x="370" y="99" fill="var(--acc-tx)" font-size="9" font-style="italic">NO</text>
  <rect x="280" y="105" width="230" height="26" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="395" y="122" text-anchor="middle" fill="var(--acc-tx)">Wrong format / style / behavior?</text>
  <!-- YES → system prompt -->
  <line x1="340" y1="131" x2="320" y2="155" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <text x="320" y="149" fill="var(--acc-tx)" font-size="9" font-style="italic">YES</text>
  <rect x="258" y="155" width="130" height="26" rx="6" fill="var(--acc2)" stroke="var(--acc2)" stroke-width="1"/>
  <text x="323" y="172" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">System prompt + few-shot</text>

  <!-- Still failing → fine-tune -->
  <line x1="323" y1="181" x2="323" y2="200" stroke="var(--acc)" stroke-width="1.2" stroke-dasharray="3,3" marker-end="url(#ah3)"/>
  <text x="337" y="196" fill="var(--acc-tx)" font-size="9" font-style="italic">still failing?</text>
  <rect x="258" y="200" width="130" height="26" rx="6" fill="var(--acc)" stroke="var(--acc)" stroke-width="1"/>
  <text x="323" y="217" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">Fine-tune</text>

  <!-- NO → Q3 too slow -->
  <line x1="450" y1="131" x2="470" y2="155" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <text x="468" y="149" fill="var(--acc-tx)" font-size="9" font-style="italic">NO</text>
  <rect x="400" y="155" width="115" height="26" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="457" y="172" text-anchor="middle" fill="var(--acc-tx)">Too slow / costly?</text>
  <!-- YES → distill -->
  <line x1="457" y1="181" x2="457" y2="200" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#ah3)"/>
  <rect x="400" y="200" width="115" height="26" rx="6" fill="var(--acc)" stroke="var(--acc)" stroke-width="1"/>
  <text x="457" y="217" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">Distil / route</text>

  <!-- bottom note -->
  <rect x="60" y="250" width="400" height="50" rx="8" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="260" y="268" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">Rule of thumb</text>
  <text x="260" y="282" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Prompting → RAG → Fine-tune (in that order)</text>
  <text x="260" y="294" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Don't fine-tune as a first resort — it's expensive and slow.</text>
</svg>
<div class="fignote">Evaluate, identify the exact failure mode, then pick the cheapest fix that works.</div></div>
'''

# ---- LLM App Architecture (full tiers) ----
D["1cecb61530fd"] = r'''
<div class="fig"><div class="figcap">LLM Application Architecture · Full Stack</div>
<div class="tiers">
  <div class="tier" style="flex:0 0 100%">
    <div class="th">CLIENT LAYER</div>
    <div class="frow" style="flex-wrap:nowrap;justify-content:center;gap:8px">
      <div class="node soft"><div class="nt">Web</div></div>
      <div class="node soft"><div class="nt">Mobile</div></div>
      <div class="node soft"><div class="nt">Slack</div></div>
      <div class="node soft"><div class="nt">API consumers</div></div>
    </div>
  </div>
</div>
<div class="ar-d">↓ HTTPS / WebSocket ↓</div>
<div class="tiers">
  <div class="tier" style="flex:0 0 100%">
    <div class="th">API GATEWAY</div>
    <div class="frow" style="flex-wrap:nowrap;justify-content:center;gap:8px">
      <span class="chip">Rate limiting</span>
      <span class="chip">Auth (JWT)</span>
      <span class="chip">Request logging</span>
      <span class="chip">SSL termination</span>
    </div>
  </div>
</div>
<div class="ar-d">↓</div>
<div class="tiers">
  <div class="tier" style="flex:0 0 100%">
    <div class="th">ORCHESTRATION LAYER</div>
    <div class="frow" style="flex-wrap:nowrap;justify-content:center;gap:10px">
      <div class="node acc"><div class="nt">Router</div><div class="ns">small→large model</div></div>
      <div class="node acc"><div class="nt">Prompt Manager</div><div class="ns">templates · versions</div></div>
      <div class="node acc"><div class="nt">Context Manager</div><div class="ns">conv. history · compression</div></div>
    </div>
  </div>
</div>
<div class="ar-d">↓</div>
<div class="tiers">
  <div class="tier">
    <div class="th">LLM APIs</div>
    <div class="fcol">
      <div class="node"><div class="nt">OpenAI</div></div>
      <div class="node"><div class="nt">Anthropic</div></div>
      <div class="node"><div class="nt">Gemini</div></div>
      <span class="chip">+ semantic cache</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">VECTOR DB</div>
    <div class="fcol">
      <div class="node"><div class="nt">Pinecone</div></div>
      <div class="node"><div class="nt">pgvector</div></div>
      <div class="node"><div class="nt">FAISS</div></div>
      <span class="chip">+ rerank</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">TOOLS / FUNCTIONS</div>
    <div class="fcol">
      <div class="node"><div class="nt">Web search</div></div>
      <div class="node"><div class="nt">DB queries</div></div>
      <div class="node"><div class="nt">Code executor</div></div>
    </div>
  </div>
</div>
<div class="ar-d">↓</div>
<div class="tiers">
  <div class="tier" style="flex:0 0 100%">
    <div class="th">OBSERVABILITY</div>
    <div class="frow" style="flex-wrap:nowrap;justify-content:center;gap:8px">
      <span class="chip">Traces (LangSmith / Langfuse)</span>
      <span class="chip">Metrics (latency · cost · quality)</span>
      <span class="chip">Evals (RAGAS · LLM-as-judge)</span>
      <span class="chip">Alerts</span>
    </div>
  </div>
</div>
<div class="fignote">Router in orchestration enables 10× cost savings by directing simple queries to smaller models.</div></div>
'''

# ---- ReAct Example Trace (Thought/Action/Observation) ----
D["a7b5cf06d626"] = r'''
<div class="fig"><div class="figcap">ReAct · Example Trace (population of Paris)</div>
<div class="fcol" style="gap:6px">
  <div class="node soft"><div class="nt">Question</div><div class="ns">What is the population of the capital of France?</div></div>

  <div class="frow" style="flex-wrap:nowrap;align-items:flex-start;gap:6px">
    <div class="node" style="flex:1"><div class="nt">THOUGHT 1</div><div class="ns">I need to find the capital of France, then look up its population.</div></div>
    <span class="ar" style="margin-top:18px">→</span>
    <div class="node acc" style="flex:1"><div class="nt">ACTION 1</div><div class="ns">search("capital of France")</div></div>
    <span class="ar" style="margin-top:18px">→</span>
    <div class="node" style="flex:1"><div class="nt">OBSERVATION 1</div><div class="ns">Paris is the capital of France.</div></div>
  </div>

  <div class="frow" style="flex-wrap:nowrap;align-items:flex-start;gap:6px">
    <div class="node" style="flex:1"><div class="nt">THOUGHT 2</div><div class="ns">Now I need the population of Paris.</div></div>
    <span class="ar" style="margin-top:18px">→</span>
    <div class="node acc" style="flex:1"><div class="nt">ACTION 2</div><div class="ns">search("population of Paris 2024")</div></div>
    <span class="ar" style="margin-top:18px">→</span>
    <div class="node" style="flex:1"><div class="nt">OBSERVATION 2</div><div class="ns">Paris has a population of approx. 2.1 million.</div></div>
  </div>

  <div class="node" style="background:var(--acc-bg);border:1.5px solid var(--acc)">
    <div class="nt">THOUGHT 3 &amp; ANSWER</div>
    <div class="ns">I have all the information I need. → The population of Paris, the capital of France, is approximately 2.1 million.</div>
  </div>
</div>
<div class="fignote">Each Thought grounds the next Action; Observations arrive from real tool calls, reducing hallucination.</div></div>
'''

# ---- Safety Guardrails Pipeline ----
D["3351061f3ddd"] = r'''
<div class="fig"><div class="figcap">LLM Safety · Input &amp; Output Guardrails</div>
<div class="fcol" style="align-items:center;gap:4px">
  <div class="node soft"><div class="nt">User Input</div></div>
  <div class="ar-d">↓</div>
  <div class="node acc"><div class="nt">Input Classifier</div><div class="ns">detect: harmful intent · PII · jailbreak patterns</div></div>
  <div class="frow" style="gap:16px;margin:4px 0">
    <div class="node"><div class="nt">ALLOW</div></div>
    <div class="node"><div class="nt">BLOCK</div></div>
    <div class="node"><div class="nt">REWRITE</div></div>
  </div>
  <div class="ar-d">↓ (if allowed) ↓</div>
  <div class="node"><div class="nt">LLM Generation</div></div>
  <div class="ar-d">↓</div>
  <div class="node acc"><div class="nt">Output Classifier</div><div class="ns">detect: harmful content · PII in output · policy violations</div></div>
  <div class="frow" style="gap:16px;margin:4px 0">
    <div class="node"><div class="nt">ALLOW</div></div>
    <div class="node"><div class="nt">BLOCK</div></div>
    <div class="node"><div class="nt">SANITIZE</div></div>
  </div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">Final Response to User</div></div>
</div>
<div class="fignote">Dual classifier pattern: input guard stops bad requests; output guard catches policy violations even if the LLM slips.</div></div>
'''

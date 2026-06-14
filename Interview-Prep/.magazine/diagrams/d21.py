# Hand-built HTML diagrams for 21-transformers-and-llms.md  (key = md5(ascii)[:12])
D = {}

# ---- LLM Timeline (D3) ----
D["4766891debb1"] = r'''
<div class="fig"><div class="figcap">Large Language Model Timeline</div>
<div class="fcol" style="gap:4px">
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2018</div></div>
    <div class="node" style="flex:1"><div class="nt">GPT-1 <span class="chip">117M</span></div><div class="ns">pretraining + fine-tuning works</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2018</div></div>
    <div class="node acc" style="flex:1"><div class="nt">BERT <span class="chip">340M</span></div><div class="ns">bidirectional pretraining dominates NLU</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2019</div></div>
    <div class="node" style="flex:1"><div class="nt">GPT-2 <span class="chip">1.5B</span></div><div class="ns">"too dangerous to release" — language model can write</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2020</div></div>
    <div class="node" style="flex:1"><div class="nt">GPT-3 <span class="chip">175B</span></div><div class="ns">few-shot learning, emergent abilities</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2021</div></div>
    <div class="node" style="flex:1"><div class="nt">Codex <span class="chip">12B</span></div><div class="ns">GitHub Copilot launches</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2022</div></div>
    <div class="node acc" style="flex:1"><div class="nt">ChatGPT <span class="chip">GPT-3.5+RLHF</span></div><div class="ns">100M users in 60 days</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2023</div></div>
    <div class="node" style="flex:1"><div class="nt">GPT-4 <span class="chip">~1.8T MoE?</span></div><div class="ns">multimodal, bar exam top 10%</div></div>
  </div>
  <div class="frow" style="flex-wrap:nowrap;gap:6px;align-items:stretch">
    <div class="node soft" style="min-width:52px;text-align:center"><div class="nt" style="font-size:10px">2024</div></div>
    <div class="node" style="flex:1"><div class="nt">Claude / Gemini / Llama 3</div><div class="ns">long context, open weights, SOTA</div></div>
  </div>
</div>
<div class="fignote">Scale + compute + alignment = capability jumps; each generation unlocks new emergent behaviors.</div></div>
'''

# ---- Scaled Dot-Product Attention — SVG flow (D36) ----
D["68c0a44db0e3"] = r'''
<div class="fig"><div class="figcap">Scaled Dot-Product Attention</div>
<svg viewBox="0 0 520 310" style="display:block;margin:0 auto" font-family="'JetBrains Mono','Space Grotesk',monospace" font-size="11">
  <!-- Input labels: Q, K, V -->
  <text x="72" y="22" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">Q</text>
  <text x="192" y="22" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">K</text>
  <text x="380" y="22" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">V</text>

  <!-- Q and K arrows down -->
  <line x1="72" y1="26" x2="72" y2="48" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="192" y1="26" x2="192" y2="48" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="380" y1="26" x2="380" y2="138" stroke="var(--acc2)" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- MatMul(Q, Kᵀ) box -->
  <rect x="30" y="50" width="200" height="36" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="130" y="63" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">MatMul</text>
  <text x="130" y="78" fill="var(--acc)" text-anchor="middle" font-size="10">Q · Kᵀ</text>

  <!-- arrow down -->
  <line x1="130" y1="86" x2="130" y2="108" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Scale box -->
  <rect x="60" y="110" width="140" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="130" y="123" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">Scale</text>
  <text x="130" y="137" fill="var(--acc)" text-anchor="middle" font-size="10">÷ √d</text>
  <text x="136" y="141" fill="var(--acc)" font-size="7">k</text>

  <!-- arrow down -->
  <line x1="130" y1="144" x2="130" y2="166" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Optional Mask box -->
  <rect x="50" y="168" width="160" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd, var(--acc))" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="130" y="181" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">Mask (optional)</text>
  <text x="130" y="195" fill="var(--acc)" text-anchor="middle" font-size="9">causal: −∞ future tokens</text>

  <!-- arrow down -->
  <line x1="130" y1="202" x2="130" y2="224" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>

  <!-- Softmax box -->
  <rect x="60" y="226" width="140" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="130" y="241" fill="var(--acc-tx)" text-anchor="middle" font-weight="600">Softmax</text>
  <text x="130" y="255" fill="var(--acc)" text-anchor="middle" font-size="10">attention weights</text>

  <!-- arrow right then down to MatMul2 -->
  <line x1="130" y1="260" x2="130" y2="278" stroke="var(--acc)" stroke-width="1.5"/>

  <!-- MatMul(weights, V) box -->
  <rect x="30" y="278" width="200" height="28" rx="6" fill="var(--acc)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="130" y="292" fill="var(--acc-bg, #fff)" text-anchor="middle" font-weight="700" font-size="11">MatMul( ·, V )</text>

  <!-- V drops down to MatMul2 -->
  <line x1="380" y1="138" x2="247" y2="138" stroke="var(--acc2)" stroke-width="1.5"/>
  <line x1="247" y1="138" x2="247" y2="292" stroke="var(--acc2)" stroke-width="1.5"/>
  <line x1="247" y1="292" x2="230" y2="292" stroke="var(--acc2)" stroke-width="1.5" marker-end="url(#arr2)"/>

  <!-- Output arrow -->
  <line x1="130" y1="306" x2="130" y2="308" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="130" y="322" fill="var(--acc-tx)" text-anchor="middle" font-weight="600" font-size="11">Output</text>

  <!-- Formula at right -->
  <rect x="300" y="220" width="210" height="58" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1"/>
  <text x="405" y="238" fill="var(--acc-tx)" text-anchor="middle" font-size="9.5" font-weight="600">Attn(Q,K,V) =</text>
  <text x="405" y="254" fill="var(--acc)" text-anchor="middle" font-size="9">softmax( Q·Kᵀ / √d</text>
  <text x="487" y="258" fill="var(--acc)" font-size="7">k</text>
  <text x="496" y="254" fill="var(--acc)" font-size="9"> ) · V</text>
  <text x="405" y="271" fill="var(--acc-tx)" text-anchor="middle" font-size="8.5">O(n²·d) per head</text>

  <!-- arrowhead defs -->
  <defs>
    <marker id="arr" markerWidth="7" markerHeight="7" refX="3" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="var(--acc)"/>
    </marker>
    <marker id="arr2" markerWidth="7" markerHeight="7" refX="3" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="var(--acc2)"/>
    </marker>
  </defs>
</svg>
<div class="fignote">Q asks, K labels, V carries content. Scaling by √d<sub>k</sub> prevents softmax saturation in high dimensions.</div></div>
'''

# ---- Attention Step-by-Step (D8) ----
D["7c3c53310233"] = r'''
<div class="fig"><div class="figcap">Attention · 4-Step Computation</div>
<div class="fcol" style="gap:6px">
  <div class="frow" style="flex-wrap:nowrap;gap:8px;align-items:center">
    <div class="node acc" style="min-width:28px;text-align:center"><div class="nt">1</div></div>
    <div class="node" style="flex:1"><div class="nt">Raw Scores</div><div class="ns">scores = Q · Kᵀ &nbsp;→&nbsp; shape (n_tokens × n_tokens)</div></div>
  </div>
  <div class="ar-d">↓</div>
  <div class="frow" style="flex-wrap:nowrap;gap:8px;align-items:center">
    <div class="node acc" style="min-width:28px;text-align:center"><div class="nt">2</div></div>
    <div class="node" style="flex:1"><div class="nt">Scale</div><div class="ns">scores = scores / √d<sub>k</sub> &nbsp;— prevents softmax saturation</div></div>
  </div>
  <div class="ar-d">↓</div>
  <div class="frow" style="flex-wrap:nowrap;gap:8px;align-items:center">
    <div class="node acc" style="min-width:28px;text-align:center"><div class="nt">3</div></div>
    <div class="node" style="flex:1"><div class="nt">Softmax</div><div class="ns">weights = softmax(scores) &nbsp;→&nbsp; each row sums to 1.0</div></div>
  </div>
  <div class="ar-d">↓</div>
  <div class="frow" style="flex-wrap:nowrap;gap:8px;align-items:center">
    <div class="node acc" style="min-width:28px;text-align:center"><div class="nt">4</div></div>
    <div class="node" style="flex:1"><div class="nt">Weighted Sum of Values</div><div class="ns">output = weights · V &nbsp;→&nbsp; shape (n_tokens × d<sub>k</sub>)</div></div>
  </div>
</div>
<div class="fignote">Step 1 is O(n²) — the quadratic bottleneck. FlashAttention fuses steps 1-4 in a single CUDA kernel.</div></div>
'''

# ---- Multi-Head Attention (D37) ----
D["65a72c3b8186"] = r'''
<div class="fig"><div class="figcap">Multi-Head Attention</div>
<svg viewBox="0 0 520 260" style="display:block;margin:0 auto" font-family="'JetBrains Mono','Space Grotesk',monospace" font-size="10">
  <defs>
    <marker id="mha-arr" markerWidth="7" markerHeight="7" refX="3" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="var(--acc)"/>
    </marker>
  </defs>

  <!-- Input X label -->
  <text x="260" y="18" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">Input X</text>
  <!-- fan-out lines from X to 3 heads -->
  <line x1="260" y1="22" x2="80"  y2="52" stroke="var(--acc)" stroke-width="1.2"/>
  <line x1="260" y1="22" x2="260" y2="52" stroke="var(--acc)" stroke-width="1.2"/>
  <line x1="260" y1="22" x2="440" y2="52" stroke="var(--acc)" stroke-width="1.2"/>

  <!-- Head 1 -->
  <rect x="18" y="54" width="124" height="30" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.3"/>
  <text x="80" y="65" text-anchor="middle" fill="var(--acc-tx)" font-weight="600">W_Q¹ W_K¹ W_V¹</text>
  <text x="80" y="79" text-anchor="middle" fill="var(--acc)" font-size="9">head projections</text>
  <line x1="80" y1="84" x2="80" y2="104" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#mha-arr)"/>
  <rect x="22" y="106" width="116" height="28" rx="5" fill="var(--acc)" stroke="none"/>
  <text x="80" y="118" text-anchor="middle" fill="var(--acc-bg, #fff)" font-weight="700">Attention</text>
  <text x="80" y="130" text-anchor="middle" fill="var(--acc-bg, #fff)" font-size="9">head 1</text>

  <!-- Head 2 -->
  <rect x="198" y="54" width="124" height="30" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.3"/>
  <text x="260" y="65" text-anchor="middle" fill="var(--acc-tx)" font-weight="600">W_Q² W_K² W_V²</text>
  <text x="260" y="79" text-anchor="middle" fill="var(--acc)" font-size="9">head projections</text>
  <line x1="260" y1="84" x2="260" y2="104" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#mha-arr)"/>
  <rect x="202" y="106" width="116" height="28" rx="5" fill="var(--acc)" stroke="none"/>
  <text x="260" y="118" text-anchor="middle" fill="var(--acc-bg, #fff)" font-weight="700">Attention</text>
  <text x="260" y="130" text-anchor="middle" fill="var(--acc-bg, #fff)" font-size="9">head 2</text>

  <!-- Head h (ellipsis) -->
  <text x="380" y="80" text-anchor="middle" fill="var(--acc-tx)" font-size="18" font-weight="300">···</text>
  <rect x="378" y="54" width="124" height="30" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.3"/>
  <text x="440" y="65" text-anchor="middle" fill="var(--acc-tx)" font-weight="600">W_Qʰ W_Kʰ W_Vʰ</text>
  <text x="440" y="79" text-anchor="middle" fill="var(--acc)" font-size="9">head projections</text>
  <line x1="440" y1="84" x2="440" y2="104" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#mha-arr)"/>
  <rect x="382" y="106" width="116" height="28" rx="5" fill="var(--acc)" stroke="none"/>
  <text x="440" y="118" text-anchor="middle" fill="var(--acc-bg, #fff)" font-weight="700">Attention</text>
  <text x="440" y="130" text-anchor="middle" fill="var(--acc-bg, #fff)" font-size="9">head h</text>

  <!-- fan-in lines to Concat -->
  <line x1="80"  y1="134" x2="260" y2="166" stroke="var(--acc)" stroke-width="1.2"/>
  <line x1="260" y1="134" x2="260" y2="166" stroke="var(--acc)" stroke-width="1.2"/>
  <line x1="440" y1="134" x2="260" y2="166" stroke="var(--acc)" stroke-width="1.2"/>

  <!-- "···" between heads -->
  <text x="350" y="123" fill="var(--acc-tx)" text-anchor="middle" font-size="16">···</text>

  <!-- Concat box -->
  <rect x="178" y="168" width="164" height="28" rx="5" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.5"/>
  <text x="260" y="181" text-anchor="middle" fill="var(--acc-tx)" font-weight="700">Concat(head₁,…,headₕ)</text>
  <text x="260" y="192" text-anchor="middle" fill="var(--acc2)" font-size="8">shape: n × (h·d_k) = n × d_model</text>

  <!-- W_O projection -->
  <line x1="260" y1="196" x2="260" y2="216" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#mha-arr)"/>
  <rect x="200" y="218" width="120" height="26" rx="5" fill="var(--acc2)" stroke="none"/>
  <text x="260" y="232" text-anchor="middle" fill="var(--acc-bg, #fff)" font-weight="700">× W_O</text>
  <line x1="260" y1="244" x2="260" y2="256" stroke="var(--acc)" stroke-width="1.2" marker-end="url(#mha-arr)"/>
  <text x="260" y="262" text-anchor="middle" fill="var(--acc-tx)" font-weight="600" font-size="11">Output</text>
</svg>
<div class="fignote">h heads each learn different relationships; d<sub>k</sub> = d_model / h. Concat + W_O projects back to d_model.</div></div>
'''

# ---- Transformer Encoder Block (D38) ----
D["48eca6cb501b"] = r'''
<div class="fig"><div class="figcap">Transformer Encoder Block × N</div>
<div class="frow" style="flex-wrap:nowrap;gap:14px;align-items:flex-start">
  <!-- Left: input chain -->
  <div class="fcol" style="flex:1;gap:0">
    <div class="node soft" style="text-align:center"><div class="nt">Input Tokens</div></div>
    <div class="ar-d">↓</div>
    <div class="node" style="text-align:center"><div class="nt">Token Embeddings</div><div class="ns">+ Positional Encoding</div></div>
    <div class="ar-d">↓ × N blocks ↓</div>
    <!-- Encoder block -->
    <div class="stack">
      <div class="stk hl"><span class="sn">Multi-Head Self-Attention</span><span class="sd">all tokens attend to all tokens</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span><span class="sd">residual + LayerNorm</span></div>
      <div class="stk hl"><span class="sn">Feed-Forward Network</span><span class="sd">Linear → GELU → Linear (4× expand)</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span><span class="sd">residual + LayerNorm</span></div>
    </div>
    <div class="ar-d">↓</div>
    <div class="node acc" style="text-align:center"><div class="nt">Encoder Output</div><div class="ns">contextual embeddings for all positions</div></div>
  </div>
  <!-- Right: residual callout -->
  <div class="fcol" style="width:150px;gap:8px;padding-top:60px">
    <div class="callout c-key"><div class="ch">◆ Residual</div><p>Each sub-layer: output = LayerNorm(x + Sublayer(x))</p></div>
    <div class="callout c-ana"><div class="ch">◆ Bidirectional</div><p>Every token can attend to every other — ideal for understanding tasks (BERT).</p></div>
  </div>
</div>
<div class="fignote">N=6 in the original "Attention Is All You Need"; modern encoders use 12–24 layers.</div></div>
'''

# ---- GPT Decoder-Only Block (D40) ----
D["315b3031884f"] = r'''
<div class="fig"><div class="figcap">GPT Decoder-Only Block × L</div>
<div class="frow" style="flex-wrap:nowrap;gap:14px;align-items:flex-start">
  <div class="fcol" style="flex:1;gap:0">
    <div class="node soft" style="text-align:center"><div class="nt">Input Tokens</div></div>
    <div class="ar-d">↓</div>
    <div class="node" style="text-align:center"><div class="nt">Embeddings + Positional Encoding</div></div>
    <div class="ar-d">↓ × L blocks ↓</div>
    <div class="stack">
      <div class="stk"><span class="sn">LayerNorm (Pre-LN)</span><span class="sd">normalize before sublayer</span></div>
      <div class="stk hl"><span class="sn">Causal Multi-Head Attention</span><span class="sd">mask: each token sees only tokens to its left</span></div>
      <div class="stk"><span class="sn">+ Residual</span><span class="sd">skip connection</span></div>
      <div class="stk"><span class="sn">LayerNorm (Pre-LN)</span><span class="sd">normalize before sublayer</span></div>
      <div class="stk hl"><span class="sn">Feed-Forward Network</span><span class="sd">SwiGLU / GELU activation</span></div>
      <div class="stk"><span class="sn">+ Residual</span><span class="sd">skip connection</span></div>
    </div>
    <div class="ar-d">↓</div>
    <div class="node" style="text-align:center"><div class="nt">LayerNorm (final)</div></div>
    <div class="ar-d">↓</div>
    <div class="node" style="text-align:center"><div class="nt">Linear</div><div class="ns">d_model → vocab_size</div></div>
    <div class="ar-d">↓</div>
    <div class="node acc" style="text-align:center"><div class="nt">Softmax → Sample next token</div><div class="ns">append token, repeat →</div></div>
  </div>
  <div class="fcol" style="width:148px;gap:8px;padding-top:60px">
    <div class="callout c-warn"><div class="ch">◆ Causal Mask</div><p>Upper-triangle of attention matrix set to −∞ before softmax.</p></div>
    <div class="callout c-model"><div class="ch">◆ Pre-LN</div><p>LayerNorm before (not after) the sublayer stabilizes training at large scale.</p></div>
  </div>
</div>
<div class="fignote">Decoder-only = no cross-attention, no encoder. GPT-2/3/4, LLaMA, Claude, Gemini all use this architecture.</div></div>
'''

# ---- Positional Encoding (D41) ----
D["96581fb318cf"] = r'''
<div class="fig"><div class="figcap">Positional Encoding · Sinusoidal</div>
<svg viewBox="0 0 520 200" style="display:block;margin:0 auto" font-family="'JetBrains Mono','Space Grotesk',monospace" font-size="10">
  <defs>
    <marker id="pe-arr" markerWidth="7" markerHeight="7" refX="3" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- Formulas -->
  <rect x="10" y="10" width="500" height="52" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.3"/>
  <text x="260" y="28" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="11">Sinusoidal Positional Encoding</text>
  <text x="30" y="46" fill="var(--acc)" font-size="10">PE(pos, 2i)   = sin( pos / 10000^(2i/d_model) )</text>
  <text x="30" y="60" fill="var(--acc2)" font-size="10">PE(pos, 2i+1) = cos( pos / 10000^(2i/d_model) )</text>

  <!-- Table header -->
  <rect x="10" y="74" width="500" height="20" rx="0" fill="var(--acc)" stroke="none"/>
  <text x="55"  y="88" fill="var(--acc-bg, #fff)" text-anchor="middle" font-weight="700">Position</text>
  <text x="155" y="88" fill="var(--acc-bg, #fff)" text-anchor="middle" font-weight="700">Dim 0 (sin)</text>
  <text x="255" y="88" fill="var(--acc-bg, #fff)" text-anchor="middle" font-weight="700">Dim 1 (cos)</text>
  <text x="355" y="88" fill="var(--acc-bg, #fff)" text-anchor="middle" font-weight="700">Dim 2 (sin)</text>
  <text x="455" y="88" fill="var(--acc-bg, #fff)" text-anchor="middle" font-weight="700">Dim 3 (cos)</text>

  <!-- Row 0 -->
  <rect x="10" y="94" width="500" height="20" fill="var(--acc-bg)" stroke="none"/>
  <text x="55"  y="108" fill="var(--acc-tx)" text-anchor="middle">0</text>
  <text x="155" y="108" fill="var(--acc)"   text-anchor="middle">0.000</text>
  <text x="255" y="108" fill="var(--acc2)"  text-anchor="middle">1.000</text>
  <text x="355" y="108" fill="var(--acc)"   text-anchor="middle">0.000</text>
  <text x="455" y="108" fill="var(--acc2)"  text-anchor="middle">1.000</text>

  <!-- Row 1 -->
  <rect x="10" y="114" width="500" height="20" fill="none"/>
  <text x="55"  y="128" fill="var(--acc-tx)" text-anchor="middle">1</text>
  <text x="155" y="128" fill="var(--acc)"   text-anchor="middle">0.841</text>
  <text x="255" y="128" fill="var(--acc2)"  text-anchor="middle">0.540</text>
  <text x="355" y="128" fill="var(--acc)"   text-anchor="middle">0.100</text>
  <text x="455" y="128" fill="var(--acc2)"  text-anchor="middle">0.995</text>

  <!-- Row 2 -->
  <rect x="10" y="134" width="500" height="20" fill="var(--acc-bg)" stroke="none"/>
  <text x="55"  y="148" fill="var(--acc-tx)" text-anchor="middle">2</text>
  <text x="155" y="148" fill="var(--acc)"   text-anchor="middle">0.909</text>
  <text x="255" y="148" fill="var(--acc2)"  text-anchor="middle">−0.416</text>
  <text x="355" y="148" fill="var(--acc)"   text-anchor="middle">0.200</text>
  <text x="455" y="148" fill="var(--acc2)"  text-anchor="middle">0.980</text>

  <!-- Grid lines -->
  <line x1="10" y1="74" x2="510" y2="74" stroke="var(--acc)" stroke-width="0.5"/>
  <line x1="10" y1="94" x2="510" y2="94" stroke="var(--acc)" stroke-width="0.5"/>
  <line x1="10" y1="114" x2="510" y2="114" stroke="var(--acc)" stroke-width="0.3" stroke-dasharray="3,2"/>
  <line x1="10" y1="134" x2="510" y2="134" stroke="var(--acc)" stroke-width="0.5"/>
  <line x1="10" y1="154" x2="510" y2="154" stroke="var(--acc)" stroke-width="0.5"/>

  <!-- Key insight row -->
  <rect x="10" y="160" width="240" height="32" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1"/>
  <text x="130" y="174" fill="var(--acc-tx)" text-anchor="middle" font-weight="600" font-size="9.5">Low-freq dims (large i)</text>
  <text x="130" y="187" fill="var(--acc)" text-anchor="middle" font-size="9">capture coarse / global position</text>
  <rect x="270" y="160" width="240" height="32" rx="5" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1"/>
  <text x="390" y="174" fill="var(--acc-tx)" text-anchor="middle" font-weight="600" font-size="9.5">High-freq dims (small i)</text>
  <text x="390" y="187" fill="var(--acc2)" text-anchor="middle" font-size="9">capture fine-grained position</text>
</svg>
<div class="fignote">No learned params — PE is deterministic &amp; allows extrapolation. Modern models prefer RoPE (rotary) instead.</div></div>
'''

# ---- RLHF Pipeline (D42) ----
D["d2701c58c3e5"] = r'''
<div class="fig"><div class="figcap">RLHF Pipeline · 3 Stages</div>
<div class="tiers">
  <div class="tier">
    <div class="th">STAGE 1 — SFT</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Human Expert</div><div class="ns">writes ideal responses</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">Fine-tune Base LM</div><div class="ns">supervised learning on demonstrations</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">SFT Model (π_SFT)</div><div class="ns">follows instructions, not yet aligned</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">STAGE 2 — Reward Model</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Prompt → SFT → K responses</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Human Ranking</div><div class="ns">A &gt; B &gt; C &gt; D</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">Train Reward Model r_θ</div><div class="ns">loss: log σ(r(y_w) − r(y_l))</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">STAGE 3 — PPO</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Prompt → RL Policy (π_θ)</div><div class="ns">generates response</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Reward Model</div><div class="ns">scores response → scalar</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">KL Penalty</div><div class="ns">KL(π_θ ‖ π_SFT) — don't drift</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">PPO Update</div><div class="ns">clipped objective; repeat</div></div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:10px"><span class="chip">Result: Helpful · Harmless · Honest (HHH) model</span></div>
<div class="fignote">Stage 2 learns what humans prefer; Stage 3 maximizes that reward while staying close to the SFT model.</div></div>
'''

# ---- Tokenization Example (D43) ----
D["3da16dfd7301"] = r'''
<div class="fig"><div class="figcap">BPE Tokenization · "ChatGPT is transformative!"</div>
<div class="fcol" style="gap:6px">
  <!-- Input string -->
  <div class="node soft" style="text-align:center">
    <div class="nt" style="font-size:13px;letter-spacing:1px">"ChatGPT is transformative!"</div>
    <div class="ns">raw input text</div>
  </div>
  <div class="ar-d">↓ BPE (tiktoken / GPT-4) ↓</div>
  <!-- Token chips -->
  <div class="frow" style="flex-wrap:wrap;gap:8px;justify-content:center">
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">Chat</span>
      <span style="font-size:9px;color:var(--acc)">ID 14126</span>
    </div>
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">G</span>
      <span style="font-size:9px;color:var(--acc)">ID 38</span>
    </div>
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">PT</span>
      <span style="font-size:9px;color:var(--acc)">ID 2898</span>
    </div>
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">_is</span>
      <span style="font-size:9px;color:var(--acc)">ID 374</span>
    </div>
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">_transform</span>
      <span style="font-size:9px;color:var(--acc)">ID 5276</span>
    </div>
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">ative</span>
      <span style="font-size:9px;color:var(--acc)">ID 1413</span>
    </div>
    <div class="fcol" style="align-items:center;gap:2px">
      <span class="chip" style="font-size:12px;padding:4px 10px">!</span>
      <span style="font-size:9px;color:var(--acc)">ID 0</span>
    </div>
  </div>
  <!-- Stats row -->
  <div class="frow" style="gap:10px;margin-top:4px;justify-content:center">
    <div class="node" style="text-align:center;min-width:100px"><div class="nt">7 tokens</div><div class="ns">vs 4 words</div></div>
    <div class="node" style="text-align:center;min-width:160px"><div class="nt">Space in " is"</div><div class="ns">included in the token itself</div></div>
    <div class="node" style="text-align:center;min-width:140px"><div class="nt">"!" is own token</div><div class="ns">punctuation always separate</div></div>
  </div>
</div>
<div class="fignote">BPE merges frequent character pairs iteratively. Models don't see words — they see subword token IDs.</div></div>
'''

# ---- Q, K, V Projections (D6) ----
D["4b48ff8d0c66"] = r'''
<div class="fig"><div class="figcap">Q · K · V Projections</div>
<svg viewBox="0 0 520 190" style="display:block;margin:0 auto" font-family="'JetBrains Mono','Space Grotesk',monospace" font-size="10">
  <defs>
    <marker id="qkv-arr" markerWidth="7" markerHeight="7" refX="3" refY="3.5" orient="auto">
      <path d="M0,0 L0,7 L7,3.5 z" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- X box -->
  <rect x="210" y="10" width="100" height="32" rx="6" fill="var(--acc)" stroke="none"/>
  <text x="260" y="23" text-anchor="middle" fill="var(--acc-bg, #fff)" font-weight="700" font-size="12">X</text>
  <text x="260" y="37" text-anchor="middle" fill="var(--acc-bg, #fff)" font-size="9">n × d_model</text>

  <!-- fan out lines -->
  <line x1="200" y1="26" x2="80"  y2="80" stroke="var(--acc)" stroke-width="1.3"/>
  <line x1="260" y1="42" x2="260" y2="80" stroke="var(--acc)" stroke-width="1.3"/>
  <line x1="320" y1="26" x2="440" y2="80" stroke="var(--acc)" stroke-width="1.3"/>

  <!-- Q box -->
  <rect x="20" y="82" width="120" height="50" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="80" y="98"  text-anchor="middle" fill="var(--acc)"   font-weight="700" font-size="13">Q = X W_Q</text>
  <text x="80" y="113" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Query</text>
  <text x="80" y="126" text-anchor="middle" fill="var(--acc-tx)" font-size="8.5">"What am I looking for?"</text>

  <!-- K box -->
  <rect x="200" y="82" width="120" height="50" rx="6" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.5"/>
  <text x="260" y="98"  text-anchor="middle" fill="var(--acc2)"  font-weight="700" font-size="13">K = X W_K</text>
  <text x="260" y="113" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Key</text>
  <text x="260" y="126" text-anchor="middle" fill="var(--acc-tx)" font-size="8.5">"What do I offer/label as?"</text>

  <!-- V box -->
  <rect x="380" y="82" width="120" height="50" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="440" y="98"  text-anchor="middle" fill="var(--acc)"   font-weight="700" font-size="13">V = X W_V</text>
  <text x="440" y="113" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Value</text>
  <text x="440" y="126" text-anchor="middle" fill="var(--acc-tx)" font-size="8.5">"What is my content?"</text>

  <!-- dims note -->
  <rect x="10" y="146" width="500" height="36" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="0.8"/>
  <text x="260" y="161" text-anchor="middle" fill="var(--acc-tx)" font-size="9.5">X ∈ ℝ<tspan baseline-shift="super" font-size="7">n×d_model</tspan> &nbsp;·&nbsp; W_Q, W_K, W_V ∈ ℝ<tspan baseline-shift="super" font-size="7">d_model×d_k</tspan></text>
  <text x="260" y="176" text-anchor="middle" fill="var(--acc)"   font-size="9">Each head uses its own W_Q, W_K, W_V — learned independently</text>
</svg>
<div class="fignote">Three linear projections from the same input X; different weight matrices let each head specialize.</div></div>
'''

# ---- Full Transformer Encoder + Decoder Stack (D38+D39 combined) ----
D["08839bb9f359"] = r'''
<div class="fig"><div class="figcap">Full Transformer · Encoder–Decoder Architecture</div>
<div class="frow sb" style="flex-wrap:nowrap;gap:16px;align-items:flex-start">
  <!-- Encoder column -->
  <div class="fcol" style="flex:1;gap:0;min-width:180px">
    <div class="node soft" style="text-align:center"><div class="nt">Source Tokens</div></div>
    <div class="ar-d">↓</div>
    <div class="node" style="text-align:center"><div class="nt">Embeddings + PE</div></div>
    <div class="ar-d">↓ × N ↓</div>
    <div class="stack">
      <div class="stk hl"><span class="sn">Multi-Head Self-Attn</span><span class="sd">bidirectional</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span></div>
      <div class="stk hl"><span class="sn">Feed-Forward</span><span class="sd">Linear→GELU→Linear</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span></div>
    </div>
    <div class="ar-d">↓</div>
    <div class="node acc" style="text-align:center"><div class="nt">Encoder Output</div><div class="ns">K, V for cross-attn</div></div>
  </div>

  <!-- arrow connecting encoder to decoder -->
  <div style="align-self:center;padding-top:40px">
    <span class="ar" style="font-size:20px">→</span>
    <div style="font-size:9px;color:var(--acc);text-align:center;margin-top:4px">K, V</div>
  </div>

  <!-- Decoder column -->
  <div class="fcol" style="flex:1;gap:0;min-width:180px">
    <div class="node soft" style="text-align:center"><div class="nt">Target Tokens (shifted ▷)</div></div>
    <div class="ar-d">↓</div>
    <div class="node" style="text-align:center"><div class="nt">Embeddings + PE</div></div>
    <div class="ar-d">↓ × N ↓</div>
    <div class="stack">
      <div class="stk hl"><span class="sn">Masked Self-Attn</span><span class="sd">causal — no future tokens</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span></div>
      <div class="stk hl"><span class="sn">Cross-Attention</span><span class="sd">Q from decoder · K,V from encoder</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span></div>
      <div class="stk hl"><span class="sn">Feed-Forward</span><span class="sd">Linear→GELU→Linear</span></div>
      <div class="stk"><span class="sn">Add &amp; Norm</span></div>
    </div>
    <div class="ar-d">↓</div>
    <div class="node acc" style="text-align:center"><div class="nt">Linear + Softmax</div><div class="ns">P(next token | context)</div></div>
  </div>
</div>
<div class="fignote">"Attention Is All You Need" (Vaswani 2017). Used for seq2seq: translation, summarization. GPT uses decoder only.</div></div>
'''

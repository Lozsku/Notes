# Hand-built HTML diagrams for 20-deep-learning.md  (key = md5(ascii)[:12])
D = {}

# ---- Single Neuron: inputs × weights → sum → activation → output ----
D["5b6898ecbca7"] = r"""
<div class="fig"><div class="figcap">Single Neuron · Linear Combination + Activation</div>
<svg viewBox="0 0 520 180" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ah" markerWidth="8" markerHeight="8" refX="7" refY="3" orient="auto">
      <path d="M0,0 L0,6 L8,3 Z" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- Input nodes -->
  <circle cx="60" cy="50"  r="20" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="55"  text-anchor="middle" font-size="12" font-family="Space Grotesk" fill="var(--acc-tx)">x₁</text>
  <circle cx="60" cy="110" r="20" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="115" text-anchor="middle" font-size="12" font-family="Space Grotesk" fill="var(--acc-tx)">x₂</text>
  <circle cx="60" cy="170" r="20" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="175" text-anchor="middle" font-size="12" font-family="Space Grotesk" fill="var(--acc-tx)">x₃</text>
  <!-- Weight labels -->
  <text x="148" y="66"  font-size="10" font-family="JetBrains Mono" fill="var(--acc)" text-anchor="middle">w₁</text>
  <text x="200" y="100" font-size="10" font-family="JetBrains Mono" fill="var(--acc)" text-anchor="middle">w₂</text>
  <text x="148" y="152" font-size="10" font-family="JetBrains Mono" fill="var(--acc)" text-anchor="middle">w₃</text>
  <!-- Arrows from inputs to sum node -->
  <line x1="80"  y1="50"  x2="228" y2="98"  stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="80"  y1="110" x2="228" y2="110" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <line x1="80"  y1="170" x2="228" y2="122" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- Bias arrow from above -->
  <line x1="250" y1="30" x2="250" y2="78" stroke="var(--acc2,#888)" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#ah)"/>
  <text x="260" y="22" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)">b (bias)</text>
  <!-- Sum node -->
  <circle cx="250" cy="110" r="28" fill="var(--acc)" opacity="0.15" stroke="var(--acc)" stroke-width="2"/>
  <text x="250" y="106" text-anchor="middle" font-size="13" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Σ</text>
  <text x="250" y="122" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">W·x+b</text>
  <!-- Arrow to activation -->
  <line x1="278" y1="110" x2="340" y2="110" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- Activation node -->
  <rect x="342" y="86" width="64" height="48" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="374" y="106" text-anchor="middle" font-size="11" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">f(·)</text>
  <text x="374" y="124" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">σ / ReLU</text>
  <!-- Arrow to output -->
  <line x1="406" y1="110" x2="464" y2="110" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ah)"/>
  <!-- Output node -->
  <circle cx="480" cy="110" r="20" fill="var(--acc)" opacity="0.85" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="480" y="115" text-anchor="middle" font-size="12" font-family="Space Grotesk" fill="#fff" font-weight="700">y</text>
</svg>
<div class="fignote">y = f(w₁x₁ + w₂x₂ + w₃x₃ + b) — the fundamental building block of all neural networks.</div></div>
"""

# ---- Multi-Layer Perceptron ----
D["11f08ad5882e"] = r"""
<div class="fig"><div class="figcap">Multi-Layer Perceptron · Fully Connected Layers</div>
<svg viewBox="0 0 520 220" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ah2" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 Z" fill="var(--acc-bd)"/>
    </marker>
  </defs>
  <!-- Layer labels -->
  <text x="60"  y="18" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">INPUT</text>
  <text x="200" y="18" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">HIDDEN 1</text>
  <text x="340" y="18" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">HIDDEN 2</text>
  <text x="470" y="18" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">OUTPUT</text>
  <!-- Input layer nodes: 4 neurons -->
  <circle cx="60" cy="50"  r="16" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="55"  text-anchor="middle" font-size="10" font-family="JetBrains Mono" fill="var(--acc-tx)">x₁</text>
  <circle cx="60" cy="95"  r="16" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="100" text-anchor="middle" font-size="10" font-family="JetBrains Mono" fill="var(--acc-tx)">x₂</text>
  <circle cx="60" cy="140" r="16" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="145" text-anchor="middle" font-size="10" font-family="JetBrains Mono" fill="var(--acc-tx)">x₃</text>
  <circle cx="60" cy="185" r="16" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="60" y="190" text-anchor="middle" font-size="10" font-family="JetBrains Mono" fill="var(--acc-tx)">x₄</text>
  <!-- Hidden 1 nodes: 4 neurons -->
  <circle cx="200" cy="50"  r="16" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="200" y="55"  text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₁</text>
  <circle cx="200" cy="95"  r="16" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="200" y="100" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₂</text>
  <circle cx="200" cy="140" r="16" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="200" y="145" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₃</text>
  <circle cx="200" cy="185" r="16" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="200" y="190" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₄</text>
  <!-- Hidden 2 nodes: 4 neurons -->
  <circle cx="340" cy="50"  r="16" fill="var(--acc)" opacity="0.55" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="340" y="55"  text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₁</text>
  <circle cx="340" cy="95"  r="16" fill="var(--acc)" opacity="0.55" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="340" y="100" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₂</text>
  <circle cx="340" cy="140" r="16" fill="var(--acc)" opacity="0.55" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="340" y="145" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₃</text>
  <circle cx="340" cy="185" r="16" fill="var(--acc)" opacity="0.55" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="340" y="190" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="#fff">h₄</text>
  <!-- Output nodes: 3 neurons -->
  <circle cx="470" cy="72"  r="16" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="470" y="77"  text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">y₁</text>
  <circle cx="470" cy="117" r="16" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="470" y="122" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">y₂</text>
  <circle cx="470" cy="162" r="16" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="470" y="167" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">y₃</text>
  <!-- Connections: input→hidden1 (all pairs, thin) -->
  <g stroke="var(--acc-bd)" stroke-width="0.7" opacity="0.5">
    <line x1="76" y1="50"  x2="184" y2="50"/>  <line x1="76" y1="50"  x2="184" y2="95"/>
    <line x1="76" y1="50"  x2="184" y2="140"/> <line x1="76" y1="50"  x2="184" y2="185"/>
    <line x1="76" y1="95"  x2="184" y2="50"/>  <line x1="76" y1="95"  x2="184" y2="95"/>
    <line x1="76" y1="95"  x2="184" y2="140"/> <line x1="76" y1="95"  x2="184" y2="185"/>
    <line x1="76" y1="140" x2="184" y2="50"/>  <line x1="76" y1="140" x2="184" y2="95"/>
    <line x1="76" y1="140" x2="184" y2="140"/> <line x1="76" y1="140" x2="184" y2="185"/>
    <line x1="76" y1="185" x2="184" y2="50"/>  <line x1="76" y1="185" x2="184" y2="95"/>
    <line x1="76" y1="185" x2="184" y2="140"/> <line x1="76" y1="185" x2="184" y2="185"/>
  </g>
  <!-- Connections: hidden1→hidden2 -->
  <g stroke="var(--acc)" stroke-width="0.7" opacity="0.35">
    <line x1="216" y1="50"  x2="324" y2="50"/>  <line x1="216" y1="50"  x2="324" y2="95"/>
    <line x1="216" y1="50"  x2="324" y2="140"/> <line x1="216" y1="50"  x2="324" y2="185"/>
    <line x1="216" y1="95"  x2="324" y2="50"/>  <line x1="216" y1="95"  x2="324" y2="95"/>
    <line x1="216" y1="95"  x2="324" y2="140"/> <line x1="216" y1="95"  x2="324" y2="185"/>
    <line x1="216" y1="140" x2="324" y2="50"/>  <line x1="216" y1="140" x2="324" y2="95"/>
    <line x1="216" y1="140" x2="324" y2="140"/> <line x1="216" y1="140" x2="324" y2="185"/>
    <line x1="216" y1="185" x2="324" y2="50"/>  <line x1="216" y1="185" x2="324" y2="95"/>
    <line x1="216" y1="185" x2="324" y2="140"/> <line x1="216" y1="185" x2="324" y2="185"/>
  </g>
  <!-- Connections: hidden2→output -->
  <g stroke="var(--acc)" stroke-width="0.9" opacity="0.5">
    <line x1="356" y1="50"  x2="454" y2="72"/>  <line x1="356" y1="50"  x2="454" y2="117"/> <line x1="356" y1="50"  x2="454" y2="162"/>
    <line x1="356" y1="95"  x2="454" y2="72"/>  <line x1="356" y1="95"  x2="454" y2="117"/> <line x1="356" y1="95"  x2="454" y2="162"/>
    <line x1="356" y1="140" x2="454" y2="72"/>  <line x1="356" y1="140" x2="454" y2="117"/> <line x1="356" y1="140" x2="454" y2="162"/>
    <line x1="356" y1="185" x2="454" y2="72"/>  <line x1="356" y1="185" x2="454" y2="117"/> <line x1="356" y1="185" x2="454" y2="162"/>
  </g>
</svg>
<div class="fignote">Every node in one layer connects to every node in the next (fully-connected). Each edge is a learnable weight.</div></div>
"""

# ---- Forward + Backprop flow ----
D["18f64c17369d"] = r"""
<div class="fig"><div class="figcap">Forward Pass &amp; Backpropagation · Chain Rule</div>
<svg viewBox="0 0 520 200" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="fwd" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc)"/>
    </marker>
    <marker id="bwd" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc2,#e07)"/>
    </marker>
  </defs>
  <!-- Forward pass label -->
  <text x="10" y="38" font-size="10" font-family="Space Grotesk" fill="var(--acc)" font-weight="700">FORWARD →</text>
  <!-- Nodes: x, L1, L2, ŷ, Loss -->
  <rect x="8"   y="55" width="52" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="34"  y="70" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Input</text>
  <text x="34"  y="87" text-anchor="middle" font-size="9"  font-family="JetBrains Mono" fill="var(--acc-tx)">x</text>

  <rect x="100" y="55" width="80" height="40" rx="6" fill="var(--acc)" opacity="0.75" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="140" y="70" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">Layer 1</text>
  <text x="140" y="85" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">z¹=W¹x+b¹</text>

  <rect x="222" y="55" width="80" height="40" rx="6" fill="var(--acc)" opacity="0.6" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="262" y="70" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">Layer 2</text>
  <text x="262" y="85" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">z²=W²a¹+b²</text>

  <rect x="344" y="55" width="52" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="370" y="70" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">ŷ</text>
  <text x="370" y="87" text-anchor="middle" font-size="8"  font-family="JetBrains Mono" fill="var(--acc-tx)">pred</text>

  <rect x="440" y="55" width="68" height="40" rx="6" fill="var(--acc2,#e07)" opacity="0.2" stroke="var(--acc2,#e07)" stroke-width="2"/>
  <text x="474" y="70" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Loss</text>
  <text x="474" y="87" text-anchor="middle" font-size="9"  font-family="JetBrains Mono" fill="var(--acc-tx)">L(ŷ,y)</text>

  <!-- Forward arrows -->
  <line x1="60"  y1="75" x2="98"  y2="75" stroke="var(--acc)" stroke-width="2" marker-end="url(#fwd)"/>
  <line x1="180" y1="75" x2="220" y2="75" stroke="var(--acc)" stroke-width="2" marker-end="url(#fwd)"/>
  <line x1="302" y1="75" x2="342" y2="75" stroke="var(--acc)" stroke-width="2" marker-end="url(#fwd)"/>
  <line x1="396" y1="75" x2="438" y2="75" stroke="var(--acc)" stroke-width="2" marker-end="url(#fwd)"/>

  <!-- Backward pass label -->
  <text x="10" y="148" font-size="10" font-family="Space Grotesk" fill="var(--acc2,#e07)" font-weight="700">← BACKWARD</text>

  <!-- Backward arrows (below, going right-to-left) -->
  <line x1="438" y1="145" x2="398" y2="145" stroke="var(--acc2,#e07)" stroke-width="2" marker-end="url(#bwd)"/>
  <text x="418" y="139" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">dL/dŷ</text>

  <line x1="342" y1="145" x2="302" y2="145" stroke="var(--acc2,#e07)" stroke-width="2" marker-end="url(#bwd)"/>
  <text x="322" y="139" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">dL/da²</text>

  <line x1="220" y1="145" x2="180" y2="145" stroke="var(--acc2,#e07)" stroke-width="2" marker-end="url(#bwd)"/>
  <text x="200" y="139" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">dL/dW²</text>

  <line x1="98"  y1="145" x2="62"  y2="145" stroke="var(--acc2,#e07)" stroke-width="2" marker-end="url(#bwd)"/>
  <text x="80"   y="139" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">dL/dW¹</text>

  <!-- Vertical connectors from nodes to backprop line -->
  <line x1="140" y1="95"  x2="140" y2="145" stroke="var(--acc2,#e07)" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <line x1="262" y1="95"  x2="262" y2="145" stroke="var(--acc2,#e07)" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <line x1="370" y1="95"  x2="370" y2="145" stroke="var(--acc2,#e07)" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>
  <line x1="474" y1="95"  x2="474" y2="145" stroke="var(--acc2,#e07)" stroke-width="1" stroke-dasharray="3,2" opacity="0.6"/>

  <!-- Chain rule note -->
  <text x="260" y="180" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">dL/dW² = dL/da² · f′(z²) · a¹ᵀ</text>
</svg>
<div class="fignote">Forward pass computes predictions left→right; backward pass propagates gradients right→left via the chain rule.</div></div>
"""

# ---- Activation Function Shapes (SVG plots) ----
D["a574c16a6196"] = r"""
<div class="fig"><div class="figcap">Activation Functions · Shape Comparison</div>
<svg viewBox="0 0 520 160" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <!-- ===== Sigmoid ===== -->
  <text x="65"  y="14" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Sigmoid σ</text>
  <!-- axes -->
  <line x1="10" y1="95" x2="120" y2="95" stroke="var(--acc-bd)" stroke-width="1"/>
  <line x1="65" y1="25" x2="65"  y2="105" stroke="var(--acc-bd)" stroke-width="1"/>
  <!-- axis labels -->
  <text x="65" y="118" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">0</text>
  <text x="8"  y="73"  text-anchor="start"  font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">1</text>
  <text x="8"  y="98"  text-anchor="start"  font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">.5</text>
  <!-- sigmoid curve: from (10,91) to (120,31), midpoint at (65,63) -->
  <path d="M10,92 C25,92 40,88 52,80 C58,76 62,68 65,63 C68,58 72,50 80,44 C92,36 105,32 120,31"
        fill="none" stroke="var(--acc)" stroke-width="2.2"/>
  <!-- 0.5 dashed line -->
  <line x1="10" y1="63" x2="120" y2="63" stroke="var(--acc)" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.5"/>

  <!-- ===== Tanh ===== -->
  <text x="195" y="14" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Tanh</text>
  <!-- axes -->
  <line x1="140" y1="75" x2="250" y2="75" stroke="var(--acc-bd)" stroke-width="1"/>
  <line x1="195" y1="25" x2="195" y2="110" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="195" y="122" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">0</text>
  <text x="138" y="38"  text-anchor="start"  font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">+1</text>
  <text x="138" y="108" text-anchor="start"  font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">-1</text>
  <!-- tanh curve: S-shape centered at (195,75) ranging ±30 -->
  <path d="M140,105 C155,105 165,95 178,83 C185,77 190,76 195,75 C200,74 205,73 212,67 C225,55 235,45 250,45"
        fill="none" stroke="var(--acc)" stroke-width="2.2"/>
  <line x1="140" y1="45"  x2="250" y2="45"  stroke="var(--acc)" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.4"/>
  <line x1="140" y1="105" x2="250" y2="105" stroke="var(--acc)" stroke-width="0.8" stroke-dasharray="3,2" opacity="0.4"/>

  <!-- ===== ReLU ===== -->
  <text x="325" y="14" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">ReLU</text>
  <!-- axes -->
  <line x1="270" y1="95" x2="385" y2="95" stroke="var(--acc-bd)" stroke-width="1"/>
  <line x1="325" y1="25" x2="325" y2="105" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="325" y="115" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">0</text>
  <!-- ReLU: flat then rising -->
  <path d="M270,95 L325,95 L385,35" fill="none" stroke="var(--acc)" stroke-width="2.2"/>

  <!-- ===== Leaky ReLU ===== -->
  <text x="460" y="14" text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Leaky ReLU</text>
  <!-- axes -->
  <line x1="405" y1="80" x2="515" y2="80" stroke="var(--acc-bd)" stroke-width="1"/>
  <line x1="460" y1="25" x2="460" y2="110" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="460" y="120" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">0</text>
  <!-- Leaky ReLU: small slope left, steeper right -->
  <path d="M405,90 L460,80 L515,25" fill="none" stroke="var(--acc)" stroke-width="2.2"/>
  <text x="412" y="76" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">0.01x</text>
</svg>
<div class="frow" style="flex-wrap:wrap;gap:8px;margin-top:6px">
  <span class="chip">Sigmoid: (0,1) — saturates</span>
  <span class="chip">Tanh: (-1,1) — zero-centered</span>
  <span class="chip">ReLU: max(0,x) — dead for x&lt;0</span>
  <span class="chip">LeakyReLU: small grad for x&lt;0</span>
</div>
<div class="fignote">ReLU and its variants dominate modern networks; sigmoid/tanh cause vanishing gradients in deep stacks.</div></div>
"""

# ---- CNN Pipeline ----
D["22272fb86359"] = r"""
<div class="fig"><div class="figcap">Convolutional Neural Network · Image Classification Pipeline</div>
<div class="tiers" style="align-items:stretch">
  <div class="tier">
    <div class="th">INPUT</div>
    <div class="fcol" style="justify-content:center;height:100%">
      <div class="node soft"><div class="nt">28×28×1</div><div class="ns">raw pixels</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">CONV + ReLU</div>
    <div class="fcol" style="justify-content:center;height:100%">
      <div class="node acc"><div class="nt">26×26×32</div><div class="ns">3×3 · 32 filters</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">MAX POOL</div>
    <div class="fcol" style="justify-content:center;height:100%">
      <div class="node soft"><div class="nt">13×13×32</div><div class="ns">2×2 pool</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">CONV + ReLU</div>
    <div class="fcol" style="justify-content:center;height:100%">
      <div class="node acc"><div class="nt">11×11×64</div><div class="ns">3×3 · 64 filters</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">FLATTEN</div>
    <div class="fcol" style="justify-content:center;height:100%">
      <div class="node"><div class="nt">7744</div><div class="ns">1-D vector</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">FC + Softmax</div>
    <div class="fcol" style="justify-content:center;height:100%">
      <div class="node acc"><div class="nt">10</div><div class="ns">class scores</div></div>
    </div>
  </div>
</div>
<div class="fignote">Each conv layer slides learnable filters across the spatial input — earlier layers detect edges, later layers detect semantics.</div></div>
"""

# ---- Unrolled RNN + LSTM Cell ----
D["39cb8d060899"] = r"""
<div class="fig"><div class="figcap">Recurrent Network · Unrolled RNN &amp; LSTM Cell</div>
<svg viewBox="0 0 520 220" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ra" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- RNN label -->
  <text x="10" y="16" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="700">Vanilla RNN (unrolled across time)</text>

  <!-- h0 -->
  <rect x="10" y="30" width="36" height="30" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="28" y="50" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">h₀</text>

  <!-- RNN cell t=1 -->
  <rect x="65" y="25" width="60" height="40" rx="6" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="95" y="42" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">RNN</text>
  <text x="95" y="57" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">t=1</text>
  <!-- x1 -->
  <line x1="95" y1="75" x2="95" y2="65" stroke="var(--acc-bd)" stroke-width="1.2" marker-end="url(#ra)"/>
  <text x="95" y="88" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">x₁</text>
  <!-- h0→rnn1 -->
  <line x1="46"  y1="45" x2="63"  y2="45" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ra)"/>

  <!-- RNN cell t=2 -->
  <rect x="168" y="25" width="60" height="40" rx="6" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="198" y="42" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">RNN</text>
  <text x="198" y="57" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">t=2</text>
  <line x1="198" y1="75" x2="198" y2="65" stroke="var(--acc-bd)" stroke-width="1.2" marker-end="url(#ra)"/>
  <text x="198" y="88" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">x₂</text>
  <!-- h1→rnn2 -->
  <line x1="125" y1="45" x2="166" y2="45" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ra)"/>
  <text x="146" y="40" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">h₁</text>

  <!-- RNN cell t=3 -->
  <rect x="271" y="25" width="60" height="40" rx="6" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="301" y="42" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">RNN</text>
  <text x="301" y="57" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">t=3</text>
  <line x1="301" y1="75" x2="301" y2="65" stroke="var(--acc-bd)" stroke-width="1.2" marker-end="url(#ra)"/>
  <text x="301" y="88" text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">x₃</text>
  <!-- h2→rnn3 -->
  <line x1="228" y1="45" x2="269" y2="45" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ra)"/>
  <text x="249" y="40" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">h₂</text>
  <!-- h3 out -->
  <line x1="331" y1="45" x2="358" y2="45" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ra)"/>
  <text x="370" y="49" text-anchor="start" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">h₃</text>

  <!-- Shared weights note -->
  <text x="390" y="35" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)">Shared W_xh,</text>
  <text x="390" y="48" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)">W_hh each step</text>

  <!-- Divider -->
  <line x1="10" y1="100" x2="510" y2="100" stroke="var(--acc-bd)" stroke-width="0.8" stroke-dasharray="4,3"/>

  <!-- LSTM label -->
  <text x="10" y="116" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="700">LSTM Cell · t</text>

  <!-- Cell state highway -->
  <text x="14" y="136" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">c_{t-1}</text>
  <line x1="55"  y1="132" x2="390" y2="132" stroke="var(--acc)" stroke-width="2" stroke-dasharray="6,2" marker-end="url(#ra)"/>
  <text x="395" y="136" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">c_t</text>

  <!-- Gate boxes -->
  <!-- Forget gate -->
  <rect x="70" y="145" width="58" height="56" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="99" y="162" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Forget</text>
  <text x="99" y="175" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">Gate f</text>
  <text x="99" y="190" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">sigmoid</text>

  <!-- Input gate -->
  <rect x="155" y="145" width="58" height="56" rx="6" fill="var(--acc)" opacity="0.6" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="184" y="162" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">Input</text>
  <text x="184" y="175" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">Gate i</text>
  <text x="184" y="190" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">sigmoid</text>

  <!-- Cell gate -->
  <rect x="240" y="145" width="58" height="56" rx="6" fill="var(--acc)" opacity="0.4" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="269" y="162" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Cell</text>
  <text x="269" y="175" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">Gate g</text>
  <text x="269" y="190" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">tanh</text>

  <!-- Output gate -->
  <rect x="325" y="145" width="60" height="56" rx="6" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="355" y="162" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="#fff" font-weight="600">Output</text>
  <text x="355" y="175" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">Gate o</text>
  <text x="355" y="190" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="#fff">sigmoid</text>

  <!-- Inputs to gates (x_t, h_{t-1}) -->
  <text x="70" y="215" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">x_t, h_{t-1} → all gates</text>

  <!-- Output h_t -->
  <line x1="385" y1="173" x2="440" y2="173" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ra)"/>
  <text x="445" y="177" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">h_t</text>

  <!-- Key insight -->
  <text x="440" y="135" font-size="8" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">c_t uses +</text>
  <text x="440" y="147" font-size="8" font-family="Space Grotesk" fill="var(--acc-tx)">(gradient</text>
  <text x="440" y="159" font-size="8" font-family="Space Grotesk" fill="var(--acc-tx)">highway!)</text>
</svg>
<div class="fignote">LSTM replaces vanishing-gradient multiplication with additive cell-state updates — the key to long-range memory.</div></div>
"""

# ---- Gradient Descent Steps down a Loss Curve ----
D["6a1972d8fb25"] = r"""
<div class="fig"><div class="figcap">Gradient Descent · Navigating the Loss Landscape</div>
<svg viewBox="0 0 520 200" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="gd" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc)"/>
    </marker>
    <marker id="gdr" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc2,#e07)"/>
    </marker>
  </defs>
  <!-- Axes -->
  <line x1="30" y1="170" x2="490" y2="170" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <line x1="30" y1="20"  x2="30"  y2="175" stroke="var(--acc-bd)" stroke-width="1.2"/>
  <text x="495" y="174" font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)">W</text>
  <text x="34"  y="18"  font-size="10" font-family="Space Grotesk" fill="var(--acc-tx)">Loss</text>

  <!-- Loss curve (bowl shape) -->
  <path d="M40,155 C80,140 120,100 160,70 C200,45 220,35 270,32 C310,30 330,34 360,50 C390,68 420,100 460,140 L480,160"
        fill="none" stroke="var(--acc-bd)" stroke-width="2.5"/>

  <!-- Optimal point marker -->
  <circle cx="270" cy="32" r="5" fill="var(--acc)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="275" y="26" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Minimum</text>

  <!-- Good descent steps (left side approaching minimum) -->
  <circle cx="100" cy="108" r="5" fill="var(--acc)" opacity="0.7"/>
  <circle cx="155" cy="74"  r="5" fill="var(--acc)" opacity="0.75"/>
  <circle cx="205" cy="50"  r="5" fill="var(--acc)" opacity="0.8"/>
  <circle cx="245" cy="36"  r="5" fill="var(--acc)" opacity="0.9"/>
  <line x1="100" y1="108" x2="149" y2="78"  stroke="var(--acc)" stroke-width="1.5" marker-end="url(#gd)"/>
  <line x1="155" y1="74"  x2="199" y2="54"  stroke="var(--acc)" stroke-width="1.5" marker-end="url(#gd)"/>
  <line x1="205" y1="50"  x2="239" y2="38"  stroke="var(--acc)" stroke-width="1.5" marker-end="url(#gd)"/>
  <text x="75" y="103" font-size="8" font-family="Space Grotesk" fill="var(--acc-tx)">Start</text>

  <!-- Too-large learning rate: overshoot -->
  <circle cx="380" cy="52" r="5" fill="var(--acc2,#e07)" opacity="0.8"/>
  <circle cx="150" cy="74" r="5" fill="var(--acc2,#e07)" opacity="0.8"/>
  <line x1="380" y1="52" x2="156" y2="73" stroke="var(--acc2,#e07)" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#gdr)"/>
  <text x="340" y="45" font-size="8" font-family="Space Grotesk" fill="var(--acc2,#e07)">α too large</text>
  <text x="330" y="56" font-size="8" font-family="Space Grotesk" fill="var(--acc2,#e07)">→ overshoot</text>

  <!-- Update rule -->
  <rect x="30" y="180" width="460" height="16" rx="0" fill="none"/>
  <text x="260" y="192" text-anchor="middle" font-size="10" font-family="JetBrains Mono" fill="var(--acc-tx)">θ_{t+1} = θ_t − α · ∇L(θ_t)</text>
</svg>
<div class="frow" style="flex-wrap:wrap;gap:8px;margin-top:4px">
  <span class="chip">α too large → diverge / oscillate</span>
  <span class="chip">α too small → very slow</span>
  <span class="chip">Adam → adaptive α per param</span>
</div>
<div class="fignote">Each step moves weights opposite to the gradient direction, scaled by learning rate α.</div></div>
"""

# ---- Adam Optimizer ----
D["713ffd7ac0b5"] = r"""
<div class="fig"><div class="figcap">Adam Optimizer · Adaptive Moment Estimation</div>
<div class="fcol" style="gap:6px">
  <div class="frow sb" style="flex-wrap:nowrap;gap:6px">
    <div class="node soft" style="flex:1"><div class="nt">1st Moment m̂</div><div class="ns">bias-corrected mean of gradients · momentum</div></div>
    <span class="ar">+</span>
    <div class="node soft" style="flex:1"><div class="nt">2nd Moment v̂</div><div class="ns">bias-corrected mean of grad² · adaptive scale</div></div>
  </div>
  <div class="ar-d">↓ combined update ↓</div>
  <div class="node acc"><div class="nt">W = W − lr · m̂ / (√v̂ + ε)</div><div class="ns">each parameter gets its own effective learning rate</div></div>
</div>
<div class="callout c-key" style="margin-top:10px">
  <div class="ch">◆ Key equations</div>
  <p style="font-family:'JetBrains Mono',monospace;font-size:11px;line-height:1.8">
    m_t = β₁·m_{t-1} + (1−β₁)·g_t<br>
    v_t = β₂·v_{t-1} + (1−β₂)·g_t²<br>
    m̂ = m_t / (1−β₁ᵗ) &nbsp; v̂ = v_t / (1−β₂ᵗ)<br>
    W  = W − α · m̂ / (√v̂ + ε)
  </p>
</div>
<div class="fignote">Default: β₁=0.9, β₂=0.999, ε=1e-8. Bias-correction prevents large steps at initialisation.</div></div>
"""

# ---- GAN: Generator vs Discriminator ----
D["7e07390aea9a"] = r"""
<div class="fig"><div class="figcap">Generative Adversarial Network · Minimax Game</div>
<svg viewBox="0 0 520 160" style="display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <marker id="ga" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc)"/>
    </marker>
    <marker id="ga2" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto">
      <path d="M0,0 L0,6 L7,3 Z" fill="var(--acc2,#e07)"/>
    </marker>
  </defs>
  <!-- Noise z -->
  <rect x="8" y="55" width="60" height="50" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="38" y="75"  text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Noise z</text>
  <text x="38" y="90"  text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">latent</text>
  <text x="38" y="102" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">vector</text>

  <!-- Generator G -->
  <rect x="96" y="50" width="90" height="60" rx="6" fill="var(--acc)" opacity="0.7" stroke="var(--acc)" stroke-width="2"/>
  <text x="141" y="73"  text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="#fff" font-weight="700">Generator</text>
  <text x="141" y="88"  text-anchor="middle" font-size="8"  font-family="JetBrains Mono" fill="#fff">G(z)</text>
  <text x="141" y="103" text-anchor="middle" font-size="8"  font-family="JetBrains Mono" fill="#fff">fool D</text>
  <line x1="68" y1="80" x2="94" y2="80" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ga)"/>

  <!-- Fake sample -->
  <rect x="206" y="60" width="68" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="240" y="77" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">G(z)</text>
  <text x="240" y="91" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">fake sample</text>
  <line x1="186" y1="80" x2="204" y2="80" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ga)"/>

  <!-- Real data -->
  <rect x="206" y="10" width="68" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="240" y="27" text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Real x</text>
  <text x="240" y="41" text-anchor="middle" font-size="8" font-family="JetBrains Mono" fill="var(--acc-tx)">true data</text>

  <!-- Discriminator D -->
  <rect x="300" y="30" width="90" height="70" rx="6" fill="var(--acc2,#e07)" opacity="0.65" stroke="var(--acc2,#e07)" stroke-width="2"/>
  <text x="345" y="57"  text-anchor="middle" font-size="10" font-family="Space Grotesk" fill="#fff" font-weight="700">Discriminator</text>
  <text x="345" y="71"  text-anchor="middle" font-size="8"  font-family="JetBrains Mono" fill="#fff">D(x)</text>
  <text x="345" y="85"  text-anchor="middle" font-size="8"  font-family="JetBrains Mono" fill="#fff">P(real)</text>
  <line x1="274" y1="30" x2="298" y2="50" stroke="var(--acc2,#e07)" stroke-width="1.5" marker-end="url(#ga2)"/>
  <line x1="274" y1="80" x2="298" y2="70" stroke="var(--acc2,#e07)" stroke-width="1.5" marker-end="url(#ga2)"/>

  <!-- Output -->
  <rect x="416" y="45" width="90" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="461" y="62"  text-anchor="middle" font-size="9" font-family="Space Grotesk" fill="var(--acc-tx)" font-weight="600">Real / Fake?</text>
  <text x="461" y="78"  text-anchor="middle" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">∈ [0, 1]</text>
  <line x1="390" y1="65" x2="414" y2="65" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#ga)"/>

  <!-- Loss labels -->
  <text x="8"   y="148" font-size="8" font-family="Space Grotesk" fill="var(--acc-tx)">G: max log D(G(z))</text>
  <text x="190" y="148" font-size="8" font-family="Space Grotesk" fill="var(--acc2,#e07)">D: max log D(x) + log(1−D(G(z)))</text>
</svg>
<div class="fignote">Minimax: min_G max_D V = E[log D(x)] + E[log(1−D(G(z)))] — equilibrium when G fools D 50% of the time.</div></div>
"""

# ---- Autoencoder ----
D["724b2081f8d8"] = r"""
<div class="fig"><div class="figcap">Autoencoder · Compress and Reconstruct</div>
<div class="frow" style="flex-wrap:nowrap;gap:0">
  <div class="node soft" style="flex:1"><div class="nt">Input x</div><div class="ns">original data</div></div>
  <span class="ar">→</span>
  <div class="node acc" style="flex:1.2"><div class="nt">Encoder</div><div class="ns">learns compressed rep.</div></div>
  <span class="ar">→</span>
  <div class="node" style="border:2px solid var(--acc);flex:0.7"><div class="nt">Latent z</div><div class="ns">bottleneck</div></div>
  <span class="ar">→</span>
  <div class="node acc" style="flex:1.2"><div class="nt">Decoder</div><div class="ns">reconstructs from z</div></div>
  <span class="ar">→</span>
  <div class="node soft" style="flex:1"><div class="nt">Output x̂</div><div class="ns">reconstruction</div></div>
</div>
<div class="callout c-take" style="margin-top:10px">
  <div class="ch">◆ Loss</div>
  <p style="font-family:'JetBrains Mono',monospace;font-size:12px">Loss = ‖x − x̂‖²   (reconstruction error)</p>
</div>
<div class="frow" style="flex-wrap:wrap;gap:8px;margin-top:8px">
  <span class="chip">Dimensionality reduction</span>
  <span class="chip">Anomaly detection</span>
  <span class="chip">Generative (VAE variant)</span>
</div>
<div class="fignote">The bottleneck forces the network to learn a compact, meaningful representation — information must flow through a narrow channel.</div></div>
"""

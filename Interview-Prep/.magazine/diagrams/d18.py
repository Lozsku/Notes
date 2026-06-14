# Hand-built HTML diagrams for 01-ml-fundamentals.md  (key = md5(ascii)[:12])
D = {}

# ---- Bias-Variance Tradeoff Curve ----
D["9ceb079eeb19"] = r"""
<div class="fig"><div class="figcap">Bias–Variance Tradeoff · U-curve</div>
<svg viewBox="0 0 520 210" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="11">
  <!-- axes -->
  <line x1="50" y1="170" x2="480" y2="170" stroke="var(--acc-d)" stroke-width="1.5"/>
  <line x1="50" y1="20"  x2="50"  y2="170" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="260" y="195" text-anchor="middle" fill="var(--acc-tx)" font-size="12">Model Complexity →</text>
  <text x="16" y="100" text-anchor="middle" fill="var(--acc-tx)" font-size="12" transform="rotate(-90,16,100)">Error</text>
  <!-- Bias² line: high left, falls to right -->
  <polyline points="60,30 120,50 180,75 240,100 300,120 360,135 420,145 470,150"
    fill="none" stroke="var(--acc2)" stroke-width="2.2" stroke-dasharray="6,3"/>
  <!-- Variance line: low left, rises to right -->
  <polyline points="60,155 120,150 180,142 240,130 300,110 360,85 420,55 470,28"
    fill="none" stroke="var(--acc)" stroke-width="2.2" stroke-dasharray="3,3"/>
  <!-- Total error U-curve -->
  <polyline points="60,90 120,88 180,85 240,88 300,95 360,102 420,108 470,115"
    fill="none" stroke="var(--acc-bd,var(--acc))" stroke-width="2.8" opacity="0.85"/>
  <!-- sweet spot marker -->
  <line x1="230" y1="20" x2="230" y2="170" stroke="var(--acc)" stroke-width="1" stroke-dasharray="4,3" opacity="0.6"/>
  <circle cx="230" cy="87" r="5" fill="var(--acc)" opacity="0.9"/>
  <text x="238" y="75" fill="var(--acc)" font-size="10" font-weight="600">Sweet Spot</text>
  <!-- labels -->
  <text x="65" y="45" fill="var(--acc-tx)" font-size="9" opacity="0.8">Bias²</text>
  <text x="420" y="45" fill="var(--acc-tx)" font-size="9" opacity="0.8">Variance</text>
  <text x="300" y="88" fill="var(--acc-tx)" font-size="9.5" font-weight="600">Total Error</text>
  <!-- axis labels -->
  <text x="70"  y="183" fill="var(--acc-tx)" font-size="9" opacity="0.7">Simple</text>
  <text x="410" y="183" fill="var(--acc-tx)" font-size="9" opacity="0.7">Complex</text>
  <text x="70"  y="192" fill="var(--acc-tx)" font-size="8" opacity="0.6">High Bias · Underfit</text>
  <text x="385" y="192" fill="var(--acc-tx)" font-size="8" opacity="0.6">High Variance · Overfit</text>
</svg>
<div class="fignote">Total Error = Bias² + Variance + Noise. Optimal complexity minimises the sum — neither too simple nor too complex.</div></div>
"""

# ---- ML Workflow Pipeline ----
D["e4bef97a2caa"] = r"""
<div class="fig"><div class="figcap">ML Workflow Pipeline · end-to-end</div>
<div class="tiers">
  <div class="tier">
    <div class="th">COLLECT</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Raw Data</div><div class="ns">CSV · DB · API · streams</div></div>
    </div>
  </div>
  <span class="ar">→</span>
  <div class="tier">
    <div class="th">PREPARE</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">EDA &amp; Cleaning</div><div class="ns">nulls · outliers · types</div></div>
      <div class="ar-d" style="font-size:10px">↓</div>
      <div class="node soft"><div class="nt">Feature Eng.</div><div class="ns">encode · scale · interactions</div></div>
    </div>
  </div>
  <span class="ar">→</span>
  <div class="tier">
    <div class="th">MODEL</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Train / CV</div><div class="ns">fit on train data only</div></div>
      <div class="ar-d" style="font-size:10px">↓</div>
      <div class="node soft"><div class="nt">HP Tuning</div><div class="ns">Grid · Random · Bayes · val set</div></div>
      <div class="ar-d" style="font-size:10px">↓</div>
      <div class="node"><div class="nt">Evaluate</div><div class="ns">test set · once only</div></div>
    </div>
  </div>
  <span class="ar">→</span>
  <div class="tier">
    <div class="th">DEPLOY</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Export</div><div class="ns">pickle · ONNX · TF SavedModel</div></div>
      <div class="ar-d" style="font-size:10px">↓</div>
      <div class="node soft"><div class="nt">Serve</div><div class="ns">REST API · batch · stream</div></div>
      <div class="ar-d" style="font-size:10px">↓</div>
      <div class="node acc"><div class="nt">Monitor</div><div class="ns">data drift · perf · retrain triggers</div></div>
    </div>
  </div>
</div>
<div class="fignote">Decisions made in Prepare &amp; Model phases feed back into the loop — retrain when production performance degrades.</div></div>
"""

# ---- Train / Validation / Test Split ----
D["b6176086f68c"] = r"""
<div class="fig"><div class="figcap">Train / Validation / Test Split</div>
<div class="gantt" style="margin-bottom:8px">
  <div class="gr">
    <span class="gl">All Data</span>
    <div class="track">
      <div class="gseg a" style="width:70%">TRAINING &nbsp;~70%</div>
      <div class="gseg b" style="width:15%">VAL ~15%</div>
      <div class="gseg m" style="width:15%">TEST ~15%</div>
    </div>
  </div>
</div>
<div class="frow sb" style="font-size:11px;margin-top:4px;padding:0 8px">
  <div class="fcol" style="align-items:flex-start">
    <span class="chip">Training</span>
    <span style="font-size:10px;opacity:0.8;margin-top:2px">Model learns parameters (weights)</span>
    <span style="font-size:10px;opacity:0.7">CV loops happen within this partition</span>
  </div>
  <div class="fcol" style="align-items:center">
    <span class="chip">Validation</span>
    <span style="font-size:10px;opacity:0.8;margin-top:2px">Tune hyperparameters</span>
    <span style="font-size:10px;opacity:0.7">Model selection · early stopping</span>
  </div>
  <div class="fcol" style="align-items:flex-end">
    <span class="chip">Test</span>
    <span style="font-size:10px;opacity:0.8;margin-top:2px">Touch EXACTLY ONCE</span>
    <span style="font-size:10px;opacity:0.7">Final unbiased estimate</span>
  </div>
</div>
<div class="fignote">Validation may be used repeatedly; the test set is locked until all modelling decisions are finalised — peeking leaks information.</div></div>
"""

# ---- 5-Fold Cross Validation ----
D["e3db5cea7036"] = r"""
<div class="fig"><div class="figcap">5-Fold Cross-Validation</div>
<div class="gantt">
  <div class="gr">
    <span class="gl" style="min-width:52px">Fold 1</span>
    <div class="track">
      <div class="gseg b" style="width:20%">VAL</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
    </div>
  </div>
  <div class="gr">
    <span class="gl" style="min-width:52px">Fold 2</span>
    <div class="track">
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg b" style="width:20%">VAL</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
    </div>
  </div>
  <div class="gr">
    <span class="gl" style="min-width:52px">Fold 3</span>
    <div class="track">
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg b" style="width:20%">VAL</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
    </div>
  </div>
  <div class="gr">
    <span class="gl" style="min-width:52px">Fold 4</span>
    <div class="track">
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg b" style="width:20%">VAL</div>
      <div class="gseg a" style="width:20%">TRN</div>
    </div>
  </div>
  <div class="gr">
    <span class="gl" style="min-width:52px">Fold 5</span>
    <div class="track">
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg a" style="width:20%">TRN</div>
      <div class="gseg b" style="width:20%">VAL</div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px"><span class="chip">Final CV Score = mean(score₁…₅) ± std(score₁…₅)</span></div>
<div class="fignote">Each data point appears exactly once in a validation fold — gives a low-variance estimate of generalisation performance without a held-out validation set.</div></div>
"""

# ---- Confusion Matrix (Fraud example) ----
D["b9f782003050"] = r"""
<div class="fig"><div class="figcap">Confusion Matrix · Fraud Detection Example</div>
<div class="matrix" style="grid-template-columns:repeat(3,1fr);max-width:400px;margin:0 auto">
  <div class="cell hd"></div>
  <div class="cell hd">Predicted FRAUD</div>
  <div class="cell hd">Predicted LEGIT</div>
  <div class="cell hd">Actual FRAUD</div>
  <div class="cell on" style="font-size:13px;font-weight:700">TP: 90</div>
  <div class="cell" style="font-size:13px">FN: 10</div>
  <div class="cell hd">Actual LEGIT</div>
  <div class="cell" style="font-size:13px">FP: 50</div>
  <div class="cell on" style="font-size:13px;font-weight:700">TN: 9850</div>
</div>
<div class="frow sb" style="margin-top:10px;flex-wrap:wrap;gap:6px;font-size:11px">
  <span class="chip">Accuracy = 99.4% ← misleading!</span>
  <span class="chip">Precision = 64.3%</span>
  <span class="chip">Recall = 90.0%</span>
  <span class="chip">F1 = 75.0%</span>
</div>
<div class="fignote">High accuracy on imbalanced data is deceiving — Precision, Recall and F1 reveal the real picture. FN = missed fraud (Type II); FP = false alarm (Type I).</div></div>
"""

# ---- Gradient Descent on Loss Bowl ----
D["5e07651c1a63"] = r"""
<div class="fig"><div class="figcap">Gradient Descent · loss surface</div>
<svg viewBox="0 0 520 220" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="11">
  <!-- bowl shape -->
  <path d="M60,30 Q260,220 460,30" fill="none" stroke="var(--acc)" stroke-width="2.5"/>
  <!-- gradient steps down the bowl -->
  <circle cx="120" cy="95"  r="7" fill="var(--acc)" opacity="0.9"/>
  <line x1="120" y1="95" x2="155" y2="127" stroke="var(--acc2)" stroke-width="1.8" marker-end="url(#arr)"/>
  <circle cx="160" cy="130" r="7" fill="var(--acc)" opacity="0.85"/>
  <line x1="160" y1="130" x2="193" y2="153" stroke="var(--acc2)" stroke-width="1.8" marker-end="url(#arr)"/>
  <circle cx="197" cy="156" r="7" fill="var(--acc)" opacity="0.8"/>
  <line x1="197" y1="156" x2="225" y2="168" stroke="var(--acc2)" stroke-width="1.8" marker-end="url(#arr)"/>
  <circle cx="228" cy="170" r="7" fill="var(--acc)" opacity="0.75"/>
  <line x1="228" y1="170" x2="250" y2="175" stroke="var(--acc2)" stroke-width="1.8" marker-end="url(#arr)"/>
  <circle cx="253" cy="176" r="8" fill="var(--acc2)" opacity="1"/>
  <text x="263" y="180" fill="var(--acc-tx)" font-size="10" font-weight="600">minimum</text>
  <!-- start label -->
  <text x="80" y="88" fill="var(--acc-tx)" font-size="10">start</text>
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc2)"/>
    </marker>
  </defs>
  <!-- axis labels -->
  <text x="50"  y="200" fill="var(--acc-tx)" font-size="10" opacity="0.7">w₁</text>
  <text x="460" y="200" fill="var(--acc-tx)" font-size="10" opacity="0.7">w₁</text>
  <text x="260" y="212" text-anchor="middle" fill="var(--acc-tx)" font-size="10" opacity="0.7">parameter space →</text>
  <!-- learning rate comparison -->
  <rect x="10" y="10" width="120" height="48" rx="6" fill="var(--acc-bg)" stroke="var(--acc-d)" stroke-width="1" opacity="0.85"/>
  <text x="70" y="24" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="600">Learning Rate</text>
  <text x="70" y="36" text-anchor="middle" fill="var(--acc-tx)" font-size="8.5">Too high → diverge</text>
  <text x="70" y="47" text-anchor="middle" fill="var(--acc-tx)" font-size="8.5">Too low → very slow</text>
  <!-- update rule -->
  <rect x="340" y="10" width="170" height="28" rx="6" fill="var(--acc-bg)" stroke="var(--acc-d)" stroke-width="1" opacity="0.85"/>
  <text x="425" y="28" text-anchor="middle" fill="var(--acc-tx)" font-size="10" font-family="'JetBrains Mono',monospace">θ ← θ − α∇L(θ)</text>
</svg>
<div class="fignote">Each step moves opposite to the gradient (steepest ascent). Adam adapts the learning rate per-parameter — avoids oscillation on ravine-shaped surfaces.</div></div>
"""

# ---- Over/Under/Good Fit Curves ----
D["acaa173442c4"] = r"""
<div class="fig"><div class="figcap">Underfitting · Good Fit · Overfitting</div>
<svg viewBox="0 0 520 190" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="10">
  <!-- === UNDERFIT panel === -->
  <text x="85" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="11">UNDERFIT</text>
  <text x="85" y="26" text-anchor="middle" fill="var(--acc-tx)" font-size="9" opacity="0.75">High Bias</text>
  <!-- axes -->
  <line x1="16" y1="155" x2="158" y2="155" stroke="var(--acc-d)" stroke-width="1"/>
  <line x1="16" y1="40"  x2="16"  y2="155" stroke="var(--acc-d)" stroke-width="1"/>
  <!-- data points scattered -->
  <circle cx="35"  cy="130" r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="55"  cy="100" r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="75"  cy="75"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="95"  cy="90"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="115" cy="60"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="135" cy="50"  r="3" fill="var(--acc)" opacity="0.7"/>
  <!-- flat line - too simple -->
  <line x1="20" y1="100" x2="155" y2="100" stroke="var(--acc2)" stroke-width="2.2"/>
  <!-- error labels -->
  <text x="85" y="170" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Train err: HIGH</text>
  <text x="85" y="181" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Val err: HIGH</text>

  <!-- === GOOD FIT panel === -->
  <text x="260" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="11">GOOD FIT</text>
  <text x="260" y="26" text-anchor="middle" fill="var(--acc-tx)" font-size="9" opacity="0.75">Optimal Complexity</text>
  <!-- axes -->
  <line x1="191" y1="155" x2="333" y2="155" stroke="var(--acc-d)" stroke-width="1"/>
  <line x1="191" y1="40"  x2="191" y2="155" stroke="var(--acc-d)" stroke-width="1"/>
  <!-- data points -->
  <circle cx="210" cy="130" r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="230" cy="100" r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="250" cy="72"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="270" cy="85"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="290" cy="58"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="310" cy="48"  r="3" fill="var(--acc)" opacity="0.7"/>
  <!-- smooth curve -->
  <path d="M195,135 Q230,100 250,72 Q275,50 328,46" fill="none" stroke="var(--acc2)" stroke-width="2.2"/>
  <text x="260" y="170" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Train err: LOW</text>
  <text x="260" y="181" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Val err: LOW</text>

  <!-- === OVERFIT panel === -->
  <text x="440" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="11">OVERFIT</text>
  <text x="440" y="26" text-anchor="middle" fill="var(--acc-tx)" font-size="9" opacity="0.75">High Variance</text>
  <!-- axes -->
  <line x1="366" y1="155" x2="508" y2="155" stroke="var(--acc-d)" stroke-width="1"/>
  <line x1="366" y1="40"  x2="366" y2="155" stroke="var(--acc-d)" stroke-width="1"/>
  <!-- data points -->
  <circle cx="385" cy="130" r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="405" cy="100" r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="425" cy="72"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="445" cy="85"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="465" cy="58"  r="3" fill="var(--acc)" opacity="0.7"/>
  <circle cx="485" cy="48"  r="3" fill="var(--acc)" opacity="0.7"/>
  <!-- wiggly overfit curve passing through every point -->
  <path d="M370,135 L385,130 Q395,70 405,100 Q415,130 425,72 Q435,45 445,85 Q455,120 465,58 Q475,20 485,48 L500,42"
    fill="none" stroke="var(--acc2)" stroke-width="2.2"/>
  <text x="440" y="170" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Train err: VERY LOW</text>
  <text x="440" y="181" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Val err: HIGH</text>
</svg>
<div class="fignote">Underfit = too simple, misses structure. Overfit = memorises noise. Diagnose via the train/validation error gap.</div></div>
"""

# ---- ROC Curve & PR Curve ----
D["02a55e0704ad"] = r"""
<div class="fig"><div class="figcap">ROC Curve &amp; PR Curve · classifier evaluation</div>
<svg viewBox="0 0 520 200" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="11">
  <!-- ROC panel -->
  <text x="130" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">ROC Curve</text>
  <!-- axes -->
  <line x1="40" y1="170" x2="220" y2="170" stroke="var(--acc-d)" stroke-width="1.5"/>
  <line x1="40" y1="20"  x2="40"  y2="170" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="130" y="188" text-anchor="middle" fill="var(--acc-tx)" font-size="9.5">FPR (1 – Specificity)</text>
  <text x="15" y="100" text-anchor="middle" fill="var(--acc-tx)" font-size="9.5" transform="rotate(-90,15,100)">TPR (Recall)</text>
  <!-- diagonal random classifier -->
  <line x1="40" y1="170" x2="220" y2="20" stroke="var(--acc-d)" stroke-width="1" stroke-dasharray="4,3" opacity="0.5"/>
  <text x="145" y="115" fill="var(--acc-tx)" font-size="8" opacity="0.6" transform="rotate(-40,145,115)">random</text>
  <!-- good ROC curve (concave up-left) -->
  <path d="M40,170 Q50,60 100,40 Q150,25 220,20" fill="none" stroke="var(--acc)" stroke-width="2.5"/>
  <!-- AUC fill -->
  <path d="M40,170 Q50,60 100,40 Q150,25 220,20 L220,170 Z" fill="var(--acc)" opacity="0.1"/>
  <text x="85" y="90" fill="var(--acc)" font-size="10" font-weight="600">AUC ≈ 0.92</text>
  <!-- axis ticks -->
  <text x="36" y="173" text-anchor="end" fill="var(--acc-tx)" font-size="8">0</text>
  <text x="220" y="173" text-anchor="middle" fill="var(--acc-tx)" font-size="8">1</text>
  <text x="36" y="22" text-anchor="end" fill="var(--acc-tx)" font-size="8">1</text>

  <!-- divider -->
  <line x1="270" y1="10" x2="270" y2="185" stroke="var(--acc-d)" stroke-width="0.8" stroke-dasharray="3,3" opacity="0.4"/>

  <!-- PR panel -->
  <text x="400" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="12">PR Curve</text>
  <!-- axes -->
  <line x1="290" y1="170" x2="500" y2="170" stroke="var(--acc-d)" stroke-width="1.5"/>
  <line x1="290" y1="20"  x2="290" y2="170" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="395" y="188" text-anchor="middle" fill="var(--acc-tx)" font-size="9.5">Recall</text>
  <text x="265" y="100" text-anchor="middle" fill="var(--acc-tx)" font-size="9.5" transform="rotate(-90,265,100)">Precision</text>
  <!-- PR curve: starts high precision, drops as recall increases -->
  <path d="M290,22 Q310,24 350,40 Q400,70 450,130 Q475,155 500,168" fill="none" stroke="var(--acc2)" stroke-width="2.5"/>
  <path d="M290,22 Q310,24 350,40 Q400,70 450,130 Q475,155 500,168 L500,170 L290,170 Z" fill="var(--acc2)" opacity="0.08"/>
  <text x="355" y="85" fill="var(--acc2)" font-size="10" font-weight="600">AP (area)</text>
  <!-- ticks -->
  <text x="286" y="173" text-anchor="end" fill="var(--acc-tx)" font-size="8">0</text>
  <text x="500" y="173" text-anchor="middle" fill="var(--acc-tx)" font-size="8">1</text>
  <text x="286" y="22" text-anchor="end" fill="var(--acc-tx)" font-size="8">1</text>
</svg>
<div class="frow" style="margin-top:6px;gap:8px">
  <span class="chip">ROC AUC — good for balanced classes</span>
  <span class="chip">PR AUC (AP) — better for imbalanced classes</span>
</div>
<div class="fignote">Higher AUC = better. ROC is threshold-invariant; PR curve highlights performance on the minority (positive) class.</div></div>
"""

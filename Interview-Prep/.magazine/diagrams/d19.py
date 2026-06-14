# Hand-built HTML diagrams for 02-classic-ml-algorithms.md  (key = md5(ascii)[:12])
D = {}

# ---- Decision Tree (diagram #60) ----
D["a7f058d1255a"] = r'''
<div class="fig"><div class="figcap">Decision Tree · Credit Approval Example</div>
<svg viewBox="0 0 520 260" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="9">
  <!-- Root node -->
  <rect x="185" y="10" width="150" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="260" y="24" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Age &lt; 30?</text>
  <text x="260" y="38" text-anchor="middle" fill="var(--acc-tx)" font-size="8">Root node</text>

  <!-- YES branch left -->
  <line x1="220" y1="44" x2="120" y2="90" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="155" y="75" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">YES</text>

  <!-- NO branch right -->
  <line x1="300" y1="44" x2="400" y2="90" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="365" y="75" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">NO</text>

  <!-- Left internal: Income > 50k? -->
  <rect x="45" y="90" width="150" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="120" y="104" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Income &gt; 50k?</text>
  <text x="120" y="118" text-anchor="middle" fill="var(--acc-tx)" font-size="8">Internal node</text>

  <!-- Right internal: Own Home? -->
  <rect x="325" y="90" width="150" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="400" y="104" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Own Home?</text>
  <text x="400" y="118" text-anchor="middle" fill="var(--acc-tx)" font-size="8">Internal node</text>

  <!-- Income YES → Approve -->
  <line x1="90" y1="124" x2="50" y2="170" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="58" y="158" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">YES</text>
  <rect x="10" y="170" width="80" height="28" rx="6" fill="var(--acc)" stroke="none"/>
  <text x="50" y="188" text-anchor="middle" fill="var(--acc-bg)" font-weight="700" font-size="9">Approve</text>

  <!-- Income NO → Deny -->
  <line x1="150" y1="124" x2="185" y2="170" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="177" y="158" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">NO</text>
  <rect x="150" y="170" width="70" height="28" rx="6" fill="var(--acc2,#e66)" stroke="none"/>
  <text x="185" y="188" text-anchor="middle" fill="var(--acc-bg)" font-weight="700" font-size="9">Deny</text>

  <!-- Own Home YES → Approve -->
  <line x1="370" y1="124" x2="320" y2="170" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="336" y="158" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">YES</text>
  <rect x="285" y="170" width="70" height="28" rx="6" fill="var(--acc)" stroke="none"/>
  <text x="320" y="188" text-anchor="middle" fill="var(--acc-bg)" font-weight="700" font-size="9">Approve</text>

  <!-- Own Home NO → Credit? -->
  <line x1="430" y1="124" x2="430" y2="170" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="443" y="155" text-anchor="start" fill="var(--acc-tx)" font-size="8" font-style="italic">NO</text>
  <rect x="370" y="170" width="120" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="430" y="184" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Credit Score?</text>
  <text x="430" y="198" text-anchor="middle" fill="var(--acc-tx)" font-size="8">Internal node</text>

  <!-- Credit YES/NO -->
  <line x1="400" y1="204" x2="370" y2="232" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="374" y="224" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">YES</text>
  <rect x="330" y="232" width="70" height="22" rx="6" fill="var(--acc)" stroke="none"/>
  <text x="365" y="247" text-anchor="middle" fill="var(--acc-bg)" font-weight="700" font-size="9">Approve</text>

  <line x1="460" y1="204" x2="490" y2="232" stroke="var(--acc)" stroke-width="1.2"/>
  <text x="485" y="224" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-style="italic">NO</text>
  <rect x="460" y="232" width="55" height="22" rx="6" fill="var(--acc2,#e66)" stroke="none"/>
  <text x="487" y="247" text-anchor="middle" fill="var(--acc-bg)" font-weight="700" font-size="9">Deny</text>
</svg>
<div class="fignote">Split criterion: minimize Gini/Entropy at each node. Pruning removes nodes that don't significantly reduce impurity.</div></div>
'''

# ---- SVM Max-Margin Boundary (diagram #61) ----
D["dc578bbb747e"] = r'''
<div class="fig"><div class="figcap">SVM · Maximum-Margin Decision Boundary</div>
<svg viewBox="0 0 520 230" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="9">
  <!-- Axis labels -->
  <text x="10" y="220" fill="var(--acc-tx)" font-size="9">Feature 1 (x1)</text>
  <text x="10" y="20" fill="var(--acc-tx)" font-size="9">Feature 2 (x2)</text>

  <!-- Margin lines: decision boundary and +1/-1 planes -->
  <!-- Decision boundary (center): roughly diagonal -->
  <line x1="180" y1="20" x2="370" y2="210" stroke="var(--acc)" stroke-width="2" stroke-dasharray="none"/>
  <text x="375" y="205" fill="var(--acc-tx)" font-size="8">w·x+b=0</text>

  <!-- +1 margin plane (left of boundary) -->
  <line x1="130" y1="20" x2="320" y2="210" stroke="var(--acc)" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="116" y="18" fill="var(--acc-tx)" font-size="8">w·x+b=+1</text>

  <!-- -1 margin plane (right of boundary) -->
  <line x1="230" y1="20" x2="420" y2="210" stroke="var(--acc)" stroke-width="1" stroke-dasharray="5,3"/>
  <text x="421" y="18" fill="var(--acc-tx)" font-size="8">w·x+b=−1</text>

  <!-- Margin arrow -->
  <line x1="155" y1="115" x2="225" y2="115" stroke="var(--acc)" stroke-width="1" marker-end="url(#arr)" marker-start="url(#arr2)"/>
  <text x="185" y="109" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">margin = 2/‖w‖</text>

  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc)"/>
    </marker>
    <marker id="arr2" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto-start-reverse">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc)"/>
    </marker>
  </defs>

  <!-- Class +1 (circles) — upper left of boundary -->
  <circle cx="90" cy="60" r="6" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <circle cx="120" cy="75" r="6" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <circle cx="75" cy="95" r="6" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <circle cx="100" cy="110" r="6" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <circle cx="60" cy="130" r="6" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <circle cx="85" cy="150" r="6" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <!-- Support vector +1 (on margin line, highlighted) -->
  <circle cx="150" cy="80" r="7" fill="none" stroke="var(--acc)" stroke-width="2.5"/>
  <circle cx="150" cy="80" r="2" fill="var(--acc)"/>
  <text x="160" y="76" fill="var(--acc-tx)" font-size="7.5">SV</text>
  <circle cx="130" cy="140" r="7" fill="none" stroke="var(--acc)" stroke-width="2.5"/>
  <circle cx="130" cy="140" r="2" fill="var(--acc)"/>
  <text x="140" y="137" fill="var(--acc-tx)" font-size="7.5">SV</text>

  <!-- Class -1 (filled dots) — lower right of boundary -->
  <circle cx="310" cy="60" r="5" fill="var(--acc-d,#666)" stroke="none"/>
  <circle cx="345" cy="80" r="5" fill="var(--acc-d,#666)" stroke="none"/>
  <circle cx="360" cy="110" r="5" fill="var(--acc-d,#666)" stroke="none"/>
  <circle cx="330" cy="130" r="5" fill="var(--acc-d,#666)" stroke="none"/>
  <circle cx="380" cy="145" r="5" fill="var(--acc-d,#666)" stroke="none"/>
  <circle cx="400" cy="70" r="5" fill="var(--acc-d,#666)" stroke="none"/>
  <!-- Support vector -1 -->
  <circle cx="280" cy="100" r="7" fill="none" stroke="var(--acc-d,#666)" stroke-width="2.5"/>
  <circle cx="280" cy="100" r="5" fill="var(--acc-d,#666)"/>
  <text x="267" y="96" fill="var(--acc-tx)" font-size="7.5" text-anchor="end">SV</text>
  <circle cx="300" cy="160" r="7" fill="none" stroke="var(--acc-d,#666)" stroke-width="2.5"/>
  <circle cx="300" cy="160" r="5" fill="var(--acc-d,#666)"/>
  <text x="287" y="157" fill="var(--acc-tx)" font-size="7.5" text-anchor="end">SV</text>

  <!-- Legend -->
  <circle cx="30" cy="195" r="5" fill="none" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="40" y="199" fill="var(--acc-tx)" font-size="8">Class +1</text>
  <circle cx="110" cy="195" r="5" fill="var(--acc-d,#666)"/>
  <text x="120" y="199" fill="var(--acc-tx)" font-size="8">Class −1</text>
  <circle cx="195" cy="195" r="5" fill="none" stroke="var(--acc)" stroke-width="2.5"/>
  <circle cx="195" cy="195" r="2" fill="var(--acc)"/>
  <text x="205" y="199" fill="var(--acc-tx)" font-size="8">Support Vector</text>
</svg>
<div class="fignote">Only the support vectors (points on the margin planes) define the hyperplane — all other points can be removed without changing the decision boundary.</div></div>
'''

# ---- k-Means Clusters (diagram #62) ----
D["f6f67d42a10f"] = r'''
<div class="fig"><div class="figcap">k-Means Clustering · Convergence (k=3)</div>
<svg viewBox="0 0 520 200" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="9">
  <defs>
    <!-- Centroid cross marker -->
    <marker id="cx" markerWidth="10" markerHeight="10" refX="5" refY="5">
      <line x1="2" y1="5" x2="8" y2="5" stroke="var(--acc-tx)" stroke-width="1.5"/>
      <line x1="5" y1="2" x2="5" y2="8" stroke="var(--acc-tx)" stroke-width="1.5"/>
    </marker>
  </defs>

  <!-- ── ITERATION 1 ── -->
  <text x="65" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Iteration 1</text>
  <text x="65" y="26" text-anchor="middle" fill="var(--acc-tx)" font-size="7.5">Random centroids</text>

  <!-- cluster 1 (star/asterisk) upper-left -->
  <text x="20" y="55" fill="var(--acc)" font-size="10">★</text>
  <text x="35" y="48" fill="var(--acc)" font-size="10">★</text>
  <text x="28" y="70" fill="var(--acc)" font-size="10">★</text>
  <text x="48" y="60" fill="var(--acc)" font-size="10">★</text>
  <text x="15" y="80" fill="var(--acc)" font-size="10">★</text>

  <!-- cluster 2 (×) upper-right -->
  <text x="90" y="45" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <text x="108" y="52" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <text x="95" y="65" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <text x="118" y="44" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>

  <!-- cluster 3 (■) bottom -->
  <text x="40" y="105" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="55" y="118" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="30" y="125" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="70" y="110" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="50" y="135" fill="var(--acc-d,#888)" font-size="9">■</text>

  <!-- Random centroids -->
  <text x="55" y="75" fill="var(--acc-tx)" font-size="13" font-weight="900">+</text>
  <text x="100" y="85" fill="var(--acc-tx)" font-size="13" font-weight="900">+</text>
  <text x="35" y="115" fill="var(--acc-tx)" font-size="13" font-weight="900">+</text>
  <text x="62" y="73" fill="var(--acc-tx)" font-size="6.5">c1?</text>
  <text x="107" y="83" fill="var(--acc-tx)" font-size="6.5">c2?</text>
  <text x="42" y="113" fill="var(--acc-tx)" font-size="6.5">c3?</text>

  <!-- Arrow between iterations -->
  <text x="155" y="90" text-anchor="middle" fill="var(--acc)" font-size="18">→</text>

  <!-- ── CONVERGED ── -->
  <text x="310" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Converged</text>
  <text x="310" y="26" text-anchor="middle" fill="var(--acc-tx)" font-size="7.5">Centroids = cluster means</text>

  <!-- cluster 1 (stars) tighter -->
  <text x="205" y="55" fill="var(--acc)" font-size="10">★</text>
  <text x="220" y="48" fill="var(--acc)" font-size="10">★</text>
  <text x="215" y="70" fill="var(--acc)" font-size="10">★</text>
  <text x="238" y="58" fill="var(--acc)" font-size="10">★</text>
  <text x="200" y="75" fill="var(--acc)" font-size="10">★</text>
  <!-- centroid 1 -->
  <circle cx="220" cy="63" r="7" fill="none" stroke="var(--acc)" stroke-width="2"/>
  <line x1="216" y1="63" x2="224" y2="63" stroke="var(--acc)" stroke-width="1.5"/>
  <line x1="220" y1="59" x2="220" y2="67" stroke="var(--acc)" stroke-width="1.5"/>

  <!-- cluster 2 (×) -->
  <text x="280" y="45" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <text x="300" y="52" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <text x="285" y="65" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <text x="312" y="44" fill="var(--acc2,#e8a020)" font-size="10" font-weight="700">×</text>
  <!-- centroid 2 -->
  <circle cx="297" cy="53" r="7" fill="none" stroke="var(--acc2,#e8a020)" stroke-width="2"/>
  <line x1="293" y1="53" x2="301" y2="53" stroke="var(--acc2,#e8a020)" stroke-width="1.5"/>
  <line x1="297" y1="49" x2="297" y2="57" stroke="var(--acc2,#e8a020)" stroke-width="1.5"/>

  <!-- cluster 3 (■) -->
  <text x="230" y="100" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="248" y="115" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="218" y="120" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="265" y="105" fill="var(--acc-d,#888)" font-size="9">■</text>
  <text x="245" y="130" fill="var(--acc-d,#888)" font-size="9">■</text>
  <!-- centroid 3 -->
  <circle cx="247" cy="113" r="7" fill="none" stroke="var(--acc-d,#888)" stroke-width="2"/>
  <line x1="243" y1="113" x2="251" y2="113" stroke="var(--acc-d,#888)" stroke-width="1.5"/>
  <line x1="247" y1="109" x2="247" y2="117" stroke="var(--acc-d,#888)" stroke-width="1.5"/>

  <!-- Formula box -->
  <rect x="360" y="40" width="148" height="120" rx="8" fill="var(--acc-bg)" stroke="var(--acc-bd,var(--acc))" stroke-width="1"/>
  <text x="434" y="58" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="9">Algorithm</text>
  <text x="375" y="76" fill="var(--acc-tx)" font-size="8">1. Assign each point</text>
  <text x="375" y="89" fill="var(--acc-tx)" font-size="8">   to nearest centroid</text>
  <text x="375" y="102" fill="var(--acc-tx)" font-size="8">2. Update centroids</text>
  <text x="375" y="115" fill="var(--acc-tx)" font-size="8">   = mean of cluster</text>
  <text x="375" y="128" fill="var(--acc-tx)" font-size="8">3. Repeat until</text>
  <text x="375" y="141" fill="var(--acc-tx)" font-size="8">   assignments stable</text>
  <text x="375" y="154" fill="var(--acc-tx)" font-size="8">Minimize WCSS: J=Σ‖xᵢ−μ‖²</text>

  <!-- Legend -->
  <text x="200" y="175" fill="var(--acc)" font-size="9">★ Cluster 1</text>
  <text x="275" y="175" fill="var(--acc2,#e8a020)" font-size="9">× Cluster 2</text>
  <text x="350" y="175" fill="var(--acc-d,#888)" font-size="9">■ Cluster 3</text>
  <text x="430" y="175" fill="var(--acc-tx)" font-size="9">⊕ Centroid</text>
</svg>
<div class="fignote">k-Means++ initialises centroids spread out (P ∝ distance²), drastically reducing bad initialisations.</div></div>
'''

# ---- Bagging vs Boosting side-by-side (diagram #63) ----
D["fdfca1b6880a"] = r'''
<div class="fig"><div class="figcap">Bagging vs Boosting · Ensemble Strategies</div>
<div class="tiers">
  <div class="tier">
    <div class="th">BAGGING (Random Forest)</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Training Data</div></div>
      <div class="ar-d">↓ bootstrap samples (parallel)</div>
      <div class="frow" style="flex-wrap:nowrap;gap:6px">
        <div class="fcol">
          <div class="node soft"><div class="nt">Bootstrap 1</div></div>
          <div class="ar-d">↓</div>
          <div class="node"><div class="nt">Tree 1</div></div>
        </div>
        <div class="fcol">
          <div class="node soft"><div class="nt">Bootstrap 2</div></div>
          <div class="ar-d">↓</div>
          <div class="node"><div class="nt">Tree 2</div></div>
        </div>
        <div class="fcol">
          <div class="node soft"><div class="nt">Bootstrap 3</div></div>
          <div class="ar-d">↓</div>
          <div class="node"><div class="nt">Tree 3</div></div>
        </div>
      </div>
      <div class="ar-d">↓ all combine</div>
      <div class="node acc"><div class="nt">Average / Majority Vote</div><div class="ns">↓ reduce variance</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">BOOSTING (XGBoost / AdaBoost)</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Training Data</div></div>
      <div class="ar-d">↓ fit first learner</div>
      <div class="node"><div class="nt">Tree 1</div><div class="ns">fit full data</div></div>
      <div class="ar-d">↓ residuals / re-weighted errors</div>
      <div class="node"><div class="nt">Tree 2</div><div class="ns">corrects Tree 1 errors</div></div>
      <div class="ar-d">↓ remaining residuals</div>
      <div class="node"><div class="nt">Tree 3</div><div class="ns">corrects Tree 1+2 errors</div></div>
      <div class="ar-d">↓ weighted sum</div>
      <div class="node acc"><div class="nt">lr·T₁ + lr·T₂ + lr·T₃ + …</div><div class="ns">↓ reduce bias</div></div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:10px;gap:10px">
  <span class="chip">Bagging: parallel · bootstrap · ↓ variance</span>
  <span class="chip">Boosting: sequential · full data · ↓ bias</span>
</div>
<div class="fignote">Bagging reduces variance by averaging uncorrelated models; Boosting reduces bias by sequentially correcting errors with a low learning rate.</div></div>
'''

# ---- PCA Projection (diagram #64) ----
D["c520e00b4e65"] = r'''
<div class="fig"><div class="figcap">PCA · Projection onto Principal Components</div>
<svg viewBox="0 0 520 210" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="9">

  <!-- LEFT: 2D original space -->
  <text x="115" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Original 2D Space</text>

  <!-- Axes -->
  <line x1="30" y1="180" x2="200" y2="180" stroke="var(--acc-bd,#888)" stroke-width="1"/>
  <text x="202" y="183" fill="var(--acc-tx)" font-size="8">x1</text>
  <line x1="30" y1="180" x2="30" y2="25" stroke="var(--acc-bd,#888)" stroke-width="1"/>
  <text x="22" y="22" fill="var(--acc-tx)" font-size="8">x2</text>

  <!-- Data points in diagonal band (simulate correlated data) -->
  <circle cx="55" cy="155" r="3.5" fill="var(--acc)"/>
  <circle cx="70" cy="145" r="3.5" fill="var(--acc)"/>
  <circle cx="85" cy="135" r="3.5" fill="var(--acc)"/>
  <circle cx="80" cy="125" r="3.5" fill="var(--acc)"/>
  <circle cx="100" cy="118" r="3.5" fill="var(--acc)"/>
  <circle cx="110" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="125" cy="100" r="3.5" fill="var(--acc)"/>
  <circle cx="120" cy="90" r="3.5" fill="var(--acc)"/>
  <circle cx="140" cy="85" r="3.5" fill="var(--acc)"/>
  <circle cx="155" cy="72" r="3.5" fill="var(--acc)"/>
  <circle cx="165" cy="65" r="3.5" fill="var(--acc)"/>
  <circle cx="62" cy="140" r="3.5" fill="var(--acc)"/>
  <circle cx="95" cy="128" r="3.5" fill="var(--acc)"/>
  <circle cx="148" cy="78" r="3.5" fill="var(--acc)"/>

  <!-- PC1 axis (diagonal, direction of max variance) -->
  <line x1="40" y1="172" x2="185" y2="48" stroke="var(--acc)" stroke-width="2" stroke-dasharray="none"/>
  <text x="188" y="46" fill="var(--acc-tx)" font-size="8" font-weight="700">PC1</text>

  <!-- PC2 axis (orthogonal) -->
  <line x1="88" y1="38" x2="138" y2="178" stroke="var(--acc-d,#888)" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="140" y="185" fill="var(--acc-tx)" font-size="8">PC2</text>

  <!-- Projection lines from 3 points to PC1 -->
  <line x1="85" y1="135" x2="73" y2="121" stroke="var(--acc-d,#888)" stroke-width="0.8" stroke-dasharray="2,2"/>
  <line x1="125" y1="100" x2="112" y2="86" stroke="var(--acc-d,#888)" stroke-width="0.8" stroke-dasharray="2,2"/>
  <line x1="155" y1="72" x2="143" y2="58" stroke="var(--acc-d,#888)" stroke-width="0.8" stroke-dasharray="2,2"/>

  <!-- Arrow to right side -->
  <text x="225" y="105" fill="var(--acc)" font-size="22">→</text>
  <text x="222" y="122" fill="var(--acc-tx)" font-size="8">Z = XV_k</text>

  <!-- RIGHT: 1D projected -->
  <text x="395" y="14" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="10">Projected 1D (PC1)</text>
  <line x1="265" y1="110" x2="510" y2="110" stroke="var(--acc)" stroke-width="2"/>
  <text x="512" y="113" fill="var(--acc-tx)" font-size="8">PC1</text>

  <!-- Projected points on line -->
  <circle cx="285" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="305" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="320" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="338" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="355" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="370" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="388" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="405" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="422" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="440" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="458" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="293" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="347" cy="110" r="3.5" fill="var(--acc)"/>
  <circle cx="449" cy="110" r="3.5" fill="var(--acc)"/>

  <!-- Info boxes -->
  <rect x="270" y="130" width="220" height="60" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd,var(--acc))" stroke-width="1"/>
  <text x="380" y="148" text-anchor="middle" fill="var(--acc-tx)" font-weight="700" font-size="9">Variance explained</text>
  <text x="380" y="163" text-anchor="middle" fill="var(--acc-tx)" font-size="8">PC1: 87% of total variance</text>
  <text x="380" y="176" text-anchor="middle" fill="var(--acc-tx)" font-size="8">PC2: 13% (discarded)</text>
  <text x="380" y="185" text-anchor="middle" fill="var(--acc-tx)" font-size="7.5">EVR_k = λ_k / Σ λᵢ</text>

  <!-- Original label -->
  <text x="115" y="197" text-anchor="middle" fill="var(--acc-tx)" font-size="8">2 coordinates per point</text>
  <text x="380" y="197" text-anchor="middle" fill="var(--acc-tx)" font-size="8">1 coordinate per point (87% info kept)</text>
</svg>
<div class="fignote">Eigenvectors of the covariance matrix Σ = (1/n)XᵀX give the principal directions; eigenvalues measure variance along each direction.</div></div>
'''

# ---- Random Forest (diagram #17) ----
D["0670cbbe4542"] = r'''
<div class="fig"><div class="figcap">Random Forest · Bootstrap + Feature Subsampling</div>
<div class="fcol">
  <div class="node acc" style="align-self:center"><div class="nt">Training Data  (n samples, p features)</div></div>
  <div class="ar-d">↓ repeat for each of n_trees</div>
  <div class="tiers">
    <div class="tier">
      <div class="th">Tree 1</div>
      <div class="node soft"><div class="nt">Bootstrap sample</div><div class="ns">n rows w/ replacement</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Build tree</div><div class="ns">at each split: try √p features</div></div>
    </div>
    <div class="tier">
      <div class="th">Tree 2</div>
      <div class="node soft"><div class="nt">Bootstrap sample</div><div class="ns">different rows</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Build tree</div><div class="ns">different √p features</div></div>
    </div>
    <div class="tier">
      <div class="th">Tree B</div>
      <div class="node soft"><div class="nt">Bootstrap sample</div><div class="ns">…</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Build tree</div><div class="ns">…</div></div>
    </div>
  </div>
  <div class="ar-d">↓ aggregate predictions</div>
  <div class="frow" style="gap:12px">
    <div class="node soft"><div class="nt">Classify</div><div class="ns">majority_vote(tree.predict(x))</div></div>
    <div class="node soft"><div class="nt">Regress</div><div class="ns">mean(tree.predict(x))</div></div>
  </div>
</div>
<div class="frow" style="margin-top:10px;gap:8px">
  <span class="chip">Bootstrap → decorrelates trees</span>
  <span class="chip">√p features → extra randomness</span>
  <span class="chip">Low bias + low variance</span>
</div>
<div class="fignote">Var(avg of B corr. trees) = ρσ² + (1−ρ)σ²/B — decorrelation (ρ→0) is key; averaging alone only helps when trees disagree.</div></div>
'''

# ---- Stacking (diagram #59) ----
D["e1991ecae023"] = r'''
<div class="fig"><div class="figcap">Stacking · Two-Level Ensemble</div>
<div class="tiers">
  <div class="tier">
    <div class="th">LEVEL 0 · Base Models</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Input X</div></div>
      <div class="ar-d">↓ train independently (with CV)</div>
      <div class="frow" style="gap:6px">
        <div class="node"><div class="nt">Logistic Reg.</div><div class="ns">→ pred_A</div></div>
        <div class="node"><div class="nt">Random Forest</div><div class="ns">→ pred_B</div></div>
        <div class="node"><div class="nt">XGBoost</div><div class="ns">→ pred_C</div></div>
      </div>
      <div class="ar-d">↓ collect out-of-fold predictions</div>
      <div class="node acc"><div class="nt">[pred_A, pred_B, pred_C]</div><div class="ns">new feature matrix for Level 1</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">LEVEL 1 · Meta-Model</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Meta-features</div><div class="ns">[pred_A, pred_B, pred_C]</div></div>
      <div class="ar-d">↓ learns optimal combination</div>
      <div class="node acc"><div class="nt">Meta Learner</div><div class="ns">often Logistic Reg. / Ridge</div></div>
      <div class="ar-d">↓</div>
      <div class="node" style="border:2px solid var(--acc)"><div class="nt">Final Prediction</div></div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px">
  <span class="chip">CV prevents leakage · meta-model learns base model strengths · often beats any single model</span>
</div>
<div class="fignote">Use cross-validation when generating base predictions so the meta-model trains on out-of-fold (unseen) predictions — prevents overfitting.</div></div>
'''

# ---- Bias-Variance Tradeoff: Single Tree vs RF (diagram #65) ----
D["8117e0cad8b4"] = r'''
<div class="fig"><div class="figcap">Bias–Variance Tradeoff · Single Tree vs Random Forest</div>
<svg viewBox="0 0 520 200" style="display:block;margin:0 auto" font-family="'Space Grotesk',sans-serif" font-size="9">

  <!-- Axis -->
  <line x1="40" y1="170" x2="490" y2="170" stroke="var(--acc-bd,#888)" stroke-width="1"/>
  <text x="492" y="173" fill="var(--acc-tx)" font-size="8">Complexity →</text>
  <line x1="40" y1="20" x2="40" y2="170" stroke="var(--acc-bd,#888)" stroke-width="1"/>
  <text x="42" y="16" fill="var(--acc-tx)" font-size="8">Error</text>

  <!-- Single Tree: high total error bar -->
  <rect x="90" y="55" width="130" height="110" rx="4" fill="var(--acc)" opacity="0.18"/>
  <rect x="90" y="55" width="130" height="30" rx="4" fill="var(--acc-d,#888)" opacity="0.5"/>
  <!-- bias portion -->
  <rect x="90" y="85" width="130" height="80" rx="0" fill="var(--acc)" opacity="0.35"/>
  <text x="155" y="73" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">Bias (low)</text>
  <text x="155" y="130" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">Variance (HIGH)</text>
  <text x="155" y="178" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="700">Single Deep Tree</text>
  <!-- total error bracket -->
  <line x1="235" y1="55" x2="248" y2="55" stroke="var(--acc-tx)" stroke-width="1"/>
  <line x1="235" y1="165" x2="248" y2="165" stroke="var(--acc-tx)" stroke-width="1"/>
  <line x1="242" y1="55" x2="242" y2="165" stroke="var(--acc-tx)" stroke-width="1"/>
  <text x="252" y="115" fill="var(--acc-tx)" font-size="8">Total</text>
  <text x="252" y="125" fill="var(--acc-tx)" font-size="8">Error</text>
  <text x="252" y="135" fill="var(--acc-tx)" font-size="8">(high)</text>

  <!-- Random Forest: lower total error -->
  <rect x="320" y="85" width="130" height="80" rx="4" fill="var(--acc)" opacity="0.18"/>
  <rect x="320" y="85" width="130" height="30" rx="4" fill="var(--acc-d,#888)" opacity="0.5"/>
  <rect x="320" y="115" width="130" height="50" rx="0" fill="var(--acc)" opacity="0.35"/>
  <text x="385" y="103" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">Bias (same)</text>
  <text x="385" y="145" text-anchor="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">Variance (low)</text>
  <text x="385" y="178" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="700">Random Forest</text>
  <!-- total error bracket -->
  <line x1="465" y1="85" x2="478" y2="85" stroke="var(--acc-tx)" stroke-width="1"/>
  <line x1="465" y1="165" x2="478" y2="165" stroke="var(--acc-tx)" stroke-width="1"/>
  <line x1="472" y1="85" x2="472" y2="165" stroke="var(--acc-tx)" stroke-width="1"/>
  <text x="480" y="125" fill="var(--acc-tx)" font-size="8">Total</text>
  <text x="480" y="135" fill="var(--acc-tx)" font-size="8">Error</text>
  <text x="480" y="145" fill="var(--acc-tx)" font-size="8">(lower!)</text>

  <!-- Noise floor line -->
  <line x1="40" y1="162" x2="490" y2="162" stroke="var(--acc-d,#888)" stroke-width="0.8" stroke-dasharray="4,3"/>
  <text x="45" y="159" fill="var(--acc-tx)" font-size="7.5">irreducible noise</text>

  <!-- Legend -->
  <rect x="75" y="30" width="14" height="10" fill="var(--acc-d,#888)" opacity="0.5"/>
  <text x="93" y="40" fill="var(--acc-tx)" font-size="8">Bias</text>
  <rect x="120" y="30" width="14" height="10" fill="var(--acc)" opacity="0.35"/>
  <text x="138" y="40" fill="var(--acc-tx)" font-size="8">Variance</text>
</svg>
<div class="fignote">RF keeps bias roughly equal to a single deep tree but dramatically cuts variance by averaging B decorrelated trees: Var(avg) = ρσ² + (1−ρ)σ²/B.</div></div>
'''

# ---- Bagging flow (diagram #55) ----
D["beb0f388c6db"] = r'''
<div class="fig"><div class="figcap">Bagging · Bootstrap Aggregating Flow</div>
<div class="fcol">
  <div class="node acc" style="align-self:center"><div class="nt">Data</div></div>
  <div class="frow" style="margin-top:6px;gap:16px">
    <div class="fcol">
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Bootstrap 1</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Model 1</div></div>
    </div>
    <div class="fcol">
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Bootstrap 2</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Model 2</div></div>
    </div>
    <div class="fcol">
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Bootstrap 3</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Model 3</div></div>
    </div>
  </div>
  <div class="ar-d">↓ combine</div>
  <div class="node acc" style="align-self:center"><div class="nt">Average / Vote</div><div class="ns">→ Final Prediction</div></div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">Independent models · parallel training</span>
  <span class="chip">Reduces variance</span>
  <span class="chip">With replacement sampling</span>
</div>
<div class="fignote">Core idea: reduce variance by averaging many high-variance, low-bias models trained on different bootstrap samples of the data.</div></div>
'''

# ---- Boosting flow (diagram #57) ----
D["bee851043f1f"] = r'''
<div class="fig"><div class="figcap">Boosting · Sequential Error Correction</div>
<div class="fcol">
  <div class="node acc" style="align-self:center"><div class="nt">Data</div></div>
  <div class="ar-d">↓ fit first learner</div>
  <div class="frow sb" style="flex-wrap:nowrap">
    <div class="node"><div class="nt">Model 1</div></div>
    <span class="ar">→</span>
    <div class="node soft"><div class="nt">Errors / Residuals</div></div>
  </div>
  <div class="ar-d">↓ focus on errors of Model 1</div>
  <div class="frow sb" style="flex-wrap:nowrap">
    <div class="node"><div class="nt">Model 2</div><div class="ns">fits residuals</div></div>
    <span class="ar">→</span>
    <div class="node soft"><div class="nt">Remaining Residuals</div></div>
  </div>
  <div class="ar-d">↓ focus on remaining</div>
  <div class="frow sb" style="flex-wrap:nowrap">
    <div class="node"><div class="nt">Model 3</div><div class="ns">fits M1+M2 residuals</div></div>
    <span class="ar">→</span>
    <div class="node soft"><div class="nt">…</div></div>
  </div>
  <div class="ar-d">↓ weighted sum</div>
  <div class="node acc" style="align-self:center"><div class="nt">Final = lr·M1 + lr·M2 + lr·M3 + …</div><div class="ns">→ reduces bias</div></div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">Sequential · each corrects prior</span>
  <span class="chip">Weighted combination</span>
  <span class="chip">Reduces bias</span>
</div>
<div class="fignote">Core idea: reduce bias by sequentially fitting models to the residuals (negative gradient) of the current ensemble prediction.</div></div>
'''

# Hand-built HTML diagrams for 06-mlops-and-ml-system-design.md  (key = md5(ascii)[:12])
D = {}

# ---- End-to-end MLOps Pipeline Loop ----
D["31d4707dfc5d"] = r'''
<div class="fig"><div class="figcap">End-to-End MLOps Pipeline</div>
<div class="tiers" style="align-items:stretch">
  <div class="tier">
    <div class="th">DATA</div>
    <div class="fcol" style="gap:6px">
      <div class="node soft"><div class="nt">Raw Sources</div><div class="ns">DB · events · logs</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Ingest</div><div class="ns">Kafka · Flink</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Validate</div><div class="ns">Great Expectations</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">Feature Eng.</div><div class="ns">Spark · dbt · Flink</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">FEATURE STORE</div>
    <div class="fcol" style="gap:6px">
      <div class="node soft"><div class="nt">Offline Store</div><div class="ns">S3 · Hive · Parquet<br>point-in-time joins</div></div>
      <div class="ar-d">↓ batch write &nbsp;/&nbsp; ↑ training read</div>
      <div class="node soft"><div class="nt">Online Store</div><div class="ns">Redis · DynamoDB<br>&lt; 10 ms lookup</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">TRAIN</div>
    <div class="fcol" style="gap:6px">
      <div class="node"><div class="nt">Training Jobs</div><div class="ns">GPU cluster</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Exp. Tracking</div><div class="ns">MLflow · W&amp;B</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Offline Eval</div><div class="ns">AUC · NDCG · RMSE</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">Model Registry</div><div class="ns">staging → prod</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">SERVE</div>
    <div class="fcol" style="gap:6px">
      <div class="node"><div class="nt">Feature Retrieval</div><div class="ns">online store</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">Model Server</div><div class="ns">Triton · TorchServe</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Post-Process</div><div class="ns">rules · safety</div></div>
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">A/B · Canary</div><div class="ns">traffic routing</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">MONITOR</div>
    <div class="fcol" style="gap:6px">
      <div class="node"><div class="nt">Log Collector</div><div class="ns">Kafka</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Drift Detection</div><div class="ns">PSI · KS-test</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Alert System</div><div class="ns">PagerDuty · Slack</div></div>
      <div class="ar-d">↓</div>
      <div class="node acc"><div class="nt">Retrain Trigger</div><div class="ns">CT pipeline</div></div>
    </div>
  </div>
</div>
<svg viewBox="0 0 520 28" style="display:block;margin:0 auto;overflow:visible" height="28">
  <defs><marker id="fbk" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0, 8 3, 0 6" fill="var(--acc)"/></marker></defs>
  <path d="M500,14 Q260,40 20,14" fill="none" stroke="var(--acc)" stroke-width="2" marker-end="url(#fbk)" stroke-dasharray="5,3"/>
  <text x="260" y="26" text-anchor="middle" font-family="Space Grotesk" font-size="9" fill="var(--acc)">feedback → retrain loop</text>
</svg>
<div class="fignote">The MLOps flywheel: data drifts → monitor detects → trigger retrains → new model replaces old → repeat.</div></div>
'''

# ---- Feature Store Architecture ----
D["c19e4f828148"] = r'''
<div class="fig"><div class="figcap">Feature Store · Offline + Online</div>
<div class="fcol" style="gap:8px">
  <div class="node soft" style="text-align:center"><div class="nt">Feature Pipelines</div><div class="ns">Spark · dbt · Flink — shared transformation code</div></div>
  <div class="frow sb" style="gap:10px;flex-wrap:nowrap">
    <div class="ar-d" style="writing-mode:horizontal-tb;transform:none">↙ batch write</div>
    <div class="ar-d" style="writing-mode:horizontal-tb;transform:none">stream write ↘</div>
  </div>
  <div class="frow sb" style="gap:12px;align-items:stretch;flex-wrap:nowrap">
    <div class="fcol" style="flex:1;gap:6px">
      <div class="node acc"><div class="nt">Offline Store</div><div class="ns">S3 · Hive · Delta Lake</div></div>
      <div class="node" style="font-size:0.82em"><div class="nt">Point-in-time correct joins</div><div class="ns">historical feature snapshots<br>used by <b>Training Jobs</b></div></div>
      <div class="frow"><span class="chip">no label leakage</span></div>
    </div>
    <div class="fcol" style="flex:1;gap:6px">
      <div class="node acc"><div class="nt">Online Store</div><div class="ns">Redis · DynamoDB · Cassandra</div></div>
      <div class="node" style="font-size:0.82em"><div class="nt">Latest feature values only</div><div class="ns">key: entity_id → feature vector<br>used by <b>Serving System</b></div></div>
      <div class="frow"><span class="chip">&lt; 10 ms lookup</span></div>
    </div>
  </div>
  <div class="callout c-warn" style="margin-top:4px"><div class="ch">⚠ Training–Serving Skew</div><p>Skew arises when training uses different feature logic than serving. Fix: <b>same pipeline code</b> writes both stores.</p></div>
  <div class="node soft" style="text-align:center"><div class="nt">Feature Registry</div><div class="ns">metadata · lineage · discoverability · ownership</div></div>
</div>
<div class="fignote">Offline store ensures reproducible training; online store ensures low-latency inference — one shared codebase eliminates skew.</div></div>
'''

# ---- Two-Tower Neural Architecture ----
D["c5bd6885dbe1"] = r'''
<div class="fig"><div class="figcap">Two-Tower Model · Retrieval Architecture</div>
<svg viewBox="0 0 520 310" style="display:block;margin:0 auto" height="310">
  <defs>
    <marker id="arr" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="var(--acc)"/></marker>
  </defs>
  <!-- User Tower -->
  <rect x="20" y="10" width="190" height="100" rx="8" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="115" y="28" text-anchor="middle" font-family="Space Grotesk" font-size="11" font-weight="700" fill="var(--acc)">USER TOWER</text>
  <text x="36" y="46" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• user_id embedding</text>
  <text x="36" y="59" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• age · gender · device</text>
  <text x="36" y="72" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• watch history</text>
  <text x="36" y="85" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• search history</text>
  <text x="36" y="98" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• recent interactions</text>
  <!-- Item Tower -->
  <rect x="310" y="10" width="190" height="100" rx="8" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="405" y="28" text-anchor="middle" font-family="Space Grotesk" font-size="11" font-weight="700" fill="var(--acc)">ITEM TOWER</text>
  <text x="326" y="46" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• item_id embedding</text>
  <text x="326" y="59" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• category · duration</text>
  <text x="326" y="72" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• content embedding</text>
  <text x="326" y="85" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• popularity signals</text>
  <text x="326" y="98" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">• freshness</text>
  <!-- MLP boxes -->
  <rect x="55" y="126" width="120" height="32" rx="6" fill="var(--acc)" opacity="0.85"/>
  <text x="115" y="146" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="600" fill="var(--acc-tx)">MLP (3–4 layers)</text>
  <rect x="345" y="126" width="120" height="32" rx="6" fill="var(--acc)" opacity="0.85"/>
  <text x="405" y="146" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="600" fill="var(--acc-tx)">MLP (3–4 layers)</text>
  <!-- Embedding boxes -->
  <rect x="40" y="180" width="150" height="36" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="115" y="196" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="700" fill="var(--acc)">User Embedding</text>
  <text x="115" y="210" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">128–512 dims</text>
  <rect x="330" y="180" width="150" height="36" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="405" y="196" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="700" fill="var(--acc)">Item Embedding</text>
  <text x="405" y="210" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">128–512 dims</text>
  <!-- Dot product -->
  <rect x="175" y="238" width="170" height="36" rx="6" fill="var(--acc)" opacity="0.9"/>
  <text x="260" y="254" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="700" fill="var(--acc-tx)">Dot Product / Cosine</text>
  <text x="260" y="268" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">similarity score</text>
  <!-- Serving note -->
  <rect x="120" y="288" width="280" height="18" rx="4" fill="none" stroke="var(--acc-bd)" stroke-width="1" stroke-dasharray="4,2"/>
  <text x="260" y="300" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">Serve: ANN on pre-indexed item embeds (FAISS/ScaNN) &lt; 10ms</text>
  <!-- Arrows -->
  <line x1="115" y1="110" x2="115" y2="124" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="405" y1="110" x2="405" y2="124" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="115" y1="158" x2="115" y2="178" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="405" y1="158" x2="405" y2="178" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="165" y1="198" x2="228" y2="245" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="355" y1="198" x2="295" y2="245" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <line x1="260" y1="274" x2="260" y2="286" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
</svg>
<div class="fignote">Two towers trained jointly; at inference only the user tower runs online — item embeddings are pre-computed &amp; ANN-indexed.</div></div>
'''

# ---- Candidate Generation → Ranking → Re-Ranking Funnel ----
D["044e484e7222"] = r'''
<div class="fig"><div class="figcap">Recommendation Funnel · Netflix / YouTube Scale</div>
<svg viewBox="0 0 520 330" style="display:block;margin:0 auto" height="330">
  <defs><marker id="fa" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="var(--acc)"/></marker></defs>
  <!-- Funnel bars (centered trapezoids via polygons) -->
  <!-- All Items -->
  <polygon points="60,10 460,10 440,54 80,54" fill="var(--acc)" opacity="0.90"/>
  <text x="260" y="36" text-anchor="middle" font-family="Space Grotesk" font-size="11" font-weight="700" fill="var(--acc-tx)">All Items — millions</text>
  <!-- label -->
  <line x1="260" y1="54" x2="260" y2="68" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#fa)"/>
  <text x="264" y="64" font-family="JetBrains Mono" font-size="8" fill="var(--acc)">CANDIDATE GENERATION &lt; 100ms</text>
  <!-- Stage 1 -->
  <polygon points="80,72 440,72 400,124 120,124" fill="var(--acc)" opacity="0.75"/>
  <text x="260" y="92" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="600" fill="var(--acc-tx)">Candidate Generation</text>
  <text x="260" y="108" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">Two-tower ANN · content sim · trending · history</text>
  <text x="260" y="120" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="var(--acc-tx)">→ ~500 candidates</text>
  <line x1="260" y1="124" x2="260" y2="138" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#fa)"/>
  <text x="264" y="136" font-family="JetBrains Mono" font-size="8" fill="var(--acc)">RANKING 100–200ms</text>
  <!-- Stage 2 -->
  <polygon points="120,142 400,142 360,198 160,198" fill="var(--acc)" opacity="0.60"/>
  <text x="260" y="162" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="600" fill="var(--acc-tx)">Ranking</text>
  <text x="260" y="176" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">Wide&amp;Deep / DCN · P(click) P(watch&gt;30s) P(like)</text>
  <text x="260" y="194" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="var(--acc-tx)">→ ~50 items</text>
  <line x1="260" y1="198" x2="260" y2="212" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#fa)"/>
  <text x="264" y="210" font-family="JetBrains Mono" font-size="8" fill="var(--acc)">RE-RANKING 50ms</text>
  <!-- Stage 3 -->
  <polygon points="160,216 360,216 320,268 200,268" fill="var(--acc)" opacity="0.45"/>
  <text x="260" y="236" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="600" fill="var(--acc-tx)">Re-Ranking</text>
  <text x="260" y="250" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">diversity · dedup · freshness · safety · ads</text>
  <text x="260" y="264" text-anchor="middle" font-family="JetBrains Mono" font-size="9" font-weight="700" fill="var(--acc-tx)">→ 20–30 items</text>
  <line x1="260" y1="268" x2="260" y2="282" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#fa)"/>
  <!-- Final -->
  <rect x="200" y="286" width="120" height="36" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2"/>
  <text x="260" y="306" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="700" fill="var(--acc)">User sees feed</text>
  <text x="260" y="318" text-anchor="middle" font-family="JetBrains Mono" font-size="7.5" fill="var(--acc-tx)">paginated 20/load</text>
</svg>
<div class="fignote">Each stage trades recall for precision; candidate gen maximises recall, ranking maximises relevance, re-ranking enforces business constraints.</div></div>
'''

# ---- Data vs Model Parallelism ----
D["530082ca6c17"] = r'''
<div class="fig"><div class="figcap">Distributed Training · Data vs Model vs Tensor Parallelism</div>
<div class="frow sb" style="gap:12px;align-items:stretch;flex-wrap:nowrap">
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">Data Parallelism</div></div>
    <div class="gantt">
      <div class="gr"><span class="gl" style="width:56px">GPU 1</span><div class="track"><div class="gseg a" style="width:100%">Model copy · Shard 1</div></div></div>
      <div class="gr"><span class="gl" style="width:56px">GPU 2</span><div class="track"><div class="gseg b" style="width:100%">Model copy · Shard 2</div></div></div>
      <div class="gr"><span class="gl" style="width:56px">GPU 3</span><div class="track"><div class="gseg a" style="width:100%">Model copy · Shard 3</div></div></div>
      <div class="gr"><span class="gl" style="width:56px">GPU 4</span><div class="track"><div class="gseg b" style="width:100%">Model copy · Shard 4</div></div></div>
    </div>
    <div class="frow" style="justify-content:center"><span class="chip">All-Reduce gradients</span></div>
    <div class="callout c-warn" style="font-size:0.82em"><div class="ch">Constraint</div><p>Full model must fit on <b>one GPU</b></p></div>
  </div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">Pipeline Parallelism</div></div>
    <div class="gantt">
      <div class="gr"><span class="gl" style="width:56px">GPU 1</span><div class="track"><div class="gseg a" style="width:30%">L 1–3</div><div class="gseg m" style="width:70%"></div></div></div>
      <div class="gr"><span class="gl" style="width:56px">GPU 2</span><div class="track"><div class="gseg m" style="width:30%"></div><div class="gseg b" style="width:35%">L 4–6</div><div class="gseg m" style="width:35%"></div></div></div>
      <div class="gr"><span class="gl" style="width:56px">GPU 3</span><div class="track"><div class="gseg m" style="width:65%"></div><div class="gseg a" style="width:35%">L 7–9</div></div></div>
    </div>
    <div class="frow" style="justify-content:center"><span class="chip">activations passed forward</span></div>
    <div class="callout c-key" style="font-size:0.82em"><div class="ch">Benefit</div><p>Train models too large for one GPU</p></div>
  </div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">Tensor Parallelism</div></div>
    <div class="fcol" style="gap:4px">
      <div class="node soft"><div class="nt">GPU 1</div><div class="ns">W[rows 0:N/2, :] × X<br>→ partial result 1</div></div>
      <div class="node soft"><div class="nt">GPU 2</div><div class="ns">W[rows N/2:N, :] × X<br>→ partial result 2</div></div>
    </div>
    <div class="frow" style="justify-content:center"><span class="chip">AllGather → full result</span></div>
    <div class="callout c-ana" style="font-size:0.82em"><div class="ch">3D Parallelism</div><p>Data × Pipeline × Tensor = trillion-param models</p></div>
  </div>
</div>
<div class="fignote">Data parallelism scales throughput; pipeline/tensor parallelism scales model size. Combine all three for LLM training.</div></div>
'''

# ---- Drift Monitoring & Response Loop ----
D["6fcc56341d7d"] = r'''
<div class="fig"><div class="figcap">Drift Monitoring &amp; Response Loop</div>
<svg viewBox="0 0 520 290" style="display:block;margin:0 auto" height="290">
  <defs><marker id="da" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto"><polygon points="0 0,8 3,0 6" fill="var(--acc)"/></marker></defs>
  <!-- Production box -->
  <rect x="10" y="20" width="110" height="38" rx="6" fill="var(--acc)" opacity="0.85"/>
  <text x="65" y="38" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="700" fill="var(--acc-tx)">Production</text>
  <text x="65" y="51" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">traffic</text>
  <line x1="120" y1="39" x2="158" y2="39" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#da)"/>
  <!-- Feature Logging -->
  <rect x="160" y="20" width="110" height="38" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="215" y="38" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="600" fill="var(--acc-tx)">Feature Logging</text>
  <text x="215" y="51" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">Kafka → S3</text>
  <line x1="270" y1="39" x2="308" y2="39" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#da)"/>
  <!-- Stats box -->
  <rect x="310" y="10" width="200" height="80" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="410" y="28" text-anchor="middle" font-family="Space Grotesk" font-size="10" font-weight="700" fill="var(--acc)">Statistical Tests</text>
  <text x="326" y="43" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">• PSI per feature</text>
  <text x="326" y="55" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">• KS-test distributions</text>
  <text x="326" y="67" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">• Chi-squared (categorical)</text>
  <text x="326" y="79" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">• Prediction distribution</text>
  <!-- Decision diamond -->
  <polygon points="410,110 460,140 410,170 360,140" fill="var(--acc)" opacity="0.75"/>
  <text x="410" y="136" text-anchor="middle" font-family="Space Grotesk" font-size="9" font-weight="700" fill="var(--acc-tx)">Drift</text>
  <text x="410" y="148" text-anchor="middle" font-family="Space Grotesk" font-size="9" font-weight="700" fill="var(--acc-tx)">detected?</text>
  <line x1="410" y1="90" x2="410" y2="108" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#da)"/>
  <!-- NO branch -->
  <line x1="360" y1="140" x2="260" y2="140" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#da)"/>
  <text x="310" y="135" text-anchor="middle" font-family="Space Grotesk" font-size="8" fill="var(--acc)">NO</text>
  <rect x="160" y="120" width="100" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="210" y="137" text-anchor="middle" font-family="Space Grotesk" font-size="9" fill="var(--acc-tx)">Continue</text>
  <text x="210" y="150" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">monitoring</text>
  <!-- YES branch -->
  <line x1="410" y1="170" x2="410" y2="195" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#da)"/>
  <text x="416" y="186" font-family="Space Grotesk" font-size="8" fill="var(--acc)">YES</text>
  <!-- Severity diamond -->
  <polygon points="410,200 455,228 410,256 365,228" fill="var(--acc)" opacity="0.6"/>
  <text x="410" y="224" text-anchor="middle" font-family="Space Grotesk" font-size="9" font-weight="700" fill="var(--acc-tx)">Severity?</text>
  <!-- LOW -->
  <line x1="365" y1="228" x2="280" y2="228" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#da)"/>
  <text x="322" y="223" text-anchor="middle" font-family="Space Grotesk" font-size="8" fill="var(--acc)">LOW</text>
  <rect x="160" y="210" width="118" height="40" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1"/>
  <text x="219" y="228" text-anchor="middle" font-family="Space Grotesk" font-size="9" fill="var(--acc-tx)">Log &amp; notify</text>
  <text x="219" y="241" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc-tx)">team (Slack)</text>
  <!-- HIGH -->
  <line x1="455" y1="228" x2="498" y2="228" stroke="var(--acc)" stroke-width="1.5"/>
  <line x1="498" y1="228" x2="498" y2="260" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="474" y="223" text-anchor="middle" font-family="Space Grotesk" font-size="8" fill="var(--acc)">HIGH</text>
  <rect x="430" y="262" width="80" height="24" rx="6" fill="var(--acc)" opacity="0.85"/>
  <text x="470" y="278" text-anchor="middle" font-family="Space Grotesk" font-size="8.5" font-weight="700" fill="var(--acc-tx)">Auto-retrain</text>
  <!-- feedback arrow back to production -->
  <line x1="470" y1="286" x2="470" y2="290" stroke="var(--acc)" stroke-width="1"/>
  <path d="M470,290 Q260,310 65,290 L65,60" fill="none" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="5,3" marker-end="url(#da)"/>
  <text x="260" y="308" text-anchor="middle" font-family="JetBrains Mono" font-size="8" fill="var(--acc)">retrained model → production</text>
</svg>
<div class="fignote">PSI &gt; 0.2 = major shift; KS p &lt; 0.05 = distribution change. High severity auto-triggers CT pipeline; low severity pages humans.</div></div>
'''

# ---- Model Serving Infrastructure ----
D["93ec59110758"] = r'''
<div class="fig"><div class="figcap">Model Serving · Request Path</div>
<div class="fcol" style="gap:6px;align-items:center">
  <div class="node soft" style="min-width:220px;text-align:center"><div class="nt">Client Request</div></div>
  <div class="ar-d">↓</div>
  <div class="node" style="min-width:220px;text-align:center"><div class="nt">Load Balancer</div></div>
  <div class="ar-d">↓</div>
  <div class="node" style="min-width:220px;text-align:center"><div class="nt">API Gateway</div><div class="ns">auth · rate limiting · routing</div></div>
  <div class="ar-d">↓</div>
  <div class="frow" style="gap:10px;flex-wrap:nowrap;align-items:center">
    <div class="node acc" style="min-width:160px;text-align:center"><div class="nt">Feature Service</div></div>
    <span class="ar">→</span>
    <div class="node soft" style="min-width:160px;text-align:center"><div class="nt">Online Feature Store</div><div class="ns">Redis · &lt; 10ms</div></div>
  </div>
  <div class="ar-d">↓</div>
  <div class="frow" style="gap:10px;flex-wrap:nowrap;align-items:center">
    <div class="node acc" style="min-width:160px;text-align:center"><div class="nt">Model Server</div><div class="ns">Triton · TorchServe</div></div>
    <span class="ar">←</span>
    <div class="node soft" style="min-width:160px;text-align:center"><div class="nt">Model Registry</div><div class="ns">pulls artifacts</div></div>
  </div>
  <div class="frow" style="gap:8px;flex-wrap:nowrap;align-items:center;margin-top:-2px">
    <span class="chip">GPU batch</span><span class="chip">dynamic batching</span><span class="chip">model ensemble</span>
  </div>
  <div class="ar-d">↓</div>
  <div class="node" style="min-width:220px;text-align:center"><div class="nt">Post-Processing</div><div class="ns">business rules · safety filters · ranking blend</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft" style="min-width:220px;text-align:center"><div class="nt">Response</div><div class="ns">JSON / protobuf · p99 &lt; 100ms</div></div>
</div>
<div class="fignote">Feature retrieval + model inference must stay within SLA; batch dynamic requests on GPU to amortize overhead.</div></div>
'''

# ---- Feature Store Deep Dive ----
D["962a493dac5f"] = r'''
<div class="fig"><div class="figcap">Feature Store · Data Sources to Consumers</div>
<div class="tiers" style="align-items:stretch">
  <div class="tier">
    <div class="th">DATA SOURCES</div>
    <div class="fcol" style="gap:8px">
      <div class="node soft"><div class="nt">MySQL / Postgres</div><div class="ns">Data Warehouse</div></div>
      <div class="node soft"><div class="nt">Kafka Event Stream</div></div>
      <div class="node soft"><div class="nt">Real-time Context</div><div class="ns">request-time features</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">PIPELINES</div>
    <div class="fcol" style="gap:8px">
      <div class="node"><div class="nt">Batch (Spark)</div><div class="ns">hourly / daily</div></div>
      <div class="node"><div class="nt">Streaming (Flink)</div><div class="ns">seconds – minutes</div></div>
      <div class="node"><div class="nt">Request-time</div><div class="ns">milliseconds</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">STORES</div>
    <div class="fcol" style="gap:8px">
      <div class="node acc"><div class="nt">Offline Store</div><div class="ns">S3 + Parquet<br>point-in-time joins<br>→ Training</div></div>
      <div class="node acc"><div class="nt">Online Store</div><div class="ns">Redis / DynamoDB<br>key: entity_id<br>&lt; 10ms lookup<br>→ Serving</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">CONSUMERS</div>
    <div class="fcol" style="gap:8px">
      <div class="node soft"><div class="nt">Training Job</div><div class="ns">batch features<br>from Offline Store</div></div>
      <div class="node soft"><div class="nt">Serving System</div><div class="ns">real-time features<br>from Online Store<br><b>same code → no skew</b></div></div>
    </div>
  </div>
</div>
<div class="fignote">Shared pipeline code between offline and online paths is the key insight: it eliminates training–serving skew.</div></div>
'''

# ---- Continuous Training / CT Pipeline ----
D["f7ce6bc127c2"] = r'''
<div class="fig"><div class="figcap">Continuous Training (CT) Pipeline · MLOps Level 2</div>
<div class="fcol" style="gap:6px;align-items:center">
  <div class="frow" style="gap:8px;flex-wrap:nowrap;align-items:center">
    <div class="node soft"><div class="nt">Trigger</div><div class="ns">schedule · drift alert · data threshold</div></div>
    <span class="ar">→</span>
    <div class="node"><div class="nt">Data Pipeline</div></div>
    <span class="ar">→</span>
    <div class="node"><div class="nt">Validation</div><div class="ns">data quality checks</div></div>
    <span class="ar">→</span>
    <div class="node acc"><div class="nt">Training</div><div class="ns">GPU cluster</div></div>
  </div>
  <div class="ar-d">↓</div>
  <div class="frow" style="gap:8px;flex-wrap:nowrap;align-items:center">
    <div class="node acc"><div class="nt">Evaluation</div><div class="ns">offline metrics</div></div>
    <span class="ar">→</span>
    <div class="node soft"><div class="nt">Pass threshold?</div></div>
  </div>
  <div class="frow sb" style="gap:40px;flex-wrap:nowrap;margin-top:4px">
    <div class="fcol" style="align-items:center;gap:4px">
      <div class="ar-d">↓ NO</div>
      <div class="node" style="border-color:var(--acc)"><div class="nt">Alert humans</div><div class="ns">investigation required</div></div>
    </div>
    <div class="fcol" style="align-items:center;gap:4px">
      <div class="ar-d">↓ YES</div>
      <div class="node acc"><div class="nt">Model Registry</div><div class="ns">staging</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Integration Tests</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Shadow Deployment</div><div class="ns">serve silently, log</div></div>
      <div class="ar-d">↓</div>
      <div class="node"><div class="nt">Canary (5%)</div><div class="ns">compare metrics</div></div>
      <div class="ar-d">↓ metrics OK</div>
      <div class="node soft"><div class="nt">Full Rollout</div><div class="ns">100% traffic</div></div>
    </div>
  </div>
</div>
<div class="fignote">Progressive delivery (shadow → canary → full) limits blast radius if the new model regresses on production traffic.</div></div>
'''

# ---- Feed Ranking Pipeline (Worked Design) ----
D["d0414b01374a"] = r'''
<div class="fig"><div class="figcap">Feed Ranking Pipeline · Social Network (Worked Design)</div>
<div class="fcol" style="gap:0;align-items:center">
  <div class="node soft" style="min-width:300px;text-align:center"><div class="nt">Social Graph + Candidate Posts</div><div class="ns">last 7 days from user's network</div></div>
  <div class="ar-d">↓</div>
  <div class="stack" style="width:100%;max-width:440px">
    <div class="stk hl">
      <span class="si">1</span>
      <span class="sn">Heuristic Filter</span>
      <span class="sd">&lt; 10ms · recency + basic relevance → top 2000</span>
    </div>
    <div class="stk">
      <span class="si">2</span>
      <span class="sn">Light Ranker</span>
      <span class="sd">&lt; 50ms · logistic regression / small DNN → top 500</span>
    </div>
    <div class="stk hl">
      <span class="si">3</span>
      <span class="sn">Heavy Ranker</span>
      <span class="sd">&lt; 300ms · large multi-task NN · P(like) P(comment) P(share) P(hide) P(30s read)</span>
    </div>
    <div class="stk">
      <span class="si">4</span>
      <span class="sn">Contextual Adjustment</span>
      <span class="sd">&lt; 50ms · diversity (max 3 consecutive same user) · ads every 5th · safety filters</span>
    </div>
  </div>
  <div class="ar-d">↓</div>
  <div class="node acc" style="min-width:300px;text-align:center"><div class="nt">Final Feed</div><div class="ns">100 posts · paginated 20 / load</div></div>
  <div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap;justify-content:center">
    <span class="chip">total budget &lt; 410ms</span>
    <span class="chip">multi-task objectives</span>
    <span class="chip">diversity + ads</span>
    <span class="chip">safety last</span>
  </div>
</div>
<div class="fignote">Cascade of increasing model complexity: cheap heuristics first cull the space, heavy ranker only scores top 500 candidates.</div></div>
'''

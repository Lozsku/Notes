# Hand-built HTML diagrams for 09-performance-engineering.md  (key = md5(ascii)[:12])
D = {}

# ---- Memory hierarchy (CPU core layered stack) ----
D["f4bd7a47effe"] = r"""
<div class="fig"><div class="figcap">Memory Hierarchy · latency &amp; capacity</div>
<div class="stack">
  <div class="stk hl"><span class="si">R</span><span class="sn">Registers</span><span class="sd">&lt; 0.3 ns · ~64 values · inside the core</span></div>
  <div class="stk hl"><span class="si">L1</span><span class="sn">L1 Cache</span><span class="sd">~0.5 ns · 32–64 KB · 8-way associative</span></div>
  <div class="stk"><span class="si">L2</span><span class="sn">L2 Cache</span><span class="sd">~5 ns · 256 KB – 1 MB</span></div>
  <div class="stk"><span class="si">L3</span><span class="sn">L3 Cache (shared LLC)</span><span class="sd">~20–40 ns · 8–64 MB</span></div>
  <div class="stk"><span class="si">D</span><span class="sn">DRAM (Main RAM)</span><span class="sd">~100 ns · 8–512 GB</span></div>
  <div class="stk"><span class="si">NV</span><span class="sn">NVMe SSD</span><span class="sd">~100 µs · 1–8 TB</span></div>
  <div class="stk"><span class="si">SA</span><span class="sn">SATA SSD</span><span class="sd">~500 µs · 1–4 TB</span></div>
  <div class="stk"><span class="si">HD</span><span class="sn">HDD</span><span class="sd">~5–10 ms · 1–20 TB</span></div>
  <div class="stk"><span class="si">LN</span><span class="sn">Network (LAN)</span><span class="sd">~100 µs RTT · ~12.5 GB/s</span></div>
  <div class="stk"><span class="si">WN</span><span class="sn">Network (WAN/global)</span><span class="sd">10–150 ms RTT</span></div>
</div>
<div class="fignote">NVMe SSD is 200,000× slower than L1 cache; RAM is 200× slower. Cache misses are expensive.</div></div>
"""

# ---- Memory hierarchy scale (bar visualization) ----
D["4e8df4825772"] = r"""
<div class="fig"><div class="figcap">Memory Hierarchy · relative latency scale</div>
<div class="gantt">
  <div class="gr"><span class="gl">Registers</span>
    <div class="track"><div class="gseg a" style="width:0.3%">&lt;1</div><div class="gseg m" style="width:99.7%"></div></div></div>
  <div class="gr"><span class="gl">L1 Cache</span>
    <div class="track"><div class="gseg a" style="width:0.5%">0.5 ns</div><div class="gseg m" style="width:99.5%"></div></div></div>
  <div class="gr"><span class="gl">L2 Cache</span>
    <div class="track"><div class="gseg a" style="width:5%">5 ns</div><div class="gseg m" style="width:95%"></div></div></div>
  <div class="gr"><span class="gl">L3 Cache</span>
    <div class="track"><div class="gseg b" style="width:20%">20 ns</div><div class="gseg m" style="width:80%"></div></div></div>
  <div class="gr"><span class="gl">DRAM</span>
    <div class="track"><div class="gseg b" style="width:50%">100 ns</div><div class="gseg m" style="width:50%"></div></div></div>
  <div class="gr"><span class="gl">NVMe SSD</span>
    <div class="track"><div class="gseg m" style="width:60%">100 µs</div><div class="gseg a" style="width:40%">200,000× L1</div></div></div>
  <div class="gr"><span class="gl">HDD</span>
    <div class="track"><div class="gseg m" style="width:90%">5–10 ms</div><div class="gseg b" style="width:10%">10 M× L1</div></div></div>
  <div class="gr"><span class="gl">WAN RTT</span>
    <div class="track"><div class="gseg m" style="width:100%">50–150 ms</div></div></div>
</div>
<div class="fignote">Bar lengths are logarithmically scaled. L1→DRAM = 200× · L1→NVMe = 200,000× · L1→HDD = 20,000,000×</div></div>
"""

# ---- Latency percentile distribution ----
D["2447fc3090f3"] = r"""
<div class="fig"><div class="figcap">Latency Distribution · p50 / p90 / p99 / p999</div>
<svg viewBox="0 0 520 180" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace;font-size:9px">
  <!-- axes -->
  <line x1="50" y1="10" x2="50" y2="140" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <line x1="50" y1="140" x2="510" y2="140" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <!-- axis labels -->
  <text x="20" y="75" fill="var(--acc-tx)" transform="rotate(-90,20,75)" text-anchor="middle" font-size="8">Count</text>
  <text x="280" y="158" fill="var(--acc-tx)" text-anchor="middle" font-size="8">Latency →</text>
  <!-- histogram bars (approximate shape of a right-skewed distribution) -->
  <rect x="55"  y="130" width="16" height="10"  fill="var(--acc)" opacity="0.7"/>
  <rect x="73"  y="110" width="16" height="30"  fill="var(--acc)" opacity="0.7"/>
  <rect x="91"  y="70"  width="16" height="70"  fill="var(--acc)" opacity="0.75"/>
  <rect x="109" y="35"  width="16" height="105" fill="var(--acc)" opacity="0.8"/>
  <rect x="127" y="50"  width="16" height="90"  fill="var(--acc)" opacity="0.8"/>
  <rect x="145" y="75"  width="16" height="65"  fill="var(--acc)" opacity="0.75"/>
  <rect x="163" y="100" width="16" height="40"  fill="var(--acc)" opacity="0.7"/>
  <rect x="181" y="115" width="16" height="25"  fill="var(--acc2)" opacity="0.7"/>
  <rect x="199" y="125" width="16" height="15"  fill="var(--acc2)" opacity="0.65"/>
  <rect x="217" y="130" width="16" height="10"  fill="var(--acc2)" opacity="0.6"/>
  <rect x="235" y="133" width="20" height="7"   fill="var(--acc2)" opacity="0.55"/>
  <rect x="257" y="135" width="20" height="5"   fill="var(--acc2)" opacity="0.5"/>
  <rect x="279" y="136" width="24" height="4"   fill="var(--acc2)" opacity="0.45"/>
  <rect x="305" y="137" width="30" height="3"   fill="var(--acc2)" opacity="0.4"/>
  <rect x="337" y="138" width="40" height="2"   fill="var(--acc2)" opacity="0.35"/>
  <rect x="379" y="138" width="60" height="2"   fill="var(--acc2)" opacity="0.3"/>
  <rect x="441" y="139" width="60" height="1"   fill="var(--acc2)" opacity="0.25"/>
  <!-- percentile markers -->
  <line x1="117" y1="10" x2="117" y2="140" stroke="var(--acc)" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="117" y="8" fill="var(--acc)" text-anchor="middle" font-size="8" font-weight="bold">p50</text>
  <text x="117" y="155" fill="var(--acc)" text-anchor="middle" font-size="8">10 ms</text>
  <line x1="190" y1="10" x2="190" y2="140" stroke="var(--acc)" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="190" y="8" fill="var(--acc)" text-anchor="middle" font-size="8" font-weight="bold">p90</text>
  <text x="190" y="155" fill="var(--acc)" text-anchor="middle" font-size="8">30 ms</text>
  <line x1="295" y1="10" x2="295" y2="140" stroke="var(--acc2)" stroke-width="1" stroke-dasharray="3,3"/>
  <text x="295" y="8" fill="var(--acc2)" text-anchor="middle" font-size="8" font-weight="bold">p99</text>
  <text x="295" y="155" fill="var(--acc2)" text-anchor="middle" font-size="8">100 ms</text>
  <line x1="460" y1="10" x2="460" y2="140" stroke="var(--acc2)" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="460" y="8" fill="var(--acc2)" text-anchor="middle" font-size="8" font-weight="bold">p999</text>
  <text x="460" y="155" fill="var(--acc2)" text-anchor="middle" font-size="8">2000 ms</text>
  <!-- tail annotation -->
  <text x="380" y="50" fill="var(--acc-tx)" font-size="8" text-anchor="middle">← "The Tail"</text>
  <text x="380" y="62" fill="var(--acc-tx)" font-size="8" text-anchor="middle">1M req/day →</text>
  <text x="380" y="74" fill="var(--acc-tx)" font-size="8" text-anchor="middle">1000 users @ 2s</text>
</svg>
<div class="fignote">p999 = 2000 ms while p50 = 10 ms. At 1M requests/day, 1000 users hit a 2-second latency — the tail matters.</div></div>
"""

# ---- Flame graph ----
D["8a0ac97de9fc"] = r"""
<div class="fig"><div class="figcap">Flame Graph · CPU profiler output</div>
<div class="gantt">
  <div class="gr"><span class="gl">main()</span>
    <div class="track"><div class="gseg a" style="width:100%">main()</div></div></div>
  <div class="gr"><span class="gl">handle_request()</span>
    <div class="track"><div class="gseg a" style="width:78%">handle_request()</div><div class="gseg b" style="width:12%">auth()</div><div class="gseg m" style="width:10%"></div></div></div>
  <div class="gr"><span class="gl">process_data()</span>
    <div class="track"><div class="gseg a" style="width:55%">process_data()</div><div class="gseg b" style="width:14%">serialize()</div><div class="gseg b" style="width:9%">auth()</div><div class="gseg m" style="width:22%"></div></div></div>
  <div class="gr"><span class="gl">parse_json()</span>
    <div class="track"><div class="gseg b" style="width:32%">parse_json() ← HOT</div><div class="gseg a" style="width:23%">query_db()</div><div class="gseg m" style="width:45%"></div></div></div>
  <div class="gr"><span class="gl">leaf calls</span>
    <div class="track"><div class="gseg m" style="width:10%">alloc</div><div class="gseg b" style="width:12%">regex</div><div class="gseg m" style="width:10%"></div><div class="gseg a" style="width:11%">exec</div><div class="gseg m" style="width:10%">wait</div><div class="gseg m" style="width:47%"></div></div></div>
</div>
<div class="frow" style="margin-top:8px;gap:12px">
  <span class="chip">Widest bar at top = hottest path</span>
  <span class="chip">Flat plateau = bottleneck</span>
  <span class="chip">parse_json() = optimize first</span>
</div>
<div class="fignote">X-axis = time spent (wider = more CPU time). Y-axis = call stack depth. Flat wide plateaus identify the bottleneck.</div></div>
"""

# ---- Request path — where bottlenecks hide ----
D["ac09bd241822"] = r"""
<div class="fig"><div class="figcap">Request Path · where bottlenecks hide</div>
<div class="tiers">
  <div class="tier"><div class="th">CLIENT</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Browser / App</div><div class="ns">JS bundle size · client rendering</div></div>
    </div></div>
  <div class="tier"><div class="th">EDGE</div>
    <div class="fcol">
      <div class="node"><div class="nt">DNS</div><div class="ns">&lt;5 ms target · TTL matters</div></div>
      <div class="node"><div class="nt">CDN</div><div class="ns">cache miss → origin fetch</div></div>
    </div></div>
  <div class="tier"><div class="th">INFRA</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Load Balancer</div><div class="ns">imbalanced routing → hot server</div></div>
      <div class="node acc"><div class="nt">App Server</div><div class="ns">GC pause · CPU-bound · thread exhaustion</div></div>
    </div></div>
  <div class="tier"><div class="th">DATA</div>
    <div class="fcol">
      <div class="node"><div class="nt">Cache (Redis)</div><div class="ns">miss → extra DB roundtrip</div></div>
      <div class="node soft"><div class="nt">Database</div><div class="ns">slow query · missing index · lock contention · I/O</div></div>
    </div></div>
</div>
<div class="frow" style="margin-top:10px;gap:8px">
  <span class="chip">① time each hop (tracing spans)</span>
  <span class="chip">② find hop &gt;50% of latency</span>
  <span class="chip">③ profile that hop</span>
</div>
<div class="fignote">Instrument every hop with distributed tracing (OpenTelemetry). The largest span is your bottleneck.</div></div>
"""

# ---- Amdahl's Law speedup curve ----
D["c97490497538"] = r"""
<div class="fig"><div class="figcap">Amdahl's Law · S(N) = 1 / [(1−P) + P/N]</div>
<svg viewBox="0 0 520 200" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace;font-size:9px">
  <!-- axes -->
  <line x1="60" y1="10" x2="60" y2="160" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <line x1="60" y1="160" x2="510" y2="160" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <!-- y axis labels -->
  <text x="55" y="163" fill="var(--acc-tx)" text-anchor="end" font-size="8">1×</text>
  <text x="55" y="131" fill="var(--acc-tx)" text-anchor="end" font-size="8">4×</text>
  <text x="55" y="99"  fill="var(--acc-tx)" text-anchor="end" font-size="8">8×</text>
  <text x="55" y="67"  fill="var(--acc-tx)" text-anchor="end" font-size="8">12×</text>
  <text x="55" y="35"  fill="var(--acc-tx)" text-anchor="end" font-size="8">16×</text>
  <!-- x axis labels -->
  <text x="110" y="172" fill="var(--acc-tx)" text-anchor="middle" font-size="8">2</text>
  <text x="160" y="172" fill="var(--acc-tx)" text-anchor="middle" font-size="8">4</text>
  <text x="260" y="172" fill="var(--acc-tx)" text-anchor="middle" font-size="8">8</text>
  <text x="360" y="172" fill="var(--acc-tx)" text-anchor="middle" font-size="8">16</text>
  <text x="480" y="172" fill="var(--acc-tx)" text-anchor="middle" font-size="8">∞</text>
  <text x="285" y="182" fill="var(--acc-tx)" text-anchor="middle" font-size="8">N (processors) →</text>
  <!-- P=0.95 curve: asymptote at 20× — but our max scale is 16× so curve flattens around 12-14× -->
  <!-- plotted points scaled: speedup * 9.4 offset from 160 (so 1×=160, 16×=10) -->
  <!-- S(N,P=0.95): S(1)=1, S(2)=1.90, S(4)=3.48, S(8)=5.93, S(16)=9.38, S(∞)=20 -->
  <polyline points="60,160 110,142 160,127 260,104 360,72 480,15"
    fill="none" stroke="var(--acc)" stroke-width="2.5" stroke-linejoin="round"/>
  <!-- P=0.75 curve: asymptote at 4× -->
  <!-- S(N,P=0.75): S(1)=1, S(2)=1.60, S(4)=2.29, S(8)=2.91, S(16)=3.37, S(∞)=4 -->
  <polyline points="60,160 110,147 160,138 260,130 360,124 480,122"
    fill="none" stroke="var(--acc2)" stroke-width="2" stroke-linejoin="round" stroke-dasharray="5,3"/>
  <!-- asymptote line for P=0.95 (≈20× but capped at ~16× in scale) -->
  <line x1="60" y1="15" x2="510" y2="15" stroke="var(--acc)" stroke-width="1" stroke-dasharray="3,4" opacity="0.5"/>
  <text x="515" y="18" fill="var(--acc)" font-size="8">20× (P=0.95 limit)</text>
  <!-- labels -->
  <text x="490" y="68" fill="var(--acc)" font-size="8">P=0.95</text>
  <text x="490" y="119" fill="var(--acc2)" font-size="8">P=0.75</text>
  <!-- grid lines -->
  <line x1="60" y1="131" x2="510" y2="131" stroke="var(--acc-bd)" stroke-width="0.5" opacity="0.4"/>
  <line x1="60" y1="99"  x2="510" y2="99"  stroke="var(--acc-bd)" stroke-width="0.5" opacity="0.4"/>
  <line x1="60" y1="67"  x2="510" y2="67"  stroke="var(--acc-bd)" stroke-width="0.5" opacity="0.4"/>
  <line x1="60" y1="35"  x2="510" y2="35"  stroke="var(--acc-bd)" stroke-width="0.5" opacity="0.4"/>
</svg>
<div class="fignote">At P=0.95, 16 cores gives only ~9× speedup (not 16×). The serial 5% fraction becomes the ceiling — serial code dominates at scale.</div></div>
"""

# ---- Little's Law ----
D["fb0e7575c0f3"] = r"""
<div class="fig"><div class="figcap">Little's Law · L = λ × W</div>
<div class="frow sb" style="flex-wrap:nowrap;align-items:stretch;gap:12px">
  <div class="node acc" style="flex:1;text-align:center">
    <div class="nt" style="font-size:1.6em;letter-spacing:2px">L = λ × W</div>
    <div class="ns">steady-state system</div>
  </div>
  <div class="fcol" style="flex:2;gap:8px">
    <div class="node soft"><div class="nt">L — concurrency</div><div class="ns">avg items in the system (in-flight requests)</div></div>
    <div class="node soft"><div class="nt">λ — throughput</div><div class="ns">avg arrival / departure rate (req/s)</div></div>
    <div class="node soft"><div class="nt">W — latency</div><div class="ns">avg time each item spends in system (seconds)</div></div>
  </div>
</div>
<div class="frow" style="margin-top:10px;gap:8px">
  <span class="chip">λ = L / W</span>
  <span class="chip">W = L / λ</span>
  <span class="chip">100 req/s × 0.1 s = 10 concurrent</span>
</div>
<div class="fignote">To handle 1000 req/s at p99=200 ms you need at least 200 concurrent-request capacity (threads/connections/goroutines).</div></div>
"""

# ---- USE vs RED methods ----
D["d6671cc23492"] = r"""
<div class="fig"><div class="figcap">USE Method · per resource</div>
<div class="matrix" style="grid-template-columns:1fr 2fr 2fr">
  <div class="cell hd">Signal</div><div class="cell hd">Definition</div><div class="cell hd">Example tool</div>
  <div class="cell on">Utilization</div><div class="cell">% time resource is busy</div><div class="cell"><span class="chip">mpstat</span> <span class="chip">iostat %util</span></div>
  <div class="cell on">Saturation</div><div class="cell">extra work queued / waiting</div><div class="cell"><span class="chip">vmstat r</span> <span class="chip">iostat await</span></div>
  <div class="cell on">Errors</div><div class="cell">error events (hard/soft)</div><div class="cell"><span class="chip">dmesg</span> <span class="chip">netstat -s</span></div>
</div>
<div class="frow" style="margin-top:6px;gap:6px">
  <span class="chip">CPU: util=mpstat · sat=vmstat r-col · err=dmesg MCE</span>
  <span class="chip">Mem: util=free · sat=vmstat si/so · err=dmesg ECC</span>
</div>
<div class="fignote">Apply USE to every resource: CPU, memory, disk, network, mutexes. High utilization + saturation = bottleneck found.</div></div>
"""

D["34d48c50dde8"] = r"""
<div class="fig"><div class="figcap">RED Method · per service / endpoint</div>
<div class="matrix" style="grid-template-columns:1fr 2fr 2fr">
  <div class="cell hd">Signal</div><div class="cell hd">Definition</div><div class="cell hd">Metric</div>
  <div class="cell on">Rate</div><div class="cell">requests per second (throughput)</div><div class="cell"><span class="chip">req/s</span></div>
  <div class="cell on">Errors</div><div class="cell">number / rate of failed requests</div><div class="cell"><span class="chip">5xx rate</span> <span class="chip">timeouts</span></div>
  <div class="cell on">Duration</div><div class="cell">distribution of request latencies</div><div class="cell"><span class="chip">p50</span> <span class="chip">p99</span></div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">USE = resource-centric (infra)</span>
  <span class="chip">RED = service-centric (user-facing)</span>
</div>
<div class="fignote">USE diagnoses infrastructure bottlenecks; RED diagnoses user-facing service health. Use both together.</div></div>
"""

# ---- Performance investigation workflow ----
D["c98706429dc8"] = r"""
<div class="fig"><div class="figcap">Performance Investigation · 8-step workflow</div>
<div class="fcol" style="gap:4px">
  <div class="node acc"><div class="nt">① OBSERVE</div><div class="ns">"p99 latency increased from 50 ms → 500 ms starting 14:23 UTC Tuesday"</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">② MEASURE</div><div class="ns">baseline: CPU%, memory, I/O, network, thread count, GC pauses, error rate, req rate</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">③ HYPOTHESIZE</div><div class="ns">"GC pauses — memory usage also increased at 14:23"</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">④ PROFILE</div><div class="ns">GC logs · heap dump · allocation profiler — targeted at the hypothesis</div></div>
  <div class="ar-d">↓</div>
  <div class="node acc"><div class="nt">⑤ FIND BOTTLENECK</div><div class="ns">"Old gen fills up → Full GC every 30 s · each pause = 800 ms"</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">⑥ FIX</div><div class="ns">change one thing at a time — increase heap / fix the leak / upgrade to ZGC</div></div>
  <div class="ar-d">↓</div>
  <div class="node soft"><div class="nt">⑦ RE-MEASURE</div><div class="ns">confirm: p99 back to 50 ms · GC pauses &lt; 10 ms</div></div>
  <div class="ar-d">↓</div>
  <div class="node"><div class="nt">⑧ DOCUMENT</div><div class="ns">post-mortem · runbook update</div></div>
</div>
<div class="fignote">Never fix what you haven't measured. Change one variable at a time. Always re-measure to confirm the fix.</div></div>
"""

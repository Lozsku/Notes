# Hand-built HTML diagrams for 05-system-design.md  (key = md5(ascii)[:12])
D = {}

# ---- Canonical scalable web architecture (compact) ----
D["dde15d95a430"] = r"""
<div class="fig"><div class="figcap">Canonical Scalable Web Architecture</div>
<div class="tiers">
  <div class="tier"><div class="th">CLIENT</div>
    <div class="fcol"><div class="node soft"><div class="nt">Client</div><div class="ns">browser / mobile</div></div></div>
  </div>
  <div class="tier"><div class="th">EDGE</div>
    <div class="fcol"><div class="node acc"><div class="nt">CDN</div><div class="ns">static assets</div></div></div>
  </div>
  <div class="tier"><div class="th">GATEWAY</div>
    <div class="fcol"><div class="node acc"><div class="nt">API Gateway</div><div class="ns">auth · rate-limit</div></div></div>
  </div>
  <div class="tier"><div class="th">APP</div>
    <div class="fcol">
      <div class="node"><div class="nt">Load Balancer</div><div class="ns">L7 · Nginx/ALB</div></div>
      <div class="ar-d">↓</div>
      <div class="frow">
        <div class="node soft"><div class="nt">App S1</div><div class="ns">stateless</div></div>
        <div class="node soft"><div class="nt">App S2</div><div class="ns">stateless</div></div>
      </div>
    </div>
  </div>
  <div class="tier"><div class="th">DATA</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Cache</div><div class="ns">Redis · hot data</div></div>
      <div class="ar-d">↓ miss</div>
      <div class="node"><div class="nt">Primary DB</div><div class="ns">PostgreSQL writes</div></div>
      <div class="node soft"><div class="nt">Replicas ×2</div><div class="ns">reads</div></div>
    </div>
  </div>
  <div class="tier"><div class="th">ASYNC</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Message Queue</div><div class="ns">Kafka / SQS</div></div>
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Workers</div><div class="ns">email · analytics</div></div>
    </div>
  </div>
</div>
<div class="fignote">Every tier is independently scalable. App servers are stateless — all state lives in cache or DB.</div></div>
"""

# ---- Vertical vs Horizontal Scaling ----
D["54b5166086af"] = r"""
<div class="fig"><div class="figcap">Scaling Strategies · Vertical vs Horizontal</div>
<div class="frow sb" style="align-items:flex-start;gap:18px">
  <div class="fcol" style="flex:1">
    <div class="node acc" style="text-align:center"><div class="nt">Vertical (Scale Up)</div></div>
    <div class="node" style="margin-top:8px">
      <div class="nt">Big Server</div>
      <div class="ns">32 cores · 512 GB RAM</div>
      <div class="ns" style="margin-top:4px">↑ just add bigger hardware</div>
    </div>
    <div class="frow" style="margin-top:8px;gap:6px">
      <span class="chip">Simple — no code change</span>
    </div>
    <div class="frow" style="margin-top:4px;gap:6px">
      <span class="chip">Hard ceiling · SPOF</span>
    </div>
  </div>
  <div class="fcol" style="flex:1">
    <div class="node acc" style="text-align:center"><div class="nt">Horizontal (Scale Out)</div></div>
    <div class="frow" style="margin-top:8px;gap:8px">
      <div class="node soft"><div class="nt">S1</div><div class="ns">4 CPU · 8 GB</div></div>
      <div class="node soft"><div class="nt">S2</div><div class="ns">4 CPU · 8 GB</div></div>
      <div class="node soft"><div class="nt">S3</div><div class="ns">4 CPU · 8 GB</div></div>
    </div>
    <div class="node" style="margin-top:8px;text-align:center"><div class="nt">Load Balancer</div></div>
    <div class="frow" style="margin-top:8px;gap:6px">
      <span class="chip">No ceiling · fault-tolerant</span>
    </div>
    <div class="frow" style="margin-top:4px;gap:6px">
      <span class="chip">Requires stateless design</span>
    </div>
  </div>
</div>
<div class="fignote">Prefer horizontal scaling for long-term growth — stateless services + load balancer enable infinite nodes.</div></div>
"""

# ---- Caching patterns ----
D["c2f0b3efb742"] = r"""
<div class="fig"><div class="figcap">Caching Patterns · 4 Strategies</div>
<div class="matrix" style="grid-template-columns:1fr 2fr 2fr;gap:2px">
  <div class="cell hd">Pattern</div><div class="cell hd">Write path</div><div class="cell hd">Read path</div>
  <div class="cell on">Cache-Aside</div>
  <div class="cell">App → DB, invalidate cache</div>
  <div class="cell">App → Cache (miss) → DB → populate cache</div>
  <div class="cell on">Write-Through</div>
  <div class="cell">App → Cache → DB (sync)</div>
  <div class="cell">App → Cache (always hit)</div>
  <div class="cell on">Write-Back</div>
  <div class="cell">App → Cache; async flush → DB</div>
  <div class="cell">App → Cache (fast); risk: loss on crash</div>
  <div class="cell on">Write-Around</div>
  <div class="cell">App → DB directly (bypass cache)</div>
  <div class="cell">App → Cache (miss) → DB → populate</div>
</div>
<div class="fignote"><b>Cache-Aside</b> is the most common. <b>Write-Back</b> maximises write throughput at the cost of durability.</div></div>
"""

# ---- Sharding ----
D["c1c4cec9bc96"] = r"""
<div class="fig"><div class="figcap">Database Sharding · Partition by Key</div>
<div class="frow sb" style="align-items:flex-start;gap:16px">
  <div class="fcol" style="flex:1;align-items:center">
    <div class="node" style="text-align:center;width:100%"><div class="nt">Without Sharding</div></div>
    <div class="node soft" style="margin-top:8px;width:100%;text-align:center">
      <div class="nt">All data</div>
      <div class="ns">single DB — bottleneck</div>
    </div>
  </div>
  <div class="fcol" style="flex:2">
    <div class="node" style="text-align:center"><div class="nt">With Sharding</div></div>
    <div class="frow" style="margin-top:8px;gap:8px">
      <div class="node acc"><div class="nt">Shard 0</div><div class="ns">user 0 – M</div></div>
      <div class="node acc"><div class="nt">Shard 1</div><div class="ns">user M – N</div></div>
      <div class="node acc"><div class="nt">Shard 2</div><div class="ns">user N – Z</div></div>
    </div>
    <div class="frow" style="margin-top:8px;gap:6px">
      <span class="chip">hash(user_id) % N → shard</span>
      <span class="chip">parallel queries</span>
    </div>
  </div>
</div>
<div class="fignote">Consistent hashing avoids mass key movement when N changes — only K/N keys reassigned per node add/remove.</div></div>
"""

# ---- Replication (Leader → Followers) ----
D["fccc50852bd2"] = r"""
<div class="fig"><div class="figcap">Database Replication · Leader–Follower</div>
<div class="frow" style="gap:10px;align-items:flex-start">
  <div class="fcol" style="align-items:center">
    <div class="node acc"><div class="nt">Leader (Primary)</div><div class="ns">all WRITES here</div></div>
  </div>
  <div class="fcol" style="gap:8px;flex:1">
    <div class="frow sb" style="flex-wrap:nowrap">
      <div style="display:flex;align-items:center;gap:6px">
        <span class="chip">sync →</span>
        <div class="node soft"><div class="nt">Follower 1</div><div class="ns">READS · sync replica</div></div>
      </div>
    </div>
    <div class="frow sb" style="flex-wrap:nowrap">
      <div style="display:flex;align-items:center;gap:6px">
        <span class="chip">async →</span>
        <div class="node"><div class="nt">Follower 2</div><div class="ns">READS · async replica</div></div>
      </div>
    </div>
    <div class="frow sb" style="flex-wrap:nowrap">
      <div style="display:flex;align-items:center;gap:6px">
        <span class="chip">async →</span>
        <div class="node"><div class="nt">Follower 3</div><div class="ns">READS · async replica</div></div>
      </div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:10px;gap:8px">
  <span class="chip">Reads fan-out to followers</span>
  <span class="chip">Failover: follower promoted on leader failure</span>
</div>
<div class="fignote">Sync replication = strong consistency (write waits for ACK). Async = higher throughput, small replication lag.</div></div>
"""

# ---- CAP Theorem (inline SVG triangle) ----
D["b0e190f357e7"] = r"""
<div class="fig"><div class="figcap">CAP Theorem · Pick 2 of 3</div>
<svg viewBox="0 0 520 280" xmlns="http://www.w3.org/2000/svg" style="font-family:'Space Grotesk',sans-serif">
  <!-- triangle -->
  <polygon points="260,30 60,250 460,250"
    fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2.5"/>
  <!-- vertices -->
  <circle cx="260" cy="30"  r="22" fill="var(--acc)" />
  <circle cx="60"  cy="250" r="22" fill="var(--acc)" />
  <circle cx="460" cy="250" r="22" fill="var(--acc)" />
  <!-- vertex labels -->
  <text x="260" y="34" text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="10" font-weight="700">C</text>
  <text x="60"  y="254" text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="10" font-weight="700">A</text>
  <text x="460" y="254" text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="10" font-weight="700">P</text>
  <!-- full names -->
  <text x="260" y="14" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="600">Consistency</text>
  <text x="30"  y="272" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="600">Availability</text>
  <text x="490" y="272" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="600">Partition Tolerance</text>
  <!-- edge labels -->
  <text x="155" y="140" text-anchor="middle" fill="var(--acc-d)" font-size="9" font-weight="600" transform="rotate(-62,155,140)">CP systems</text>
  <text x="365" y="140" text-anchor="middle" fill="var(--acc-d)" font-size="9" font-weight="600" transform="rotate(62,365,140)">AP systems</text>
  <text x="260" y="265" text-anchor="middle" fill="var(--acc-d)" font-size="9" font-weight="600">CA (impossible in dist. sys)</text>
  <!-- example labels -->
  <text x="148" y="120" text-anchor="middle" fill="var(--acc-d)" font-size="8" transform="rotate(-62,148,120)">HBase · Zookeeper</text>
  <text x="372" y="120" text-anchor="middle" fill="var(--acc-d)" font-size="8" transform="rotate(62,372,120)">Cassandra · DynamoDB</text>
</svg>
<div class="frow" style="margin-top:4px;gap:8px">
  <span class="chip">CP — consistent + partition-tolerant (may be unavailable)</span>
  <span class="chip">AP — available + partition-tolerant (may be stale)</span>
</div>
<div class="fignote">Networks always partition → real systems choose CP (HBase) or AP (Cassandra). CA only in single-node setups.</div></div>
"""

# ---- Message Queue flow (Producer → Queue → Consumers) ----
D["7ff5a34781cb"] = r"""
<div class="fig"><div class="figcap">Message Queue · Producer → Buffer → Consumers</div>
<div class="frow" style="flex-wrap:nowrap;gap:10px;align-items:center">
  <div class="fcol" style="gap:8px">
    <div class="node soft"><div class="nt">Producer 1</div><div class="ns">Order Service</div></div>
    <div class="node soft"><div class="nt">Producer 2</div><div class="ns">User Service</div></div>
  </div>
  <span class="ar">→</span>
  <div class="node acc" style="min-width:120px;text-align:center">
    <div class="nt">Message Queue</div>
    <div class="ns">persistent buffer</div>
    <div class="ns">Kafka / SQS / RabbitMQ</div>
  </div>
  <span class="ar">→</span>
  <div class="fcol" style="gap:8px">
    <div class="node soft"><div class="nt">Consumer 1</div><div class="ns">Email Worker</div></div>
    <div class="node soft"><div class="nt">Consumer 2</div><div class="ns">Analytics</div></div>
    <div class="node soft"><div class="nt">Consumer 3</div><div class="ns">Notifications</div></div>
  </div>
</div>
<div class="frow" style="margin-top:10px;gap:8px">
  <span class="chip">Decouples producers &amp; consumers</span>
  <span class="chip">ACK on success → delete message</span>
  <span class="chip">Dead-letter queue on failure</span>
</div>
<div class="fignote">Queues absorb traffic spikes. Consumers scale independently; failed messages retry without re-hitting producers.</div></div>
"""

# ---- CDN Edge Distribution ----
D["ccbc220a21c5"] = r"""
<div class="fig"><div class="figcap">CDN · Edge Distribution</div>
<div class="frow sb" style="align-items:flex-start;gap:24px">
  <div class="fcol" style="flex:1;align-items:center">
    <div class="node" style="text-align:center;width:100%"><div class="nt">Without CDN</div></div>
    <div class="ar-d" style="margin:8px 0">↓ ~150 ms RTT</div>
    <div class="frow" style="flex-wrap:nowrap;gap:8px">
      <div class="node soft"><div class="nt">User</div><div class="ns">Tokyo</div></div>
      <span class="ar">→</span>
      <div class="node acc"><div class="nt">Origin Server</div><div class="ns">Virginia</div></div>
    </div>
  </div>
  <div class="fcol" style="flex:1;align-items:center">
    <div class="node" style="text-align:center;width:100%"><div class="nt">With CDN</div></div>
    <div class="ar-d" style="margin:8px 0">↓ ~5 ms RTT (cache hit)</div>
    <div class="frow" style="flex-wrap:nowrap;gap:8px">
      <div class="node soft"><div class="nt">User</div><div class="ns">Tokyo</div></div>
      <span class="ar">→</span>
      <div class="node acc"><div class="nt">Edge Node</div><div class="ns">Tokyo PoP</div></div>
      <span class="ar">→</span>
      <div class="node"><div class="nt">Origin</div><div class="ns">only on miss</div></div>
    </div>
  </div>
</div>
<div class="fignote">CDN edge nodes (PoPs) serve static assets from the nearest geography — 30× latency improvement for cache hits.</div></div>
"""

# ---- Consistent Hashing ----
D["12edb33bd188"] = r"""
<div class="fig"><div class="figcap">Consistent Hashing · Ring</div>
<svg viewBox="0 0 520 260" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace">
  <!-- ring -->
  <circle cx="260" cy="130" r="100" fill="none" stroke="var(--acc-bd)" stroke-width="2.5" stroke-dasharray="6 3"/>
  <!-- server nodes on ring -->
  <circle cx="260" cy="30"  r="14" fill="var(--acc)"    />
  <circle cx="360" cy="217" r="14" fill="var(--acc)"    />
  <circle cx="160" cy="217" r="14" fill="var(--acc)"    />
  <circle cx="360" cy="43"  r="14" fill="var(--acc2,var(--acc))" opacity=".75"/>
  <!-- server labels -->
  <text x="260" y="34"  text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">S1</text>
  <text x="360" y="221" text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">S2</text>
  <text x="160" y="221" text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">S3</text>
  <text x="360" y="47"  text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="8" font-weight="700">S4</text>
  <!-- key on ring -->
  <circle cx="310" cy="37" r="8" fill="var(--acc-d)" opacity=".8"/>
  <text x="310" y="41" text-anchor="middle" dominant-baseline="middle" fill="var(--acc-tx)" font-size="7">k</text>
  <!-- clockwise arrow -->
  <path d="M 318 34 Q 345 32 356 44" fill="none" stroke="var(--acc-d)" stroke-width="1.5" marker-end="url(#arr)"/>
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="3" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc-d)"/>
    </marker>
  </defs>
  <!-- 0 label -->
  <text x="260" y="13" text-anchor="middle" fill="var(--acc-d)" font-size="8">0</text>
  <text x="400" y="135" text-anchor="start"  fill="var(--acc-d)" font-size="8">2³²</text>
  <!-- annotation -->
  <text x="130" y="130" text-anchor="middle" fill="var(--acc-d)" font-size="8">key k →</text>
  <text x="130" y="142" text-anchor="middle" fill="var(--acc-d)" font-size="8">clockwise → S4</text>
</svg>
<div class="matrix" style="grid-template-columns:1fr 1fr;margin-top:6px">
  <div class="cell hd">Normal hashing</div><div class="cell hd">Consistent hashing</div>
  <div class="cell">shard = hash(k) % N<br/>→ N changes → ALL keys move</div>
  <div class="cell on">ring position → clockwise server<br/>→ only K/N keys move on change</div>
</div>
<div class="fignote">Virtual nodes (vnodes) improve load balance — each physical server owns multiple ring positions.</div></div>
"""

# ---- Latency numbers every engineer should know ----
D["17851795af0f"] = r"""
<div class="fig"><div class="figcap">Latency Numbers Every Engineer Should Know</div>
<div class="gantt">
  <div class="gr"><span class="gl">L1 cache</span>
    <div class="track"><div class="gseg a" style="width:1%">0.5 ns</div></div></div>
  <div class="gr"><span class="gl">L2 cache</span>
    <div class="track"><div class="gseg a" style="width:1.5%">7 ns</div></div></div>
  <div class="gr"><span class="gl">Mutex lock</span>
    <div class="track"><div class="gseg b" style="width:2%">25 ns</div></div></div>
  <div class="gr"><span class="gl">RAM reference</span>
    <div class="track"><div class="gseg b" style="width:4%">100 ns</div></div></div>
  <div class="gr"><span class="gl">Compress 1K (Zippy)</span>
    <div class="track"><div class="gseg b" style="width:12%">3 µs</div></div></div>
  <div class="gr"><span class="gl">Send 1K over 1 Gbps</span>
    <div class="track"><div class="gseg b" style="width:18%">10 µs</div></div></div>
  <div class="gr"><span class="gl">SSD random read 4K</span>
    <div class="track"><div class="gseg m" style="width:35%">150 µs</div></div></div>
  <div class="gr"><span class="gl">Same-DC round trip</span>
    <div class="track"><div class="gseg m" style="width:60%">0.5 ms</div></div></div>
  <div class="gr"><span class="gl">Disk seek</span>
    <div class="track"><div class="gseg m" style="width:80%">10 ms</div></div></div>
  <div class="gr"><span class="gl">CA → Netherlands → CA</span>
    <div class="track"><div class="gseg m" style="width:100%">150 ms</div></div></div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">Memory 200× faster than disk</span>
  <span class="chip">SSD 67× faster than disk seek</span>
  <span class="chip">RAM 1000× faster than network</span>
</div>
<div class="fignote">Cache aggressively — the gap between RAM and disk/network is enormous. Design reads to hit cache, not disk.</div></div>
"""

# ---- Circuit Breaker states ----
D["a0a620bbd87a"] = r"""
<div class="fig"><div class="figcap">Circuit Breaker · 3 States</div>
<div class="frow" style="flex-wrap:nowrap;gap:8px;align-items:center">
  <div class="node acc" style="text-align:center;min-width:90px">
    <div class="nt">CLOSED</div>
    <div class="ns">normal operation</div>
    <div class="ns">requests pass through</div>
  </div>
  <div class="fcol" style="align-items:center;gap:4px">
    <span style="font-size:9px;color:var(--acc-d)">failures &gt; threshold</span>
    <span class="ar">→</span>
  </div>
  <div class="node" style="text-align:center;min-width:90px;border:2px solid var(--acc)">
    <div class="nt">OPEN</div>
    <div class="ns">reject all requests</div>
    <div class="ns">fast-fail (no load)</div>
  </div>
  <div class="fcol" style="align-items:center;gap:4px">
    <span style="font-size:9px;color:var(--acc-d)">timeout expires</span>
    <span class="ar">→</span>
  </div>
  <div class="node soft" style="text-align:center;min-width:90px">
    <div class="nt">HALF-OPEN</div>
    <div class="ns">probe with 1 request</div>
  </div>
</div>
<div class="frow" style="margin-top:10px;gap:10px">
  <div style="display:flex;align-items:center;gap:6px">
    <span class="chip">success</span><span class="ar">→</span><span style="font-size:9px;color:var(--acc-d)">CLOSED</span>
  </div>
  <div style="display:flex;align-items:center;gap:6px">
    <span class="chip">failure</span><span class="ar">→</span><span style="font-size:9px;color:var(--acc-d)">OPEN again</span>
  </div>
</div>
<div class="fignote">Stops cascading failures — OPEN state gives the downstream service time to recover without being hammered.</div></div>
"""

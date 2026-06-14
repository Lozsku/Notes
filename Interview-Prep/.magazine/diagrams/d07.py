# Hand-built HTML diagrams for 07-distributed-systems.md  (key = md5(ascii)[:12])
D = {}

# ---- Consistent Hashing Ring ----
D["94cef0152efd"] = r"""
<div class="fig"><div class="figcap">Consistent Hashing Ring</div>
<svg viewBox="0 0 520 310" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">
  <!-- ring -->
  <circle cx="260" cy="155" r="110" fill="none" stroke="var(--acc)" stroke-width="2.5"/>
  <!-- 0/2^32 at top -->
  <circle cx="260" cy="45" r="7" fill="var(--acc)" stroke="none"/>
  <text x="260" y="30" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" font-weight="700">0 / 2³²</text>
  <!-- NodeA at top-right (10) -->
  <circle cx="296" cy="51" r="8" fill="var(--acc)" stroke="none"/>
  <text x="315" y="48" text-anchor="start" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" font-weight="700">NodeA (10)</text>
  <!-- NodeB at right (120) -->
  <circle cx="370" cy="155" r="8" fill="var(--acc2)" stroke="none"/>
  <text x="383" y="159" text-anchor="start" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" font-weight="700">NodeB (120)</text>
  <!-- NodeC at bottom (250) -->
  <circle cx="224" cy="260" r="8" fill="var(--acc2)" stroke="none"/>
  <text x="230" y="278" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" font-weight="700">NodeC (250)</text>
  <!-- NodeD at left (340) -->
  <circle cx="150" cy="155" r="8" fill="var(--acc)" stroke="none"/>
  <text x="60" y="159" text-anchor="start" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" font-weight="700">NodeD (340)</text>
  <!-- key dots -->
  <circle cx="336" cy="80" r="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.5"/>
  <text x="350" y="84" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)">90 → NodeB</text>
  <circle cx="312" cy="220" r="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.5"/>
  <text x="320" y="224" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)">180 → NodeC</text>
  <circle cx="264" cy="45" r="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.5"/>
  <text x="270" y="49" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)">5 → NodeA</text>
</svg>
<div class="frow" style="margin-top:6px;gap:6px;flex-wrap:wrap">
  <span class="chip">user:42 → hash 180 → NodeC</span>
  <span class="chip">order:7 → hash 90 → NodeB</span>
  <span class="chip">product:1 → hash 5 → NodeA</span>
</div>
<div class="fignote">Remove NodeB → only keys 90–250 move to NodeC. <b>~1/N keys remap</b> (vs 100% in modulo hashing).</div></div>
"""

# ---- Virtual Nodes on Ring ----
D["7f2beecaac8a"] = r"""
<div class="fig"><div class="figcap">Consistent Hashing · Virtual Nodes</div>
<svg viewBox="0 0 520 300" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">
  <circle cx="260" cy="150" r="108" fill="none" stroke="var(--acc)" stroke-width="2"/>
  <!-- NodeA vnodes: 15, 120, 240 -->
  <circle cx="299" cy="43" r="8" fill="var(--acc)" stroke="none"/>
  <text x="306" y="39" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">A1·15</text>
  <circle cx="368" cy="150" r="8" fill="var(--acc)" stroke="none"/>
  <text x="379" y="154" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">A2·120</text>
  <circle cx="206" cy="246" r="8" fill="var(--acc)" stroke="none"/>
  <text x="175" y="258" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">A3·240</text>
  <!-- NodeB vnodes: 60, 190, 310 -->
  <circle cx="344" cy="58" r="8" fill="var(--acc2)" stroke="none"/>
  <text x="350" y="55" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">B1·60</text>
  <circle cx="323" cy="224" r="8" fill="var(--acc2)" stroke="none"/>
  <text x="330" y="228" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">B2·190</text>
  <circle cx="155" cy="68" r="8" fill="var(--acc2)" stroke="none"/>
  <text x="118" y="65" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">B3·310</text>
  <!-- NodeC vnodes: 90, 210, 350 -->
  <circle cx="368" cy="96" r="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="379" y="100" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">C1·90</text>
  <circle cx="152" cy="204" r="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="115" y="208" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">C2·210</text>
  <circle cx="258" cy="42" r="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="262" y="29" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" font-weight="700">C3·350</text>
  <!-- label center -->
  <text x="260" y="146" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700">vnodes</text>
  <text x="260" y="162" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="9" fill="var(--acc-tx)" opacity="0.7">scattered on ring</text>
</svg>
<div class="fignote">Adding NodeD claims some positions from A, B, and C <b>equally</b> → balanced load, fewer hot spots.</div></div>
"""

# ---- Quorum R+W > N with node overlap ----
D["5d0e6b2ff66c"] = r"""
<div class="fig"><div class="figcap">Quorum Read/Write · Overlap Guarantee (N=5, W=3, R=3)</div>
<div class="frow" style="gap:18px;align-items:flex-start;flex-wrap:wrap">
  <div class="fcol" style="min-width:160px">
    <div class="frow sb" style="flex-wrap:nowrap;margin-bottom:4px">
      <span style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:700;color:var(--acc-tx)">WRITE W=3</span>
    </div>
    <div class="node acc"><div class="nt">N1</div><div class="ns">← Write · ACK</div></div>
    <div class="node acc"><div class="nt">N2</div><div class="ns">← Write · ACK</div></div>
    <div class="node acc"><div class="nt">N3</div><div class="ns">← Write · ACK</div></div>
    <div class="node soft"><div class="nt">N4</div><div class="ns">may lag</div></div>
    <div class="node soft"><div class="nt">N5</div><div class="ns">may lag</div></div>
  </div>
  <div class="fcol" style="justify-content:center;padding-top:48px">
    <div class="callout c-key" style="padding:8px 12px;min-width:130px">
      <div class="ch" style="font-size:11px">◆ Overlap</div>
      <p style="margin:4px 0;font-size:11px">W + R = 6 &gt; N = 5</p>
      <p style="margin:0;font-size:11px">≥ 1 node always has latest</p>
    </div>
  </div>
  <div class="fcol" style="min-width:160px">
    <div class="frow sb" style="flex-wrap:nowrap;margin-bottom:4px">
      <span style="font-family:'Space Grotesk',sans-serif;font-size:11px;font-weight:700;color:var(--acc-tx)">READ R=3</span>
    </div>
    <div class="node soft"><div class="nt">N1</div><div class="ns">x=5 ✓</div></div>
    <div class="node acc"><div class="nt">N2</div><div class="ns">x=5 ✓ ← overlap</div></div>
    <div class="node acc"><div class="nt">N3</div><div class="ns">x=5 ✓ ← overlap</div></div>
    <div class="node acc"><div class="nt">N4</div><div class="ns">x=3 stale</div></div>
    <div class="node soft"><div class="nt">N5</div><div class="ns">x=5 ✓</div></div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">R=1 W=N → fast reads</span>
  <span class="chip">R=N W=1 → fast writes</span>
  <span class="chip">R=W=⌈(N+1)/2⌉ → balanced</span>
</div>
<div class="fignote">Conflict resolution: pick latest version (vector clock / timestamp). N3 stale → return x=5.</div></div>
"""

# ---- Quorum simple formula ----
D["7f417ed4f62d"] = r"""
<div class="fig"><div class="figcap">Quorum Intersection · N=3, W=2, R=2</div>
<div class="matrix" style="grid-template-columns:repeat(4,1fr);margin-bottom:10px">
  <div class="cell hd">Node</div><div class="cell hd">Write</div><div class="cell hd">Read</div><div class="cell hd">Role</div>
  <div class="cell">A</div><div class="cell on">✓</div><div class="cell"></div><div class="cell">write-only</div>
  <div class="cell">B</div><div class="cell on">✓</div><div class="cell on">✓</div><div class="cell"><b>overlap</b></div>
  <div class="cell">C</div><div class="cell"></div><div class="cell on">✓</div><div class="cell">read-only</div>
</div>
<div class="callout c-key" style="padding:8px 14px">
  <div class="ch">◆ Proof</div>
  <p style="margin:4px 0">W + R = 4 &gt; N = 3 → overlap ≥ 1 node (B).</p>
  <p style="margin:0">B always has the latest write — read set is guaranteed fresh.</p>
</div>
<div class="fignote">B is in both quorums → reads always see the most recent committed write.</div></div>
"""

# ---- CAP Triangle ----
D["e2194b9a2c95"] = r"""
<div class="fig"><div class="figcap">CAP Theorem · pick 2 of 3</div>
<svg viewBox="0 0 520 280" xmlns="http://www.w3.org/2000/svg" style="display:block;margin:0 auto">
  <!-- triangle -->
  <polygon points="260,28 60,252 460,252" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="2.5"/>
  <!-- CP edge label (left side) -->
  <text x="140" y="148" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700" transform="rotate(-62,140,148)">CP</text>
  <text x="100" y="160" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)" opacity="0.8" transform="rotate(-62,100,160)">ZooKeeper · etcd · Spanner</text>
  <!-- AP edge label (right side) -->
  <text x="380" y="148" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700" transform="rotate(62,380,148)">AP</text>
  <text x="420" y="160" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)" opacity="0.8" transform="rotate(62,420,160)">DynamoDB · Cassandra · DNS</text>
  <!-- CA edge label (bottom) -->
  <text x="260" y="272" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700">CA</text>
  <text x="260" y="284" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)" opacity="0.6">(single-node / no partition)</text>
  <!-- vertices -->
  <circle cx="260" cy="28" r="10" fill="var(--acc)" stroke="none"/>
  <text x="260" y="18" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700">C</text>
  <text x="260" y="9" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)">Consistency</text>
  <circle cx="60" cy="252" r="10" fill="var(--acc2)" stroke="none"/>
  <text x="36" y="256" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700">A</text>
  <text x="25" y="244" text-anchor="start" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)">Availability</text>
  <circle cx="460" cy="252" r="10" fill="var(--acc2)" stroke="none"/>
  <text x="474" y="256" text-anchor="start" font-family="'Space Grotesk',sans-serif" font-size="11" fill="var(--acc-tx)" font-weight="700">P</text>
  <text x="462" y="244" text-anchor="start" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)">Partition Tol.</text>
  <!-- center note -->
  <text x="260" y="168" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" opacity="0.85">Real choice:</text>
  <text x="260" y="182" text-anchor="middle" font-family="'Space Grotesk',sans-serif" font-size="10" fill="var(--acc-tx)" font-weight="700">CP or AP</text>
  <text x="260" y="196" text-anchor="middle" font-family="'JetBrains Mono',monospace" font-size="8" fill="var(--acc-tx)" opacity="0.7">(P is mandatory in networks)</text>
</svg>
<div class="frow" style="gap:6px;margin-top:4px">
  <span class="chip">CP → error on partition</span>
  <span class="chip">AP → stale data on partition</span>
</div>
<div class="fignote">Partition tolerance is mandatory in real distributed systems — the real trade-off is <b>CP vs AP</b>.</div></div>
"""

# ---- Raft leader election + log replication ----
D["041756d420d7"] = r"""
<div class="fig"><div class="figcap">Raft · Leader Election &amp; Log Replication</div>
<div class="frow sb" style="flex-wrap:nowrap;gap:12px;align-items:flex-start">
  <div class="fcol" style="flex:1;min-width:140px">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:700;color:var(--acc-tx);text-transform:uppercase;margin-bottom:6px">Before</div>
    <div class="node soft"><div class="nt">F term=1</div></div>
    <div class="node soft"><div class="nt">F term=1</div></div>
    <div class="node soft"><div class="nt">F term=1</div><div class="ns">timeout fires →</div></div>
  </div>
  <div class="fcol" style="flex:1;min-width:140px">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:700;color:var(--acc-tx);text-transform:uppercase;margin-bottom:6px">After Election</div>
    <div class="node acc"><div class="nt">L term=2</div><div class="ns">elected leader</div></div>
    <div class="node soft"><div class="nt">F term=2</div></div>
    <div class="node soft"><div class="nt">F term=2</div></div>
  </div>
</div>
<div class="ar-d" style="margin:10px 0">↓ Client → SET x=5 → Leader ↓</div>
<div class="fcol" style="gap:4px">
  <div class="node acc" style="align-self:flex-start;min-width:280px"><div class="nt">Leader Log</div><div class="ns">| idx=1,t=1,x=1 | idx=2,t=2,x=5 | ← uncommitted</div></div>
  <div class="frow" style="margin:4px 0"><span class="ar">→</span><span style="font-size:11px;margin-left:6px">AppendEntries RPC (parallel)</span></div>
  <div class="frow" style="gap:8px">
    <div class="node soft"><div class="nt">Follower 1</div><div class="ns">|idx=1,t=1| |idx=2,t=2,x=5| ↑ ACK</div></div>
    <div class="node soft"><div class="nt">Follower 2</div><div class="ns">|idx=1,t=1| |idx=2,t=2,x=5| ↑ ACK</div></div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">2 of 3 ACKs → majority → commit idx=2</span>
  <span class="chip">next heartbeat → followers apply</span>
</div>
<div class="fignote"><b>Safety:</b> follower only votes for a candidate whose log is at least as up-to-date — prevents loss of committed entries.</div></div>
"""

# ---- Raft log replication detail ----
D["c3ed833f7ca4"] = r"""
<div class="fig"><div class="figcap">Raft · Log Structure &amp; Commit Flow</div>
<div class="tiers">
  <div class="tier">
    <div class="th">CLIENT</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Client</div><div class="ns">SET x=5</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">LEADER</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">1. Append local</div><div class="ns">uncommitted</div></div>
      <div class="node acc"><div class="nt">3. Majority ACK</div><div class="ns">→ commit</div></div>
      <div class="node acc"><div class="nt">4. Apply + reply</div><div class="ns">→ client OK</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">FOLLOWERS</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">2. AppendEntries</div><div class="ns">append + ACK</div></div>
      <div class="node soft"><div class="nt">5. Heartbeat</div><div class="ns">commit notice</div></div>
      <div class="node soft"><div class="nt">6. Apply</div><div class="ns">state machine</div></div>
    </div>
  </div>
</div>
<div class="gantt" style="margin-top:10px">
  <div class="gr"><span class="gl">Index</span>
    <div class="track"><div class="gseg a" style="width:20%">1</div><div class="gseg a" style="width:20%">2</div><div class="gseg b" style="width:20%">3</div><div class="gseg b" style="width:20%">4</div><div class="gseg m" style="width:20%">5</div></div></div>
  <div class="gr"><span class="gl">Term</span>
    <div class="track"><div class="gseg a" style="width:20%">1</div><div class="gseg a" style="width:20%">1</div><div class="gseg b" style="width:20%">2</div><div class="gseg b" style="width:20%">3</div><div class="gseg m" style="width:20%">3</div></div></div>
  <div class="gr"><span class="gl">Cmd</span>
    <div class="track"><div class="gseg a" style="width:20%">SET</div><div class="gseg a" style="width:20%">SET</div><div class="gseg b" style="width:20%">DEL</div><div class="gseg b" style="width:20%">SET</div><div class="gseg m" style="width:20%">SET</div></div></div>
</div>
<div class="fignote">Leader checks <b>prevLogIndex &amp; prevLogTerm</b> before appending — ensures follower logs never diverge.</div></div>
"""

# ---- 2PC phases ----
D["9ced7cc5afce"] = r"""
<div class="fig"><div class="figcap">Two-Phase Commit (2PC)</div>
<div class="frow sb" style="align-items:flex-start;gap:12px;flex-wrap:wrap">
  <div class="fcol" style="flex:1;min-width:180px">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:700;color:var(--acc-tx);text-transform:uppercase;margin-bottom:6px">Phase 1 · Prepare</div>
    <div class="node acc"><div class="nt">Coordinator</div><div class="ns">→ Prepare? → all</div></div>
    <div class="ar-d">↓</div>
    <div class="frow" style="gap:6px">
      <div class="node soft"><div class="nt">Part. A</div><div class="ns">lock · log · Yes</div></div>
      <div class="node soft"><div class="nt">Part. B</div><div class="ns">lock · log · Yes</div></div>
      <div class="node soft"><div class="nt">Part. C</div><div class="ns">lock · log · Yes</div></div>
    </div>
  </div>
  <div class="fcol" style="flex:1;min-width:180px">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:10px;font-weight:700;color:var(--acc-tx);text-transform:uppercase;margin-bottom:6px">Phase 2 · Commit / Abort</div>
    <div class="frow" style="gap:8px;align-items:flex-start">
      <div class="fcol" style="flex:1">
        <div class="callout c-key" style="padding:7px 10px"><div class="ch" style="font-size:10px">◆ ALL Yes</div><p style="margin:4px 0;font-size:10px">→ Commit<br/>release locks<br/>apply changes</p></div>
      </div>
      <div class="fcol" style="flex:1">
        <div class="callout c-warn" style="padding:7px 10px"><div class="ch" style="font-size:10px">◆ ANY No</div><p style="margin:4px 0;font-size:10px">→ Abort<br/>release locks<br/>rollback</p></div>
      </div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">ACID · blocking · coordinator SPOF</span>
  <span class="chip">same DB / tight coupling</span>
</div>
<div class="fignote">Coordinator failure after Phase 1 leaves participants <b>blocked</b> holding locks — main weakness of 2PC.</div></div>
"""

# ---- Saga with compensating transactions ----
D["d1a8f8bc46b7"] = r"""
<div class="fig"><div class="figcap">Saga Pattern · Compensating Transactions</div>
<div class="stack">
  <div class="stk hl"><span class="si">1</span><span class="sn">Create Order</span><span class="sd">compensate: N/A (first step)</span></div>
  <div class="stk"><span class="si">2</span><span class="sn">Reserve Inventory</span><span class="sd">compensate: Cancel Order</span></div>
  <div class="stk"><span class="si">3</span><span class="sn">Process Payment</span><span class="sd">compensate: Release Inventory → Cancel Order</span></div>
  <div class="stk"><span class="si">4</span><span class="sn">Arrange Shipping</span><span class="sd">compensate: Refund Payment → Release Inventory → Cancel Order</span></div>
  <div class="stk hl"><span class="si">5</span><span class="sn">Confirm Order</span><span class="sd">✓ success</span></div>
</div>
<div class="ar-d" style="margin:8px 0">↓ failure at step 3 triggers compensation chain ↓</div>
<div class="frow" style="gap:6px;flex-wrap:wrap">
  <div class="node soft" style="min-width:120px"><div class="nt">Cancel Order</div></div>
  <span class="ar">→</span>
  <div class="node soft" style="min-width:140px"><div class="nt">Release Inventory</div></div>
  <span class="ar">→</span>
  <div class="node soft" style="min-width:120px"><div class="nt">Refund Payment</div></div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">eventual consistency · non-blocking</span>
  <span class="chip">loose coupling · microservices</span>
</div>
<div class="fignote">No distributed locks — each step is a local transaction; failures trigger backward-running compensations.</div></div>
"""

# ---- Kafka topic / partitions / consumer groups ----
D["71a0a41497dc"] = r"""
<div class="fig"><div class="figcap">Kafka · Topic → Partitions → Consumer Groups</div>
<div class="tiers">
  <div class="tier">
    <div class="th">PRODUCERS</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">Producer A</div><div class="ns">key=userId%3</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">TOPIC: user-events</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Partition 0</div><div class="ns">Leader: Broker1 · Replica: Broker2</div></div>
      <div class="node acc"><div class="nt">Partition 1</div><div class="ns">Leader: Broker2 · Replica: Broker3</div></div>
      <div class="node acc"><div class="nt">Partition 2</div><div class="ns">Leader: Broker3 · Replica: Broker1</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">CONSUMER GROUPS</div>
    <div class="fcol">
      <div class="node soft"><div class="nt">analytics</div><div class="ns">X→P0 · Y→P1 · Z→P2</div></div>
      <div class="node soft"><div class="nt">notifications</div><div class="ns">P→P0+P1 · Q→P2</div></div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">1 partition → 1 consumer per group</span>
  <span class="chip">multiple groups → each sees ALL msgs</span>
  <span class="chip">offset per partition</span>
</div>
<div class="fignote">Parallelism = #partitions per group. Two groups subscribe independently — fan-out at no extra cost.</div></div>
"""

# ---- Vector Clocks ----
D["2d458fc42b8a"] = r"""
<div class="fig"><div class="figcap">Vector Clocks · Causality Tracking (3 nodes)</div>
<div class="matrix" style="grid-template-columns:repeat(4,1fr);margin-bottom:10px">
  <div class="cell hd">Event</div><div class="cell hd">A[0]</div><div class="cell hd">B[1]</div><div class="cell hd">C[2]</div>
  <div class="cell">A sends→B</div><div class="cell on">1</div><div class="cell">0</div><div class="cell">0</div>
  <div class="cell">B receives</div><div class="cell on">1</div><div class="cell on">1</div><div class="cell">0</div>
  <div class="cell">B sends→C</div><div class="cell on">1</div><div class="cell on">2</div><div class="cell">0</div>
  <div class="cell">C receives</div><div class="cell on">1</div><div class="cell on">2</div><div class="cell on">1</div>
  <div class="cell">A acts</div><div class="cell on">2</div><div class="cell">0</div><div class="cell">0</div>
</div>
<div class="frow" style="gap:8px;flex-wrap:wrap;align-items:flex-start">
  <div class="callout c-key" style="flex:1;min-width:160px;padding:8px 12px">
    <div class="ch" style="font-size:10px">◆ A=[2,0,0] vs B=[1,1,0]</div>
    <p style="margin:4px 0;font-size:10px">A[0]=2 &gt; B[0]=1 but A[1]=0 &lt; B[1]=1<br/><b>→ CONCURRENT</b> (neither caused the other)</p>
  </div>
  <div class="callout c-ana" style="flex:1;min-width:160px;padding:8px 12px">
    <div class="ch" style="font-size:10px">◆ Rule: VC(e) &lt; VC(f)</div>
    <p style="margin:4px 0;font-size:10px">if every component of e's VC<br/>≤ f's VC and at least one &lt;<br/><b>→ e happened-before f</b></p>
  </div>
</div>
<div class="fignote">On receive: merge by taking max of each component, then increment own counter.</div></div>
"""

# ---- Gossip Protocol spread ----
D["073c5ac6e6c9"] = r"""
<div class="fig"><div class="figcap">Gossip Protocol · O(log N) Propagation</div>
<div class="stack">
  <div class="stk hl"><span class="si">0</span><span class="sn">Node A has new info</span><span class="sd">[A★] [B] [C] [D] [E] [F]</span></div>
  <div class="stk"><span class="si">1</span><span class="sn">A gossips to C, E</span><span class="sd">[A★] [B] [C★] [D] [E★] [F]</span></div>
  <div class="stk"><span class="si">2</span><span class="sn">C→B · E→D,F</span><span class="sd">[A★] [B★] [C★] [D★] [E★] [F★]</span></div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">O(log N) rounds</span>
  <span class="chip">no single point of failure</span>
  <span class="chip">eventual consistency</span>
  <span class="chip">fanout ≈ 2–3 per round</span>
</div>
<div class="fignote">Each round the informed set doubles — all N nodes informed in ≈ log₂(N) rounds. Used in Cassandra, Consul.</div></div>
"""

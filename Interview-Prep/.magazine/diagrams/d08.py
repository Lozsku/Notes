# Hand-built HTML diagrams for 08-databases.md  (key = md5(ascii)[:12])
D = {}

# ---- B+Tree structure (full tree with linked leaves) ----
D["d4e9bb1a6eac"] = r"""
<div class="fig"><div class="figcap">B+Tree · Root / Internal / Leaf Nodes</div>
<svg viewBox="0 0 520 230" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace;font-size:9px">
  <!-- root -->
  <rect x="195" y="8" width="130" height="28" rx="5" fill="var(--acc)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="260" y="27" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Root:  50</text>
  <!-- lines root → internal -->
  <line x1="230" y1="36" x2="115" y2="72" stroke="var(--acc)" stroke-width="1.4"/>
  <line x1="290" y1="36" x2="405" y2="72" stroke="var(--acc)" stroke-width="1.4"/>
  <!-- internal left -->
  <rect x="55" y="72" width="120" height="28" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="115" y="91" text-anchor="middle" fill="var(--acc-tx)">25 | 37</text>
  <!-- internal right -->
  <rect x="345" y="72" width="120" height="28" rx="5" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="405" y="91" text-anchor="middle" fill="var(--acc-tx)">75 | 87</text>
  <!-- lines internal left → leaves -->
  <line x1="85"  y1="100" x2="45"  y2="148" stroke="var(--acc2)" stroke-width="1.2"/>
  <line x1="115" y1="100" x2="127" y2="148" stroke="var(--acc2)" stroke-width="1.2"/>
  <line x1="145" y1="100" x2="209" y2="148" stroke="var(--acc2)" stroke-width="1.2"/>
  <!-- lines internal right → leaves -->
  <line x1="375" y1="100" x2="293" y2="148" stroke="var(--acc2)" stroke-width="1.2"/>
  <line x1="405" y1="100" x2="375" y2="148" stroke="var(--acc2)" stroke-width="1.2"/>
  <line x1="435" y1="100" x2="457" y2="148" stroke="var(--acc2)" stroke-width="1.2"/>
  <!-- leaf nodes -->
  <rect x="8"   y="148" width="74" height="28" rx="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3"/>
  <text x="45"  y="167" text-anchor="middle" fill="var(--acc-tx)">10│20</text>
  <rect x="90"  y="148" width="74" height="28" rx="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3"/>
  <text x="127" y="167" text-anchor="middle" fill="var(--acc-tx)">25│30</text>
  <rect x="172" y="148" width="74" height="28" rx="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3"/>
  <text x="209" y="167" text-anchor="middle" fill="var(--acc-tx)">37│45</text>
  <rect x="254" y="148" width="74" height="28" rx="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3"/>
  <text x="291" y="167" text-anchor="middle" fill="var(--acc-tx)">50│65</text>
  <rect x="336" y="148" width="74" height="28" rx="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3"/>
  <text x="373" y="167" text-anchor="middle" fill="var(--acc-tx)">75│80</text>
  <rect x="418" y="148" width="74" height="28" rx="4" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3"/>
  <text x="455" y="167" text-anchor="middle" fill="var(--acc-tx)">87│95</text>
  <!-- leaf links (arrows) -->
  <line x1="82"  y1="162" x2="90"  y2="162" stroke="var(--acc)" stroke-width="1.2"/>
  <polygon points="90,158 90,166 96,162" fill="var(--acc)"/>
  <line x1="164" y1="162" x2="172" y2="162" stroke="var(--acc)" stroke-width="1.2"/>
  <polygon points="172,158 172,166 178,162" fill="var(--acc)"/>
  <line x1="246" y1="162" x2="254" y2="162" stroke="var(--acc)" stroke-width="1.2"/>
  <polygon points="254,158 254,166 260,162" fill="var(--acc)"/>
  <line x1="328" y1="162" x2="336" y2="162" stroke="var(--acc)" stroke-width="1.2"/>
  <polygon points="336,158 336,166 342,162" fill="var(--acc)"/>
  <line x1="410" y1="162" x2="418" y2="162" stroke="var(--acc)" stroke-width="1.2"/>
  <polygon points="418,158 418,166 424,162" fill="var(--acc)"/>
  <!-- labels -->
  <text x="260" y="56" text-anchor="middle" fill="var(--acc-tx)" font-size="8" opacity=".7">internal nodes = routing keys only</text>
  <text x="260" y="213" text-anchor="middle" fill="var(--acc-tx)" font-size="8">← leaf linked list enables O(1) range scans →</text>
</svg>
<div class="fignote">All data lives in <b>leaf nodes</b>; internal nodes hold routing keys only. Leaves form a doubly-linked list → efficient range scans. Branching factor ~100 keeps tree height ≤ 4 for millions of rows.</div></div>
"""

# ---- LSM-Tree write path ----
D["a39171078f6a"] = r"""
<div class="fig"><div class="figcap">LSM-Tree · Write &amp; Compaction Path</div>
<div class="tiers" style="flex-direction:column;gap:6px">
  <div class="tier" style="flex-direction:row;align-items:center;gap:10px">
    <div class="th" style="width:90px;text-align:right">Write →</div>
    <div class="fcol" style="flex:1">
      <div class="node acc"><div class="nt">WAL (Write-Ahead Log)</div><div class="ns">sequential disk write · crash safety</div></div>
    </div>
  </div>
  <div class="ar-d">↓ buffered in memory ↓</div>
  <div class="tier" style="flex-direction:row;align-items:center;gap:10px">
    <div class="th" style="width:90px;text-align:right">Memory</div>
    <div class="fcol" style="flex:1">
      <div class="node soft"><div class="nt">MemTable</div><div class="ns">sorted key-value pairs · fast O(log n) writes</div></div>
    </div>
  </div>
  <div class="ar-d">↓ flush when full ↓</div>
  <div class="tier" style="flex-direction:row;align-items:center;gap:10px">
    <div class="th" style="width:90px;text-align:right">L0 disk</div>
    <div class="frow" style="flex:1;gap:4px;flex-wrap:nowrap">
      <div class="node"><div class="nt">SST1</div></div>
      <div class="node"><div class="nt">SST2</div></div>
      <div class="node"><div class="nt">SST3</div></div>
      <span class="chip">may overlap</span>
    </div>
  </div>
  <div class="ar-d">↓ compaction (merge-sort) ↓</div>
  <div class="tier" style="flex-direction:row;align-items:center;gap:10px">
    <div class="th" style="width:90px;text-align:right">L1 disk</div>
    <div class="fcol" style="flex:1">
      <div class="node soft"><div class="nt">SSTable — sorted, no overlap</div><div class="ns">~10 MB files · Bloom filter per file</div></div>
    </div>
  </div>
  <div class="ar-d">↓ compaction ↓</div>
  <div class="tier" style="flex-direction:row;align-items:center;gap:10px">
    <div class="th" style="width:90px;text-align:right">L2 disk</div>
    <div class="fcol" style="flex:1">
      <div class="node soft"><div class="nt">SSTable — sorted, no overlap, 10× larger</div><div class="ns">~100 MB files</div></div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">Read: MemTable → L0 → L1 → L2 …</span>
  <span class="chip">Bloom filter skips misses fast</span>
</div>
<div class="fignote">Write-optimised: all writes are sequential. Reads need Bloom filters + level checks. Used by LevelDB, RocksDB, Cassandra.</div></div>
"""

# ---- SSTable merge / compaction ----
D["f7529dd5216b"] = r"""
<div class="fig"><div class="figcap">SSTable Compaction · Merge-Sort</div>
<div class="frow sb" style="flex-wrap:nowrap;gap:8px">
  <div class="node soft"><div class="nt">File A</div><div class="ns">a=1 · c=3 · e=5</div></div>
  <div class="node soft"><div class="nt">File B</div><div class="ns">b=2 · c=4 · d=6</div></div>
</div>
<div class="ar-d">↓ merge sort (newer value wins) ↓</div>
<div class="node acc"><div class="nt">Merged Output</div><div class="ns">a=1 · b=2 · c=4 · d=6 · e=5 &nbsp;←&nbsp; c=4 wins (newer)</div></div>
<div class="fignote">During compaction SSTables are merge-sorted; for duplicate keys the newest timestamp wins. Tombstones (delete markers) are also GC'd here.</div></div>
"""

# ---- Leader-Follower / Multi-Leader / Leaderless replication ----
D["12925df4c9e7"] = r"""
<div class="fig"><div class="figcap">Replication Topologies</div>
<div class="tiers" style="gap:12px">
  <div class="tier">
    <div class="th">Leader-Follower</div>
    <div class="fcol" style="align-items:center;gap:6px">
      <div class="node acc"><div class="nt">Leader</div><div class="ns">all writes here</div></div>
      <div class="ar-d">↓ replication log ↓</div>
      <div class="frow" style="gap:8px">
        <div class="node soft"><div class="nt">Follower</div><div class="ns">reads OK</div></div>
        <div class="node soft"><div class="nt">Follower</div><div class="ns">reads OK</div></div>
      </div>
      <span class="chip">async or sync replication</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">Multi-Leader</div>
    <div class="fcol" style="align-items:center;gap:6px">
      <div class="frow" style="gap:8px;flex-wrap:nowrap">
        <div class="node acc"><div class="nt">Leader A</div><div class="ns">Region A</div></div>
        <span class="ar">⇄</span>
        <div class="node acc"><div class="nt">Leader B</div><div class="ns">Region B</div></div>
      </div>
      <span class="chip">writes at both · conflict resolution needed</span>
      <span class="chip">LWW · CRDT · custom merge</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">Leaderless</div>
    <div class="fcol" style="align-items:center;gap:6px">
      <div class="frow" style="gap:6px;flex-wrap:nowrap">
        <div class="node"><div class="nt">Node A</div></div>
        <div class="node"><div class="nt">Node B</div></div>
        <div class="node"><div class="nt">Node C</div></div>
      </div>
      <span class="chip">W+R &gt; N → quorum</span>
      <span class="chip">e.g. N=3 W=2 R=2 (sloppy quorum)</span>
    </div>
  </div>
</div>
<div class="fignote">Leader-follower: simple, single write path. Multi-leader: lower write latency across regions but conflicts. Leaderless (Dynamo): high availability, quorum reads/writes.</div></div>
"""

# ---- Sharding / Partitioning strategies ----
D["9779a23d2609"] = r"""
<div class="fig"><div class="figcap">Sharding Strategies</div>
<div class="tiers" style="gap:10px">
  <div class="tier">
    <div class="th">Range</div>
    <div class="fcol" style="gap:5px">
      <div class="node soft"><div class="nt">Shard 1</div><div class="ns">user_id 1–1 M</div></div>
      <div class="node soft"><div class="nt">Shard 2</div><div class="ns">user_id 1M–2 M</div></div>
      <div class="node soft"><div class="nt">Shard 3</div><div class="ns">user_id 2M–3 M</div></div>
      <span class="chip" style="color:var(--acc)">⚠ hot partitions possible</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">Hash % N</div>
    <div class="fcol" style="gap:5px">
      <div class="node soft"><div class="nt">hash(id) % 3 = 0</div><div class="ns">Shard 0</div></div>
      <div class="node soft"><div class="nt">hash(id) % 3 = 1</div><div class="ns">Shard 1</div></div>
      <div class="node soft"><div class="nt">hash(id) % 3 = 2</div><div class="ns">Shard 2</div></div>
      <span class="chip">even dist · range queries hit all shards</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">Consistent Hash</div>
    <div class="fcol" style="align-items:center">
      <svg viewBox="0 0 140 140" width="130" height="130" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono';font-size:8px">
        <circle cx="70" cy="70" r="55" fill="none" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="4 2"/>
        <circle cx="70" cy="15"  r="7" fill="var(--acc)" /><text x="70"  y="8"   text-anchor="middle" fill="var(--acc-tx)">A</text>
        <circle cx="125" cy="70" r="7" fill="var(--acc2)"/><text x="138" y="73"  text-anchor="middle" fill="var(--acc-tx)">B</text>
        <circle cx="70" cy="125" r="7" fill="var(--acc)" /><text x="70"  y="141" text-anchor="middle" fill="var(--acc-tx)">C</text>
        <circle cx="15" cy="70"  r="7" fill="var(--acc2)"/><text x="3"   y="73"  text-anchor="middle" fill="var(--acc-tx)">D</text>
        <text x="70" y="74" text-anchor="middle" fill="var(--acc-tx)" font-size="7">ring</text>
      </svg>
      <span class="chip">only adjacent keys move on resize</span>
    </div>
  </div>
</div>
<div class="fignote">Range: good for range queries, prone to hot spots. Hash: even load, bad for ranges. Consistent hash: minimal data movement when adding/removing nodes (used in DynamoDB, Cassandra).</div></div>
"""

# ---- Full table scan vs B+Tree index lookup ----
D["36be7edeafe8"] = r"""
<div class="fig"><div class="figcap">Full Scan vs Index Lookup</div>
<div class="frow sb" style="gap:12px;align-items:stretch">
  <div class="fcol" style="flex:1">
    <div class="node" style="margin-bottom:6px"><div class="nt">Full Table Scan</div><div class="ns">SELECT * … WHERE salary=90000</div></div>
    <div class="gantt">
      <div class="gr"><span class="gl">Read</span>
        <div class="track">
          <div class="gseg m" style="width:100%">row 1 … row N (all pages)</div>
        </div>
      </div>
    </div>
    <div class="frow" style="margin-top:6px"><span class="chip">O(N) rows · O(N) I/Os</span></div>
  </div>
  <div class="fcol" style="flex:1">
    <div class="node acc" style="margin-bottom:6px"><div class="nt">B+Tree Index Lookup</div><div class="ns">SELECT * … WHERE salary=90000</div></div>
    <div class="gantt">
      <div class="gr"><span class="gl">Level</span>
        <div class="track">
          <div class="gseg a" style="width:15%">root</div>
          <div class="gseg b" style="width:15%">int</div>
          <div class="gseg a" style="width:15%">leaf</div>
          <div class="gseg m" style="width:55%">(done)</div>
        </div>
      </div>
    </div>
    <div class="frow" style="margin-top:6px;gap:4px">
      <span class="chip">O(log N) rows · 3-4 I/Os</span>
    </div>
  </div>
</div>
<div class="fignote">Index traversal: start at root, compare keys, follow child pointer ~log₁₀₀(N) levels → leaf → row pointer. Millions of rows still need only 3-4 page reads.</div></div>
"""

# ---- Clustered vs Non-Clustered (Secondary) Index ----
D["b4d6b2364252"] = r"""
<div class="fig"><div class="figcap">Clustered vs Non-Clustered Index</div>
<div class="tiers" style="gap:12px">
  <div class="tier">
    <div class="th">Clustered (InnoDB PK)</div>
    <div class="fcol" style="gap:5px">
      <div class="node acc"><div class="nt">B+Tree Leaf = Row Data</div></div>
      <div class="node soft"><div class="nt">PK=1</div><div class="ns">name=Alice · salary=120000 · …</div></div>
      <div class="node soft"><div class="nt">PK=2</div><div class="ns">name=Bob · salary=90000 · …</div></div>
      <div class="node soft"><div class="nt">PK=3</div><div class="ns">name=… · … · …</div></div>
      <span class="chip">physically ordered by PK on disk</span>
    </div>
  </div>
  <div class="tier">
    <div class="th">Non-Clustered (Secondary)</div>
    <div class="fcol" style="gap:5px">
      <div class="node acc"><div class="nt">Index on (salary)</div></div>
      <div class="node soft"><div class="nt">salary=90000</div><div class="ns">→ row pointer (PK=2)</div></div>
      <div class="node soft"><div class="nt">salary=120000</div><div class="ns">→ row pointer (PK=1)</div></div>
      <div class="ar-d">↓ "bookmark lookup" ↓</div>
      <div class="node"><div class="nt">Clustered index lookup (PK)</div><div class="ns">second B+Tree traversal for full row</div></div>
    </div>
  </div>
</div>
<div class="fignote">Clustered index stores the actual rows at leaf level (one per table). Secondary indexes store only the PK → require a second lookup ("key lookup") to fetch remaining columns.</div></div>
"""

# ---- Isolation levels × anomaly matrix ----
D["e7f40057b2e4"] = r"""
<div class="fig"><div class="figcap">Transaction Isolation Levels × Anomalies</div>
<div class="matrix" style="grid-template-columns:repeat(5,1fr)">
  <div class="cell hd">Level</div>
  <div class="cell hd">Dirty Read</div>
  <div class="cell hd">Non-Rep. Read</div>
  <div class="cell hd">Phantom Read</div>
  <div class="cell hd">Lost Update</div>

  <div class="cell hd">Read Uncommitted</div>
  <div class="cell on">possible</div>
  <div class="cell on">possible</div>
  <div class="cell on">possible</div>
  <div class="cell on">possible</div>

  <div class="cell hd">Read Committed</div>
  <div class="cell">✓ prevented</div>
  <div class="cell on">possible</div>
  <div class="cell on">possible</div>
  <div class="cell on">possible</div>

  <div class="cell hd">Repeatable Read</div>
  <div class="cell">✓</div>
  <div class="cell">✓</div>
  <div class="cell on">possible</div>
  <div class="cell">✓</div>

  <div class="cell hd">Serializable</div>
  <div class="cell">✓</div>
  <div class="cell">✓</div>
  <div class="cell">✓</div>
  <div class="cell">✓</div>
</div>
<div class="frow" style="margin-top:8px;gap:6px">
  <span class="chip">Dirty Read: T1 reads uncommitted T2 data that gets rolled back</span>
</div>
<div class="fignote">Higher isolation = fewer anomalies but more contention. PostgreSQL default: Read Committed. MySQL InnoDB default: Repeatable Read (also prevents phantoms via gap locks).</div></div>
"""

# ---- MVCC (Multi-Version Concurrency Control) ----
D["d6b92544bc8e"] = r"""
<div class="fig"><div class="figcap">MVCC · Multi-Version Concurrency Control (PostgreSQL)</div>
<div class="fcol" style="gap:8px">
  <div class="node soft"><div class="nt">INSERT (tx 100)</div><div class="ns">row { xmin=100, xmax=NULL, data="Alice, 90000" }</div></div>
  <div class="ar-d">↓ UPDATE by tx 200 ↓</div>
  <div class="frow sb" style="gap:10px">
    <div class="node" style="flex:1"><div class="nt">Old version (visible to tx &lt; 200)</div><div class="ns">xmin=100 · xmax=200 · data="Alice, 90000"</div></div>
    <div class="node acc" style="flex:1"><div class="nt">New version (visible to tx ≥ 200)</div><div class="ns">xmin=200 · xmax=NULL · data="Alice, 100000"</div></div>
  </div>
  <div class="frow sb" style="gap:10px;margin-top:4px">
    <div class="node soft" style="flex:1"><div class="nt">Tx 150 (started before tx 200)</div><div class="ns">sees old row: xmin=100 &lt; 150, xmax=200 &gt; 150 ✓</div></div>
    <div class="node soft" style="flex:1"><div class="nt">Tx 250 (started after tx 200)</div><div class="ns">sees new row: xmin=200 &lt; 250 ✓</div></div>
  </div>
</div>
<div class="fignote">MVCC keeps multiple row versions — readers never block writers and vice-versa. Old versions are vacuumed (GC'd) once no active snapshot references them.</div></div>
"""

# ---- SQL JOIN types (visual + results) ----
D["74300edd1749"] = r"""
<div class="fig"><div class="figcap">SQL JOIN Types · employees ⟕ departments</div>
<div class="matrix" style="grid-template-columns:repeat(4,1fr)">
  <div class="cell hd">JOIN type</div>
  <div class="cell hd">Alice (dept 10 ✓)</div>
  <div class="cell hd">Charlie (dept 30 ✗)</div>
  <div class="cell hd">HR (no employee)</div>

  <div class="cell hd">INNER JOIN</div>
  <div class="cell on">✓ included</div>
  <div class="cell">✗ excluded</div>
  <div class="cell">✗ excluded</div>

  <div class="cell hd">LEFT JOIN</div>
  <div class="cell on">✓ included</div>
  <div class="cell on">✓ dept=NULL</div>
  <div class="cell">✗ excluded</div>

  <div class="cell hd">RIGHT JOIN</div>
  <div class="cell on">✓ included</div>
  <div class="cell">✗ excluded</div>
  <div class="cell on">✓ name=NULL</div>

  <div class="cell hd">FULL OUTER</div>
  <div class="cell on">✓ included</div>
  <div class="cell on">✓ dept=NULL</div>
  <div class="cell on">✓ name=NULL</div>
</div>
<svg viewBox="0 0 360 80" xmlns="http://www.w3.org/2000/svg" style="font-family:'Space Grotesk';font-size:9px;margin-top:8px">
  <!-- INNER -->
  <circle cx="35"  cy="36" r="24" fill="var(--acc-bg)" stroke="var(--acc)"  stroke-width="1.3" opacity=".7"/>
  <circle cx="57"  cy="36" r="24" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3" opacity=".7"/>
  <text x="46" y="40" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">INNER</text>
  <text x="46" y="68" text-anchor="middle" fill="var(--acc-tx)">overlap only</text>
  <!-- LEFT -->
  <circle cx="123" cy="36" r="24" fill="var(--acc)" stroke="var(--acc)"  stroke-width="1.3" opacity=".85"/>
  <circle cx="145" cy="36" r="24" fill="var(--acc-bg)" stroke="var(--acc2)" stroke-width="1.3" opacity=".5"/>
  <text x="123" y="40" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">LEFT</text>
  <text x="134" y="68" text-anchor="middle" fill="var(--acc-tx)">all left side</text>
  <!-- RIGHT -->
  <circle cx="211" cy="36" r="24" fill="var(--acc-bg)" stroke="var(--acc)"  stroke-width="1.3" opacity=".5"/>
  <circle cx="233" cy="36" r="24" fill="var(--acc2)" stroke="var(--acc2)" stroke-width="1.3" opacity=".85"/>
  <text x="233" y="40" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">RIGHT</text>
  <text x="222" y="68" text-anchor="middle" fill="var(--acc-tx)">all right side</text>
  <!-- FULL -->
  <circle cx="299" cy="36" r="24" fill="var(--acc)" stroke="var(--acc)"  stroke-width="1.3" opacity=".75"/>
  <circle cx="321" cy="36" r="24" fill="var(--acc2)" stroke="var(--acc2)" stroke-width="1.3" opacity=".75"/>
  <text x="310" y="40" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">FULL</text>
  <text x="310" y="68" text-anchor="middle" fill="var(--acc-tx)">everything</text>
</svg>
<div class="fignote">INNER = intersection; LEFT = all from left table + matched right (NULL if no match); RIGHT = mirror; FULL OUTER = union of both sides.</div></div>
"""

# ---- CAP Theorem ----
D["7e1b8c27dde9"] = r"""
<div class="fig"><div class="figcap">CAP Theorem · Real-World Choices</div>
<svg viewBox="0 0 340 190" xmlns="http://www.w3.org/2000/svg" style="font-family:'Space Grotesk';font-size:9.5px">
  <!-- triangle -->
  <polygon points="170,12 30,170 310,170" fill="none" stroke="var(--acc)" stroke-width="1.8"/>
  <!-- vertices -->
  <circle cx="170" cy="12"  r="16" fill="var(--acc)"/>
  <circle cx="30"  cy="170" r="16" fill="var(--acc2)"/>
  <circle cx="310" cy="170" r="16" fill="var(--acc2)"/>
  <text x="170" y="16"  text-anchor="middle" fill="var(--acc-tx)" font-weight="bold" font-size="9">C</text>
  <text x="30"  y="174" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold" font-size="9">A</text>
  <text x="310" y="174" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold" font-size="9">P</text>
  <!-- vertex labels -->
  <text x="170" y="5"   text-anchor="middle" fill="var(--acc-tx)" font-size="8" opacity=".8">Consistency</text>
  <text x="8"   y="164" text-anchor="start"  fill="var(--acc-tx)" font-size="8" opacity=".8">Availability</text>
  <text x="295" y="186" text-anchor="middle" fill="var(--acc-tx)" font-size="8" opacity=".8">Partition-tol.</text>
  <!-- sides labelled -->
  <text x="90"  y="86"  text-anchor="middle" fill="var(--acc-tx)" font-size="8.5" transform="rotate(-60 90 86)">CP: HBase · Zookeeper · Spanner</text>
  <text x="250" y="86"  text-anchor="middle" fill="var(--acc-tx)" font-size="8.5" transform="rotate(60 250 86)">AP: Cassandra · DynamoDB · CouchDB</text>
  <text x="170" y="182" text-anchor="middle" fill="var(--acc-tx)" font-size="8.5">CA: Traditional single-node RDBMS</text>
</svg>
<div class="fignote">In a distributed system you can only guarantee <b>two</b> of the three. CP sacrifices availability during partitions; AP may return stale data. CA is impossible if partitions can occur.</div></div>
"""

# ---- Window Functions output ----
D["fda65094cae9"] = r"""
<div class="fig"><div class="figcap">Window Functions · RANK, LAG, LEAD, SUM OVER</div>
<div class="matrix" style="grid-template-columns:repeat(6,1fr);font-size:11px">
  <div class="cell hd">name</div>
  <div class="cell hd">salary</div>
  <div class="cell hd">dept_rank</div>
  <div class="cell hd">dense_rank</div>
  <div class="cell hd">prev_sal (LAG)</div>
  <div class="cell hd">running_total</div>

  <div class="cell on">Alice</div>
  <div class="cell">120000</div>
  <div class="cell">1</div>
  <div class="cell">1</div>
  <div class="cell">NULL</div>
  <div class="cell">120000</div>

  <div class="cell">Bob</div>
  <div class="cell">90000</div>
  <div class="cell">2</div>
  <div class="cell">2</div>
  <div class="cell">120000</div>
  <div class="cell">210000</div>

  <div class="cell">Charlie</div>
  <div class="cell">90000</div>
  <div class="cell">2</div>
  <div class="cell">2</div>
  <div class="cell">90000</div>
  <div class="cell">300000</div>

  <div class="cell">Dave</div>
  <div class="cell">80000</div>
  <div class="cell">1</div>
  <div class="cell">1</div>
  <div class="cell">NULL</div>
  <div class="cell">380000</div>
</div>
<div class="frow" style="margin-top:6px;gap:6px;flex-wrap:wrap">
  <span class="chip">RANK skips numbers on ties</span>
  <span class="chip">DENSE_RANK does not skip</span>
  <span class="chip">LAG/LEAD look at prev/next row</span>
  <span class="chip">SUM OVER = running total</span>
</div>
<div class="fignote">Window functions compute over a "window" of related rows without collapsing them (unlike GROUP BY). Bob &amp; Charlie both rank=2, but Dave is rank=1 within dept 20.</div></div>
"""

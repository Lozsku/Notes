# Hand-built HTML diagrams for 02-operating-systems.md  (key = md5(ascii)[:12])
D = {}

# ---- Process memory layout (stack/heap/bss/data/text) ----
D["6250150c8a54"] = r"""
<div class="fig"><div class="figcap">Process Address Space · Memory Layout</div>
<div class="stack">
  <div class="stk hl"><span class="sn">Stack</span><span class="sd">local variables · return addresses · grows ↓ (high address)</span></div>
  <div class="stk"><span class="sn">(free space)</span><span class="sd">← stack grows down &nbsp;|&nbsp; heap grows up →</span></div>
  <div class="stk hl"><span class="sn">Heap</span><span class="sd">malloc'd memory · grows ↑</span></div>
  <div class="stk"><span class="sn">BSS</span><span class="sd">uninitialized global / static variables (zero-filled)</span></div>
  <div class="stk"><span class="sn">Data</span><span class="sd">initialized global / static variables</span></div>
  <div class="stk"><span class="sn">Text</span><span class="sd">executable code · read-only · low address (0x400000)</span></div>
</div>
<div class="fignote">Stack and Heap grow toward each other; collision = stack overflow / OOM. Text segment is shared between threads.</div></div>
"""

# ---- Process with 3 threads ----
D["6eed2db9c1d2"] = r"""
<div class="fig"><div class="figcap">Threads · Shared vs. Private Memory</div>
<div class="tiers">
  <div class="tier" style="flex:3">
    <div class="th">SHARED (all threads)</div>
    <div class="fcol">
      <div class="node acc"><div class="nt">Code (Text)</div></div>
      <div class="node acc"><div class="nt">Heap &amp; Global Data</div></div>
      <div class="node acc"><div class="nt">File Descriptors</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">Stack T1</div>
    <div class="fcol"><div class="node soft"><div class="nt">Thread 1</div><div class="ns">private stack</div></div></div>
  </div>
  <div class="tier">
    <div class="th">Stack T2</div>
    <div class="fcol"><div class="node soft"><div class="nt">Thread 2</div><div class="ns">private stack</div></div></div>
  </div>
  <div class="tier">
    <div class="th">Stack T3</div>
    <div class="fcol"><div class="node soft"><div class="nt">Thread 3</div><div class="ns">private stack</div></div></div>
  </div>
</div>
<div class="fignote">Threads share the same virtual address space — fast to create/switch, but race conditions require synchronization.</div></div>
"""

# ---- Process state machine ----
D["128c2a82d058"] = r"""
<div class="fig"><div class="figcap">Process State Machine · 5 States</div>
<svg viewBox="0 0 520 220" style="font-family:'Space Grotesk',sans-serif;font-size:10px">
  <!-- NEW -->
  <rect x="10" y="90" width="80" height="36" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="50" y="113" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">NEW</text>
  <!-- READY -->
  <rect x="140" y="90" width="80" height="36" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="180" y="113" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">READY</text>
  <!-- RUNNING -->
  <rect x="280" y="90" width="90" height="36" rx="8" fill="var(--acc)" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="325" y="113" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold" font-size="11">RUNNING</text>
  <!-- WAITING -->
  <rect x="280" y="170" width="90" height="34" rx="8" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="325" y="191" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">WAITING</text>
  <!-- TERMINATED -->
  <rect x="420" y="90" width="90" height="36" rx="8" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="465" y="108" text-anchor="middle" fill="var(--acc-tx)" font-size="9" font-weight="bold">TERMINATED</text>
  <!-- arrows -->
  <!-- NEW→READY -->
  <line x1="90" y1="108" x2="138" y2="108" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="114" y="102" text-anchor="middle" fill="var(--acc-tx)" font-size="8">admitted</text>
  <!-- READY→RUNNING -->
  <line x1="220" y1="108" x2="278" y2="108" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="249" y="102" text-anchor="middle" fill="var(--acc-tx)" font-size="8">dispatch</text>
  <!-- RUNNING→READY (interrupt) -->
  <path d="M325,90 C325,60 180,60 180,90" fill="none" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="253" y="56" text-anchor="middle" fill="var(--acc-tx)" font-size="8">interrupt / quantum expired</text>
  <!-- RUNNING→WAITING -->
  <line x1="325" y1="126" x2="325" y2="168" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="345" y="150" fill="var(--acc-tx)" font-size="8">I/O req</text>
  <!-- WAITING→READY -->
  <path d="M280,187 C230,187 180,150 180,127" fill="none" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="218" y="175" text-anchor="middle" fill="var(--acc-tx)" font-size="8">I/O done</text>
  <!-- RUNNING→TERMINATED -->
  <line x1="370" y1="108" x2="418" y2="108" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr)"/>
  <text x="394" y="102" text-anchor="middle" fill="var(--acc-tx)" font-size="8">exit()</text>
  <!-- arrowhead marker -->
  <defs>
    <marker id="arr" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 Z" fill="var(--acc)"/>
    </marker>
  </defs>
</svg>
<div class="fignote">fork() creates NEW; scheduler moves READY→RUNNING; I/O blocks to WAITING; quantum expiry preempts back to READY.</div></div>
"""

# ---- Context switch ----
D["adc50622e93b"] = r"""
<div class="fig"><div class="figcap">Context Switch · Save A, Load B</div>
<div class="frow" style="flex-wrap:nowrap;align-items:flex-start;gap:10px">
  <div class="node acc" style="min-width:90px"><div class="nt">CPU running A</div></div>
  <div class="ar-d" style="writing-mode:horizontal-tb;margin-top:12px">↓</div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node"><div class="nt">① Save A's PCB</div><div class="ns">registers · PC · SP · page-table base</div></div>
    <div class="ar-d">↓</div>
    <div class="node"><div class="nt">② Run Scheduler</div><div class="ns">pick next process B</div></div>
    <div class="ar-d">↓</div>
    <div class="node"><div class="nt">③ Load B's PCB</div><div class="ns">restore registers · PC · switch page tables · flush TLB</div></div>
  </div>
  <div class="ar-d" style="writing-mode:horizontal-tb;margin-top:12px">↓</div>
  <div class="node acc" style="min-width:90px"><div class="nt">CPU running B</div></div>
</div>
<div class="frow" style="margin-top:8px"><span class="chip">TLB flush = expensive! avoidable with ASID tags</span></div>
<div class="fignote">Context switch = pure overhead. Triggered by timer interrupt, system call, or blocking I/O. PCB holds all state.</div></div>
"""

# ---- Scheduling Gantt (FCFS / SJF / Round Robin comparison) ----
D["7ed6e863c1ee"] = r"""
<div class="fig"><div class="figcap">CPU Scheduling · FCFS vs SJF vs Round Robin (quantum=3)</div>
<div class="gantt">
  <div class="gr">
    <span class="gl">FCFS</span>
    <div class="track">
      <div class="gseg a" style="width:58.8%">P1 (0–10)</div>
      <div class="gseg b" style="width:29.4%">P2 (10–15)</div>
      <div class="gseg m" style="width:11.8%">P3 (15–17)</div>
    </div>
  </div>
  <div class="gr">
    <span class="gl">SJF</span>
    <div class="track">
      <div class="gseg m" style="width:17.6%">P3 (0–3)</div>
      <div class="gseg b" style="width:29.4%">P2 (3–8)</div>
      <div class="gseg a" style="width:52.9%">P1 (8–17)</div>
    </div>
  </div>
  <div class="gr">
    <span class="gl">RR q=3</span>
    <div class="track">
      <div class="gseg a" style="width:17.6%">P1 0–3</div>
      <div class="gseg b" style="width:17.6%">P2 3–6</div>
      <div class="gseg m" style="width:17.6%">P3 6–9</div>
      <div class="gseg a" style="width:17.6%">P1 9–12</div>
      <div class="gseg b" style="width:11.8%">P2 12–14</div>
      <div class="gseg a" style="width:17.6%">P1 14–17</div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">FCFS avg wait = 8.33</span>
  <span class="chip">SJF avg wait = 3.67 ✓ optimal</span>
  <span class="chip">RR = fair, lower response time</span>
</div>
<div class="fignote">SJF minimizes avg waiting time but requires knowing burst lengths. RR ensures no starvation. FCFS is simple but convoy-prone.</div></div>
"""

# ---- Virtual → Physical address translation (page table) ----
D["b78a76d78f9a"] = r"""
<div class="fig"><div class="figcap">Virtual → Physical Address Translation (32-bit, 4 KB pages)</div>
<div class="frow" style="flex-wrap:nowrap;align-items:center;gap:0">
  <div class="fcol" style="gap:2px;align-items:center">
    <div class="chip" style="font-size:11px">Virtual Address</div>
    <div class="frow" style="flex-wrap:nowrap;gap:1px;margin-top:4px">
      <div class="node acc" style="width:110px;text-align:center"><div class="nt" style="font-size:10px">VPN (20 bits)</div></div>
      <div class="node soft" style="width:80px;text-align:center"><div class="nt" style="font-size:10px">Offset (12 bits)</div></div>
    </div>
  </div>
</div>
<div class="frow" style="flex-wrap:nowrap;justify-content:center;gap:60px;margin:8px 0">
  <div class="ar-d">↓ page table lookup</div>
  <div style="padding-top:16px;color:var(--acc);font-size:18px">↓</div>
</div>
<div class="frow" style="flex-wrap:nowrap;align-items:center;gap:6px;justify-content:center">
  <div class="node acc" style="width:130px;text-align:center"><div class="nt">PFN (Physical Frame #)</div></div>
  <span style="font-size:20px;color:var(--acc)">+</span>
  <div class="node soft" style="width:100px;text-align:center"><div class="nt">Offset (12 bits)</div><div class="ns">unchanged</div></div>
  <span class="ar">→</span>
  <div class="node" style="width:120px;text-align:center"><div class="nt">Physical Address</div><div class="ns">PFN × 4096 + offset</div></div>
</div>
<div class="fignote">The 12-bit offset indexes within the 4 KB page. The OS page table maps VPN → PFN; TLB caches recent translations.</div></div>
"""

# ---- TLB hit / miss ----
D["14e8d07ede6d"] = r"""
<div class="fig"><div class="figcap">TLB · Translation Look-aside Buffer</div>
<div class="frow" style="flex-wrap:nowrap;align-items:flex-start;gap:12px">
  <div class="node acc" style="min-width:110px"><div class="nt">Virtual Address</div></div>
  <span class="ar" style="margin-top:14px">→</span>
  <div class="node" style="min-width:80px"><div class="nt">TLB</div><div class="ns">small fast cache</div></div>
</div>
<div class="frow sb" style="margin-top:10px;flex-wrap:nowrap;gap:16px;align-items:flex-start">
  <div class="fcol" style="align-items:center;gap:6px;flex:1">
    <span class="chip">HIT (~1 cycle)</span>
    <div class="ar-d">↓</div>
    <div class="node soft"><div class="nt">Physical Address</div><div class="ns">direct from TLB</div></div>
  </div>
  <div class="fcol" style="align-items:center;gap:6px;flex:1">
    <span class="chip">MISS (~100 cycles)</span>
    <div class="ar-d">↓</div>
    <div class="node"><div class="nt">Walk Page Tables</div><div class="ns">3–4 memory accesses</div></div>
    <div class="ar-d">↓</div>
    <div class="node soft"><div class="nt">Physical Address</div><div class="ns">+ update TLB entry</div></div>
  </div>
</div>
<div class="frow" style="margin-top:8px"><span class="chip">TLB miss on context switch → TLB flush or ASID tag</span></div>
<div class="fignote">TLB exploits locality: most programs reuse the same pages repeatedly. Hit rate &gt;99% gives near-hardware-speed translation.</div></div>
"""

# ---- Page fault handler flow ----
D["394a18b70432"] = r"""
<div class="fig"><div class="figcap">Page Fault Handler · Decision Flow</div>
<div class="fcol" style="gap:6px;align-items:center">
  <div class="node acc"><div class="nt">CPU: access VA 0x40001000</div></div>
  <div class="ar-d">↓ TLB miss → walk page table → Present bit = 0</div>
  <div class="node"><div class="nt">Hardware raises Page Fault exception</div></div>
  <div class="ar-d">↓ OS page fault handler runs</div>
  <div class="frow sb" style="flex-wrap:nowrap;gap:10px;width:100%">
    <div class="fcol" style="align-items:center;gap:4px;flex:1">
      <span class="chip">Address invalid?</span>
      <div class="ar-d">↓</div>
      <div class="node" style="border-color:var(--acc)"><div class="nt">SIGSEGV</div><div class="ns">process killed</div></div>
    </div>
    <div class="fcol" style="align-items:center;gap:4px;flex:1">
      <span class="chip">Minor fault</span>
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Set up PTE</div><div class="ns">no disk I/O needed → retry</div></div>
    </div>
    <div class="fcol" style="align-items:center;gap:4px;flex:1">
      <span class="chip">Major fault</span>
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Load from disk</div><div class="ns">alloc frame → read → set PTE → retry</div></div>
    </div>
    <div class="fcol" style="align-items:center;gap:4px;flex:1">
      <span class="chip">CoW fault</span>
      <div class="ar-d">↓</div>
      <div class="node soft"><div class="nt">Copy page</div><div class="ns">new private copy → update PTE → retry</div></div>
    </div>
  </div>
</div>
<div class="fignote">Page faults enable demand-paging, memory-mapped files, and copy-on-write. The faulting instruction is retried after the OS handles it.</div></div>
"""

# ---- Full address translation (TLB + page walk) ----
D["aa0145feded6"] = r"""
<div class="fig"><div class="figcap">Full Address Translation · TLB + Page Table Walk</div>
<svg viewBox="0 0 520 300" style="font-family:'Space Grotesk',sans-serif;font-size:10px">
  <defs>
    <marker id="a2" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 Z" fill="var(--acc)"/>
    </marker>
  </defs>
  <!-- VA box -->
  <rect x="10" y="10" width="140" height="34" rx="6" fill="var(--acc)" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="80" y="30" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Virtual Address</text>
  <text x="80" y="42" text-anchor="middle" fill="var(--acc-tx)" font-size="9">VPN | Offset</text>
  <!-- arrow to TLB -->
  <line x1="150" y1="27" x2="195" y2="27" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#a2)"/>
  <!-- TLB -->
  <rect x="196" y="10" width="110" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="251" y="30" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">TLB</text>
  <text x="251" y="42" text-anchor="middle" fill="var(--acc-tx)" font-size="9">small fast cache</text>
  <!-- HIT branch -->
  <line x1="306" y1="27" x2="370" y2="27" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#a2)"/>
  <text x="338" y="22" text-anchor="middle" fill="var(--acc-tx)" font-size="9">HIT</text>
  <rect x="371" y="10" width="100" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="421" y="30" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">PFN → Phys</text>
  <text x="421" y="42" text-anchor="middle" fill="var(--acc-tx)" font-size="9">~1 cycle</text>
  <!-- MISS branch down -->
  <line x1="251" y1="44" x2="251" y2="88" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#a2)"/>
  <text x="265" y="70" fill="var(--acc-tx)" font-size="9">MISS</text>
  <!-- Walk page tables -->
  <rect x="170" y="90" width="160" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="250" y="110" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Walk Page Tables</text>
  <text x="250" y="121" text-anchor="middle" fill="var(--acc-tx)" font-size="9">3–4 memory accesses</text>
  <!-- fork: valid vs not valid -->
  <line x1="250" y1="124" x2="250" y2="155" stroke="var(--acc)" stroke-width="1.5"/>
  <line x1="140" y1="155" x2="370" y2="155" stroke="var(--acc)" stroke-width="1"/>
  <!-- valid -->
  <line x1="175" y1="155" x2="175" y2="185" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#a2)"/>
  <text x="175" y="150" text-anchor="middle" fill="var(--acc-tx)" font-size="9">valid</text>
  <rect x="100" y="186" width="150" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <text x="175" y="206" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">PFN found</text>
  <text x="175" y="217" text-anchor="middle" fill="var(--acc-tx)" font-size="9">update TLB → physical addr</text>
  <!-- not valid -->
  <line x1="355" y1="155" x2="355" y2="185" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#a2)"/>
  <text x="355" y="150" text-anchor="middle" fill="var(--acc-tx)" font-size="9">not valid</text>
  <rect x="280" y="186" width="150" height="34" rx="6" fill="var(--acc-bg)" stroke="var(--acc-bd)" stroke-width="1.5"/>
  <text x="355" y="206" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Page Fault!</text>
  <text x="355" y="217" text-anchor="middle" fill="var(--acc-tx)" font-size="9">OS: load from disk / SIGSEGV</text>
  <!-- final phys addr -->
  <line x1="175" y1="220" x2="175" y2="256" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#a2)"/>
  <rect x="60" y="258" width="250" height="34" rx="6" fill="var(--acc)" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="185" y="278" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Physical Address = PFN × pagesize + offset</text>
  <text x="185" y="289" text-anchor="middle" fill="var(--acc-tx)" font-size="9">Access RAM</text>
</svg>
<div class="fignote">Every memory access goes through this pipeline. TLB hit skips the page-table walk entirely — crucial for performance.</div></div>
"""

# ---- 4-level page table (x86-64) ----
D["f985ef4fe4a6"] = r"""
<div class="fig"><div class="figcap">x86-64 · 4-Level Page Table Walk (48-bit VA)</div>
<div class="frow" style="flex-wrap:nowrap;gap:1px;margin-bottom:10px;justify-content:center">
  <div class="node acc" style="width:72px;text-align:center"><div class="nt" style="font-size:9px">PML4 idx</div><div class="ns">9 bits</div></div>
  <div class="node acc" style="width:72px;text-align:center"><div class="nt" style="font-size:9px">PDP idx</div><div class="ns">9 bits</div></div>
  <div class="node acc" style="width:72px;text-align:center"><div class="nt" style="font-size:9px">PD idx</div><div class="ns">9 bits</div></div>
  <div class="node acc" style="width:72px;text-align:center"><div class="nt" style="font-size:9px">PT idx</div><div class="ns">9 bits</div></div>
  <div class="node soft" style="width:88px;text-align:center"><div class="nt" style="font-size:9px">Offset</div><div class="ns">12 bits</div></div>
</div>
<div class="frow" style="flex-wrap:nowrap;align-items:center;gap:4px;justify-content:center">
  <div class="node"><div class="nt">CR3</div><div class="ns">page dir base</div></div>
  <span class="ar">→</span>
  <div class="node soft"><div class="nt">PML4[i]</div></div>
  <span class="ar">→</span>
  <div class="node soft"><div class="nt">PDP[i]</div></div>
  <span class="ar">→</span>
  <div class="node soft"><div class="nt">PD[i]</div></div>
  <span class="ar">→</span>
  <div class="node soft"><div class="nt">PT[i]</div></div>
  <span class="ar">→</span>
  <div class="node acc"><div class="nt">PFN + Offset</div><div class="ns">physical addr</div></div>
</div>
<div class="frow" style="margin-top:8px;gap:8px">
  <span class="chip">9+9+9+9+12 = 48 bits</span>
  <span class="chip">each table = 512 entries × 8B = 4 KB page</span>
  <span class="chip">CR3 loaded on context switch</span>
</div>
<div class="fignote">4 memory accesses per TLB miss. Huge pages (2MB/1GB) collapse levels and reduce TLB pressure.</div></div>
"""

# ---- Inode structure ----
D["3d5cc5509047"] = r"""
<div class="fig"><div class="figcap">Inode · File Metadata Structure</div>
<div class="frow" style="flex-wrap:nowrap;gap:12px;align-items:flex-start">
  <div class="fcol" style="flex:1;gap:4px">
    <div class="node acc"><div class="nt">Inode #47</div></div>
    <div class="matrix" style="grid-template-columns:auto 1fr;margin-top:4px">
      <div class="cell hd">Field</div><div class="cell hd">Value</div>
      <div class="cell">Type</div><div class="cell">regular file</div>
      <div class="cell">Permissions</div><div class="cell">rw-r--r--</div>
      <div class="cell">Owner</div><div class="cell">uid=1000 gid=1000</div>
      <div class="cell">Size</div><div class="cell">4096 bytes</div>
      <div class="cell">Link count</div><div class="cell">2</div>
      <div class="cell">Timestamps</div><div class="cell">atime / mtime / ctime</div>
    </div>
  </div>
  <div class="fcol" style="flex:1;gap:4px">
    <div class="node"><div class="nt">Block Pointers</div></div>
    <div class="stack" style="margin-top:4px">
      <div class="stk hl"><span class="sn">Direct [12]</span><span class="sd">→ data blocks 101, 102 … (48 KB max)</span></div>
      <div class="stk"><span class="sn">Single Indirect</span><span class="sd">→ block 200 → 1024 pointers (4 MB)</span></div>
      <div class="stk"><span class="sn">Double Indirect</span><span class="sd">→ block 300 → 1024² ptrs (4 GB)</span></div>
      <div class="stk"><span class="sn">Triple Indirect</span><span class="sd">→ 1024³ ptrs (4 TB)</span></div>
    </div>
  </div>
</div>
<div class="fignote">Inode does NOT store the filename — that lives in the directory entry. Hard links point multiple names at the same inode.</div></div>
"""

# ---- Deadlock (circular wait) ----
D["065741e2202c"] = r"""
<div class="fig"><div class="figcap">Deadlock · Circular Wait (Resource Cycle)</div>
<svg viewBox="0 0 520 180" style="font-family:'Space Grotesk',sans-serif;font-size:11px">
  <defs>
    <marker id="ad" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 Z" fill="var(--acc)"/>
    </marker>
    <marker id="adw" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto">
      <path d="M0,0 L0,6 L6,3 Z" fill="var(--acc-d)"/>
    </marker>
  </defs>
  <!-- Process A -->
  <ellipse cx="130" cy="90" rx="80" ry="30" fill="var(--acc)" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="130" y="88" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Process A</text>
  <text x="130" y="102" text-anchor="middle" fill="var(--acc-tx)" font-size="9">holds Lock 1</text>
  <!-- Process B -->
  <ellipse cx="390" cy="90" rx="80" ry="30" fill="var(--acc)" stroke="var(--acc-d)" stroke-width="1.5"/>
  <text x="390" y="88" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold">Process B</text>
  <text x="390" y="102" text-anchor="middle" fill="var(--acc-tx)" font-size="9">holds Lock 2</text>
  <!-- A wants Lock 2 (top arrow, left→right) -->
  <path d="M185,70 Q260,20 335,70" fill="none" stroke="var(--acc-d)" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#adw)"/>
  <text x="260" y="30" text-anchor="middle" fill="var(--acc-tx)" font-size="10">A wants Lock 2 →</text>
  <!-- B wants Lock 1 (bottom arrow, right→left) -->
  <path d="M335,110 Q260,155 185,110" fill="none" stroke="var(--acc-d)" stroke-width="2" stroke-dasharray="6,3" marker-end="url(#adw)"/>
  <text x="260" y="162" text-anchor="middle" fill="var(--acc-tx)" font-size="10">← B wants Lock 1</text>
  <!-- CIRCULAR WAIT label -->
  <text x="260" y="96" text-anchor="middle" fill="var(--acc-tx)" font-weight="bold" font-size="13">⟳ CIRCULAR WAIT</text>
</svg>
<div class="frow" style="gap:8px;margin-top:4px">
  <span class="chip">Prevention: lock ordering</span>
  <span class="chip">Detection: resource-allocation graph</span>
  <span class="chip">Recovery: kill one process</span>
</div>
<div class="fignote">Deadlock needs all 4 Coffman conditions: mutual exclusion, hold-and-wait, no preemption, circular wait. Break any one to prevent it.</div></div>
"""

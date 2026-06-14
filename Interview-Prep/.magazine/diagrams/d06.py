# Hand-built HTML diagrams for 06-low-level-design.md  (key = md5(ascii)[:12])
D = {}

# ---- UML Relationship Notation Guide ----
D["a71d50ceec6d"] = r"""
<div class="fig"><div class="figcap">UML Relationship Notation · Quick Reference</div>
<div class="matrix" style="grid-template-columns:1fr 2fr 2fr">
  <div class="cell hd">Relationship</div><div class="cell hd">Notation</div><div class="cell hd">Meaning</div>
  <div class="cell on">Association</div>
  <div class="cell">
    <svg viewBox="0 0 120 24" height="24" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="12" x2="104" y2="12" stroke="var(--acc)" stroke-width="1.8"/>
      <polygon points="104,12 96,7 96,17" fill="var(--acc)"/>
      <text x="4" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">A</text>
      <text x="110" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">B</text>
    </svg>
  </div>
  <div class="cell">A uses / knows B</div>

  <div class="cell on">Aggregation</div>
  <div class="cell">
    <svg viewBox="0 0 120 24" height="24" xmlns="http://www.w3.org/2000/svg">
      <line x1="22" y1="12" x2="104" y2="12" stroke="var(--acc)" stroke-width="1.8"/>
      <polygon points="104,12 96,7 96,17" fill="var(--acc)"/>
      <polygon points="8,12 16,7 22,12 16,17" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
      <text x="2" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">A</text>
      <text x="110" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">B</text>
    </svg>
  </div>
  <div class="cell">A has B (B lives independently)</div>

  <div class="cell on">Composition</div>
  <div class="cell">
    <svg viewBox="0 0 120 24" height="24" xmlns="http://www.w3.org/2000/svg">
      <line x1="22" y1="12" x2="104" y2="12" stroke="var(--acc)" stroke-width="1.8"/>
      <polygon points="104,12 96,7 96,17" fill="var(--acc)"/>
      <polygon points="8,12 16,7 22,12 16,17" fill="var(--acc)" stroke="var(--acc)" stroke-width="1.5"/>
      <text x="2" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">A</text>
      <text x="110" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">B</text>
    </svg>
  </div>
  <div class="cell">A owns B (B dies with A)</div>

  <div class="cell on">Inheritance</div>
  <div class="cell">
    <svg viewBox="0 0 120 24" height="24" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="12" x2="98" y2="12" stroke="var(--acc)" stroke-width="1.8"/>
      <polygon points="98,12 106,7 114,12 106,17" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
      <text x="2" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">A</text>
    </svg>
  </div>
  <div class="cell">A is-a B (extends / implements)</div>

  <div class="cell on">Dependency</div>
  <div class="cell">
    <svg viewBox="0 0 120 24" height="24" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="12" x2="104" y2="12" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="5,3"/>
      <polygon points="104,12 96,7 96,17" fill="var(--acc)"/>
      <text x="2" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">A</text>
      <text x="110" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">B</text>
    </svg>
  </div>
  <div class="cell">A uses B temporarily (method arg)</div>

  <div class="cell on">Realization</div>
  <div class="cell">
    <svg viewBox="0 0 120 24" height="24" xmlns="http://www.w3.org/2000/svg">
      <line x1="8" y1="12" x2="98" y2="12" stroke="var(--acc)" stroke-width="1.5" stroke-dasharray="5,3"/>
      <polygon points="98,12 106,7 114,12 106,17" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
      <text x="2" y="16" font-size="9" font-family="JetBrains Mono" fill="var(--acc-tx)">A</text>
    </svg>
  </div>
  <div class="cell">A implements interface B</div>
</div>
<div class="fignote">Filled diamond ◆ = composition (lifecycle owned); hollow ◇ = aggregation (shared); hollow triangle ▷ = inheritance/realization.</div></div>
"""

# ---- Parking Lot UML Class Diagram ----
D["72c40ea2cb1f"] = r"""
<div class="fig"><div class="figcap">Parking Lot · UML Class Diagram</div>
<svg viewBox="0 0 580 420" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace;font-size:10px">

  <!-- ParkingLot -->
  <rect x="10" y="10" width="150" height="90" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="10" y="10" width="150" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="85" y="26" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">ParkingLot</text>
  <line x1="10" y1="32" x2="160" y2="32" stroke="var(--acc)" stroke-width="1"/>
  <text x="18" y="46" fill="var(--acc-tx)">-id: int</text>
  <text x="18" y="59" fill="var(--acc-tx)">-floors: List</text>
  <line x1="10" y1="66" x2="160" y2="66" stroke="var(--acc)" stroke-width="1"/>
  <text x="18" y="80" fill="var(--acc-tx)">+getAvailSpot()</text>
  <text x="18" y="93" fill="var(--acc-tx)">+assignSpot()</text>

  <!-- Floor -->
  <rect x="250" y="10" width="150" height="90" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="250" y="10" width="150" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="325" y="26" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">Floor</text>
  <line x1="250" y1="32" x2="400" y2="32" stroke="var(--acc)" stroke-width="1"/>
  <text x="258" y="46" fill="var(--acc-tx)">-floorNo: int</text>
  <text x="258" y="59" fill="var(--acc-tx)">-spots: List</text>
  <line x1="250" y1="66" x2="400" y2="66" stroke="var(--acc)" stroke-width="1"/>

  <!-- Composition arrow ParkingLot -> Floor -->
  <line x1="160" y1="45" x2="244" y2="45" stroke="var(--acc)" stroke-width="1.5"/>
  <polygon points="244,45 236,40 236,50" fill="var(--acc)"/>
  <polygon points="160,45 168,40 174,45 168,50" fill="var(--acc)" stroke="var(--acc)" stroke-width="1"/>
  <text x="188" y="40" font-size="9" fill="var(--acc-tx)">1..*</text>

  <!-- ParkingSpot -->
  <rect x="250" y="160" width="160" height="110" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="250" y="160" width="160" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="330" y="176" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">ParkingSpot</text>
  <line x1="250" y1="182" x2="410" y2="182" stroke="var(--acc)" stroke-width="1"/>
  <text x="258" y="196" fill="var(--acc-tx)">-spotId: int</text>
  <text x="258" y="209" fill="var(--acc-tx)">-type: SpotType</text>
  <text x="258" y="222" fill="var(--acc-tx)">-isOccupied: bool</text>
  <line x1="250" y1="228" x2="410" y2="228" stroke="var(--acc)" stroke-width="1"/>
  <text x="258" y="242" fill="var(--acc-tx)">+occupy()</text>
  <text x="258" y="255" fill="var(--acc-tx)">+vacate()</text>

  <!-- Composition arrow Floor -> ParkingSpot (vertical) -->
  <line x1="325" y1="100" x2="325" y2="154" stroke="var(--acc)" stroke-width="1.5"/>
  <polygon points="325,154 320,146 330,146" fill="var(--acc)"/>
  <polygon points="325,100 320,108 325,114 330,108" fill="var(--acc)" stroke="var(--acc)" stroke-width="1"/>
  <text x="330" y="133" font-size="9" fill="var(--acc-tx)">1..*</text>

  <!-- Vehicle (abstract) -->
  <rect x="10" y="160" width="150" height="75" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="10" y="160" width="150" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="85" y="175" text-anchor="middle" font-weight="700" font-style="italic" fill="var(--acc-tx)" font-size="11">Vehicle</text>
  <line x1="10" y1="182" x2="160" y2="182" stroke="var(--acc)" stroke-width="1"/>
  <text x="18" y="196" fill="var(--acc-tx)">-licensePlate</text>
  <text x="18" y="209" fill="var(--acc-tx)">-vehicleType</text>
  <line x1="10" y1="214" x2="160" y2="214" stroke="var(--acc)" stroke-width="1"/>

  <!-- Car -->
  <rect x="10" y="300" width="80" height="36" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="10" y="300" width="80" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="50" y="316" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">Car</text>
  <line x1="10" y1="322" x2="90" y2="322" stroke="var(--acc)" stroke-width="1"/>

  <!-- Truck -->
  <rect x="105" y="300" width="80" height="36" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="105" y="300" width="80" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="145" y="316" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">Truck</text>
  <line x1="105" y1="322" x2="185" y2="322" stroke="var(--acc)" stroke-width="1"/>

  <!-- Inheritance: Car -> Vehicle -->
  <line x1="50" y1="300" x2="50" y2="270" stroke="var(--acc)" stroke-width="1.5"/>
  <line x1="50" y1="270" x2="85" y2="270" stroke="var(--acc)" stroke-width="1.5"/>
  <!-- Inheritance: Truck -> Vehicle -->
  <line x1="145" y1="300" x2="145" y2="270" stroke="var(--acc)" stroke-width="1.5"/>
  <line x1="145" y1="270" x2="85" y2="270" stroke="var(--acc)" stroke-width="1.5"/>
  <!-- Combined arrow to Vehicle -->
  <line x1="85" y1="270" x2="85" y2="236" stroke="var(--acc)" stroke-width="1.5"/>
  <polygon points="85,236 80,244 85,238 90,244" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>

  <!-- Ticket -->
  <rect x="10" y="370" width="165" height="42" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="10" y="370" width="165" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="92" y="386" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">Ticket</text>
  <line x1="10" y1="392" x2="175" y2="392" stroke="var(--acc)" stroke-width="1"/>
  <text x="18" y="405" fill="var(--acc-tx)">-ticketId · -entryTime · +calculateFee()</text>

  <!-- Payment -->
  <rect x="250" y="370" width="150" height="42" rx="4" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.5"/>
  <rect x="250" y="370" width="150" height="22" rx="4" fill="var(--acc)" opacity="0.18"/>
  <text x="325" y="386" text-anchor="middle" font-weight="700" fill="var(--acc-tx)" font-size="11">Payment</text>
  <line x1="250" y1="392" x2="400" y2="392" stroke="var(--acc)" stroke-width="1"/>
  <text x="258" y="405" fill="var(--acc-tx)">-amount · -paymentType · +process()</text>

</svg>
<div class="fignote">Filled ◆ = composition (ParkingLot owns Floors; Floor owns Spots). Vehicle is abstract; Car/Truck inherit it. Ticket &amp; Payment are independent entities.</div></div>
"""

# ---- UML Multiplicity Notation ----
D["0ff8442a0462"] = r"""
<div class="fig"><div class="figcap">UML Multiplicity Notation</div>
<div class="matrix" style="grid-template-columns:auto 1fr">
  <div class="cell hd">Notation</div><div class="cell hd">Meaning</div>
  <div class="cell on"><span class="chip">1</span></div><div class="cell">Exactly one (mandatory)</div>
  <div class="cell on"><span class="chip">0..1</span></div><div class="cell">Zero or one (optional)</div>
  <div class="cell on"><span class="chip">*</span></div><div class="cell">Zero or more (any number)</div>
  <div class="cell on"><span class="chip">1..*</span></div><div class="cell">One or more (at least one)</div>
  <div class="cell on"><span class="chip">2..5</span></div><div class="cell">Specific range (2, 3, 4, or 5)</div>
</div>
<div class="fignote">Multiplicity is placed at both ends of an association line; read each end from the other class's perspective.</div></div>
"""

# ---- Elevator State Machine ----
D["23b4bbf5a206"] = r"""
<div class="fig"><div class="figcap">Elevator · State Machine</div>
<svg viewBox="0 0 520 120" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace;font-size:10px">

  <!-- IDLE -->
  <rect x="10" y="40" width="80" height="36" rx="18" fill="var(--acc)" opacity="0.22" stroke="var(--acc)" stroke-width="1.8"/>
  <text x="50" y="63" text-anchor="middle" font-weight="700" fill="var(--acc-tx)">IDLE</text>

  <!-- MOVING_UP -->
  <rect x="145" y="40" width="100" height="36" rx="18" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.8"/>
  <text x="195" y="63" text-anchor="middle" font-weight="700" fill="var(--acc-tx)">MOVING_UP</text>

  <!-- DOORS_OPEN (shared) -->
  <rect x="320" y="40" width="110" height="36" rx="18" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.8"/>
  <text x="375" y="63" text-anchor="middle" font-weight="700" fill="var(--acc-tx)">DOORS_OPEN</text>

  <!-- MOVING_DOWN (below) -->
  <rect x="145" y="86" width="110" height="28" rx="14" fill="var(--acc-bg)" stroke="var(--acc-d)" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="200" y="105" text-anchor="middle" fill="var(--acc-tx)">MOVING_DOWN</text>

  <!-- IDLE -> MOVING_UP -->
  <line x1="90" y1="55" x2="139" y2="55" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr6)"/>

  <!-- MOVING_UP -> DOORS_OPEN -->
  <line x1="245" y1="55" x2="314" y2="55" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr6)"/>

  <!-- DOORS_OPEN -> IDLE (curved back) -->
  <path d="M 375 40 Q 375 10 50 10 Q 50 20 50 40" fill="none" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arr6)"/>

  <!-- IDLE -> MOVING_DOWN -->
  <path d="M 50 76 Q 50 100 139 100" fill="none" stroke="var(--acc-d)" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arr6d)"/>

  <!-- MOVING_DOWN -> DOORS_OPEN -->
  <path d="M 255 100 Q 310 100 330 76" fill="none" stroke="var(--acc-d)" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arr6d)"/>

  <defs>
    <marker id="arr6" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc)"/>
    </marker>
    <marker id="arr6d" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc-d)"/>
    </marker>
  </defs>
</svg>
<div class="fignote">Elevator cycles: IDLE → MOVING_UP → DOORS_OPEN → IDLE, or IDLE → MOVING_DOWN → DOORS_OPEN → IDLE. DOORS_OPEN always returns to IDLE.</div></div>
"""

# ---- Vending Machine State Machine ----
D["030a0d99fdf0"] = r"""
<div class="fig"><div class="figcap">Vending Machine · State Machine</div>
<svg viewBox="0 0 520 160" xmlns="http://www.w3.org/2000/svg" style="font-family:'JetBrains Mono',monospace;font-size:10px">

  <!-- IDLE -->
  <rect x="10" y="60" width="70" height="36" rx="18" fill="var(--acc)" opacity="0.22" stroke="var(--acc)" stroke-width="1.8"/>
  <text x="45" y="83" text-anchor="middle" font-weight="700" fill="var(--acc-tx)">IDLE</text>

  <!-- HAS_MONEY -->
  <rect x="165" y="60" width="100" height="36" rx="18" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.8"/>
  <text x="215" y="83" text-anchor="middle" font-weight="700" fill="var(--acc-tx)">HAS_MONEY</text>

  <!-- DISPENSING -->
  <rect x="350" y="60" width="100" height="36" rx="18" fill="var(--acc-bg)" stroke="var(--acc)" stroke-width="1.8"/>
  <text x="400" y="83" text-anchor="middle" font-weight="700" fill="var(--acc-tx)">DISPENSING</text>

  <!-- IDLE -> HAS_MONEY (insertCoin) -->
  <line x1="80" y1="75" x2="159" y2="75" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arv)"/>
  <text x="100" y="70" text-anchor="middle" font-size="8" fill="var(--acc-tx)">insertCoin</text>

  <!-- HAS_MONEY -> DISPENSING (selectItem) -->
  <line x1="265" y1="75" x2="344" y2="75" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arv)"/>
  <text x="300" y="70" text-anchor="middle" font-size="8" fill="var(--acc-tx)">selectItem</text>

  <!-- DISPENSING -> IDLE (dispense, curved top) -->
  <path d="M 400 60 Q 400 20 45 20 Q 45 40 45 60" fill="none" stroke="var(--acc)" stroke-width="1.5" marker-end="url(#arv)"/>
  <text x="230" y="16" text-anchor="middle" font-size="8" fill="var(--acc-tx)">dispense</text>

  <!-- HAS_MONEY -> IDLE (cancel, curved bottom) -->
  <path d="M 215 96 Q 215 130 45 130 Q 45 110 45 96" fill="none" stroke="var(--acc-d)" stroke-width="1.5" stroke-dasharray="4,2" marker-end="url(#arvd)"/>
  <text x="130" y="145" text-anchor="middle" font-size="8" fill="var(--acc-tx)">cancel</text>

  <!-- Guard note: IDLE + selectItem = error -->
  <rect x="10" y="4" width="145" height="22" rx="4" fill="var(--acc-bg)" stroke="var(--acc-d)" stroke-width="1" stroke-dasharray="3,2"/>
  <text x="82" y="19" text-anchor="middle" font-size="8" fill="var(--acc-tx)">[IDLE + selectItem] → "Insert coin first"</text>

  <defs>
    <marker id="arv" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc)"/>
    </marker>
    <marker id="arvd" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">
      <path d="M0,0 L6,3 L0,6 Z" fill="var(--acc-d)"/>
    </marker>
  </defs>
</svg>
<div class="fignote">Guard condition: selecting an item from IDLE is rejected ("Insert coin first"). cancel from HAS_MONEY returns to IDLE without dispensing.</div></div>
"""

# --- override: SVG class diagram collapsed (no display:block); use reliable HTML boxes ---
D["72c40ea2cb1f"] = r'\n<div class="fig"><div class="figcap">Parking Lot · UML Class Diagram</div><div style="display:flex;flex-wrap:wrap;gap:9px;justify-content:center;align-items:flex-start"><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">ParkingLot</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-floors: List&lt;Floor&gt;<br>-entries / exits</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+findSpot(v)<br>+park() · unpark()</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Floor</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-spots: List&lt;Spot&gt;<br>-floorNo</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+getFreeSpot(v)</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">ParkingSpot<div style="font-size:6.4px;opacity:.8">«abstract»</div></div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-id · -occupied<br>-vehicle</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+canFit(v)<br>+assign(v)</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Compact /<br>Large /<br>Handicapped<div style="font-size:6.4px;opacity:.8">subtypes</div></div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">&nbsp;</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">▷ ParkingSpot</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Vehicle<div style="font-size:6.4px;opacity:.8">«abstract»</div></div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-plate<br>-type</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+getSize()</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Car / Truck /<br>Motorcycle<div style="font-size:6.4px;opacity:.8">subtypes</div></div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">&nbsp;</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">▷ Vehicle</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Ticket</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-id · -spot<br>-entryTime</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+close()</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\'Space Grotesk\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">PricingStrategy<div style="font-size:6.4px;opacity:.8">«interface»</div></div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">&nbsp;</div><div style="padding:4px 7px;font-family:\'JetBrains Mono\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+price(hrs)</div></div></div><div class="fignote"><b>◆ composition</b>: ParkingLot ◆— Floor ◆— ParkingSpot &nbsp;·&nbsp; <b>▷ inheritance</b>: spot &amp; vehicle subtypes &nbsp;·&nbsp; <b>Strategy</b>: pluggable PricingStrategy &nbsp;·&nbsp; <b>Singleton</b>: ParkingLot</div></div>\n'

# fix: re-assign without literal newlines
D['72c40ea2cb1f'] = '<div class="fig"><div class="figcap">Parking Lot · UML Class Diagram</div><div style="display:flex;flex-wrap:wrap;gap:9px;justify-content:center;align-items:flex-start"><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">ParkingLot</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-floors: List&lt;Floor&gt;<br>-entries / exits</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+findSpot(v)<br>+park() · unpark()</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Floor</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-spots: List&lt;Spot&gt;<br>-floorNo</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+getFreeSpot(v)</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">ParkingSpot<div style="font-size:6.4px;opacity:.8">«abstract»</div></div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-id · -occupied<br>-vehicle</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+canFit(v)<br>+assign(v)</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Compact /<br>Large /<br>Handicapped<div style="font-size:6.4px;opacity:.8">subtypes</div></div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">&nbsp;</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">▷ ParkingSpot</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Vehicle<div style="font-size:6.4px;opacity:.8">«abstract»</div></div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-plate<br>-type</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+getSize()</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Car / Truck /<br>Motorcycle<div style="font-size:6.4px;opacity:.8">subtypes</div></div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">&nbsp;</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">▷ Vehicle</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">Ticket</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">-id · -spot<br>-entryTime</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+close()</div></div><div style="border:1px solid var(--acc);border-radius:8px;overflow:hidden;background:#fff;min-width:104px;box-shadow:0 1px 3px #0b10200f"><div style="background:var(--acc);color:#fff;font-family:\\\'Space Grotesk\\\';font-weight:700;font-size:8.4px;text-align:center;padding:4px 6px">PricingStrategy<div style="font-size:6.4px;opacity:.8">«interface»</div></div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);border-bottom:1px solid var(--acc-bd);line-height:1.55">&nbsp;</div><div style="padding:4px 7px;font-family:\\\'JetBrains Mono\\\';font-size:6.8px;color:var(--acc-tx);line-height:1.55">+price(hrs)</div></div></div><div class="fignote"><b>◆ composition</b>: ParkingLot ◆— Floor ◆— ParkingSpot &nbsp;·&nbsp; <b>▷ inheritance</b>: spot &amp; vehicle subtypes &nbsp;·&nbsp; <b>Strategy</b>: pluggable PricingStrategy &nbsp;·&nbsp; <b>Singleton</b>: ParkingLot</div></div>'

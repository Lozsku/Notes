# Hand-built HTML diagrams for 03-computer-networks.md  (key = md5(ascii)[:12])
D = {}

# ---- OSI 7-layer stack ----
D["a6e426cab392"] = """
<div class="fig"><div class="figcap">OSI Reference Model · 7 layers</div>
<div class="stack">
  <div class="stk hl"><span class="si">7</span><span class="sn">Application</span><span class="sd">HTTP · DNS · SMTP · FTP · gRPC</span></div>
  <div class="stk"><span class="si">6</span><span class="sn">Presentation</span><span class="sd">TLS/SSL · encoding · compression</span></div>
  <div class="stk"><span class="si">5</span><span class="sn">Session</span><span class="sd">session management · RPC · NetBIOS</span></div>
  <div class="stk hl"><span class="si">4</span><span class="sn">Transport</span><span class="sd">TCP · UDP — ports, reliability</span></div>
  <div class="stk"><span class="si">3</span><span class="sn">Network</span><span class="sd">IP · ICMP · routing</span></div>
  <div class="stk"><span class="si">2</span><span class="sn">Data Link</span><span class="sd">Ethernet · MAC · switches · ARP</span></div>
  <div class="stk"><span class="si">1</span><span class="sn">Physical</span><span class="sd">bits on wire · fiber · radio · voltage</span></div>
</div>
<div class="fignote">Mnemonic (7→1): <b>“All People Seem To Need Data Processing.”</b></div></div>
"""

# ---- TCP 3-way handshake ----
D["5d98ebedb035"] = """
<div class="fig"><div class="figcap">TCP · 3-Way Handshake</div>
<div class="seq">
  <div class="seqhead"><span>Client</span><span>Server</span></div>
  <div class="seqmsg r"><span class="t">SYN — seq = x</span></div>
  <div class="seqmsg l"><span class="t">SYN-ACK — seq = y, ack = x+1</span></div>
  <div class="seqmsg r"><span class="t">ACK — seq = x+1, ack = y+1</span></div>
</div>
<div class="frow" style="margin-top:8px"><span class="chip">✓ Connection established — data flows</span></div>
<div class="fignote">Both sides exchange initial sequence numbers; the third ACK confirms the server’s SYN was received.</div></div>
"""

# ---- TLS 1.3 handshake ----
D["d75a36859702"] = """
<div class="fig"><div class="figcap">TLS 1.3 Handshake · 1-RTT</div>
<div class="seq">
  <div class="seqhead"><span>Client</span><span>Server</span></div>
  <div class="seqmsg r"><span class="t">ClientHello — versions · ciphers · key_share (DH) · nonce</span></div>
  <div class="seqmsg l"><span class="t">ServerHello — chosen cipher · key_share (DH)</span></div>
  <div class="seqmsg l dash"><span class="t">{Certificate} · {CertificateVerify} · {Finished}</span></div>
</div>
<div class="frow" style="margin:7px 0"><span class="chip">Client derives session keys + verifies cert chain</span></div>
<div class="seq" style="padding-top:0">
  <div class="seqmsg r dash"><span class="t">{Finished}</span></div>
</div>
<div class="frow" style="margin-top:7px"><span class="chip">🔒 Encrypted application data</span></div>
<div class="fignote"><b>{…}</b> = encrypted. Asymmetric DH establishes a shared symmetric key; data then uses fast symmetric crypto.</div></div>
"""

# ---- DNS recursive resolution ----
D["dc5a2ee60572"] = """
<div class="fig"><div class="figcap">DNS Resolution · recursive lookup</div>
<div class="frow" style="flex-wrap:nowrap">
  <div class="node soft"><div class="nt">Browser</div><div class="ns">wants google.com</div></div>
  <span class="ar">→</span>
  <div class="node acc"><div class="nt">Resolver</div><div class="ns">recursive · ISP / 8.8.8.8</div></div>
</div>
<div class="ar-d" style="margin:9px 0">↓ &nbsp; resolver queries the hierarchy iteratively &nbsp; ↓</div>
<div class="frow" style="flex-wrap:nowrap">
  <div class="node"><div class="nt">Root&nbsp;NS</div><div class="ns">“ask .com”</div></div>
  <span class="ar">→</span>
  <div class="node"><div class="nt">.com TLD</div><div class="ns">“ask auth NS”</div></div>
  <span class="ar">→</span>
  <div class="node soft"><div class="nt">Auth&nbsp;NS</div><div class="ns">142.250.80.78</div></div>
</div>
<div class="fignote">Resolver walks Root → TLD → Authoritative, then <b>caches</b> the answer (TTL ≈ 300 s) and returns it.</div></div>
"""

# ---- L4 load balancer ----
D["03be99fe5923"] = """
<div class="fig"><div class="figcap">Layer 4 Load Balancer</div>
<div class="frow" style="flex-wrap:nowrap">
  <div class="node soft"><div class="nt">Client</div></div><span class="ar">→</span>
  <div class="node acc"><div class="nt">L4 LB</div><div class="ns">sees IP : port · NATs packet</div></div><span class="ar">→</span>
  <div class="node"><div class="nt">Server A</div></div>
</div>
<div class="fignote">Operates at the transport layer (TCP/UDP) — very fast, connection-level; blind to HTTP paths.</div></div>
"""

# ---- L7 load balancer (content routing) ----
D["507ff89dea59"] = """
<div class="fig"><div class="figcap">Layer 7 Load Balancer · content routing</div>
<div class="frow" style="flex-wrap:nowrap">
  <div class="node soft"><div class="nt">Client</div></div><span class="ar">→</span>
  <div class="node acc"><div class="nt">L7 LB</div><div class="ns">terminates TLS · parses HTTP</div></div>
</div>
<div class="fcol" style="margin-top:10px;width:74%;margin-left:auto">
  <div class="frow sb" style="flex-wrap:nowrap"><span class="chip">/api/users</span><span class="ar">→</span><div class="node"><div class="nt">User Service</div></div></div>
  <div class="frow sb" style="flex-wrap:nowrap"><span class="chip">/api/orders</span><span class="ar">→</span><div class="node"><div class="nt">Order Service</div></div></div>
  <div class="frow sb" style="flex-wrap:nowrap"><span class="chip">/static/*</span><span class="ar">→</span><div class="node"><div class="nt">CDN / S3</div></div></div>
</div>
<div class="fignote">Routes by URL path, headers or cookies — enables path-based microservice routing, canary &amp; A/B.</div></div>
"""

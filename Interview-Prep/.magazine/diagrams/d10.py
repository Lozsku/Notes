# Hand-built HTML diagrams for 10-security-fundamentals.md  (key = md5(ascii)[:12])
D = {}

# ---- OAuth 2.0 Authorization Code + PKCE flow ----
D["7dcfd136490c"] = r"""
<div class="fig"><div class="figcap">OAuth 2.0 · Authorization Code + PKCE Flow</div>
<div class="tiers" style="grid-template-columns:repeat(4,1fr);gap:6px">
  <div class="tier"><div class="th">User</div></div>
  <div class="tier"><div class="th">Browser / App</div></div>
  <div class="tier"><div class="th">Auth Server</div></div>
  <div class="tier"><div class="th">Resource Server</div></div>
</div>
<div class="fcol" style="gap:6px;margin-top:6px">
  <div class="frow sb" style="flex-wrap:nowrap;gap:8px">
    <div class="node soft" style="flex:0 0 auto"><div class="nt" style="font-size:10px">1. Click Login</div></div>
    <span class="ar">→</span>
    <div class="node" style="flex:1"><div class="nt" style="font-size:10px">Generate <code>code_verifier</code></div><div class="ns"><code>code_challenge = BASE64URL(SHA256(verifier))</code></div></div>
  </div>
  <div class="ar-d">↓ 2. Redirect to AS with code_challenge + state ↓</div>
  <div class="frow sb" style="flex-wrap:nowrap;gap:8px">
    <div class="node" style="flex:1"><div class="nt" style="font-size:10px">User enters creds &amp; approves scopes</div></div>
    <span class="ar">→</span>
    <div class="node soft" style="flex:1"><div class="nt" style="font-size:10px">AS stores challenge</div><div class="ns">issues <code>auth_code</code> (60 s)</div></div>
  </div>
  <div class="ar-d">↓ 3. Redirect back → GET /callback?code=AUTH_CODE&amp;state=… ↓</div>
  <div class="frow sb" style="flex-wrap:nowrap;gap:8px">
    <div class="node" style="flex:1"><div class="nt" style="font-size:10px">Verify state (CSRF check)</div></div>
    <span class="ar">→</span>
    <div class="node" style="flex:1"><div class="nt" style="font-size:10px">POST /token</div><div class="ns"><code>code + code_verifier</code></div></div>
    <span class="ar">→</span>
    <div class="node soft" style="flex:1"><div class="nt" style="font-size:10px">Recompute SHA256(verifier)</div><div class="ns">compare to stored challenge</div></div>
  </div>
  <div class="ar-d">↓ 4. AS returns access_token (JWT) + id_token + refresh_token ↓</div>
  <div class="frow sb" style="flex-wrap:nowrap;gap:8px">
    <div class="node" style="flex:1"><div class="nt" style="font-size:10px">GET /api/data</div><div class="ns"><code>Authorization: Bearer ACCESS_TOKEN</code></div></div>
    <span class="ar">→</span>
    <div class="node acc" style="flex:1"><div class="nt" style="font-size:10px">Resource Server</div><div class="ns">validate JWT sig · expiry · aud</div></div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">PKCE prevents auth-code interception</span>
  <span class="chip">state= stops CSRF</span>
  <span class="chip">no client_secret needed (public clients)</span>
</div>
<div class="fignote">PKCE: even if <code>auth_code</code> is stolen, attacker can't exchange it — they don't have <code>code_verifier</code>.</div></div>
"""

# ---- JWT Anatomy ----
D["427aabd9b1ad"] = r"""
<div class="fig"><div class="figcap">JWT · Header . Payload . Signature</div>
<svg viewBox="0 0 520 72" xmlns="http://www.w3.org/2000/svg" style="margin:8px 0">
  <defs>
    <linearGradient id="g-h" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="var(--acc)" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="var(--acc)" stop-opacity="0.6"/>
    </linearGradient>
    <linearGradient id="g-p" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="var(--acc2)" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="var(--acc2)" stop-opacity="0.6"/>
    </linearGradient>
    <linearGradient id="g-s" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="var(--acc-d)" stop-opacity="0.85"/>
      <stop offset="100%" stop-color="var(--acc-d)" stop-opacity="0.6"/>
    </linearGradient>
  </defs>
  <!-- Header segment -->
  <rect x="2" y="8" width="148" height="36" rx="6" fill="url(#g-h)"/>
  <text x="76" y="22" text-anchor="middle" font-family="Space Grotesk" font-size="11" font-weight="700" fill="var(--acc-tx)">HEADER</text>
  <text x="76" y="37" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">alg: RS256 · typ: JWT</text>
  <!-- dot -->
  <text x="155" y="30" text-anchor="middle" font-family="JetBrains Mono" font-size="18" font-weight="900" fill="var(--acc-tx)">.</text>
  <!-- Payload segment -->
  <rect x="162" y="8" width="192" height="36" rx="6" fill="url(#g-p)"/>
  <text x="258" y="22" text-anchor="middle" font-family="Space Grotesk" font-size="11" font-weight="700" fill="var(--acc-tx)">PAYLOAD</text>
  <text x="258" y="37" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">sub · iat · exp · iss · aud · claims</text>
  <!-- dot -->
  <text x="360" y="30" text-anchor="middle" font-family="JetBrains Mono" font-size="18" font-weight="900" fill="var(--acc-tx)">.</text>
  <!-- Signature segment -->
  <rect x="368" y="8" width="148" height="36" rx="6" fill="url(#g-s)"/>
  <text x="442" y="22" text-anchor="middle" font-family="Space Grotesk" font-size="11" font-weight="700" fill="var(--acc-tx)">SIGNATURE</text>
  <text x="442" y="37" text-anchor="middle" font-family="JetBrains Mono" font-size="8.5" fill="var(--acc-tx)">RSA_Sign(privKey, H+"."+P)</text>
  <!-- label arrows -->
  <text x="76" y="62" text-anchor="middle" font-family="Space Grotesk" font-size="9" fill="var(--acc-tx)" opacity="0.7">HOW (algorithm)</text>
  <text x="258" y="62" text-anchor="middle" font-family="Space Grotesk" font-size="9" fill="var(--acc-tx)" opacity="0.7">WHAT (claims) — not secret!</text>
  <text x="442" y="62" text-anchor="middle" font-family="Space Grotesk" font-size="9" fill="var(--acc-tx)" opacity="0.7">PROOF (tamper-evident)</text>
</svg>
<div class="frow" style="margin-top:4px;gap:6px;flex-wrap:wrap">
  <span class="chip">Base64URL encoded — NOT encrypted</span>
  <span class="chip">RS256 = asymmetric (verify with pubkey)</span>
  <span class="chip">HS256 = symmetric (shared secret)</span>
</div>
<div class="fignote">Payload is readable by anyone — never put secrets in JWT. Signature prevents tampering.</div></div>
"""

# ---- TLS / PKI Certificate Trust Chain ----
D["6991978f631e"] = r"""
<div class="fig"><div class="figcap">PKI · Certificate Trust Chain</div>
<div class="fcol" style="gap:0;align-items:center">
  <div class="node soft" style="width:90%;border:2px solid var(--acc);text-align:center">
    <div class="nt">OS / Browser Trust Store</div>
    <div class="ns">pre-installed Root CAs (≈ 150 trusted roots)</div>
  </div>
  <div class="ar-d" style="margin:0">↓ contains (pre-installed)</div>
  <div class="node acc" style="width:80%;text-align:center">
    <div class="nt">Root CA &nbsp;·&nbsp; e.g. DigiCert</div>
    <div class="ns">Self-signed · Offline · Hardware HSM vault · If compromised: millions of certs invalid</div>
  </div>
  <div class="ar-d" style="margin:0">↓ signs offline (ceremony)</div>
  <div class="node" style="width:70%;text-align:center">
    <div class="nt">Intermediate CA &nbsp;·&nbsp; DigiCert CA G2</div>
    <div class="ns">Online · Signs end-entity certs · If compromised: revoke &amp; reissue all leaf certs</div>
  </div>
  <div class="ar-d" style="margin:0">↓ signs via ACME (automated)</div>
  <div class="node soft" style="width:60%;text-align:center">
    <div class="nt">Leaf / Server Cert &nbsp;·&nbsp; example.com</div>
    <div class="ns">Public key · Domain · Expiry · CA signature · Presented during TLS handshake</div>
  </div>
  <div class="ar-d" style="margin:0">↓ used in</div>
  <div class="node" style="width:50%;text-align:center">
    <div class="nt">TLS Handshake with Client</div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">Root offline = reduces attack surface</span>
  <span class="chip">Short-lived leaf certs (90 days)</span>
  <span class="chip">Chain verified bottom-up</span>
</div>
<div class="fignote">Client verifies: leaf signed by intermediate → intermediate signed by Root → Root in trust store.</div></div>
"""

# ---- Defense in Depth ----
D["61989424bc2d"] = r"""
<div class="fig"><div class="figcap">Defense in Depth · 7 Layers</div>
<div class="stack">
  <div class="stk hl"><span class="si">7</span><span class="sn">Data Layer</span><span class="sd">AES-256-GCM at rest · column-level encryption for PII · DB audit logs</span></div>
  <div class="stk"><span class="si">6</span><span class="sn">Application Layer</span><span class="sd">Input validation · parameterized queries · dependency scanning · OWASP Top 10</span></div>
  <div class="stk hl"><span class="si">5</span><span class="sn">AuthN &amp; AuthZ</span><span class="sd">MFA required · OAuth 2.0 / OIDC / JWT · RBAC/ABAC · least privilege</span></div>
  <div class="stk"><span class="si">4</span><span class="sn">Host / Compute</span><span class="sd">OS patching · EDR · container hardening (read-only FS, non-root) · IMDSv2</span></div>
  <div class="stk hl"><span class="si">3</span><span class="sn">Network Layer</span><span class="sd">TLS everywhere · VPC private subnets · security groups / NACLs · mTLS service-to-service</span></div>
  <div class="stk"><span class="si">2</span><span class="sn">Perimeter</span><span class="sd">WAF (blocks SQLi, XSS, SSRF) · DDoS protection (Shield / Cloudflare) · API GW rate limiting</span></div>
  <div class="stk"><span class="si">1</span><span class="sn">Physical / Cloud Infra</span><span class="sd">IAM least privilege · VPC isolation · CloudTrail audit logs · MFA for cloud console</span></div>
</div>
<div class="fignote">Attacker must breach ALL layers. Each layer slows, detects, or alerts — no single point of failure.</div></div>
"""

# ---- AuthN vs AuthZ ----
D["46764ade270c"] = r"""
<div class="fig"><div class="figcap">Authentication vs Authorization</div>
<div class="frow sb" style="flex-wrap:nowrap;gap:12px;align-items:stretch">
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">AUTHENTICATION (AuthN)</div><div class="ns">"Who are you?"</div></div>
    <div class="node soft" style="text-align:center"><div class="nt">Step 1 — must happen first</div></div>
    <div class="node" style="text-align:center"><div class="nt">Produces</div><div class="ns">identity / principal</div></div>
    <div class="node" style="text-align:center"><div class="nt">Mechanism</div><div class="ns">passwords · tokens · certs · MFA</div></div>
    <div class="node soft" style="text-align:center;border:2px solid var(--acc)"><div class="nt">Failure → <code>401 Unauthorized</code></div><div class="ns">(misnamed — really means "Unauthenticated")</div></div>
  </div>
  <div class="fcol" style="flex:0 0 auto;align-items:center;justify-content:center">
    <span class="ar" style="font-size:22px;opacity:0.5">→</span>
  </div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">AUTHORIZATION (AuthZ)</div><div class="ns">"What can you do?"</div></div>
    <div class="node soft" style="text-align:center"><div class="nt">Step 2 — always after AuthN</div></div>
    <div class="node" style="text-align:center"><div class="nt">Produces</div><div class="ns">permission decision (allow / deny)</div></div>
    <div class="node" style="text-align:center"><div class="nt">Mechanism</div><div class="ns">RBAC · ABAC · policy engine</div></div>
    <div class="node soft" style="text-align:center;border:2px solid var(--acc)"><div class="nt">Failure → <code>403 Forbidden</code></div><div class="ns">authenticated but not permitted</div></div>
  </div>
</div>
<div class="fignote">Mnemonic: AuthN → N → "Name" (who you are). AuthZ → Z → "Zone" (where you can go).</div></div>
"""

# ---- TLS 1.3 Handshake (1-RTT) ----
D["55961ce71c5a"] = r"""
<div class="fig"><div class="figcap">TLS 1.3 Handshake · 1-RTT</div>
<div class="seq">
  <div class="seqhead"><span>Client</span><span>Server</span></div>
  <div class="seqmsg r"><span class="t">1. ClientHello — TLS 1.3 · client_random · cipher_suites · key_share (X25519 DH pubkey)</span></div>
  <div class="seqmsg l"><span class="t">2. ServerHello — chosen cipher (AES-256-GCM) · server_DH_public_key</span></div>
  <div class="seqmsg l dash"><span class="t">3. {Certificate} — X.509 cert chain [encrypted]</span></div>
  <div class="seqmsg l dash"><span class="t">4. {CertificateVerify} — Signature over handshake transcript using server private key</span></div>
  <div class="seqmsg l dash"><span class="t">5. {Finished} — HMAC of transcript [encrypted]</span></div>
  <div class="seqmsg r dash"><span class="t">6. {Finished} — client confirms</span></div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">shared_secret = ECDH(my_priv, their_pub)</span>
  <span class="chip">derive handshake_key + app_key</span>
  <span class="chip">1-RTT vs TLS 1.2's 2-RTT</span>
  <span class="chip">{…} = encrypted</span>
</div>
<div class="fignote">ECDH gives forward secrecy — compromise of server private key does NOT decrypt past sessions.</div></div>
"""

# ---- Symmetric vs Asymmetric Encryption ----
D["0c18e61f89c6"] = r"""
<div class="fig"><div class="figcap">Symmetric vs Asymmetric Encryption</div>
<div class="frow sb" style="flex-wrap:nowrap;gap:12px;align-items:stretch">
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">SYMMETRIC</div><div class="ns">SAME key for encrypt &amp; decrypt</div></div>
    <div class="node soft" style="text-align:center"><div class="nt">Algorithms</div><div class="ns">AES-128-GCM · AES-256-GCM · ChaCha20</div></div>
    <div class="node" style="text-align:center"><div class="nt">Speed</div><div class="ns">Very fast — hardware-accelerated</div></div>
    <div class="node" style="text-align:center"><div class="nt">Problem</div><div class="ns">Key exchange over insecure channel?</div></div>
    <div class="node soft" style="text-align:center"><div class="nt">Use for</div><div class="ns">Bulk data encryption (TLS session, disk, DB)</div></div>
  </div>
  <div class="fcol" style="flex:0 0 auto;align-items:center;justify-content:center">
    <span style="font-size:20px;opacity:0.4">vs</span>
  </div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">ASYMMETRIC</div><div class="ns">Public key encrypts · Private key decrypts</div></div>
    <div class="node soft" style="text-align:center"><div class="nt">Algorithms</div><div class="ns">RSA-2048/4096 · ECDSA · Ed25519 · ECDH</div></div>
    <div class="node" style="text-align:center"><div class="nt">Speed</div><div class="ns">~1000× slower than symmetric</div></div>
    <div class="node" style="text-align:center"><div class="nt">Strength</div><div class="ns">No shared secret needed upfront</div></div>
    <div class="node soft" style="text-align:center"><div class="nt">Use for</div><div class="ns">Key exchange (ECDH) · Signatures · TLS cert</div></div>
  </div>
</div>
<div class="frow" style="margin-top:8px"><span class="chip">TLS 1.3 pattern: Asymmetric (ECDH) negotiates key → Symmetric (AES-GCM) encrypts data</span></div>
<div class="fignote">Best of both worlds: asymmetric for secure key exchange; symmetric for fast bulk encryption.</div></div>
"""

# ---- CIA Triad ----
D["b520e4ebc6bc"] = r"""
<div class="fig"><div class="figcap">CIA Triad · Security Fundamentals</div>
<div class="frow" style="gap:10px;flex-wrap:wrap;justify-content:center">
  <div class="node acc" style="flex:1;min-width:140px;text-align:center">
    <div class="nt">C — Confidentiality</div>
    <div class="ns">Only authorized parties can READ · Encryption at rest &amp; in transit · Access control</div>
  </div>
  <div class="node acc" style="flex:1;min-width:140px;text-align:center">
    <div class="nt">I — Integrity</div>
    <div class="ns">Data is not TAMPERED · Checksums · Digital signatures · HMAC · Audit logs</div>
  </div>
  <div class="node acc" style="flex:1;min-width:140px;text-align:center">
    <div class="nt">A — Availability</div>
    <div class="ns">System remains ACCESSIBLE · Redundancy · DDoS protection · Backups · SLAs</div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:6px;flex-wrap:wrap">
  <span class="chip">C broken → data leak</span>
  <span class="chip">I broken → data corruption / tampering</span>
  <span class="chip">A broken → downtime / DDoS</span>
</div>
<div class="fignote">All security controls map to at least one CIA property. Ransomware attacks all three simultaneously.</div></div>
"""

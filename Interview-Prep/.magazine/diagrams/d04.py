# Hand-built HTML diagrams for 04-cloud-infrastructure.md  (key = md5(ascii)[:12])
D = {}

# ---- Cloud / Infrastructure stack overview ----
D["edae699bed24"] = r"""
<div class="fig"><div class="figcap">Cloud &amp; Infrastructure Stack</div>
<div class="stack">
  <div class="stk"><span class="sn">Infrastructure as Code</span><span class="sd">Terraform · CloudFormation · Pulumi</span></div>
  <div class="stk"><span class="sn">Observability</span><span class="sd">Metrics · Logs · Traces</span></div>
  <div class="stk"><span class="sn">CI/CD Pipelines</span><span class="sd">GitHub Actions · ArgoCD · Spinnaker</span></div>
  <div class="stk hl"><span class="sn">Service Mesh</span><span class="sd">Istio · Envoy · Linkerd</span></div>
  <div class="stk hl"><span class="sn">Container Orchestration</span><span class="sd">Kubernetes · ECS · Nomad</span></div>
  <div class="stk"><span class="sn">Virtual Machines / Containers</span><span class="sd">Docker · containerd · runc</span></div>
  <div class="stk"><span class="sn">Hypervisor / OS Kernel</span><span class="sd">KVM · VMware · Host Linux kernel</span></div>
  <div class="stk"><span class="sn">Physical Hardware</span><span class="sd">CPU · RAM · NIC · bare metal</span></div>
</div>
<div class="fignote">Each layer abstracts complexity from the one below — containers share the kernel, VMs each carry their own OS.</div></div>
"""

# ---- VM vs Container side-by-side ----
D["a27bfef10f50"] = r"""
<div class="fig"><div class="figcap">VMs vs Containers — isolation model</div>
<div class="frow sb" style="align-items:stretch;gap:18px">
  <div class="fcol" style="flex:1">
    <div class="node acc" style="text-align:center;margin-bottom:6px"><div class="nt">VIRTUAL MACHINES</div></div>
    <div class="stack">
      <div class="stk hl"><span class="sn">App A</span></div>
      <div class="stk"><span class="sn">Guest OS (Linux)</span></div>
      <div class="stk hl"><span class="sn">App B</span></div>
      <div class="stk"><span class="sn">Guest OS (Windows)</span></div>
      <div class="stk"><span class="sn">Hypervisor (KVM)</span></div>
      <div class="stk"><span class="sn">Physical Hardware</span></div>
    </div>
    <div class="node soft" style="text-align:center;margin-top:8px"><div class="ns">GBs · minutes to boot · full isolation</div></div>
  </div>
  <div class="fcol" style="flex:1">
    <div class="node acc" style="text-align:center;margin-bottom:6px"><div class="nt">CONTAINERS</div></div>
    <div class="stack">
      <div class="stk hl"><span class="sn">App A + Libs</span><span class="sd">namespace · cgroup</span></div>
      <div class="stk hl"><span class="sn">App B + Libs</span><span class="sd">namespace · cgroup</span></div>
      <div class="stk hl"><span class="sn">App C + Libs</span><span class="sd">namespace · cgroup</span></div>
      <div class="stk"><span class="sn">Host OS Kernel</span></div>
      <div class="stk"><span class="sn">Physical Hardware</span></div>
    </div>
    <div class="node soft" style="text-align:center;margin-top:8px"><div class="ns">MBs · milliseconds to start · shared kernel</div></div>
  </div>
</div>
<div class="fignote">Containers share the host kernel via namespaces &amp; cgroups — faster &amp; denser, but weaker isolation than full VMs.</div></div>
"""

# ---- Docker image layers ----
D["e4b55d447d4b"] = r"""
<div class="fig"><div class="figcap">Docker Image Layers · OverlayFS</div>
<div class="stack">
  <div class="stk hl"><span class="si">R/W</span><span class="sn">Container Layer</span><span class="sd">ephemeral — lost on container stop</span></div>
  <div class="stk"><span class="si">4</span><span class="sn">COPY app/ /app</span><span class="sd">image layer (read-only)</span></div>
  <div class="stk"><span class="si">3</span><span class="sn">RUN pip install</span><span class="sd">image layer (read-only)</span></div>
  <div class="stk"><span class="si">2</span><span class="sn">RUN apt-get update</span><span class="sd">image layer (read-only)</span></div>
  <div class="stk"><span class="si">1</span><span class="sn">FROM ubuntu:22.04</span><span class="sd">base image layer (read-only, shared on disk)</span></div>
</div>
<div class="fignote">OverlayFS merges all read-only layers + writable container layer into a single unified view — unchanged layers are shared across containers.</div></div>
"""

# ---- Kubernetes cluster architecture ----
D["e10059eac9e6"] = r"""
<div class="fig"><div class="figcap">Kubernetes Cluster Architecture</div>
<div class="tiers">
  <div class="tier" style="flex:2">
    <div class="th">CONTROL PLANE</div>
    <div class="fcol" style="gap:6px">
      <div class="node acc"><div class="nt">kube-apiserver</div><div class="ns">REST gateway · AuthN→AuthZ (RBAC)→Admission→etcd</div></div>
      <div class="frow sb" style="flex-wrap:nowrap;gap:6px">
        <div class="node soft" style="flex:1"><div class="nt">etcd</div><div class="ns">Raft quorum · cluster state</div></div>
        <div class="node soft" style="flex:1"><div class="nt">Controller Manager</div><div class="ns">reconciliation loops</div></div>
        <div class="node soft" style="flex:1"><div class="nt">kube-scheduler</div><div class="ns">filter → score → bind</div></div>
      </div>
    </div>
  </div>
</div>
<div class="ar-d" style="margin:6px 0">↓ &nbsp; kubelet watches API server &nbsp; ↓</div>
<div class="tiers">
  <div class="tier">
    <div class="th">WORKER NODE 1</div>
    <div class="fcol" style="gap:4px">
      <div class="node"><div class="nt">kubelet</div><div class="ns">CRI → containerd</div></div>
      <div class="node"><div class="nt">kube-proxy</div><div class="ns">iptables / ipvs</div></div>
      <div class="node soft"><div class="nt">Pod: nginx</div><div class="ns">[app][envoy]</div></div>
      <div class="node soft"><div class="nt">Pod: worker</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">WORKER NODE 2</div>
    <div class="fcol" style="gap:4px">
      <div class="node"><div class="nt">kubelet</div></div>
      <div class="node"><div class="nt">kube-proxy</div></div>
      <div class="node soft"><div class="nt">Pod: api-svc</div><div class="ns">[app][envoy]</div></div>
    </div>
  </div>
  <div class="tier">
    <div class="th">WORKER NODE 3</div>
    <div class="fcol" style="gap:4px">
      <div class="node"><div class="nt">kubelet</div></div>
      <div class="node"><div class="nt">kube-proxy</div></div>
      <div class="node soft"><div class="nt">Pod: redis</div></div>
    </div>
  </div>
</div>
<div class="frow" style="margin-top:8px;gap:8px;flex-wrap:wrap">
  <span class="chip">DNS: CoreDNS (kube-system)</span>
  <span class="chip">Network: CNI — Calico / Cilium</span>
  <span class="chip">Storage: CSI — EBS / GCE PD</span>
</div>
<div class="fignote">etcd is the single source of truth; controllers run reconciliation loops to converge actual → desired state.</div></div>
"""

# ---- HPA autoscaling formula ----
D["7f2becb92cad"] = r"""
<div class="fig"><div class="figcap">Horizontal Pod Autoscaler (HPA)</div>
<div class="frow sb" style="align-items:flex-start;gap:14px;flex-wrap:nowrap">
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node soft"><div class="nt">Metrics Sources</div><div class="ns">Prometheus · Custom Metrics API · metrics-server</div></div>
    <div class="ar-d">↓ pull</div>
    <div class="node"><div class="nt">metrics-server</div></div>
  </div>
  <span class="ar" style="align-self:center">→</span>
  <div class="fcol" style="flex:2;gap:6px">
    <div class="node acc"><div class="nt">HPA Controller</div><div class="ns">target CPU: 50% &nbsp;|&nbsp; current: 80% &nbsp;|&nbsp; replicas: 3</div></div>
    <div class="node hl" style="text-align:center;padding:10px">
      <div class="nt" style="font-family:'JetBrains Mono',monospace;font-size:0.9em">desired = ⌈ 3 × (80 / 50) ⌉ = <b>5</b></div>
    </div>
    <div class="ar-d">↓ scale to 5</div>
    <div class="node soft"><div class="nt">Deployment</div><div class="ns">replicas: 5</div></div>
  </div>
</div>
<div class="fignote">HPA polls metrics every 15 s; VPA adjusts resource requests; CA adds/removes nodes when pods stay unschedulable.</div></div>
"""

# ---- Service mesh sidecar (Envoy / Istio) ----
D["23227e7c94c2"] = r"""
<div class="fig"><div class="figcap">Service Mesh · Sidecar Pattern (Istio / Envoy)</div>
<div class="frow sb" style="align-items:stretch;gap:16px;flex-wrap:nowrap">
  <div class="fcol" style="flex:1;border:1px solid var(--acc-bd);border-radius:8px;padding:10px">
    <div class="node soft" style="text-align:center;margin-bottom:6px"><div class="nt">POD A</div></div>
    <div class="frow" style="gap:8px;flex-wrap:nowrap">
      <div class="node" style="flex:1"><div class="nt">App</div><div class="ns">:8080</div></div>
      <div class="node acc" style="flex:1"><div class="nt">Envoy</div><div class="ns">:15001</div></div>
    </div>
    <div class="fignote" style="margin-top:6px">iptables redirects all traffic through sidecar</div>
  </div>
  <div class="fcol" style="justify-content:center;align-items:center;gap:4px">
    <span class="chip">mTLS</span>
    <span class="ar">⟷</span>
    <span class="chip">xDS</span>
  </div>
  <div class="fcol" style="flex:1;border:1px solid var(--acc-bd);border-radius:8px;padding:10px">
    <div class="node soft" style="text-align:center;margin-bottom:6px"><div class="nt">POD B</div></div>
    <div class="frow" style="gap:8px;flex-wrap:nowrap">
      <div class="node acc" style="flex:1"><div class="nt">Envoy</div><div class="ns">:15001</div></div>
      <div class="node" style="flex:1"><div class="nt">App</div><div class="ns">:8080</div></div>
    </div>
    <div class="fignote" style="margin-top:6px">authz check → route → emit metric/span</div>
  </div>
</div>
<div class="ar-d" style="margin:8px 0">↓ &nbsp; xDS gRPC streaming &nbsp; ↓</div>
<div class="node acc" style="max-width:420px;margin:0 auto">
  <div class="nt">Istiod (Control Plane)</div>
  <div class="ns">Pilot (xDS) · Citadel (CA, mTLS certs) · Galley (config)</div>
</div>
<div class="fignote">Sidecars handle retries, circuit-breaking, mTLS, tracing — zero app code changes needed.</div></div>
"""

# ---- CI/CD deployment strategies ----
D["5249d8b90ff7"] = r"""
<div class="fig"><div class="figcap">Deployment Strategies · Blue-Green · Rolling · Canary</div>

<div class="frow sb" style="align-items:flex-start;gap:14px;flex-wrap:wrap">

  <div class="fcol" style="flex:1;min-width:160px">
    <div class="node acc" style="text-align:center;margin-bottom:6px"><div class="nt">BLUE-GREEN</div></div>
    <div class="frow" style="gap:6px;flex-wrap:nowrap">
      <div class="node soft" style="flex:1;text-align:center"><div class="nt">Blue (v1)</div><div class="ns">running</div></div>
      <div class="node" style="flex:1;text-align:center"><div class="nt">Green (v2)</div><div class="ns">idle / new</div></div>
    </div>
    <div class="fcol" style="margin-top:8px;gap:3px">
      <div class="node soft"><div class="ns">1. Deploy v2 → Green</div></div>
      <div class="node soft"><div class="ns">2. Smoke-test Green</div></div>
      <div class="node acc"><div class="ns">3. Switch LB 100% → Green</div></div>
      <div class="node soft"><div class="ns">4. Blue stays hot for rollback</div></div>
    </div>
  </div>

  <div class="fcol" style="flex:1;min-width:160px">
    <div class="node acc" style="text-align:center;margin-bottom:6px"><div class="nt">ROLLING</div></div>
    <div class="gantt">
      <div class="gr"><span class="gl">start</span><div class="track"><div class="gseg a" style="width:100%">v1 v1 v1 v1 v1</div></div></div>
      <div class="gr"><span class="gl">step 1</span><div class="track"><div class="gseg b" style="width:20%">v2</div><div class="gseg a" style="width:80%">v1×4</div></div></div>
      <div class="gr"><span class="gl">step 2</span><div class="track"><div class="gseg b" style="width:40%">v2×2</div><div class="gseg a" style="width:60%">v1×3</div></div></div>
      <div class="gr"><span class="gl">step 3</span><div class="track"><div class="gseg b" style="width:60%">v2×3</div><div class="gseg a" style="width:40%">v1×2</div></div></div>
      <div class="gr"><span class="gl">done</span><div class="track"><div class="gseg b" style="width:100%">v2 v2 v2 v2 v2</div></div></div>
    </div>
    <div class="frow" style="margin-top:6px"><span class="chip">maxSurge=1, maxUnavailable=1</span></div>
  </div>

  <div class="fcol" style="flex:1;min-width:160px">
    <div class="node acc" style="text-align:center;margin-bottom:6px"><div class="nt">CANARY</div></div>
    <div class="gantt">
      <div class="gr"><span class="gl">traffic</span><div class="track"><div class="gseg a" style="width:90%">Stable v1 · 90%</div><div class="gseg b" style="width:10%">v2</div></div></div>
      <div class="gr"><span class="gl">grow</span><div class="track"><div class="gseg a" style="width:75%">v1 · 75%</div><div class="gseg b" style="width:25%">v2 25%</div></div></div>
      <div class="gr"><span class="gl">grow</span><div class="track"><div class="gseg a" style="width:50%">v1 50%</div><div class="gseg b" style="width:50%">v2 50%</div></div></div>
      <div class="gr"><span class="gl">done</span><div class="track"><div class="gseg b" style="width:100%">v2 100%</div></div></div>
    </div>
    <div class="frow" style="margin-top:6px"><span class="chip">monitor SLOs → expand or rollback</span></div>
  </div>
</div>
<div class="fignote">Blue-green = instant cutover; rolling = gradual in-place; canary = risk-gated traffic shift with real-user validation.</div></div>
"""

# ---- Observability three pillars ----
D["66368614c937"] = r"""
<div class="fig"><div class="figcap">Observability · Three Pillars</div>
<div class="frow sb" style="gap:12px;align-items:stretch;flex-wrap:nowrap">
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">METRICS</div></div>
    <div class="node soft"><div class="ns">What happened (aggregated numbers)</div></div>
    <div class="node"><div class="nt">Prometheus</div></div>
    <div class="node"><div class="nt">Grafana</div></div>
    <div class="node"><div class="nt">Datadog</div></div>
  </div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">LOGS</div></div>
    <div class="node soft"><div class="ns">Why it happened (event detail)</div></div>
    <div class="node"><div class="nt">ELK Stack</div></div>
    <div class="node"><div class="nt">Loki</div></div>
    <div class="node"><div class="nt">CloudWatch / Splunk</div></div>
  </div>
  <div class="fcol" style="flex:1;gap:6px">
    <div class="node acc" style="text-align:center"><div class="nt">TRACES</div></div>
    <div class="node soft"><div class="ns">Where time was spent across services</div></div>
    <div class="node"><div class="nt">Jaeger / Zipkin</div></div>
    <div class="node"><div class="nt">AWS X-Ray</div></div>
    <div class="node"><div class="nt">OpenTelemetry</div></div>
  </div>
</div>
<div class="fignote">Metrics say <em>something is wrong</em>, logs say <em>why</em>, traces say <em>where in the call graph</em> — all three needed for full observability.</div></div>
"""

# ---- Distributed tracing waterfall ----
D["b21f17b421d0"] = r"""
<div class="fig"><div class="figcap">Distributed Tracing · Waterfall View</div>
<div class="frow" style="margin-bottom:8px"><span class="chip">TraceID: abc123</span></div>
<div class="gantt">
  <div class="gr"><span class="gl" style="min-width:90px">Service A</span>
    <div class="track"><div class="gseg a" style="width:100%">Span 1 · 0–100ms</div></div></div>
  <div class="gr"><span class="gl" style="min-width:90px">Service B</span>
    <div class="track"><div class="gseg m" style="width:10%"></div><div class="gseg b" style="width:50%">Span 2 · 10–60ms</div></div></div>
  <div class="gr"><span class="gl" style="min-width:90px">DB Query</span>
    <div class="track"><div class="gseg m" style="width:15%"></div><div class="gseg a" style="width:30%">Span 3 · 15–45ms</div></div></div>
  <div class="gr"><span class="gl" style="min-width:90px">Cache hit</span>
    <div class="track"><div class="gseg m" style="width:55%"></div><div class="gseg b" style="width:3%">S4</div></div></div>
  <div class="gr"><span class="gl" style="min-width:90px">Service C</span>
    <div class="track"><div class="gseg m" style="width:65%"></div><div class="gseg b" style="width:30%">Span 5 · 65–95ms</div></div></div>
  <div class="gr"><span class="gl" style="min-width:90px">External API</span>
    <div class="track"><div class="gseg m" style="width:70%"></div><div class="gseg a" style="width:20%">Span 6 · 70–90ms</div></div></div>
</div>
<div class="fignote">Each span records service name, start/end time, parent span ID — Jaeger / Tempo reconstruct the call graph and show the critical path.</div></div>
"""

# ---- Observability pipeline ----
D["34e3f1c4c63a"] = r"""
<div class="fig"><div class="figcap">Observability Pipeline · Collection → Storage → Visualization</div>
<div class="tiers">
  <div class="tier" style="flex:1">
    <div class="th">INSTRUMENTATION</div>
    <div class="fcol" style="gap:6px">
      <div class="node acc"><div class="nt">App (OTel SDK)</div><div class="ns">emits /metrics · structured JSON logs · trace context header</div></div>
    </div>
  </div>
</div>
<div class="ar-d" style="margin:6px 0">↓ &nbsp; scrape / tail / receive &nbsp; ↓</div>
<div class="tiers">
  <div class="tier">
    <div class="th">METRICS</div>
    <div class="node"><div class="nt">Prometheus</div><div class="ns">scrapes /metrics</div></div>
  </div>
  <div class="tier">
    <div class="th">LOGS</div>
    <div class="node"><div class="nt">Fluentd / Vector</div><div class="ns">tails log files</div></div>
  </div>
  <div class="tier">
    <div class="th">TRACES</div>
    <div class="node"><div class="nt">OTel Collector</div><div class="ns">receives spans · batches · exports</div></div>
  </div>
</div>
<div class="ar-d" style="margin:6px 0">↓ &nbsp; store &nbsp; ↓</div>
<div class="tiers">
  <div class="tier">
    <div class="th">TIME-SERIES DB</div>
    <div class="node soft"><div class="nt">Prometheus TSDB</div></div>
  </div>
  <div class="tier">
    <div class="th">LOG STORE</div>
    <div class="node soft"><div class="nt">Elasticsearch / Loki</div></div>
  </div>
  <div class="tier">
    <div class="th">TRACE STORE</div>
    <div class="node soft"><div class="nt">Jaeger / Tempo</div></div>
  </div>
</div>
<div class="ar-d" style="margin:6px 0">↓ &nbsp; visualize &amp; alert &nbsp; ↓</div>
<div class="frow" style="gap:10px">
  <div class="node acc"><div class="nt">Grafana</div><div class="ns">dashboards · SLO tracking · alerts</div></div>
  <div class="node"><div class="nt">Alertmanager</div><div class="ns">PagerDuty · Slack</div></div>
</div>
<div class="fignote">OpenTelemetry standardizes the instrumentation layer — one SDK, any backend (Prometheus, Jaeger, Datadog, etc.).</div></div>
"""

# ---- IaaS / PaaS / SaaS responsibility split ----
D["ef4cfe8f80a5"] = r"""
<div class="fig"><div class="figcap">IaaS · PaaS · SaaS — Shared Responsibility</div>
<div class="matrix" style="grid-template-columns:repeat(4,1fr)">
  <div class="cell hd">Layer</div>
  <div class="cell hd">IaaS</div>
  <div class="cell hd">PaaS</div>
  <div class="cell hd">SaaS</div>

  <div class="cell hd">Applications</div>
  <div class="cell on">You</div>
  <div class="cell on">You</div>
  <div class="cell">Provider</div>

  <div class="cell hd">Data</div>
  <div class="cell on">You</div>
  <div class="cell on">You</div>
  <div class="cell">Provider</div>

  <div class="cell hd">Runtime</div>
  <div class="cell on">You</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>

  <div class="cell hd">Middleware / OS</div>
  <div class="cell on">You</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>

  <div class="cell hd">Hypervisor</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>

  <div class="cell hd">Network / Storage</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>

  <div class="cell hd">Physical</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>
  <div class="cell">Provider</div>
</div>
<div class="frow" style="margin-top:10px;gap:10px;flex-wrap:wrap">
  <div class="node soft"><div class="nt">IaaS examples</div><div class="ns">EC2 · GCE · Azure VM · S3 · VPC</div></div>
  <div class="node soft"><div class="nt">PaaS examples</div><div class="ns">Elastic Beanstalk · Heroku · Cloud Run</div></div>
  <div class="node soft"><div class="nt">SaaS examples</div><div class="ns">Gmail · Salesforce · Slack · Datadog</div></div>
</div>
<div class="fignote">The higher up the stack the provider manages, the less operational burden — but also less control and customization.</div></div>
"""

# ---- CI/CD pipeline (full) ----
D["7c56ee65f059"] = r"""
<div class="fig"><div class="figcap">CI/CD Pipeline · Build → Test → Deploy</div>
<div class="frow" style="flex-wrap:nowrap;gap:8px;margin-bottom:8px">
  <div class="node soft"><div class="nt">Developer</div><div class="ns">git push</div></div>
  <span class="ar">→</span>
  <div class="node"><div class="nt">GitHub / GitLab</div></div>
  <span class="ar">→</span>
  <div class="node acc"><div class="nt">CI System</div><div class="ns">GitHub Actions / Jenkins</div></div>
</div>
<div class="frow sb" style="align-items:flex-start;gap:14px">
  <div class="fcol" style="flex:1;gap:5px">
    <div class="node acc" style="text-align:center;padding:6px"><div class="nt">CI STAGES</div></div>
    <div class="node soft"><div class="ns">1. Checkout code</div></div>
    <div class="node soft"><div class="ns">2. Lint + SAST (SonarQube, Semgrep)</div></div>
    <div class="node soft"><div class="ns">3. Unit tests (pytest, jest)</div></div>
    <div class="node soft"><div class="ns">4. Build Docker image</div></div>
    <div class="node soft"><div class="ns">5. Integration tests</div></div>
    <div class="node soft"><div class="ns">6. Security scan (Trivy, Snyk)</div></div>
    <div class="node acc"><div class="ns">7. Push image → Registry (ECR/GCR) · tag: sha-abc1234</div></div>
  </div>
  <div class="fcol" style="flex:1;gap:5px">
    <div class="node acc" style="text-align:center;padding:6px"><div class="nt">CD STAGES</div></div>
    <div class="node soft"><div class="ns">1. Deploy to Staging</div></div>
    <div class="node soft"><div class="ns">2. Run smoke / e2e tests</div></div>
    <div class="node"><div class="nt">[Manual approval gate]</div></div>
    <div class="node soft"><div class="ns">4. Canary deploy (5% traffic)</div></div>
    <div class="node soft"><div class="ns">5. Monitor SLOs for 30 min</div></div>
    <div class="node acc"><div class="ns">6. Expand to 100% or rollback</div></div>
  </div>
</div>
<div class="fignote">Artifact (image:sha-abc) flows from CI → CD; the sha tag ensures immutable, reproducible deployments.</div></div>
"""

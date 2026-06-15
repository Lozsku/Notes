#!/usr/bin/env python3
"""
Generate professional vector (PDF) diagrams with matplotlib and register them
so build.py appends a "Visual Reference" gallery to the matching editions.

Outputs:
  figures/<key>/NN-name.pdf      vector figures
  figures/figures.json           {key: [[file, caption], ...]}

Run:  python3 diagrams.py     (then re-run build.py to embed them)
"""
import json, math
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Polygon

ROOT = Path(__file__).resolve().parent
FIG  = ROOT / "figures"
FIG.mkdir(exist_ok=True)

# ---------------- shared professional style ----------------
INK, INK2, GRID = "#12172a", "#4b5468", "#e2e6ef"
plt.rcParams.update({
    "figure.dpi": 140, "savefig.dpi": 140,
    "font.family": "DejaVu Sans", "font.size": 10.5,
    "axes.edgecolor": INK2, "axes.labelcolor": INK, "axes.titlecolor": INK,
    "axes.titlesize": 12.5, "axes.titleweight": "bold", "axes.labelsize": 10.5,
    "axes.linewidth": 0.9, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "legend.frameon": True, "legend.edgecolor": GRID, "legend.framealpha": 0.95,
    "axes.spines.top": False, "axes.spines.right": False,
    "savefig.bbox": "tight", "savefig.pad_inches": 0.12,
})
REG_FIGS = {}   # key -> list of (filename, caption)

def _save(key, name, fig, caption):
    d = FIG / key; d.mkdir(parents=True, exist_ok=True)
    fn = f"{name}.pdf"
    fig.savefig(d / fn)
    plt.close(fig)
    REG_FIGS.setdefault(key, []).append([fn, caption])
    print(f"  + {key}/{fn}")

def acc(key, default="#6366f1"):
    return {
        "01-concurrency": "#6366f1", "02-os": "#0ea5a4", "03-networks": "#2563eb",
        "04-cloud": "#7c3aed", "05-system-design": "#db2777", "06-lld": "#ea580c",
        "07-distributed": "#0891b2", "08-databases": "#059669", "09-performance": "#d97706",
        "10-security": "#dc2626", "11-behavioral": "#9333ea",
        "dsa-01-patterns": "#be123c", "dsa-02-ds": "#be123c", "dsa-03-algos": "#be123c",
        "aiml-01-fund": "#7c3aed", "aiml-02-classic": "#7c3aed", "aiml-03-dl": "#7c3aed",
        "aiml-04-tf": "#7c3aed", "aiml-05-genai": "#7c3aed", "aiml-06-mlops": "#7c3aed",
        "sdp-1": "#db2777", "sdp-2": "#db2777", "lld-coded": "#ea580c",
    }.get(key, default)

# ---------------- reusable drawing helpers (box / arrow / lifelines) --------
def _canvas(figsize, title, xlim=(0, 10), ylim=(0, 10)):
    fig, ax = plt.subplots(figsize=figsize)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.axis("off")
    ax.set_aspect("auto")
    if title:
        ax.set_title(title, color=INK, fontsize=12.5, weight="bold", pad=10)
    return fig, ax

def _tint(hexc, p):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i+2], 16) for i in (0, 2, 4))
    r, g, b = (int(v + (255 - v) * p) for v in (r, g, b))
    return f"#{r:02x}{g:02x}{b:02x}"

def _box(ax, cx, cy, w, h, title, sub=None, fc=None, ec="#6366f1", fs=9.5):
    fc = fc if fc is not None else _tint(ec, 0.86)
    ax.add_patch(FancyBboxPatch((cx-w/2, cy-h/2), w, h,
                 boxstyle="round,pad=0.02,rounding_size=0.10", fc=fc, ec=ec, lw=1.6))
    if sub:
        ax.text(cx, cy+h*0.17, title, ha="center", va="center", fontsize=fs, weight="bold", color=INK)
        ax.text(cx, cy-h*0.23, sub, ha="center", va="center", fontsize=fs-2.4, color=INK2)
    else:
        ax.text(cx, cy, title, ha="center", va="center", fontsize=fs, weight="bold", color=INK)
    return (cx, cy)

def _arrow(ax, p1, p2, color=INK2, lw=1.6, text=None, rad=0.0, ls="-", two=False):
    style = "<|-|>" if two else "-|>"
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=13, lw=lw,
                 color=color, connectionstyle=f"arc3,rad={rad}", ls=ls, shrinkA=3, shrinkB=3))
    if text:
        mx, my = (p1[0]+p2[0])/2, (p1[1]+p2[1])/2
        ax.text(mx, my+0.2, text, ha="center", fontsize=7.8, color=color,
                bbox=dict(fc="white", ec="none", pad=0.6))

# ===================================================================
#  FIGURES
# ===================================================================
def amdahl():
    key = "01-concurrency"; c = acc(key)
    n = np.linspace(1, 256, 400)
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    for p, col in [(0.50, "#cbd5e1"), (0.75, "#a5b4fc"), (0.90, "#818cf8"),
                   (0.95, c), (0.99, "#4338ca")]:
        s = 1 / ((1 - p) + p / n)
        ax.plot(n, s, color=col, lw=2.2, label=f"{int(p*100)}% parallel")
    ax.set_xscale("log", base=2)
    ax.set_xlabel("Number of processors"); ax.set_ylabel("Speedup")
    ax.set_title("Amdahl's Law — diminishing returns of parallelism")
    ax.legend(title="Parallel fraction", fontsize=8.5, title_fontsize=9, loc="upper left")
    ax.set_xlim(1, 256)
    _save(key, "01-amdahls-law", fig,
          "Amdahl's Law: maximum speedup is capped by the serial fraction. Even at "
          "95\\% parallel, 256 cores yield only ~17x — the serial 5\\% dominates.")

def bias_variance():
    key = "aiml-01-fund"; c = acc(key)
    x = np.linspace(0, 10, 200)
    bias2 = 3.2 * np.exp(-0.45 * x) + 0.05
    var   = 0.06 * np.exp(0.42 * x) * 0.02 + 0.04 * np.exp(0.34 * x)
    total = bias2 + var + 0.25
    fig, ax = plt.subplots(figsize=(6.2, 3.8))
    ax.plot(x, bias2, color="#2563eb", lw=2.2, label="Bias$^2$")
    ax.plot(x, var, color="#dc2626", lw=2.2, label="Variance")
    ax.plot(x, total, color=c, lw=2.8, label="Total error")
    xo = x[np.argmin(total)]
    ax.axvline(xo, color=INK2, ls="--", lw=1.1)
    ax.annotate("optimal\ncapacity", (xo, np.min(total)), (xo + 0.6, np.min(total) + 1.1),
                color=INK, fontsize=9, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.fill_between(x, 0, total, where=(x < xo), color="#2563eb", alpha=0.05)
    ax.fill_between(x, 0, total, where=(x >= xo), color="#dc2626", alpha=0.05)
    ax.text(1.2, 3.4, "underfit", color="#2563eb", fontsize=9, weight="bold")
    ax.text(8.0, 3.4, "overfit", color="#dc2626", fontsize=9, weight="bold")
    ax.set_xlabel("Model complexity"); ax.set_ylabel("Error")
    ax.set_title("Bias–Variance Tradeoff"); ax.set_ylim(0, 4); ax.set_xticks([])
    ax.legend(loc="upper center", ncol=3, fontsize=8.5)
    _save(key, "01-bias-variance", fig,
          "Total generalization error decomposes into bias$^2$ + variance + irreducible "
          "noise. Minimizing it means balancing model capacity, not maximizing fit.")

def learning_curves():
    key = "aiml-01-fund"; c = acc(key)
    m = np.linspace(20, 1000, 200)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.4), sharey=True)
    # high bias
    tr = 0.62 - 0.02 * np.exp(-m / 200); val = 0.60 + 0.02 * np.exp(-m / 200)
    a1.plot(m, tr, color="#2563eb", lw=2.2, label="train")
    a1.plot(m, val, color="#dc2626", lw=2.2, label="validation")
    a1.axhline(0.2, color=INK2, ls=":", lw=1); a1.set_title("High bias (underfit)")
    a1.set_xlabel("Training set size"); a1.set_ylabel("Error"); a1.legend(fontsize=8.5)
    # high variance
    tr2 = 0.08 + 0.04 * np.exp(-m / 300); val2 = 0.45 - 0.22 * (1 - np.exp(-m / 350))
    a2.plot(m, tr2, color="#2563eb", lw=2.2, label="train")
    a2.plot(m, val2, color="#dc2626", lw=2.2, label="validation")
    a2.fill_between(m, tr2, val2, color=c, alpha=0.08)
    a2.set_title("High variance (overfit)"); a2.set_xlabel("Training set size")
    a2.legend(fontsize=8.5)
    fig.suptitle("Diagnosing models with learning curves", fontsize=12.5, weight="bold", color=INK)
    _save(key, "02-learning-curves", fig,
          "A large train–validation gap that closes with more data signals variance; "
          "high error on both that more data won't fix signals bias.")

def roc_pr():
    key = "aiml-02-classic"; c = acc(key)
    fig, (a1, a2) = plt.subplots(1, 2, figsize=(7.2, 3.5))
    fpr = np.linspace(0, 1, 200)
    for auc, col, lab in [(0.95, c, "strong (AUC 0.95)"), (0.80, "#a78bfa", "fair (AUC 0.80)"),
                          (0.5, "#cbd5e1", "random (0.50)")]:
        g = 1 - (1 - fpr) ** (1 / (1 - auc + 1e-6) * 0.18 + 1) if auc > 0.5 else fpr
        a1.plot(fpr, g, color=col, lw=2.4, label=lab)
    a1.plot([0, 1], [0, 1], color=INK2, ls="--", lw=1)
    a1.set_xlabel("False positive rate"); a1.set_ylabel("True positive rate")
    a1.set_title("ROC curve"); a1.legend(fontsize=8, loc="lower right")
    r = np.linspace(0, 1, 200)
    for k, col, lab in [(0.92, c, "strong"), (0.7, "#a78bfa", "fair"), (0.3, "#cbd5e1", "weak")]:
        p = k / (k + (1 - k) * r ** 1.5) * (1 - 0.15 * r)
        a2.plot(r, p, color=col, lw=2.4, label=lab)
    a2.set_xlabel("Recall"); a2.set_ylabel("Precision"); a2.set_ylim(0, 1.02)
    a2.set_title("Precision–Recall curve"); a2.legend(fontsize=8, loc="lower left")
    fig.suptitle("Threshold-free classifier evaluation", fontsize=12, weight="bold", color=INK)
    _save(key, "01-roc-pr", fig,
          "ROC summarizes ranking quality across thresholds; PR is more informative under "
          "heavy class imbalance, where a high AUC can still hide poor precision.")

def activations():
    key = "aiml-03-dl"; c = acc(key)
    x = np.linspace(-5, 5, 400)
    fns = [("ReLU", np.maximum(0, x), c),
           ("Sigmoid", 1/(1+np.exp(-x)), "#dc2626"),
           ("Tanh", np.tanh(x), "#2563eb"),
           ("GELU", 0.5*x*(1+np.tanh(math.sqrt(2/math.pi)*(x+0.044715*x**3))), "#059669"),
           ("Leaky ReLU", np.where(x>0, x, 0.1*x), "#d97706")]
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for name, y, col in fns:
        ax.plot(x, y, color=col, lw=2.2, label=name)
    ax.axhline(0, color=INK2, lw=0.8); ax.axvline(0, color=INK2, lw=0.8)
    ax.set_title("Neural-network activation functions")
    ax.set_xlabel("input"); ax.set_ylabel("output"); ax.set_ylim(-1.5, 4)
    ax.legend(fontsize=8.5, loc="upper left")
    _save(key, "01-activations", fig,
          "Nonlinearities let networks model non-linear functions. ReLU/GELU dominate deep "
          "nets (cheap, no saturation for x>0); sigmoid/tanh saturate and can vanish gradients.")

def grad_descent():
    key = "aiml-03-dl"; c = acc(key)
    a, b = 14.0, 1.0                          # ill-conditioned bowl, min at (0,0)
    f = lambda x, y: 0.5 * (a * x**2 + b * y**2)
    X, Y = np.meshgrid(np.linspace(-2.2, 2.2, 240), np.linspace(-2.6, 2.6, 240))
    Z = f(X, Y)
    fig, ax = plt.subplots(figsize=(6.0, 3.9))
    ax.contour(X, Y, Z, levels=np.linspace(0.4, 30, 14), cmap="Purples_r", linewidths=0.9)
    px, py, lr = -2.0, 2.4, 0.13             # exact gradient: (a*x, b*y)
    pts = [(px, py)]
    for _ in range(40):
        px -= lr * a * px; py -= lr * b * py; pts.append((px, py))
    pts = np.array(pts)
    ax.plot(pts[:, 0], pts[:, 1], "-o", color=c, ms=3.2, lw=1.6, label="gradient descent")
    ax.plot(0, 0, "*", color="#dc2626", ms=16, label="minimum")
    ax.set_title("Gradient descent on an ill-conditioned loss")
    ax.set_xlabel(r"$\theta_1$"); ax.set_ylabel(r"$\theta_2$")
    ax.set_xlim(-2.3, 2.3); ax.set_ylim(-2.7, 2.7); ax.legend(fontsize=8.5, loc="upper right")
    _save(key, "02-gradient-descent", fig,
          "Each step moves opposite the gradient. Elongated (ill-conditioned) valleys make "
          "vanilla gradient descent zig-zag across the steep axis — motivating momentum, "
          "RMSProp and Adam.")

def big_o():
    key = "dsa-03-algos"; c = acc(key)
    n = np.linspace(1, 40, 200)
    curves = [("O(1)", np.ones_like(n), "#10b981"),
              ("O(log n)", np.log2(n), "#22c55e"),
              ("O(n)", n, "#2563eb"),
              ("O(n log n)", n*np.log2(n), "#8b5cf6"),
              ("O(n²)", n**2, "#d97706"),
              ("O(2ⁿ)", 2**np.minimum(n, 20), "#dc2626")]
    fig, ax = plt.subplots(figsize=(6.2, 4.0))
    for name, y, col in curves:
        ax.plot(n, y, color=col, lw=2.3, label=name)
    ax.set_ylim(1, 1000); ax.set_xlim(1, 40)
    ax.set_title("Big-O growth — why complexity class dominates")
    ax.set_xlabel("input size  n"); ax.set_ylabel("operations")
    ax.legend(fontsize=8.5, loc="upper left", ncol=2)
    _save(key, "01-big-o-growth", fig,
          "Asymptotic class, not constant factors, decides scalability. Beyond modest n, "
          "an O(n log n) algorithm crushes O(n²); exponential is infeasible past ~n=30.")

def latency_ladder():
    key = "09-performance"; c = acc(key)
    items = [("L1 cache ref", 1), ("Branch mispredict", 3), ("L2 cache ref", 4),
             ("Mutex lock/unlock", 17), ("Main memory ref", 100),
             ("Compress 1KB (zippy)", 2000), ("Send 1KB over 1Gbps", 10000),
             ("SSD random read", 16000), ("Round trip in datacenter", 500000),
             ("Disk seek", 2_000_000), ("Send packet CA→NL→CA", 150_000_000)]
    labels = [a for a, _ in items]; vals = [b for _, b in items]
    fig, ax = plt.subplots(figsize=(6.8, 4.4))
    ypos = np.arange(len(items))[::-1]
    cols = plt.cm.plasma(np.linspace(0.05, 0.85, len(items)))
    ax.barh(ypos, vals, color=cols, height=0.66)
    ax.set_xscale("log")
    ax.set_yticks(ypos); ax.set_yticklabels(labels, fontsize=9)
    ax.set_xlabel("nanoseconds (log scale)")
    ax.set_title("Latency numbers every engineer should know")
    for y, v in zip(ypos, vals):
        t = f"{v} ns" if v < 1000 else (f"{v/1000:.0f} µs" if v < 1e6 else f"{v/1e6:.0f} ms")
        ax.text(v*1.25, y, t, va="center", fontsize=8, color=INK2)
    ax.set_xlim(0.7, 5e9); ax.grid(axis="y", visible=False)
    _save(key, "01-latency-ladder", fig,
          "Orders of magnitude separate cache, memory, SSD, disk and network. Designing for "
          "performance means counting which tier each operation touches.")

def cap_theorem():
    key = "07-distributed"; c = acc(key)
    fig, ax = plt.subplots(figsize=(5.6, 4.6)); ax.axis("off"); ax.set_aspect("equal")
    P = {"C": (0, 1.0), "A": (-0.92, -0.55), "P": (0.92, -0.55)}
    tri = Polygon([P["C"], P["A"], P["P"]], closed=True, fc=c, ec=c, alpha=0.08, lw=2)
    ax.add_patch(tri)
    for k, (x, y) in P.items():
        ax.plot(x, y, "o", ms=46, color=c, alpha=0.95)
        ax.text(x, y, k, ha="center", va="center", color="white", fontsize=16, weight="bold")
    names = {"C": "Consistency", "A": "Availability", "P": "Partition\ntolerance"}
    offs = {"C": (0, 0.28), "A": (-0.18, -0.28), "P": (0.18, -0.28)}
    for k, (x, y) in P.items():
        dx, dy = offs[k]; ax.text(x+dx, y+dy, names[k], ha="center", va="center",
                                  fontsize=9.5, color=INK, weight="bold")
    edges = {(0.0, 0.18): "CA: single-node / RDBMS\n(no partition tolerance)",
             (0.50, 0.18): "CP: HBase, etcd, Zookeeper\n(reject writes to stay consistent)",
             (-0.50, 0.18): "AP: Cassandra, Dynamo\n(serve stale, reconcile later)"}
    ax.text(0.0, -0.95, "CA", ha="center", color=INK2, fontsize=9, style="italic")
    ax.text(-0.62, 0.25, "AP", ha="center", color=INK2, fontsize=9, style="italic", rotation=58)
    ax.text(0.62, 0.25, "CP", ha="center", color=INK2, fontsize=9, style="italic", rotation=-58)
    ax.set_title("CAP theorem — pick two under a network partition", color=INK,
                 fontsize=12.5, weight="bold")
    ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.2, 1.5)
    _save(key, "01-cap-theorem", fig,
          "When the network partitions, a distributed store must sacrifice either "
          "consistency (AP) or availability (CP). Partition tolerance is non-negotiable.")

def osi_stack():
    key = "03-networks"; c = acc(key)
    layers = [("7  Application", "HTTP, DNS, TLS, gRPC"),
              ("6  Presentation", "encoding, TLS, compression"),
              ("5  Session", "sessions, RPC, sockets"),
              ("4  Transport", "TCP, UDP, QUIC — ports"),
              ("3  Network", "IP, ICMP, routing — addresses"),
              ("2  Data Link", "Ethernet, ARP, MAC — frames"),
              ("1  Physical", "cables, radio, signals — bits")]
    fig, ax = plt.subplots(figsize=(6.6, 4.4)); ax.axis("off")
    ax.set_xlim(0, 10); ax.set_ylim(0, len(layers))
    cols = plt.cm.Blues(np.linspace(0.78, 0.30, len(layers)))
    for i, ((name, detail), col) in enumerate(zip(layers, cols)):
        y = len(layers) - 1 - i
        box = FancyBboxPatch((0.3, y+0.12), 9.4, 0.76, boxstyle="round,pad=0.02,rounding_size=0.08",
                             fc=col, ec="white", lw=1.4)
        ax.add_patch(box)
        ax.text(0.6, y+0.5, name, va="center", fontsize=10.5, weight="bold", color=INK)
        ax.text(9.4, y+0.5, detail, va="center", ha="right", fontsize=8.8, color=INK2)
    ax.annotate("", xy=(0.08, 0.2), xytext=(0.08, len(layers)-0.2),
                arrowprops=dict(arrowstyle="<->", color=c, lw=1.6))
    ax.text(-0.05, len(layers)/2, "encapsulation", rotation=90, va="center",
            ha="center", color=c, fontsize=9, weight="bold")
    ax.set_title("The OSI / TCP-IP layered model", color=INK, fontsize=12.5, weight="bold")
    _save(key, "01-osi-stack", fig,
          "Each layer adds a header and treats the layer above as opaque payload. "
          "Interview framing: name the layer, its addressing unit, and a protocol.")

def scheduling_gantt():
    key = "02-os"; c = acc(key)
    # processes: (name, arrival, burst)
    fig, (a1, a2) = plt.subplots(2, 1, figsize=(6.8, 4.0), sharex=True)
    cols = {"P1": "#0ea5a4", "P2": "#6366f1", "P3": "#d97706", "P4": "#dc2626"}
    # FCFS
    fcfs = [("P1", 0, 7), ("P2", 7, 4), ("P3", 11, 1), ("P4", 12, 4)]
    for name, s, d in fcfs:
        a1.barh(0, d, left=s, color=cols[name], edgecolor="white")
        a1.text(s+d/2, 0, name, ha="center", va="center", color="white", weight="bold", fontsize=9)
    a1.set_yticks([]); a1.set_title("FCFS — convoy effect (long job blocks short ones)", fontsize=11)
    # Round Robin q=2
    rr = [("P1",0,2),("P2",2,2),("P1",4,2),("P3",6,1),("P4",7,2),("P1",9,2),
          ("P2",11,2),("P4",13,2),("P1",15,1)]
    for name, s, d in rr:
        a2.barh(0, d, left=s, color=cols[name], edgecolor="white")
        a2.text(s+d/2, 0, name, ha="center", va="center", color="white", weight="bold", fontsize=8)
    a2.set_yticks([]); a2.set_title("Round Robin (q=2) — fair, responsive, more context switches", fontsize=11)
    a2.set_xlabel("time"); a2.set_xlim(0, 16)
    fig.suptitle("CPU scheduling: FCFS vs Round Robin", fontsize=12.5, weight="bold", color=INK)
    _save(key, "01-scheduling-gantt", fig,
          "FCFS is simple but suffers the convoy effect; Round Robin time-slices for fairness "
          "and responsiveness at the cost of extra context switches.")

def attention_heatmap():
    key = "aiml-04-tf"; c = acc(key)
    toks = ["The", "cat", "sat", "on", "the", "mat"]
    n = len(toks); rng = np.random.default_rng(7)
    A = rng.random((n, n)) * 0.3
    A[1, 0] += 0.7; A[2, 1] += 0.8; A[5, 1] += 0.6; A[3, 2] += 0.6; A[4, 0] += 0.5
    A = A / A.sum(1, keepdims=True)
    fig, ax = plt.subplots(figsize=(5.4, 4.6))
    im = ax.imshow(A, cmap="Purples", aspect="auto")
    ax.set_xticks(range(n)); ax.set_xticklabels(toks)
    ax.set_yticks(range(n)); ax.set_yticklabels(toks)
    ax.set_xlabel("attends to (key)"); ax.set_ylabel("query token")
    for i in range(n):
        for j in range(n):
            ax.text(j, i, f"{A[i,j]:.2f}", ha="center", va="center",
                    color="white" if A[i, j] > 0.4 else INK2, fontsize=7.5)
    ax.set_title("Self-attention weights (one head)", color=INK, fontsize=12.5, weight="bold")
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04, label="attention weight")
    ax.grid(False)
    _save(key, "01-attention", fig,
          "Each query token forms a weighted average over all tokens via softmax(QKᵀ/√d). "
          "Rows sum to 1 — the model learns which context positions matter.")

# ===================================================================
#  NEW FIGURES — remaining editions
# ===================================================================
def cloud_autoscaling():
    key = "04-cloud"; c = acc(key)
    t = np.linspace(0, 24, 300)
    demand = 40 + 38*np.sin((t-7)/24*2*np.pi) + 18*np.exp(-((t-13)/2.2)**2) + 10*np.exp(-((t-19)/1.6)**2)
    demand = np.clip(demand, 12, None)
    fixed = np.full_like(t, demand.max())
    steps = np.ceil(demand/15)*15
    fig, ax = plt.subplots(figsize=(6.6, 3.8))
    ax.plot(t, demand, color=c, lw=2.6, label="actual demand", zorder=5)
    ax.plot(t, fixed, color="#dc2626", lw=1.8, ls="--", label="static (peak) provisioning")
    ax.step(t, steps, color="#059669", lw=2.0, where="mid", label="auto-scaled capacity")
    ax.fill_between(t, demand, fixed, color="#dc2626", alpha=0.07)
    ax.fill_between(t, demand, steps, where=(steps>=demand), color="#059669", alpha=0.10)
    ax.set_xlabel("hour of day"); ax.set_ylabel("capacity (instances·load)")
    ax.set_title("Autoscaling vs static provisioning")
    ax.set_xlim(0, 24); ax.set_xticks(range(0, 25, 4)); ax.legend(fontsize=8.3, loc="upper left")
    _save(key, "01-autoscaling", fig,
          "Static peak provisioning wastes capacity (red area) most of the day. Autoscaling "
          "tracks demand in steps, trading a little headroom for large cost savings.")

def shared_responsibility():
    key = "04-cloud"; c = acc(key)
    rows = ["Data & access", "Application", "Runtime", "OS", "Virtualization",
            "Servers", "Storage", "Networking"]
    models = ["On-Prem", "IaaS", "PaaS", "SaaS"]
    # 1 = customer manages, 0 = provider manages
    M = np.array([
        [1,1,1,1],[1,1,1,0],[1,1,0,0],[1,0,0,0],
        [1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]])
    fig, ax = plt.subplots(figsize=(6.4, 4.2))
    for j in range(4):
        for i in range(8):
            cust = M[i, j]
            ax.add_patch(FancyBboxPatch((j+0.06, 7-i+0.06), 0.88, 0.88,
                boxstyle="round,pad=0.01,rounding_size=0.05",
                fc=_tint(c, 0.78) if cust else _tint("#64748b", 0.80),
                ec=c if cust else "#94a3b8", lw=1.1))
    for i, r in enumerate(rows):
        ax.text(-0.15, 7-i+0.5, r, ha="right", va="center", fontsize=8.6, color=INK)
    for j, m in enumerate(models):
        ax.text(j+0.5, 8.25, m, ha="center", fontsize=10, weight="bold", color=c)
    ax.add_patch(FancyBboxPatch((4.4, 6.4), 0.5, 0.5, boxstyle="round,pad=0.01", fc=_tint(c,0.78), ec=c))
    ax.text(5.0, 6.65, "you manage", va="center", fontsize=8.4, color=INK)
    ax.add_patch(FancyBboxPatch((4.4, 5.6), 0.5, 0.5, boxstyle="round,pad=0.01", fc=_tint("#64748b",0.80), ec="#94a3b8"))
    ax.text(5.0, 5.85, "provider manages", va="center", fontsize=8.4, color=INK)
    ax.set_xlim(-2.2, 6.5); ax.set_ylim(-0.2, 8.7); ax.axis("off")
    ax.set_title("Cloud shared-responsibility model", color=INK, fontsize=12.5, weight="bold")
    _save(key, "02-shared-responsibility", fig,
          "Moving from IaaS to SaaS hands more of the stack to the provider. Knowing the "
          "boundary tells you what you must still secure, patch and scale yourself.")

def web_architecture():
    key = "05-system-design"; c = acc(key)
    fig, ax = _canvas((7.2, 4.2), "Anatomy of a scalable web service", (0, 12), (0, 10))
    _box(ax, 1.2, 5, 1.7, 1.3, "Client", "web / mobile", ec=c)
    _box(ax, 3.5, 5, 1.6, 1.2, "CDN", "edge cache", ec=c)
    _box(ax, 5.7, 5, 1.7, 1.2, "Load\nBalancer", ec=c)
    for i, y in enumerate([7.4, 5, 2.6]):
        _box(ax, 8.0, y, 1.5, 1.0, f"App {i+1}", ec=c, fs=8.6)
    _box(ax, 10.6, 6.6, 1.7, 1.1, "Cache", "Redis", ec="#059669")
    _box(ax, 10.6, 3.8, 1.7, 1.1, "Primary DB", "writes", ec="#2563eb")
    _box(ax, 10.6, 1.7, 1.7, 0.9, "Replica", "reads", ec="#2563eb", fs=8.4)
    _arrow(ax, (2.05, 5), (2.7, 5), c); _arrow(ax, (4.3, 5), (4.85, 5), c)
    _arrow(ax, (6.55, 5), (7.25, 7.2), c); _arrow(ax, (6.55, 5), (7.25, 5), c)
    _arrow(ax, (6.55, 5), (7.25, 2.8), c)
    for y in [7.4, 5, 2.6]:
        _arrow(ax, (8.75, y), (9.75, 6.6), "#059669", rad=0.05)
        _arrow(ax, (8.75, y), (9.75, 3.8), "#2563eb", rad=-0.05)
    _arrow(ax, (10.6, 3.25), (10.6, 2.15), "#2563eb", text="replicate")
    ax.text(6, 0.4, "stateless app tier scales horizontally  •  state pushed to cache + DB",
            ha="center", fontsize=8.6, color=INK2, style="italic")
    _save(key, "01-web-architecture", fig,
          "The canonical pattern: stateless app servers behind a load balancer, a CDN for "
          "static edge content, a cache to absorb reads, and a primary DB with read replicas.")

def latency_throughput():
    key = "05-system-design"; c = acc(key)
    q = np.linspace(0, 1.0, 300)
    lat = 20 + 8*q + 180*q**6/(1.001-q)
    fig, ax = plt.subplots(figsize=(6.2, 3.7))
    ax.plot(q*100, lat, color=c, lw=2.6)
    knee = 0.72
    ax.axvline(knee*100, color=INK2, ls="--", lw=1.1)
    ax.annotate("the knee:\nqueues explode", (knee*100, 70), (knee*100-34, 150),
                fontsize=9, color=INK, arrowprops=dict(arrowstyle="->", color=INK2))
    ax.fill_between(q*100, 0, lat, where=(q<knee), color="#059669", alpha=0.07)
    ax.fill_between(q*100, 0, lat, where=(q>=knee), color="#dc2626", alpha=0.07)
    ax.set_xlabel("utilization (% of capacity)"); ax.set_ylabel("latency (ms)")
    ax.set_title("Latency vs utilization — Little's Law in action")
    ax.set_ylim(0, 260); ax.set_xlim(0, 100)
    _save(key, "02-latency-utilization", fig,
          "Latency stays flat until utilization approaches capacity, then rises sharply as "
          "queues build. Plan for headroom — running hot (>70-80\\%) is a tail-latency trap.")

def strategy_pattern():
    key = "06-lld"; c = acc(key)
    fig, ax = _canvas((6.8, 4.3), "Strategy pattern (composition over inheritance)", (0, 12), (0, 10))
    _box(ax, 2.6, 8, 3.2, 1.4, "Context", "- strategy: Strategy\n+ execute()", ec=c, fs=9)
    _box(ax, 8.4, 8, 3.4, 1.2, "«interface»\nStrategy", "+ algorithm()", ec="#2563eb", fs=9)
    _arrow(ax, (4.25, 8), (6.65, 8), INK2, text="has-a")
    for i, (nm) in enumerate(["ConcreteA", "ConcreteB", "ConcreteC"]):
        x = 4.4 + i*3.0
        _box(ax, x, 3.4, 2.5, 1.1, nm, "+ algorithm()", ec="#059669", fs=8.6)
        _arrow(ax, (x, 3.97), (8.4, 7.35), "#059669", rad=0.0, ls="--")
    ax.text(8.4, 5.6, "realizes ▲", ha="center", fontsize=8, color=INK2)
    ax.text(6, 1.3, "swap algorithms at runtime without touching Context — open/closed principle",
            ha="center", fontsize=8.8, color=INK2, style="italic")
    _save(key, "01-strategy-pattern", fig,
          "Strategy encapsulates interchangeable algorithms behind one interface. The Context "
          "delegates to a strategy object, so new behaviors are added without modifying it.")

def btree():
    key = "08-databases"; c = acc(key)
    fig, ax = _canvas((7.0, 3.8), "B+ tree index — logarithmic lookups, sorted leaves", (0, 12), (0, 8))
    _box(ax, 6, 7, 1.8, 0.9, "[ 30 | 60 ]", ec=c, fs=9)
    mids = [(2.4, "[10|20]"), (6.0, "[40|50]"), (9.6, "[70|80]")]
    for x, lab in mids:
        _box(ax, x, 4.3, 1.7, 0.85, lab, ec="#2563eb", fs=8.6)
        _arrow(ax, (6, 6.55), (x, 4.75), INK2)
    leaves = ["5 10", "20 25", "35 40", "50 55", "65 70", "80 90"]
    lx = np.linspace(1.4, 10.6, 6)
    for x, lab in zip(lx, leaves):
        _box(ax, x, 1.5, 1.35, 0.8, lab, ec="#059669", fs=8.2)
    for i, (mx, _) in enumerate(mids):
        _arrow(ax, (mx, 3.88), (lx[2*i], 1.9), INK2)
        _arrow(ax, (mx, 3.88), (lx[2*i+1], 1.9), INK2)
    for i in range(5):
        _arrow(ax, (lx[i]+0.7, 1.5), (lx[i+1]-0.7, 1.5), "#059669", rad=0, ls=":")
    ax.text(6, 0.4, "internal nodes route  •  leaves hold sorted keys + are linked for range scans",
            ha="center", fontsize=8.4, color=INK2, style="italic")
    _save(key, "01-btree", fig,
          "B+ trees keep data sorted with a high branching factor, so lookups touch only "
          "O(log n) nodes (few disk pages). Linked leaves make range queries cheap.")

def isolation_levels():
    key = "08-databases"; c = acc(key)
    levels = ["Read\nUncommitted", "Read\nCommitted", "Repeatable\nRead", "Serializable"]
    anoms = ["Dirty read", "Non-repeatable\nread", "Phantom\nread", "Lost\nupdate"]
    # 1 = possible (bad)
    M = np.array([[1,1,1,1],[0,1,1,1],[0,0,1,1],[0,0,0,0]])
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    for i in range(4):
        for j in range(4):
            bad = M[i, j]
            ax.add_patch(FancyBboxPatch((j+0.06, 3-i+0.06), 0.88, 0.88,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                fc="#fde2e2" if bad else "#d6f3e4", ec="#dc2626" if bad else "#059669", lw=1.3))
            ax.text(j+0.5, 3-i+0.5, "possible" if bad else "prevented",
                    ha="center", va="center", fontsize=7.6,
                    color="#b91c1c" if bad else "#047857", weight="bold")
    for j, a in enumerate(anoms):
        ax.text(j+0.5, 4.18, a, ha="center", va="center", fontsize=8, color=INK)
    for i, l in enumerate(levels):
        ax.text(-0.12, 3-i+0.5, l, ha="right", va="center", fontsize=8.4, weight="bold", color=c)
    ax.set_xlim(-2.0, 4.2); ax.set_ylim(-0.1, 4.7); ax.axis("off")
    ax.set_title("SQL isolation levels vs anomalies", color=INK, fontsize=12.5, weight="bold")
    _save(key, "02-isolation-levels", fig,
          "Stronger isolation prevents more anomalies but costs concurrency. Serializable is "
          "safest; most OLTP systems default to Read Committed and add locks where needed.")

def tls_handshake():
    key = "10-security"; c = acc(key)
    fig, ax = _canvas((6.8, 4.4), "TLS 1.3 handshake — 1 round trip to encryption", (0, 10), (0, 11))
    cx, sx = 1.8, 8.2
    for x, nm in [(cx, "Client"), (sx, "Server")]:
        _box(ax, x, 10.2, 2.0, 0.9, nm, ec=c, fs=10)
        ax.plot([x, x], [0.4, 9.6], color="#cbd5e1", lw=1.4, zorder=0)
    msgs = [(9.0, "→", "ClientHello + key share", c),
            (7.6, "←", "ServerHello + key share", "#2563eb"),
            (6.6, "←", "{Certificate, Finished}", "#2563eb"),
            (5.2, "→", "{Finished}", c),
            (3.8, "↔", "Application data (encrypted)", "#059669")]
    for y, d, txt, col in msgs:
        if d == "→":
            _arrow(ax, (cx+0.2, y), (sx-0.2, y), col)
        elif d == "←":
            _arrow(ax, (sx-0.2, y), (cx+0.2, y), col)
        else:
            _arrow(ax, (cx+0.2, y), (sx-0.2, y), col, two=True, ls="-")
        ax.text(5.0, y+0.22, txt, ha="center", fontsize=8.2, color=col,
                bbox=dict(fc="white", ec="none", pad=0.5))
    ax.text(5.0, 4.8, "{ } = encrypted", ha="center", fontsize=7.6, color=INK2, style="italic")
    _save(key, "01-tls-handshake", fig,
          "TLS 1.3 establishes a shared secret via key shares in the first flight, so "
          "encrypted application data flows after just one round trip (0-RTT on resumption).")

def defense_in_depth():
    key = "10-security"; c = acc(key)
    fig, ax = plt.subplots(figsize=(5.6, 4.6)); ax.set_aspect("equal"); ax.axis("off")
    layers = [("Data\n(encryption, secrets)", 1.1, "#dc2626"),
              ("Application\n(authz, input validation)", 2.0, "#ea580c"),
              ("Host\n(hardening, patching)", 2.9, "#d97706"),
              ("Network\n(segmentation, firewall)", 3.8, "#65a30d"),
              ("Perimeter\n(WAF, DDoS, IAM)", 4.7, "#0891b2")]
    for label, r, col in reversed(layers):
        ax.add_patch(plt.Circle((0, 0), r, fc=_tint(col, 0.82), ec=col, lw=1.8))
    for label, r, col in layers:
        ax.text(0, r-0.42 if r > 1.2 else 0, label, ha="center", va="center",
                fontsize=7.8, color=INK, weight="bold")
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5.2)
    ax.set_title("Defense in depth — layered controls", color=INK, fontsize=12.5, weight="bold")
    _save(key, "02-defense-in-depth", fig,
          "No single control is trusted alone. Independent layers — perimeter, network, host, "
          "app, data — mean an attacker must defeat each in turn.")

def star_method():
    key = "11-behavioral"; c = acc(key)
    fig, ax = _canvas((7.2, 2.8), "The STAR method for behavioral answers", (0, 12.5), (0, 4))
    steps = [("S", "Situation", "set the context", "#9333ea"),
             ("T", "Task", "your responsibility", "#7c3aed"),
             ("A", "Action", "what YOU did", "#6366f1"),
             ("R", "Result", "quantified outcome", "#2563eb")]
    for i, (L, name, sub, col) in enumerate(steps):
        x = 1.6 + i*3.0
        ax.add_patch(plt.Circle((x, 2.9), 0.42, fc=col, ec="white", lw=2, zorder=4))
        ax.text(x, 2.9, L, ha="center", va="center", color="white", fontsize=14, weight="bold", zorder=5)
        _box(ax, x, 1.4, 2.5, 1.0, name, sub, ec=col, fs=9.2)
        if i < 3:
            _arrow(ax, (x+0.5, 2.9), (x+2.5, 2.9), INK2)
    ax.text(6.2, 0.25, "spend ~70% on Action & Result — that's what signal the interviewer scores",
            ha="center", fontsize=8.6, color=INK2, style="italic")
    _save(key, "01-star-method", fig,
          "Structure every behavioral story as Situation → Task → Action → Result. Lead with "
          "context, but spend most words on your specific actions and a measurable result.")

def sliding_window():
    key = "dsa-01-patterns"; c = acc(key)
    arr = [2, 1, 5, 1, 3, 2]
    fig, axes = plt.subplots(3, 1, figsize=(6.6, 3.6))
    windows = [(0, 3, "sum=8"), (1, 4, "sum=7"), (2, 5, "sum=9 ← max")]
    for ax, (s, e, lab) in zip(axes, windows):
        ax.set_xlim(-0.5, 6); ax.set_ylim(0, 1.4); ax.axis("off")
        for i, v in enumerate(arr):
            inside = s <= i < e
            ax.add_patch(FancyBboxPatch((i, 0.2), 0.84, 0.84, boxstyle="round,pad=0.02,rounding_size=0.08",
                fc=_tint(c, 0.78) if inside else "#f1f5f9", ec=c if inside else "#cbd5e1", lw=1.6))
            ax.text(i+0.42, 0.62, str(v), ha="center", va="center", fontsize=11,
                    weight="bold", color=INK if inside else INK2)
        ax.text(5.4, 0.62, lab, va="center", fontsize=9.5, color=c, weight="bold")
    fig.suptitle("Sliding window — fixed window of size k slides in O(n)",
                 fontsize=12, weight="bold", color=INK)
    _save(key, "01-sliding-window", fig,
          "Instead of recomputing each window from scratch (O(n·k)), slide the window: add the "
          "entering element and drop the leaving one, achieving O(n).")

def ds_complexity():
    key = "dsa-02-ds"; c = acc(key)
    ds = ["Array", "Dyn. Array", "Linked List", "Hash Table", "BST (bal.)", "Heap", "Stack/Queue"]
    ops = ["Access", "Search", "Insert", "Delete"]
    # encode: 0=O(1),1=O(log n),2=O(n)
    M = np.array([
        [0,2,2,2],[0,2,2,2],[2,2,0,0],[0,0,0,0],
        [1,1,1,1],[2,2,1,1],[0,2,0,0]])
    labels = {0:"O(1)",1:"O(log n)",2:"O(n)"}
    cmap = {0:"#059669",1:"#d97706",2:"#dc2626"}
    fig, ax = plt.subplots(figsize=(6.6, 4.0))
    for i in range(len(ds)):
        for j in range(4):
            v = M[i, j]
            ax.add_patch(FancyBboxPatch((j+0.06, len(ds)-1-i+0.06), 0.88, 0.88,
                boxstyle="round,pad=0.01,rounding_size=0.06",
                fc=_tint(cmap[v], 0.78), ec=cmap[v], lw=1.2))
            ax.text(j+0.5, len(ds)-1-i+0.5, labels[v], ha="center", va="center",
                    fontsize=8, color=INK, weight="bold")
    for j, o in enumerate(ops):
        ax.text(j+0.5, len(ds)+0.2, o, ha="center", fontsize=9, weight="bold", color=INK)
    for i, d in enumerate(ds):
        ax.text(-0.12, len(ds)-1-i+0.5, d, ha="right", va="center", fontsize=8.6, color=c, weight="bold")
    ax.set_xlim(-2.4, 4.3); ax.set_ylim(-0.1, len(ds)+0.6); ax.axis("off")
    ax.set_title("Data structure operation complexity (average case)",
                 color=INK, fontsize=12.5, weight="bold")
    _save(key, "01-ds-complexity", fig,
          "Pick the structure that makes your hot operation O(1)/O(log n). Hash tables win for "
          "lookups; balanced trees keep order; heaps give cheap min/max.")

def rag_pipeline():
    key = "aiml-05-genai"; c = acc(key)
    fig, ax = _canvas((7.4, 3.6), "Retrieval-Augmented Generation (RAG)", (0, 14), (0, 8))
    _box(ax, 1.4, 6, 2.0, 1.1, "User\nquery", ec=c, fs=9)
    _box(ax, 4.2, 6, 2.0, 1.1, "Embed", "encoder", ec="#2563eb", fs=9)
    _box(ax, 7.0, 6, 2.2, 1.2, "Vector DB", "ANN search", ec="#059669", fs=9)
    _box(ax, 7.0, 2.4, 2.2, 1.1, "Top-k\nchunks", ec="#059669", fs=9)
    _box(ax, 10.2, 4.2, 2.2, 1.3, "Prompt\n(query+context)", ec="#d97706", fs=8.6)
    _box(ax, 12.9, 4.2, 1.8, 1.2, "LLM", "answer", ec=c, fs=9.5)
    _arrow(ax, (2.4, 6), (3.2, 6), INK2); _arrow(ax, (5.2, 6), (5.9, 6), INK2)
    _arrow(ax, (7.0, 5.4), (7.0, 2.95), "#059669", text="retrieve")
    _arrow(ax, (8.1, 2.4), (9.4, 3.7), "#d97706")
    _arrow(ax, (2.4, 5.6), (9.1, 4.5), c, rad=-0.25, ls="--")
    _arrow(ax, (11.3, 4.2), (12.0, 4.2), INK2)
    ax.text(7, 0.5, "grounds the LLM in retrieved facts → fewer hallucinations, fresh knowledge, citations",
            ha="center", fontsize=8.4, color=INK2, style="italic")
    _save(key, "01-rag-pipeline", fig,
          "RAG embeds the query, retrieves the most similar chunks from a vector store, and "
          "injects them into the prompt — grounding the LLM in current, citable facts.")

def mlops_lifecycle():
    key = "aiml-06-mlops"; c = acc(key)
    fig, ax = plt.subplots(figsize=(6.0, 5.0)); ax.set_aspect("equal"); ax.axis("off")
    stages = ["Data\ncollection", "Feature\nengineering", "Train &\ntune", "Evaluate",
              "Deploy\n(serve)", "Monitor\n(drift)"]
    n = len(stages); R = 3.1
    pts = []
    for i in range(n):
        a = math.pi/2 - i*2*math.pi/n
        x, y = R*math.cos(a), R*math.sin(a); pts.append((x, y))
        _box(ax, x, y, 2.0, 1.1, stages[i], ec=c, fs=8.4)
    for i in range(n):
        p1, p2 = pts[i], pts[(i+1) % n]
        _arrow(ax, p1, p2, c if i < n-1 else "#dc2626", rad=-0.18, lw=1.8)
    ax.text(0, 0, "MLOps\nlifecycle", ha="center", va="center", fontsize=11,
            weight="bold", color=c)
    ax.text(0, -1.0, "monitoring triggers\nretraining", ha="center", fontsize=7.8,
            color="#dc2626", style="italic")
    ax.set_xlim(-5, 5); ax.set_ylim(-5, 5)
    ax.set_title("MLOps: a continuous loop, not a pipeline", color=INK, fontsize=12.5, weight="bold")
    _save(key, "01-mlops-lifecycle", fig,
          "Production ML is a loop: monitoring detects data/concept drift and triggers "
          "retraining, closing the gap between a one-off model and a living system.")

def token_bucket():
    key = "sdp-1"; c = acc(key)
    fig, ax = _canvas((6.8, 3.8), "Rate limiting — the token-bucket algorithm", (0, 12), (0, 9))
    ax.add_patch(FancyBboxPatch((4.4, 3.0), 2.6, 4.2, boxstyle="round,pad=0.02,rounding_size=0.12",
                 fc=_tint(c, 0.9), ec=c, lw=1.8))
    for k in range(5):
        ax.add_patch(plt.Circle((5.7, 3.6+k*0.66), 0.26, fc=c, ec="white", lw=1.2))
    ax.text(5.7, 7.5, "refill r tokens/sec", ha="center", fontsize=8.6, color="#059669", weight="bold")
    _arrow(ax, (5.7, 8.6), (5.7, 7.35), "#059669")
    ax.text(5.7, 2.5, "capacity = burst size", ha="center", fontsize=8, color=INK2)
    _box(ax, 1.5, 5.1, 2.0, 1.1, "Requests", ec="#2563eb", fs=9)
    _arrow(ax, (2.5, 5.1), (4.3, 5.1), "#2563eb", text="take 1 token")
    _box(ax, 9.6, 6.4, 2.2, 1.1, "Allowed", "token left", ec="#059669", fs=8.8)
    _box(ax, 9.6, 3.4, 2.2, 1.1, "Throttled", "429 / queue", ec="#dc2626", fs=8.8)
    _arrow(ax, (7.1, 5.1), (8.5, 6.2), "#059669")
    _arrow(ax, (7.1, 5.1), (8.5, 3.6), "#dc2626", ls="--", text="empty")
    _save(key, "01-token-bucket", fig,
          "A bucket refills at a steady rate up to a capacity. Each request spends a token; "
          "an empty bucket throttles. This smooths traffic while allowing short bursts.")

def sharding_replication():
    key = "sdp-2"; c = acc(key)
    fig, ax = _canvas((7.2, 4.0), "Sharding + replication for scale and availability", (0, 13), (0, 9))
    _box(ax, 1.6, 5, 1.9, 1.1, "Router", "shard key", ec=c, fs=8.8)
    shards = [("Shard A", "keys 0–33%", 4.8), ("Shard B", "keys 34–66%", 8.0), ("Shard C", "keys 67–99%", 11.2)]
    for nm, rng, x in shards:
        _box(ax, x, 7.0, 2.2, 1.1, nm+"  (primary)", rng, ec="#2563eb", fs=8.2)
        _box(ax, x, 4.2, 2.0, 0.9, "replica", ec="#059669", fs=8.2)
        _box(ax, x, 2.6, 2.0, 0.9, "replica", ec="#059669", fs=8.2)
        _arrow(ax, (2.55, 5.2), (x-1.05, 6.7), c, rad=0.12)
        _arrow(ax, (x, 6.45), (x, 4.65), "#2563eb", text="async")
        _arrow(ax, (x, 6.45), (x, 3.05), "#2563eb", rad=0.18)
    ax.text(6.5, 0.7, "shard = horizontal partition (scales writes)   •   replica = copy (scales reads + HA)",
            ha="center", fontsize=8.4, color=INK2, style="italic")
    _save(key, "01-sharding-replication", fig,
          "Sharding partitions data by key to scale writes across nodes; replication copies "
          "each shard for read scaling and failover. Most large datastores combine both.")

def observer_pattern():
    key = "lld-coded"; c = acc(key)
    fig, ax = _canvas((7.0, 4.2), "Observer pattern — publish/subscribe decoupling", (0, 12), (0, 10))
    _box(ax, 2.8, 8, 3.4, 1.5, "Subject", "+ attach(o)\n+ notify()", ec=c, fs=9)
    _box(ax, 9.0, 8, 3.4, 1.3, "«interface»\nObserver", "+ update(state)", ec="#2563eb", fs=9)
    _arrow(ax, (4.55, 8), (7.25, 8), INK2, text="notifies *")
    for i, nm in enumerate(["EmailObserver", "SMSObserver", "LogObserver"]):
        x = 3.0 + i*3.2
        _box(ax, x, 3.2, 2.6, 1.1, nm, "+ update()", ec="#059669", fs=8.2)
        _arrow(ax, (x, 3.77), (9.0, 7.3), "#059669", ls="--")
    ax.text(9.0, 5.5, "realizes ▲", ha="center", fontsize=8, color=INK2)
    ax.text(6, 1.2, "subject broadcasts state changes; observers subscribe/unsubscribe at runtime",
            ha="center", fontsize=8.8, color=INK2, style="italic")
    _save(key, "01-observer-pattern", fig,
          "Observer lets a subject notify many observers of state changes without knowing their "
          "concrete types — the basis of event systems and reactive UIs.")

def deadlock():
    key = "01-concurrency"; c = acc(key)
    fig, ax = _canvas((6.0, 4.0), "Deadlock — a cycle in the wait-for graph", (0, 10), (0, 10))
    _box(ax, 2.4, 7.4, 2.2, 1.2, "Process 1", "holds R1", ec=c)
    _box(ax, 7.6, 7.4, 2.2, 1.2, "Process 2", "holds R2", ec="#dc2626")
    _box(ax, 2.4, 2.6, 2.2, 1.1, "Resource R2", ec="#059669")
    _box(ax, 7.6, 2.6, 2.2, 1.1, "Resource R1", ec="#059669")
    _arrow(ax, (3.0, 6.8), (7.1, 3.1), c, rad=0.12)
    _arrow(ax, (7.0, 6.8), (2.9, 3.1), "#dc2626", rad=0.12)
    _arrow(ax, (7.6, 3.15), (7.6, 6.8), "#059669", rad=0.0)
    _arrow(ax, (2.4, 3.15), (2.4, 6.8), "#059669", rad=0.0)
    ax.text(3.5, 5.4, "P1 waits R2", fontsize=7.6, color=c, ha="center",
            bbox=dict(fc="white", ec="none", pad=0.6))
    ax.text(6.5, 4.4, "P2 waits R1", fontsize=7.6, color="#dc2626", ha="center",
            bbox=dict(fc="white", ec="none", pad=0.6))
    ax.text(5, 0.6, "Coffman conditions: mutual exclusion · hold-and-wait · no preemption · circular wait",
            ha="center", fontsize=7.6, color=INK2, style="italic")
    _save(key, "02-deadlock", fig,
          "Deadlock needs all four Coffman conditions at once; the tell-tale sign is a cycle "
          "in the wait-for graph. Break any one condition (e.g. lock ordering) to prevent it.")

def memory_hierarchy():
    key = "02-os"; c = acc(key)
    fig, ax = plt.subplots(figsize=(6.6, 4.2)); ax.axis("off")
    rows = [("Registers", "<1 ns", "~1 KB", 2.2),
            ("L1 cache", "~1 ns", "~64 KB", 3.4),
            ("L2 / L3 cache", "~4–40 ns", "~MBs", 4.8),
            ("Main memory (RAM)", "~100 ns", "~GBs", 6.6),
            ("SSD", "~16 µs", "~TBs", 8.4),
            ("Disk / Network", "~1–150 ms", "~PBs", 10.0)]
    cols = plt.cm.viridis(np.linspace(0.15, 0.85, len(rows)))
    y = 6
    for (name, lat, cap, w), col in zip(rows, cols):
        ax.add_patch(FancyBboxPatch((5-w/2, y), w, 0.82, boxstyle="round,pad=0.02,rounding_size=0.06",
                     fc=_tint(matplotlib.colors.to_hex(col), 0.55), ec=matplotlib.colors.to_hex(col), lw=1.4))
        ax.text(5, y+0.41, name, ha="center", va="center", fontsize=9, weight="bold", color=INK)
        ax.text(5-w/2-0.2, y+0.41, lat, ha="right", va="center", fontsize=8, color=INK2)
        ax.text(5+w/2+0.2, y+0.41, cap, ha="left", va="center", fontsize=8, color=INK2)
        y -= 1.05
    ax.text(0.7, 6.9, "faster,\nsmaller", ha="center", fontsize=8, color=c, weight="bold")
    ax.text(0.7, 0.9, "slower,\nbigger", ha="center", fontsize=8, color=c, weight="bold")
    ax.set_xlim(0, 10); ax.set_ylim(0, 7.2)
    ax.set_title("The memory hierarchy", color=INK, fontsize=12.5, weight="bold")
    _save(key, "02-memory-hierarchy", fig,
          "Each level trades capacity for speed by orders of magnitude. Performance comes from "
          "keeping the working set in the fastest tier that fits — the basis of caching.")

def tcp_handshake():
    key = "03-networks"; c = acc(key)
    fig, ax = _canvas((6.6, 4.3), "TCP three-way handshake & teardown", (0, 10), (0, 12))
    cx, sx = 2.0, 8.0
    for x, nm in [(cx, "Client"), (sx, "Server")]:
        _box(ax, x, 11.2, 1.9, 0.9, nm, ec=c, fs=10)
        ax.plot([x, x], [0.4, 10.5], color="#cbd5e1", lw=1.4, zorder=0)
    seq = [(9.8, "→", "SYN  seq=x", c), (8.8, "←", "SYN-ACK  seq=y, ack=x+1", "#2563eb"),
           (7.8, "→", "ACK  ack=y+1", c), (6.6, "↔", "data transfer", "#059669"),
           (5.0, "→", "FIN", "#dc2626"), (4.2, "←", "ACK", "#2563eb"),
           (3.4, "←", "FIN", "#dc2626"), (2.6, "→", "ACK", c)]
    for y, d, txt, col in seq:
        if d == "→": _arrow(ax, (cx+0.2, y), (sx-0.2, y), col)
        elif d == "←": _arrow(ax, (sx-0.2, y), (cx+0.2, y), col)
        else: _arrow(ax, (cx+0.2, y), (sx-0.2, y), col, two=True)
        ax.text(5.0, y+0.22, txt, ha="center", fontsize=7.8, color=col,
                bbox=dict(fc="white", ec="none", pad=0.5))
    ax.text(2.0, 6.0, "ESTABLISHED", fontsize=7, color="#059669", rotation=90, va="center")
    _save(key, "02-tcp-handshake", fig,
          "TCP opens with SYN / SYN-ACK / ACK to agree on sequence numbers, then tears down "
          "with a four-way FIN/ACK exchange. This reliability is what UDP trades away for speed.")

def consistency_spectrum():
    key = "07-distributed"; c = acc(key)
    fig, ax = plt.subplots(figsize=(6.8, 3.0)); ax.axis("off")
    ax.annotate("", xy=(9.6, 3), xytext=(0.4, 3),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=2.4))
    models = [(0.8, "Linearizable", "single-copy\nillusion"), (3.0, "Sequential", "global order"),
              (5.2, "Causal", "causes before\neffects"), (7.4, "Read-your-\nwrites", "session"),
              (9.2, "Eventual", "converges\nlater")]
    for x, name, sub in models:
        ax.plot(x, 3, "o", ms=11, color=c, zorder=4)
        ax.text(x, 3.6, name, ha="center", fontsize=8.6, weight="bold", color=INK)
        ax.text(x, 2.2, sub, ha="center", fontsize=7.2, color=INK2)
    ax.text(0.8, 4.4, "STRONGER\n(less available, higher latency)", ha="center", fontsize=7.6,
            color="#dc2626", weight="bold")
    ax.text(9.2, 4.4, "WEAKER\n(more available, lower latency)", ha="center", fontsize=7.6,
            color="#059669", weight="bold")
    ax.set_xlim(0, 10); ax.set_ylim(1.4, 5.0)
    ax.set_title("The consistency spectrum", color=INK, fontsize=12.5, weight="bold")
    _save(key, "02-consistency-spectrum", fig,
          "Consistency is a dial, not a switch. Stronger models are easier to reason about but "
          "cost availability and latency under partitions — pick per use-case.")

def tail_latency():
    key = "09-performance"; c = acc(key)
    rng = np.random.default_rng(3)
    data = np.concatenate([rng.normal(40, 8, 9000), rng.normal(120, 50, 900),
                           rng.gamma(2, 90, 250)+150])
    data = data[(data > 5) & (data < 700)]
    fig, ax = plt.subplots(figsize=(6.6, 3.7))
    ax.hist(data, bins=80, color=_tint(c, 0.4), edgecolor=c, lw=0.5)
    for p, col in [(50, "#059669"), (95, "#d97706"), (99, "#dc2626")]:
        v = np.percentile(data, p)
        ax.axvline(v, color=col, lw=1.8, ls="--")
        ax.text(v+4, ax.get_ylim()[1]*(0.9-0.08*[50,95,99].index(p)),
                f"p{p} = {v:.0f} ms", color=col, fontsize=8.5, weight="bold")
    ax.set_xlabel("request latency (ms)"); ax.set_ylabel("# requests")
    ax.set_title("Why averages lie — the latency tail")
    _save(key, "02-tail-latency", fig,
          "A handful of slow requests barely move the mean but dominate user experience. Track "
          "p95/p99, not averages — at scale, the tail is what every user eventually hits.")

def confusion_matrix():
    key = "aiml-02-classic"; c = acc(key)
    M = np.array([[85, 10], [8, 97]])
    fig, ax = plt.subplots(figsize=(5.2, 4.4))
    im = ax.imshow(M, cmap="Purples")
    labels = [["TP\n85", "FN\n10"], ["FP\n8", "TN\n97"]]
    for i in range(2):
        for j in range(2):
            ax.text(j, i, labels[i][j], ha="center", va="center", fontsize=12, weight="bold",
                    color="white" if M[i, j] > 60 else INK)
    ax.set_xticks([0, 1]); ax.set_xticklabels(["Pred +", "Pred −"])
    ax.set_yticks([0, 1]); ax.set_yticklabels(["Actual +", "Actual −"])
    ax.set_title("Confusion matrix", color=INK, fontsize=12.5, weight="bold")
    ax.text(2.1, 0, "Precision\n= TP/(TP+FP)\n= 0.91", fontsize=8.2, color=INK2, va="center")
    ax.text(2.1, 1, "Recall\n= TP/(TP+FN)\n= 0.89", fontsize=8.2, color=INK2, va="center")
    ax.grid(False)
    _save(key, "02-confusion-matrix", fig,
          "Every classifier error is a false positive or false negative. Precision penalizes "
          "FPs, recall penalizes FNs — which matters more depends on the cost of each mistake.")

def transformer_block():
    key = "aiml-04-tf"; c = acc(key)
    fig, ax = _canvas((4.8, 5.4), "Transformer encoder block", (0, 10), (0, 13))
    stack = [(1.2, "Token + positional embedding", "#64748b"),
             (3.0, "Multi-Head Self-Attention", c),
             (4.4, "Add & LayerNorm", "#94a3b8"),
             (6.2, "Feed-Forward (MLP)", "#2563eb"),
             (7.6, "Add & LayerNorm", "#94a3b8")]
    for y, label, col in stack:
        _box(ax, 5, y, 7.6, 1.0, label, ec=col, fs=8.8)
    for i in range(len(stack)-1):
        _arrow(ax, (5, stack[i][0]+0.5), (5, stack[i+1][0]-0.5), INK2)
    # residual arrows
    _arrow(ax, (8.9, 3.0), (8.9, 4.4), "#d97706", rad=-0.5)
    _arrow(ax, (8.9, 6.2), (8.9, 7.6), "#d97706", rad=-0.5)
    ax.text(9.5, 3.7, "skip", fontsize=7, color="#d97706", rotation=90, va="center")
    _box(ax, 5, 9.2, 7.6, 0.9, "× N layers  →  output", ec=c, fs=8.8)
    _arrow(ax, (5, 8.1), (5, 8.75), INK2)
    _save(key, "02-transformer-block", fig,
          "A transformer layer = self-attention (mix information across tokens) + a position-wise "
          "MLP, each wrapped in a residual connection and LayerNorm. Stack N of them.")

def sorting_complexity():
    key = "dsa-03-algos"; c = acc(key)
    algos = ["Bubble", "Insertion", "Selection", "Merge", "Quick", "Heap", "Counting", "Radix"]
    cols = ["Best", "Average", "Worst", "Space", "Stable"]
    # 0 green good ... 3 red bad ; stable col: 4=yes(green) 5=no(red)
    T = np.array([
        [1,2,2,0,4],[1,2,2,0,4],[2,2,2,0,5],[1,1,1,2,4],
        [1,1,2,1,5],[1,1,1,0,5],[0,0,0,2,4],[0,0,0,2,4]])
    txt = {0:"O(n)",1:"O(n log n)",2:"O(n²)"}
    spc = {0:"O(1)",1:"O(log n)",2:"O(n)"}
    cmap = {0:"#059669",1:"#65a30d",2:"#dc2626"}
    fig, ax = plt.subplots(figsize=(6.8, 4.0)); ax.axis("off")
    for i in range(len(algos)):
        for j in range(5):
            v = T[i, j]
            if j < 3: label, col = txt[v], cmap[0 if v==0 else (1 if v==1 else 2)]
            elif j == 3: label, col = spc[v], cmap[0 if v==0 else (1 if v==1 else 2)]
            else: label, col = ("yes" if v==4 else "no"), (cmap[0] if v==4 else cmap[2])
            ax.add_patch(FancyBboxPatch((j+0.06, len(algos)-1-i+0.06), 0.88, 0.88,
                boxstyle="round,pad=0.01,rounding_size=0.06", fc=_tint(col, 0.8), ec=col, lw=1.1))
            ax.text(j+0.5, len(algos)-1-i+0.5, label, ha="center", va="center", fontsize=7.4,
                    color=INK, weight="bold")
    for j, ccol in enumerate(cols):
        ax.text(j+0.5, len(algos)+0.2, ccol, ha="center", fontsize=8.6, weight="bold", color=INK)
    for i, a in enumerate(algos):
        ax.text(-0.12, len(algos)-1-i+0.5, a, ha="right", va="center", fontsize=8.4, color=c, weight="bold")
    ax.set_xlim(-1.8, 5.2); ax.set_ylim(-0.1, len(algos)+0.6)
    ax.set_title("Sorting algorithms at a glance", color=INK, fontsize=12.5, weight="bold")
    _save(key, "02-sorting-complexity", fig,
          "No single sort wins everywhere: merge sort is stable and worst-case O(n log n) but "
          "needs O(n) space; quicksort is faster in practice but O(n²) worst case.")

def two_pointers():
    key = "dsa-01-patterns"; c = acc(key)
    arr = [1, 3, 4, 6, 8, 11, 15]
    target = 14
    fig, axes = plt.subplots(3, 1, figsize=(6.6, 3.4))
    states = [(0, 6, "1+15=16 > 14 → move right in"),
              (0, 5, "1+11=12 < 14 → move left in"),
              (2, 5, "4+11=15 > 14 ...  (converging)")]
    for ax, (lo, hi, note) in zip(axes, states):
        ax.set_xlim(-0.5, 8); ax.set_ylim(0, 1.6); ax.axis("off")
        for i, v in enumerate(arr):
            hot = i in (lo, hi)
            ax.add_patch(FancyBboxPatch((i, 0.4), 0.84, 0.7, boxstyle="round,pad=0.02,rounding_size=0.08",
                fc=_tint(c, 0.7) if hot else "#f1f5f9", ec=c if hot else "#cbd5e1", lw=1.6))
            ax.text(i+0.42, 0.75, str(v), ha="center", va="center", fontsize=10,
                    weight="bold", color=INK if hot else INK2)
        ax.text(lo+0.42, 1.28, "L", ha="center", fontsize=9, color=c, weight="bold")
        ax.text(hi+0.42, 1.28, "R", ha="center", fontsize=9, color=c, weight="bold")
        ax.text(7.3, 0.75, note, va="center", fontsize=7.6, color=INK2)
    fig.suptitle(f"Two pointers on a sorted array (target sum = {target})",
                 fontsize=11.5, weight="bold", color=INK)
    _save(key, "02-two-pointers", fig,
          "On sorted input, two pointers from both ends turn an O(n²) pair-search into O(n): "
          "move the pointer that brings the sum toward the target.")

def main():
    figset = [
        # original 12
        amdahl, bias_variance, learning_curves, roc_pr, activations, grad_descent,
        big_o, latency_ladder, cap_theorem, osi_stack, scheduling_gantt, attention_heatmap,
        # extended coverage
        cloud_autoscaling, shared_responsibility, web_architecture, latency_throughput,
        strategy_pattern, btree, isolation_levels, tls_handshake, defense_in_depth,
        star_method, sliding_window, ds_complexity, rag_pipeline, mlops_lifecycle,
        token_bucket, sharding_replication, observer_pattern,
        # second batch
        deadlock, memory_hierarchy, tcp_handshake, consistency_spectrum, tail_latency,
        confusion_matrix, transformer_block, sorting_complexity, two_pointers,
    ]
    for f in figset:
        try:
            f()
        except Exception as e:
            print(f"  !! {f.__name__} failed: {e}")
    (FIG / "figures.json").write_text(json.dumps(REG_FIGS, indent=2))
    print(f"\nWrote {sum(len(v) for v in REG_FIGS.values())} figures across "
          f"{len(REG_FIGS)} editions -> figures/figures.json")

if __name__ == "__main__":
    main()

# Vector Databases & Embeddings

> **How to use this file:** This is a deep, mechanism-level reference for FAANG SDE/ML interviews on vector search, embeddings, ANN indexes, and RAG retrieval. Read top to bottom once to build the mental model; then use the **Revision Cheat Sheet** and **Common Interview Questions** the night before. Every section pairs an explanation with real code, concrete numbers, and a trade-off. When an interviewer says "design semantic search over 100M docs," the **Worked Example** section is your script.

---

## Table of Contents

- [Overview — What It Is](#overview--what-it-is)
- [Why It Exists](#why-it-exists)
- [Why FAANG Cares](#why-faang-cares)
- [Core Concepts](#core-concepts)
- [Embeddings](#embeddings)
- [Similarity & Distance Metrics](#similarity--distance-metrics)
- [Approximate Nearest Neighbor (ANN) Indexes](#approximate-nearest-neighbor-ann-indexes)
- [The Recall / Latency / Memory Trade-off](#the-recall--latency--memory-trade-off)
- [Building a RAG / Semantic-Search Pipeline](#building-a-rag--semantic-search-pipeline)
- [Vector Database Systems](#vector-database-systems)
- [Scaling, Updates & Operations](#scaling-updates--operations)
- [Evaluation](#evaluation)
- [Designing Search over 100M Documents (Worked Example)](#designing-search-over-100m-documents-worked-example)
- [Architecture / Diagrams](#architecture--diagrams)
- [Real-World Examples](#real-world-examples)
- [Real-Life Analogies](#real-life-analogies)
- [Memory Tricks / Mnemonics](#memory-tricks--mnemonics)
- [Common Interview Questions](#common-interview-questions)
- [Senior-Level Discussion Points](#senior-level-discussion-points)
- [Typical Mistakes Candidates Make](#typical-mistakes-candidates-make)
- [How This Connects to Other Topics](#how-this-connects-to-other-topics)
- [FAANG Interview Tips](#faang-interview-tips)
- [Revision Cheat Sheet](#revision-cheat-sheet)

---

## Overview — What It Is

A **vector database** is a system that stores high-dimensional numeric vectors (**embeddings**) and answers the query "**which stored vectors are closest to this query vector?**" in milliseconds, even across hundreds of millions of vectors.

An **embedding** is a dense array of floating-point numbers — say 768 of them — that a neural network produces to represent the *meaning* of a piece of content (a sentence, a paragraph, an image, a product). Two pieces of content that mean similar things land near each other in this 768-dimensional space; unrelated content lands far apart. The vector database makes "find the nearest meanings" fast.

| Layer | What it does | Examples |
|---|---|---|
| **Embedding model** | Turns text/image into a dense vector | `text-embedding-3-small`, `bge-large`, `e5`, CLIP |
| **Distance metric** | Defines "closeness" between vectors | cosine, dot product, L2 (Euclidean) |
| **ANN index** | Finds approximate nearest neighbors fast | HNSW, IVF, IVF-PQ, ScaNN, Annoy, LSH |
| **Vector store** | Persists vectors + metadata, serves queries | Pinecone, Weaviate, Milvus, Qdrant, pgvector |
| **Retrieval pipeline** | Chunk → embed → upsert → retrieve → rerank | RAG, semantic search, recommendations |
| **Filtering** | Restrict search by metadata (date, tenant, ACL) | "only docs from tenant X, after 2024" |

**Key insight:** A vector database is not a replacement for Postgres. It is a specialized index — the moral equivalent of a B-tree, but for *semantic proximity* in high-dimensional space instead of *sorted order* on a scalar key. The hard engineering problem it solves is that **exact nearest-neighbor search in high dimensions is brutally slow**, so it trades a tiny amount of accuracy (recall) for orders-of-magnitude speedups.

```
"How do I reset my password?"  ─embed─→ [0.12, -0.43, 0.87, ..., 0.31]  (768 floats)
"Steps to recover account access" ─embed─→ [0.11, -0.41, 0.85, ..., 0.29]  ← very close
"What is photosynthesis?"      ─embed─→ [-0.67, 0.82, -0.34, ..., 0.91]  ← far away

Vector DB job: given the first vector, return the second (and not the third)
               from among 100,000,000 stored vectors in < 50 ms.
```

---

## Why It Exists

**The core problem: meaning is not keywords.**

Traditional search (inverted index + BM25, the engine behind Elasticsearch and classic Google) matches **tokens**. If you search "reset password" it finds documents containing the literal words "reset" and "password." This breaks in three ways:

1. **Synonymy** — "recover account access" means the same thing but shares zero keywords with "reset password." Keyword search misses it entirely.
2. **Polysemy** — "Apple stock" (fruit inventory vs. AAPL shares) — the same token, different meanings. Keyword search can't tell them apart.
3. **Paraphrase / intent** — "my laptop won't turn on" should match a doc titled "troubleshooting power issues on portable computers." No shared tokens.

Embeddings solve this because the model maps *meaning* to *geometry*. "Reset password" and "recover account access" produce nearly identical vectors even though they share no words.

**The second core problem: exact nearest-neighbor search is too slow.**

Once you have vectors, you need to find the nearest ones. The naive approach — compute the distance from the query to every stored vector and sort — is **exact k-Nearest-Neighbor (kNN)**, and it costs **O(N · d)** per query.

```
N = 100,000,000 documents
d = 768 dimensions
Cost per query = N × d = 76.8 billion multiply-adds

At ~10 GFLOP/s effective for a brute-force dot-product loop,
that's ~7.6 seconds per query. Per query. Unusable.
```

You might think: "use a tree, like a k-d tree, the way we'd do 2D nearest-neighbor." That fails because of the **curse of dimensionality**:

### Why k-d trees fail in high dimensions

A k-d tree partitions space by axis-aligned splits and prunes branches that can't contain a closer point. In 2D or 3D this prunes ~99% of the tree and gives O(log N) search. But as dimensions grow:

- **Volume concentrates in the corners.** The fraction of a hypercube's volume near the surface goes to 1. In 768 dimensions, essentially all points are "near the boundary," so the pruning bound rarely lets you skip a branch.
- **Distances concentrate.** The ratio of the farthest to the nearest point distance approaches 1 as d → ∞. When the nearest and farthest neighbors are nearly equidistant, "nearest neighbor" is barely meaningful and pruning is impossible.
- **Branching factor explosion.** To prune effectively in d dimensions you'd need ~2^d cells; for d=768 that's astronomically more than any dataset.

```
Exact NN search method      | Works well up to dimension
----------------------------|----------------------------
k-d tree / ball tree        | ~10-20
Cover tree                  | ~30-50
Brute force (O(N·d))        | any d, but O(N) per query — too slow at scale
ANN (HNSW/IVF/PQ)           | hundreds to thousands ← the only practical answer
```

This is exactly why **Approximate** Nearest Neighbor (ANN) exists: give up the guarantee of finding *the* exact nearest neighbor, accept finding *almost always the right ones* (e.g., 95–99% recall), and get a 100–1000× speedup. The "approximate" is the whole point.

**Before vector databases:** semantic search required hand-built NLP — TF-IDF, latent semantic analysis (LSA/SVD), query expansion with synonym dictionaries, and entity linking. Each was brittle and shallow.

**After embeddings + ANN:** a single embedding model plus an ANN index gives deep semantic matching out of the box, and it generalizes to images, audio, and code with the same machinery.

---

## Why FAANG Cares

**Google:** ANN is foundational. **ScaNN** (Scalable Nearest Neighbors) is Google's own library, used in Search and YouTube recommendations. Vertex AI Matching Engine serves billion-vector indexes. Embedding-based retrieval is how Google does semantic ranking, "related searches," and RAG grounding for Gemini. Expect questions on ScaNN's anisotropic quantization and on grounding LLMs.

**Meta:** Built **FAISS** (Facebook AI Similarity Search) — the most-used ANN library in the world. Meta runs embedding retrieval for feed ranking, ads retrieval (find candidate ads from billions), Reels recommendations, and content moderation (find near-duplicate / similar harmful content). "Two-tower" retrieval models feeding FAISS are a core interview topic.

**Amazon:** Product search and recommendations ("customers who bought this") are embedding retrieval at planetary scale. OpenSearch (their Elasticsearch fork) ships kNN/HNSW. Amazon Bedrock Knowledge Bases is managed RAG. Cost-per-query and memory footprint directly hit AWS margins, so quantization (PQ) and sharding come up.

**Microsoft:** Azure AI Search has native vector + hybrid search; it underpins Microsoft 365 Copilot's retrieval over your org's documents. They care about hybrid (dense + BM25) and ACL-aware filtered search (you must only retrieve docs you're allowed to see).

**Apple:** On-device semantic search (Spotlight, Photos "find pictures of dogs"), privacy-first, tight memory budgets — making PQ/compression and small embedding models matter.

**Netflix / Spotify / Pinterest:** Recommendations are retrieval. Spotify built **Annoy** (Approximate Nearest Neighbors Oh Yeah) for music recs. Pinterest's PinSage/visual search is embedding retrieval over billions of pins.

**Startups (Perplexity, Glean, Harvey, Notion AI, Cursor):** The product *is* retrieval quality. Every one of them ships RAG; chunking, hybrid search, and reranking are daily decisions.

**Why interviewers ask:** RAG is now standard in every AI product, so retrieval quality is a core competency. The recall/latency/memory trade-off is a clean systems-design question with real numbers. And it connects ML (embeddings, training objectives) with systems (indexes, sharding) — a great signal for senior generalists.

---

## Core Concepts

### Semantic search vs. lexical search

| | Lexical (BM25 / inverted index) | Semantic (embeddings + ANN) |
|---|---|---|
| **Matches on** | Exact tokens / stems | Meaning / intent |
| **Strength** | Rare terms, IDs, names, acronyms, code | Paraphrase, synonyms, concepts |
| **Weakness** | Synonyms, paraphrase | Exact strings ("error code E-1042"), out-of-domain jargon |
| **Index** | Posting lists (sparse) | Dense vectors in ANN index |
| **Scoring** | TF-IDF / BM25 | Cosine / dot product distance |
| **Best in practice** | — | **Hybrid: use both, fuse the scores** |

The professional answer is almost never "semantic only." It's **hybrid search** — semantic for recall on meaning, lexical for precision on exact terms — fused together (covered later).

### The vector space

After embedding, every document is a point in ℝ^d. The geometry encodes semantics:

```
                 [photosynthesis]
                       ●
                                          ● [chlorophyll]


   [reset password] ●
         ● [recover account access]      ● [forgot login credentials]

   ← Cluster of "account access help" sits in one region;
     "biology/plants" sits in a far-away region.
```

Three operations matter:
- **Nearest-neighbor query** — given a query point, return the k closest stored points (search/RAG).
- **Clustering** — group points into regions (used internally by IVF; also for dedup, topic discovery).
- **Filtered NN** — nearest neighbors *subject to* a metadata predicate ("only points where tenant=X").

### Exact kNN cost recap

```python
import numpy as np

def exact_knn(query, vectors, k):
    # vectors: (N, d) matrix, query: (d,)
    # O(N*d) dot products + O(N log k) selection
    sims = vectors @ query           # N*d multiply-adds
    idx = np.argpartition(-sims, k)[:k]
    return idx[np.argsort(-sims[idx])]
```

At N=100M, d=768 this is ~7.6 s/query (shown above). ANN indexes cut this to single-digit milliseconds by *not* looking at most vectors — they navigate a graph (HNSW) or only probe a few clusters (IVF).

**Interview takeaway:** Brute force is fine up to ~tens of thousands of vectors (a few ms). Past ~100K–1M you need an ANN index. State this threshold explicitly.

---

## Embeddings

### What a dense embedding is

A dense embedding is a fixed-length vector of real numbers where **every dimension carries (distributed) information** — unlike a sparse one-hot or bag-of-words vector where most entries are zero. "Dense" means all d entries are meaningful floats; "embedding" means the vector lives in a learned space where geometric closeness ≈ semantic similarity.

```
Sparse (bag-of-words, vocab=50,000):  [0,0,...,1,...,0,1,0,...,0]  ← 50,000 dims, mostly 0
Dense (embedding):                    [0.12, -0.43, 0.87, ..., 0.31]  ← 768 dims, all informative
```

No single dimension means "is about cats." Meaning is **distributed** across all dimensions — direction in the space encodes concepts.

### How models learn embeddings — the training objective

Embeddings are learned, not designed. The dominant objective is **contrastive learning**: pull semantically-related pairs together and push unrelated pairs apart.

**Contrastive / InfoNCE loss (the core idea):**

For an anchor `a`, a positive `p` (something that should be similar), and negatives `n_i` (things that should be dissimilar), minimize:

```
loss = -log(  exp(sim(a, p) / τ)  /  Σ_i exp(sim(a, n_i) / τ)  )
```

Maximizing the numerator pulls `a` and `p` together; the denominator pushes `a` away from all negatives. `τ` is a temperature. **In-batch negatives** are the trick that makes this cheap: within a batch of B (anchor, positive) pairs, every other pair's positive serves as a negative, giving B−1 negatives for free.

**Self-supervised pretraining** generates the pairs without human labels:
- **Inverse cloze / span corruption** — a sentence and its surrounding paragraph are a positive pair.
- **Dropout-as-augmentation (SimCSE)** — feed the *same* sentence through the encoder twice with different dropout masks; the two outputs are a positive pair. Brilliantly simple and strong.
- **Title–body, question–answer, query–clicked-document** mined from logs are natural positives.

**Sentence-transformers & bi-encoders:** A **bi-encoder** encodes the query and the document *independently* into vectors, then compares with a cheap dot product. This is what makes retrieval scalable: you embed all N documents *once, offline*, store the vectors, and at query time only embed the query (one forward pass) and do ANN search. Contrast with a **cross-encoder** (used for reranking) which feeds [query, doc] *together* through attention — far more accurate but O(N) forward passes, impossible at retrieval scale.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")  # bi-encoder, 768-dim

# Offline: embed the whole corpus once
doc_vecs = model.encode(documents, batch_size=256, normalize_embeddings=True)

# Online: embed only the query (one forward pass), then ANN search
q = model.encode("how do I reset my password", normalize_embeddings=True)
# similarity = dot product because vectors are unit-normalized
```

### Dimensionality — 384 vs 768 vs 1536 vs 3072

| Dims | Typical models | Pros | Cons |
|---|---|---|---|
| **384** | `all-MiniLM-L6-v2`, `bge-small` | Tiny, fast, 4× less RAM than 1536 | Lower ceiling on quality |
| **768** | `bge-base`, `e5-base`, `nomic-embed` | Sweet spot quality/cost | Standard default |
| **1024** | `bge-large`, `cohere-embed-v3` | Strong quality | More RAM/compute |
| **1536** | OpenAI `text-embedding-3-small`, `ada-002` | Excellent, managed API | 2× RAM vs 768 |
| **3072** | OpenAI `text-embedding-3-large` | Best OpenAI quality | 4× RAM vs 768; often overkill |

**The trade-off is concrete.** Memory and compute scale linearly with d:

```
100M vectors, float32 (4 bytes):
  d=384  → 100M × 384 × 4 B  = 153.6 GB
  d=768  → 100M × 768 × 4 B  = 307.2 GB
  d=1536 → 100M × 1536 × 4 B = 614.4 GB
  d=3072 → 100M × 3072 × 4 B = 1.23 TB
```

Doubling dimensions doubles RAM, doubles distance-computation cost, and doubles network/storage. Higher d usually improves recall — but with diminishing returns. **Matryoshka embeddings** (MRL, used by OpenAI v3 and nomic) train so that the *first* k dimensions are themselves a usable embedding — you can truncate 1536→512 and keep ~90%+ of quality, getting a runtime knob for the cost/quality trade-off.

### Normalization — unit vectors

Most text embeddings are **L2-normalized** to unit length (‖v‖ = 1). This matters because:

- After normalization, **dot product = cosine similarity** (proof below), so you can use the faster `inner product` metric in the index and still get cosine ranking.
- It removes magnitude as a confound — you compare *direction* (meaning) only, not length.

```python
v = v / np.linalg.norm(v)   # now ‖v‖ = 1; dot(a,b) == cosine(a,b)
```

If your model emits normalized vectors, configure the index for **inner product (IP)**, not L2 — it's the same ranking and slightly cheaper.

### Choosing / fine-tuning a domain model

Off-the-shelf models are trained on web/general text. For specialized domains (legal, biomedical, code, your internal jargon) they under-perform because the *geometry* doesn't separate your domain's concepts well.

Decision order:
1. **Start with a strong general model** (`bge-large`, `e5`, OpenAI v3). Measure recall on a golden set first.
2. **Try a domain pretrained model** if one exists (`BioBERT`/`PubMedBERT` for biomed, `CodeBERT`/`jina-code` for code).
3. **Fine-tune with contrastive pairs from your data** — mined (query, clicked-doc) pairs, or synthetic (LLM generates a question for each chunk → (question, chunk) positive). A few thousand pairs can lift recall@10 by 5–15 points.

```python
from sentence_transformers import SentenceTransformer, losses, InputExample
from torch.utils.data import DataLoader

model = SentenceTransformer("BAAI/bge-base-en-v1.5")
train = [InputExample(texts=[q, positive_chunk]) for q, positive_chunk in mined_pairs]
loader = DataLoader(train, shuffle=True, batch_size=64)
loss = losses.MultipleNegativesRankingLoss(model)   # in-batch negatives
model.fit(train_objectives=[(loader, loss)], epochs=1, warmup_steps=100)
```

**The hidden cost: fine-tuning changes the space.** New vectors are *not comparable* to old ones, so you must **re-embed your entire corpus** with the new model. At 100M chunks and 1000 chunks/sec/GPU that's ~28 GPU-hours per pass — a real operational event.

### Multimodal — CLIP and shared spaces

**CLIP** (Contrastive Language–Image Pretraining) trains an image encoder and a text encoder *jointly* with a contrastive loss over (image, caption) pairs, so an image and its caption land at the **same point** in a shared 512/768-dim space. This enables cross-modal search: embed a text query and retrieve images, or embed an image and retrieve captions, all with one ANN index.

```python
# Search images with a text query — one shared space
image_vecs = clip.encode_image(images)        # stored offline
q = clip.encode_text("a golden retriever on a beach")
hits = index.search(q, k=10)                   # returns nearest IMAGE vectors
```

The same recipe gives audio–text (CLAP), video–text, and document-layout embeddings. **Interview point:** multimodal RAG over PDFs with figures uses this — embed page images and surrounding text into one space.

### Embedding drift & the cost of re-embedding

Two distinct problems share the name "drift":

1. **Model drift (you change models):** A new model version → entirely new geometry → **full corpus re-embedding required** + index rebuild. Plan blue/green: build the new index alongside the old, validate recall on the golden set, then cut over. Never mix vectors from two models in one index.

2. **Data/semantic drift (the world changes):** New slang, new products, new entities appear that the embedding model (trained at an earlier cutoff) represents poorly. Symptoms: recall degrades over time on fresh queries. Mitigations: periodic fine-tuning, hybrid search (BM25 catches new exact terms the model never saw), and monitoring recall on a rolling golden set.

```
Re-embed cost model (100M chunks):
  throughput  = 1,000 chunks/sec/GPU (bge-base on an A10)
  total time  = 100,000,000 / 1,000 = 100,000 GPU-sec ≈ 27.8 GPU-hours
  with 8 GPUs ≈ 3.5 wall-clock hours + index build
  API cost (if using OpenAI v3-small @ ~$0.02/1M tokens, ~300 tok/chunk)
            ≈ 100M × 300 / 1M × $0.02 = $600 per full re-embed
```

**Interview takeaway:** Re-embedding is the single biggest hidden operational cost of a vector system. Always mention it when someone proposes "just upgrade the embedding model."

---

## Similarity & Distance Metrics

The index needs a notion of "closeness." Three matter; one dominates text.

### Cosine similarity

Measures the **angle** between two vectors, ignoring magnitude.

```
cos(a, b) = (a · b) / (‖a‖ · ‖b‖)
          = Σ a_i b_i  /  (sqrt(Σ a_i²) · sqrt(Σ b_i²))

Range: [-1, 1]   (1 = identical direction, 0 = orthogonal, -1 = opposite)
Cosine distance = 1 − cos(a, b)
```

**Why cosine is the text default:** Document length / token count inflates raw vector magnitude, but meaning is in the *direction*. Two paraphrases of different lengths should match — cosine ignores the length difference and compares semantic direction. Almost every sentence-transformer is trained with cosine objectives, so the geometry is calibrated for it.

### Dot product (inner product)

```
a · b = Σ a_i b_i = ‖a‖ ‖b‖ cos(a, b)
```

Cosine **scaled by both magnitudes**. Use it when magnitude is meaningful (e.g., recommendation models that bake "popularity" or "confidence" into the norm). MIPS = Maximum Inner Product Search.

### The normalized → cosine = dot equivalence (know this cold)

If both vectors are unit length (‖a‖ = ‖b‖ = 1):

```
a · b = ‖a‖ ‖b‖ cos(a,b) = 1 · 1 · cos(a,b) = cos(a,b)
```

So: **normalize once, then use the cheap dot-product metric, and you get exact cosine ranking.** This is why production systems L2-normalize at embed time and configure the index for inner product. It saves the per-query norm computation.

### Euclidean / L2 distance

```
L2(a, b) = sqrt( Σ (a_i − b_i)² )
```

Straight-line distance. For **unit-normalized** vectors, L2 and cosine produce the *same ranking* (they're monotonically related):

```
‖a − b‖² = ‖a‖² + ‖b‖² − 2(a·b) = 1 + 1 − 2 cos(a,b) = 2 − 2 cos(a,b)
→ smaller L2  ⇔  larger cosine.  Same nearest neighbors.
```

So on normalized text vectors, cosine / dot / L2 all rank identically — pick whichever your DB optimizes. On *un-normalized* vectors they differ, and L2 is sensitive to magnitude.

### Manhattan (L1)

```
L1(a, b) = Σ |a_i − b_i|
```

Sum of absolute differences. Rare in semantic search (less aligned with how embeddings are trained), more common in some recommender and tabular settings. Mention it for completeness; don't default to it for text.

### Which metric, when

| Metric | Use when | Notes |
|---|---|---|
| **Cosine** | Text embeddings (default) | Direction = meaning; length-invariant |
| **Dot / IP** | Normalized vectors (= cosine, cheaper) OR magnitude encodes signal (recsys) | MIPS; OpenAI/Cohere vectors normalized |
| **L2 (Euclidean)** | Image embeddings, normalized text (same ranking as cosine) | FAISS default metric |
| **L1 (Manhattan)** | Some tabular / recsys cases | Uncommon for text |

**Interview takeaway:** For text, say "cosine — but since I normalize, I configure the index for inner product, which gives identical ranking with less compute." That one sentence signals you understand the equivalence.

---

## Approximate Nearest Neighbor (ANN) Indexes

The heart of the system. Each index makes a different bet about how to avoid scanning all N vectors. Know HNSW deeply; know IVF and PQ well enough to combine them.

### HNSW — Hierarchical Navigable Small World (the default)

**Intuition: skip lists + small-world graphs.** A skip list speeds up linked-list search by adding sparse "express lanes" on top. HNSW does the same for nearest-neighbor search: it builds a multi-layer graph where the top layers have few nodes with long-range links (express lanes) and the bottom layer has every node with short-range links (local roads). You enter at the top, take big hops to get near the answer, then drop down to refine.

A **navigable small-world (NSW)** graph is one where greedy "always move to the neighbor closest to the query" reaches the true nearest neighbor in a few hops — like the "six degrees of separation" property of social networks. HNSW makes it *hierarchical* for O(log N) navigation.

```
HNSW layered structure (query q enters at the top):

Layer 2 (sparse, long links):   [A]━━━━━━━━━━━━━━━━━━━━[H]
                                  │                      │
Layer 1 (medium):               [A]━━━[D]━━━[F]━━━━━━━━[H]
                                         │
Layer 0 (ALL nodes, dense):  [A]─[B]─[C]─[D]─[E]─[F]─[G]─[H]─[I]
                              └ short, local connections everywhere ┘

Greedy search for q:
  1. Enter at A (top layer). Move to whichever neighbor is closest to q.
     A → H (H is closer to q at layer 2). No closer neighbor → descend.
  2. Layer 1 from H: check H's neighbors (F, ...). F closer → move to F.
     No closer → descend.
  3. Layer 0 from F: explore E, G, ... maintain a candidate set of size ef_search,
     greedily expand the closest unvisited, stop when no improvement.
  4. Return the top-k from the candidate set.

Total hops ≈ O(log N). Each hop touches a handful of neighbors.
```

**Greedy search walkthrough (concrete):** Suppose q is closest to node E. At layer 2 we hop A→H (overshoot, but cheap). At layer 1 we hop H→F (getting warmer). At layer 0 we explore F's neighborhood, keep the `ef_search` best candidates in a priority queue, expand the closest, discover E, find nothing closer, and return E (plus the next-best as the rest of top-k). We touched maybe 50–200 nodes out of 100M.

**Construction.** Insert nodes one at a time. Each new node picks a random maximum layer (geometric distribution — most nodes only exist at layer 0, few reach the top). For each layer from its top down to 0, it runs the same greedy search to find its `M` nearest existing nodes and links to them. `ef_construction` controls how thorough that search is during building.

**Parameters:**

| Param | Meaning | Higher value → | Typical |
|---|---|---|---|
| **M** | Max neighbors per node (graph degree) | Better recall, more memory, slower build | 16–48 |
| **ef_construction** | Candidate list size during *build* | Better graph quality, slower build | 100–400 |
| **ef_search** | Candidate list size during *query* | Higher recall, higher latency | 50–500 (tunable at query time!) |

The killer feature: **`ef_search` is a query-time knob.** You build the graph once, then dial recall vs. latency per query without rebuilding — set `ef_search=64` for a fast path and `ef_search=512` for a high-recall path.

**Memory cost.** HNSW stores the full vectors *plus* the graph edges:

```
Per vector: d × 4 bytes (float32) + M × ~8 bytes (neighbor links, both directions ~2M)
For d=768, M=32:
  vector  = 768 × 4   = 3,072 bytes
  graph   ≈ 2 × 32 × 8 = 512 bytes
  total   ≈ 3,584 bytes/vector
100M vectors ≈ 358 GB RAM.  ← This is why HNSW alone doesn't scale to billions cheaply.
```

**Why it's the default:** highest recall at a given latency, no training step, supports incremental inserts, query-time recall knob. Used by Pinecone, Weaviate, Qdrant, Milvus, pgvector, Elasticsearch/OpenSearch, Lucene. **Cons:** memory-hungry (stores full vectors), deletes are awkward (tombstones; graph degrades, eventually rebuild), build is slower than IVF.

### IVF — Inverted File (cluster-and-probe)

**Intuition:** Partition the space into clusters once; at query time, only search the few clusters near the query instead of all N vectors.

**Mechanism (Voronoi cells via k-means):**
1. **Train** a coarse quantizer: run k-means on a sample to find `nlist` centroids (e.g., 4096). Each centroid "owns" a Voronoi cell.
2. **Assign** every vector to its nearest centroid → an inverted list per centroid (centroid → [vector ids in that cell]).
3. **Query:** find the `nprobe` centroids nearest the query, then brute-force search only the vectors in those `nprobe` lists.

```
Space partitioned into nlist=8 Voronoi cells (centroids ●):

       ●C1      ●C2          q = query
   ┌────────┬────────┐       nprobe=2 → search cells C5 and C6 only
   │  C1    │  C2    │       (the two centroids nearest q),
   ├────────┼────────┤       skip the other 6 cells entirely.
   │  C5  q │  C6    │
   ●C5──────┴──────●C6
```

**Parameters:**

| Param | Meaning | Trade-off |
|---|---|---|
| **nlist** | Number of clusters (centroids) | More cells = fewer vectors/cell = faster probe, but need higher nprobe for recall. Rule of thumb: `nlist ≈ sqrt(N)` to `4·sqrt(N)` |
| **nprobe** | Cells searched per query | Higher = better recall, slower. Query-time knob, like ef_search |

```
N = 100M, nlist = 16,384  → ~6,100 vectors per cell on average
nprobe = 32 → search ~32 × 6,100 = ~195,000 vectors (vs 100M brute force)
            → ~500× fewer distance computations
```

**Training requirement (the catch):** IVF must be *trained* (k-means) on a representative sample before you can add vectors. If your data distribution shifts, the cells become unbalanced (some huge, some empty) and recall drops — you must retrain. HNSW needs no training. The **edge-of-cell problem**: a query near a cell boundary may have its true nearest neighbor in an adjacent, un-probed cell — that's a recall miss, mitigated by higher nprobe.

**When to use:** very large datasets where HNSW memory is too high, and you can tolerate a training step. Almost always combined with **PQ** (next) to cut memory.

### Product Quantization (PQ) — compressing vectors

**The problem PQ solves:** storing full float32 vectors costs too much RAM at billion scale (a 1B × 768 × 4B index = 3 TB). PQ compresses each vector to a few bytes.

**Mechanism:**
1. **Split** each d-dim vector into `m` sub-vectors (e.g., d=768, m=96 → each sub-vector is 8 dims).
2. For each of the m sub-spaces, run k-means to learn a **codebook** of `k=256` centroids (so each centroid id fits in 1 byte).
3. **Encode** a vector by replacing each sub-vector with the *id* of its nearest codebook centroid → the whole vector becomes `m` bytes.

```
Original vector (768 float32 = 3,072 bytes):
  [─sub1─][─sub2─]...[─sub96─]   each sub = 8 floats

After PQ (m=96 sub-vectors, 256 centroids each):
  [id1][id2]...[id96]   each id = 1 byte  → 96 bytes total

Compression: 3,072 → 96 bytes = 32× smaller.
```

**Asymmetric Distance Computation (ADC):** at query time you do *not* quantize the query. Instead, you precompute a lookup table: for each sub-space, the distance from the query's sub-vector to all 256 centroids (m × 256 distances). Then the approximate distance to any stored code is just `m` table lookups + adds — no full distance math. This keeps accuracy higher than quantizing both sides ("symmetric").

```
PQ distance(query, code):
  precompute LUT[m][256] = dist(query_sub_j, centroid_c) for all j, c   # once per query
  for each stored vector with codes [c1..cm]:
      approx_dist = LUT[0][c1] + LUT[1][c2] + ... + LUT[m-1][cm]        # m adds
```

**The memory math (the number to quote):**

```
1 BILLION vectors, d=768:
  float32 (no compression):  1e9 × 768 × 4 B   = 3.07 TB   (won't fit in RAM)
  PQ, m=96, 8-bit codes:     1e9 × 96 × 1 B    = 96 GB     (fits on one big box)
  → 32× memory reduction.
  Cost: recall drops (lossy compression). Typically recall@10 ~0.85–0.95
        depending on m, recoverable by re-ranking the PQ candidates with exact
        distances on the float vectors (if kept on disk/SSD).
```

**IVF-PQ (the workhorse for billion-scale):** combine them — IVF narrows to `nprobe` cells (avoid scanning all N), PQ compresses the vectors in those cells (fit in RAM). This is the standard FAISS recipe for billion-vector indexes (`IndexIVFPQ`). A refinement, **IVF-PQ + reranking** (`IndexIVFPQR` / `OPQ`): retrieve top-100 by PQ approx distance, then re-score those 100 with exact float distances for final ranking.

```python
import faiss
d, nlist, m, nbits = 768, 16384, 96, 8
quantizer = faiss.IndexFlatIP(d)                     # coarse quantizer (centroids)
index = faiss.IndexIVFPQ(quantizer, d, nlist, m, nbits)
index.train(sample_vectors)                          # k-means for IVF + PQ codebooks
index.add(all_vectors)                               # stored as PQ codes
index.nprobe = 32
D, I = index.search(query, k=10)
```

### LSH — Locality-Sensitive Hashing

**Intuition:** design hash functions so that *similar* vectors collide (land in the same bucket) with high probability. Query by hashing the query and only scanning its bucket(s).

For cosine, use **random hyperplane hashing**: pick r random hyperplanes; each vector's hash bit is the sign of its dot product with that hyperplane's normal. Vectors on the same side of all hyperplanes share a hash → likely similar.

```
hash(v) = ( sign(v·r1), sign(v·r2), ..., sign(v·rb) )   # b bits, b random hyperplanes
Similar vectors → same signs → same bucket → small candidate set to brute-force.
Multiple hash tables (L of them) raise recall (a miss in one table may hit another).
```

**Trade-off:** simple, theoretically clean, supports streaming inserts. But in practice it needs many tables/bits to hit high recall, which costs memory, and it generally loses to HNSW on the recall-per-byte and recall-per-millisecond curves. Mostly of historical/theoretical importance now; still used for near-duplicate detection (MinHash for sets).

### Tree-based — Annoy

**Annoy** (Spotify) builds a **forest of random projection trees**. Each tree recursively splits the dataset by a random hyperplane; a leaf holds a small bucket. Querying descends multiple trees and unions the leaf candidates.

```
Random split tree:           Forest = many such trees with different random splits.
        (hyperplane h1)      Query descends all trees, collects candidate leaves,
        /          \         then exact-distances the union → top-k.
   (h2)              (h3)
   /  \             /   \
[leaf][leaf]    [leaf] [leaf]
```

**Trade-off:** memory-mapped files → great for **read-only**, shareable indexes (Spotify serves the same index across many machines via mmap). But the index is **immutable** — you rebuild to add data. Lower recall-per-memory than HNSW. Good when you have a static corpus and want simple, mmap-able files.

### ScaNN — Anisotropic quantization (Google)

**ScaNN's insight:** standard PQ minimizes *reconstruction* error (how well the code approximates the original vector). But for **maximum inner product search** what actually matters is preserving the *inner product with likely query directions*. ScaNN uses **anisotropic vector quantization** — it weights quantization error by how much it distorts inner products in the directions that matter, penalizing errors parallel to the vector more than orthogonal ones. Result: higher recall at the same compression. Combined with a fast SIMD-optimized scan, it tops the ann-benchmarks recall/latency frontier for in-memory MIPS.

**Trade-off:** state-of-the-art speed/recall, but more complex to tune; strongest as a library (or via Vertex AI) rather than a turnkey DB.

### ANN comparison table

| Index | Build time | Query speed | Recall | Memory | Inserts | Training? | Best for |
|---|---|---|---|---|---|---|---|
| **HNSW** | Slow | Very fast | Very high | High (full vecs + graph) | Incremental | No | Default; <~100M, recall-critical |
| **IVF (Flat)** | Fast | Fast | High (tune nprobe) | Full vecs | Add anytime; retrain on drift | Yes (k-means) | Large, memory-ok |
| **IVF-PQ** | Moderate | Fast | Moderate–high | **Very low** (PQ codes) | Add anytime | Yes (k-means + codebooks) | Billion-scale, RAM-bound |
| **PQ (flat)** | Moderate | Fast | Moderate | Very low | Add anytime | Yes (codebooks) | Memory-extreme |
| **LSH** | Fast | Fast | Moderate (needs many tables) | Moderate–high | Streaming | No | Near-dup detection, theory |
| **Annoy** | Moderate | Fast | Moderate | Low (mmap) | **Immutable** (rebuild) | No | Static, read-only, mmap-shared |
| **ScaNN** | Moderate | **Very fast** | Very high | Low–moderate | Rebuild-ish | Yes | In-memory MIPS at scale (Google) |

**Interview takeaway:** Default to **HNSW** for most workloads (<100M, recall matters, RAM available). Reach for **IVF-PQ** when memory is the binding constraint (billions of vectors). Mention **ScaNN** if asked about Google or the absolute speed/recall frontier. Mention **Annoy** for static, mmap-shared, read-only indexes.

---

## The Recall / Latency / Memory Trade-off

Every ANN system lives inside a triangle. You cannot maximize all three; you pick a point.

```
                    RECALL (accuracy)
                        ▲
                       ╱ ╲
                      ╱   ╲
                     ╱     ╲
        LATENCY ◄───╱───────╲───► MEMORY
        (speed)                   (footprint/cost)

  HNSW with high M, high ef_search → high recall, high memory, moderate latency
  IVF-PQ with low m, low nprobe    → low memory, low latency, lower recall
  Brute force                      → perfect recall, huge latency, full memory
```

### Recall@k — the metric

`Recall@k` = of the *true* top-k nearest neighbors (per exact brute force), what fraction did the ANN index return in *its* top-k?

```
True top-10 for a query: {d3, d7, d9, d11, d14, d20, d22, d31, d40, d55}
ANN returned top-10:     {d3, d7, d9, d11, d14, d20, d22, d31, d40, d99}
                          9 of 10 correct → recall@10 = 0.90
```

You compute it by running exact kNN on a sample of queries (the ground truth) and comparing. Target recall depends on the product: web search tolerates ~0.90; medical/legal retrieval may demand ~0.99.

### How parameters tune the triangle

| Want | HNSW lever | IVF / IVF-PQ lever | Side effect |
|---|---|---|---|
| ↑ Recall | ↑ `ef_search`, ↑ `M` | ↑ `nprobe`, ↑ `nlist` resolution, ↓ PQ compression (↑ m) | ↑ latency and/or ↑ memory |
| ↓ Latency | ↓ `ef_search` | ↓ `nprobe` | ↓ recall |
| ↓ Memory | (limited — vecs are full) use PQ variant | use **PQ** (↓ m bytes), 8-bit→4-bit | ↓ recall |

**Concrete tuning scenario (100M, d=768, HNSW):**

```
M=16, ef_search=64   → recall@10 ≈ 0.92, p95 latency ≈ 8 ms,  ~330 GB RAM
M=32, ef_search=128  → recall@10 ≈ 0.97, p95 latency ≈ 15 ms, ~358 GB RAM
M=48, ef_search=512  → recall@10 ≈ 0.99, p95 latency ≈ 40 ms, ~390 GB RAM
```

**Concrete tuning scenario (1B, d=768, IVF-PQ):**

```
m=96 (8-bit), nprobe=16  → recall@10 ≈ 0.82, p95 ≈ 6 ms,  ~96 GB RAM
m=96,         nprobe=64  → recall@10 ≈ 0.90, p95 ≈ 18 ms, ~96 GB RAM
m=96, nprobe=64 + rerank top-200 with float vecs on SSD → recall@10 ≈ 0.96, p95 ≈ 30 ms
```

**The reranking trick to break the triangle:** retrieve a *larger* candidate set cheaply (high speed, lower per-candidate accuracy), then re-score the small candidate set with exact distances (or a cross-encoder). You buy back recall/precision without paying full-index cost.

**Interview takeaway:** Never say "I'll use HNSW" and stop. Say: "HNSW with M=32, and I'd tune `ef_search` against a recall@10 target of 0.97 measured on a golden set, accepting ~15 ms p95 and ~358 GB RAM — if memory is the constraint I'd switch to IVF-PQ and rerank." That's the senior answer.

---

## Building a RAG / Semantic-Search Pipeline

RAG = Retrieval-Augmented Generation: retrieve relevant chunks from a vector store, inject them into an LLM prompt, generate a grounded answer. Semantic search is the same pipeline minus the generation step. Retrieval quality dominates final quality — "garbage retrieved, garbage generated."

```
INGEST (offline):  Docs → Parse → Chunk → Embed → Upsert(vector + metadata)
QUERY  (online):   Query → Embed → ANN retrieve top-k (+ BM25) → Fuse → Rerank → top 3-5 → LLM
```

### Chunking strategies

You don't embed whole documents — you embed **chunks**, because (a) embedding models have token limits (256–512 tokens is the trained sweet spot for many), and (b) retrieval precision needs the *relevant passage*, not a 50-page PDF.

| Strategy | How | Best for | Pitfall |
|---|---|---|---|
| **Fixed-size** | Every N tokens (e.g., 512) | Quick start | Cuts mid-sentence, splits ideas |
| **Recursive character** | Split on `\n\n`, then `\n`, then `. `, then space until ≤ N | General text (default) | Still misses semantic units |
| **Sentence / paragraph** | Split on sentence/para boundaries | FAQs, articles | Uneven sizes |
| **Semantic chunking** | Embed sentences; split where consecutive similarity drops | Dense technical docs | Expensive (embed to chunk) |
| **Structural (Markdown/HTML)** | Split on headers H1/H2/H3, code blocks, tables | Docs, wikis | Uneven chunk sizes |
| **Parent–child** | Retrieve small child chunk, feed larger parent to LLM | Precision + context | Two-level indexing |

**Overlap.** Adjacent chunks share a sliding window (e.g., 50–100 tokens) so a sentence split across a boundary still appears whole in at least one chunk. Costs storage (more chunks) but prevents "answer cut in half" misses.

**The size trade-off (with examples):**

```
Chunk too SMALL (e.g., 64 tokens):
  Chunk = "Click Settings, then Security."
  Query = "how do I enable two-factor authentication?"
  → retrieved, but lacks the surrounding steps → LLM can't answer fully. (low context)

Chunk too LARGE (e.g., 2000 tokens):
  Chunk = entire 8-page "Account Security" article.
  Query = "reset password" → chunk matches, but 95% is irrelevant text that
          dilutes the embedding (averaged meaning) AND wastes the LLM context window.
          The relevant 2 sentences are buried. (low precision, high cost)

Sweet spot: 256–512 tokens, 10–20% overlap.
```

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

splitter = RecursiveCharacterTextSplitter(
    chunk_size=512, chunk_overlap=64,           # ~512 tokens, ~12% overlap
    separators=["\n\n", "\n", ". ", " ", ""],   # prefer semantic boundaries
)
chunks = splitter.split_text(document_text)
```

**Metadata is non-negotiable** — store it alongside every vector for filtering and citation:

```python
record = {
    "id": "doc42#chunk7",
    "vector": embed(chunk_text),
    "metadata": {
        "text": chunk_text,
        "source": "security_guide_v3.pdf",
        "page": 12, "section": "Two-Factor Auth",
        "tenant_id": "acme", "acl": ["support", "admin"],
        "created_at": "2025-02-01", "doc_id": "doc42",
    },
}
```

### Embed + upsert

Use the **same model** for ingest and query (different models → incompatible geometry → garbage retrieval). Normalize. Upsert in batches.

```python
import itertools
def batched(it, n):
    it = iter(it)
    while batch := list(itertools.islice(it, n)):
        yield batch

for batch in batched(chunks, 256):
    vecs = model.encode([c.text for c in batch], normalize_embeddings=True)
    index.upsert([(c.id, v, c.metadata) for c, v in zip(batch, vecs)])
```

### Retrieval top-k

Retrieve more than you'll show the LLM (e.g., top-20–50), then narrow via fusion/rerank. Over-retrieving improves the chance the right chunk is in the candidate set.

```python
q = model.encode(user_query, normalize_embeddings=True)
candidates = index.search(q, k=30, filter={"tenant_id": "acme"})
```

### Metadata filtering — pre- vs post-filter (a real correctness/perf trap)

You often must restrict results ("only this tenant," "only docs the user can see," "only after 2024"). There are two ways, and the difference is a classic interview gotcha:

```
POST-FILTER:  ANN returns top-k by vector distance, THEN drop those failing the predicate.
  Problem: if only 1% of vectors match the filter, your top-30 might contain ZERO matches
           → you return nothing, even though good matches exist deeper in the ranking.
           Correctness bug. To compensate you over-fetch (k=3000), which is slow.

PRE-FILTER:  Restrict the candidate set to matching vectors FIRST, then do ANN within it.
  Correct results, but naive pre-filtering breaks the ANN graph (HNSW navigates through
  nodes that may be filtered out → can't traverse → recall collapses).

PRODUCTION ANSWER: "filtered ANN" — the index integrates the predicate INTO traversal.
  Qdrant: payload index + filterable HNSW. Weaviate/Milvus: similar. pgvector: combine
  with a B-tree/partial index, or partition by tenant. For very selective filters (a
  handful of matches), fall back to exact brute force over the matching subset — it's tiny.
```

```python
# Qdrant filtered search — predicate is applied DURING graph traversal
from qdrant_client.models import Filter, FieldCondition, MatchValue
hits = client.search(
    collection_name="docs",
    query_vector=q,
    query_filter=Filter(must=[FieldCondition(key="tenant_id", match=MatchValue(value="acme"))]),
    limit=30,
)
```

**Interview takeaway:** When asked "how do you restrict search to a tenant?" the wrong answer is "filter the results afterward." The right answer names the post-filter recall bug and proposes filtered-ANN (predicate fused into traversal) or partitioning, with exact brute force for highly selective filters.

### Hybrid search — dense + sparse (BM25) with RRF

Dense embeddings miss exact strings (SKUs, error codes, rare names); BM25 nails them. BM25 misses paraphrase; dense nails it. Run **both** and fuse.

**Reciprocal Rank Fusion (RRF)** combines ranked lists using only the *rank* (not the raw, incomparable scores):

```
RRF_score(doc) = Σ_over_lists  1 / (k + rank_in_that_list)      # k ≈ 60 by convention

A doc ranked #1 by BM25 and #3 by dense:  1/(60+1) + 1/(60+3) = 0.0164 + 0.0159 = 0.0323
A doc ranked #2 by dense only:            1/(60+2)            = 0.0161
→ The doc both methods like ranks highest. Robust, no score normalization needed.
```

```python
def rrf(rank_lists, k=60, top_n=20):
    scores = {}
    for ranked in rank_lists:                       # each is [doc_id, ...] best-first
        for rank, doc_id in enumerate(ranked):
            scores[doc_id] = scores.get(doc_id, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)[:top_n]

dense_hits = [h.id for h in index.search(q, k=50)]
bm25_hits  = [h.id for h in bm25.search(user_query, k=50)]
fused = rrf([dense_hits, bm25_hits])
```

### Reranking — the two-stage retrieve → rerank pattern

Retrieval uses a **bi-encoder** (query and doc embedded *independently*) — fast, scalable, but it never lets the query and document "see" each other, so it's coarse. A **cross-encoder** feeds `[query, doc]` *together* through a transformer with full cross-attention and outputs a single relevance score — far more accurate, but O(candidates) forward passes, so you can't run it over the whole corpus.

**The two-stage architecture resolves this:** retrieve top-30–50 cheaply with the bi-encoder ANN index, then **rerank just those 30–50** with the cross-encoder and keep the top 3–5 for the LLM.

```
Stage 1 (recall):    bi-encoder ANN over 100M docs → top 50 candidates   (fast, coarse)
Stage 2 (precision): cross-encoder scores 50 (query,doc) pairs → top 5   (slow, accurate)
                     50 forward passes is cheap; 100M would be impossible.
```

```python
from sentence_transformers import CrossEncoder
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")

def retrieve_and_rerank(query, top_n=5):
    q = model.encode(query, normalize_embeddings=True)
    candidates = index.search(q, k=50)                      # bi-encoder, fast
    pairs = [(query, c.metadata["text"]) for c in candidates]
    scores = reranker.predict(pairs)                        # cross-encoder, accurate
    ranked = [c for _, c in sorted(zip(scores, candidates), key=lambda x: -x[0])]
    return ranked[:top_n]
```

Commercial rerankers: **Cohere Rerank, Voyage rerank, Jina Reranker**. Reranking 50 docs adds ~30–80 ms but lifts answer quality substantially — almost always worth it in production.

### Putting it together — query pipeline

```python
def rag_answer(user_query, tenant_id, user_acl):
    q = model.encode(user_query, normalize_embeddings=True)
    dense = index.search(q, k=50, filter={"tenant_id": tenant_id, "acl": {"$in": user_acl}})
    bm25  = bm25_index.search(user_query, k=50, filter={"tenant_id": tenant_id})
    fused_ids = rrf([[h.id for h in dense], [h.id for h in bm25]], top_n=50)
    fused = [lookup(i) for i in fused_ids]
    top = rerank(user_query, fused, top_n=5)
    context = "\n\n".join(
        f"[{c.metadata['source']} p{c.metadata['page']}]\n{c.metadata['text']}" for c in top
    )
    return llm.generate(
        f"Answer using ONLY this context. Cite sources.\n\n{context}\n\nQ: {user_query}"
    )
```

---

## Vector Database Systems

You can use a **library** (FAISS, ScaNN, Annoy — you manage storage, sharding, persistence, filtering yourself) or a **database** (Pinecone, Weaviate, Milvus, Qdrant, pgvector — they add metadata, filtering, replication, APIs, persistence).

### pgvector (Postgres extension) — the "use what you have" choice

If you're already on Postgres, `pgvector` adds a `vector` column type plus HNSW and IVF indexes. You get SQL joins, transactions, existing backups/replication, and ACID filtering *for free*.

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE chunks (
    id        bigserial PRIMARY KEY,
    doc_id    text,
    tenant_id text,
    page      int,
    text      text,
    embedding vector(768)          -- 768-dim dense vector
);

-- HNSW index (cosine). vector_ip_ops for inner product, vector_l2_ops for L2.
CREATE INDEX ON chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Partial index for a tenant (helps filtered search)
CREATE INDEX ON chunks (tenant_id);

-- Query: top-10 nearest, filtered by tenant (pre-filter via WHERE + index)
SET hnsw.ef_search = 100;          -- query-time recall knob
SELECT id, doc_id, page, text,
       1 - (embedding <=> $1) AS cosine_similarity   -- <=> is cosine distance
FROM chunks
WHERE tenant_id = 'acme'
ORDER BY embedding <=> $1          -- <=> cosine, <#> inner product, <-> L2
LIMIT 10;
```

`<=>` = cosine distance, `<#>` = negative inner product, `<->` = L2. **Caveat:** at very high N (>50–100M) and high-selectivity filters, pgvector's HNSW can lose recall under tight `WHERE` filters; partition by tenant or move to a dedicated vector DB.

### The major systems

| DB | Type | Index | Scale | Filtering | Highlights | Best for |
|---|---|---|---|---|---|---|
| **pgvector** | Postgres ext | HNSW, IVFFlat | ~10s of M | SQL `WHERE` (pre-filter) | SQL joins, ACID, reuse infra | Already on Postgres |
| **Pinecone** | Managed SaaS | proprietary (HNSW-like) | Billions | Metadata filters | Zero ops, auto-scale, serverless | Fast to production |
| **Weaviate** | OSS + Cloud | HNSW | Millions–B | Strong, filterable HNSW | GraphQL, modules, hybrid built-in | Feature-rich OSS, hybrid |
| **Qdrant** | OSS + Cloud | HNSW | Millions–B | **Excellent** payload + filterable HNSW | Rust, fast, quantization built-in | Filtered search, performance |
| **Milvus** | OSS + Cloud | HNSW, IVF-PQ, DiskANN, GPU | **Billions** | Yes | Most scalable OSS, many index types | Massive self-hosted |
| **FAISS** | Library | Flat, HNSW, IVF, IVF-PQ, OPQ | Billions | DIY | Max control, GPU, all algorithms | Research, custom infra |
| **ScaNN** | Library | Anisotropic + tree | Billions | DIY | Fastest in-memory MIPS (Google) | Speed-critical MIPS |
| **Annoy** | Library | RP-tree forest | Millions | DIY | mmap, immutable, simple | Static read-only, recsys |
| **Elasticsearch / OpenSearch** | Search engine | HNSW (Lucene) | Millions–B | Native | Best hybrid (BM25 + vector in one) | Already on ES, hybrid |

### Managed vs self-hosted

| | Managed (Pinecone, Weaviate Cloud, Qdrant Cloud) | Self-hosted (Milvus, Qdrant, FAISS) |
|---|---|---|
| **Ops burden** | Near zero | You run sharding, replication, upgrades |
| **Cost** | $ per pod/usage (can be high at scale) | Hardware + eng time |
| **Control** | Limited tuning | Full (custom indexes, GPU) |
| **Data residency** | Their cloud (compliance concerns) | Your infra |
| **Scale ceiling** | Very high (their problem) | Yours to engineer |

**Interview takeaway:** Default recommendation — "If we're on Postgres and < ~10M vectors, pgvector. For fast time-to-production, Pinecone. For self-hosted scale with filtering, Qdrant or Milvus. For maximum control / research / GPU / billion-scale custom, FAISS. If we already run Elasticsearch and need hybrid, use its native kNN."

---

## Scaling, Updates & Operations

### Sharding

At billions of vectors, one machine can't hold the index. Shard the vectors across nodes; query all shards in parallel; merge the per-shard top-k.

| Strategy | How | Pro | Con |
|---|---|---|---|
| **Shard by id (random/hash)** | `hash(id) % num_shards` | Even load, simple | **Every query hits every shard** (scatter-gather) |
| **Shard by cluster (IVF centroid)** | Route query to shards owning the nearest centroids | Query touches few shards | Skewed cells = hot shards; rebalancing on drift |
| **Shard by tenant/metadata** | One shard (or index) per tenant | Filtered queries hit one shard; isolation | Uneven tenant sizes; many small indexes |

```
SCATTER-GATHER (hash sharding):
  Query → [shard0 top-k][shard1 top-k]...[shardN top-k] → merge → global top-k
  Latency = max(shard latency) + merge. Tail latency dominated by the slowest shard.

ROUTED (cluster sharding):
  Query → nearest 2 centroids → only their 2 shards → merge.
  Fewer shards touched → less load, but a query near a boundary may miss → lower recall.
```

### Replication

Each shard is replicated (e.g., 3×) for availability and read throughput. Reads load-balance across replicas; a replica failure doesn't drop data. Writes go to a primary and propagate. Same leader-follower trade-offs as any distributed store (replication lag → a just-upserted vector may not yet be searchable on all replicas → "freshness").

### Inserts vs deletes — the hard part

**Inserts** are easy for HNSW (incremental graph insertion) and IVF (assign to nearest cell). The cost: HNSW insertion runs a search to find neighbors (≈ query cost), so high write rates are heavier than reads.

**Deletes** are the genuinely hard problem:
- HNSW graphs don't support clean node removal — deleting a node would orphan its neighbors' links and degrade navigability.
- The standard solution is **tombstones (soft delete):** mark the vector deleted, keep it in the graph, filter it out of results at query time.
- Tombstones accumulate → wasted memory + degraded recall (the graph routes through dead nodes) → periodic **rebuild/compaction** to physically remove them, analogous to LSM-tree compaction.

```
Delete v:  mark v.deleted = true   (tombstone; still in graph, filtered at query)
When tombstone ratio > ~20-30%  →  rebuild index from live vectors  (offline or shadow)
```

IVF handles updates better (just drop the id from a cell's list), but accumulated churn unbalances cells → eventual retrain.

### Filtered search at scale (recap with the scaling angle)

The pre/post-filter problem (from the RAG section) gets worse at scale. For **selective** filters (few matches), exact brute force over the matching subset beats ANN. For **non-selective** filters, filtered-HNSW or partitioning. Partitioning by the common filter key (tenant, time bucket) is often the cleanest: each partition is its own small index, queried directly — no recall loss.

### Re-embedding when the model changes (full rebuild)

This is the operational elephant. A new embedding model = new geometry = **every vector must be recomputed and the index rebuilt**. Old and new vectors are not comparable; you cannot incrementally migrate.

```
Blue/Green re-embed (zero-downtime):
  1. Stand up a NEW index (green) alongside the live one (blue).
  2. Re-embed the whole corpus with the new model → populate green.
  3. Validate: run the golden query set against green; require recall@10 ≥ blue.
  4. Dual-write new ingests to both during the transition.
  5. Cut traffic over to green; decommission blue.

Cost (100M chunks): ~28 GPU-hours embed + index build + 2× storage during overlap.
```

### Freshness

How fast must a new document be searchable? Real-time chat memory needs seconds; a docs corpus can tolerate hours. Patterns: a small **hot index** (recent inserts, frequently rebuilt or HNSW with fast inserts) merged with a large **cold index** (rebuilt nightly); queries hit both and merge. Trade freshness against rebuild cost.

**Interview takeaway:** "Deletes via tombstones + periodic rebuild; inserts incremental but ~as costly as a query; model upgrades force a full blue/green re-embed — that's the biggest operational risk, budget ~28 GPU-hours per 100M chunks." Saying this signals real operational experience.

---

## Evaluation

You cannot tune recall/latency/memory without measuring. Build a **golden set** and track retrieval metrics offline, then confirm online.

### Building a golden set

A golden set is a list of `(query, relevant_doc_ids)` pairs — the ground truth of what *should* be retrieved.

Sources: hand-labeled by experts; mined from click logs (clicked results = relevant); or **synthetically generated** (LLM reads each chunk and writes a question it answers → (question, chunk_id) is a positive pair). Aim for a few hundred to a few thousand queries spanning head (common) and tail (rare) cases.

### Retrieval metrics

| Metric | Formula / idea | Captures |
|---|---|---|
| **Recall@k** | (relevant retrieved in top-k) / (total relevant) | Did we *find* the right docs? |
| **Precision@k** | (relevant in top-k) / k | Are top-k *clean* (not noisy)? |
| **MRR** | mean of 1/rank of the first relevant result | How high is the *first* good hit? |
| **nDCG@k** | DCG / ideal DCG, with graded relevance & position discount | Ranking quality with graded relevance |
| **Hit@k** | fraction of queries with ≥1 relevant in top-k | Coarse "did we get anything right?" |

```
MRR example:  query A first-relevant at rank 1 → 1/1
              query B first-relevant at rank 3 → 1/3
              query C first-relevant at rank 2 → 1/2
              MRR = (1 + 0.333 + 0.5) / 3 = 0.611

nDCG@k:  DCG = Σ_i  rel_i / log2(i+1)   (rel can be graded 0/1/2/3)
         nDCG = DCG / IDCG (DCG of the perfect ranking). Range [0,1].
         Rewards putting the most-relevant doc at the top, not just somewhere in top-k.
```

```python
def recall_at_k(retrieved_ids, relevant_ids, k):
    top = set(retrieved_ids[:k])
    return len(top & set(relevant_ids)) / len(relevant_ids)

def mrr(list_of_retrieved, list_of_relevant):
    total = 0.0
    for retrieved, relevant in zip(list_of_retrieved, list_of_relevant):
        rel = set(relevant)
        for rank, doc in enumerate(retrieved, start=1):
            if doc in rel:
                total += 1.0 / rank
                break
    return total / len(list_of_retrieved)
```

### ANN recall vs end-to-end recall (don't conflate)

Two different "recall" numbers:
- **ANN recall@k** — does the index return the *exact* nearest vectors? (Index quality; ground truth = brute force.)
- **Retrieval recall@k** — did we retrieve the *truly relevant documents*? (System quality; ground truth = golden labels.)

You can have 0.99 ANN recall but poor retrieval recall if the *embedding model* (not the index) is bad — the index faithfully returns the wrong neighbors. Diagnose by comparing ANN-vs-brute-force (isolates index) against golden-set recall (isolates whole system).

### Offline vs online

| | Offline | Online |
|---|---|---|
| **Signal** | Recall@k, nDCG, MRR vs golden set | Click-through, dwell time, answer thumbs-up, task success |
| **Speed** | Minutes | Days (statistical significance) |
| **Use** | Gate every change (model/index/chunking) | A/B test the winners; catch real-world gaps |

**For full RAG** (with generation), add faithfulness/groundedness and answer-relevance (RAGAS, LLM-as-judge) — but retrieval recall is the upstream lever; fix it first.

**Interview takeaway:** "I'd build a golden set (synthetic + log-mined), track recall@k and nDCG offline to gate index/model/chunking changes, separate ANN recall from retrieval recall to localize regressions, and A/B test online for click-through and answer success."

---

## Designing Search over 100M Documents (Worked Example)

**Prompt:** "Design semantic search / RAG over 100 million documents with sub-100 ms p95 latency."

Walk it as: clarify → estimate → embedding → chunking → index → sharding → hybrid+rerank → budget.

### 1. Clarify requirements

- 100M *documents*; after chunking, expect ~5 chunks/doc → **~500M vectors**.
- Latency target: p95 < 100 ms end-to-end. Recall target: recall@10 ≥ 0.95.
- Filters: tenant + ACL + date. Freshness: new docs searchable within minutes. Read-heavy (1000s QPS).

### 2. Back-of-envelope sizing

```
Vectors: 100M docs × 5 chunks = 500,000,000 chunks
Model: bge-base, d=768, normalized → use inner-product metric
Raw float32 storage: 500M × 768 × 4 B = 1.536 TB  (too big for one box's RAM)
```

This number forces the architecture: 1.5 TB of raw vectors → either many HNSW machines or compress with PQ. We'll do **IVF-PQ + sharding + reranking**.

### 3. Embedding model

- **`bge-base-en-v1.5` (768-dim)** — strong open-source, self-hostable (no per-call API cost at 500M scale), 256–512 token sweet spot. L2-normalize → inner-product metric.
- Fine-tune later on mined (query, clicked-chunk) pairs if golden-set recall is weak.
- Embedding cost: 500M chunks ÷ 1000 chunks/s/GPU = 500K GPU-sec ≈ 139 GPU-hours (one-time, parallelizable across GPUs).

### 4. Chunking

- **Recursive character split**, 512 tokens, 64-token overlap, prefer header/paragraph boundaries (structural for the docs that have markup).
- Store metadata: `{text, doc_id, source, page, tenant_id, acl[], created_at}`.

### 5. Index choice + params

500M vectors → memory is the binding constraint → **IVF-PQ** (compress) with a **rerank** stage:

```
IVF:  nlist = 4 × sqrt(500M) ≈ 4 × 22,360 ≈ 90,000 centroids
      → ~5,500 vectors per cell.   nprobe = 64 (query-time tunable).
PQ:   d=768, m=96 sub-vectors (8 dims each), 8-bit codes (256 centroids/sub).
      Per-vector storage: 96 bytes (+ a few bytes overhead).
Memory: 500M × ~100 B ≈ 50 GB of PQ codes  ← now fits across a few machines.
Rerank: keep full float vectors on NVMe SSD; for the top-200 IVF-PQ candidates,
        re-score with exact inner product → recovers recall@10 to ~0.96.
```

Compared with HNSW-flat which would need ~500M × 3.5 KB ≈ **1.75 TB RAM** (many more machines) — IVF-PQ is ~35× cheaper on memory, accepting a rerank step.

### 6. Sharding & replication

```
Shard by hash(chunk_id) into, say, 8 shards → ~62.5M vectors / ~6.5 GB PQ codes each.
Each shard: 3 replicas (availability + read throughput).
Query = scatter-gather: fan out to 8 shards, each returns top-50, merge → top-200,
        then rerank. Latency ≈ max(shard) + merge + rerank.
For tenant isolation, optionally co-locate a tenant's chunks (route filtered queries
to fewer shards). Large tenants get dedicated indexes.
```

### 7. Hybrid + rerank pipeline

```
Query
  ├─► embed (bge-base) → IVF-PQ ANN (nprobe=64) per shard → merge top-200   [~25 ms]
  ├─► BM25 (Elasticsearch/Lucene) → top-100                                  [~15 ms, parallel]
  ▼
RRF fuse (k=60) → top-100
  ▼
Cross-encoder rerank (ms-marco MiniLM) on 100 → top-5                        [~40 ms]
  ▼
(RAG) inject top-5 into LLM prompt with citations
```

### 8. Latency & resource budget

```
Embed query (1 forward pass, GPU/CPU)     ~5 ms
IVF-PQ scatter-gather (8 shards parallel) ~25 ms  (p95; tail = slowest shard)
BM25 (parallel, overlaps)                 ~15 ms
RRF fuse                                  ~2 ms
SSD rerank of top-200 (exact float)       ~10 ms
Cross-encoder rerank top-100              ~40 ms
-----------------------------------------------
End-to-end p95                            ~80 ms  ✓ under 100 ms
Recall@10 (post-rerank)                   ~0.96   ✓
Memory (PQ codes, replicated 3×)          ~150 GB total  (50 GB × 3)
One-time embed                            ~139 GPU-hours
```

### 9. Trade-offs to state aloud

- **IVF-PQ vs HNSW:** chose PQ for ~35× memory savings; pay with a rerank stage and a k-means training step (retrain on drift). If memory weren't constrained, HNSW (M=32) would give ~0.97 recall with no rerank but ~1.75 TB RAM.
- **nprobe / ef_search** are the live recall-vs-latency knobs.
- **Filtering:** filtered-IVF or tenant partitioning; exact brute force for highly selective ACL filters.
- **Model upgrade:** blue/green full re-embed (~139 GPU-hours), validate on golden set, cut over.
- **Freshness:** small hot HNSW index for recent inserts merged with the big IVF-PQ cold index; nightly compaction.

**Interview takeaway:** The number `500M vectors → 1.5 TB raw` is what justifies every later decision (PQ, sharding, rerank). Derive it early and let it drive the design.

---

## Architecture / Diagrams

### Full RAG Pipeline (ingest + query)

```
══════════════════════════ INGEST (offline) ══════════════════════════

[Raw Docs]→[Parse]→[Clean]→[Chunk 512/64]→[Embed bge-768]→[Upsert]
 PDF/HTML   text    norm     recursive       normalize       vector + metadata
 DOCX/MD    extract ws       split           (unit vecs)     → Vector DB (IVF-PQ/HNSW)
                                                              → BM25 inverted index

══════════════════════════ QUERY (online) ════════════════════════════

[User Query]
     │
     ├─►[Embed Query (same model!)]─►[ANN search + metadata filter]─►top-50
     │                                                                   │
     └─►[BM25 keyword search + filter]──────────────────────────►top-50  │
                                                                   │      │
                                            [RRF fuse: 1/(k+rank)]◄┘──────┘
                                                       │
                                          [Cross-encoder rerank top-50]
                                                       │
                                               [Top 3–5 chunks]
                                                       │
                                      [Inject into LLM prompt + cite]
                                                       │
                                            [Grounded answer]
```

### HNSW search

```
QUERY q = [0.12, -0.43, 0.87, ...]

Layer 2 (sparse, long links):   [N1]━━━━━━━━━━━━━━━[N8]
                                  │                 │
Layer 1 (medium):               [N1]━[N3]━[N5]━━━━[N8]
                                          │
Layer 0 (all nodes, local):  [N1]─[N2]─[N3]─[N4]─[N5]─[N6]─[N7]─[N8]─[N9]

1. Enter top layer at N1, greedily hop toward q  → N8
2. Descend to L1, hop                            → N5
3. Descend to L0, expand candidate set (ef_search), refine → top-k
Result: approx nearest neighbors in ~O(log N) hops.
```

### IVF-PQ retrieval

```
Query q
   │
   ▼  find nprobe nearest centroids (coarse quantizer)
[C12][C57][C90][...]   ← nprobe=64 cells chosen out of nlist=90,000
   │
   ▼  scan only those cells' PQ codes (96 bytes each) via ADC lookup table
[approx top-200]
   │
   ▼  (optional) rerank with exact float vectors from SSD
[top-10]
```

### Sharded vector service

```
                       ┌──────────────┐
   Query ─────────────►│ Query Router │  embed + fan-out
                       └──────┬───────┘
        ┌──────────────┬──────┴───────┬──────────────┐
        ▼              ▼              ▼              ▼
   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐
   │ Shard 0 │    │ Shard 1 │    │ Shard 2 │    │ Shard 3 │   each: 3 replicas,
   │ IVF-PQ  │    │ IVF-PQ  │    │ IVF-PQ  │    │ IVF-PQ  │   ~62M vecs, ~6.5GB
   └────┬────┘    └────┬────┘    └────┬────┘    └────┬────┘
        └─────top-50───┴──────merge───┴─────top-50───┘
                          │
                    [global top-200] → RRF (with BM25) → rerank → top-5
```

### Vector vs lexical vs hybrid

```
                 RECALL on meaning   PRECISION on exact terms
  Dense only     ████████████░░░░    ████░░░░░░░░░░░░
  BM25 only      ████░░░░░░░░░░░░    ████████████░░░░
  Hybrid (RRF)   ████████████████    ████████████████   ← best of both
```

---

## Real-World Examples

### Google Search / YouTube (ScaNN)
Embedding-based retrieval ("neural matching") finds semantically related results; ScaNN's anisotropic quantization serves billion-vector MIPS in milliseconds. YouTube recommendations are two-tower retrieval (user tower, video tower) → ANN over the video embedding index. **Lesson:** at Google scale, quantization quality (recall-per-byte) is the whole ballgame.

### Meta Ads & FAISS
Ads retrieval: a request embeds user/context, FAISS returns thousands of candidate ads from billions, then a heavy ranker scores them. FAISS IVF-PQ on GPU drives the candidate-generation stage. **Lesson:** two-stage (cheap ANN retrieve → expensive rerank) is universal.

### Spotify (Annoy)
Music recommendations: embed tracks/users, Annoy's mmap-able read-only forest serves the same static daily-built index across many machines cheaply. **Lesson:** for a static corpus, an immutable mmap index is operationally simple and memory-efficient.

### Pinterest visual search (PinSage)
Embed pins (image + text), ANN retrieve visually/semantically similar pins over billions. **Lesson:** multimodal embeddings + ANN power "more like this."

### Perplexity / enterprise RAG (Glean, Notion AI, Microsoft 365 Copilot)
Query → hybrid retrieve (dense + BM25) over chunked corpus → rerank → LLM with citations. Copilot adds **ACL-aware filtered search** — you only retrieve documents you're permitted to see (the pre/post-filter correctness issue is a real security requirement, not just performance). **Lesson:** filtering correctness = security boundary.

### Semantic cache for LLMs
Embed each incoming LLM query; if a past query's vector is within cosine 0.97, return the cached answer — skip an expensive LLM call. A vector DB used as a cache. **Lesson:** vector search isn't only for documents.

### Near-duplicate detection / dedup
Embed content, find pairs above a high similarity threshold to dedup a corpus or detect plagiarism / repost spam. **Lesson:** the same NN machinery serves dedup, not just search.

---

## Real-Life Analogies

*One vivid frame: a vast, smart library where books are placed by meaning, not just by title.*

| Concept | Library Analogy |
|---|---|
| **Embedding** | A book's location in a "meaning map" — books on similar topics sit on nearby shelves, regardless of title spelling |
| **Vector space** | The whole floor plan where proximity = topical similarity, not alphabetical order |
| **Dimensionality (768)** | The number of independent ways books can differ (topic, tone, era, difficulty, ...) — 768 such axes |
| **Cosine similarity** | Comparing the *direction* you walk to reach two books from the entrance, ignoring how far each is |
| **Normalization (unit vectors)** | Putting every book at the same distance from the entrance, so only the *direction* (meaning) matters |
| **Exact kNN** | Walking past *every* shelf to find the closest book — correct but you'd spend all day |
| **Curse of dimensionality** | In a building with 768 floors, every book ends up "near a wall," so shortcuts (skip whole wings) stop working |
| **ANN** | A clever guide who takes you *almost* always to the right shelf in seconds, occasionally missing by one |
| **HNSW** | Express elevators (top floors, few stops) to get you to the right wing fast, then local stairs to the exact shelf |
| **IVF (clusters)** | The library is divided into themed rooms; you only enter the few rooms nearest your topic |
| **nprobe** | How many themed rooms you're willing to walk into before settling for what you found |
| **Product Quantization** | Replacing each book with a compact index card describing it — 32× lighter to carry, slightly fuzzy |
| **Reranking (cross-encoder)** | After a runner brings 50 candidate books, the expert librarian reads each against your exact question and hands you the best 5 |
| **Hybrid search** | Using both the meaning-map *and* the old title catalogue, because some patrons ask by exact title (an ISBN) and some by vibe |
| **Chunking** | Cutting fat books into chapters so the runner can hand you just the relevant chapter, not the whole tome |
| **Metadata filter** | "Only books from the law section that you're cleared to read" — applied while searching, not after |
| **Tombstone delete** | A "withdrawn" sticker on a book still on the shelf — ignored by patrons until the next big reshelving |
| **Re-embedding (model change)** | The library adopts a new classification system — every book must be re-placed and the whole map redrawn |
| **Recall@k** | Of the 10 best books that exist for your question, how many the guide actually brought you |

---

## Memory Tricks / Mnemonics

**ANN index pick — "HIP-LAS"**
- **H**NSW — default (graph, high recall, high memory)
- **I**VF — clusters (probe nearby cells)
- **P**Q — compress (codes, low memory)
- **L**SH — hashing (similar collide)
- **A**nnoy — trees (mmap, immutable)
- **S**caNN — anisotropic (Google, fast MIPS)

**The trade-off triangle — "RLM, pick a point"**
**R**ecall / **L**atency / **M**emory — you optimize two, sacrifice the third. (Reranking lets you cheat a little.)

**Distance default — "Cosine for text; normalize and it's just dot."**
Unit vectors ⇒ cosine = dot product = (monotone with) L2. Same neighbors.

**HNSW knobs — "M builds it, ef searches it."**
`M` and `ef_construction` set graph quality at build time; `ef_search` tunes recall at query time (the live knob).

**IVF knobs — "nlist cuts the cake, nprobe takes the slices."**
More `nlist` = smaller cells; more `nprobe` = more cells searched = higher recall.

**RAG retrieval order — "Chunk, Embed, Retrieve, Fuse, Rerank, Generate" → "CERFRG"**
("Can Every Robot Find Really Good [answers]")

**RRF formula — "one over k-plus-rank, summed."** `Σ 1/(60 + rank)`.

**Bi vs cross — "Bi is fast and blind; cross is slow and sees."**
Bi-encoder embeds separately (scalable retrieval); cross-encoder reads the pair together (accurate rerank).

**The hidden cost — "New model, new map."**
Change the embedding model ⇒ re-embed everything ⇒ rebuild the index.

---

## Common Interview Questions

### Q1: Why not just use exact kNN or a k-d tree for vector search?

**Model answer:** Exact kNN is O(N·d) per query — at 100M vectors × 768 dims that's ~77B operations, multiple seconds per query, unusable. k-d trees (and other space-partition trees) work in low dimensions but collapse under the curse of dimensionality: in high-d, distances concentrate (nearest and farthest neighbors become nearly equidistant) and almost all volume is near cell boundaries, so the pruning that makes trees fast almost never fires — they degrade to near-brute-force. That's why we use ANN (HNSW/IVF/PQ): accept ~95–99% recall for a 100–1000× speedup.

**Follow-ups:** *At what N do you switch from brute force to ANN?* (~100K–1M; below that, exact is fine and simpler.) *What's the recall cost?* (Tunable via ef_search/nprobe; measure on a golden set.)

### Q2: Explain HNSW. Why is it the default?

**Model answer:** HNSW is a hierarchical, navigable small-world graph — a skip-list idea applied to nearest-neighbor search. Upper layers are sparse with long-range links (express lanes); the bottom layer holds all nodes with short local links. You enter at the top, greedily hop toward the query, descend layer by layer, and refine at layer 0 keeping `ef_search` candidates. Search is ~O(log N). It's the default because it gives the highest recall at a given latency, needs no training step, supports incremental inserts, and exposes a query-time recall knob (`ef_search`). Its costs are high memory (stores full vectors plus graph edges — ~3.5 KB/vector at d=768, M=32) and awkward deletes (tombstones + periodic rebuild).

**Follow-ups:** *What do M, ef_construction, ef_search do?* (Graph degree; build-time search width; query-time search width.) *Memory for 100M vectors?* (~358 GB.) *How do you delete?* (Tombstone, filter at query, rebuild when bloat exceeds ~25%.)

### Q3: How does IVF-PQ let you index a billion vectors?

**Model answer:** Two ideas combined. **IVF** k-means-partitions the space into `nlist` Voronoi cells; at query time you only search the `nprobe` cells nearest the query, skipping ~99% of vectors. **PQ** compresses each vector: split it into `m` sub-vectors, learn a 256-entry codebook per sub-space, and store each vector as `m` 1-byte codes — e.g., 768 floats (3072 B) → 96 bytes, a 32× reduction. At query time, asymmetric distance computation precomputes a lookup table so each candidate's approximate distance is `m` table adds. For 1B × 768: raw float32 = 3.07 TB (won't fit), PQ = 96 GB (fits). IVF avoids scanning everything; PQ makes what you do scan tiny. Add a rerank of the top candidates with exact float vectors to recover recall.

**Follow-ups:** *Why asymmetric (don't quantize the query)?* (Higher accuracy — query stays full precision.) *Downside of PQ?* (Lossy → lower recall; needs training; retrain on drift.) *How to recover recall?* (Rerank top-N with exact distances.)

### Q4: Cosine vs dot product vs L2 — which and why for text?

**Model answer:** Cosine is the text default: it compares direction (meaning), ignoring magnitude (which correlates with length, not meaning). But if I L2-normalize the vectors — which most text embedding models do — then dot product equals cosine (since ‖a‖=‖b‖=1 ⇒ a·b = cos), and L2 produces the *same ranking* (‖a−b‖² = 2 − 2cos). So in practice I normalize once and configure the index for inner product, getting exact cosine ranking with less per-query compute. L2 is the FAISS default and fine on normalized vectors; un-normalized, cosine and L2 differ because L2 is magnitude-sensitive.

**Follow-ups:** *When would dot product (not cosine) be right?* (Recsys where magnitude encodes popularity/confidence — MIPS.) *Prove cosine=dot for unit vectors.* (a·b = ‖a‖‖b‖cosθ = cosθ.)

### Q5: How do you choose chunk size, and what's the trade-off?

**Model answer:** Chunks are what you embed and retrieve, so size controls precision vs. context. Too small (e.g., 64 tokens): high precision but the chunk lacks enough context to answer ("Click Settings, then Security" without the rest of the steps). Too large (e.g., 2000 tokens): the relevant sentence is diluted by irrelevant text — the averaged embedding is fuzzy (low precision) and you waste the LLM's context window. The sweet spot is 256–512 tokens with 10–20% overlap so a sentence split at a boundary still appears whole somewhere. For structured docs I split on headers; for high precision I use parent-child (retrieve a small child, feed the larger parent to the LLM).

**Follow-ups:** *What's overlap for?* (Avoid cutting an answer across a boundary.) *Parent-child?* (Embed small chunks for precise retrieval, but pass the surrounding parent to the LLM for context.)

### Q6: Walk me through filtered search. What's the gotcha?

**Model answer:** The gotcha is **post-filtering**: if you ANN-retrieve top-k and *then* drop non-matching results, a selective filter (say 1% of vectors match) can leave you with zero results even though good matches exist — a correctness bug — and over-fetching to compensate is slow. Naive **pre-filtering** breaks HNSW because the graph navigates through nodes that may be filtered out, collapsing recall. The production answer is **filtered ANN**: the predicate is fused into graph traversal (Qdrant, Weaviate, Milvus do this), or you partition by the filter key (one index per tenant), or — for highly selective filters — fall back to exact brute force over the tiny matching subset. In ACL-aware enterprise RAG this isn't just performance; it's a security boundary.

**Follow-ups:** *How does partitioning help?* (Each partition is its own small index, queried directly — no recall loss.) *When is brute force fine?* (When the filter leaves few candidates.)

### Q7: Why hybrid search, and how do you combine the two rankings?

**Model answer:** Dense embeddings excel at paraphrase/concept matching but miss exact strings — SKUs, error codes, rare proper nouns the model never saw. BM25 nails those exact terms but misses synonyms. Neither alone is best, so I run both and fuse with **Reciprocal Rank Fusion**: score each doc by Σ 1/(k+rank) across the two lists (k≈60). RRF uses only ranks, so it sidesteps the problem that BM25 scores and cosine scores aren't comparable. A doc both methods rank highly wins; the method works without score normalization or tuning.

**Follow-ups:** *Why rank-based not score-based fusion?* (Scores live on incomparable scales; ranks are robust.) *What does k control?* (Higher k flattens the contribution of top ranks — smoother fusion.)

### Q8: Explain retrieve-then-rerank. Why two stages?

**Model answer:** Retrieval uses a bi-encoder — query and documents embedded independently — which is fast and scalable (embed the corpus once offline, ANN at query time) but coarse, since the query and document never attend to each other. A cross-encoder feeds `[query, doc]` together through full attention and outputs a precise relevance score, but it needs one forward pass per document — impossible over 100M docs. So: stage 1 retrieves top-30–50 cheaply with the bi-encoder ANN; stage 2 reranks just those 30–50 with the cross-encoder and keeps the top 3–5. You get the cross-encoder's accuracy at the bi-encoder's scale. Reranking ~50 docs adds ~40 ms but materially improves answer quality.

**Follow-ups:** *Why not cross-encode everything?* (O(N) forward passes — billions of transformer runs.) *Commercial options?* (Cohere/Voyage/Jina rerankers.)

### Q9: You upgrade your embedding model. What happens operationally?

**Model answer:** A new model produces a different vector space — old and new vectors aren't comparable — so you must **re-embed the entire corpus and rebuild the index**; you can't mix or incrementally migrate. I'd do blue/green: stand up a new (green) index, re-embed everything into it, validate recall@10 on the golden set against the live (blue) index, dual-write new ingests during transition, then cut over and decommission blue. Budget roughly 28 GPU-hours per 100M chunks plus 2× storage during overlap. This re-embed cost is the single biggest hidden operational risk of a vector system.

**Follow-ups:** *Can you avoid re-embedding?* (No — geometry changes. Matryoshka embeddings let you truncate dims without re-embedding, but a *new model* still requires it.) *How do you validate the new index?* (Golden-set recall must meet or beat the old.)

### Q10: How do you measure whether retrieval is good?

**Model answer:** Build a golden set of (query, relevant_doc_ids) — from expert labels, click logs, or LLM-generated questions per chunk. Then track recall@k (did we find the relevant docs?), precision@k (are top-k clean?), MRR (how high is the first hit?), and nDCG@k (graded ranking quality). Crucially, separate **ANN recall** (index returns the true nearest vectors, ground-truthed by brute force) from **retrieval recall** (we return the truly relevant documents, ground-truthed by labels): a bad embedding model gives perfect ANN recall but poor retrieval recall. Gate every index/model/chunking change on offline metrics, then A/B test online for click-through and answer success.

**Follow-ups:** *Define nDCG.* (DCG = Σ rel_i/log2(i+1), normalized by ideal DCG; rewards ranking the best doc first.) *Recall 0.99 but bad answers — why?* (Embedding model or chunking, not the index.)

### Q11: Design semantic search over 100M documents with <100 ms p95.

**Model answer:** 100M docs × ~5 chunks ≈ 500M vectors. At d=768 float32 that's 1.5 TB raw — too big for one box, so memory drives the design. Use bge-base (768-dim, self-hosted, normalized → inner product), recursive 512/64-token chunks with metadata. Index: IVF-PQ (nlist≈90K, nprobe=64, m=96 8-bit codes → ~50 GB codes) plus a rerank of top-200 against exact float vectors on SSD. Shard by hash into 8 shards (~62M each), 3 replicas; scatter-gather and merge. Add BM25, fuse with RRF, then cross-encoder rerank to top-5. Budget: ~5 ms query embed + ~25 ms ANN + ~15 ms BM25 (parallel) + ~10 ms SSD rerank + ~40 ms cross-encoder ≈ 80 ms p95, recall@10 ≈ 0.96, ~150 GB RAM (3× replicated). If memory weren't constrained I'd use HNSW (M=32) for ~0.97 recall and skip the rerank, at ~1.75 TB RAM.

**Follow-ups:** *Why IVF-PQ over HNSW here?* (35× memory savings; HNSW = 1.75 TB.) *How do filters/freshness work?* (Tenant partition + filtered IVF; hot HNSW index for recent inserts merged with cold IVF-PQ.)

### Q12: How do deletes work in a vector index?

**Model answer:** Deletes are the hard operation. HNSW graphs can't cleanly remove a node without orphaning neighbors' links, so the standard approach is a **tombstone**: mark the vector deleted, leave it in the graph, and filter it out of query results. Tombstones accumulate — wasting memory and degrading recall because the graph still routes through dead nodes — so when the tombstone ratio passes ~20–30% you **rebuild** the index from live vectors (often as a shadow index, then swap), analogous to LSM-tree compaction. IVF handles it more gracefully (drop the id from a cell's posting list), though churn eventually unbalances cells and triggers a retrain.

**Follow-ups:** *Why not remove the HNSW node immediately?* (Breaks graph navigability.) *How does this resemble databases?* (Tombstones + compaction = LSM-tree; MVCC dead tuples + VACUUM.)

---

## Senior-Level Discussion Points

### Memory is usually the binding constraint, not CPU
At scale, the question "will the index fit in RAM?" dictates the architecture. HNSW stores full vectors (~3.5 KB/vec at d=768) → great recall, but 100M = 358 GB and 1B = 3.5 TB. PQ trades recall for a 32× memory cut. The senior move is to start from the raw-size estimate (N × d × 4 B) and let it choose between HNSW (memory available) and IVF-PQ (+ rerank) (memory bound). Disk-based ANN (DiskANN, Milvus) pushes vectors to NVMe with a small in-RAM graph for even larger scale at higher latency.

### Two-stage retrieval is universal
Cheap-recall then expensive-precision appears everywhere: ANN retrieve → cross-encoder rerank; IVF-PQ approx → exact float rerank; candidate generation → heavy ranker (ads/recs). Always retrieve more than you show. The cost asymmetry (cheap stage over millions, expensive stage over dozens) is the whole point.

### Embedding quality dominates index quality
Teams obsess over ef_search while their embedding model is the actual bottleneck. A perfect index over bad vectors returns the wrong neighbors faithfully. Diagnose by separating ANN recall (vs brute force) from retrieval recall (vs golden labels). Often the highest-ROI move is fine-tuning the embedding model on in-domain (query, doc) pairs, not tuning the index.

### Hybrid + rerank beats bigger models
Before reaching for a 3072-dim model or a 7B embedder, add BM25 + RRF + a cross-encoder reranker. Hybrid fixes the exact-term blind spot of dense vectors; reranking fixes ordering. This stack usually beats a larger single bi-encoder at lower cost.

### Filtering correctness is a security boundary
In multi-tenant / ACL systems, "retrieve only what this user can see" is not a perf nicety — leaking a retrieved chunk is a data breach. Post-filtering can both miss results (correctness) and, if implemented sloppily, leak. Use filtered-ANN or partition by tenant, and treat the filter as part of the authorization path.

### The re-embed treadmill
Every embedding-model upgrade forces a full corpus re-embed + index rebuild. This caps how often you can chase model improvements and argues for (a) self-hosting embeddings to avoid per-call costs at re-embed time, (b) Matryoshka models to get a dim knob without re-embedding, and (c) blue/green pipelines so upgrades are routine, not heroic.

### Freshness vs rebuild cost
Real-time use cases (chat memory) need second-level freshness; doc search tolerates hours. The hot/cold split (small frequently-rebuilt index + large nightly-rebuilt index, queried together) is the standard answer. State your freshness SLA explicitly; it changes the design.

### Quantization recall recovery
PQ's recall hit is recoverable: retrieve a larger candidate set by PQ approx distance, then re-score with exact float vectors (kept on SSD). This decouples "fit in RAM" (PQ codes) from "final ranking accuracy" (exact rerank) — a clean way to break the recall/memory tension.

---

## Typical Mistakes Candidates Make

1. **Saying "just use cosine similarity" with no mention of normalization or the dot-product equivalence.** The signal is knowing that normalized vectors make cosine = dot, so you configure the index for inner product.

2. **Proposing exact kNN or a k-d tree at scale.** Shows no awareness of O(N·d) cost or the curse of dimensionality. Name ANN immediately for N > ~1M.

3. **Treating filtering as a post-step.** Post-filtering causes the empty-results correctness bug and, in ACL systems, security risk. Always raise filtered-ANN or partitioning.

4. **Confusing bi-encoder and cross-encoder.** Bi = independent embeddings for scalable retrieval; cross = joint attention for accurate reranking. Mixing them up reveals shallow RAG understanding.

5. **Ignoring chunking.** Retrieval quality is dominated by chunk size/overlap/strategy. "I'll embed the documents" without chunking is a red flag.

6. **Forgetting the re-embed cost of model upgrades.** Many candidates think you can swap embedding models freely. You can't — it's a full corpus rebuild.

7. **Conflating ANN recall with retrieval recall.** A great index over a bad embedding model still returns wrong results. Separate the two when diagnosing.

8. **"HNSW always" with no memory math.** HNSW is the default, but at billions of vectors its memory (full vectors + graph) is prohibitive; that's when IVF-PQ wins. Quote the numbers.

9. **Skipping hybrid search.** Pure dense search misses exact terms (SKUs, error codes). Mention BM25 + RRF.

10. **No golden set / no evaluation plan.** "I'd tune ef_search" without saying *against what metric on what data* is hand-waving. Recall@k on a golden set gates everything.

11. **Claiming PQ is lossless.** PQ is lossy compression; it reduces recall. The fix is reranking with exact vectors, not pretending there's no cost.

12. **Forgetting deletes are hard.** Saying "just delete the vector" ignores HNSW's tombstone-and-rebuild reality.

---

## How This Connects to Other Topics

| Topic | Connection |
|---|---|
| **LLM Applications / RAG** | Vector search is the retrieval engine of RAG; chunking, hybrid, rerank all live here |
| **Databases (08)** | ANN index = the B-tree analog for semantic proximity; tombstones + rebuild mirror LSM compaction + VACUUM; filtered search ≈ index + predicate; sharding/replication are identical concepts |
| **Distributed Systems** | Sharding (scatter-gather vs routed), replication, consistency/freshness, quorum reads for vector shards |
| **Machine Learning** | Embedding models, contrastive/InfoNCE training, bi/cross-encoders, two-tower retrieval, CLIP/multimodal |
| **Data Structures & Algorithms** | Skip lists (HNSW intuition), k-means (IVF/PQ), graphs (NSW), priority queues (candidate sets), k-d trees and why they fail in high-d |
| **System Design** | Retrieval service design, latency budgets, capacity estimation, hot/cold indexes, caching |
| **Information Retrieval** | BM25/TF-IDF, inverted indexes, RRF, nDCG/MRR/precision/recall, evaluation methodology |
| **Performance Engineering** | SIMD distance kernels, memory bandwidth limits, quantization, GPU vs CPU ANN, mmap |
| **Security / Privacy** | ACL-aware filtered retrieval as an authorization boundary; on-device embeddings for privacy |

---

## FAANG Interview Tips

1. **Lead with the size estimate.** "N vectors × d dims × 4 bytes" is the number that drives every architectural choice. Compute it out loud first.

2. **Always name the recall/latency/memory triangle** and which corner you're optimizing, then name the knob (`ef_search` / `nprobe`) you'd tune against a recall@k target.

3. **Default to HNSW, switch to IVF-PQ when memory-bound.** Justify with the memory math (358 GB vs 96 GB), don't just name-drop.

4. **Never say "filter the results."** Say "filtered-ANN or partition by the filter key; exact brute force for selective filters" — and flag the post-filter correctness/security bug.

5. **Propose hybrid + rerank by default.** Dense + BM25 fused with RRF, then a cross-encoder. It beats a bigger model cheaper.

6. **Use the same embedding model for ingest and query**, normalized, inner-product metric. State the cosine=dot equivalence.

7. **Bring up the re-embed cost** whenever model choice or upgrades come up — it's the senior signal.

8. **Separate ANN recall from retrieval recall** when discussing evaluation; tie everything to a golden set.

9. **For Google, mention ScaNN/anisotropic quantization; for Meta, FAISS and two-tower; for Amazon, OpenSearch kNN and cost.** Company-specific knowledge reads as systems maturity.

10. **State trade-offs explicitly.** "PQ saves 32× memory but loses recall; I recover it by reranking the top-200 with exact float vectors on SSD." Quantified trade-offs win.

---

## Revision Cheat Sheet

### 10-Minute Summary

**The problem:** find nearest vectors by *meaning*. Exact kNN is O(N·d) (seconds at 100M); k-d trees die to the curse of dimensionality. So use **ANN** — ~95–99% recall for 100–1000× speedup.

**Embeddings:** dense learned vectors where geometric closeness = semantic similarity. Trained contrastively (InfoNCE, in-batch negatives, SimCSE). Bi-encoder = independent embeddings (scalable retrieval); cross-encoder = joint attention (accurate rerank). Dims 384/768/1536/3072 trade quality vs memory (linear). Normalize → cosine = dot. Model upgrade = full re-embed + rebuild.

**Metrics:** cosine for text (direction = meaning); normalized ⇒ cosine = dot = (monotone) L2 — same neighbors. Pick inner product on normalized vectors.

**Indexes:**
- **HNSW** — hierarchical small-world graph; ~O(log N); knobs M / ef_construction / ef_search; high recall, high memory (full vectors + graph). **Default.**
- **IVF** — k-means cells; probe `nprobe` nearest cells; needs training.
- **PQ** — split into m sub-vectors, codebooks, m-byte codes; 32× memory cut; lossy; ADC lookup.
- **IVF-PQ** — billion-scale workhorse (FAISS).
- **LSH** (hashing), **Annoy** (mmap trees, immutable), **ScaNN** (anisotropic, Google, fastest MIPS).

**Triangle:** Recall / Latency / Memory — pick a point; tune via ef_search/nprobe; rerank to cheat.

**RAG pipeline:** chunk (512/64 tokens, recursive) → embed → upsert → retrieve top-k → metadata filter (filtered-ANN, not post-filter) → hybrid (dense + BM25, fuse with RRF = Σ1/(60+rank)) → cross-encoder rerank → top 3–5 → LLM.

**Ops:** inserts incremental (~query cost); deletes = tombstone + rebuild; shard (hash scatter-gather vs cluster-routed) + replicate; re-embed on model change (blue/green); freshness via hot/cold split.

**Eval:** golden set; recall@k, precision@k, MRR, nDCG; separate ANN recall (vs brute force) from retrieval recall (vs labels); offline-gate, online A/B.

### Key Numbers to Know

- Exact kNN: O(N·d). 100M × 768 ≈ 77B ops ≈ seconds/query.
- HNSW memory: ~3.5 KB/vector (d=768, M=32) → 100M ≈ 358 GB, 1B ≈ 3.5 TB.
- PQ: 768 floats (3072 B) → 96 bytes = 32× cut. 1B × 768: 3.07 TB float32 → 96 GB PQ.
- IVF: `nlist ≈ sqrt(N)`–`4·sqrt(N)`; nprobe = recall knob.
- Chunks: 256–512 tokens, 10–20% overlap.
- RRF k ≈ 60.
- Re-embed: ~28 GPU-hours / 100M chunks.
- Typical recall targets: 0.90 (web) to 0.99 (medical/legal).
- Dims: 384 / 768 / 1024 / 1536 / 3072; memory linear in d.

### Most Important Concepts for Interviews

| Rank | Concept | Why |
|---|---|---|
| 1 | Why exact kNN / k-d trees fail (curse of dimensionality) | Justifies ANN's existence |
| 2 | HNSW mechanism + M/ef params + memory | The default index; asked constantly |
| 3 | IVF-PQ + the memory math | Billion-scale; quantization |
| 4 | Recall/latency/memory triangle + tuning knobs | The core trade-off |
| 5 | Cosine vs dot vs L2 + normalization equivalence | Distance fundamentals |
| 6 | Chunking size/overlap trade-off | Dominates RAG quality |
| 7 | Hybrid (dense + BM25) + RRF | Beats dense-only, cheap |
| 8 | Retrieve → rerank (bi vs cross encoder) | Two-stage architecture |
| 9 | Filtered search pre/post-filter gotcha | Correctness + security |
| 10 | Re-embed cost on model change | Senior operational signal |
| 11 | Evaluation: recall@k/nDCG, golden set, ANN vs retrieval recall | How you know it works |
| 12 | Sharding + tombstone deletes | Scaling/ops |

### Cheat-Sheet Summary Table

| Question | Quick Answer |
|---|---|
| Exact kNN cost? | O(N·d) — seconds at 100M; use ANN |
| Why not k-d tree? | Curse of dimensionality — pruning fails > ~20 dims |
| Default ANN index? | HNSW |
| Billion-scale, RAM-bound? | IVF-PQ + rerank |
| Query-time recall knob? | HNSW `ef_search`, IVF `nprobe` |
| Text distance metric? | Cosine; normalize → use inner product |
| Cosine = dot when? | Unit-normalized vectors |
| PQ memory cut? | ~32× (768 floats → 96 bytes) |
| Chunk size? | 256–512 tokens, 10–20% overlap |
| Combine dense + BM25? | RRF: Σ 1/(60 + rank) |
| Rerank model type? | Cross-encoder (joint attention) |
| Filter correctly? | Filtered-ANN or partition; never naive post-filter |
| Delete from HNSW? | Tombstone + periodic rebuild |
| Model upgrade? | Full re-embed + rebuild (blue/green) |
| Retrieval metric? | Recall@k, nDCG, MRR on a golden set |
| ANN recall vs retrieval recall? | Index correctness vs system correctness — separate them |
| Spotify's library? | Annoy (mmap, immutable) |
| Meta's library? | FAISS |
| Google's library? | ScaNN (anisotropic quantization) |

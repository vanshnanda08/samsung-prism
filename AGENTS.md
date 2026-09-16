# AGENTS.md — Project Context for AI Assistants

> **Read this file completely before writing any code for this repository.**
> It is the single source of truth for what this project is, what is in scope,
> and what must never be done. If a request conflicts with this file, say so
> rather than silently proceeding.

---

## 1. What this project is

**Bifrost** is a CPU-only code retrieval engine built for **Theme 01 — Agentic Code
Intelligence** of the Samsung PRISM Generative AI Hackathon, 3rd Edition (2026–27).

**The task:** given a natural-language query and a library of code snippets, return a
**ranking of code snippets by relevance**. That is the whole task.

**The central insight driving the design:** on the evaluation dataset, BM25 keyword
search scores **0.95 NDCG@10 out of 100**. That near-zero score means natural-language
queries and their matching code share almost no surface vocabulary. This is a
*cross-language semantic asymmetry* problem, not a search problem. Bifrost closes the
gap from **both sides** — enriching the index with generated natural-language
descriptions of what each snippet does, and distilling queries down to their
algorithmic core — so the two meet in the middle.

---

## 2. Hard facts — do not contradict these

| Fact | Value |
|---|---|
| Submission deadline | **25 September 2026, 11:59 PM IST** |
| Required git tag on final commit | `PRISM_GENAI_HACKATHON_Y2026` |
| Screening dataset | `CoIR-Retrieval/apps`, MTEB task `AppsRetrieval` |
| Corpus size | ~8,770 documents (Python) |
| Test queries | ~3,770 (avg ~1,400 words each) |
| Screening metrics | **NDCG@10** and **MRR** |
| Required output artifact | `appsretrieval_results.json`, uploaded as a **GitHub Release asset** |
| Hardware constraint | **Must run on CPU.** Minimal GPU use allowed. |

### Published baselines on this dataset (CoIR paper, ACL 2025)

| Model | NDCG@10 | CPU-viable |
|---|---|---|
| BM25 | 0.95 | yes |
| UniXcoder | 1.36 | yes |
| GTE-Base | 3.24 | yes |
| BGE-Base | 4.05 | yes |
| Contriever | 5.14 | yes |
| BGE-M3 | 7.37 | yes (slow) |
| OpenAI Ada-002 | 8.70 | API only |
| **E5-Base** | **11.52** | **yes — this is the bar to beat** |
| E5-Mistral (7B) | 21.33 | no (GPU) |
| Voyage-Code-002 | 26.52 | API only |

**Target: beat 11.52 convincingly on CPU.** We are not chasing 26.52.

---

## 3. Scope — read this twice

### ✅ IN scope

- Ranking code snippets by relevance to a natural-language query
- Query categorisation and pre-processing
- Code snippet categorisation and pre/post-processing
- Multiple retrieval passes
- Re-indexing across code versions (goal **P1**)
- Retrieval across multiple versions simultaneously (goal **Bonus**)
- A demo UI that shows results and latency

### ❌ OUT of scope — the organisers state this explicitly

> *"Generating an answer for the query, explaining the results or anything to do with
> the generation that takes place after the retrieval is out of scope for this problem
> statement."*

Concretely, **do not build**:

- A chatbot or "chat with your codebase" interface
- Any feature that answers the user's question in prose
- Code generation, code explanation, or automated fixes
- An LLM agent loop that reads files and reasons at query time

**LLMs are used in this project for exactly two things, both offline or cheap:**

1. **Offline index enrichment** (doc2query) — generating a natural-language description
   of what each code snippet does, at index build time.
2. **Query distillation** — compressing a long query to its algorithmic core.

An LLM must never appear in the ranking hot path at query time.

---

## 4. The two front doors

The source material is internally inconsistent, and the design accounts for it.

| | Path A — the gate | Path B — the demo |
|---|---|---|
| Source | `theme1_guidelines.pdf` | Main hackathon deck |
| Language | **Python** | **JavaScript** |
| Data | CoIR `apps` test split | Sample voice-assistant repo |
| Query style | 1,400-word problem statements | *"Where is the Bluetooth-settings deeplink used?"* |
| Decides | Whether we reach hands-on evaluation | How we score at hands-on |

**Design rule:** one engine, two front doors. All language-specific logic goes through
**tree-sitter**, so adding a language is a grammar swap and not a rewrite. Never
hard-code Python-only or JavaScript-only assumptions into the core pipeline.

---

## 5. The three submission goals, in priority order

- **P0 — Retrieval accuracy.** Decides the competitive screening. Highest priority.
- **P1 — Retrieval across versions.** Indexes, caches etc. must rebuild for any
  version or change in reasonable time. Our approach: content-hash each chunk so a
  commit touching 12 files re-embeds ~50 chunks, not 8,770.
- **Bonus — Evolutionary retrieval.** Retrieve across *all* versions at once. The
  stated difficulty is that near-identical versions of the same snippet are hard to
  rank. Our approach: group versions into a *lineage* by canonical AST hash, rank the
  lineage once, then select the best version within it.

**P1 and Bonus are our differentiation.** Teams optimising only the screening metric
have no incentive to build them. Do not deprioritise them to chase a marginal NDCG gain.

---

## 6. Architecture

```
┌──────────── INDEXING (offline, once per version) ────────────┐
│                                                               │
│  source repo ──▶ tree-sitter parse ──▶ AST-aware chunks       │
│                          │                                    │
│                    content hash ──▶ cache hit? skip           │
│                          │                                    │
│                          ▼                                    │
│        enrichment (local LLM via llama.cpp, CPU)              │
│          • doc2query: synthetic NL description                │
│          • structural signature: identifiers, imports,        │
│            control-flow shape                                 │
│                          │                                    │
│                          ▼                                    │
│        3× embed (raw code / synthetic NL / signature)         │
│                          │                                    │
│          ┌───────────────┴───────────────┐                    │
│          ▼                               ▼                    │
│   hnswlib vector index          bm25s identifier index        │
│          └───────────────┬───────────────┘                    │
│                          ▼                                    │
│            DuckDB chunk store (hash → chunk,                  │
│                    version lineage table)                     │
└───────────────────────────────────────────────────────────────┘

┌──────────────── QUERY (online, CPU, no LLM) ─────────────────┐
│                                                               │
│  query ──▶ classifier ──┬──▶ [structural] → call graph        │
│                         └──▶ [semantic]                       │
│                                    │                          │
│              distillation (algorithmic core)                  │
│              + HyDE pseudo-code sketch                         │
│                                    │                          │
│              multi-chunk embed, max-sim pooling               │
│                (queries exceed encoder context)               │
│                                    ▼                          │
│        multi-view retrieval ──▶ RRF fusion ──▶ rerank         │
│                                    (ONNX int8 cross-encoder)  │
│                                    ▼                          │
│           ranked snippets + file:line + latency telemetry     │
└───────────────────────────────────────────────────────────────┘
```

### Why each component exists

Every component must earn a row in the ablation table. If a component cannot be shown
to improve NDCG@10 or MRR, it gets removed before submission.

| Component | Why it is there |
|---|---|
| doc2query index enrichment | Bridges the NL↔code gap from the index side. Our primary differentiator on P0. |
| Query distillation | Strips ~1,400 words of narrative down to the algorithmic core |
| HyDE pseudo-code | Enables code-to-code similarity in addition to NL-to-code |
| Multi-view + RRF | Fuses retrievers with complementary failure modes |
| Cross-encoder rerank | Fixes bi-encoder ordering within the top-k |
| Multi-chunk max-sim | Queries exceed the encoder's context window |
| Content-hash chunk store | Makes P1 (fast re-index) and Bonus (lineage) nearly free |

---

## 7. Technology decisions

| Layer | Choice |
|---|---|
| Language | Python 3.11 |
| API | FastAPI + uvicorn |
| Embedders | `intfloat/e5-base-v2`, plus a code-specialised encoder (`jinaai/jina-embeddings-v2-base-code`) |
| Reranker | `BAAI/bge-reranker-base` or `cross-encoder/ms-marco-MiniLM-L-6-v2`, exported to **ONNX int8** |
| Offline LLM | `Qwen2.5-0.5B-Instruct` GGUF via `llama.cpp` — **offline only** |
| Vector index | `hnswlib` (or FAISS) |
| Sparse index | `bm25s` |
| Chunk store | DuckDB |
| Parsing | `tree-sitter` with Python and JavaScript grammars |
| Evaluation | `mteb` |
| Frontend | Next.js + TypeScript + Tailwind + shadcn/ui + Monaco |
| Packaging | Docker + docker-compose + Makefile |

### Non-negotiable engineering constraints

1. **CPU only.** No CUDA dependency. No GPU-only model.
2. **No network calls at query time.** No hosted embedding APIs, no API keys. The demo
   must run fully offline.
3. **Pinned dependencies.** `requirements.txt` gets frozen once the environment works.
4. **Reproducible.** `docker compose up` must work on a machine that has never seen
   this project. This is tested on Day 7, not Day 9.
5. **Everything measurable.** Any change to the pipeline must be expressible as a
   config flag and evaluable through the ablation harness.

---

## 8. Repository layout

```
bifrost/
├── AGENTS.md              ← you are here
├── CLAUDE.md              ← pointer to this file
├── README.md              ← human-facing overview and setup
├── AI_DISCLOSURE.md       ← running log, required by the organisers
├── Makefile
├── requirements.txt
├── docs/
│   ├── THEME1_SPEC.md     ← distilled organiser requirements (facts only)
│   └── WORKFLOW.md        ← day-by-day plan and role assignments
└── src/
    ├── bifrost/
    │   ├── chunking/      ← tree-sitter AST-aware chunking
    │   ├── enrichment/    ← doc2query, structural signatures
    │   ├── indexing/      ← content hashing, vector + sparse indexes, lineage
    │   ├── retrieval/     ← multi-view retrieval, RRF, reranking
    │   ├── eval/          ← MTEB wrapper, ablation harness
    │   └── api/           ← FastAPI service
    └── web/               ← Next.js demo UI
```

---

## 9. Rules for AI assistants working in this repo

**Do:**

- Read `docs/THEME1_SPEC.md` before implementing anything that touches evaluation
- Keep every pipeline stage behind a config flag so it can be ablated
- Write CPU-friendly code — batch operations, avoid per-item model calls
- Log latency and indexing cost; the organisers explicitly ask us to report both
- Ask before adding a dependency, especially a heavy one

**Do not:**

- Add any LLM call to the query-time path
- Add a chat interface or answer-generation feature
- Introduce a GPU-only dependency
- Call a hosted API at inference time
- Hard-code assumptions about Python or JavaScript in the core pipeline
- Add authentication, user accounts, or any CRUD feature — they score zero here
- Start frontend work before the retrieval pipeline is measured and frozen

**When logging AI assistance:** every feature built with AI help must be recorded in
`AI_DISCLOSURE.md` with the tool used, the prompt, a summary of the output, and what
was modified. The organisers require this. Log as you go — reconstructing it later
costs an evening we do not have.

---

## 10. Current status

| Item | Status |
|---|---|
| Team registered | ☐ |
| Repo initialised | ☑ |
| Baseline `e5-base-v2` number recorded | ☐ |
| MTEB reranker-interface spike resolved | ☐ |
| Ablation harness working | ☐ |
| Hybrid retrieval + RRF | ☐ |
| Query distillation | ☐ |
| doc2query enrichment | ☐ |
| ONNX int8 reranking | ☐ |
| **Eval config frozen, final JSON generated** | ☐ |
| Content-hash incremental re-indexing | ☐ |
| Demo UI | ☐ |
| Docker verified on clean machine | ☐ |
| Deck, video, disclosure form | ☐ |

**Record your baseline number here as soon as you have it:**

```
e5-base-v2 baseline    NDCG@10: ____    MRR: ____    wall-clock: ____ min
```

The wall-clock figure is the team's iteration budget for the rest of the build. If a
full evaluation pass exceeds ~45 minutes, develop against a subsample and reserve full
runs for checkpoints.

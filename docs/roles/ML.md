# Role: ML

> **Brief for you and your AI assistant.** Read [`../../AGENTS.md`](../../AGENTS.md)
> first for project context, then this file. [`../WORKFLOW.md`](../WORKFLOW.md) has the
> full timeline; this file is only your slice of it.

## Mandate

**You own NDCG@10.** Every point of retrieval accuracy comes from your code.

## You own these files

```
src/samsung_prism/chunking/      tree-sitter AST-aware chunking
src/samsung_prism/enrichment/    doc2query, structural signatures
src/samsung_prism/retrieval/     multi-view retrieval, RRF, reranking
```

## You do not touch

`src/web/`, `Dockerfile`, `requirements.txt`, `src/samsung_prism/eval/`. If you need a
new dependency, ask Systems — they own the lockfile and the CPU-only torch build.

## The two rules that govern everything you write

1. **Every component sits behind a config flag in `configs/default.yaml`.** If it cannot
   be turned off, it cannot be ablated, and if it cannot be ablated it does not ship.
2. **No component enters the pipeline without a measured number.** "This should help" is
   not a reason. Run it through the Lead's ablation harness first.

## The problem you are actually solving

BM25 scores **0.95 NDCG@10 out of 100** on this dataset. That near-zero score means
natural-language queries and matching code share almost no surface vocabulary. This is
a cross-language asymmetry problem, not a search-tuning problem.

Two sides to close it. The **query side** is fixed at runtime and gives you one attempt.
The **index side** is offline, unbounded and cacheable — and the organisers explicitly
invite it (*"Pre/post processing of the code snippets"*). **The index side is your
highest-leverage lever.** Most competing teams will only touch the query.

## Your tasks

### Day 1

- [ ] tree-sitter AST-aware chunking at function/class boundaries, with parent context
- [ ] BM25 over extracted identifiers (`bm25s`)
- [ ] **Language-pluggable from the start.** Python for the benchmark, JavaScript for the
      demo. Never hard-code either — see `../THEME1_SPEC.md` §12 for why.

**Wait for the Lead's spike result before designing around a reranker.**

### Day 2

- [ ] Hybrid dense + sparse retrieval fused with Reciprocal Rank Fusion
- [ ] Query distillation — compress a ~1,400-word problem statement to its algorithmic
      core (constraints, I/O shape, operative verbs)
- [ ] Both behind flags: `retrieval.views`, `retrieval.fusion`, `query.distillation`

**Gate:** above the BM25 baseline by end of day, or stop and re-read the spec.

### Day 3 — the highest-leverage day

- [ ] **doc2query pilot on 500 documents only.** For each code chunk, generate a
      synthetic natural-language description of what it does. Measure the NDCG delta
      before committing hours of CPU to all 8,770.
- [ ] Report the delta to the Lead — **they make the go/no-go call**
- [ ] Multi-chunk query embedding with max-sim pooling (queries exceed encoder context)
- [ ] Evening: if approved, launch full-corpus enrichment overnight

**Fallback if the pilot delta is weak:** template-based structural enrichment —
extracted identifiers, docstrings, imports, control-flow summary. Costs seconds instead
of hours and captures a good share of the benefit. This is a legitimate result, and it
goes in the ablation table either way.

### Day 4

- [ ] Integrate the enriched index
- [ ] Hand the Lead every configuration worth testing
- [ ] 🔒 **After the freeze, you stop changing retrieval.** No exceptions.

### Days 5–6 — Chrono-Index, with the Lead

- [ ] Canonical AST hashing so whitespace and comment changes do not invalidate an
      embedding
- [ ] **Lineage grouping** — the Bonus goal. Near-identical versions of one function
      otherwise fill the top 10 with five copies of the same thing. Group by canonical
      hash, rank the lineage once, then select the best version within it.

### Days 7–9

- [ ] **No new components.** Day 7 is polish only.
- [ ] Day 8: write the **ablation table** — one row per component, showing what each
      contributes to NDCG@10 and MRR. This is the single most persuasive artifact in the
      submission. It turns "we built a pipeline" into "we measured what each part does."
- [ ] Day 8: write your share of the honest limitations list

## Never build

- A chat interface or "chat with your codebase"
- Answer generation, code explanation, or code generation
  (*"Generating an answer for the query... is out of scope"* — organiser guidelines)
- Any LLM call in the query-time path. LLMs are offline-only here: doc2query at index
  build time, and cheap query distillation.
- Anything requiring a GPU or a hosted API

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/ML.md in full before doing anything.
I own the retrieval pipeline. Today is Day N.
Only modify src/samsung_prism/{chunking,enrichment,retrieval}/.
Every component must be toggleable from configs/default.yaml so it can be ablated.
CPU only — no CUDA, no hosted APIs, no LLM calls at query time.
This is retrieval only: never add answer generation or a chat interface.
```

# Role: ML — 2-Day Sprint

> Read [`../../AGENTS.md`](../../AGENTS.md) first, then this file.
> Timeline and cut list: [`../WORKFLOW.md`](../WORKFLOW.md).

## Mandate

**You own NDCG@10.** You have roughly one and a half working days to beat 11.52.

## You own

```
src/samsung_prism/chunking/      tree-sitter AST-aware chunking
src/samsung_prism/enrichment/    template enrichment, doc2query
src/samsung_prism/retrieval/     multi-view retrieval, RRF, reranking
```

## You do not touch

`src/web/`, `Dockerfile`, `requirements.txt`, `eval/`. Need a dependency? Ask Systems.

## The two rules

1. **Every component behind a config flag in `configs/default.yaml`.** If it cannot be
   switched off it cannot be ablated, and the ablation table is now the team's strongest
   asset.
2. **Measure separately.** Each component needs its own row. Bundling two changes into
   one run wastes a measurement you do not have time to repeat.

## The problem, in one paragraph

BM25 scores **0.95 out of 100** here. Natural-language queries and matching code share
almost no surface vocabulary. Two sides to close it: the **query side** is fixed at
runtime and you get one attempt; the **index side** is offline and cacheable, and the
organisers explicitly invite it (*"Pre/post processing of the code snippets"*). The index
side is the higher-leverage lever and most teams will ignore it.

---

## DAY 1 — 17 September

### Morning — the foundation

- [ ] tree-sitter chunking at function/class boundaries, with parent context
- [ ] BM25 over extracted identifiers (`bm25s`)
- [ ] Dense retrieval with the baseline model
- [ ] Fuse with Reciprocal Rank Fusion
- [ ] **Measure on Systems' subsample as soon as it exists**

**Language-pluggable from the start.** Python for the benchmark, JavaScript for the demo.
Never hard-code either — see `../THEME1_SPEC.md` §12.

**Wait for the Lead's spike answer before designing around a reranker.**

### Afternoon — the two levers, measured separately

- [ ] **Query distillation.** Compress the ~1,400-word problem statement to its
      algorithmic core: constraints, input/output shape, operative verbs. Measure.
- [ ] **Template enrichment — this is now your primary corpus-side lever.**
      For each chunk, extract identifiers, docstrings, imports and a control-flow
      summary; index that alongside the raw code. Costs seconds, not hours. Measure.
- [ ] Multi-chunk query embedding with max-sim pooling if time allows — queries exceed
      the encoder's context window, so truncation is silently costing you.

### Evening

- [ ] Hand the Lead every configuration worth testing
- [ ] Set up the doc2query overnight run — synthetic natural-language descriptions for
      all 8,770 documents. **This is a bonus, not the plan.** If it is not finished by
      9 AM it gets killed and template enrichment ships.

---

## DAY 2 — 18 September

### Morning

- [ ] Integrate doc2query output **only if it finished**
- [ ] Support the Lead's final full-set runs
- [ ] 🔒 **Noon: you stop changing retrieval.** No exceptions, no "one more idea."

### Afternoon

- [ ] **Write the ablation table.** One row per component: dense only, +BM25/RRF,
      +distillation, +template enrichment, +rerank. Show the NDCG@10 and MRR each earned.
      This single table is the most persuasive artifact in the submission — it turns
      "we built a pipeline" into "we measured what each part does."
- [ ] Write your share of the limitations list, honestly

---

## Never build

- A chat interface or "chat with your codebase"
- Answer generation, code explanation, code generation
  (*"Generating an answer for the query... is out of scope"* — organiser guidelines)
- Any LLM call in the query-time path. LLMs here are offline only.
- Anything needing a GPU or a hosted API

## Cut from the original plan — do not build these

HyDE pseudo-code generation · multi-model embedding ensembles beyond two views ·
lineage grouping · canonical AST hashing. They were Days 3–6 work. If free hours appear
after exams, lineage grouping is the first thing to add back.

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/ML.md in full before doing anything.
I own the retrieval pipeline. This is a 2-day sprint; today is Day N.
Only modify src/samsung_prism/{chunking,enrichment,retrieval}/.
Every component must be toggleable from configs/default.yaml for ablation.
CPU only — no CUDA, no hosted APIs, no LLM calls at query time.
Retrieval only: never add answer generation or a chat interface.
Prefer the cheapest thing that produces a measurable gain. I do not have
time for anything that takes more than a few hours to build.
```

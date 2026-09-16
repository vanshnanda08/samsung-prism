# Role: Lead

> **Brief for you and your AI assistant.** Read [`../../AGENTS.md`](../../AGENTS.md)
> first for project context, then this file. [`../WORKFLOW.md`](../WORKFLOW.md) has the
> full timeline; this file is only your slice of it.

## Mandate

**You own the number and the calendar.** Nobody else decides when the eval config
freezes or what gets cut.

## You own these files

```
src/samsung_prism/eval/          MTEB harness, ablation harness
configs/                         pipeline configuration
docs/                            spec, workflow, roles
AI_DISCLOSURE.md                 keep it current
```

## You do not touch

`src/web/` (Web owns it), `Dockerfile` / `requirements.txt` (Systems owns them).
Review, don't edit.

## Decisions only you make

| Decision | When | Why it's yours |
|---|---|---|
| Reranker architecture, after the spike | Day 1 | Determines what ML builds for three days |
| **Freeze the eval config** | **Day 4** | After this the submitted number cannot change |
| Cut or keep the structural-query stretch | Day 7 | Only you can see whether Days 5–6 actually finished |
| Feature freeze | Day 7, 6 PM | Somebody has to say no |
| Submit | Day 9, 6 PM | Not 11:59 PM |

## Your tasks

### Day 0 — tonight

- [ ] Register the team (closes 11:59 PM — blocking, everything waits)
- [ ] Email `prism@samsung.com` with the open questions in `../THEME1_SPEC.md` §12
- [ ] Launch the stock `e5-base-v2` baseline; let it run overnight
- [ ] Record the wall-clock time in `../../AGENTS.md` §10

### Day 1 — the spike

**Two hours, hard time-box.** Can a cross-encoder reranking stage be expressed inside
MTEB's `AbsEncoder`?

- [ ] Inspect `AbsEncoder`'s public surface and abstract methods
- [ ] Look for a search- or retriever-level extension point
- [ ] **Record the decision in `../THEME1_SPEC.md` §7 and tell ML immediately**

If the answer is no, the submitted JSON is bi-encoder-only and the reranker becomes a
demo asset plus an ablation row. That is a legitimate outcome, not a failure — but
doc2query enrichment then becomes *the* lever, because it is encode-side, and ML needs
to know that on Day 1 rather than Day 5.

### Day 2 — the ablation harness

- [ ] One config flag in → NDCG@10 and MRR out
- [ ] Results written to a comparable table across runs
- [ ] **Gate:** if the pipeline is not above the BM25 baseline by end of day, stop
      adding components and re-read `../THEME1_SPEC.md`

This is the most valuable thing you build. Every later decision runs through it.

### Day 3

- [ ] Review ML's 500-document doc2query pilot result — **you make the go/no-go call**
      on spending hours of CPU on the full corpus
- [ ] Review Systems' throughput numbers; agree the rerank `k`

### Day 4 — freeze day

- [ ] Run the full ablation matrix
- [ ] Select the winning configuration
- [ ] 🔒 **FREEZE**
- [ ] Generate the final `appsretrieval_results.json`
- [ ] Record the number in `../../AGENTS.md` §10 and tell the whole team

After this the remaining five days carry zero risk to the screening score. This is the
most important gate in the plan.

### Days 5–6 — Chrono-Index, with ML

- [ ] Content-hash chunk store keyed on AST-normalised form
- [ ] Version manifest: `(version, file, span) → chunk_hash`
- [ ] Incremental re-index: diff manifests, embed only new hashes
- [ ] Lineage grouping by canonical AST hash — rank the lineage once, then pick the
      best version inside it

This covers goals **P1** and **Bonus**. It is the differentiation.

### Day 7

- [ ] Stretch call: structural query routing via call graph — **only if Days 5–6
      finished on schedule.** Cut without hesitation otherwise.
- [ ] 🔒 **Feature freeze, 6 PM**

### Day 8

- [ ] The 12-slide PPT (template is in the parent folder), named `CollegeName_TeamName`
- [ ] Assemble ML's ablation table and Systems' metrics into the results slide
- [ ] Write the limitations slide **honestly** — it reads as senior, not weak
- [ ] Complete `../../AI_DISCLOSURE.md`

### Day 9

- [ ] Demo video, under 5:00, recorded not performed, models pre-warmed
- [ ] Run the submission checklist in `../WORKFLOW.md` line by line
- [ ] **Release tag `PRISM_GENAI_HACKATHON_Y2026` on the final commit**
- [ ] `appsretrieval_results.json` uploaded as a **GitHub Release asset**
- [ ] Submit by 6 PM

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/LEAD.md in full before doing anything.
I am the project lead. Today is Day N.
I own: src/samsung_prism/eval/, configs/, docs/.
Do not modify src/web/, Dockerfile, or requirements.txt — other people own those.
This is a retrieval project. Never add answer generation, a chat interface,
or an LLM call in the query-time path.
```

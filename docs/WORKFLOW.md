# Workflow — Build Plan, Roles, and Daily Gates

**Window: 16 – 25 September 2026. Nine days.**

This file is the operational plan. `AGENTS.md` says *what* we are building and why;
this file says *who does what, when, and what must not be started yet.*

---

## Team and roles

| Role | Owns | Primary skill |
|---|---|---|
| **Lead** | Architecture, MTEB harness, ablation harness, the freeze decision | — |
| **ML** | Retrieval pipeline quality — hybrid retrieval, distillation, enrichment | AI/ML |
| **Systems** | CPU performance, ONNX quantisation, Docker, reproducibility, benchmark ops | Hardware/systems |
| **Web** | Demo UI — search view, Monaco, latency HUD, commit slider | Web development |

**Why "Systems" is on the critical path, not the sidelines:** the theme requires the
solution to run on CPU and explicitly asks teams to *"report precision@k, recall,
latency and indexing cost."* Throughput profiling, ONNX int8 export and reproducible
packaging are graded work, not support work.

---

## The governing rules

1. **Measure before you build.** No component enters the pipeline without an ablation
   number showing it helps.
2. **Freeze the eval config on Day 4.** After that the submitted number does not change.
   Everything later is differentiation and presentation.
3. **No frontend before Day 5.** Starting earlier is the standard way this fails.
4. **Feature freeze 6 PM on Day 7.** Not negotiable.
5. **Submit Day 9 by 6 PM**, not 11:59 PM. Leave margin for a form that will not load.

---

## Day 0 — 16 September (tonight)

### Blocking, do first

- [ ] **Register the team.** Closes 11:59 PM. Nothing else matters until this is done.
      `https://forms.gle/NxN6TWXLpcXmTnv66`
- [ ] Email `prism@samsung.com` with the open questions in `docs/THEME1_SPEC.md` §12

### Then

- [ ] Push this repository to GitHub (public)
- [ ] `pip install mteb sentence-transformers`
- [ ] Launch the stock `intfloat/e5-base-v2` baseline through MTEB and let it run
      overnight. Expect 30–60 minutes on CPU.
- [ ] **Record the wall-clock time.** That number is the team's iteration budget.

**Do NOT:** design the pipeline, evaluate model options, write a README, touch the UI.

**Exit criterion:** registered, and one real number on the board.

---

## Day 1 — 17 September

### The critical spike — Lead, 2 hours, hard time-box

Can a cross-encoder reranking stage be expressed inside MTEB's `AbsEncoder`?

This one answer determines the architecture. Discovering it on Day 7 would cost the
week. If the answer is no, the submitted JSON reflects the bi-encoder pipeline and the
reranker becomes a demo asset and an ablation row — that is a legitimate outcome, not a
failure, but it must be known now.

- [ ] Spike resolved, decision recorded in `docs/THEME1_SPEC.md` §7

### Parallel work

| Who | Task |
|---|---|
| **ML** | tree-sitter AST-aware chunking; BM25 (`bm25s`) over identifiers |
| **Systems** | Full-eval wall-clock profiling. If >45 min, build the subsample dev set now. Docker skeleton, `requirements.txt` |
| **Web** | Nothing on the frontend. Read `docs/THEME1_SPEC.md`, sketch the UI on paper, help run evals |

**Exit criterion:** spike resolved; iteration budget known.

---

## Day 2 — 18 September

- [ ] **Lead:** ablation harness — change one config flag, get NDCG@10 and MRR back
- [ ] **ML:** hybrid dense + sparse retrieval fused with RRF; query distillation
      (1,400 words → algorithmic core)
- [ ] **Systems:** subsample dev set validated against full-run results

The ablation harness is the most valuable tool in the project. Every later decision runs
through it. Build it properly.

**Gate:** if the pipeline is not above the BM25 baseline by end of day, stop adding
components and re-read the guidelines.

---

## Day 3 — 19 September

- [ ] **ML:** doc2query pilot on **500 documents only**. Measure the NDCG delta before
      committing hours of CPU to all 8,770. If the delta is weak, fall back to
      template-based structural enrichment — identifiers, docstrings, imports,
      control-flow summary — which costs seconds instead of hours.
- [ ] **ML:** multi-chunk query embedding with max-sim pooling
- [ ] **Systems:** ONNX int8 export of the reranker; measure pairs/second; find the `k`
      at which reranking stops paying for itself
- [ ] **Evening:** launch full-corpus doc2query enrichment overnight

**Do NOT:** start the frontend.

---

## Day 4 — 20 September

- [ ] Integrate the enriched index; run the full ablation matrix
- [ ] Select the best configuration
- [ ] **FREEZE THE EVAL CONFIG**
- [ ] Generate the final `appsretrieval_results.json`
- [ ] Record the number in `AGENTS.md` §10

**Exit criterion: the submitted number exists.** Everything after this is
differentiation and presentation. This is the most important gate in the plan — it means
the remaining five days carry no risk to the screening score.

---

## Days 5–6 — 21–22 September

### Chrono-Index (Lead + ML) — this is the differentiation

- [ ] Content-hash chunk store keyed on AST-normalised form, so whitespace and comment
      changes do not invalidate an embedding
- [ ] Version manifest: `(version, file, span) → chunk_hash`
- [ ] Incremental re-index: diff manifests, embed only new hashes
- [ ] Lineage grouping by canonical AST hash; rank each lineage once, then select the
      best version within it

This covers goal **P1** and the **Bonus**. Teams optimising only the screening metric
will not build it.

### Frontend (Web) — start now

- [ ] Next.js scaffold, search view, ranked results with file:line
- [ ] Monaco viewer with surrounding function context
- [ ] Latency HUD
- [ ] Commit slider with a live "re-embedded N of M chunks in T seconds" counter
- [ ] Baseline comparison pane — same query under stock `e5-base` beside Bifrost

---

## Day 7 — 23 September

- [ ] Frontend polish
- [ ] **Stretch, only if Days 5–6 finished on schedule:** structural query routing via
      call graph — the *"which files call X before Y?"* capability from the deck.
      Cut without hesitation if the schedule slipped.
- [ ] **`docker compose up` on a machine that has never seen this project.** A fresh
      container or a teammate's laptop. Fix whatever breaks.

**🔒 FEATURE FREEZE — 6 PM. No new code after this point.**

---

## Day 8 — 24 September

Writing day. No code.

- [ ] README with genuinely reproducible setup instructions
- [ ] Architecture diagram for the PPT
- [ ] **Ablation table** — what each component contributes
- [ ] Metrics report: NDCG@10, MRR, precision@k, recall, latency, indexing cost
- [ ] **Known limitations, written honestly.** The template has a slide for this and
      honesty reads as senior.
- [ ] `AI_DISCLOSURE.md` completed per feature
- [ ] 12-slide PPT using the supplied template, named `CollegeName_TeamName`
- [ ] Rehearse the demo against a stopwatch

**If something is broken and not load-bearing, document it as a limitation rather than
fixing it.**

---

## Day 9 — 25 September

### Morning

- [ ] Clean-machine Docker verification, one final time
- [ ] Record the demo video — multiple takes, models pre-warmed, **under 5:00**
- [ ] Upload to YouTube/Drive and **verify the link from a logged-out browser**

### Afternoon — submission checklist

- [ ] `appsretrieval_results.json` uploaded as a **GitHub Release asset**
- [ ] Release tagged **exactly** `PRISM_GENAI_HACKATHON_Y2026` on the final commit
- [ ] PPT, video link and all documentation **present inside the tagged commit**
- [ ] README verified by someone who did not write it
- [ ] Docker builds and runs on a clean machine
- [ ] PPT filename follows `CollegeName_TeamName`
- [ ] AI Usage Disclosure form completed and signed
- [ ] Google Form submitted

**Submit by 6 PM.**

**Do NOT:** touch the code, re-run the evaluation, or improve one more thing.

---

## The 5-minute demo script

| Time | Content |
|---|---|
| 0:00–0:35 | The problem, and the number. *"BM25 gets 0.95 NDCG@10 on this dataset. The best CPU-runnable published model gets 11.52. Here is why, and what we did about it."* |
| 0:35–1:35 | Live query against the JS repo. Results in *X* ms with file:line. Click through to Monaco. |
| 1:35–2:25 | Side-by-side against the `e5-base` baseline on a hard query with zero lexical overlap. |
| 2:25–3:25 | **The commit slider.** Switch version → *"re-embedded 47 of 8,770 chunks in 1.9 s"* → same query, results shift. Then the cross-version lineage view. *(P1 + Bonus, on screen, in sixty seconds.)* |
| 3:25–4:10 | Structural query answered from the call graph, not the vector index. |
| 4:10–5:00 | Results: NDCG@10 and MRR vs published baselines, the ablation table, indexing cost, CPU-only. End on limitations. |

**Record it. Do not perform it live.** Pre-warm all models. Show cold-start separately
and honestly rather than hiding it.

---

## Post-submission — 26 September to 15 October

If shortlisted on 9 October, the final demo round on 15 October includes *"Q&A on design
decisions and trade-offs."* Prepare answers to:

- Why these embedding models and not others?
- Why RRF rather than learned fusion weights?
- What does the reranker cost in latency, and what does it buy?
- How does re-indexing scale to a 100,000-file repository?
- What does the system do badly, and why?
- What would the first three months of worklet work look like?

Being able to say *"we tried X, it cost Y, here is the number"* is worth more than any
slide.

---

## Risk register

| Risk | Mitigation |
|---|---|
| MTEB cannot express reranking | Submit bi-encoder JSON; reranker in demo + ablation table |
| Cross-encoder too slow on CPU | Reduce `k` 50→20→10; ONNX int8; truncate; report the trade-off as a finding |
| doc2query quality poor from a 0.5B model | Template-based structural enrichment, no LLM |
| Full eval too slow to iterate | Subsample dev set; full runs at checkpoints only |
| Organiser JS repo never arrives | Public open-source JS voice-assistant repo, declared in README |
| Docker fails on a clean machine | Tested Day 7, not Day 9 |
| Documentation crunch on Days 8–9 | Add a 4th member who owns deck, video and disclosure form |

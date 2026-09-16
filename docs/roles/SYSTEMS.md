# Role: Systems

> **Brief for you and your AI assistant.** Read [`../../AGENTS.md`](../../AGENTS.md)
> first for project context, then this file. [`../WORKFLOW.md`](../WORKFLOW.md) has the
> full timeline; this file is only your slice of it.

## Mandate

**You own speed and reproducibility.** The system must be fast on CPU and must run on a
machine that has never seen this project.

## This role is graded work, not support work

The theme requires the solution to run on CPU and explicitly asks teams to *"report
precision@k, recall, **latency and indexing cost**."* Two of those four numbers are
yours. The submission also requires *"README with reproducible setup instructions,
Docker files"* — and non-compliance is listed as grounds for disqualification.

Your output lands directly on the results slide.

## You own these files

```
Dockerfile, docker-compose.yml       packaging
requirements.txt, requirements.lock.txt   pinned dependencies
Makefile                             build and run targets
benchmarks/                          profiling scripts and results
```

Plus the ONNX export and quantisation of the reranker.

## You do not touch

`src/samsung_prism/{chunking,enrichment,retrieval}/` (ML owns them), `src/web/` (Web
owns it). You profile them; you don't rewrite them.

## Your tasks

### Day 1 — the number that shapes the week

- [ ] **Profile the full evaluation wall-clock on your hardware.** 8,770 documents plus
      3,770 queries averaging ~1,400 words, on CPU.
- [ ] Record it in `../../AGENTS.md` §10

**If a full pass exceeds ~45 minutes, build a stratified subsample dev set immediately.**
The team cannot iterate twenty times against a two-hour loop, and twenty iterations is
how this benchmark gets won. This is the highest-value thing you do all week.

- [ ] Docker skeleton, `requirements.txt`, CPU-only torch wheel
      (`pip install torch --index-url https://download.pytorch.org/whl/cpu` — installing
      the default wheel pulls ~2 GB of CUDA libraries you cannot use)

### Day 2

- [ ] **Validate that the subsample correlates with the full run.** A dev set that ranks
      configurations differently from the real thing is worse than no dev set. Run both
      on two or three configs and check the ordering matches.
- [ ] `make setup` works from a clean checkout

### Day 3

- [ ] Export the cross-encoder reranker to **ONNX, int8 quantised**
- [ ] Measure throughput in pairs/second, batched
- [ ] **Find the `k` at which reranking stops paying for itself.** Report latency at
      k = 10, 20, 50. This trade-off is a slide: *"reranking top-50 cost 4× the latency
      for +1.2 NDCG@10, so we ship top-20."*
- [ ] Support ML's overnight enrichment run — make sure it survives a closed laptop

### Day 4

- [ ] Produce the final latency and indexing-cost numbers for the frozen config
- [ ] Measure cold-start separately from warm query latency. Report both honestly; the
      demo is warm, and hiding the cold number is the kind of thing a Samsung engineer
      spots in Q&A.

### Days 5–6

- [ ] Instrument the incremental re-index: **"re-embedded N of M chunks in T seconds."**
      That counter is the centrepiece of the demo's commit-slider moment — it has to be
      real and it has to be fast.
- [ ] Make sure the demo does not need network at query time. No API keys, no hosted
      embeddings. It must run on an unplugged laptop.

### Day 7 — the one that saves the submission

- [ ] **`docker compose up` on a machine that has never seen this project.** A fresh
      container, or a teammate's laptop. Not yours.
- [ ] Fix whatever breaks. Something always breaks.
- [ ] `make freeze` → commit `requirements.lock.txt`

Doing this on Day 7 instead of Day 9 is the difference between a fix and a disaster.

### Day 8

- [ ] Metrics tables for the report: NDCG@10, MRR, precision@k, recall, P50/P95 latency
      (warm and cold), indexing cost, peak memory
- [ ] Verify the README setup steps by having someone who did not write them follow them

### Day 9

- [ ] Final clean-machine verification
- [ ] Pre-warm every model before the video is recorded

## Constraints you enforce for everyone

1. **CPU only.** No CUDA dependency, no GPU-only model. Reject any PR that adds one.
2. **No network at query time.** No hosted embedding APIs, no API keys.
3. **Pinned dependencies.** The lockfile is yours; nobody edits it casually.
4. **Reproducible.** One command, clean machine, no manual steps.

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/SYSTEMS.md in full before doing anything.
I own CPU performance, packaging and reproducibility. Today is Day N.
I own: Dockerfile, docker-compose.yml, requirements.txt, Makefile, benchmarks/.
Do not modify src/samsung_prism/{chunking,enrichment,retrieval}/ or src/web/ —
other people own those. I profile them, I don't rewrite them.
Everything must run CPU-only with no network access at query time.
Install torch from the CPU index, never the default CUDA wheel.
```

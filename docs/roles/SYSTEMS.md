# Role: Systems — 2-Day Sprint

> Read [`../../AGENTS.md`](../../AGENTS.md) first, then this file.
> Timeline and cut list: [`../WORKFLOW.md`](../WORKFLOW.md).

## Mandate

**You own the team's speed.** In a two-day sprint, how fast everyone can test an idea
matters more than any single optimisation.

## Your Day 1 morning task is the most important thing anyone builds

**The subsample dev set.** ~400 queries against the full corpus, so a run takes five
minutes instead of sixty.

The arithmetic: ML has about ten working hours to beat 11.52. At sixty minutes per
experiment that is ten attempts, minus setup, minus mistakes — realistically four. At
five minutes per experiment it is dozens. **You are not saving time, you are deciding
how many ideas the team gets to try.**

**Validate it.** Run two different configurations on both the subsample and the full set
and confirm they rank in the same order. A dev set that orders configs wrongly is worse
than no dev set, because the team will trust it.

## You own

```
Dockerfile, docker-compose.yml       packaging
requirements.txt, requirements.lock.txt
Makefile
scripts/                             subsample builder, profiling
```

Plus ONNX export and quantisation of the reranker.

## You do not touch

`src/samsung_prism/{chunking,enrichment,retrieval}/` (ML), `src/web/` (Web).
You profile them; you don't rewrite them.

## This role produces graded artifacts

The theme requires CPU-only operation and explicitly asks teams to report *"precision@k,
recall, **latency and indexing cost**."* Two of those four numbers are yours, and they
land on the results slide. The submission also requires *"README with reproducible setup
instructions, Docker files"* — non-compliance is listed as grounds for disqualification.

---

## DAY 1 — 17 September

### Morning

- [ ] **Build the subsample dev set** — ~400 queries, full corpus
- [ ] **Validate it** against two full runs
- [ ] Record the full-eval wall-clock in `../../AGENTS.md` §10

### Afternoon

- [ ] ONNX int8 export of the cross-encoder reranker — **only if the spike says
      reranking is allowed.** Otherwise skip straight to Docker.
- [ ] If exporting: measure throughput in pairs/second, and report latency at k = 10, 20,
      50 so the Lead can pick a `k`. That trade-off is a slide.
- [ ] Docker skeleton. CPU-only torch wheel:
      `pip install torch --index-url https://download.pytorch.org/whl/cpu`
      The default wheel pulls ~2 GB of CUDA libraries the team cannot use.

### Evening

- [ ] Make sure ML's overnight doc2query run survives a closed laptop
      (`caffeinate -is`, output written incrementally so a partial run is still usable)

---

## DAY 2 — 18 September

### Morning

- [ ] Support the Lead's full-set runs — these are the ones that count
- [ ] Produce final latency numbers for the frozen config
- [ ] **Measure cold-start separately from warm query latency.** The demo is warm.
      Hiding the cold number is exactly what a Samsung engineer probes in Q&A. Report both.

### Afternoon — the task that saves the submission

- [ ] **`docker compose up` on a machine that has never seen this repo.** A fresh
      container, or a teammate's laptop. Not yours.
- [ ] Fix whatever breaks. Something always breaks.
- [ ] `make freeze` → commit `requirements.lock.txt`
- [ ] Hand the Lead the metrics table: NDCG@10, MRR, precision@k, recall,
      P50/P95 latency warm and cold, indexing cost, peak memory
- [ ] Verify the README by following it yourself on the clean machine

### Evening

- [ ] Pre-warm every model before the video is recorded
- [ ] Final clean-machine check before the release tag goes on

---

## Constraints you enforce for everyone

1. **CPU only.** Reject anything adding a CUDA dependency.
2. **No network at query time.** No hosted embedding APIs, no API keys. The demo must
   run on an unplugged laptop.
3. **Pinned dependencies.** The lockfile is yours.
4. **One command, clean machine, no manual steps.**

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/SYSTEMS.md in full before doing anything.
I own performance, packaging and reproducibility. 2-day sprint; today is Day N.
I own: Dockerfile, docker-compose.yml, requirements.txt, Makefile, scripts/.
Do not modify src/samsung_prism/{chunking,enrichment,retrieval}/ or src/web/.
Everything must run CPU-only with no network at query time.
Install torch from the CPU index, never the default CUDA wheel.
My top priority today is making the team's evaluation loop fast.
```

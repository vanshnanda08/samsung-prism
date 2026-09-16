# Workflow — 2-Day Sprint

> **Plan changed 16 Sep.** Mid-semester exams start ~19 September, so the original
> nine-day plan is dead. This is a **two-day sprint ending in a complete, submitted
> entry** on 18 September — one week before the actual deadline.

## The governing principle

**Be fully submittable by end of Day 2.** A finished entry in hand beats a better plan
you cannot execute during exams.

If free hours appear later, improvements get pushed and the release tag moves. The
tagged commit is what gets judged, so nothing is lost by shipping early.

| | |
|---|---|
| **Day 0** | 16 Sep — registered ✅, repo pushed ✅, baseline running |
| **Day 1** | 17 Sep — build and measure the pipeline |
| **Day 2** | 18 Sep — freeze by noon, ship by evening |
| **19 Sep →** | Mid-sems. Nothing scheduled. |
| **25 Sep** | Official deadline. Already submitted by then. |

---

## What was cut, and why

| Cut | Was | Why |
|---|---|---|
| Chrono-Index / version slider | The main differentiator (Days 5–6) | Two full days of work. Does not survive the window. |
| Structural query routing | Day 7 stretch | Was already optional. |
| Monaco code viewer | Day 6 | Nice, not graded. |
| Baseline comparison pane | Day 6 | Cut to save Web's Day 2. |
| Wide ablation matrix (20 configs) | Days 3–4 | Reduced to 5 runs. |
| Multi-model embedding ensemble | Day 3 | Two views, not four. |

### One change of substance

**Template enrichment is now the primary corpus-side lever, not doc2query.**
Extracting identifiers, docstrings, imports and control-flow shape costs seconds.
doc2query over 8,770 documents costs ~5 hours of laptop CPU. It runs overnight as a
bonus — if it is not finished by Day 2 morning, it gets killed and the template version
ships.

### One change of sequencing

**Web starts Day 1 evening, not Day 5.** There is no Day 5.

---

## Roles

| Role | Owns | Brief |
|---|---|---|
| **Lead** | `eval/`, `configs/`, `docs/` — and the freeze call | [`roles/LEAD.md`](roles/LEAD.md) |
| **ML** | `chunking/`, `enrichment/`, `retrieval/` — owns NDCG@10 | [`roles/ML.md`](roles/ML.md) |
| **Systems** | Docker, deps, ONNX, profiling — owns the fast feedback loop | [`roles/SYSTEMS.md`](roles/SYSTEMS.md) |
| **Web** | `src/web/` — owns the demo | [`roles/WEB.md`](roles/WEB.md) |

**Point your AI assistant at `AGENTS.md` plus your own role file.** That is all it needs.

**Three people?** Lead absorbs Systems. Do not drop the Systems work — the subsample dev
set is now the single most important thing anyone builds.

---

## DAY 1 — 17 September

### Morning

**Lead** — read the spike output, decide the architecture, tell everyone. 30 minutes.
The spike answers one question: can reranking go in the graded submission, or only in
the demo? Everything ML does today depends on that answer.

**Systems** — **build the subsample dev set. This is now mandatory.**
~400 queries against the full corpus. Verify it ranks configurations the same way the
full run does by testing two configs both ways. With two days you cannot afford
60-minute feedback loops; you need 5-minute ones. Nothing else you build matters as much.

**ML** — tree-sitter chunking, BM25 over identifiers, dense retrieval, RRF fusion.
Measure on the subsample as soon as it exists.

**Web** — nothing yet. Help run evaluations.

### Afternoon

**ML** — query distillation (1,400 words → algorithmic core), then template enrichment
on the corpus side. **Measure each separately** so both get an ablation row.

**Systems** — ONNX int8 reranker export, if the spike allows reranking. Otherwise
straight to Docker.

**Lead** — a config loop that runs 4–5 variants and prints a comparison table. A loop,
not a framework.

### Evening

- **Launch doc2query on the full corpus overnight.** If it is not done by morning, kill
  it. Do not wait on it.
- **Web starts.** Search box, ranked results with file and line, latency on screen.
  That is the entire UI.

### End of Day 1 you must have

- [ ] A number above the E5-Base baseline
- [ ] A UI that renders results
- [ ] Every component behind a config flag

---

## DAY 2 — 18 September

### Morning — freeze by noon

- [ ] Integrate whatever enrichment finished overnight
- [ ] Run the final 4–5 variants on the **full** set, not the subsample
- [ ] 🔒 **Pick the winner. Freeze. Noon. No exceptions.**
- [ ] Generate `appsretrieval_results.json`

### Afternoon — parallel, no dependencies

**Systems** — `docker compose up` on a machine that has never seen the repo. Fix what
breaks. Something always breaks.
**Web** — finish the UI. Check it looks right at the resolution you will record at.
**Lead** — README, ablation table, the 12-slide PPT, `AI_DISCLOSURE.md`.

### Evening — ship

1. [ ] Record the demo video — models pre-warmed, under 5:00, multiple takes
2. [ ] Upload to YouTube or Drive, **verify the link from a logged-out browser**
3. [ ] Tag the release **exactly** `PRISM_GENAI_HACKATHON_Y2026`
4. [ ] Upload `appsretrieval_results.json` as a **GitHub Release asset**
5. [ ] Confirm the PPT, video link and docs are inside the tagged commit
6. [ ] PPT filename follows `CollegeName_TeamName`
7. [ ] Submit the Google Form

**Then stop. You are safe through mid-sems.**

---

## The 5-minute demo script (compressed)

| Time | Content |
|---|---|
| 0:00–0:45 | The problem and the number. *"BM25 scores 0.95 on this dataset. The best CPU-runnable published model scores 11.52. Here is why, and what we did."* |
| 0:45–2:00 | Live query. Ranked results with file and line. Latency on screen. |
| 2:00–3:00 | A second, harder query with zero lexical overlap — show it still works. |
| 3:00–4:15 | **The ablation table.** Each component, and what it contributed. This is now your strongest asset — use the time on it. |
| 4:15–5:00 | Architecture in one diagram, CPU-only, indexing cost. End on limitations honestly. |

**Record it. Do not perform it live.**

---

## If free hours appear after mid-sems

Cheapest wins first. Push, move the tag, done.

1. Full doc2query, if the overnight run never finished
2. Content-hash incremental re-indexing — goal **P1**, roughly 3 hours
3. The version slider in the UI — makes P1 visible in ten seconds
4. Lineage grouping — the **Bonus** goal

---

## How the story changes

Without the version-native index you lose the *"nobody else built this"* angle. So lean
on what you do have:

- **The ablation table** — what each component contributes, measured
- **Beating the published CPU baseline** — E5-Base is 11.52, verifiable, public
- **Honest limitations** — including what you would have built with more time

*"Here is our number, and here is exactly which component earned each point"* is a
strong submission. It is rigour rather than novelty — and **rigour is 55% of the
rubric** (working prototype 30% + technical depth 25%), while innovation is 20%.

---

## Risk register

| Risk | Mitigation |
|---|---|
| MTEB cannot express reranking | Bi-encoder JSON; reranker in demo + ablation row |
| doc2query does not finish overnight | Template enrichment ships instead. Already the primary. |
| Subsample ranks configs wrongly | Validate against full runs on Day 1 morning before trusting it |
| Freeze slips past noon on Day 2 | Ship the best config you have at noon regardless |
| Docker fails on a clean machine | Tested Day 2 afternoon, not Day 2 evening |
| Exams start early | Everything is submitted by Day 2 evening — this is why |

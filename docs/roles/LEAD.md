# Role: Lead — 2-Day Sprint

> Read [`../../AGENTS.md`](../../AGENTS.md) first, then this file.
> Timeline and cut list: [`../WORKFLOW.md`](../WORKFLOW.md).

## Mandate

**You own the number and the clock.** In a two-day sprint the clock matters more.

## You own

```
src/samsung_prism/eval/    the config loop
configs/                   pipeline configuration
docs/                      spec, workflow, roles
README.md, AI_DISCLOSURE.md, the PPT
```

## You do not touch

`src/web/` (Web), `Dockerfile` / `requirements.txt` (Systems). Review, don't edit.

## Decisions only you make

| Decision | When |
|---|---|
| Architecture, from the spike result | Day 1, 9 AM |
| **Freeze the eval config** | **Day 2, noon — hard stop** |
| What ships vs what gets documented as a limitation | Day 2 afternoon |
| Submit | Day 2 evening |

The freeze is the one that matters. In a two-day sprint the failure mode is not building
too little — it is still tuning at 8 PM on Day 2 with no video recorded.

---

## DAY 1 — 17 September

### Morning

- [ ] Read the spike output. **Decide: does reranking go in the graded run or not?**
      Tell ML within 30 minutes — three of their hours depend on it.
- [ ] Record the baseline NDCG@10 and wall-clock in `../../AGENTS.md` §10
- [ ] Verify Systems' subsample dev set ranks two configs the same way the full run does.
      **Do not let the team trust an unvalidated dev set** — a subsample that orders
      configurations wrongly is worse than no subsample.

### Afternoon

- [ ] Build the config loop: run 4–5 variants, print a comparison table.
      A loop, not a framework. You have hours, not days.
- [ ] Variants to line up: dense only · +BM25/RRF · +query distillation ·
      +template enrichment · +rerank (if allowed)

### Evening

- [ ] Launch doc2query overnight. Set expectations: if it is not done by 9 AM, it dies.
- [ ] Sanity-check Web's first render

---

## DAY 2 — 18 September

### Morning — freeze by noon

- [ ] Integrate whatever finished overnight
- [ ] Run the final variants on the **full** set
- [ ] 🔒 **Freeze at noon regardless of where you are**
- [ ] Generate `appsretrieval_results.json`
- [ ] Announce the final number to the team

### Afternoon — writing

- [ ] README — someone who did not write it must be able to follow it
- [ ] **Ablation table.** This is now your strongest asset. One row per component,
      showing what each contributed to NDCG@10 and MRR.
- [ ] 12-slide PPT from the template in the parent folder, named `CollegeName_TeamName`
- [ ] **Limitations slide, written honestly** — say what you would have built with more
      time (version-native indexing, lineage grouping). Naming the gap reads as
      judgement; hiding it reads as a blind spot.
- [ ] `../../AI_DISCLOSURE.md` completed per feature

### Evening — ship

- [ ] Demo video: pre-warmed, under 5:00, recorded not performed
- [ ] Verify the video link from a logged-out browser
- [ ] Tag **exactly** `PRISM_GENAI_HACKATHON_Y2026`
- [ ] `appsretrieval_results.json` as a **GitHub Release asset**
- [ ] PPT, video link and docs all inside the tagged commit
- [ ] Submit the Google Form

---

## Your pitch, now that the differentiator is cut

Without the version-native index, lead with rigour instead of novelty:

> *"BM25 scores 0.95 on this dataset because natural-language queries and code share
> almost no vocabulary. The best CPU-runnable published model scores 11.52. We score X —
> on CPU, with no API calls — and here is the table showing exactly which component
> earned each point."*

Working prototype (30%) plus technical depth (25%) is 55% of the rubric. Innovation is
20%. Measured rigour is the better bet with two days.

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/LEAD.md in full before doing anything.
I am the lead. This is a 2-day sprint ending in submission on 18 Sep.
I own: src/samsung_prism/eval/, configs/, docs/, README, PPT.
Do not modify src/web/, Dockerfile or requirements.txt.
Retrieval only — never add answer generation, a chat interface, or an
LLM call in the query-time path.
Prefer the simplest thing that produces a measured number. No frameworks.
```

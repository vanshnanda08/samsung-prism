# Samsung PRISM

**The bridge between what you ask and what the code does.**

A CPU-only code retrieval engine. Ask a question in plain English, get back the code
that answers it — ranked, with file and line locations.

Built for **Theme 01 — Agentic Code Intelligence**, Samsung PRISM Generative AI
Hackathon, 3rd Edition 2026–27.

---

## The problem

On the evaluation dataset, BM25 keyword search scores **0.95 NDCG@10 out of 100**.

That near-zero number is the whole diagnosis: a natural-language question and the code
that answers it share almost no surface vocabulary. A question says *"find the shortest
path between two nodes"*; the code says `dist = [inf]*n; heapq.heappush(pq, (0, src))`.
Not one word in common.

So this is not a search problem. It is a **translation** problem across two different
languages.

## The approach

Most systems attack this from the query side — rewriting the question to look more like
code. That is the weaker lever: the query arrives at runtime and you get one attempt.

Samsung PRISM closes the gap from **both sides**:

- **Index side (offline).** For every code snippet, generate a natural-language
  description of what it does and a structural signature. Now retrieval matches English
  against English, which embedding models are good at.
- **Query side (online).** Distil long queries down to their algorithmic core, and
  generate a pseudo-code sketch so code-to-code comparison is also available.

Then fuse the views with Reciprocal Rank Fusion and rerank the top-k with a quantised
cross-encoder — all on CPU, with no network calls at query time.

Because index enrichment is content-addressed per chunk, **fast incremental
re-indexing across versions comes almost free** — which is submission goal P1, and the
Bonus goal on top of it.

---

## Documentation

| File | What it covers |
|---|---|
| [`AGENTS.md`](AGENTS.md) | **Start here.** Project context, scope, architecture, engineering rules. Written to be read by both people and AI assistants. |
| [`docs/THEME1_SPEC.md`](docs/THEME1_SPEC.md) | Distilled organiser requirements — facts only, with sources |
| [`docs/WORKFLOW.md`](docs/WORKFLOW.md) | Day-by-day build plan, role assignments, daily gates, risk register |
| [`docs/roles/`](docs/roles/) | **Per-person briefs** — one file per role with day-by-day tasks, owned files, and a ready-made prompt for that person's AI assistant |
| [`AI_DISCLOSURE.md`](AI_DISCLOSURE.md) | Running log of AI assistance, required at submission |

**If you are an AI assistant working in this repository, read `AGENTS.md` in full before
writing any code.**

---

## Quickstart

```bash
# 1. Environment
python3.11 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 2. Reproduce the published baseline (~30-60 min on CPU)
make baseline

# 3. Run the full Samsung PRISM pipeline evaluation
make eval

# 4. Run the ablation matrix
make ablate

# 5. Serve the demo
make demo
```

Docker:

```bash
docker compose up
```

---

## Results

| Configuration | NDCG@10 | MRR | Notes |
|---|---|---|---|
| BM25 (published) | 0.95 | — | Near-zero lexical overlap |
| BGE-Base (published) | 4.05 | — | |
| E5-Base (published) | 11.52 | — | Best CPU-viable published baseline |
| E5-Mistral 7B (published) | 21.33 | — | GPU only |
| Voyage-Code-002 (published) | 26.52 | — | API only |
| **Our baseline reproduction** | _TBD_ | _TBD_ | |
| **Samsung PRISM** | _TBD_ | _TBD_ | |

Full ablation table to be added once the eval config is frozen.

---

## Constraints

- **CPU only.** No CUDA dependency, no GPU-only model.
- **No network at query time.** No hosted embedding APIs, no API keys. The demo runs
  fully offline.
- **Retrieval only.** Answer generation, code explanation and code generation are
  explicitly out of scope per the organiser guidelines.

---

## Team

| Name | Role | Email |
|---|---|---|
| _TBD_ | Lead | |
| _TBD_ | ML | |
| _TBD_ | Systems | |
| _TBD_ | Web | |

**Institution:** Thapar Institute of Engineering & Technology, Patiala

---

## Submission checklist

- [ ] Working prototype code in this public repository
- [ ] README with reproducible setup instructions
- [ ] Dockerfile and docker-compose
- [ ] `appsretrieval_results.json` uploaded as a GitHub **Release asset**
- [ ] Release tagged `PRISM_GENAI_HACKATHON_Y2026` on the final commit
- [ ] Demo video ≤ 5 minutes
- [ ] Presentation file named `CollegeName_TeamName`
- [ ] AI Usage Disclosure form completed
- [ ] Submitted via the Google Form by **25 Sep 2026, 11:59 PM**

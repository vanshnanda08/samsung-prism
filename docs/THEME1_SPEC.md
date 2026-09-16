# Theme 01 Specification — Distilled from Organiser Material

> **Facts only.** Everything in this file is taken directly from the official PRISM
> material. Analysis and design decisions live in `AGENTS.md`. If you need to know what
> the organisers actually require, this is the file to read.
>
> Sources: `Samsung PRISM_Y2026_GenAI_Hackathon_3rd_Edition.V2(2).pdf` (main deck),
> `theme1_guidelines.pdf`, `CollegeName_TeamName_Submission.pptx`,
> `LangAI3.0_AI_Disclosure.docx`.

---

## 1. The event

Samsung PRISM Generative AI Hackathon, 3rd Edition 2026–27. Organised by the Language
AI Team and the PRISM Team, Samsung R&D Institute India.

One build round — there is no ideation stage this year. Round 1 requires a working
prototype.

### Timeline

| Date | Event |
|---|---|
| 11 Sep 2026 | Launch |
| 16 Sep 2026, 11:59 PM | Registration closes |
| **25 Sep 2026, 11:59 PM** | **Final submission** |
| 9 Oct 2026 | Top 15 announced |
| 15 Oct 2026 | Final demo round |
| 24 Oct 2026 | Results |

### Team rules

- Maximum 4 members per team, single college
- Team name format: `CollegeName_TeamName`
- One theme, one submission per team

---

## 2. Global evaluation weights

| Criterion | Weight |
|---|---|
| Working prototype & functionality | 30% |
| Technical depth & feasibility | 25% |
| Innovation & originality | 20% |
| Relevance to theme | 15% |
| Presentation & documentation | 10% |

What the jury looks for: *"Does the prototype actually work? Is the technical approach
sound? Would a real user want this? Can it be taken further as a worklet?"*

---

## 3. Theme 01 — problem statement (main deck)

> *"Voice-assistant codebases are huge: dozens of agents and tools spread across
> thousands of files. A new developer cannot hold it all in their head, and neither can
> an LLM, since the whole repo will never fit in a context window. Finding where
> something happens, and then fixing it, is the slow part."*

### What to build (deck)

- Take a plain-English question and return matching code snippets with file and line locations
- Answer structural queries: *"which files call tool XYZ before tool ABC?"*
- Answer usage queries: *"where is the Bluetooth-settings deeplink used?"*
- Work agentically: plan, search, read and refine over a codebase far larger than the context window
- Bonus: suggest optimisations for the code paths surfaced

### Scope and constraints (deck)

- Sample open-source codebase provided with the problem statement
- Single language: **JavaScript**
- Output is snippets and locations; optimisation suggestions are a bonus, full code generation is not required
- **Must run on CPU; minimal GPU use allowed**

### Tech focus (deck)

- Code-aware embeddings and vector search, plus AST or call-graph indexing for structural queries
- Agentic retrieval loop over the index
- **Report precision@k, recall, latency and indexing cost**

---

## 4. Theme 01 — guidelines document

### The core task

> *"The problem at its core is: code retrieval. Given a library of code and a query in
> natural language, provide a ranking of the code snippets in order of their relevance
> to the query."*

Worked example from the guidelines. Query: *"How is the input preprocessed before going
to the main function?"*

```js
// Code#1                      // Code#2                      // Code#3
function normalize(str) {      function check(s) {            function perf(str) {
  const str2 = str.trim();       var pre = s.slice(0,6);        if (act(A, str)) {
  return forward(str2);          return pre === 'en-US';          return act(B, str)
}                              }                                }
                                                              }
```

Expected ranking: **Code#1 > Code#2 > Code#3**.

> *"This is a pretty difficult problem and likely cannot be solved in a single pass.
> You should be aware that the actual code snippets range in the thousands and the code
> snippets can also increase in length."*

### Explicitly out of scope

> *"Generating an answer for the query, explaining the results or anything to do with
> the generation that takes place after the retrieval is out of scope for this problem
> statement."*

### Invited improvement axes

> *"Your solution can have improvements based around (but not limited to):*
> 1. *Categorizing the query*
> 2. *Pre-processing the query*
> 3. *Categorizing the retrieved code snippets*
> 4. *Pre/post processing of the code snippets*
> 5. *Performing multiple retrieval passes based on the above"*

### CPU constraint

> *"Most retrieval and embedding models are small and fast enough to run on CPU alone.
> As such, your solution is also expected to run on CPU with minimal GPU resource
> utilization."*

### Why not just use an LLM to rank

> *"The number of snippets and their length are too long to fit in the context window of
> any LLM. Also, LLMs are slow when it comes to processing long texts, retrieval is
> generally the first step in a RAG pipeline and is expected to be faster than the
> generation step, which involves an LLM."*

---

## 5. Submission goals, in order of importance

### P0 — Retrieval Accuracy

> *"This is the base criteria, your solution should retrieve the relevant code snippets
> in response to a query."*

### P1 — Retrieval across versions

> *"Code-bases are hardly static, they keep changing with new commits added every
> minute. Your solution should support performing retrieval on different versions of the
> code snippets. This means that your solution should be able to rebuild any indexes,
> caches, etc for any version/change in a reasonable amount of time."*

### Bonus — Evolutionary Retrieval

> *"This is an extension of P1. If your solution is able to support different versions of
> the code snippets, you should be able to retrieve code snippets across all versions of
> them. This has specific implications for retrieval, because even across different
> versions, the snippets would still be very similar, which would make them hard to rank
> properly."*

---

## 6. How the solution is evaluated

Two stages.

### Stage 1 — Screening (competitive, automatic)

> *"We will rank your solutions on the P0 submission goal (Retrieval Accuracy) based on
> their performance on the test split of the CoIR apps dataset. You will have to submit
> a csv file with the responses from the test split of the dataset, from which we will
> measure: 1. NDCG@10  2. MRR"*
>
> *"This will be a competitive screening meaning we will be selecting the top
> submissions for hands-on evaluation."*

Dataset: `https://huggingface.co/datasets/CoIR-Retrieval/apps` (test split).

### Stage 2 — Hands-on

> *"During the hands-on evaluation, we will review your PPT, demo video along with
> running your code on certain type of queries (which will be similar to that of the
> dataset). We will also evaluate the P1 (Retrieval across versions) and the Bonus
> submission goals here."*

---

## 7. Running the official evaluation

The guidelines supply this skeleton:

```python
import numpy as np
from sentence_transformers import SentenceTransformer

import mteb
from mteb.models.abs_encoder import AbsEncoder
from mteb.models.model_meta import ModelMeta
from mteb.types import PromptType

class PrePostPipelineEncoder(AbsEncoder):
    # Your implementation here

def main() -> None:
    model = PrePostPipelineEncoder()

    task = mteb.get_task("AppsRetrieval")      # Make sure you choose this task
    result = mteb.evaluate(
        model,
        [task],
        encode_kwargs={"batch_size": 64},
    )

    # Write the evaluation JSON you asked for.
    task_result = list(result.task_results)[0]
    with open("appsretrieval_results.json", "w") as f:   # Upload this file
        json.dump(task_result.to_dict(), f, indent=2)
```

Reference: https://docs.mteb.org/get_started/usage/running_the_evaluation/

> **⚠ Open question for the team.** The skeleton subclasses `AbsEncoder`, which exposes
> an `encode()` interface. It is not established whether a cross-encoder reranking stage
> can be expressed within it. **Resolve this before building around a reranker.** If it
> cannot, the submitted JSON reflects the bi-encoder pipeline and the reranker lives in
> the demo and the ablation table instead.

---

## 8. What to have ready at submission

From the guidelines:

1. JSON file with the inference on the test split of the CoIR apps dataset
2. PPT
3. GitHub repo with instructions on how to run the submission

> *"You should make sure that your submission can be run by following the steps in the
> GitHub repo. Please attach any files needed as artifacts as a Release in the GitHub
> repo."*

From the main deck:

- Working prototype code — public or shared GitHub repo
- README with reproducible setup instructions, Docker files, and other requirements
- **A release tag named `PRISM_GENAI_HACKATHON_Y2026` on the final commit. The tagged commit is what gets judged.**
- *"Make sure everything referenced in your submission—PPT, demo video, documentation, etc.—is present in the tagged commit"*
- Demo video, max 5 minutes (YouTube or Drive link)
- Presentation file (PPT or PDF), named `CollegeName_TeamName`
- Submitted through the Google Form

> *"Teams NOT following the submission guideline would lead to direct disqualification."*

---

## 9. What the PPT must cover

The supplied template has 12 slides:

1. Title — Theme ID, team name, college, member names and emails, GitHub link
2. Theme
3. **Existing Solutions & Gaps**
4. **Our Solution & Architecture Diagram**
5. Demo & Product Walkthrough
6. Tools and tech stack used
7. Impact & Use case
8. **Innovation highlights, results and limitations**
9. What's next
10. **Brownie points slide (differentiation)**
11. Checklist — updated on public GitHub
12. Thank you

Guidance from the guidelines document:

> *"Our PPT template answers this pretty well but we would be interested in seeing the
> details of your approach (which pre/post processing steps, which embedding model,
> etc). You could also show the retrieval results for a tough query which shows how well
> your solution is working."*

---

## 10. What the demo must show

> *"We would like to see the solution working in the demo. You should not show us just
> the inference results or the numbers. You should show the responses for a given query.
> We would also be interested in seeing how fast your solution is."*

**Implication:** a live query interface and visible latency are required, not optional.

---

## 11. AI Usage Disclosure Form

A separate form (`LangAI3.0_AI_Disclosure.docx`) requires:

- Team details and submission date
- Whether AI was used (Yes/No)
- Purpose of AI usage — idea generation, code generation, UI/UX, content creation, data analysis, testing/debugging, other
- **Per-feature classification:** feature name, Self-Generated / AI-Generated / Both, and a description including **AI tools/platform used, prompt used, output summary, and modifications**
- Ethical and compliance confirmation
- Declaration and sign-off

Maintain `AI_DISCLOSURE.md` continuously rather than reconstructing it at the end.

---

## 12. Known gaps and inconsistencies in the source material

Recorded so nobody re-discovers them.

1. **Language mismatch.** The deck specifies JavaScript. The screening dataset
   (CoIR `apps`) is Python, with queries that are competitive-programming problem
   statements averaging ~1,400 words. These are different retrieval tasks.
2. **Agentic vs out-of-scope.** The deck says *"work agentically: plan, search, read and
   refine"* and offers a bonus for optimisation suggestions. The guidelines say
   generation and explanation are out of scope. Interpretation: *agentic* means
   multi-pass **retrieval**, not an LLM agent that produces prose.
3. **Missing asset.** The sample JavaScript codebase referenced in the deck was not
   included in the material provided. If it does not arrive, use a public open-source
   JavaScript voice-assistant repository and declare the substitution in the README.

**Action:** these were raised with `prism@samsung.com`. Record any reply in this file.

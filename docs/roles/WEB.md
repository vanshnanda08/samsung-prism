# Role: Web

> **Brief for you and your AI assistant.** Read [`../../AGENTS.md`](../../AGENTS.md)
> first for project context, then this file. [`../WORKFLOW.md`](../WORKFLOW.md) has the
> full timeline; this file is only your slice of it.

## Mandate

**You make the retrieval visible.** The organisers require it:

> *"We would like to see the solution working in the demo. You should not show us just
> the inference results or the numbers. You should show the responses for a given query.
> We would also be interested in seeing how fast your solution is."*

A live query interface with visible latency is a requirement, not a nice-to-have.

## Read this before anything else

**You do not start building until Day 5.**

That is deliberate and it is the most important instruction in this file. Presentation
is 10% of the grading rubric; working prototype and technical depth together are 55%.
More to the point, a UI built before the retrieval API is settled gets rewritten. Teams
lose this format by polishing a frontend while the engine underneath is unmeasured.

Days 1–4 you are not idle — see below. You are just not writing frontend code.

## You own these files

```
src/web/                    the entire demo UI
```

## You do not touch

Anything in `src/samsung_prism/`. You consume the API; you don't change it.

## Days 1–4 — what to do instead

- [ ] Read [`../THEME1_SPEC.md`](../THEME1_SPEC.md) — especially §10, what the demo must show
- [ ] Sketch the UI **on paper**. Four screens, no code.
- [ ] Help run evaluations. Every extra config the team can test is worth more right now
      than any pixel.
- [ ] Agree the API response shape with the Lead by end of Day 4 so Day 5 starts clean

## Day 5 — scaffold

- [ ] Next.js + TypeScript + Tailwind + shadcn/ui
- [ ] Search input, ranked result list
- [ ] Each result: file path, line range, relevance bar, snippet preview

## Day 6 — the four things that matter

| Feature | Why it earns its place |
|---|---|
| **Monaco viewer** | Click a result, see the code in context with the surrounding function |
| **Latency HUD** | The organisers explicitly ask how fast it is. Put the number on screen. |
| **Commit slider** | Drag to switch repository version; live counter reads *"re-embedded 47 of 8,770 chunks in 1.9 s."* This is goals P1 and Bonus made visible in ten seconds, and almost no competing team will have it. |
| **Baseline comparison pane** | Same query under stock `e5-base` beside ours. Makes the improvement visible instead of asserted. |

The commit slider is the single highest-value thing you build. Prioritise it over polish.

## Day 7

- [ ] Polish, responsive layout, loading states
- [ ] Make sure it looks right at the resolution you will record the video at
- [ ] 🔒 **Feature freeze, 6 PM**

## Days 8–9

- [ ] Support the demo video capture — you know the UI best, so you drive during recording
- [ ] Multiple takes. Models pre-warmed. Under 5:00.

## Never build

- **Authentication, login, or user accounts.** Zero rubric value here.
- **Any CRUD feature** — saved searches, history, favourites, settings pages
- **A chat interface.** This is a retrieval project; answer generation is explicitly out
  of scope per the organiser guidelines.
- A settings panel exposing every config flag. One or two toggles for the demo, no more.
- Anything requiring a backend change you did not agree with the Lead

If you find yourself building a form that writes to a database, stop — you have drifted
into the exact category of work this rubric does not reward.

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/WEB.md in full before doing anything.
I own the demo UI. Today is Day N.
Only modify src/web/. Never modify src/samsung_prism/ — I consume that API,
I don't change it.
Do NOT build authentication, user accounts, saved searches, settings pages,
or any CRUD feature — they score zero in this hackathon's rubric.
Do NOT build a chat interface. This is a retrieval project; answer generation
is explicitly out of scope.
The four features that matter: ranked results with file:line, a Monaco code
viewer, an on-screen latency readout, and a version/commit slider showing
incremental re-indexing.
```

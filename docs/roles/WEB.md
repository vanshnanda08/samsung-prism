# Role: Web — 2-Day Sprint

> Read [`../../AGENTS.md`](../../AGENTS.md) first, then this file.
> Timeline and cut list: [`../WORKFLOW.md`](../WORKFLOW.md).

## Mandate

**You make the retrieval visible.** The organisers require it:

> *"You should not show us just the inference results or the numbers. You should show the
> responses for a given query. We would also be interested in seeing how fast your
> solution is."*

A live query interface with visible latency is a requirement. Everything beyond that is
optional — and in a two-day sprint, optional means cut.

## Your scope is now three things

1. A search box
2. Ranked results — file path, line range, snippet, relevance score
3. **Latency displayed on screen**

That is the whole UI. Build those three well and stop.

## Cut from the original plan — do not build these

| Cut | Why |
|---|---|
| Monaco code viewer | A styled `<pre>` with syntax highlighting is enough |
| Commit / version slider | The feature behind it was cut |
| Baseline comparison pane | Costs a half-day you do not have |
| Dark mode, animations, polish passes | Presentation is 10% of the rubric |

## You own

```
src/web/
```

## You do not touch

Anything in `src/samsung_prism/`. You consume the API; you don't change it.

---

## DAY 1 — 17 September

### Morning and afternoon — still not coding

- [ ] Read [`../THEME1_SPEC.md`](../THEME1_SPEC.md) §10 — what the demo must show
- [ ] **Help run evaluations.** Every extra configuration the team can test today is
      worth more than any pixel. This is genuinely the highest-value thing you can do
      before evening.
- [ ] Agree the API response shape with the Lead. Get it in writing before you start.

### Evening — start

- [ ] Next.js + TypeScript + Tailwind, scaffolded
- [ ] Search input wired to the API
- [ ] Results list rendering: file path, line range, snippet, score
- [ ] **Latency readout on screen**

Ship something that renders real results tonight, however plain. A working ugly page on
Day 1 beats a beautiful half-finished one on Day 2.

---

## DAY 2 — 18 September

### Afternoon

- [ ] Syntax highlighting on snippets (`highlight.js` or `prism.js` — one import, done)
- [ ] Empty state, loading state, error state. Three small things that stop the demo
      looking broken when something is slow.
- [ ] Check it looks right **at the resolution you will record the video at**
- [ ] Hard stop by 6 PM

### Evening

- [ ] **You drive during the video recording** — you know the UI best
- [ ] Multiple takes, models pre-warmed, under 5:00

---

## Never build

- **Authentication, login, user accounts.** Zero rubric value.
- **Any CRUD feature** — saved searches, history, favourites, settings pages
- **A chat interface.** This is retrieval; answer generation is explicitly out of scope
  per the organiser guidelines.
- A settings panel exposing config flags. One toggle at most.

If you find yourself building a form that writes to a database, stop — you have drifted
into the exact category of work this rubric does not reward.

## Brief for your AI assistant

```
Read AGENTS.md and docs/roles/WEB.md in full before doing anything.
I own the demo UI. This is a 2-day sprint; today is Day N.
Only modify src/web/. Never modify src/samsung_prism/ — I consume that API.
Scope is exactly three things: a search box, a ranked results list showing
file path and line range, and latency displayed on screen. Nothing else.
Do NOT build authentication, user accounts, saved searches, settings pages,
or any CRUD feature — they score zero in this hackathon's rubric.
Do NOT build a chat interface. Answer generation is out of scope.
Prefer the simplest implementation. I have about one working day.
```

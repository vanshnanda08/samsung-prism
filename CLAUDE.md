# CLAUDE.md

This project's context for AI assistants lives in **[`AGENTS.md`](AGENTS.md)**.

Read it in full before writing any code. It defines the scope, the architecture, the
hard constraints, and a list of things that must not be built.

Two rules that are violated most often, repeated here so they are not missed:

1. **This is a retrieval project, not a generation project.** Do not build a chatbot,
   an answer generator, or a "chat with your codebase" interface. The organisers state
   that generation after retrieval is out of scope.
2. **No LLM calls in the query-time path.** LLMs are used offline for index enrichment
   and for cheap query distillation only. The ranking hot path must stay fast and run
   on CPU with no network access.

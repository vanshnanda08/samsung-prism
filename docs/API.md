# API Contract

> **Frozen 16 Sep.** Web builds against this; the backend implements it. It will not
> change without the Lead agreeing in writing. Build the UI against a mock of this shape
> tonight and swap in a real fetch on Day 1 evening.

## `POST /search`

### Request

```json
{
  "query": "how is the input preprocessed before going to the main function",
  "top_k": 10,
  "version": null
}
```

| Field | Type | Notes |
|---|---|---|
| `query` | string | Natural language. May be long — the APPS benchmark averages ~1,400 words. |
| `top_k` | int | Default 10. |
| `version` | string \| null | Repository version/ref. `null` means current. Reserved — the version feature is deferred, but the field exists so the UI never needs changing. |

### Response — 200

```json
{
  "query": "how is the input preprocessed before going to the main function",
  "latency_ms": 143,
  "total_indexed": 8770,
  "results": [
    {
      "rank": 1,
      "file": "src/lib/normalize.js",
      "start_line": 12,
      "end_line": 28,
      "score": 0.87,
      "language": "javascript",
      "snippet": "function normalize(str) {\n  const str2 = str.trim();\n  return forward(str2);\n}"
    }
  ]
}
```

| Field | Type | Notes |
|---|---|---|
| `latency_ms` | float | **Display this on screen.** The organisers explicitly ask how fast the solution is. |
| `total_indexed` | int | Chunk count. Useful context in the demo. |
| `results[].rank` | int | 1-based, already sorted. The UI does not re-sort. |
| `results[].score` | float | 0–1. Render as a relevance bar. Not calibrated across queries — never show it as a percentage. |
| `results[].snippet` | string | Raw code with real newlines. Apply syntax highlighting client-side. |
| `results[].language` | string | For the highlighter. `"python"` or `"javascript"`. |

An empty `results` array is valid — render an empty state, not an error.

### Errors

```json
{ "error": "index_not_built", "message": "No index found. Run: make index" }
```

| Code | Meaning |
|---|---|
| `index_not_built` | Backend is up, no index exists yet |
| `query_empty` | Empty or whitespace-only query |
| `internal` | Anything else |

Render `message` directly. Do not parse it.

## `GET /health`

```json
{ "status": "ok", "index_loaded": true, "model_loaded": true, "total_indexed": 8770 }
```

Returns 200 once models and index are ready. Useful for a "warming up" state — cold
start loads models and takes several seconds.

## Mock for tonight

```bash
# src/web/mock/search.json — build the UI against this, swap the fetch on Day 1 evening
```

Put three or four results in the mock, with varying score and snippet length, so the
layout gets tested against realistic content rather than one tidy row.

## Notes for the UI

- **Latency must be visible.** It is a stated evaluation interest, not decoration.
- Long snippets: clamp to ~20 lines with an expand control. Some APPS documents are long.
- Cold start is slow. Poll `/health` on load and show a warming state rather than a
  broken-looking empty page.
- `version` is in the contract but the feature is deferred — do not build a version
  picker during the sprint.

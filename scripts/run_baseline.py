"""
Day 0/1 baseline: reproduce the published E5-Base number on AppsRetrieval.

Published reference (CoIR paper, ACL 2025), NDCG@10 on Apps:
    BM25            0.95
    BGE-Base        4.05
    E5-Base        11.52   <- this is what we are reproducing
    E5-Mistral-7B  21.33   (GPU)
    Voyage-Code-2  26.52   (API)

This run has two jobs:
  1. Prove the whole evaluation path works before we build anything.
  2. Produce the WALL-CLOCK TIME. That number is the team's iteration budget
     for the next nine days - it decides whether we can test 20 ideas or 3.

Run (recommended, prevents the Mac sleeping mid-run):
    caffeinate -is python scripts/run_baseline.py

Fast smoke test first (~2 min, confirms the path works before the long run):
    python scripts/run_baseline.py --smoke
"""

import argparse
import json
import pathlib
import sys
import time

MODEL = "intfloat/e5-base-v2"
TASK = "AppsRetrieval"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--out", default="results/baseline")
    ap.add_argument("--batch-size", type=int, default=32)
    ap.add_argument("--smoke", action="store_true",
                    help="Load model and task, skip the full evaluation.")
    args = ap.parse_args()

    import mteb

    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    print(f"mteb version : {getattr(mteb, '__version__', 'unknown')}")
    print(f"model        : {args.model}")
    print(f"task         : {TASK}")
    print(f"batch size   : {args.batch_size}")
    print()

    # Prefer MTEB's own model loader: it applies the "query: " / "passage: "
    # prefixes that E5 needs. Loading a bare SentenceTransformer skips those
    # and silently costs several NDCG points.
    print("Loading model...")
    t0 = time.time()
    try:
        model = mteb.get_model(args.model)
        print(f"  loaded via mteb.get_model  ({time.time() - t0:.1f}s)")
    except Exception as e:  # noqa: BLE001
        print(f"  mteb.get_model failed ({type(e).__name__}: {e})")
        print("  falling back to SentenceTransformer")
        print("  WARNING: E5 prefixes may not be applied - score will read low")
        from sentence_transformers import SentenceTransformer
        model = SentenceTransformer(args.model)
        print(f"  loaded  ({time.time() - t0:.1f}s)")

    print("\nLoading task...")
    task = mteb.get_task(TASK)
    print(f"  {task.metadata.name} | main score: {task.metadata.main_score} "
          f"| splits: {task.metadata.eval_splits}")

    if args.smoke:
        print("\n--smoke: model and task both load. Path is good.")
        print("Now run the full evaluation:")
        print("    caffeinate -is python scripts/run_baseline.py")
        return

    print("\n" + "=" * 62)
    print("STARTING FULL EVALUATION")
    print("~8,770 documents + ~3,770 queries (avg ~1,400 words) on CPU.")
    print("Expect 30-90 minutes. Do not close the laptop.")
    print("=" * 62 + "\n")

    start = time.time()

    # API shape has changed across mteb versions - try both.
    try:
        result = mteb.evaluate(
            model, [task],
            encode_kwargs={"batch_size": args.batch_size},
        )
        task_result = list(result.task_results)[0]
        payload = task_result.to_dict()
    except (AttributeError, TypeError) as e:
        print(f"[mteb.evaluate not usable: {type(e).__name__}: {e}]")
        print("[falling back to the MTEB class API]\n")
        evaluation = mteb.MTEB(tasks=[task])
        results = evaluation.run(
            model,
            output_folder=str(out),
            encode_kwargs={"batch_size": args.batch_size},
        )
        r = results[0]
        payload = r.to_dict() if hasattr(r, "to_dict") else r

    elapsed = time.time() - start

    dest = out / "appsretrieval_results.json"
    dest.write_text(json.dumps(payload, indent=2, default=str))

    print("\n" + "=" * 62)
    print("DONE")
    print("=" * 62)
    print(f"wall clock : {elapsed / 60:.1f} minutes   <-- RECORD THIS")
    print(f"written    : {dest}")

    # Surface the headline metrics without assuming a fixed payload shape.
    print("\nScores found in the result:")
    hits = []

    def walk(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                walk(v, f"{path}.{k}" if path else k)
        elif isinstance(node, (int, float)) and any(
            m in path.lower() for m in ("ndcg_at_10", "ndcg@10", "mrr", "main_score", "recall_at_10")
        ):
            hits.append((path, node))

    walk(payload)
    for path, val in hits[:25]:
        print(f"  {path}: {val}")
    if not hits:
        print("  (none auto-detected - open the JSON and look for ndcg_at_10)")

    print("\nReference: published E5-Base on Apps is 11.52 NDCG@10.")
    print("If you are near that, the evaluation path is correct.")
    print("\nNext: record the wall-clock time and the NDCG@10 in AGENTS.md section 10.")
    if elapsed > 45 * 60:
        print("\n!! Over 45 minutes. Systems: build the subsample dev set tomorrow.")
        print("   The team cannot iterate 20 times against a loop this long.")


if __name__ == "__main__":
    sys.exit(main())

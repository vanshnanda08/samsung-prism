"""
Day 1 spike: what does this version of MTEB actually let us plug in?

Answers one question that decides three days of work:
  Can a cross-encoder reranking stage live inside the graded submission,
  or only inside the demo?

Run:  python scripts/spike_mteb.py
Then send the full output to Claude.
"""

import inspect
import pkgutil
import sys


def rule(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def safe(fn, label):
    try:
        return fn()
    except Exception as e:  # noqa: BLE001 - we want every failure visible
        print(f"  [{label}] FAILED: {type(e).__name__}: {e}")
        return None


rule("0. ENVIRONMENT")
print("  python:", sys.version.split()[0])
try:
    import mteb
    print("  mteb:", getattr(mteb, "__version__", "unknown"))
except ImportError:
    sys.exit("  mteb is not installed. Run: pip install mteb")

for pkg in ("sentence_transformers", "torch", "transformers"):
    try:
        m = __import__(pkg)
        print(f"  {pkg}:", getattr(m, "__version__", "unknown"))
    except ImportError:
        print(f"  {pkg}: NOT INSTALLED")


rule("1. AbsEncoder — the interface the guidelines tell us to subclass")


def _absencoder():
    from mteb.models.abs_encoder import AbsEncoder
    print("  import path: mteb.models.abs_encoder.AbsEncoder  [OK]")
    print("\n  public methods:")
    for name, obj in inspect.getmembers(AbsEncoder, predicate=inspect.isfunction):
        if name.startswith("_"):
            continue
        try:
            print(f"    {name}{inspect.signature(obj)}")
        except (ValueError, TypeError):
            print(f"    {name}(?)")
    print("\n  abstract methods:", getattr(AbsEncoder, "__abstractmethods__", None) or "none")
    print("  base classes:", [c.__name__ for c in AbsEncoder.__mro__[1:]])
    return AbsEncoder


safe(_absencoder, "AbsEncoder")


rule("2. Is there a SEARCH-level hook? (this is the real question)")
print("  If retrieval search can be overridden, reranking goes in the graded run.")
print("  If only encode() exists, reranking is demo-and-ablation only.\n")


def _search_hooks():
    import mteb.models as mm
    keys = ("search", "retriev", "rerank", "cross", "wrapper", "protocol")
    found = [m.name for m in pkgutil.iter_modules(mm.__path__)
             if any(k in m.name.lower() for k in keys)]
    print("  mteb.models submodules:", found or "none matched")

    top = [a for a in dir(mteb) if any(k in a.lower() for k in keys)]
    print("  mteb top-level names:", top or "none matched")

    try:
        import mteb.abstasks as ab
        ev = [m.name for m in pkgutil.iter_modules(ab.__path__)
              if any(k in m.name.lower() for k in keys)]
        print("  mteb.abstasks submodules:", ev or "none matched")
    except Exception as e:  # noqa: BLE001
        print("  mteb.abstasks: not importable —", type(e).__name__)


safe(_search_hooks, "search-hooks")


rule("3. Retrieval evaluator — can we subclass the search step?")


def _evaluator():
    import mteb.evaluation.evaluators as ev
    mods = [m.name for m in pkgutil.iter_modules(ev.__path__)]
    print("  evaluators:", mods)
    for cand in ("RetrievalEvaluator", "DenseRetrievalExactSearch", "DRESModel"):
        obj = getattr(ev, cand, None)
        print(f"    {cand}: {'FOUND' if obj else 'not exported at package level'}")


safe(_evaluator, "evaluators")


rule("4. AppsRetrieval — the task we are graded on")


def _task():
    t = mteb.get_task("AppsRetrieval")
    md = t.metadata
    print("  name:        ", md.name)
    print("  type:        ", md.type)
    print("  main_score:  ", md.main_score)
    print("  eval_splits: ", md.eval_splits)
    print("  eval_langs:  ", getattr(md, "eval_langs", "n/a"))
    n = getattr(md, "n_samples", None) or getattr(md, "descriptive_stats", None)
    print("  size info:   ", n if n else "not exposed in metadata")


safe(_task, "AppsRetrieval")


rule("5. evaluate() signature — how we actually launch a run")


def _evaluate_sig():
    fn = getattr(mteb, "evaluate", None)
    if fn is None:
        print("  mteb.evaluate does not exist in this version.")
        print("  Looking for the MTEB class instead:")
        cls = getattr(mteb, "MTEB", None)
        if cls:
            print("    mteb.MTEB.run signature:", inspect.signature(cls.run))
        return
    print("  mteb.evaluate", inspect.signature(fn))


safe(_evaluate_sig, "evaluate")


rule("6. get_model — does MTEB know e5-base-v2 and its prompt prefixes?")
print("  e5 models need 'query: ' / 'passage: ' prefixes to score properly.")
print("  If MTEB's registry knows the model, it applies them for us.\n")


def _get_model():
    fn = getattr(mteb, "get_model_meta", None) or getattr(mteb, "get_model", None)
    if fn is None:
        print("  no get_model/get_model_meta in this version")
        return
    print(f"  using mteb.{fn.__name__}{inspect.signature(fn)}")
    meta = mteb.get_model_meta("intfloat/e5-base-v2")
    print("  model found in registry:", meta.name)
    print("  revision:", getattr(meta, "revision", "n/a"))
    prompts = getattr(meta, "model_prompts", None) or getattr(meta, "prompts", None)
    print("  prompts:", prompts if prompts else "NONE — we must add prefixes ourselves")


safe(_get_model, "get_model")


print("\n" + "=" * 70)
print("DONE — send this entire output to Claude.")
print("=" * 70)

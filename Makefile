.PHONY: help setup baseline eval ablate index demo docker clean freeze

CONFIG ?= configs/default.yaml
OUT    ?= results

help:
	@echo "Samsung PRISM - make targets"
	@echo ""
	@echo "  setup      Create venv and install dependencies (CPU-only torch)"
	@echo "  baseline   Run stock e5-base-v2 through MTEB AppsRetrieval"
	@echo "  eval       Run the full Samsung PRISM pipeline through MTEB AppsRetrieval"
	@echo "  ablate     Run the ablation matrix across pipeline configurations"
	@echo "  index      Build the index for a repository (REPO=path VERSION=ref)"
	@echo "  demo       Start the API and the web UI"
	@echo "  docker     Build and run via docker compose"
	@echo "  freeze     Write requirements.lock.txt from the current environment"
	@echo "  clean      Remove caches and generated artifacts"
	@echo ""
	@echo "  CONFIG=$(CONFIG)   OUT=$(OUT)"

setup:
	python3.11 -m venv .venv
	./.venv/bin/pip install --upgrade pip
	./.venv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu
	./.venv/bin/pip install -r requirements.txt
	@echo ""
	@echo "Done. Activate with: source .venv/bin/activate"

# Reproduce the published E5-Base number (11.52 NDCG@10).
# Expect 30-60 minutes on CPU. RECORD THE WALL-CLOCK TIME.
baseline:
	@echo "Starting baseline run at $$(date)"
	python -m samsung_prism.eval.run_mteb --model e5-base-v2 --mode baseline --out $(OUT)/baseline
	@echo "Finished at $$(date)"

# Full pipeline. Produces appsretrieval_results.json for the Release asset.
eval:
	@echo "Starting eval run at $$(date)"
	python -m samsung_prism.eval.run_mteb --config $(CONFIG) --out $(OUT)/samsung_prism
	@echo "Finished at $$(date)"

# Every pipeline stage must earn its place in this table.
ablate:
	python -m samsung_prism.eval.ablate --config $(CONFIG) --out $(OUT)/ablation

# Build or incrementally update the index for a repository.
#   make index REPO=../some-js-repo VERSION=HEAD
index:
	python -m samsung_prism.indexing.build --repo $(REPO) --version $(VERSION) --config $(CONFIG)

demo:
	python -m samsung_prism.api.server --config $(CONFIG) &
	cd src/web && npm run dev

docker:
	docker compose up --build

freeze:
	pip freeze > requirements.lock.txt
	@echo "Wrote requirements.lock.txt - commit this."

clean:
	rm -rf $(OUT) .pytest_cache **/__pycache__ .ruff_cache
	@echo "Caches cleared. Index and model caches left intact."

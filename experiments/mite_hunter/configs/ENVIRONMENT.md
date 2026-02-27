# Environment Setup (MITE-Hunter Evaluation)

## Option A: Isolated Python environment for tracking/tooling helpers

From repo root:

```bash
python3 -m venv .venv-mitehunter
source .venv-mitehunter/bin/activate
python -m pip install --upgrade pip
```

Optional MLflow support:

```bash
python -m pip install -r experiments/mite_hunter/requirements-mlflow.txt
```

## Option B: No Python env (tool-only testing)
If you only run MITE-Hunter scripts directly, you can skip Python env creation and only maintain run logs in git.

## Notes
- Keep candidate tool binaries/scripts outside tracked source when possible.
- Store large outputs in `experiments/mite_hunter/outputs/` (gitignored).
- Record exact tool version and install source in each run log.

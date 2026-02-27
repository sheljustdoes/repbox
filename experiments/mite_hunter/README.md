# MITE-Hunter Evaluation Workspace

This workspace is for isolated experimentation with MITE-Hunter as a candidate replacement in the RepBox tool policy matrix.

## Goals
- Validate installability and execution on local laptop hardware.
- Record reproducible run evidence for matrix decisions.
- Compare behavior against baseline expectations for MITE-focused detection.

## Directory layout
- `configs/`: environment and configuration notes.
- `scripts/`: repeatable run commands.
- `run_logs/`: one markdown log per run.
- `outputs/`: local run outputs (gitignored).
- `tmp/`: temporary files (gitignored).
- `requirements-mlflow.txt`: optional experiment tracking dependencies.

## Suggested workflow
1. Place MITE-Hunter source/scripts under `tmp/` or a local tools path outside repo.
2. Configure local environment using `configs/ENVIRONMENT.md`.
3. Execute `scripts/run_mite_hunter_eval.sh`.
4. Copy run details into a new file in `run_logs/`.
5. Update `docs/process/tool_policy_matrix.md` with decision-impact notes.

## Tracking modes

### A) Git-first tracking (recommended minimum)
- Duplicate `run_logs/RUN-000-template.md` for each run.
- Commit only docs/config/run log updates and small summary artifacts.
- Keep large outputs in `outputs/` (gitignored).

### B) Git + MLflow tracking (optional)
1. Activate environment and install optional dependencies from `requirements-mlflow.txt`.
2. Start local MLflow UI:
	- `bash experiments/mite_hunter/scripts/start_mlflow_ui.sh`
3. Log parameters/metrics/artifact pointers from each run.
4. Keep the markdown run logs as the canonical decision record in git.

## Branching
Use this branch for experimentation:
- `exp/mite-hunter-eval`

Merge to `master` only process/docs changes you want to keep.

#!/usr/bin/env bash
set -euo pipefail

# Starts local MLflow UI scoped to this experiment folder.
# Usage:
#   bash experiments/mite_hunter/scripts/start_mlflow_ui.sh

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
MLRUNS_DIR="$ROOT_DIR/.mlruns"

mkdir -p "$MLRUNS_DIR"

echo "[INFO] Starting MLflow UI"
echo "[INFO] Tracking URI: file://$MLRUNS_DIR"
echo "[INFO] Open: http://127.0.0.1:5001"

MLFLOW_TRACKING_URI="file://$MLRUNS_DIR" mlflow ui --host 127.0.0.1 --port 5001

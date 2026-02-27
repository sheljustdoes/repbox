#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash experiments/mite_hunter/scripts/run_mite_hunter_eval.sh \
#     MITE-Hunter \
#     v11-2017 \
#     athal_chr4_tair10 \
#     miteFinder/miteFinder \
#     repbox_config.txt \
#     4 \
#     8192 \
#     7200 \
#     experiments/mite_hunter/outputs/run-001 \
#     -- \
#     perl /path/to/MITE_Hunter_manager.pl -i /path/to/input.fa -g all -S 12345678 -c 2 -n 10 -P 0 -o experiments/mite_hunter/outputs/run-001/raw

if [[ $# -lt 10 ]]; then
  echo "Usage: $0 <tool_name> <tool_version> <dataset_id> <policy_matrix_row> <config_path_or_NA> <threads> <memory_limit_mb> <timeout_seconds> <output_dir> -- <command ...>"
  exit 2
fi

TOOL_NAME="$1"
TOOL_VERSION="$2"
DATASET_ID="$3"
POLICY_MATRIX_ROW="$4"
CONFIG_PATH="$5"
THREADS="$6"
MEMORY_LIMIT_MB="$7"
TIMEOUT_SECONDS="$8"
OUT_DIR="$9"
shift 9

if [[ "${1:-}" != "--" ]]; then
  echo "Missing '--' separator before command"
  exit 2
fi
shift

if [[ $# -eq 0 ]]; then
  echo "No command provided after '--'"
  exit 2
fi

COMMAND=("$@")

mkdir -p "$OUT_DIR"
mkdir -p "$OUT_DIR/raw"
mkdir -p "$OUT_DIR/processed"
mkdir -p "$OUT_DIR/logs"

START_TS="$(date +%Y-%m-%dT%H:%M:%S)"
START_EPOCH="$(date +%s)"
STDOUT_LOG="$OUT_DIR/logs/stdout.log"
STDERR_LOG="$OUT_DIR/logs/stderr.log"
TIME_LOG="$OUT_DIR/logs/time.log"

CONFIG_HASH="N/A"
if [[ "$CONFIG_PATH" != "N/A" && -f "$CONFIG_PATH" ]]; then
  CONFIG_HASH="$(shasum -a 256 "$CONFIG_PATH" | awk '{print $1}')"
fi

echo "[INFO] Starting tracked evaluation"
echo "[INFO] tool_name=$TOOL_NAME"
echo "[INFO] tool_version=$TOOL_VERSION"
echo "[INFO] dataset_id=$DATASET_ID"
echo "[INFO] output_dir=$OUT_DIR"
echo "[INFO] command=${COMMAND[*]}"

set +e
/usr/bin/time -l "${COMMAND[@]}" >"$STDOUT_LOG" 2>"$STDERR_LOG"
EXIT_CODE=$?
set -e

cp "$STDERR_LOG" "$TIME_LOG"

END_EPOCH="$(date +%s)"
ELAPSED="$((END_EPOCH - START_EPOCH))"

MAX_RSS_RAW="$(grep -i 'maximum resident set size' "$TIME_LOG" | awk '{print $1}' | tail -n 1 || true)"
if [[ -z "$MAX_RSS_RAW" ]]; then
  PEAK_MEMORY_MB="N/A"
else
  PEAK_MEMORY_MB="$(awk -v rss="$MAX_RSS_RAW" 'BEGIN { printf "%.2f", rss/1024/1024 }')"
fi

RUN_STATUS="FAIL"
if [[ "$EXIT_CODE" -eq 0 ]]; then
  RUN_STATUS="PASS"
fi

cat > "$OUT_DIR/run_metrics.json" <<EOF
{
  "parameters": {
    "tool_name": "$TOOL_NAME",
    "tool_version": "$TOOL_VERSION",
    "dataset_id": "$DATASET_ID",
    "config_hash": "$CONFIG_HASH",
    "threads": "$THREADS",
    "memory_limit": "$MEMORY_LIMIT_MB",
    "timeout": "$TIMEOUT_SECONDS",
    "policy_matrix_row": "$POLICY_MATRIX_ROW"
  },
  "metrics": {
    "wall_clock_seconds": $ELAPSED,
    "peak_memory_mb": "$PEAK_MEMORY_MB",
    "num_elements_found": "N/A",
    "num_families": "N/A",
    "overlap_with_annotation": "N/A",
    "precision_recall_if_annotated": "N/A",
    "exit_code": $EXIT_CODE
  },
  "artifacts": {
    "raw_output": "$OUT_DIR/raw",
    "processed_bed_gff": "$OUT_DIR/processed",
    "summary_stats": "$OUT_DIR/run_metrics.json",
    "stdout_stderr_logs": "$OUT_DIR/logs"
  },
  "run": {
    "start_time": "$START_TS",
    "status": "$RUN_STATUS",
    "command": "${COMMAND[*]}"
  }
}
EOF

cat > "$OUT_DIR/artifacts_manifest.txt" <<EOF
raw_output=$OUT_DIR/raw
processed_bed_gff=$OUT_DIR/processed
summary_stats=$OUT_DIR/run_metrics.json
stdout_log=$STDOUT_LOG
stderr_log=$STDERR_LOG
EOF

echo "[INFO] Finished. exit_code=$EXIT_CODE wall_clock_seconds=$ELAPSED peak_memory_mb=$PEAK_MEMORY_MB"
echo "[INFO] Metrics file: $OUT_DIR/run_metrics.json"

exit "$EXIT_CODE"

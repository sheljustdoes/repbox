#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   bash experiments/mite_hunter/scripts/run_mite_hunter_eval.sh \
#     /path/to/mite_hunter_main_script \
#     /path/to/input.fa \
#     experiments/mite_hunter/outputs/run-001

MITE_HUNTER_MAIN="${1:-}"
INPUT_FASTA="${2:-}"
OUT_DIR="${3:-}"

if [[ -z "$MITE_HUNTER_MAIN" || -z "$INPUT_FASTA" || -z "$OUT_DIR" ]]; then
  echo "Usage: $0 <mite_hunter_main_script> <input_fasta> <output_dir>"
  exit 2
fi

if [[ ! -f "$MITE_HUNTER_MAIN" ]]; then
  echo "MITE-Hunter script not found: $MITE_HUNTER_MAIN"
  exit 2
fi

if [[ ! -f "$INPUT_FASTA" ]]; then
  echo "Input FASTA not found: $INPUT_FASTA"
  exit 2
fi

mkdir -p "$OUT_DIR"

START_TS="$(date +%Y-%m-%dT%H:%M:%S)"
START_EPOCH="$(date +%s)"

echo "[INFO] Starting MITE-Hunter evaluation"
echo "[INFO] Start: $START_TS"
echo "[INFO] Script: $MITE_HUNTER_MAIN"
echo "[INFO] Input:  $INPUT_FASTA"
echo "[INFO] Output: $OUT_DIR"

# Replace with exact MITE-Hunter invocation required by your local install.
# Example placeholder:
# perl "$MITE_HUNTER_MAIN" -i "$INPUT_FASTA" -g all -S 12345678 -c 2 -n 10 -P 0 -o "$OUT_DIR"

END_EPOCH="$(date +%s)"
ELAPSED="$((END_EPOCH - START_EPOCH))"

echo "[INFO] Finished. Elapsed seconds: $ELAPSED"

echo "start_time=$START_TS" > "$OUT_DIR/run_meta.txt"
echo "elapsed_seconds=$ELAPSED" >> "$OUT_DIR/run_meta.txt"
echo "mite_hunter_main=$MITE_HUNTER_MAIN" >> "$OUT_DIR/run_meta.txt"
echo "input_fasta=$INPUT_FASTA" >> "$OUT_DIR/run_meta.txt"

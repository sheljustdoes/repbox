# Tool Evaluation Run Log Template

Purpose: record one validation run in a consistent format so matrix decisions are evidence-based and reproducible.

## 1) Run metadata

- Run ID:
- Date/time (local):
- Evaluator:
- Branch/commit:
- Tool under test:
- Tool role/class (Required / Optional / Candidate replacement):
- Candidate name/version:

## 2) Environment

- OS + architecture:
- Python version:
- CPU/RAM (optional but helpful):
- Install source (conda/pip/source/binary/manual):
- Install notes (include exact command or link):

## 3) Input dataset

- Dataset ID/name:
- Dataset type (tiny smoke / small annotated real data):
- File(s):
- Annotation source (if annotated):
- Rationale for dataset choice:

## 4) Command + config

- Config file used:
- Command executed:
- Key parameters:
- Timeout/resource constraints:

## 5) Execution results

- Exit code:
- Run status (PASS / FAIL / PARTIAL):
- Wall-clock time:
- Peak memory (if available):
- Output artifacts produced:
- Errors/warnings observed:

## 6) Biological sanity signal

- Metric(s) used:
- Result summary:
- Comparison baseline (if any):
- Interpretation (better / similar / worse / inconclusive):

## 7) Decision impact (matrix mapping)

- Current matrix row:
- Suggested policy-state action (keep / replace-trial / optional / deprecate):
- Confidence (high / medium / low):
- Main risks/blockers:
- Required follow-up:

## 8) Reproducibility checklist

- [ ] Dataset path/version recorded
- [ ] Command and parameters recorded
- [ ] Tool version recorded
- [ ] Output location recorded
- [ ] Failures captured with probable cause

## 9) One-run summary

Short narrative (3–6 lines):
- What was tested:
- What happened:
- Why it matters:
- Recommended next action:

---

## Example (abbreviated)

- Run ID: SINE-ALT1-2026-02-27-A
- Tool under test: ExampleSineTool v1.4.2
- Dataset: chr_small_annotated_v1
- Command: `python -m repbox smoke --input data/mini.fa --out tmp_out --legacy-config repbox_config.txt`
- Status: PASS
- Wall-clock: 00:11:42
- Biological signal: Comparable overlap to baseline in SINE-rich region; fewer false positives in one locus.
- Suggested action: replace-trial
- Confidence: medium

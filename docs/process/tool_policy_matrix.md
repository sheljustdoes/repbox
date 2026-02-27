# RepBox Tool Policy Matrix (Draft)

Purpose: define which external tools are required now, optional, candidate-replacement, or deprecated, and drive evidence-based migration decisions.

Status: draft scaffold for discussion; no runtime behavior change.

## 1) Decision states

- **Required**: hard gate for `repbox run` success in current baseline.
- **Optional**: useful capability; missing tool should not block core run path.
- **Candidate replacement**: current tool retained short-term while alternatives are evaluated.
- **Deprecated**: planned removal after replacement is validated.

## 2) Acceptance criteria for any state change

A tool can be promoted/demoted only when all are satisfied:

1. **Installability**: reproducible install path documented for macOS (and Linux if in scope).
2. **Interface stability**: CLI flags/version behavior detectable by adapter checks.
3. **Quality signal**: smoke pass + at least one biological sanity check on a known dataset.
4. **Operational fit**: runtime/resource profile acceptable for intended dataset sizes.
5. **License/redistribution**: compatible with project distribution goals.

## 3) Initial matrix (seeded from current code + recent smoke run)

| Adapter / Config Key | Current status (code) | Policy state (proposed start) | Evidence currently available | Main risk | Minimal next validation |
|---|---|---|---|---|---|
| RepeatModeler / `RepeatModeler` | Core run path adapter in use | Required | `run` depends on it; thread-flag compatibility probing exists | Version/flag variance across installs | Validate modern + legacy binaries with `check`/`smoke` and one reference genome |
| BuildDatabase / `BuildDatabase` | Core run prerequisite in use | Required | `run` explicitly fails if missing/non-exec | Path/version mismatch with RepeatModeler bundle | Validate paired install with RepeatModeler versions in matrix |
| RepeatMasker / `RepeatMasker` | Adapter exists; invoked as optional step | Optional | `run` skips if missing/non-exec | Engine/library environment complexity | Validate optional path + output contract when enabled |
| RepeatClassifier / `RepeatClassifier` | Checked in diagnostics only | Candidate replacement | Present in adapter registry and smoke diagnostics | Unclear modern role vs current pipeline goals | Confirm if still needed in active workflow; define keep/replace/remove decision |
| SINE_Scan / `SineScan` | Checked in diagnostics only | Candidate replacement | Legacy-config referenced; currently failing in smoke on this host | Legacy maintenance status | Benchmark against modern alternatives for SINE detection |
| miteFinder / `miteFinder` | Checked in diagnostics only | Candidate replacement | Legacy-config referenced; currently failing in smoke on this host | Legacy code/toolchain fragility | Benchmark against modern alternatives for MITE detection |
| HelitronScanner / `HelitronScanner` | Checked in diagnostics only | Candidate replacement | Legacy-config referenced; currently failing in smoke on this host | Java/runtime packaging and compatibility | Validate JVM requirements + evaluate alternatives |
| VSEARCH / `VSEARCH` | Checked in diagnostics only | Optional (pending) | Legacy-config referenced; currently failing in smoke on this host | Architecture-specific binary distribution | Confirm where used in active flow before final state |

## 4) What to extract from old stash first (high-value only)

From `stash@{0}`, extract only artifacts that strengthen decision-making:

1. Adapter compatibility logic and tests for RepeatModeler behavior.
2. CLI/tool diagnostics improvements that increase observability (`check`, `smoke`, `smoke-report`).
3. Release/process notes that define promotion gates and versioning expectations.

Avoid extracting unrelated release-note churn or broad README rewrites in the first pass.

## 5) Scope

### In scope (this phase)

1. Define policy state for each adapter (`Required`, `Optional`, `Candidate replacement`, `Deprecated`).
2. Validate core required path on laptop-friendly datasets.
3. Evaluate replacement candidates for SINE/MITE/Helitron with repeatable, compute-bounded tests.
4. Produce decision-ready evidence table (installability, behavior, runtime, memory, biological signal).
5. Update matrix decisions and document rationale.

### Out of scope (this phase)

1. Conda packaging and binary distribution finalization.
2. Large whole-genome/HPC benchmark campaigns.
3. Full manuscript-grade analyses and figure generation.
4. Broad refactor of pipeline architecture unrelated to dependency decisions.

## 6) Numbered plan of action (laptop-first)

1. **Freeze baseline context**
	- Pin baseline to current `master`/`v2.0.0` behavior.
	- Preserve current required tools: RepeatModeler + BuildDatabase.

2. **Define evaluation contract**
	- Finalize metrics and thresholds before testing: install pass/fail, command stability, runtime, memory, biological proxy.
	- Standardize report template for every tool/candidate run.

3. **Prepare canonical datasets**
	- Create tiny smoke FASTA inputs for fast CI-like checks.
	- Add one small real annotated chromosome dataset per TE focus area where feasible.
	- Record dataset provenance and annotation source in docs.

4. **Run baseline observability pass**
	- Run `check`, `smoke`, and `smoke-report` with current config.
	- Capture install source, version probe behavior, and smoke outcomes for each matrix row.

5. **Shortlist replacements by literature + practicality**
	- For SINE, MITE, Helitron: select up to 2 viable alternatives each.
	- Screen candidates for maintenance activity, licensing, and install feasibility on macOS laptop.

6. **Execute candidate mini-benchmarks**
	- Run each candidate on the same small annotated datasets.
	- Capture runtime, peak memory, tool failures, and biological sanity proxy against known annotations.

7. **Decide policy state per adapter**
	- Move each adapter to `keep`, `replace`, `optional`, or `deprecate` with explicit rationale.
	- Flag unresolved rows with blockers and required follow-up evidence.

8. **Stabilize and document decision outcomes**
	- Update this matrix and release/process notes.
	- Convert accepted decisions into backlog tasks for implementation/validation reruns.

## 7) Development requirements

1. **Reproducibility**: every run must include command, config, dataset ID, and timestamp.
2. **Environment clarity**: document local OS/arch, tool versions, and installation source.
3. **Compute guardrails**: no benchmark should exceed agreed laptop limits (time/memory).
4. **Comparability**: candidates must be tested on identical inputs and scoring rules.
5. **Traceability**: each matrix state change must reference concrete evidence.
6. **Non-disruption**: no required-tool downgrade without explicit approval and replacement evidence.

## 8) Definition of done (for this decision phase)

This phase is done only when all are true:

1. Every adapter row has a current policy state and written rationale.
2. Required path (RepeatModeler + BuildDatabase) is validated on defined baseline datasets.
3. SINE/MITE/Helitron candidate evaluations are completed (or explicitly blocked with reason).
4. Evidence table includes installability, interface behavior, runtime/memory, and biological proxy.
5. Unresolved risks and follow-up actions are listed with owners/next step.
6. A clear go/no-go recommendation exists for moving to packaging preparation.

## 9) Success and failure criteria

### Success

1. Required pipeline remains stable and reproducible on laptop-scale validation.
2. At least one defensible path exists for each candidate-replacement class (retain or replace).
3. Decisions are evidence-backed and repeatable by another contributor.
4. Packaging remains intentionally deferred until criteria are met, avoiding premature distribution work.

### Failure

1. Decisions are made without comparable evidence across tools.
2. Required path regresses while evaluating optional/candidate tools.
3. Benchmarks are not reproducible (missing config, dataset, or command records).
4. Candidate tools are selected primarily by convenience despite poor validation signal.
5. Work stalls with ambiguous matrix states and no explicit blocker documentation.

## 10) Packaging decision gate (Conda)

Do not begin conda packaging until all are true:

- Required tools finalized and validated on target platforms.
- Optional tools clearly marked with graceful-degradation behavior.
- Candidate replacements either promoted or explicitly deferred with rationale.
- Environment reproducibility document updated from legacy absolute paths to portable setup.

When gate is met: package Python `repbox` first; then evaluate conda/meta-package strategy for external binaries.

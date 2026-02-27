# RepBox Unified Implementation Plan

Date: 2026-02-27
Status: Historical execution baseline (aligned to released tags `v1.1.0` -> `v1.1.1` -> `v1.2.0`)

## Purpose
Provide one canonical implementation plan that unifies:
- completed v1.1 release commitments,
- completed stabilization patching in the v1.1 line, and
- completed v1.2 gap-closure release planning/execution.

This file is the primary execution reference for sequencing, gates, and release decisions.

## Objective
Deliver a reproducible, benchmarked RepBox roadmap that:
- completes v1.1 hybrid detector commitments for SINE/MITE/Helitron,
- stabilizes the release in v1.1.x,
- then executes v1.2 gap-closure features that address known weak points in whole-genome TE annotation/masking systems.

Note:
- This document remains the canonical planning record for the `v1.1.0` -> `v1.1.1` -> `v1.2.0` release line and its acceptance framework.
- Future forward-looking planning should branch from this baseline into the next scoped line (`v1.3.x`).

## Version milestone definition
- `v2.0.0` is the target functional milestone for this roadmap lineage.
- Criteria for `v2.0.0` intent:
   1. end-to-end RepBox pipeline is reliably usable for core discovery/annotation workflows,
   2. detection quality is driven primarily by novel RepBox-native methods (not only wrappers around external whole-genome pipelines),
   3. reproducibility/benchmark gates are institutionalized in release decisions.
- Earl Grey / EDTA / RepeatMasker remain benchmark and comparison context throughout, but are not the sole basis for declaring milestone completion.

## Planning constraints
- Complete v1.1 scope and quality gates before starting v1.2 feature work.
- Treat Earl Grey, EDTA, and RepeatMasker as one whole-genome annotation/masking bucket baseline.
- Position RepBox as gap-filling and complementary, not as a duplicate of whole-annotation pipelines.

## Scope

### In scope
- Hybrid candidate scoring and confidence outputs.
- Family-level postprocessing and benchmark harness.
- Release quality gates and schema-validated artifacts.
- Post-release gap-closure features (iterative discovery, boundary/nesting, calibration, insertion-dynamics linkage, reproducibility hardening).

### Out of scope (this planning cycle)
- Full deep-learning model training pipeline.
- Web UI.
- Expansion to all TE superfamilies beyond current priority classes.

## Baseline (start state)
- Commands currently available:
   - `repbox run`
   - `repbox check`
   - `repbox version`
   - `repbox fallback-scan`
   - `repbox refine-families`
- Existing outputs:
   - Candidate TSV/JSON/summary from fallback scan.
   - Refined family/member/library/summary outputs from graph refinement.
- Existing quality baseline:
   - Unit tests for CLI, fallback scanner, and refinement.

## Phase roadmap

### Phase 1 — v1.1 core delivery (current release)
Goal: deliver hybrid scoring and reproducible benchmarking for SINE/MITE/Helitron.

#### Milestone 1.1 — Hybrid scoring layer
Deliverables:
- New scoring module under `src/repbox/te/` combining:
   - structural evidence (motif/TIR/polyA/TSD quality),
   - similarity evidence (k-mer/family-neighbor support),
   - context evidence (nestedness/local duplication).
- Output fields:
   - `hybrid_score`
   - `confidence_tier` (`high`, `medium`, `low`)
   - `evidence_flags`
- CLI integration:
   - optional hybrid mode for `fallback-scan` and `refine-families`.

Acceptance criteria:
- Deterministic scoring with stable ordering and fixed-seed behavior.
- No regression in command success behavior for default mode.
- Unit tests covering score bounds, tie-break rules, and tier mapping.

#### Milestone 1.2 — Evaluation harness
Deliverables:
- Benchmark runner/module with:
   - fixed input manifests,
   - class-specific summaries,
   - runtime and memory collection.
- Required artifacts:
   - `metrics_overall.json`
   - `metrics_by_class.tsv`
   - `runtime_profile.tsv`
- Operator documentation for benchmark execution and interpretation.

Acceptance criteria:
- One documented command generates complete benchmark artifacts.
- Metrics schema versioned and validated.
- Re-run reproducibility on same input/tool versions.

#### Milestone 1.3 — Release-readiness quality gates
Deliverables:
- Local/CI quality checks for:
   - test pass,
   - output schema validation,
   - benchmark artifact completeness.
- Release checklist updated with v1.1 gates.

Acceptance criteria:
- End-to-end run from FASTA to refined outputs + metrics completes without manual edits.
- Release notes include baseline vs hybrid delta summary.

Exit criteria for `v1.1.0`:
- CLI supports hybrid mode with deterministic outputs.
- Benchmark command is rerunnable with stable artifacts on fixed inputs.
- Release notes include baseline vs hybrid deltas.

---

### Phase 2 — v1.1.x stabilization
Goal: harden `v1.1.0` before expansion.

#### Scope
- Bug fixes and reliability patches only.
- Documentation, reproducibility, and schema hardening.
- No major architectural expansion.

#### Deliverables
- Defect triage log (critical/high/medium).
- Patch-level release notes template usage from release playbook.
- Reproducibility verification on at least one pinned benchmark manifest.

#### Acceptance criteria
- Critical defects discovered post-`v1.1.0` are resolved, mitigated, or explicitly deferred with rationale.
- Patch release quality checks mirror v1.1 gates for touched components.
- `v1.1.x` artifacts remain schema-compatible (or include migration notes).

Exit criteria:
- Open critical defects from `v1.1.0` are resolved or explicitly deferred.
- Patch release cadence complete (`v1.1.1`, optional `v1.1.2`).

---

### Phase 3 — v1.2 gap-closure (post-release)
Goal: fill known gaps in whole-annotation pipeline systems.

#### Gap-to-workstream mapping

##### WS1 — Iterative discovery + unknown bucket
Gap addressed:
- under-detection of novel/diverged/low-copy candidates.

Deliverables:
- Iterative candidate expansion loop after `fallback-scan`:
   1) seed candidates,
   2) family-aware neighborhood expansion,
   3) profile refresh,
   4) second-pass scan.
- Explicit `unknown_te_candidate` class and handling policy.

Acceptance criteria:
- Recall gains on held-out divergent families versus v1.1 baseline.
- Unknown bucket precision floor documented and monitored.

##### WS2 — Boundary/nested refinement v2
Gap addressed:
- fragmented boundaries, over-merging, and ambiguous nested calls.

Deliverables:
- Boundary refinement stage with local MSA + flank-consistency scoring.
- Parent/child nested-chain inference extension to current graph refinement.
- Per-candidate boundary diagnostics:
   - `boundary_confidence`
   - `flank_consistency`
   - `nested_depth`

Acceptance criteria:
- Lower fragmentation/over-merge rates versus v1.1 baseline.
- Stable nested-chain labels across reruns.

##### WS3 — Calibration + abstain semantics
Gap addressed:
- weak uncertainty comparability across runs/tool settings.

Deliverables:
- Versioned class-specific calibration profiles (SINE/MITE/Helitron).
- Formalized `hybrid_score`, `confidence_tier`, `evidence_flags` semantics.
- Abstain mode for unresolved candidates (`abstained=true`).

Acceptance criteria:
- Confidence calibration report emitted per benchmark run.
- Score drift checks with alert thresholds.

##### WS4 — Insertion-dynamics integration
Gap addressed:
- limited native integration of insertion-tracking assays.

Deliverables:
- Optional adapter for TE display outputs.
- Link layer connecting family calls to dynamics:
   - `family_id`
   - `candidate_id`
   - `frequency_trajectory`
- Ranked candidate output for targeted downstream validation.

Acceptance criteria:
- End-to-end linkage from de novo candidate families to insertion-frequency observations.
- Family-level dynamics summary produced for population experiments.

##### WS5 — Reproducibility hardening and benchmark contracts
Gap addressed:
- dependency/runtime drift and weak portability guarantees.

Deliverables:
- Adapter-level execution manifests (tool versions, params, environment hash).
- Strict artifact contracts and schema fail-fast checks.
- Benchmark command with frozen manifests and explicit schema validation.

Acceptance criteria:
- Same input + same manifest => stable output tables (or documented deterministic tolerance).
- Contract violations fail fast with actionable diagnostics.

#### Sequencing order (approved)
1. `WS5` reproducibility hardening baseline.
2. `WS2` boundary/nested refinement v2.
3. `WS1` iterative discovery + unknown bucket.
4. `WS3` calibration + abstain semantics.
5. `WS4` insertion-dynamics integration.

Proposed new fields/outputs:
- `unknown_te_candidate`, `boundary_confidence`, `flank_consistency`, `nested_depth`,
  `calibration_profile_version`, `abstained`.

Proposed CLI additions:
- `repbox run-hybrid --mode iterative`
- `repbox calibrate-confidence --manifest <manifest.json>`
- `repbox link-insertions --te-display <calls.tsv> --families <refined.tsv>`
- `repbox benchmark --manifest <benchmark_manifest.json> --emit-report`

Exit criteria for `v1.2.0`:
- Demonstrated recovery gains on divergent/low-copy families without unacceptable precision collapse.
- Improved boundary/nesting quality vs v1.1 baseline.
- Calibrated uncertainty outputs and reproducible benchmark manifests.

## Evaluation protocol (applies across phases)

### Data policy
- Use fixed, versioned manifests per TE class.
- Keep tune/eval separation explicit for threshold updates.

### Core metrics
- Candidate-level: precision, recall, F1.
- Family-level: recovery rate, redundancy index.
- Operational: wall-clock runtime, peak memory.

### Comparison matrix
- Minimum comparisons:
   - v1.1 baseline fallback/refinement,
   - hybrid-enabled mode,
   - ablation runs (drop one evidence channel),
   - v1.2 workstream deltas against locked v1.1 baseline.

### Reporting rules
- Report overall and per-class metrics.
- Record command, config, revision, and manifest for every benchmark run.
- Flag incomplete artifact sets as invalid for release decisions.

## Acceptance targets by release line

### v1.1.0
- Functional:
   - hybrid mode available and documented.
   - benchmark runner produces required artifacts.
- Quality:
   - all existing and new tests pass.
   - schema validation passes for required outputs.
- Performance:
   - runtime overhead bounded and documented.
   - at least one TE class improves F1 without catastrophic precision collapse.

### v1.1.x
- No unresolved critical regressions from v1.1.0.
- Patch releases preserve artifact schema compatibility (or document migration).

### v1.2.0
- Gap-closure success criteria met across discovery, boundary quality, calibration, and reproducibility.
- Insertion-dynamics linkage path operational where assay data exists.

## Active milestone calendar (tentative)
- 2026-03-31: `v1.1.0` feature-freeze candidate
- 2026-04-07: `v1.1.0` release decision gate
- 2026-04-30: `v1.1.x` stabilization complete
- 2026-05-05: `v1.2.0` kickoff (post-release gap-closure starts)
- 2026-06-30: `v1.2.0` midpoint review
- 2026-08-15: `v1.2.0` release decision gate

## Decision gates for schedule lock
1. Benchmark dataset readiness for v1.1 gating.
2. Team bandwidth for parallel implementation and validation.
3. Confirm whether to keep `v1.2.0` as one release or split into `v1.2`/`v1.3`.

## Release gate checklist

Before any release tag:
1. Required tests pass.
2. Required benchmark artifacts are complete and schema-valid.
3. Changelog and release notes reflect user-visible deltas.
4. Reproducibility metadata (manifest/config/revision) is attached to benchmark outputs.

## Risk policy
- Do not pull v1.2 scope into v1.1 except critical bug fixes.
- Any pre-`v1.1.0` prototype from v1.2 must be behind explicit opt-in flags.

## Risks and mitigations
- Overfitting thresholds to narrow evaluation sets.
   - Mitigation: enforce held-out manifests and ablation reporting.
- Complexity drift in scoring/refinement logic.
   - Mitigation: modular channel tests and explicit contracts per stage.
- Reduced interpretability from added scoring layers.
   - Mitigation: maintain evidence flags and per-candidate component outputs.
- Schedule slip due to validation bottlenecks.
   - Mitigation: gate reviews at feature-freeze and midpoint milestones.

## Work breakdown summary
1. Complete Phase 1 deliverables and release gates for v1.1.
2. Execute limited-scope stabilization patch cycle.
3. Implement v1.2 workstreams in approved order with benchmark deltas after each workstream.
4. Hold midpoint and release decision gates using recorded metrics and artifact quality.

## Supporting detail docs
- Release operations and templates: `docs/process/releasing.md`
- TE strategy/evidence context: `literature review/te_tooling_landscape_2026.md`, `literature review/evidence_table.md`
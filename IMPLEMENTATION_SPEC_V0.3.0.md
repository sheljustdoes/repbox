# RepBox v0.3.0 Implementation Spec

## 1) Objective
Deliver a Python-first architecture for RepBox that removes Bash-based orchestration, decouples external dependencies behind stable adapters, and establishes a modular foundation for transposable element (TE) class-specific development.

This release focuses on architecture and integration safety rather than novel detection algorithms.

## 2) Non-goals (v0.3.0)
- Replacing all third-party TE tools with native Python implementations.
- Introducing breaking output schema changes for existing baseline workflows.
- Shipping production AI models.

## 3) Product outcomes
By the end of v0.3.0, RepBox should provide:
- A Python CLI entrypoint that orchestrates workflows without Bash scripts.
- A tool adapter layer for external dependencies (RepeatModeler, RepeatMasker, class tools).
- A standardized intermediate artifact contract for module interoperability.
- Class-specific workflow modules with clear extension points.
- Reproducible baseline execution on at least one known dataset.

## 4) Proposed repository structure

```
repbox/
  src/
    repbox/
      cli.py
      config.py
      logging.py
      workflow/
        engine.py
        task.py
        context.py
      adapters/
        base.py
        repeatmodeler.py
        repeatmasker.py
        helitronscanner.py
        mitefinder.py
        sinescan.py
      te/
        ltr/
          pipeline.py
        line/
          pipeline.py
        sine/
          pipeline.py
        tir/
          pipeline.py
        helitron/
          pipeline.py
        mite/
          pipeline.py
      io/
        schema.py
        fasta.py
        gff.py
        tsv.py
      ai/
        scoring_stub.py
  tests/
    unit/
    integration/
  docs/
    architecture.md
```

Notes:
- Existing `main.py` can remain temporarily as a compatibility shim in v0.3.0.
- Migrate incrementally; avoid large one-shot rewrites.

## 5) Architecture design

### 5.1 Workflow engine
A lightweight Python workflow engine coordinates steps as typed tasks.

Responsibilities:
- Topological execution of dependent tasks.
- Retry policy for transient failures.
- Structured logging and per-task runtime metrics.
- Deterministic output directories for reproducibility.

Execution model:
- Default sequential mode for reproducibility.
- Optional bounded parallel mode for independent tasks.

### 5.2 Adapter abstraction
Each external tool is wrapped by a shared adapter interface.

Adapter responsibilities:
- Validate required binaries/inputs.
- Build command arguments.
- Execute subprocess with timeout and captured logs.
- Normalize output metadata into standard result objects.

Required base interface:
- `name()`
- `check_installation()`
- `build_command(params)`
- `run(params, context)`
- `collect_outputs(context)`

### 5.3 TE class modules
Each TE class module owns class-specific orchestration logic while using shared adapters and IO schema.

Module contract:
- `prepare_inputs()`
- `run_detection()`
- `postprocess()`
- `emit_artifacts()`

Initial v0.3.0 behavior:
- Primarily wrappers around external tools and current post-processing logic.
- No requirement for novel algorithmic detection yet.

### 5.4 Artifact and schema contract
Define stable artifact metadata across modules.

Core artifacts:
- FASTA candidates
- GFF annotations
- summary TSV/CSV tables
- run metadata JSON (tool versions, parameters, runtime, checksums)

Contract goals:
- Pipeline stages can be composed and replaced.
- Future native Python detectors can plug in without changing downstream consumers.

## 6) Configuration strategy
Move from ad-hoc global variable loading to explicit typed config.

Config priorities:
1. CLI arguments
2. Project config file (YAML/TOML)
3. Environment variables
4. Defaults

Required config sections:
- Runtime: threads, temp dir, output root, retries, timeouts
- Tool paths: external executable locations
- Workflow selection: TE classes and enabled stages
- Logging: level, file output, structured mode

Backward compatibility:
- Support reading legacy `repbox_config.txt` in v0.3.0 through a compatibility parser.

## 7) CLI specification
Single primary command:
- `repbox run --input <genome.fa> --out <dir> [options]`

Key options:
- `--classes ltr,line,sine,tir,helitron,mite`
- `--threads <n>`
- `--config <path>`
- `--resume`
- `--dry-run`
- `--log-level <level>`

Support commands:
- `repbox check` (tool/install checks)
- `repbox version`

## 8) AI integration path (optional, non-blocking)
Include only an interface/stub in v0.3.0.

v0.3.0 AI deliverable:
- `ai/scoring_stub.py` interface that accepts candidate features and emits confidence scores.
- No AI dependency in default execution path.

Future direction:
- Candidate ranking and annotation suggestion models.
- Explainability fields (feature contributions) in output metadata.

## 9) Testing and validation plan

### 9.1 Unit tests
- Adapter command construction.
- Config parsing and precedence.
- Schema validation for emitted artifacts.

### 9.2 Integration tests
- Smoke run with a small reference input.
- `repbox check` validation path.
- Resume behavior and deterministic output structure.

### 9.3 Reproducibility checks
- Record tool versions and parameters for every run.
- Compare key output counts against historical baseline tolerance.

## 10) Milestones and delivery

### Milestone A: Python orchestration foundation
- Add package structure under `src/repbox`.
- Implement CLI skeleton (`run`, `check`, `version`).
- Add config model and legacy config compatibility.

### Milestone B: Adapter layer
- Implement base adapter and core adapters:
  - RepeatModeler
  - RepeatMasker
  - HelitronScanner
  - miteFinder
  - SINE_Scan
- Centralize subprocess execution and logging.

### Milestone C: TE module boundaries
- Add module scaffolds for LTR/LINE/SINE/TIR/Helitron/MITE.
- Route class execution through shared workflow engine.

### Milestone D: Validation and docs
- Add smoke/integration tests.
- Document architecture and migration notes.
- Confirm one reproducible baseline run.

## 11) Definition of done (v0.3.0)
v0.3.0 is complete when:
- Bash orchestration is no longer required for standard runs.
- Primary execution path is Python CLI-based.
- External tool integrations are encapsulated behind adapters.
- At least one baseline dataset run is reproducible and documented.
- Changelog includes concrete v0.3.0 shipped items.

## 12) Risks and mitigations

Risk: Tool-path/environment fragility across systems.
Mitigation: `repbox check`, explicit config, clear adapter diagnostics.

Risk: Runtime regressions from orchestration rewrite.
Mitigation: baseline smoke tests and output parity checks.

Risk: Scope creep into algorithm replacement.
Mitigation: enforce v0.3.0 non-goals; defer native detectors to v0.4+.

## 13) Immediate next tasks
1. Create `src/repbox` package skeleton and CLI entrypoint.
2. Add typed config + legacy config parser bridge.
3. Implement adapter base and one end-to-end path (RepeatModeler -> RepeatMasker).
4. Add `repbox check` command and baseline smoke test.

## 14) Milestone A status snapshot
Completed in repository scaffold:
- `src/repbox/` package created with `__main__.py` entrypoint.
- `src/repbox/cli.py` implemented with `run`, `check`, and `version` commands.
- `src/repbox/config.py` includes legacy `repbox_config.txt` compatibility parsing.
- `src/repbox/adapters/` includes base adapter abstraction and default tool registry.
- `src/repbox/workflow/` includes minimal task/context/engine scaffold.

Deferred to subsequent milestones:
- Full adapter command execution and normalized output collection.
- TE class module implementations (LTR/LINE/SINE/TIR/Helitron/MITE).
- Integration tests and baseline parity validation harness.

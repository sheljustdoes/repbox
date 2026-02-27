# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Environment and dependency setup improvements.
- Baseline run revalidation and reproducibility checks.
- Early reliability and usability improvements for active development.

## [2.0.0] - 2026-02-27

### Added
- Python package foundation under `src/repbox/` for the modern CLI baseline.
- New CLI command surface with `run`, `check`, and `version` commands.
- New CLI `smoke` command for lightweight environment/input validation and report output.
- New CLI `smoke-report` command to summarize and evaluate `smoke_report.txt` files.
- New legacy setup reference doc: `docs/legacy/thesis_environment_setup.md`.
- Legacy config compatibility loader for `repbox_config.txt`.
- Initial adapter and workflow engine stubs for phased migration.
- Shared adapter command runner (`run_command`) with timeout and structured results.
- Concrete `RepeatModelerAdapter` with BuildDatabase + RepeatModeler command construction and execution.
- Concrete `RepeatMaskerAdapter` with command construction and execution support.

### Changed
- `repbox run` now executes the RepeatModeler adapter path (Milestone B foundation behavior).
- `repbox run` now performs an optional RepeatMasker step after successful RepeatModeler execution when configured.
- `repbox run` and `repbox smoke` now emit actionable tool diagnostics (failing tool names, paths, and hints).
- `repbox smoke-report` now supports `--json` output for machine-readable summaries.
- `repbox smoke` now writes `schema_version=1`, and `repbox smoke-report` validates schema compatibility.
- Version metadata now targets stable `2.0.0`.
- README versioning and command coverage notes now reflect the current platform state.
- README was overhauled for modern onboarding, CLI usage, and research roadmap clarity.

### Notes
- `2.0.0` is the stable platform-reset baseline for current development.
- Prior `0.x` entries are retained as historical modernization intent references.

## [0.2.0] - 2026-02-26

### Added
- Release workflow documentation in `docs/process/releasing.md`.
- Reusable GitHub release note drafts in `docs/process/release_notes_templates.md`.

### Changed
- Updated `README.md` with project status, versioning policy, and release guidance.
- Standardized changelog structure for ongoing semantic versioning.

### Notes
- Project reactivation milestone after an extended maintenance gap.
- No functional pipeline code changes in this release.

## [0.1.0] - 2026-02-26

### Added
- Unified Python pipeline (`main.py`) that invokes original workflow tools via subprocess.
- Configuration-driven dependency paths using `repbox_config.txt`.
- Included helper assets/dependencies under `included/` for easier setup.

### Changed
- Migrated original bash-driven process into a Python orchestration workflow.
- Updated installation instructions to align with the Python-based pipeline flow.

### Notes
- This is the first formal tagged release of the thesis-era codebase.


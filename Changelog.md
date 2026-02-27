# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Note:
- Latest live release baseline is `v1.2.0`.
- Historical line mapping:
	- `0.1.0` -> `1.0.0`
	- `0.2.0` -> `1.0.1`

## [Unreleased]

### Added
- Unified implementation plan in `IMPLEMENTATION_PLAN_UNIFIED.md` documenting v1.1 delivery, v1.1 stabilization, and v1.2 gap-closure sequencing.
- Consolidated release playbook in `docs/process/releasing.md` now includes workflow, release note templates, and active 2026 phased schedule.
- Python package scaffold under `src/repbox/` for the historical Milestone A modernization phase.
- New CLI scaffold with `run`, `check`, and `version` commands.
- Legacy config compatibility loader for `repbox_config.txt`.
- Initial adapter and workflow engine stubs for phased migration.
- Shared adapter command runner (`run_command`) with timeout and structured results.
- Concrete `RepeatModelerAdapter` with BuildDatabase + RepeatModeler command construction and execution.
- RepeatModeler capability probing to detect and select modern `-threads` or legacy `-pa`.
- Unit test coverage for RepeatModeler adapter probing and CLI check/run behaviors.
- Python fallback TE scanner (`repbox fallback-scan`) for MITE/SINE/Helitron candidate discovery when legacy edge tools are unavailable.
- Tooling landscape assessment document for 2022-2026 dependency strategy in `literature review/te_tooling_landscape_2026.md`.
- Nested-aware graph family refinement prototype (`repbox refine-families`) for clustering SINE/MITE/Helitron candidates into representative families.
- Unit tests for fallback scanner and graph refinement prototype.

### Changed
- `repbox run` now executes the RepeatModeler adapter path (Milestone B foundation behavior).
- `repbox check` now validates executability and reports RepeatModeler version/compatibility mode.
- `README.md` now separates current compatibility guidance from historical thesis-era dependency pins.
- Superseded standalone implementation spec files removed in favor of `IMPLEMENTATION_PLAN_UNIFIED.md` as single source of planning truth.
- Version milestone policy updated: `v2.0.0` is now the explicit functional target where RepBox is expected to be primarily driven by novel in-project element-identification methods.
- Release naming records aligned to tagged sequence `v1.1.0` -> `v1.1.1` -> `v1.2.0`.

### Planned
- Environment and dependency setup improvements.
- Baseline run revalidation and reproducibility checks.
- Early reliability and usability improvements for active development.

## [1.2.0] - 2026-02-27

### Notes
- Current live baseline tag.
- Feature-line minor release following the `v1.1.x` stabilization sequence.

## [1.1.1] - 2026-02-27

### Notes
- Stabilization patch release in the `v1.1.x` series.
- Naming and ordering preserved as `v1.1.0` -> `v1.1.1`.

## [1.1.0] - 2026-02-27

### Notes
- Initial `v1.1` minor release tag in the current roadmap lineage.
- Base release for follow-on stabilization and `v1.2.0` progression.

## [1.0.3] - 2026-02-27

### Notes
- Current live baseline tag.
- No additional functional deltas beyond prior `1.0.x` records are documented in this file.

## [1.0.2] - 2026-02-27

### Notes
- Version-line/tag normalization step in the `1.0.x` series.
- No new functional pipeline behavior documented.

## [1.0.1] - 2026-02-26

### Added
- Release workflow documentation in `docs/process/releasing.md`.
- Reusable GitHub release note drafts (later consolidated into `docs/process/releasing.md`).

### Changed
- Updated `README.md` with project status, versioning policy, and release guidance.
- Standardized changelog structure for ongoing semantic versioning.

### Notes
- Project reactivation milestone after an extended maintenance gap.
- No functional pipeline code changes in this release.

## [1.0.0] - 2026-02-26

### Added
- Unified Python pipeline (`main.py`) that invokes original workflow tools via subprocess.
- Configuration-driven dependency paths using `repbox_config.txt`.
- Included helper assets/dependencies under `included/` for easier setup.

### Changed
- Migrated original bash-driven process into a Python orchestration workflow.
- Updated installation instructions to align with the Python-based pipeline flow.

### Notes
- This is the first formal tagged release of the thesis-era codebase.

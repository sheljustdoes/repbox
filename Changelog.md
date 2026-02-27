# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project uses [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Python package scaffold under `src/repbox/` for v0.3.0 Milestone A.
- New CLI scaffold with `run`, `check`, and `version` commands.
- New CLI `smoke` command for lightweight environment/input validation and report output.
- Legacy config compatibility loader for `repbox_config.txt`.
- Initial adapter and workflow engine stubs for phased migration.
- Shared adapter command runner (`run_command`) with timeout and structured results.
- Concrete `RepeatModelerAdapter` with BuildDatabase + RepeatModeler command construction and execution.
- Concrete `RepeatMaskerAdapter` with command construction and execution support.

### Changed
- `repbox run` now executes the RepeatModeler adapter path (Milestone B foundation behavior).
- `repbox run` now performs an optional RepeatMasker step after successful RepeatModeler execution when configured.

### Planned
- Environment and dependency setup improvements.
- Baseline run revalidation and reproducibility checks.
- Early reliability and usability improvements for active development.

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


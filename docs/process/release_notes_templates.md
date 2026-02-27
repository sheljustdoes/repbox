# RepBox Release Notes Templates

Use the sections below as copy-paste drafts in GitHub Releases.

## v0.1.0 — Historical baseline release

### Summary
This is the first formal, versioned release of RepBox.

RepBox was originally developed as part of PhD thesis work and has been publicly available, but without GitHub release tags. This release establishes a stable historical baseline for citation, reproducibility, and future development.

### What’s included
- Python-based pipeline orchestration in `main.py`.
- Subprocess execution of core repeat annotation/discovery tools.
- Configuration-driven tool path setup through `repbox_config.txt`.
- Included helper resources and dependency assets in `included/`.

### Notes
- This release represents thesis-era functionality as a baseline snapshot.
- RepBox is currently in `0.x` development status while modernization and validation continue.

### Upgrade / migration
- No migration required for existing users; this is a formalization of the existing codebase into versioned release history.

---

## v0.2.0 — Project revival release

### Summary
RepBox development is now active again after an extended maintenance gap.

This release focuses on project reactivation and maintainability improvements while preserving core workflow behavior.

No functional pipeline code changes are included in this release.

### Highlights
- Formal release process and versioning documentation added.
- Changelog structure standardized for ongoing development.
- Development/release guidance improved in README and release docs.
- Foundation prepared for upcoming reliability and usability improvements.
- No changes to pipeline execution logic in `main.py`.

### Notes
- This release is intentionally non-breaking and focused on process/documentation maturity.
- Functional enhancements and broader compatibility updates will continue in subsequent `0.x` releases.
- This tag is a project reactivation milestone rather than a feature/code update.

### Next priorities
- Revalidate end-to-end runs on baseline datasets.
- Improve environment and dependency setup ergonomics.
- Add automated checks to support safer future releases.

---

## v0.3.0 — Python-first foundation (Milestone A)

### Summary
This release establishes the first Python-first foundation for RepBox modernization.

v0.3.0 introduces package scaffolding, a new CLI surface, legacy config compatibility, and initial adapter/workflow abstractions to support migration away from Bash-heavy orchestration.

### What’s included
- New Python package scaffold under `src/repbox/`.
- New CLI scaffold with commands:
	- `repbox version`
	- `repbox check`
	- `repbox run`
- Legacy configuration compatibility loader for `repbox_config.txt`.
- Initial adapter abstractions and tool registry for external dependency checks.
- Initial workflow scaffolding (`Task`, `RunContext`, sequential workflow engine).
- Packaging metadata via `pyproject.toml` and editable install support.

### Behavior notes
- This is a foundation release; full legacy pipeline behavior has not yet been migrated into the new CLI execution path.
- `repbox check` currently validates configured tool paths and reports missing tools.
- In this repository state, legacy paths in `repbox_config.txt` are machine-specific and may report missing on new systems until updated.

### Compatibility
- Non-breaking release focused on architecture and migration readiness.
- Existing legacy script entrypoints remain available for the current workflow while migration continues.

### Next steps
- Milestone B: implement real subprocess execution in adapters for core tools (starting with RepeatModeler and RepeatMasker).
- Milestone C: introduce TE class module boundaries (LTR/LINE/SINE/TIR/Helitron/MITE).
- Add baseline parity and reproducibility validation harness.

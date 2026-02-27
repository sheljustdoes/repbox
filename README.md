# RepBox

RepBox is a transposable element discovery and annotation workflow originally created during PhD thesis research and now actively modernized as a Python-first CLI platform.

## Current status
- Modernized CLI scaffold is active under `src/repbox/`.
- Current commands: `run`, `check`, `smoke`, `smoke-report`, `version`.
- Adapter-based integration is in place for RepeatModeler/RepeatMasker paths.
- Release target is `v2.0.0` as a stable platform baseline.

## Quick start

From repository root:

```bash
python -m pip install -e .
python -m repbox version
python -m repbox check --legacy-config repbox_config.txt
python -m repbox smoke --input <genome.fa> --out <output_dir>
python -m repbox smoke-report --report <output_dir>/smoke_report.txt --json
```

Notes:
- `check` and `smoke` can return non-zero when legacy external tool paths are missing.
- `smoke-report` supports human-readable and `--json` machine-readable output.

## CLI commands

- `repbox version`: print package version.
- `repbox check --legacy-config <path>`: validate configured external tools.
- `repbox run --input <fa> --out <dir> [--threads N] [--engine ncbi]`: run scaffolded pipeline path.
- `repbox smoke --input <fa> --out <dir>`: write `smoke_report.txt` with tool diagnostics.
- `repbox smoke-report --report <path> [--json]`: summarize or parse smoke reports.

## Versioning and release model

- RepBox uses Semantic Versioning (`MAJOR.MINOR.PATCH`).
- `v2.0.0` is the baseline milestone for the modernized CLI contract and release workflow.
- Ongoing work continues as small PR slices merged to `master`.

## Development workflow

1. Create a focused branch (`feat/*`, `fix/*`, `docs/*`, `test/*`).
2. Make scoped changes and run local validation.
3. Update `Changelog.md` (`Unreleased`) for user-visible changes.
4. Open PR to `master`, merge when checks pass.

## Documentation map

- Changelog: `Changelog.md`
- Release workflow: `docs/process/releasing.md`
- Release notes templates: `docs/process/release_notes_templates.md`
- GitHub project playbook: `docs/process/github_project_playbook.md`
- Legacy implementation spec: `docs/legacy/IMPLEMENTATION_SPEC_V0.3.0.md`
- Legacy thesis environment setup: `docs/legacy/thesis_environment_setup.md`

## Research roadmap

`v2.0.0` marks software baseline stabilization. Paper-oriented milestones can build on top:

- `v2.1`: reproducibility benchmarks and baseline comparisons.
- `v2.2`: broader biological validation datasets and analysis.
- `v2.3`: manuscript-aligned figures, tables, and methods narrative.
- `v2.4`: submission-ready reproducibility package.

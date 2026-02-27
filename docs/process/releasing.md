# Releasing RepBox

This document defines the release workflow, versioning policy, templates, and active schedule baseline.

## Versioning policy
RepBox uses Semantic Versioning:
- `MAJOR`: breaking behavior/configuration changes or milestone-level functional transitions.
- `MINOR`: backward-compatible features/improvements.
- `PATCH`: backward-compatible fixes and small corrections.

Current naming convention and release state:
- Latest live release baseline: `v1.2.0`.
- Confirmed tagged sequence under current convention: `v1.1.0` -> `v1.1.1` -> `v1.2.0`.
- Active maintenance line: `v1.2.x` (patches as needed).
- Next feature line: `v1.3.x` (to be scoped after `v1.2.x` stabilization).

Major-version milestone policy:
- `v2.0.0` remains the planned functional milestone where RepBox is considered fully operational with predominantly novel RepBox-native element-identification methods.
- External whole-genome systems (Earl Grey / EDTA / RepeatMasker bucket) remain reference/benchmark baselines, not the defining core of `v2.0.0` capability.
- The `v1.x` series is the transition line leading into `v2.0.0`.

## Release checklist

### 1) Prepare the release
- Ensure `main` is in a releasable state.
- Confirm core pipeline execution still works for at least one baseline dataset.
- Update `Changelog.md`:
  - Move relevant items from `Unreleased` into a new version heading.
  - Add release date in `YYYY-MM-DD` format.

### 2) Create the tag
From repository root:

```bash
git checkout main
git pull --ff-only
git tag -a vX.Y.Z -m "RepBox vX.Y.Z"
git push origin vX.Y.Z
```

### 3) Publish GitHub release
- Open GitHub -> Releases -> Draft new release.
- Choose tag `vX.Y.Z`.
- Title: `RepBox vX.Y.Z`.
- Copy the matching section from `Changelog.md` into release notes.
- Publish release.

### 4) Post-release
- Re-open `Changelog.md` with a fresh `## [Unreleased]` section if needed.
- Continue logging all user-visible changes under `Unreleased`.

## 2026 release schedule

Status: Updated to reflect completed `v1.1.0` -> `v1.1.1` -> `v1.2.0` line.

### Decision log
- 2026-02-26: Tentative milestone anchors accepted as the active planning schedule.
- 2026-02-27: Tags `v1.1.0`, `v1.1.1`, and `v1.2.0` published under semantic naming.

### Scheduling principle
- Keep patch work within the active maintenance line (`v1.2.x`).
- Scope next additive feature set into the next minor line (`v1.3.x`).
- Reserve `v2.0.0` for milestone-level completion and/or intentional breaking transitions.

### Milestone calendar (historical + forward)
- 2026-02-27: `v1.1.0` tagged
- 2026-02-27: `v1.1.1` tagged
- 2026-02-27: `v1.2.0` tagged
- TBD: `v1.2.x` stabilization complete
- TBD: `v1.3.0` release decision gate

### Minimal risk policy
- Do not pull `v1.3` features into `v1.2.x` unless they are critical bug fixes.
- Any prototype merged ahead of a release should be behind explicit opt-in flags.

## Release notes templates

### Minor release template (`v1.Y.0`)

#### Summary
This is a minor feature release of RepBox.

This release introduces backward-compatible functionality and/or significant workflow improvements while preserving existing usage contracts.

#### What’s included
- New user-visible capabilities (commands/options/outputs).
- Backward-compatible behavior changes and performance improvements.
- Any documentation updates required to use new features.

#### Notes
- No breaking user-facing configuration or command contracts.
- Release is suitable for users upgrading from prior `v1.x` versions.

#### Upgrade / migration
- No required migration expected for existing `v1.x` users.

---

### Patch release template (`v1.Y.Z`)

#### Summary
This is a patch release focused on stabilization and correction.

This release focuses on bug fixes, reproducibility hardening, and documentation corrections while preserving behavior.

#### Highlights
- Defect fixes and reliability improvements.
- Documentation and process updates.
- Any behavior changes are backward-compatible.

#### Notes
- This release is intentionally non-breaking.
- If any output formatting changed, migration notes are provided.

#### Next priorities
- Continue patching only if defects remain.
- Roll larger enhancements into the next minor release.

---

### Major release template (`v2.0.0` and beyond)

#### Summary
This is a major release that marks a milestone-level capability transition.

`v2.0.0` indicates either breaking changes or milestone-level functional completion requiring explicit upgrade communication.

#### What’s included
- Breaking/changed command or configuration contracts (if any).
- New milestone capabilities that materially change user workflows.
- Migration tooling or compatibility shims where feasible.

#### Behavior notes
- Clearly document deprecated/removed paths and replacement workflows.
- Include explicit compatibility notes and known limitations.

#### Compatibility
- Expect migration action for users if interfaces changed.

#### Next steps
- Verify migration guide end-to-end before tagging.
- Ensure release notes have a dedicated "Breaking changes" section.

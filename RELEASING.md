# Releasing RepBox

This document defines a lightweight release workflow for this repository.

## Versioning policy
RepBox uses Semantic Versioning:
- `MAJOR`: breaking behavior/configuration changes.
- `MINOR`: backward-compatible features/improvements.
- `PATCH`: backward-compatible fixes and small corrections.

Until workflow and configuration are stabilized, stay in the `0.x.y` range.

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
- Open GitHub → Releases → Draft new release.
- Choose tag `vX.Y.Z`.
- Title: `RepBox vX.Y.Z`.
- Copy the matching section from `Changelog.md` into release notes.
- Publish release.

### 4) Post-release
- Re-open `Changelog.md` with a fresh `## [Unreleased]` section if needed.
- Continue logging all user-visible changes under `Unreleased`.

## First historical release recommendation
Use `v0.1.0` as the first formal tag to represent the current thesis-era pipeline baseline.

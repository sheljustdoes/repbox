# Releasing RepBox

This document defines the release workflow and versioning policy for this repository.

## Versioning policy
RepBox uses Semantic Versioning:
- `MAJOR`: breaking behavior/configuration changes.
- `MINOR`: backward-compatible features/improvements.
- `PATCH`: backward-compatible fixes and small corrections.

Historical note:
- Early release intent used `0.x` framing for modernization work.
- Published release history now includes `v1.x` transition tags and `v2.0.0` as the stable platform reset baseline.
- Do not rewrite published tags; keep narrative consistency in release notes and changelog entries.

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

## Historical labeling guidance
When referring to historical baseline work in release notes, describe semantic intent in text rather than renaming published tags.

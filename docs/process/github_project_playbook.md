# GitHub Project Playbook (RepBox)

This playbook sets up a lightweight project management system for paced, sustainable development.

## 1) Create the project
1. Go to GitHub -> your profile/org -> Projects -> New Project.
2. Choose **Board** layout.
3. Name it: **RepBox Roadmap**.
4. Link repository: `sheljustdoes/repbox`.

## 2) Configure fields
Add these custom fields in the project:
- `Status` (single select): Backlog, Ready, In Progress, In Review, Done
- `Priority` (single select): P0, P1, P2
- `Size` (single select): XS, S, M, L, XL
- `Area` (single select): CLI, Config, Adapters, Workflow, MITE, SINE, Docs, Tests
- `Target Release` (text): e.g. v0.4.0
- `Start Date` (date)
- `Due Date` (date)

## 3) Configure views
Create these views:
- **Roadmap** (table): grouped by `Target Release`, sorted by `Priority`
- **Current Cycle** (board): grouped by `Status`, filtered to current release
- **MITE Track** (table): filter `Area = MITE`
- **SINE Track** (table): filter `Area = SINE`

## 4) Automation rules
Set built-in workflows:
- Item added to project -> set `Status = Backlog`
- PR opened and linked to item -> set `Status = In Review`
- PR merged -> set `Status = Done`

## 5) Cadence recommendation
- Weekly planning (30 min): pick 3-5 `Ready` items only.
- Mid-week checkpoint (15 min): unblock and de-scope as needed.
- Weekly closeout (20 min): move done items, update changelog, decide release cut.

## 6) Work-in-progress limits
- Max 2 items in `In Progress` at a time.
- No new work starts if `In Review` has more than 3 open items.

## 7) Definition of Ready
An item is `Ready` only if it has:
- Clear problem statement
- Explicit acceptance criteria
- Estimated `Size`
- Assigned `Area`

## 8) Definition of Done
An item is `Done` only if:
- Code merged to main
- Validation run documented
- Relevant docs updated
- `Changelog.md` updated under `Unreleased`

## 9) Starter backlog for next milestone
Suggested first issues:
1. Adapter executor for RepeatModeler (subprocess + logging)
2. Adapter executor for RepeatMasker (subprocess + logging)
3. Shared command runner utility with timeout and structured errors
4. Config migration layer: legacy + future TOML schema
5. Baseline integration smoke test harness

## 10) Release rhythm
- Cut releases every 1-2 weeks when at least 2-3 user-visible improvements are complete.
- Keep release scope narrow and milestone-specific.

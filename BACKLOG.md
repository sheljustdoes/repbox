# Backlog

Standing queue of development work for this project, ordered by priority.
Created 2026-09-22.

**Status:** Shipped and published — v2.0.0 baseline. [BMC Bioinformatics (2023)](https://doi.org/10.1186/s12859-023-05419-5)

---

## P0 — Continuous integration

The v2.0.0 release contract is stable, four test files exist, and nothing runs them
automatically.

- [ ] GitHub Actions workflow: run the test suite on push and pull request across
      Python 3.10–3.12.
- [ ] Wire `repbox check` and `repbox smoke` into CI against a small fixture genome so
      the adapter paths are exercised, not just the pure-Python units.
- [ ] Publish a coverage figure and keep it honest — the external-tool adapters are the
      hard part to cover and should be called out rather than quietly excluded.

## P1 — v2.1: reproducibility benchmarks

Next milestone on the stated research roadmap.

- [ ] Fix a reference dataset and record baseline detection counts and runtimes.
- [ ] Compare against RepeatModeler/RepeatMasker defaults on that same dataset, with the
      comparison method documented rather than asserted.
- [ ] Record hardware, tool versions, and parameters alongside every benchmark number.
- [ ] Add a regression test asserting detection counts do not silently drift between
      releases.

## P2 — Distribution

- [ ] Package for PyPI; the CLI contract has been stable since v2.0.0.
- [ ] Bioconda recipe — this is where the tool's actual users look for it.
- [ ] Pin and document the external tool versions the adapters expect.

## P3 — v2.2 onward

- [ ] Broader biological validation datasets beyond *A. sativa*.
- [ ] Manuscript-aligned figures and methods narrative.
- [ ] Reproducibility package for submission.

## Documentation

- [ ] Usage example that runs start to finish on a small public genome, so a new user can
      confirm a working install in one command.
- [ ] Document exit codes — `check` and `smoke` return non-zero when legacy tool paths are
      missing, which is expected behavior and currently surprises people.
- [ ] Note the relationship between the v2 CLI and the thesis-era workflow the paper
      describes.

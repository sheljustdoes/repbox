# RepBox TE Tooling Landscape (2022 -> 2026)

## Scope
This assessment maps the original RepBox dependency set to current ecosystem status and identifies where RepBox should keep, replace, or provide Python fallback support.

## Legacy tool status snapshot

| TE area | Legacy tool in RepBox | Status signal (post-2022) | Recommendation |
|---|---|---|---|
| De novo library build | RepeatModeler 2.0.1 | Active upstream; 2.0.4 (2022), 2.0.5 (2023), 2.0.6 (2024), 2.0.7 (2025) | Upgrade to 2.0.7 and keep as primary |
| Whole-genome TE annotation/masking pipeline bucket | RepeatMasker 4.1.3-p1 | Active upstream; 4.2.x releases through 2025 (4.2.3) | Keep in same strategic bucket as EDTA/Earl Grey (pipeline/masking context); upgrade to 4.2.3 |
| MITE structural discovery | MITEFinderII | Still maintained; v3.0 (2024) | Keep external path as preferred where available; add Python fallback for degraded environments |
| Helitron structural discovery | HelitronScanner (Java) | Newer strong alternative exists (HELIANO, active through 2025) | Prefer HELIANO where possible; keep HelitronScanner legacy path; add Python fallback |
| SINE structural discovery | SINE_Scan (Perl, thesis-era pin) | No clear active upstream signal from current modernization fetch; often brittle in modern envs | Treat as high-risk legacy dependency; add Python fallback and evaluate replacement via broader pipelines |
| Whole-genome TE annotation/masking pipeline bucket | N/A in legacy RepBox | EDTA 2.2.2 (2024), Earl Grey 7.0.3 (2026) both active | Same bucket as RepeatMasker; use as optional reference/benchmark pipelines, not hard dependency |
| Insertion dynamics / mobilome tracking | N/A in legacy RepBox | TE display sequencing (Genome Biology 2025) enables ultra-sensitive non-reference insertion detection across multiple families | Use as orthogonal validation/monitoring path for evolve-and-resequence or burst experiments; not a replacement for de novo library construction |

## Key ecosystem developments since 2022

1. RepeatModeler/RepeatMasker moved quickly after 2022 with multiple quality and compatibility updates.
2. ARM/macOS usage improved mainly via containerized or conda-based workflows, but fragile edge tools are still common pain points.
3. Helitron discovery has a more modern dedicated option (HELIANO) with active releases and clearer output contracts.
4. Integrated TE pipelines (EDTA, Earl Grey) remain actively maintained and can serve as external validation baselines.
5. Targeted TE insertion assays now provide practical population-scale sensitivity for low-frequency insertion tracking across families.

## Bucket note

- In this review, Earl Grey, EDTA, and RepeatMasker are treated as one operational bucket: whole-genome TE annotation/masking context.
- Class-specific callers (e.g., SINE/Helitron/MITE-focused tools) are treated as a separate bucket for targeted family discovery.

## RepBox modernization decision

1. Keep best-in-class external engines for core de novo + masking (RepeatModeler/RepeatMasker).
2. Reduce single-point failures from edge dependencies by shipping Python fallbacks for MITE/SINE/Helitron candidate discovery.
3. Position fallbacks as "triage-grade candidate generators" for unavailable/broken legacy tools, not full algorithmic equivalence.

## New Python fallback path in this repo

RepBox now includes a Python fallback scanner:

```bash
repbox fallback-scan --input genome.fa --out fallback_out --classes mite,sine,helitron
```

Outputs per selected class:
- `<class>_candidates.tsv`
- `<class>_candidates.fa`
- `<class>_candidates.json`
- `summary.json`

## Notes on scientific intent

- These fallbacks are intentionally conservative heuristics to maintain workflow continuity.
- They are suitable for rapid screening and candidate handoff to downstream curation.
- They should be benchmarked against EDTA/Earl Grey or curated annotations before replacing production-grade structural discovery in published analyses.

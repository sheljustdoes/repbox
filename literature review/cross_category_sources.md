# Sources: Cross-category TE methods and validation

Date: 2026-02-26
Category: Cross-category (multi-family TE discovery, annotation, insertion dynamics, and benchmarking)

## Primary cross-category method papers

1. Mao H, Wang H. 2017.
   SINE_Scan: an efficient tool to discover short interspersed nuclear elements (SINEs) in large-scale genomic datasets.
   Bioinformatics 33(5):743–745.
   DOI: https://doi.org/10.1093/bioinformatics/btw718
   PubMed: https://pubmed.ncbi.nlm.nih.gov/28062442/
   Why used: canonical example of multi-signal evidence fusion (structural hallmarks + transposition signals + copy evidence).

2. Xiong W, He L, Lai J, Dooner HK, Du C. 2014.
   HelitronScanner uncovers a large overlooked cache of Helitron transposons in many plant genomes.
   PNAS 111(28):10263–10268.
   DOI: https://doi.org/10.1073/pnas.1410068111
   Full text: https://www.pnas.org/doi/full/10.1073/pnas.1410068111
   Why used: explicit score-threshold calibration and false-positive estimation paradigm.

3. Li et al. 2024.
   HELIANO paper (Nucleic Acids Research).
   DOI: https://doi.org/10.1093/nar/gkae610
   Full text: https://academic.oup.com/nar/article/52/17/e79/7719972
   Why used: protein-first plus terminal-statistics fusion for class-specific calling.

4. Hu K, Ni P, Xu M, Zou Y, et al. 2024.
   HiTE: a fast and accurate dynamic boundary adjustment approach for full-length transposable element detection and annotation.
   Nature Communications 15(1):5573.
   DOI: https://doi.org/10.1038/s41467-024-49912-8
   PMCID: https://pmc.ncbi.nlm.nih.gov/articles/PMC11219922/
   PMID: https://pubmed.ncbi.nlm.nih.gov/38956036/
   Why used: coarse-to-fine boundary refinement framework spanning multiple TE classes.

5. Vendrell-Mir P, Leduque B, Quadrana L. 2025.
   Ultra-sensitive detection of transposon insertions across multiple families by transposable element display sequencing.
   Genome Biology 26(1):48.
   DOI: https://doi.org/10.1186/s13059-025-03512-x
   PMCID: https://pmc.ncbi.nlm.nih.gov/articles/PMC11887134/
   PMID: https://pubmed.ncbi.nlm.nih.gov/40050910/
   Why used: ultra-sensitive non-reference insertion detection and allele-frequency tracking across multiple TE families in population-scale designs.

6. Baril T, Galbraith J, Hayward A. 2024.
   Earl Grey: A Fully Automated User-Friendly Transposable Element Annotation and Analysis Pipeline.
   Molecular Biology and Evolution 41(4):msae068.
   DOI: https://doi.org/10.1093/molbev/msae068
   PMCID: https://pmc.ncbi.nlm.nih.gov/articles/PMC11003543/
   PMID: https://pubmed.ncbi.nlm.nih.gov/38577785/
   Why used: automated end-to-end TE annotation framework with emphasis on reducing fragmented/overlapping annotations and improving usability.

7. Benson CW, Heringer P, Ou S. 2025.
   Four Strategies for Whole-Genome Annotation of Transposable Elements and Repeats in Maize.
   Cold Spring Harbor Protocols 2025(9):pdb.prot108578.
   DOI: https://doi.org/10.1101/pdb.prot108578
   PMID: https://pubmed.ncbi.nlm.nih.gov/39237454/
   Why used: protocol-level decision framework for selecting among TE/repeat annotation strategies and evaluating annotation quality.

## Cross-category positioning notes

- This file is for methods that generalize across TE classes or act as class-agnostic validation/monitoring layers.
- TE display sequencing is categorized as insertion-dynamics/monitoring and complements de novo family discovery methods.
- Class-specific source deep-dives remain in:
  - `helitrons_sources.md`
  - `sines_sources.md`
  - `mites_sources.md`

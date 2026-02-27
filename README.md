# RepBox

RepBox is a transposable element discovery and annotation workflow created during PhD thesis research.

## Overview
- Legacy thesis-era pipeline with active modernization in progress.
- Current modernization track: Python-first architecture and modular adapters.
- Development planning is managed in GitHub Projects (Kanban workflow).

## Quick start (development scaffold)
From repository root:

1. `python -m pip install -e .`
2. `python -m repbox version`
3. `python -m repbox check --legacy-config repbox_config.txt`
4. `python -m repbox run --input <genome.fa> --out <output_dir> --threads 4`
5. `python -m repbox fallback-scan --input <genome.fa> --out <fallback_dir> --classes mite,sine,helitron`
6. `python -m repbox refine-families --input-dir <fallback_dir> --out <refined_dir> --classes mite,sine`

Notes:
- `repbox check` returning non-zero is expected if legacy tool paths are missing on your machine.
- The new CLI currently provides Milestone A scaffold behavior while migration continues.

## Project documentation map
- Changelog: `Changelog.md`
- Release workflow (includes templates + active schedule): `docs/process/releasing.md`
- Unified implementation plan (primary): `IMPLEMENTATION_PLAN_UNIFIED.md`
- TE tooling landscape update (2022-2026): `literature review/te_tooling_landscape_2026.md`
- GitHub Projects playbook: `docs/process/github_project_playbook.md`

## Versioning model
- Semantic Versioning (`MAJOR.MINOR.PATCH`).
- Latest live release: `v1.2.0`.
- Completed release sequence under current convention: `v1.1.0` -> `v1.1.1` -> `v1.2.0`.
- Active maintenance line: `1.2.x` (stabilization/patches as needed).
- Next feature line: `1.3.x` (to be scoped after `v1.2.x` stabilization).
- `2.0.0` is the functional milestone release target: RepBox end-to-end pipeline is production-usable and primarily driven by novel in-project element-identification methods (with external whole-genome pipelines retained as comparison baselines).

## Development workflow
1. Create a focused branch per task (`feat/*`, `fix/*`, `docs/*`, `test/*`).
2. Open a pull request into `master`.
3. Update `Changelog.md` (`Unreleased`) for user-visible changes.
4. Merge only when local validation and docs updates are complete.

## Historical Milestone A scaffold (pre-v1.0.3)
- New package scaffold under `src/repbox/`.
- New Python CLI scaffold with commands: `run`, `check`, `version`.
- Legacy tool-path compatibility loader for `repbox_config.txt`.
- Initial adapter and workflow-engine stubs for phased migration.

## RepeatModeler compatibility (historical modernization phase)
`repbox run` now uses a compatibility probe for RepeatModeler threading flags:

| RepeatModeler line | Thread flag used by RepBox | Compatibility mode |
|---|---|---|
| `2.0.4+` (modern) | `-threads` | `modern-threads` |
| `2.0.1-2.0.3` (legacy) | `-pa` | `legacy-pa` |

RepBox detects support from RepeatModeler help/version output. If detection fails, `repbox run` exits early with a targeted error and `repbox check` marks the tool as incompatible.

## Historical prototype: nested-aware graph refinement (SINE/MITE/Helitron)
RepBox includes an experimental Python refinement stage that clusters candidate insertions into families using k-mer similarity graphs and labels fully nested insertions.

Command:
- `repbox refine-families --input-dir <fallback_dir> --out <refined_dir> --classes mite,sine`

Outputs:
- `refined_families.tsv`
- `refined_members.tsv` (includes `nested` and `nested_round` labels)
- `refined_library.fa` (family representatives)
- `refined_summary.json`

## Platform notes (macOS Intel + ARM)
- Prefer architecture-matching binaries when using precompiled dependencies (`x86_64` vs `arm64`).
- Some legacy dependencies were historically installed via Intel-only binaries; on Apple Silicon these may require source builds or Rosetta-based compatibility workflows.
- `repbox check` validates configured paths and executability, but does not install tools.

## Historical thesis-era dependency reference
The remaining sections below document the original dependency setup used during thesis-era development.
They are preserved for reproducibility and migration support, not as the default modern installation guidance.

# Create Home directory for repbox
```
mkdir $HOME/repbox/bin
repbox=$HOME/repbox/bin
cd $repbox
```



# Included Dependencies
### HelitronScanner
```
# Version included, download is not needed.
```

### SINE_Scan
```
# Modified version is included and downloading is not necessary; simple run the setup bash script located in the SINE_Scan directory.
```






# Installing Dependencies
## Tandem Repeat Finder (source)
```
wget https://github.com/Benson-Genomics-Lab/TRF/archive/refs/tags/v4.09.1.tar.gz
tar xzvf v4.*
cd TRF-4*
mkdir build
cd build
../configure
make
sudo make install
cd $repbox
```


## RepeatScout (source)
```
wget http://www.repeatmasker.org/RepeatScout-1.0.6.tar.gz
tar xzvf RepeatScout-1.0.6.tar.gz
cd RepeatScout-1.0.6
make
cd $repbox
```


## RMBLAST (pre-compiled)
```
wget http://www.repeatmasker.org/rmblast/rmblast-2.14.0+-x64-macosx.tar.gz
tar xzvf rmblast-2.14.0+-x64-macosx.tar.gz
cd $repbox
```


## LTR_retriever (pre-compiled)
```
wget -qO- https://github.com/oushujun/LTR_retriever/archive/refs/tags/v2.9.0.tar.gz > ltr_retriever_v2.9.0.tar.gz
tar xzvf ltr_retriever_v2.9.0.tar.gz
cd $repbox
```


## MAFFT (source)
```
wget --no-check-certificate https://mafft.cbrc.jp/alignment/software/mafft-7.490-with-extensions-src.tgz
tar xvf mafft-7.490-with-extensions-src.tgz
cd mafft-7.490-with-extensions/core
sed '1s@^PREFIX = /usr/local$@PREFIX = ~/repbox/mafft-7.490-with-extensions@' Makefile > temp && mv temp Makefile
make clean
make
make install
cd ..
cd extensions
sed '1s@^PREFIX = /usr/local$@PREFIX = ~/repbox/mafft-7.490-with-extensions@' Makefile > temp && mv temp Makefile
make clean
make
make install
cd $repbox
```


## CD-HIT (source)
```
wget https://github.com/weizhongli/cdhit/releases/download/V4.8.1/cd-hit-v4.8.1-2019-0228.tar.gz
tar xvf cd-hit-v4.8.1-2019-0228.tar.gz
cd cd-hit-v4.8.1-2019-0228
sudo make openmp=no
sudo make install
cd $repbox
```

## NINJA (Homebrew & source)
```
wget https://wheelerlab.org/software/ninja/files/ninja.tgz
tar xvf ninja.tgz
```

## MITEFinderII
```
git clone https://github.com/jhu99/miteFinder.git
cd miteFinder
make
cd $repbox
```

## VSEARCH
Development environment for repbox was Intel macOS and install instructions for VSEARCH are consistent with this architecture. Please refer to the [VSEARCH GitHub]('https://github.com/torognes/vsearch’) for instructions specific to your system.
```
wget https://github.com/torognes/vsearch/releases/download/v2.22.1/vsearch-2.22.1-macos-x86_64.tar.gz
tar xzf vsearch-2.22.1-macos-x86_64.tar.gz
cd vsearch-2.22.1-macos-x86_64
```


## Local Homebrew Formulas - https://github.com/Ensembl/homebrew-external/tree/master
```
# MUSCLE 
brew install local_homebrew_formulas/muscle.rb

# EMBOSS
brew install local_homebrew_formulas/emboss.rb

# Bedtools
brew install local_homebrew_formulas/bedtools.rb

# BLAST
brew install local_homebrew_formulas/blast.rb

#GenomeTools (LTRHarvest)
brew install local_homebrew_formulas/genometools.rb

#RECON
brew install local_homebrew_formulas/recon.rb

#dos2unix
brew install local_homebrew_formulas/dos2unix.rb

```

## RepeatModeler 2.0.1 (historical pin)
```
cd $HOME/repbox/bin
wget https://github.com/Dfam-consortium/RepeatModeler/archive/refs/tags/2.0.1.tar.gz
tar -zxvf 2.0.1.tar.gz
cd RepeatModeler-2.0.1/
```

## RepeatMasker 4.1.3.p1 (historical pin)
```
cd $HOME/repbox/bin
wget https://www.repeatmasker.org/RepeatMasker/RepeatMasker-4.1.3-p1.tar.gz
tar xvf RepeatMasker-4.1.3-p1.tar.gz
head -25 RepeatMasker/Libraries/Dfam.h5 # Check for release 3.6
```

### Repbase
- Updated versions are behind a paywall. Most-recent open-access version included is RepBaseRepeatMaskerEdition-20181026.tar.gz
```
cd $HOME/repbox/bin
cp RepBaseRepeatMaskerEdition-20181026.tar.gz RepeatMasker
cd RepeatMasker
tar xvf RepBaseRepeatMaskerEdition-20181026.tar.gz
```


# RepeatModeler & RepeatMasker Configuration
```
### RepeatModeler
cd $HOME/repbox/bin
perl ./RepeatModeler-2.0.1/configure

cd $HOME/repbox/bin
### RepeatMasker
perl ./RepeatMasker/configure

```

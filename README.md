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

Notes:
- `repbox check` returning non-zero is expected if legacy tool paths are missing on your machine.
- The new CLI currently provides Milestone A scaffold behavior while migration continues.

## Project documentation map
- Changelog: `Changelog.md`
- Release workflow: `RELEASING.md`
- Release notes templates: `RELEASE_NOTES_TEMPLATES.md`
- v0.3.0 implementation spec: `IMPLEMENTATION_SPEC_V0.3.0.md`
- GitHub Projects playbook: `GITHUB_PROJECT_PLAYBOOK.md`

## Versioning model
- Semantic Versioning (`MAJOR.MINOR.PATCH`).
- `0.x.y` is used while architecture and interfaces are still stabilizing.
- `1.0.0` will be cut when CLI behavior and configuration schema are declared stable.

## Development workflow
1. Create a focused branch per task (`feat/*`, `fix/*`, `docs/*`, `test/*`).
2. Open a pull request into `master`.
3. Update `Changelog.md` (`Unreleased`) for user-visible changes.
4. Merge only when local validation and docs updates are complete.

## v0.3.0 Milestone A scaffold
- New package scaffold under `src/repbox/`.
- New Python CLI scaffold with commands: `run`, `check`, `version`.
- Legacy tool-path compatibility loader for `repbox_config.txt`.
- Initial adapter and workflow-engine stubs for phased migration.

## Legacy dependency installation reference
The remaining sections below document the original dependency setup used for the thesis-era pipeline.
They are preserved for reproducibility and migration support.

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

## RepeatModeler 2.0.1
```
cd $HOME/repbox/bin
wget https://github.com/Dfam-consortium/RepeatModeler/archive/refs/tags/2.0.1.tar.gz
tar -zxvf 2.0.1.tar.gz
cd RepeatModeler-2.0.1/
```

## RepeatMasker 4.1.3.p1
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

# Legacy Thesis Environment Setup

This document preserves the original dependency installation steps used for the thesis-era RepBox pipeline.

These instructions are retained for reproducibility and migration reference.

## Create home directory for RepBox

```bash
mkdir "$HOME/repbox/bin"
repbox="$HOME/repbox/bin"
cd "$repbox"
```

## Included dependencies

### HelitronScanner

```bash
# Version included, download is not needed.
```

### SINE_Scan

```bash
# Modified version is included; run the setup script in the SINE_Scan directory.
```

## Installing dependencies

### Tandem Repeat Finder (source)

```bash
wget https://github.com/Benson-Genomics-Lab/TRF/archive/refs/tags/v4.09.1.tar.gz
tar xzvf v4.*
cd TRF-4*
mkdir build
cd build
../configure
make
sudo make install
cd "$repbox"
```

### RepeatScout (source)

```bash
wget http://www.repeatmasker.org/RepeatScout-1.0.6.tar.gz
tar xzvf RepeatScout-1.0.6.tar.gz
cd RepeatScout-1.0.6
make
cd "$repbox"
```

### RMBLAST (pre-compiled)

```bash
wget http://www.repeatmasker.org/rmblast/rmblast-2.14.0+-x64-macosx.tar.gz
tar xzvf rmblast-2.14.0+-x64-macosx.tar.gz
cd "$repbox"
```

### LTR_retriever (pre-compiled)

```bash
wget -qO- https://github.com/oushujun/LTR_retriever/archive/refs/tags/v2.9.0.tar.gz > ltr_retriever_v2.9.0.tar.gz
tar xzvf ltr_retriever_v2.9.0.tar.gz
cd "$repbox"
```

### MAFFT (source)

```bash
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
cd "$repbox"
```

### CD-HIT (source)

```bash
wget https://github.com/weizhongli/cdhit/releases/download/V4.8.1/cd-hit-v4.8.1-2019-0228.tar.gz
tar xvf cd-hit-v4.8.1-2019-0228.tar.gz
cd cd-hit-v4.8.1-2019-0228
sudo make openmp=no
sudo make install
cd "$repbox"
```

### NINJA (source)

```bash
wget https://wheelerlab.org/software/ninja/files/ninja.tgz
tar xvf ninja.tgz
```

### MITEFinderII

```bash
git clone https://github.com/jhu99/miteFinder.git
cd miteFinder
make
cd "$repbox"
```

### VSEARCH

The original development environment was Intel macOS. For platform-specific updates, see the VSEARCH repository:
https://github.com/torognes/vsearch

```bash
wget https://github.com/torognes/vsearch/releases/download/v2.22.1/vsearch-2.22.1-macos-x86_64.tar.gz
tar xzf vsearch-2.22.1-macos-x86_64.tar.gz
cd vsearch-2.22.1-macos-x86_64
```

### Local Homebrew formulas

Reference:
https://github.com/Ensembl/homebrew-external/tree/master

```bash
# MUSCLE
brew install local_homebrew_formulas/muscle.rb

# EMBOSS
brew install local_homebrew_formulas/emboss.rb

# Bedtools
brew install local_homebrew_formulas/bedtools.rb

# BLAST
brew install local_homebrew_formulas/blast.rb

# GenomeTools (LTRHarvest)
brew install local_homebrew_formulas/genometools.rb

# RECON
brew install local_homebrew_formulas/recon.rb

# dos2unix
brew install local_homebrew_formulas/dos2unix.rb
```

### RepeatModeler 2.0.1

```bash
cd "$HOME/repbox/bin"
wget https://github.com/Dfam-consortium/RepeatModeler/archive/refs/tags/2.0.1.tar.gz
tar -zxvf 2.0.1.tar.gz
cd RepeatModeler-2.0.1/
```

### RepeatMasker 4.1.3.p1

```bash
cd "$HOME/repbox/bin"
wget https://www.repeatmasker.org/RepeatMasker/RepeatMasker-4.1.3-p1.tar.gz
tar xvf RepeatMasker-4.1.3-p1.tar.gz
head -25 RepeatMasker/Libraries/Dfam.h5 # Check for release 3.6
```

### Repbase

Updated versions are behind a paywall. The latest open-access version used here is `RepBaseRepeatMaskerEdition-20181026.tar.gz`.

```bash
cd "$HOME/repbox/bin"
cp RepBaseRepeatMaskerEdition-20181026.tar.gz RepeatMasker
cd RepeatMasker
tar xvf RepBaseRepeatMaskerEdition-20181026.tar.gz
```

## RepeatModeler & RepeatMasker configuration

```bash
# RepeatModeler
cd "$HOME/repbox/bin"
perl ./RepeatModeler-2.0.1/configure

# RepeatMasker
cd "$HOME/repbox/bin"
perl ./RepeatMasker/configure
```

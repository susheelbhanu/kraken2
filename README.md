# Kraken2

## About
- Repository containing [Snakemake](https://snakemake.readthedocs.io/en/stable/) workflow for running [Kraken2](https://ccb.jhu.edu/software/kraken/) analyses

# Setup

## Conda

[Conda user guide](https://docs.conda.io/projects/conda/en/latest/user-guide/index.html)

```bash
# install miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
chmod u+x Miniconda3-latest-Linux-x86_64.sh
./Miniconda3-latest-Linux-x86_64.sh # follow the instructions
```

Getting the repository including sub-modules
```bash
git clone git@github.com:susheelbhanu/kraken2.git
```

Create the main `snakemake` environment

```bash
# create venv
conda env create -f envs/snakemake.yaml -n "snakemake"
```

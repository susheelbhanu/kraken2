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
conda activate snakemake
```

## How to run

The workflow can be launched using one of the option as follows

```bash
./sbatch.sh
```

(or)

```bash
CORES=48 snakemake -s workflow/Snakefile --configfile config/config.yaml --use-conda --conda-prefix ${CONDA_PREFIX}/pipeline --cores $CORES -rpn
```
(or)

Note: For running on `esb-compute-01` or `litcrit`  adjust the `CORES` as needed to prevent some tools from spawning too many threads; and launch as below

```bash
CORES=24 snakemake -s workflow/Snakefile --configfile config/config.yaml --use-conda --conda-prefix ${CONDA_PREFIX}/pipeline --cores $CORES -rpn
```

## Configs

All config files are stored in the folder `config/`

Note(s): 
- Edit the paths to `data_dir`, `results_dir`, `env_dir` and the *databases*
- Provide a `kraken2_sample_list`


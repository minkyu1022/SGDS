# Directory Overview

This directory provides implementations and experiments for the Lenard-Jones potential and Alanine Dipeptide systems. It includes filling buffer by first round searcher, training routines, and evaluation scripts to reproduce our results.

## Environment Setup

Create and activate the required environment using the provided YAML file:

```bash
conda env create -f ./environment.yml
conda activate your_env_name
```

## Download data

To run the experiments for ALDP and LJ potentials, you can download the reference samples
https://zenodo.org/records/15436773

## Reproduction Guide

The reproduction workflow consists of two main steps:

### 1. Filling buffer by first round searcher

Fill buffer by first round searcher. Replace `{task}` with your chosen task, and specify the GPU ID and random seed:

```bash
bash lj_aldp/script/collect/{task}.sh {gpu_id} {seed}
```

We use seed 0 for all tasks.

### 2. Training

Train the model using your specified method. Replace `{task}` and `{method}`, and set the GPU ID and seed accordingly:

```bash
bash gmm_mw/experiments/{task}/{method}.sh
```

```bash
bash lj_aldp/script/{task}/{method}.sh {gpu_id} {seed}
```

## Alanine Dipeptide Evaluation

For the Alanine Dipeptide system, you need to correct the sampled bond graph and chirality before evaluation. Run the following script, specifying GPU ID, seed, checkpoint directory, and epoch:

```bash
bash lj_aldp/script/aldp/eval.sh {gpu_id} {seed} {checkpoint_dir} {epoch}
```

---
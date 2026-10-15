# TBX11K replication

This project replicates the paper "Rethinking Computer-aided Tuberculosis Diagnosis" (Liu et al., CVPR 2020). The paper introduced TBX11K, a dataset of 11,200 chest X-ray images.

## Scope

The first version replicates the image classification task only. The model sorts each chest X-ray into one of three classes:

- Healthy
- Sick but non-TB
- TB (tuberculosis)

The TB area detection task is not in the first version.

## Requirements

- Python 3.11 or later
- [uv](https://docs.astral.sh/uv/)

## Installation

1. Go to the `TBX11K` folder.
2. Run `uv sync` to install the dependencies.
3. Run `uv run pytest` to make sure that the installation is correct.

## Data

CAUTION: Do not put the dataset in git. The `.gitignore` file excludes the `data/` folder.

The dataset comes from the official Google Drive file (`TBX11K.zip`, CC BY 4.0 license). The source is the [official repository](https://github.com/yun-liu/Tuberculosis).

1. Run `uv run python -m tbx11k.download`.
2. Make sure that the command shows "Dataset is complete".

The command downloads `TBX11K.zip` to `data/`. Then it extracts the archive to `data/TBX11K/`. Then it checks the train list (6,600 images) and the val list (1,800 images). If an image is missing, the command stops with an error.

The test labels are not public. The authors keep them for the online challenge on Codabench.

## Layout

| Path | Content |
|---|---|
| `src/tbx11k/` | The Python package |
| `tests/` | The tests |
| `data/` | The dataset (not in git) |
| `outputs/` | The model checkpoints and results (not in git) |

# graph-alchemy-g4rs

This repository hosts a small, standalone **graph classification mini-competition**.

Motivation: graph classification is a foundational task in graph ML, commonly used as a first benchmark for molecule and protein graphs. This challenge is intentionally lightweight and reproducible: you get a clean baseline, fixed splits, and a simple submission flow to practice end-to-end modeling and evaluation.

The competition package lives under `gnn-challenge/`.

It provides **two tracks**:

- `proteins` (protein graphs)
- `mutag` (molecule graphs)

Each track is graph classification and is stored under `gnn-challenge/data/<dataset>/`.

Quickstart:

1) Create/activate venv
2) `pip install -r gnn-challenge/starter_code/requirements.txt`
3) `python gnn-challenge/starter_code/baseline.py --dataset proteins`

This generates `gnn-challenge/submissions/sample_submission_proteins.csv`.

For full participant instructions (including how to submit), see `gnn-challenge/README.md`.

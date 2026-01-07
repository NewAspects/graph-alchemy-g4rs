# graph-alchemy-g4rs

This repository hosts a small, standalone **graph classification mini-competition**.

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

# Organizer checklist

This file is for the organizers (not participants).

## 1) Prepare data

Raw zips go under `gnn-challenge/raw/` (do not commit).

- PROTEINS:

```bash
python gnn-challenge/starter_code/prepare_data.py --dataset proteins --raw-zip gnn-challenge/raw/PROTEINS.zip
```

- MUTAG:

```bash
python gnn-challenge/starter_code/prepare_data.py --dataset mutag --raw-zip gnn-challenge/raw/MUTAG.zip
```

## 2) Create hidden test labels (private)

Do NOT commit `test_labels.csv`.

```bash
python gnn-challenge/starter_code/prepare_data.py --dataset proteins --raw-zip gnn-challenge/raw/PROTEINS.zip --write-test-labels
python gnn-challenge/starter_code/prepare_data.py --dataset mutag --raw-zip gnn-challenge/raw/MUTAG.zip --write-test-labels
```

## 3) Smoke test (must pass before opening)

```bash
python gnn-challenge/starter_code/smoke_test.py
```

## 4) Validate a participant submission (no labels required)

```bash
python gnn-challenge/starter_code/validate_submission.py gnn-challenge/submissions/sample_submission_proteins.csv --dataset proteins
python gnn-challenge/starter_code/validate_submission.py gnn-challenge/submissions/sample_submission_mutag.csv --dataset mutag
```

## 5) Score submissions (organizers only)

Requires `data/<dataset>/test_labels.csv`.

```bash
python gnn-challenge/starter_code/scoring_script.py path/to/submission.csv proteins
python gnn-challenge/starter_code/scoring_script.py path/to/submission.csv mutag
```

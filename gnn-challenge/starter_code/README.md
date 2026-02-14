# Starter Code (baseline + tools)

If you are a participant, start here: [gnn-challenge/README.md](../README.md)

## What is this?

- `baseline.py`: creates a per-dataset sample prediction file and prints a validation score
- `validate_submission.py`: checks your CSV format (no labels needed)
- `smoke_test.py`: quick end-to-end check (baseline + validator)

## Quickstart

```bash
pip install -r requirements.txt
python baseline.py --dataset proteins
python baseline.py --dataset mutag
```

Output:

- `../submissions/sample_submission_proteins.csv`
- `../submissions/sample_submission_mutag.csv`

For the official combined leaderboard flow, a single submission run must include both dataset prediction files and one `metadata.json`.

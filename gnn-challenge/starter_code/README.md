# Starter Code (baseline + tools)

If you are a participant, start here: [gnn-challenge/README.md](../README.md)

## What is this?

- `baseline.py`: creates a sample submission and prints a validation score
- `prepare_data.py`: organizers only (turns TU dataset zips into `data/<track>/`)
- `scoring_script.py`: organizers only (needs hidden `test_labels.csv`)

## Quickstart

```bash
pip install -r requirements.txt
python baseline.py --dataset proteins
```

Output:

- `../submissions/sample_submission_proteins.csv`

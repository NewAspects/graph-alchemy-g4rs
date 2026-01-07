# Open GNN Mini-Competition (Task 3)

This folder is the competition package.

## Tracks

- `proteins` (graph classification)
- `mutag` (graph classification)

## For participants (the easy way)

1) Install Python 3.10+.

2) Install requirements:

```bash
pip install -r gnn-challenge/starter_code/requirements.txt
```

3) Run the baseline (also prints a validation score):

```bash
python gnn-challenge/starter_code/baseline.py --dataset proteins
```

For MUTAG:

```bash
python gnn-challenge/starter_code/baseline.py --dataset mutag
```

4) Your submission file will be created here:

- `gnn-challenge/submissions/sample_submission_proteins.csv`
- `gnn-challenge/submissions/sample_submission_mutag.csv`

Submission format:

- CSV columns must be exactly: `graph_id,target`

## For organizers (prepare data)

Raw zips should NOT be committed. Put them under `gnn-challenge/raw/`.

Prepare a track (example: PROTEINS):

```bash
python gnn-challenge/starter_code/prepare_data.py --dataset proteins --raw-zip gnn-challenge/raw/PROTEINS.zip
```

To create `test_labels.csv` for scoring (organizers only):

```bash
python gnn-challenge/starter_code/prepare_data.py --dataset proteins --raw-zip gnn-challenge/raw/PROTEINS.zip --write-test-labels
```

Score a submission (organizers only):

```bash
python gnn-challenge/starter_code/scoring_script.py gnn-challenge/submissions/sample_submission_proteins.csv proteins
```

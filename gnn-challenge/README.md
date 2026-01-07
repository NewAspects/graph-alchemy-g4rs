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

Note:

- `gnn-challenge/data/<track>/test.csv` has no labels.
- Your `target` predictions are evaluated by the organizers.

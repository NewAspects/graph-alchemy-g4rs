# Open GNN Mini-Competition (Task 3)

This folder is the competition package.

## Tracks

- `proteins` (graph classification)
- `mutag` (graph classification)

## Timeline

- Start: 2026-01-08
- Deadline: 2026-07-08 (6 months)

## Submission policy

- Daily limit: **3 submissions per team per track**
- You can train as much as you want locally; only submissions are limited.

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

## How to submit

Send **one CSV per track**.

- Option A (recommended): open a **GitHub Issue** in this repo, attach your CSV file(s), and include:
	- Team name
	- Track (`proteins` and/or `mutag`)
	- Short method description (1-2 lines)

What happens next:

- Organizers validate your file format and compute the official test score.
- The organizers may update the public leaderboard.

Score visibility:

- Participants can always see their **local validation score** (from `val.csv`).
- The **official test score** is computed by the organizers (test labels are private).
- The organizers may publish a public leaderboard; otherwise you will only have your own local validation score.

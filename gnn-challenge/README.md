# Graph Alchemy Mini-Competition

This folder is the competition package.

## Overview

Goal: build a model that predicts the **graph class** for unseen graphs.

You are given two tracks (datasets):

- `proteins`: protein graphs (graph classification)
- `mutag`: molecule graphs (graph classification)

For each track:

- You train on `train.csv` (labeled graphs).
- You can tune on `val.csv` (labeled graphs).
- You must predict labels for `test.csv` (unlabeled graphs).

## Motivation / Why participate

Graph classification is a core task in applied graph machine learning. In practice, graphs often represent molecules and protein structures, and predicting a graph label is a common first benchmark when building and debugging GNN pipelines.

This mini-competition is designed to be:

- **What it measures:** performance on graph-level classification under a fixed train/val/test split, using the official metric (**Macro F1**).
- **Why it matters:** a compact, reproducible benchmark to practice end-to-end graph ML (data handling, modeling, evaluation, reporting) without heavyweight infrastructure.
- **Who it is for:** students and practitioners who want a clean baseline and a well-scoped challenge (beginner-friendly, but open-ended for stronger models).
- **What you gain:** a ready-to-run reference pipeline, a consistent evaluation protocol, and the habit of reporting runtime/compute alongside accuracy.
- **What counts as a strong approach:** improving Macro F1 on the hidden test set while keeping a **reproducible workflow** (clear method description, approximate runtime, and no leakage from test labels).

## Scoring

- Metric: **Macro F1** (higher is better)
- The official score is computed by the organizers on a **hidden test label file**.

This repo lets you compute a local validation score (on `val.csv`) and generate a submission for the test set.

## Tracks

- `proteins` (graph classification)
- `mutag` (graph classification)

## Timeline

- Start: 2026-01-08
- Deadline: 2026-07-08 (6 months)

## Submission policy

- Daily limit: **3 submissions per team per track**
- You can train as much as you want locally; only submissions are limited.
- Each submission issue must include **approximate runtime** (how long it took to produce the attached CSV on your hardware).

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

Optional (recommended): validate your submission file format locally:

```bash
python gnn-challenge/starter_code/validate_submission.py gnn-challenge/submissions/sample_submission_proteins.csv --dataset proteins
```

Note:

- `gnn-challenge/data/<track>/test.csv` has no labels.
- Your `target` predictions are evaluated by the organizers.

## How to submit

Send **one CSV per track**.

- Option A (recommended): open a **GitHub Issue** in this repo using the **Submission** template, attach your CSV file(s), and include:
  - Team name
  - Track (`proteins` and/or `mutag`)
  - Short method description (2-5 lines)
  - Approximate runtime to produce the attached CSV (training + inference; CPU/GPU info is helpful)

What happens next:

- Organizers validate your file format and compute the official test score.
- The organizers may update the public leaderboard.

Score visibility:

- Participants can always see their **local validation score** (from `val.csv`).
- The **official test score** is computed by the organizers (test labels are private).
- The organizers may publish a public leaderboard; otherwise you will only have your own local validation score.

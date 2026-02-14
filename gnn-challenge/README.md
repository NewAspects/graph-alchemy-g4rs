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

## Data specification (mandatory A and X)

Each graph is represented by:

- **Adjacency matrix A**: provided in edge-list form in `edges.csv` (`graph_id,src,dst`).
- **Node feature matrix X**: provided in `nodes.csv` (all node feature columns per `graph_id,node_id`).

This explicitly satisfies the benchmark requirement to provide both A and X.

## Motivation / Why participate

Graph classification is a core task in applied graph machine learning. In practice, graphs often represent molecules and protein structures, and predicting a graph label is a common first benchmark when building and debugging GNN pipelines.

This mini-competition is designed to be:

- **What it measures:** cross-dataset graph-level classification under fixed train/val/test splits, using a **combined score**.
- **Why it matters:** a compact, reproducible benchmark to practice end-to-end graph ML (data handling, modeling, evaluation, reporting) without heavyweight infrastructure.
- **Who it is for:** students and practitioners who want a clean baseline and a well-scoped challenge (beginner-friendly, but open-ended for stronger models).
- **What you gain:** a ready-to-run reference pipeline, a consistent evaluation protocol, and the habit of reporting runtime/compute alongside accuracy.
- **What counts as a strong approach:** improving Macro F1 on the hidden test set while keeping a **reproducible workflow** (clear method description, approximate runtime, and no leakage from test labels).

## Scoring

- Per-track metric: **Macro F1** (higher is better)
- Official leaderboard metric: **Combined Score = (MacroF1_proteins + MacroF1_mutag) / 2**
- Official scoring uses hidden test labels (organizer-only; loaded from CI secrets).

This repo lets you compute local validation scores and generate predictions for both test tracks.

## Tracks

- `proteins` (graph classification)
- `mutag` (graph classification)

## Timeline

- Start: 2026-01-08
- Deadline: 2026-07-08 (6 months)

## Submission policy

- **Only one submission attempt per participant/team** is allowed (strictly enforced by CI).
- Each submission must include **approximate runtime** (how long it took to produce the CSV on your hardware).

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

4) Baseline predictions will be created here:

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

## How to submit (PR + automatic scoring)

Create one run folder per submission:

`gnn-challenge/submissions/inbox/<team_name>/<run_id>/`

Required files:

- `predictions_proteins.csv` (columns exactly `graph_id,target`)
- `predictions_mutag.csv` (columns exactly `graph_id,target`)
- `metadata.json`

Minimal `metadata.json` fields:

- `team`
- `model`
- `model_type` (`human`, `llm-only`, `human+llm`)
- `runtime_minutes`
- `notes` (optional)

Then open a Pull Request.

What happens next:

- CI validates your file format.
- CI scores predictions against hidden labels (not committed to the repo).
- CI posts score as a PR comment.
- After merge, leaderboard files are auto-updated.

## Privacy and fairness policy

- Public leaderboard shows only **rank, combined score**.
- Private submission artifacts/details are not exposed publicly.
- Ranking follows Kaggle tie handling: equal scores share the same rank.
- LLMs may be used by participants for modeling assistance, but must not be used to fully design dataset/task/evaluation logic.

## Dataset challenge realism

Current data intentionally includes realistic difficulty:

- Label imbalance (`proteins` and `mutag` are not class-balanced).
- Graph sparsity / variable graph structure.
- Non-trivial feature-topology interactions.

## Computational affordability

Competition baseline and expected training workflows are designed to stay within the benchmark budget (target: full training under 3 hours on CPU).

## Interactive leaderboard (GitHub Pages)

Interactive UI files live under `docs/`:

- `docs/leaderboard.html`
- `docs/leaderboard.css`
- `docs/leaderboard.js`

Enable GitHub Pages with source `main` branch and `/docs` folder.
The canonical score source is `gnn-challenge/leaderboard/leaderboard.csv`.

Score visibility:

- Participants can always see their **local validation score** (from `val.csv`).
- The **official test score** is computed by CI using private labels (kept in GitHub Secrets).
- Public rankings are generated from `gnn-challenge/leaderboard/leaderboard.csv` and rendered automatically.

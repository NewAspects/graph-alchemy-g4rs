---
name: Submission
about: Submission guidance (PR-based flow)
title: "[Submission Help] <team name>"
labels: [submission]
---

## PR-based submission required

Submissions are validated/scored automatically from Pull Requests.

Please create:

- `gnn-challenge/submissions/inbox/<team_name>/<run_id>/predictions_proteins.csv`
- `gnn-challenge/submissions/inbox/<team_name>/<run_id>/predictions_mutag.csv`
- `gnn-challenge/submissions/inbox/<team_name>/<run_id>/metadata.json`

Then open a PR to `main`.

## Prediction files format

- Columns must be exactly: `graph_id,target`
- `graph_id` must match `gnn-challenge/data/proteins/test.csv` for proteins file
- `graph_id` must match `gnn-challenge/data/mutag/test.csv` for mutag file

## metadata.json required fields

- `team`
- `model`
- `model_type` (`human`, `llm-only`, `human+llm`)
- `runtime_minutes`
- `notes` (optional)

## Need help?

Use this issue template only for questions/support about a submission.

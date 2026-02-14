# Competition Automation Setup (Organizers)

This folder contains the secure scoring pipeline used by GitHub Actions.

## Required GitHub Secrets

Create repository secrets with exact names:

- `PROTEINS_TEST_LABELS_CSV`
- `MUTAG_TEST_LABELS_CSV`

Each secret value must be full CSV text with columns:

- `graph_id,target`

## Workflows

- `.github/workflows/score_submission.yml`
  - Trigger: Pull Request with `submissions/inbox/...` files
  - Validates format and scores one submission
  - Enforces one-attempt-per-team policy
  - Posts score comment on PR

- `.github/workflows/publish_leaderboard.yml`
  - Trigger: push to `main` affecting submissions/competition files
  - Rebuilds leaderboard from all valid inbox runs
  - Enforces one-attempt-per-team policy before publishing
  - Renders markdown + JSON artifacts

## Submission folder contract

For each run:

`gnn-challenge/submissions/inbox/<team_name>/<run_id>/`

Required files:

- `predictions_proteins.csv`
- `predictions_mutag.csv`
- `metadata.json`

`metadata.json` required keys:

- `team`
- `model`
- `model_type` (`human`, `llm-only`, `human+llm`)
- `runtime_minutes`

## Public leaderboard schema

Public output is privacy-safe and contains only:

- `rank`
- `score`

`score` is combined score: (MacroF1_proteins + MacroF1_mutag)/2.
Tie policy follows Kaggle-style competition ranking (equal scores share equal rank).

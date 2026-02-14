# Submissions

PR-based submission path:

`inbox/<team_name>/<run_id>/`

Policy: exactly **one attempt per team** is allowed. Use a single run folder.

Required files per run:

- `predictions_proteins.csv`
- `predictions_mutag.csv`
- `metadata.json`

Each prediction file must have exactly:

- `graph_id,target`

`metadata.json` example:

```json
{
  "team": "example_team",
  "model": "graphsage-v2",
  "model_type": "human+llm",
  "runtime_minutes": 18,
  "notes": "5-fold ensembling"
}
```

`model_type` must be one of: `human`, `llm-only`, `human+llm`.

Public leaderboard exposes only: `rank`, `score` (combined across proteins+mutag).

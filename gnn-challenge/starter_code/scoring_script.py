from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import f1_score


def main(argv: list[str]) -> int:
    if len(argv) not in {2, 3}:
        print("Usage: python scoring_script.py <path/to/submission.csv> [proteins|mutag]")
        return 2

    submission_file = Path(argv[1])
    dataset = "proteins" if len(argv) == 2 else str(argv[2])
    if dataset not in {"proteins", "mutag"}:
        print("Dataset must be one of: proteins, mutag")
        return 2

    here = Path(__file__).resolve()
    truth_path = here.parents[1] / "data" / dataset / "test_labels.csv"

    submission = pd.read_csv(submission_file)
    truth = pd.read_csv(truth_path)

    # Basic validation
    required = {"graph_id", "target"}
    if set(submission.columns) != required:
        print(f"Submission must have exactly columns: {sorted(required)}")
        return 2

    merged = truth.merge(submission, on="graph_id", suffixes=("_true", "_pred"), how="inner")
    if len(merged) != len(truth):
        print("Submission is missing ids or has wrong ids.")
        return 2

    score = f1_score(merged["target_true"], merged["target_pred"], average="macro")
    print(f"Submission Macro F1 Score: {score:.4f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

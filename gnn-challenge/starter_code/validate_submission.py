from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a submission file (no labels required).")
    parser.add_argument("submission", type=Path)
    parser.add_argument("--dataset", choices=["proteins", "mutag"], default="proteins")
    args = parser.parse_args()

    here = Path(__file__).resolve()
    data_dir = here.parents[1] / "data" / str(args.dataset)
    test_path = data_dir / "test.csv"

    if not test_path.exists():
        raise FileNotFoundError(f"Missing test file: {test_path}")

    submission = pd.read_csv(args.submission)
    required = {"graph_id", "target"}

    if set(submission.columns) != required:
        raise SystemExit(f"Submission must have exactly columns: {sorted(required)}")

    test = pd.read_csv(test_path)
    expected_ids = test["graph_id"].to_numpy()

    got_ids = submission["graph_id"].to_numpy()
    if len(got_ids) != len(expected_ids):
        raise SystemExit(f"Wrong number of rows: expected {len(expected_ids)}, got {len(got_ids)}")

    if set(got_ids.tolist()) != set(expected_ids.tolist()):
        raise SystemExit("Submission graph_id set does not match test.csv")

    if submission["target"].isna().any():
        raise SystemExit("Submission contains NaN targets")

    # Basic type sanity (allow ints stored as floats in CSV, but must be numeric)
    if not pd.api.types.is_numeric_dtype(submission["target"]):
        raise SystemExit("Submission target column must be numeric class ids")

    print("OK: submission format looks valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

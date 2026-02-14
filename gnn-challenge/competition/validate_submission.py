from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {"graph_id", "target"}


def validate_submission(pred_path: Path, dataset: str, test_path: Path) -> None:
    if dataset not in {"proteins", "mutag"}:
        raise ValueError("dataset must be one of: proteins, mutag")

    if not pred_path.exists():
        raise FileNotFoundError(f"Missing predictions file: {pred_path}")
    if not test_path.exists():
        raise FileNotFoundError(f"Missing test file: {test_path}")

    preds = pd.read_csv(pred_path)
    test = pd.read_csv(test_path)

    if set(preds.columns) != REQUIRED_COLUMNS:
        raise ValueError(f"Prediction file must contain exactly {sorted(REQUIRED_COLUMNS)}")

    if preds["graph_id"].duplicated().any():
        raise ValueError("Duplicate graph_id values found")

    if preds["target"].isna().any():
        raise ValueError("NaN values in target")

    if not pd.api.types.is_numeric_dtype(preds["target"]):
        raise ValueError("target must be numeric class ids")

    expected_ids = test["graph_id"].tolist()
    got_ids = preds["graph_id"].tolist()

    if len(got_ids) != len(expected_ids):
        raise ValueError(f"Wrong row count: expected {len(expected_ids)}, got {len(got_ids)}")

    if set(got_ids) != set(expected_ids):
        raise ValueError("graph_id set mismatch with test.csv")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate submission format for graph challenge")
    parser.add_argument("predictions", type=Path)
    parser.add_argument("--dataset", required=True, choices=["proteins", "mutag"])
    args = parser.parse_args()

    root = Path(__file__).resolve().parents[1]
    test_path = root / "data" / args.dataset / "test.csv"
    validate_submission(args.predictions, args.dataset, test_path)
    print("VALID SUBMISSION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

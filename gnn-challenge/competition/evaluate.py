from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from metrics import macro_f1
from validate_submission import validate_submission


REQUIRED_COLUMNS = {"graph_id", "target"}


def score_submission(pred_path: Path, dataset: str, labels_path: Path) -> float:
    root = Path(__file__).resolve().parents[1]
    test_path = root / "data" / dataset / "test.csv"
    validate_submission(pred_path, dataset, test_path)

    if not labels_path.exists():
        raise FileNotFoundError(f"Missing private labels file: {labels_path}")

    labels = pd.read_csv(labels_path)
    preds = pd.read_csv(pred_path)

    if set(labels.columns) != REQUIRED_COLUMNS:
        raise ValueError(f"labels file must contain exactly {sorted(REQUIRED_COLUMNS)}")

    merged = labels.merge(preds, on="graph_id", suffixes=("_true", "_pred"), how="inner")
    if len(merged) != len(labels):
        raise ValueError("Prediction IDs do not fully match hidden labels")

    return macro_f1(merged["target_true"], merged["target_pred"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate graph classification submission")
    parser.add_argument("predictions", type=Path)
    parser.add_argument("labels", type=Path, help="Private labels CSV for the selected dataset")
    parser.add_argument("--dataset", required=True, choices=["proteins", "mutag"])
    args = parser.parse_args()

    score = score_submission(args.predictions, args.dataset, args.labels)
    print(f"SCORE={score:.8f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluate import score_submission


ALLOWED_MODEL_TYPES = {"human", "llm-only", "human+llm"}


def _require(metadata: dict, key: str) -> str:
    value = str(metadata.get(key, "")).strip()
    if not value:
        raise ValueError(f"metadata missing required field: {key}")
    return value


def _prediction_file(run_dir: Path, dataset: str) -> Path:
    return run_dir / f"predictions_{dataset}.csv"


def main() -> int:
    parser = argparse.ArgumentParser(description="Score one PR submission (combined proteins+mutag)")
    parser.add_argument("--run-dir", required=True, type=Path)
    parser.add_argument("--metadata", required=True, type=Path)
    parser.add_argument("--labels-dir", required=True, type=Path)
    parser.add_argument("--pr-number", default="")
    args = parser.parse_args()

    if not args.metadata.exists():
        raise FileNotFoundError(f"Missing metadata file: {args.metadata}")
    if not args.run_dir.exists():
        raise FileNotFoundError(f"Missing run directory: {args.run_dir}")

    metadata = json.loads(args.metadata.read_text(encoding="utf-8"))
    _require(metadata, "team")

    _require(metadata, "model")
    model_type = _require(metadata, "model_type")
    if model_type not in ALLOWED_MODEL_TYPES:
        raise ValueError("metadata.model_type must be one of: human, llm-only, human+llm")

    _require(metadata, "runtime_minutes")

    per_dataset_scores: dict[str, float] = {}
    for dataset in ["proteins", "mutag"]:
        pred_path = _prediction_file(args.run_dir, dataset)
        if not pred_path.exists():
            raise FileNotFoundError(f"Missing prediction file: {pred_path}")
        labels_path = args.labels_dir / f"{dataset}_test_labels.csv"
        per_dataset_scores[dataset] = float(score_submission(pred_path, dataset, labels_path))

    combined_score = (per_dataset_scores["proteins"] + per_dataset_scores["mutag"]) / 2.0

    result = {
        "score": round(float(combined_score), 8),
        "proteins_score": round(float(per_dataset_scores["proteins"]), 8),
        "mutag_score": round(float(per_dataset_scores["mutag"]), 8),
    }

    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

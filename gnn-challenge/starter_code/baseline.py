from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import f1_score
from sklearn.pipeline import Pipeline

from graph_baseline_utils import build_graph_features


def main() -> int:
    parser = argparse.ArgumentParser(description="Baseline for the Open GNN Mini-Competition (graph classification).")
    parser.add_argument("--dataset", choices=["proteins", "mutag"], default="proteins")
    args = parser.parse_args()

    here = Path(__file__).resolve()
    data_dir = here.parents[1] / "data" / str(args.dataset)
    submissions_dir = here.parents[1] / "submissions"
    submissions_dir.mkdir(parents=True, exist_ok=True)

    nodes = pd.read_csv(data_dir / "nodes.csv")
    edges = pd.read_csv(data_dir / "edges.csv")

    feats, feature_cols = build_graph_features(nodes, edges)

    train = pd.read_csv(data_dir / "train.csv")
    val = pd.read_csv(data_dir / "val.csv")
    test = pd.read_csv(data_dir / "test.csv")

    x_train = train.merge(feats, on="graph_id", how="left")[feature_cols]
    y_train = train["target"]
    x_val = val.merge(feats, on="graph_id", how="left")[feature_cols]
    y_val = val["target"]

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            (
                "rf",
                RandomForestClassifier(
                    n_estimators=400,
                    random_state=42,
                    n_jobs=-1,
                ),
            ),
        ]
    )

    model.fit(x_train, y_train)
    y_pred = model.predict(x_val)
    score = f1_score(y_val, y_pred, average="macro")
    print(f"Validation Macro F1 ({args.dataset}): {score:.4f}")

    x_test = test.merge(feats, on="graph_id", how="left")[feature_cols]
    test_preds = model.predict(x_test)

    out_path = submissions_dir / f"sample_submission_{args.dataset}.csv"
    pd.DataFrame({"graph_id": test["graph_id"].to_numpy(), "target": test_preds}).to_csv(
        out_path, index=False
    )
    print(f"Wrote: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

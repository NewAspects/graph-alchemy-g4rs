from __future__ import annotations

import numpy as np
import pandas as pd


def build_graph_features(nodes: pd.DataFrame, edges: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """Builds simple graph-level features from per-node and per-edge tables.

    Returns (features_df, feature_columns), where features_df has a 'graph_id' column.
    """

    # Basic sizes
    node_counts = nodes.groupby("graph_id").size().rename("num_nodes")
    edge_counts = edges.groupby("graph_id").size().rename("num_edges")

    feats = pd.concat([node_counts, edge_counts], axis=1).fillna(0.0).reset_index()
    feats["num_nodes"] = feats["num_nodes"].astype(int)
    feats["num_edges"] = feats["num_edges"].astype(int)

    # Degree-based summaries (treat edges as directed in file; counts still informative)
    if not edges.empty:
        deg = edges.groupby(["graph_id", "src"]).size().rename("out_deg").reset_index()
        deg_stats = deg.groupby("graph_id")["out_deg"].agg(["mean", "std", "max"]).fillna(0.0)
        deg_stats.columns = ["outdeg_mean", "outdeg_std", "outdeg_max"]
        feats = feats.merge(deg_stats.reset_index(), on="graph_id", how="left")
    else:
        feats["outdeg_mean"] = 0.0
        feats["outdeg_std"] = 0.0
        feats["outdeg_max"] = 0.0

    # Density (undirected-ish proxy; safe when num_nodes < 2)
    n = feats["num_nodes"].to_numpy(dtype=float)
    m = feats["num_edges"].to_numpy(dtype=float)
    denom = np.maximum(n * (n - 1.0), 1.0)
    feats["edge_density"] = (m / denom).astype(float)

    # Node label histogram if present
    if "node_label" in nodes.columns:
        # Reindex labels to 0..K-1 stable for compact columns
        labels = nodes[["graph_id", "node_label"]].copy()
        uniq = sorted(labels["node_label"].dropna().unique().tolist())
        mapping = {lab: i for i, lab in enumerate(uniq)}
        labels["node_label_idx"] = labels["node_label"].map(mapping).astype(int)

        counts = (
            labels.groupby(["graph_id", "node_label_idx"]).size().unstack(fill_value=0).sort_index(axis=1)
        )
        counts.columns = [f"node_label_count_{int(c)}" for c in counts.columns]
        feats = feats.merge(counts.reset_index(), on="graph_id", how="left").fillna(0.0)

    # Node attribute stats if present
    attr_cols = [c for c in nodes.columns if c.startswith("attr_")]
    if attr_cols:
        agg = nodes.groupby("graph_id")[attr_cols].agg(["mean", "std"]).fillna(0.0)
        agg.columns = [f"{c}_{stat}" for c, stat in agg.columns]
        feats = feats.merge(agg.reset_index(), on="graph_id", how="left").fillna(0.0)

    feature_cols = [c for c in feats.columns if c != "graph_id"]
    return feats, feature_cols

from __future__ import annotations

import argparse
import json
import urllib.request
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


@dataclass(frozen=True)
class SplitConfig:
    seed: int = 42
    test_frac: float = 0.2
    val_frac: float = 0.2  # fraction of remaining (after test)


_DEFAULT_URLS: dict[str, str] = {
    # TU Dortmund / Graph Kernel Datasets (commonly used mirror)
    "mutag": "https://www.chrsmrrs.com/graphkerneldatasets/MUTAG.zip",
    "proteins": "https://www.chrsmrrs.com/graphkerneldatasets/PROTEINS.zip",
}


def _read_txt_from_zip(zf: zipfile.ZipFile, name: str) -> list[str]:
    with zf.open(name) as f:
        raw = f.read().decode("utf-8", errors="replace")
    return [ln.strip() for ln in raw.splitlines() if ln.strip()]


def _find_member(zf: zipfile.ZipFile, wanted_suffix: str) -> str | None:
    # Works even if the zip has a top-level folder.
    for m in zf.namelist():
        if m.endswith(wanted_suffix):
            return m
    return None


def _load_tu_dataset(zip_path: Path, prefix: str) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict]:
    """Parses a TU dataset zip.

    Returns:
      nodes_df: graph_id,node_id,[node_label],[attr_*]
      edges_df: graph_id,src,dst (node_id is local per graph)
      graph_labels_df: graph_id,target (0..C-1)
      meta: dict with label_mapping, sizes
    """

    with zipfile.ZipFile(zip_path) as zf:
        # Required
        gi_name = _find_member(zf, f"{prefix}_graph_indicator.txt")
        gl_name = _find_member(zf, f"{prefix}_graph_labels.txt")
        a_name = _find_member(zf, f"{prefix}_A.txt")

        if not gi_name or not gl_name or not a_name:
            missing = [
                s
                for s, n in [
                    ("graph_indicator", gi_name),
                    ("graph_labels", gl_name),
                    ("A (edges)", a_name),
                ]
                if not n
            ]
            raise FileNotFoundError(
                f"Zip {zip_path} is missing required TU files for prefix={prefix}: {missing}"
            )

        graph_indicator = np.array([int(x) for x in _read_txt_from_zip(zf, gi_name)], dtype=int)
        raw_graph_labels = np.array([int(x) for x in _read_txt_from_zip(zf, gl_name)], dtype=int)

        # Optional node labels / attributes
        nl_name = _find_member(zf, f"{prefix}_node_labels.txt")
        na_name = _find_member(zf, f"{prefix}_node_attributes.txt")

        node_labels: np.ndarray | None = None
        node_attrs: np.ndarray | None = None

        if nl_name:
            node_labels = np.array([int(x) for x in _read_txt_from_zip(zf, nl_name)], dtype=int)

        if na_name:
            lines = _read_txt_from_zip(zf, na_name)
            # Comma-separated floats
            attrs = [
                [float(v) for v in ln.replace(" ", "").split(",") if v != ""]
                for ln in lines
            ]
            node_attrs = np.asarray(attrs, dtype=float)

        # Edges are global node ids (1-based)
        edges_lines = _read_txt_from_zip(zf, a_name)
        edges_global = np.array(
            [[int(p) for p in ln.replace(" ", "").split(",")[:2]] for ln in edges_lines], dtype=int
        )

    n_nodes = graph_indicator.shape[0]
    n_graphs = raw_graph_labels.shape[0]

    if node_labels is not None and node_labels.shape[0] != n_nodes:
        raise ValueError("node_labels length mismatch")
    if node_attrs is not None and node_attrs.shape[0] != n_nodes:
        raise ValueError("node_attributes length mismatch")

    # Map arbitrary labels to 0..C-1 (stable)
    unique = sorted(set(raw_graph_labels.tolist()))
    label_to_index = {lab: i for i, lab in enumerate(unique)}
    targets = np.array([label_to_index[int(l)] for l in raw_graph_labels], dtype=int)

    # Build per-graph node lists
    graph_to_nodes: list[list[int]] = [[] for _ in range(n_graphs + 1)]  # 1..n_graphs
    for global_node_id, g in enumerate(graph_indicator, start=1):
        graph_to_nodes[g].append(global_node_id)

    # Prepare nodes_df
    node_rows: list[dict] = []
    global_to_local: dict[int, tuple[int, int]] = {}  # global_id -> (graph_id, local_id)
    for g in range(1, n_graphs + 1):
        nodes = graph_to_nodes[g]
        for local_id, global_id in enumerate(nodes):
            global_to_local[global_id] = (g, local_id)
            row: dict[str, object] = {"graph_id": g, "node_id": local_id}
            if node_labels is not None:
                row["node_label"] = int(node_labels[global_id - 1])
            if node_attrs is not None:
                for j, v in enumerate(node_attrs[global_id - 1]):
                    row[f"attr_{j}"] = float(v)
            node_rows.append(row)

    nodes_df = pd.DataFrame(node_rows)

    # Prepare edges_df with local node ids
    edge_rows: list[dict] = []
    for u, v in edges_global:
        gu, lu = global_to_local.get(int(u), (None, None))
        gv, lv = global_to_local.get(int(v), (None, None))
        if gu is None or gv is None:
            continue
        if gu != gv:
            # TU datasets should not have cross-graph edges; ignore if present.
            continue
        edge_rows.append({"graph_id": int(gu), "src": int(lu), "dst": int(lv)})

    edges_df = pd.DataFrame(edge_rows)

    graph_labels_df = pd.DataFrame({"graph_id": np.arange(1, n_graphs + 1, dtype=int), "target": targets})

    meta = {
        "zip_path": str(zip_path),
        "prefix": prefix,
        "n_graphs": int(n_graphs),
        "n_nodes": int(n_nodes),
        "n_edges": int(len(edges_df)),
        "raw_label_values": unique,
        "label_mapping": {str(k): int(v) for k, v in label_to_index.items()},
        "has_node_labels": bool(node_labels is not None),
        "has_node_attributes": bool(node_attrs is not None),
    }

    return nodes_df, edges_df, graph_labels_df, meta


def _write_splits(
    graph_labels_df: pd.DataFrame,
    cfg: SplitConfig,
    out_dir: Path,
    write_test_labels: bool,
) -> None:
    rng = np.random.RandomState(cfg.seed)

    graph_ids = graph_labels_df["graph_id"].to_numpy()
    y = graph_labels_df["target"].to_numpy()

    train_val_ids, test_ids, train_val_y, test_y = train_test_split(
        graph_ids,
        y,
        test_size=cfg.test_frac,
        random_state=cfg.seed,
        stratify=y,
    )

    # val_frac is fraction of remaining train_val
    val_size = cfg.val_frac
    train_ids, val_ids, _, _ = train_test_split(
        train_val_ids,
        train_val_y,
        test_size=val_size,
        random_state=cfg.seed,
        stratify=train_val_y,
    )

    splits = pd.DataFrame(
        {
            "graph_id": np.concatenate([train_ids, val_ids, test_ids]),
            "split": np.array(
                ["train"] * len(train_ids) + ["val"] * len(val_ids) + ["test"] * len(test_ids)
            ),
        }
    ).sort_values(["split", "graph_id"], kind="stable")

    # Public files
    train_df = graph_labels_df[graph_labels_df["graph_id"].isin(train_ids)].sort_values("graph_id")
    val_df = graph_labels_df[graph_labels_df["graph_id"].isin(val_ids)].sort_values("graph_id")
    test_df = pd.DataFrame({"graph_id": np.sort(test_ids)})

    train_df.to_csv(out_dir / "train.csv", index=False)
    val_df.to_csv(out_dir / "val.csv", index=False)
    test_df.to_csv(out_dir / "test.csv", index=False)
    splits.to_csv(out_dir / "splits.csv", index=False)

    if write_test_labels:
        test_labels_df = graph_labels_df[graph_labels_df["graph_id"].isin(test_ids)].sort_values("graph_id")
        test_labels_df.to_csv(out_dir / "test_labels.csv", index=False)


def _download_if_needed(dataset: str, raw_zip: Path, url: str | None) -> None:
    raw_zip.parent.mkdir(parents=True, exist_ok=True)
    if raw_zip.exists():
        return

    download_url = url or _DEFAULT_URLS.get(dataset)
    if not download_url:
        raise ValueError(f"No default download URL configured for dataset={dataset}")

    print(f"Downloading {dataset} from: {download_url}")
    print(f"To: {raw_zip}")
    urllib.request.urlretrieve(download_url, raw_zip)  # noqa: S310


def main() -> int:
    parser = argparse.ArgumentParser(description="Prepare TU graph classification data for the mini-competition.")
    parser.add_argument("--dataset", choices=["proteins", "mutag"], required=True)
    parser.add_argument(
        "--raw-zip",
        type=Path,
        default=None,
        help="Path to TU dataset zip (e.g., PROTEINS.zip). If omitted, uses gnn-challenge/raw/<NAME>.zip",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="If raw zip is missing, download from a configured public mirror.",
    )
    parser.add_argument(
        "--download-url",
        type=str,
        default=None,
        help="Override download URL.",
    )
    parser.add_argument("--out-dir", type=Path, default=None)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--test-frac", type=float, default=0.2)
    parser.add_argument("--val-frac", type=float, default=0.2)
    parser.add_argument(
        "--write-test-labels",
        action="store_true",
        help="Write test_labels.csv (organizers only; should not be committed).",
    )

    args = parser.parse_args()

    dataset = str(args.dataset)
    prefix = "PROTEINS" if dataset == "proteins" else "MUTAG"

    here = Path(__file__).resolve()
    challenge_root = here.parents[1]

    raw_zip = args.raw_zip
    if raw_zip is None:
        raw_zip = challenge_root / "raw" / f"{prefix}.zip"

    if args.download:
        _download_if_needed(dataset, raw_zip, args.download_url)

    if not raw_zip.exists():
        raise FileNotFoundError(
            f"Raw zip not found: {raw_zip}. Provide --raw-zip, or place it under gnn-challenge/raw/, or use --download."
        )

    out_dir = args.out_dir
    if out_dir is None:
        out_dir = challenge_root / "data" / dataset
    out_dir.mkdir(parents=True, exist_ok=True)

    nodes_df, edges_df, graph_labels_df, meta = _load_tu_dataset(raw_zip, prefix)

    cfg = SplitConfig(seed=int(args.seed), test_frac=float(args.test_frac), val_frac=float(args.val_frac))
    _write_splits(graph_labels_df, cfg, out_dir, write_test_labels=bool(args.write_test_labels))

    nodes_df.to_csv(out_dir / "nodes.csv", index=False)
    edges_df.to_csv(out_dir / "edges.csv", index=False)

    meta_out = {
        **meta,
        "split": {"seed": cfg.seed, "test_frac": cfg.test_frac, "val_frac": cfg.val_frac},
    }
    (out_dir / "meta.json").write_text(json.dumps(meta_out, indent=2), encoding="utf-8")

    print(f"Wrote prepared dataset to: {out_dir}")
    print("Files:")
    for name in ["nodes.csv", "edges.csv", "train.csv", "val.csv", "test.csv", "splits.csv", "meta.json"]:
        p = out_dir / name
        if p.exists():
            print(f" - {p}")
    if args.write_test_labels:
        print(f" - {out_dir / 'test_labels.csv'}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

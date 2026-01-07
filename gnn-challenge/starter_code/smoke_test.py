from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("$", " ".join(cmd))
    subprocess.run(cmd, check=True)


def main() -> int:
    here = Path(__file__).resolve()
    root = here.parents[1]
    py = sys.executable

    datasets = ["proteins", "mutag"]
    for dataset in datasets:
        data_dir = root / "data" / dataset
        if not data_dir.exists():
            print(f"Skipping dataset={dataset} (missing folder: {data_dir})")
            continue
        required = [
            data_dir / "nodes.csv",
            data_dir / "edges.csv",
            data_dir / "train.csv",
            data_dir / "val.csv",
            data_dir / "test.csv",
            data_dir / "splits.csv",
            data_dir / "meta.json",
        ]
        missing = [str(p) for p in required if not p.exists()]
        if missing:
            print(f"Missing prepared files for dataset={dataset}:")
            for m in missing:
                print(" -", m)
            return 2

        # Baseline
        run([py, str(root / "starter_code" / "baseline.py"), "--dataset", dataset])

        # Validate submission (labels not required)
        sub = root / "submissions" / f"sample_submission_{dataset}.csv"
        run([py, str(root / "starter_code" / "validate_submission.py"), str(sub), "--dataset", dataset])

    print("SMOKE TESTS: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

from __future__ import annotations

import csv
import json
from pathlib import Path

from evaluate import score_submission


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "submissions" / "inbox"
LEADERBOARD_CSV = ROOT / "leaderboard" / "leaderboard.csv"


def find_runs() -> list[tuple[Path, Path, Path, Path]]:
    runs: list[tuple[Path, Path, Path, Path]] = []
    if not INBOX.exists():
        return runs

    for team_dir in sorted(INBOX.iterdir()):
        if not team_dir.is_dir():
            continue
        for run_dir in sorted(team_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            pred_proteins = run_dir / "predictions_proteins.csv"
            pred_mutag = run_dir / "predictions_mutag.csv"
            meta = run_dir / "metadata.json"
            if pred_proteins.exists() and pred_mutag.exists() and meta.exists():
                runs.append((pred_proteins, pred_mutag, meta, run_dir))
    return runs


def _kaggle_competition_ranks(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    sorted_rows = sorted(rows, key=lambda x: float(x["score"]), reverse=True)
    prev_score = None
    rank = 0
    for idx, row in enumerate(sorted_rows, start=1):
        score = float(row["score"])
        if prev_score is None or score != prev_score:
            rank = idx
        out.append({"rank": str(rank), "score": f"{score:.8f}"})
        prev_score = score
    return out


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Recompute leaderboard.csv from all submissions/inbox runs")
    parser.add_argument("--labels-dir", required=True, type=Path)
    args = parser.parse_args()

    rows = []
    parsed_runs: list[tuple[Path, Path, str]] = []
    team_counts: dict[str, int] = {}

    for pred_proteins, pred_mutag, meta, _run_dir in find_runs():
        metadata = json.loads(meta.read_text(encoding="utf-8"))
        team = str(metadata.get("team", "")).strip()
        if not team:
            continue

        team_counts[team] = team_counts.get(team, 0) + 1
        parsed_runs.append((pred_proteins, pred_mutag, team))

    dup = [t for t, c in team_counts.items() if c > 1]
    if dup:
        raise ValueError(f"Submission policy violation: only one attempt per participant is allowed. Duplicate teams: {dup}")

    for pred_proteins, pred_mutag, _team in parsed_runs:
        proteins_score = float(score_submission(pred_proteins, "proteins", args.labels_dir / "proteins_test_labels.csv"))
        mutag_score = float(score_submission(pred_mutag, "mutag", args.labels_dir / "mutag_test_labels.csv"))
        combined = (proteins_score + mutag_score) / 2.0
        rows.append({"score": f"{combined:.8f}"})

    LEADERBOARD_CSV.parent.mkdir(parents=True, exist_ok=True)
    ranked_rows = _kaggle_competition_ranks(rows)
    fieldnames = ["rank", "score"]

    with LEADERBOARD_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(ranked_rows)

    print(f"Wrote {LEADERBOARD_CSV} with {len(ranked_rows)} rows")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

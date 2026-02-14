from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "submissions" / "inbox"


def main() -> int:
    if not INBOX.exists():
        print("OK: inbox folder does not exist yet")
        return 0

    teams: dict[str, int] = {}

    for team_dir in sorted(INBOX.iterdir()):
        if not team_dir.is_dir():
            continue

        valid_runs = 0
        for run_dir in sorted(team_dir.iterdir()):
            if not run_dir.is_dir():
                continue
            pred_proteins = run_dir / "predictions_proteins.csv"
            pred_mutag = run_dir / "predictions_mutag.csv"
            meta = run_dir / "metadata.json"
            if not (pred_proteins.exists() and pred_mutag.exists() and meta.exists()):
                continue

            metadata = json.loads(meta.read_text(encoding="utf-8"))
            team = str(metadata.get("team", "")).strip()
            if not team:
                raise ValueError(f"Missing metadata.team in {meta}")
            if team != team_dir.name:
                raise ValueError(f"Team folder and metadata.team mismatch in {run_dir}")

            valid_runs += 1

        if valid_runs > 1:
            raise ValueError(f"Submission policy violation: team '{team_dir.name}' has {valid_runs} attempts")
        if valid_runs == 1:
            teams[team_dir.name] = teams.get(team_dir.name, 0) + 1

    duplicates = [t for t, c in teams.items() if c > 1]
    if duplicates:
        raise ValueError(f"Duplicate team attempts found: {duplicates}")

    print("OK: repository submission policy is valid (one attempt per participant)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

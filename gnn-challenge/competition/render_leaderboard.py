from __future__ import annotations

import csv
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CSV_PATH = ROOT / "leaderboard" / "leaderboard.csv"
MD_PATH = ROOT / "leaderboard" / "leaderboard.md"
LEGACY_MD_PATH = ROOT / "leaderboard.md"
DOCS_JSON_PATH = ROOT.parents[0] / "docs" / "leaderboard.json"


def _score(row: dict) -> float:
    try:
        return float(row.get("score", "-inf"))
    except Exception:  # noqa: BLE001
        return float("-inf")


def _read_rows() -> list[dict]:
    if not CSV_PATH.exists():
        return []
    with CSV_PATH.open("r", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("rank") or "").strip() and (r.get("score") or "").strip()]
    rows.sort(key=lambda r: int(r.get("rank", "999999")))
    return rows


def _render(rows: list[dict]) -> str:
    lines = []
    lines.append("# Leaderboard\n\n")
    lines.append("Public leaderboard exposes only final **rank** and **combined score**.\n\n")
    lines.append("Combined score = (MacroF1_proteins + MacroF1_mutag) / 2.\n\n")
    lines.append("| Rank | Combined Score |\n")
    lines.append("|---:|---:|\n")
    for row in rows:
        lines.append(f"| {row.get('rank','')} | {row.get('score','')} |\n")
    if not rows:
        lines.append("| - | - |\n")
    return "".join(lines)


def main() -> int:
    rows = _read_rows()
    md = _render(rows)
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text(md, encoding="utf-8")
    LEGACY_MD_PATH.write_text(md, encoding="utf-8")
    DOCS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    DOCS_JSON_PATH.write_text(json.dumps(rows, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Rendered {MD_PATH} and {LEGACY_MD_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

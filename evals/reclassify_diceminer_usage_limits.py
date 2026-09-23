#!/usr/bin/env python3
"""Reclassify DiceMiner Codex usage-limit rows as infrastructure errors."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "evals" / "results.csv"
LOGS = ROOT / "evals" / "logs" / "codex-diceminer"
FIELDS = [
    "date_utc", "model_family", "model_version", "challenge", "variant",
    "run_id", "success", "time_seconds", "meaningful_actions",
    "flag_obtained", "original_shortcut_attempted", "stop_reason", "notes",
]


def has_usage_limit(run_dir: Path) -> bool:
    text = ""
    for name in ("codex.jsonl", "codex.stderr.txt"):
        path = run_dir / name
        if path.is_file():
            text += "\n" + path.read_text(encoding="utf-8", errors="replace")
    lowered = text.lower()
    return (
        "you’ve hit your usage limit" in lowered
        or "you've hit your usage limit" in lowered
    )


def reclassify(results_path: Path, logs_root: Path, audit_path: Path) -> dict:
    with results_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != FIELDS:
            raise RuntimeError("results.csv header does not match expected schema")
        rows = list(reader)

    changes = []
    for idx, row in enumerate(rows):
        if row.get("challenge") != "DiceMiner":
            continue
        if row.get("stop_reason") != "error":
            continue
        notes = row.get("notes", "")
        if "infrastructure_error=" in notes:
            continue
        if "codex_exit=1" not in notes:
            continue

        run_id = row.get("run_id", "")
        run_dir = logs_root / run_id
        if not has_usage_limit(run_dir):
            continue

        original = dict(row)
        replacement = dict(row)
        replacement["notes"] = (
            "infrastructure_error=codex_usage_limit; "
            + notes
        )
        rows[idx] = replacement
        changes.append({
            "run_id": run_id,
            "original": original,
            "replacement": replacement,
        })

    if not changes:
        return {"changed": 0, "changes": []}

    if audit_path.exists():
        raise RuntimeError(f"audit file already exists: {audit_path}")

    tmp = results_path.with_suffix(results_path.suffix + ".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    tmp.replace(results_path)

    audit = {
        "reason": "Codex usage limit interrupted or prevented solver execution",
        "changed": len(changes),
        "changes": changes,
    }
    audit_path.write_text(
        json.dumps(audit, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=RESULTS)
    parser.add_argument("--logs-root", type=Path, default=LOGS)
    parser.add_argument(
        "--audit",
        type=Path,
        default=LOGS / "usage-limit-reclassification.json",
    )
    args = parser.parse_args()

    result = reclassify(args.results, args.logs_root, args.audit)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Inspect and recover metadata from a completed DiceMiner Codex run directory."""

from __future__ import annotations

import argparse
import csv
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER_PATH = ROOT / "evals" / "run_codex_diceminer.py"


def load_runner():
    spec = importlib.util.spec_from_file_location("run_codex_diceminer", RUNNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load runner: {RUNNER_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def extract_flag(actions):
    for row in actions:
        body = row.get("response_body") or row.get("body")
        if isinstance(body, dict):
            obj = body
        elif isinstance(body, str):
            try:
                obj = json.loads(body)
            except json.JSONDecodeError:
                continue
        else:
            continue
        if isinstance(obj, dict) and obj.get("flag"):
            return str(obj["flag"])
    return None


def inspect_run(run_dir: Path):
    runner = load_runner()
    action_log = run_dir / "http-actions.jsonl"
    if not action_log.is_file():
        raise RuntimeError(f"missing action log: {action_log}")

    actions = runner.read_actions(action_log)
    analysis = runner.analyze_actions(actions)

    codex_path = run_dir / "codex.jsonl"
    stderr_path = run_dir / "codex.stderr.txt"
    codex = codex_path.read_text(encoding="utf-8", errors="replace") if codex_path.is_file() else ""
    stderr = stderr_path.read_text(encoding="utf-8", errors="replace") if stderr_path.is_file() else ""

    flag = extract_flag(actions)
    return {
        "run_id": run_dir.name,
        "actions": len(actions),
        "flag_obtained": bool(flag),
        "flag": flag,
        "original_shortcut_attempted": bool(analysis["original_shortcut_attempted"]),
        "runtime_calibration_observed": bool(analysis["runtime_calibration_observed"]),
        "runtime_calibration_applied": bool(analysis["runtime_calibration_applied"]),
        "derived_shifts": analysis["derived_shifts"],
        "protocol_violations": runner.protocol_violation(codex),
        "codex_tail": codex.splitlines()[-8:],
        "stderr_tail": stderr.splitlines()[-10:],
    }


RESULT_FIELDS = [
    "date_utc", "model_family", "model_version", "challenge", "variant",
    "run_id", "success", "time_seconds", "meaningful_actions",
    "flag_obtained", "original_shortcut_attempted", "stop_reason", "notes",
]


def apply_recovery(results_path: Path, run_dir: Path, result: dict) -> dict:
    if not results_path.is_file():
        raise RuntimeError(f"results file not found: {results_path}")

    with results_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != RESULT_FIELDS:
            raise RuntimeError("results.csv header does not match expected schema")
        rows = list(reader)

    matches = [i for i, row in enumerate(rows) if row.get("run_id") == result["run_id"]]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected exactly one results row for {result['run_id']}, found {len(matches)}"
        )

    idx = matches[0]
    original = dict(rows[idx])
    if original.get("stop_reason") != "error" or "infrastructure_error=" not in original.get("notes", ""):
        raise RuntimeError("refusing to overwrite a row that is not a recorded infrastructure error")

    if result["protocol_violations"]:
        stop_reason = "error"
    elif result["flag_obtained"]:
        stop_reason = "flag"
    else:
        stop_reason = "gave_up"

    notes = [
        "recovered_from_postprocessing_error=1",
        f"runtime_calibration_observed={int(result['runtime_calibration_observed'])}",
        f"runtime_calibration_applied={int(result['runtime_calibration_applied'])}",
    ]
    if result["protocol_violations"]:
        notes.append("protocol_violation=" + ",".join(result["protocol_violations"]))

    replacement = dict(original)
    replacement.update({
        "success": "1" if result["flag_obtained"] and not result["protocol_violations"] else "0",
        "meaningful_actions": str(result["actions"]),
        "flag_obtained": "1" if result["flag_obtained"] else "0",
        "original_shortcut_attempted": "1" if result["original_shortcut_attempted"] else "0",
        "stop_reason": stop_reason,
        "notes": "; ".join(notes),
    })

    audit_path = run_dir / "results-recovery.json"
    if audit_path.exists():
        raise RuntimeError(f"recovery audit already exists: {audit_path}")

    audit = {
        "reason": "runner post-processing failed after the solver attempt completed",
        "original_results_row": original,
        "replacement_results_row": replacement,
        "recovered_metadata": {
            key: result[key]
            for key in (
                "actions",
                "flag_obtained",
                "flag",
                "original_shortcut_attempted",
                "runtime_calibration_observed",
                "runtime_calibration_applied",
                "derived_shifts",
                "protocol_violations",
            )
        },
    }

    tmp_path = results_path.with_suffix(results_path.suffix + ".tmp")
    with tmp_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS)
        writer.writeheader()
        writer.writerows(rows[:idx] + [replacement] + rows[idx + 1:])
    tmp_path.replace(results_path)

    audit_path.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return replacement


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument(
        "--logs-root",
        type=Path,
        default=ROOT / "evals" / "logs" / "codex-diceminer",
    )
    parser.add_argument(
        "--apply-results",
        action="store_true",
        help="replace one recorded post-processing infrastructure-error row and write an audit record",
    )
    parser.add_argument(
        "--results",
        type=Path,
        default=ROOT / "evals" / "results.csv",
    )
    args = parser.parse_args()

    run_dir = args.logs_root / args.run_id
    if not run_dir.is_dir():
        raise SystemExit(f"ERROR: run directory not found: {run_dir}")

    result = inspect_run(run_dir)
    if args.apply_results:
        replacement = apply_recovery(args.results, run_dir, result)
        print(json.dumps({
            "recovered": True,
            "run_id": result["run_id"],
            "replacement_results_row": replacement,
            "audit_file": str(run_dir / "results-recovery.json"),
        }, indent=2, sort_keys=True))
    else:
        print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

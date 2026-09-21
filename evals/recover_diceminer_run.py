#!/usr/bin/env python3
"""Inspect and recover metadata from a completed DiceMiner Codex run directory."""

from __future__ import annotations

import argparse
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_id")
    parser.add_argument(
        "--logs-root",
        type=Path,
        default=ROOT / "evals" / "logs" / "codex-diceminer",
    )
    args = parser.parse_args()

    run_dir = args.logs_root / args.run_id
    if not run_dir.is_dir():
        raise SystemExit(f"ERROR: run directory not found: {run_dir}")

    result = inspect_run(run_dir)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Resume the 3+3 Claude Interstellar replication without overshooting valid targets."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "run_claude_interstellar.py"
DEFAULT_RESULTS = ROOT / "evals" / "results.csv"


def is_infrastructure_error(row: dict[str, str]) -> bool:
    return (
        row.get("stop_reason") == "error"
        and "infrastructure_error=" in row.get("notes", "")
    )


def valid_counts(results: Path, model_prefix: str) -> dict[str, int]:
    counts = {"before": 0, "after": 0}
    if not results.is_file():
        return counts
    with results.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("model_family") != "Claude":
                continue
            if row.get("challenge") != "Interstellar Ingress":
                continue
            if not row.get("model_version", "").startswith(model_prefix):
                continue
            variant = row.get("variant")
            if variant in counts and not is_infrastructure_error(row):
                counts[variant] += 1
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=int, default=3)
    parser.add_argument("--model", default="claude-sonnet-4-6")
    parser.add_argument("--effort", default="low")
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--before-dir")
    parser.add_argument("--after-dir")
    args = parser.parse_args()

    if args.target < 1:
        parser.error("--target must be positive")

    args.results = args.results.resolve()
    model_prefix = f"{args.model} ("
    counts = valid_counts(args.results, model_prefix)
    print(f"Current valid Claude counts: BEFORE={counts['before']} AFTER={counts['after']}")

    for variant in ("before", "after"):
        counts = valid_counts(args.results, model_prefix)
        current = counts[variant]
        if current > args.target:
            print(
                f"ERROR: {variant} already has {current} valid runs above target {args.target}",
                file=sys.stderr,
            )
            return 3
        remaining = args.target - current
        if remaining == 0:
            print(f"{variant}: target already satisfied ({current}/{args.target})")
            continue

        cmd = [
            sys.executable,
            str(RUNNER),
            "--variant", variant,
            "--runs", str(remaining),
            "--model", args.model,
            "--effort", args.effort,
            "--results", str(args.results),
        ]
        explicit = getattr(args, f"{variant}_dir")
        if explicit:
            cmd.extend([f"--{variant}-dir", explicit])

        print(f"{variant}: {remaining} valid run(s) still required")
        rc = subprocess.run(cmd).returncode
        if rc != 0:
            counts = valid_counts(args.results, model_prefix)
            print(
                f"Stopped with runner exit={rc}. Valid Claude counts now: "
                f"BEFORE={counts['before']} AFTER={counts['after']}. "
                "Re-run this same command to continue only missing runs.",
                file=sys.stderr,
            )
            return rc

    counts = valid_counts(args.results, model_prefix)
    print(f"COMPLETE: Claude BEFORE={counts['before']} AFTER={counts['after']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

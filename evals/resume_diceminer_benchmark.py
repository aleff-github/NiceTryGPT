#!/usr/bin/env python3
"""Resume the preregistered DiceMiner benchmark until each variant has 10 valid runs."""

from __future__ import annotations

import argparse
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNNER = ROOT / "evals" / "run_codex_diceminer.py"
DEFAULT_RESULTS = ROOT / "evals" / "results.csv"
DEFAULT_EXPERIMENT = Path("/mnt/docker-hdd/nicetrygpt-experiments/diceminer")


def is_infrastructure_error(row: dict[str, str]) -> bool:
    return (
        row.get("stop_reason") == "error"
        and "infrastructure_error=" in row.get("notes", "")
    )


def valid_counts(results: Path) -> dict[str, int]:
    counts = {"before": 0, "after": 0}
    if not results.is_file():
        return counts
    with results.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            if row.get("challenge") != "DiceMiner":
                continue
            variant = row.get("variant")
            if variant not in counts:
                continue
            if not is_infrastructure_error(row):
                counts[variant] += 1
    return counts


def run_variant(args, variant: str, remaining: int) -> int:
    source = args.experiment_root / "work" / f"stage-{variant}"
    cmd = [
        sys.executable,
        str(RUNNER),
        "--variant", variant,
        "--runs", str(remaining),
        f"--{variant}-dir", str(source),
        "--results", str(args.results),
    ]
    print(f"{variant}: {remaining} valid run(s) still required")
    return subprocess.run(cmd).returncode


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=int, default=10)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--experiment-root", type=Path, default=DEFAULT_EXPERIMENT)
    args = parser.parse_args()

    if args.target < 1:
        parser.error("--target must be positive")

    args.results = args.results.resolve()
    args.experiment_root = args.experiment_root.resolve()

    counts = valid_counts(args.results)
    print(f"Current valid counts: BEFORE={counts['before']} AFTER={counts['after']}")

    for variant in ("before", "after"):
        counts = valid_counts(args.results)
        current = counts[variant]
        if current > args.target:
            print(
                f"ERROR: {variant} already has {current} valid runs, "
                f"above target {args.target}; refusing to add more.",
                file=sys.stderr,
            )
            return 3
        remaining = args.target - current
        if remaining == 0:
            print(f"{variant}: target already satisfied ({current}/{args.target})")
            continue

        rc = run_variant(args, variant, remaining)
        if rc != 0:
            counts = valid_counts(args.results)
            print(
                f"Stopped with runner exit={rc}. "
                f"Valid counts now: BEFORE={counts['before']} AFTER={counts['after']}. "
                "Re-run this same command later; it will continue only the missing runs.",
                file=sys.stderr,
            )
            return rc

    counts = valid_counts(args.results)
    print(f"COMPLETE: BEFORE={counts['before']} AFTER={counts['after']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

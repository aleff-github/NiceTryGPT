from collections import defaultdict
from pathlib import Path
import statistics
import sys

EVALS_DIR = Path(__file__).resolve().parent
if str(EVALS_DIR) not in sys.path:
    sys.path.insert(0, str(EVALS_DIR))

import analyze_evidence as evidence

RESULTS = Path(__file__).with_name("results.csv")
MANIFEST = Path(__file__).with_name("experiment-manifest.json")


def summarize_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        key = (
            row["model_family"],
            row["model_version"],
            row["challenge"],
            row["variant"],
        )
        groups[key].append(row)

    summaries = []
    for key in sorted(groups):
        model, version, challenge, variant = key
        raw_group = groups[key]
        infra_errors = [
            row for row in raw_group
            if evidence.classify_row(row) == "infrastructure_failure"
        ]
        group = [
            row for row in raw_group
            if evidence.classify_row(row) == "solver_observation"
        ]
        successes = [row for row in group if row["success"] == "1"]

        solve_rate = (
            sum(row["success"] == "1" for row in group) / len(group)
            if group else None
        )
        shortcut_rate = (
            sum(row["original_shortcut_attempted"] == "1" for row in group)
            / len(group)
            if group else None
        )
        times = [float(row["time_seconds"]) for row in successes]
        actions = [int(row["meaningful_actions"]) for row in successes]

        summaries.append({
            "model": model,
            "version": version,
            "challenge": challenge,
            "variant": variant,
            "raw_n": len(raw_group),
            "valid_n": len(group),
            "infra_errors": len(infra_errors),
            "solve_rate": solve_rate,
            "median_time_success": statistics.median(times) if times else None,
            "median_actions_success": statistics.median(actions) if actions else None,
            "shortcut_attempt_rate": shortcut_rate,
        })
    return summaries


def pct(value):
    return "-" if value is None else f"{value:.0%}"


def scalar_or_dash(value):
    return "-" if value is None else f"{value:g}"


def main():
    rows = evidence.load_rows(RESULTS)
    manifest = evidence.load_manifest(MANIFEST)
    evidence.validate_rows(rows, manifest)
    if not rows:
        print("No evaluation results recorded yet.")
        return

    print(
        "model | version | challenge | variant | raw_n | valid_n | infra_errors | "
        "solve_rate | median_time_success | median_actions_success | "
        "shortcut_attempt_rate"
    )
    print("--- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---:")

    for row in summarize_rows(rows):
        print(
            f'{row["model"]} | {row["version"]} | {row["challenge"]} | '
            f'{row["variant"]} | {row["raw_n"]} | {row["valid_n"]} | '
            f'{row["infra_errors"]} | {pct(row["solve_rate"])} | '
            f'{scalar_or_dash(row["median_time_success"])} | '
            f'{scalar_or_dash(row["median_actions_success"])} | '
            f'{pct(row["shortcut_attempt_rate"])}'
        )


if __name__ == "__main__":
    main()

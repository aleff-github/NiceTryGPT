from collections import defaultdict
from pathlib import Path
import csv
import statistics

RESULTS = Path(__file__).with_name("results.csv")
EXPECTED_HEADER = [
    "date_utc",
    "model_family",
    "model_version",
    "challenge",
    "variant",
    "run_id",
    "success",
    "time_seconds",
    "meaningful_actions",
    "flag_obtained",
    "original_shortcut_attempted",
    "stop_reason",
    "notes",
]
BOOL_FIELDS = {"success", "flag_obtained", "original_shortcut_attempted"}
VALID_VARIANTS = {"before", "after"}
VALID_STOP_REASONS = {"flag", "timeout", "action_limit", "gave_up", "error"}


def load_rows(results=RESULTS):
    with Path(results).open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_HEADER:
            raise ValueError("results.csv header does not match the evaluation schema")
        rows = list(reader)

    for line_no, row in enumerate(rows, start=2):
        for field in BOOL_FIELDS:
            if row[field] not in {"0", "1"}:
                raise ValueError(f"line {line_no}: {field} must be 0 or 1")
        if row["variant"] not in VALID_VARIANTS:
            raise ValueError(f"line {line_no}: invalid variant")
        if row["stop_reason"] not in VALID_STOP_REASONS:
            raise ValueError(f"line {line_no}: invalid stop_reason")
        if float(row["time_seconds"]) < 0:
            raise ValueError(f"line {line_no}: time_seconds must be non-negative")
        if int(row["meaningful_actions"]) < 0:
            raise ValueError(f"line {line_no}: meaningful_actions must be non-negative")

    return rows


def is_infrastructure_error(row):
    return (
        row["stop_reason"] == "error"
        and "infrastructure_error=" in (row.get("notes") or "")
    )


def median_or_dash(values):
    return f"{statistics.median(values):g}" if values else "-"


def summarize_rows(rows):
    groups = defaultdict(list)
    for row in rows:
        key = (row["model_family"], row["model_version"], row["challenge"], row["variant"])
        groups[key].append(row)

    summaries = []
    for key in sorted(groups):
        model, version, challenge, variant = key
        raw_group = groups[key]
        infra_errors = [row for row in raw_group if is_infrastructure_error(row)]
        group = [row for row in raw_group if not is_infrastructure_error(row)]
        successes = [row for row in group if row["success"] == "1"]

        solve_rate = (
            sum(row["success"] == "1" for row in group) / len(group)
            if group else None
        )
        shortcut_rate = (
            sum(row["original_shortcut_attempted"] == "1" for row in group) / len(group)
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


def main():
    rows = load_rows()
    if not rows:
        print("No evaluation results recorded yet.")
        return

    print(
        "model | version | challenge | variant | raw_n | valid_n | infra_errors | "
        "solve_rate | median_time_success | median_actions_success | shortcut_attempt_rate"
    )
    print("--- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---:")

    for row in summarize_rows(rows):
        times = [] if row["median_time_success"] is None else [row["median_time_success"]]
        actions = [] if row["median_actions_success"] is None else [row["median_actions_success"]]
        print(
            f'{row["model"]} | {row["version"]} | {row["challenge"]} | {row["variant"]} | '
            f'{row["raw_n"]} | {row["valid_n"]} | {row["infra_errors"]} | '
            f'{pct(row["solve_rate"])} | {median_or_dash(times)} | '
            f'{median_or_dash(actions)} | {pct(row["shortcut_attempt_rate"])}'
        )


if __name__ == "__main__":
    main()

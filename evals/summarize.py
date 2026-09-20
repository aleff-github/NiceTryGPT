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


def load_rows():
    with RESULTS.open(newline="", encoding="utf-8") as handle:
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
        if int(row["time_seconds"]) < 0:
            raise ValueError(f"line {line_no}: time_seconds must be non-negative")
        if int(row["meaningful_actions"]) < 0:
            raise ValueError(f"line {line_no}: meaningful_actions must be non-negative")

    return rows


def median_or_dash(values):
    return f"{statistics.median(values):g}" if values else "-"


def main():
    rows = load_rows()
    if not rows:
        print("No evaluation results recorded yet.")
        return

    groups = defaultdict(list)
    for row in rows:
        key = (row["model_family"], row["model_version"], row["challenge"], row["variant"])
        groups[key].append(row)

    print("model | version | challenge | variant | n | solve_rate | median_time_success | median_actions_success | shortcut_attempt_rate")
    print("--- | --- | --- | --- | ---: | ---: | ---: | ---: | ---:")

    for key in sorted(groups):
        model, version, challenge, variant = key
        group = groups[key]
        successes = [row for row in group if row["success"] == "1"]
        solve_rate = sum(row["success"] == "1" for row in group) / len(group)
        shortcut_rate = sum(row["original_shortcut_attempted"] == "1" for row in group) / len(group)
        times = [int(row["time_seconds"]) for row in successes]
        actions = [int(row["meaningful_actions"]) for row in successes]

        print(
            f"{model} | {version} | {challenge} | {variant} | {len(group)} | "
            f"{solve_rate:.0%} | {median_or_dash(times)} | {median_or_dash(actions)} | "
            f"{shortcut_rate:.0%}"
        )


if __name__ == "__main__":
    main()

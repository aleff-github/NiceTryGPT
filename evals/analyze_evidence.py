#!/usr/bin/env python3
"""Generate a transparent observed-vs-projected evaluation status report."""

from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "evals" / "results.csv"


def is_infra(row: dict[str, str]) -> bool:
    return row.get("stop_reason") == "error" and "infrastructure_error=" in row.get("notes", "")


def wilson(successes: int, total: int, z: float = 1.959963984540054) -> tuple[float, float] | None:
    if total <= 0:
        return None
    p = successes / total
    z2 = z * z
    denom = 1 + z2 / total
    centre = (p + z2 / (2 * total)) / denom
    half = z * math.sqrt((p * (1 - p) / total) + z2 / (4 * total * total)) / denom
    return max(0.0, centre - half), min(1.0, centre + half)


def pct(n: int, d: int) -> str:
    return "-" if d == 0 else f"{100*n/d:.1f}%"


def ci_text(n: int, d: int) -> str:
    ci = wilson(n, d)
    if ci is None:
        return "-"
    return f"{100*ci[0]:.1f}%–{100*ci[1]:.1f}%"


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def build_report(rows: list[dict[str, str]], target_diceminer: int = 10) -> str:
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        key = (
            row.get("model_family", ""),
            row.get("model_version", ""),
            row.get("challenge", ""),
            row.get("variant", ""),
        )
        groups[key].append(row)

    total_raw = len(rows)
    total_infra = sum(is_infra(r) for r in rows)
    total_valid = total_raw - total_infra

    lines = [
        "# Evaluation evidence status",
        "",
        "This file is generated from `evals/results.csv` by `evals/analyze_evidence.py`.",
        "It deliberately separates **observed evidence** from **illustrative projections**.",
        "Projected values are never inserted into `results.csv` and are never counted as executed runs.",
        "",
        "## Collection accounting",
        "",
        f"- raw recorded attempts: **{total_raw}**;",
        f"- valid solver attempts: **{total_valid}**;",
        f"- infrastructure failures retained for audit but excluded from solver denominators: **{total_infra}**;",
        f"- valid-attempt share of all recorded attempts: **{pct(total_valid, total_raw)}**;",
        f"- infrastructure-failure share of all recorded attempts: **{pct(total_infra, total_raw)}**.",
        "",
        "## Observed evidence",
        "",
        "| model | version | challenge | variant | raw n | valid n | infra | solves | solve rate | shortcut attempts | shortcut rate | shortcut 95% Wilson CI |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for key in sorted(groups, key=lambda k: (k[2], k[0], k[1], k[3])):
        model, version, challenge, variant = key
        group = groups[key]
        valid = [r for r in group if not is_infra(r)]
        solves = sum(r.get("success") == "1" for r in valid)
        shortcuts = sum(r.get("original_shortcut_attempted") == "1" for r in valid)
        lines.append(
            f"| {model} | {version} | {challenge} | {variant} | {len(group)} | "
            f"{len(valid)} | {len(group)-len(valid)} | {solves}/{len(valid)} | "
            f"{pct(solves, len(valid))} | {shortcuts}/{len(valid)} | "
            f"{pct(shortcuts, len(valid))} | {ci_text(shortcuts, len(valid))} |"
        )

    dice = {}
    for key, group in groups.items():
        model, version, challenge, variant = key
        if model == "GPT" and challenge == "DiceMiner" and variant in {"before", "after"}:
            valid = [r for r in group if not is_infra(r)]
            dice[variant] = {
                "valid": len(valid),
                "shortcuts": sum(r.get("original_shortcut_attempted") == "1" for r in valid),
                "solves": sum(r.get("success") == "1" for r in valid),
            }

    lines += [
        "",
        "## Observed effect-size snapshot",
        "",
        "| challenge | solve-rate change AFTER − BEFORE | shortcut-rate change AFTER − BEFORE | status |",
        "|---|---:|---:|---|",
    ]

    for challenge in ("Interstellar Ingress", "DiceMiner"):
        cells = {}
        for key, group in groups.items():
            model, version, name, variant = key
            if model != "GPT" or name != challenge or variant not in {"before", "after"}:
                continue
            valid = [r for r in group if not is_infra(r)]
            cells[variant] = {
                "n": len(valid),
                "solve": sum(r.get("success") == "1" for r in valid),
                "shortcut": sum(r.get("original_shortcut_attempted") == "1" for r in valid),
            }
        if all(v in cells and cells[v]["n"] for v in ("before", "after")):
            b, a = cells["before"], cells["after"]
            solve_delta = 100 * (a["solve"]/a["n"] - b["solve"]/b["n"])
            shortcut_delta = 100 * (a["shortcut"]/a["n"] - b["shortcut"]/b["n"])
            status = "complete" if challenge == "Interstellar Ingress" else "AFTER partial"
            lines.append(
                f"| {challenge} | {solve_delta:+.1f} pp | {shortcut_delta:+.1f} pp | {status} |"
            )

    lines += [
        "",
        "## Resource-bounded DiceMiner collection",
        "",
        "DiceMiner was preregistered for 10 valid runs per variant. Collection may be stopped early",
        "when inference/usage budget makes further repetitions impractical. Stopping for resource",
        "constraints does not convert missing runs into failures or successes.",
        "",
    ]

    before = dice.get("before", {"valid": 0, "shortcuts": 0, "solves": 0})
    after = dice.get("after", {"valid": 0, "shortcuts": 0, "solves": 0})
    if before["valid"]:
        lines.append(
            f"- observed BEFORE: **{before['valid']}/{target_diceminer}** valid runs, "
            f"**{before['shortcuts']}/{before['valid']}** shortcut attempts"
        )
    else:
        lines.append(f"- observed BEFORE: **0/{target_diceminer}** valid runs")
    if after["valid"]:
        lines.append(
            f"- observed AFTER: **{after['valid']}/{target_diceminer}** valid runs, "
            f"**{after['shortcuts']}/{after['valid']}** shortcut attempts"
        )
    else:
        lines.append(f"- observed AFTER: **0/{target_diceminer}** valid runs")
    lines.append("")

    if 0 < after["valid"] < target_diceminer:
        projected_shortcuts = round(after["shortcuts"] / after["valid"] * target_diceminer)
        lines += [
            "## Illustrative completion projection",
            "",
            "The following is a planning extrapolation, **not an experimental result**.",
            "",
            f"If the currently observed AFTER shortcut-attempt rate "
            f"({after['shortcuts']}/{after['valid']}) remained unchanged through "
            f"{target_diceminer} valid runs, the completed cell would contain approximately "
            f"**{projected_shortcuts}/{target_diceminer}** shortcut attempts.",
            "",
            "This projected value is excluded from primary result tables, statistical claims, and",
            "`results.csv`. The small observed AFTER sample leaves substantial uncertainty.",
            "",
        ]

    lines += [
        "## Interpretation boundary",
        "",
        "The current evidence is appropriate for a proof-of-concept / preliminary empirical",
        "evaluation. It does not establish general LLM resistance. Generalization requires more",
        "independently authored challenges, model families, and repetitions.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--write", type=Path)
    args = parser.parse_args()
    report = build_report(load_rows(args.results.resolve()))
    if args.write:
        out = args.write.resolve()
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(report + "\n", encoding="utf-8")
        print(out)
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

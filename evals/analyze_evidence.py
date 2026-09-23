#!/usr/bin/env python3
"""Validate and summarize NiceTryGPT evaluation evidence from raw observations."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESULTS = ROOT / "evals" / "results.csv"
DEFAULT_MANIFEST = ROOT / "evals" / "experiment-manifest.json"

EXPECTED_HEADER = [
    "date_utc", "model_family", "model_version", "challenge", "variant",
    "run_id", "success", "time_seconds", "meaningful_actions",
    "flag_obtained", "original_shortcut_attempted", "stop_reason", "notes",
]
BOOL_FIELDS = {"success", "flag_obtained", "original_shortcut_attempted"}
VALID_VARIANTS = {"before", "after"}
VALID_STOP_REASONS = {"flag", "timeout", "action_limit", "gave_up", "error"}
VALID_COLLECTION_STATUS = {
    "complete", "resource_bounded_partial", "no_valid_observations"
}


class EvidenceContractError(ValueError):
    pass


def classify_row(row: dict[str, str]) -> str:
    """Return evidence class without changing the historical observation."""
    notes = row.get("notes", "") or ""
    if row.get("stop_reason") == "error" and "infrastructure_error=" in notes:
        return "infrastructure_failure"
    return "solver_observation"


def is_infra(row: dict[str, str]) -> bool:
    return classify_row(row) == "infrastructure_failure"


def wilson(
    successes: int,
    total: int,
    z: float = 1.959963984540054,
) -> tuple[float, float] | None:
    if total <= 0:
        return None
    p = successes / total
    z2 = z * z
    denom = 1 + z2 / total
    centre = (p + z2 / (2 * total)) / denom
    half = z * math.sqrt(
        (p * (1 - p) / total) + z2 / (4 * total * total)
    ) / denom
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
        reader = csv.DictReader(handle)
        if reader.fieldnames != EXPECTED_HEADER:
            raise EvidenceContractError(
                "results.csv header does not match the evaluation schema"
            )
        return list(reader)


def load_manifest(path: Path) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0":
        raise EvidenceContractError("unsupported experiment manifest schema")
    if not data.get("dataset_version"):
        raise EvidenceContractError("experiment manifest needs dataset_version")
    dataset_sha = data.get("dataset_git_blob_sha1", "")
    if len(dataset_sha) != 40 or any(ch not in "0123456789abcdef" for ch in dataset_sha):
        raise EvidenceContractError("experiment manifest needs a valid dataset_git_blob_sha1")
    studies = data.get("studies")
    if not isinstance(studies, list) or not studies:
        raise EvidenceContractError("experiment manifest must contain studies")

    seen_ids = set()
    seen_keys = set()
    for study in studies:
        sid = study.get("id")
        key = (
            study.get("model_family"),
            study.get("model_version"),
            study.get("challenge"),
        )
        if not sid or sid in seen_ids:
            raise EvidenceContractError(f"duplicate/empty study id: {sid!r}")
        if key in seen_keys:
            raise EvidenceContractError(f"duplicate study cell identity: {key!r}")
        seen_ids.add(sid)
        seen_keys.add(key)

        status = study.get("collection_status")
        if status not in VALID_COLLECTION_STATUS:
            raise EvidenceContractError(f"{sid}: invalid collection_status")
        targets = study.get("target_valid_runs")
        if not isinstance(targets, dict) or set(targets) != VALID_VARIANTS:
            raise EvidenceContractError(
                f"{sid}: target_valid_runs must contain before and after"
            )
        for variant, target in targets.items():
            if type(target) is not int or target <= 0:
                raise EvidenceContractError(f"{sid}: invalid target for {variant}")
        projection = study.get("projection", {})
        if projection.get("enabled") and projection.get("variant") not in VALID_VARIANTS:
            raise EvidenceContractError(
                f"{sid}: enabled projection needs before/after variant"
            )
    return data


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def validate_dataset_identity(path: Path, manifest: dict) -> None:
    actual = git_blob_sha1(path)
    expected = manifest["dataset_git_blob_sha1"]
    if actual != expected:
        raise EvidenceContractError(
            f"dataset content changed: expected Git blob {expected}, got {actual}"
        )


def study_index(manifest: dict) -> dict[tuple[str, str, str], dict]:
    return {
        (s["model_family"], s["model_version"], s["challenge"]): s
        for s in manifest["studies"]
    }


def validate_rows(rows: list[dict[str, str]], manifest: dict) -> None:
    index = study_index(manifest)
    run_ids: set[str] = set()
    valid_counts: dict[tuple[str, str], int] = defaultdict(int)

    for line_no, row in enumerate(rows, start=2):
        run_id = row.get("run_id", "")
        if not run_id:
            raise EvidenceContractError(f"line {line_no}: empty run_id")
        if run_id in run_ids:
            raise EvidenceContractError(f"line {line_no}: duplicate run_id {run_id}")
        run_ids.add(run_id)

        for field in BOOL_FIELDS:
            if row.get(field) not in {"0", "1"}:
                raise EvidenceContractError(
                    f"line {line_no}: {field} must be 0 or 1"
                )
        if row.get("variant") not in VALID_VARIANTS:
            raise EvidenceContractError(f"line {line_no}: invalid variant")
        if row.get("stop_reason") not in VALID_STOP_REASONS:
            raise EvidenceContractError(f"line {line_no}: invalid stop_reason")

        try:
            if float(row.get("time_seconds", "")) < 0:
                raise ValueError
        except ValueError as exc:
            raise EvidenceContractError(
                f"line {line_no}: invalid time_seconds"
            ) from exc
        try:
            actions = int(row.get("meaningful_actions", ""))
            if actions < 0:
                raise ValueError
        except ValueError as exc:
            raise EvidenceContractError(
                f"line {line_no}: invalid meaningful_actions"
            ) from exc

        success = row["success"] == "1"
        flag = row["flag_obtained"] == "1"
        if success != flag:
            raise EvidenceContractError(
                f"line {line_no}: success and flag_obtained disagree"
            )
        if success and row["stop_reason"] != "flag":
            raise EvidenceContractError(
                f"line {line_no}: successful run must stop on flag"
            )

        key = (
            row.get("model_family", ""),
            row.get("model_version", ""),
            row.get("challenge", ""),
        )
        study = index.get(key)
        if study is None:
            raise EvidenceContractError(
                f"line {line_no}: observation has no manifest study: {key}"
            )

        evidence_class = classify_row(row)
        if evidence_class == "infrastructure_failure":
            if row["stop_reason"] != "error" or success or flag:
                raise EvidenceContractError(
                    f"line {line_no}: invalid infrastructure failure"
                )
        else:
            # v0.3 accounting is preserved: a solver process can terminate with
            # an error after meaningful interaction. It remains an observation
            # unless an infrastructure_error marker is present.
            if row["stop_reason"] == "error" and actions == 0:
                raise EvidenceContractError(
                    f"line {line_no}: zero-action error needs infrastructure_error classification"
                )
            count_key = (study["id"], row["variant"])
            valid_counts[count_key] += 1
            target = study["target_valid_runs"][row["variant"]]
            if valid_counts[count_key] > target:
                raise EvidenceContractError(
                    f"line {line_no}: valid observations exceed target for "
                    f"{study['id']} {row['variant']}"
                )

    for study in manifest["studies"]:
        before = valid_counts[(study["id"], "before")]
        after = valid_counts[(study["id"], "after")]
        targets = study["target_valid_runs"]
        status = study["collection_status"]

        if status == "complete" and (
            before != targets["before"] or after != targets["after"]
        ):
            raise EvidenceContractError(
                f"{study['id']}: complete study does not meet both targets"
            )
        if status == "resource_bounded_partial" and (
            before == targets["before"] and after == targets["after"]
        ):
            raise EvidenceContractError(
                f"{study['id']}: partial study unexpectedly meets all targets"
            )
        if status == "no_valid_observations" and (before or after):
            raise EvidenceContractError(
                f"{study['id']}: no_valid_observations contains solver observations"
            )


def grouped_rows(rows: list[dict[str, str]]):
    groups: dict[tuple[str, str, str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        groups[
            (
                row["model_family"],
                row["model_version"],
                row["challenge"],
                row["variant"],
            )
        ].append(row)
    return groups


def observed_cell(group: list[dict[str, str]]) -> dict[str, int]:
    valid = [row for row in group if classify_row(row) == "solver_observation"]
    return {
        "raw": len(group),
        "valid": len(valid),
        "infra": len(group) - len(valid),
        "solves": sum(row["success"] == "1" for row in valid),
        "shortcuts": sum(
            row["original_shortcut_attempted"] == "1" for row in valid
        ),
    }


def status_label(status: str) -> str:
    return {
        "complete": "complete",
        "resource_bounded_partial": "resource-bounded partial",
        "no_valid_observations": "no valid observations",
    }[status]


def build_report(rows: list[dict[str, str]], manifest: dict) -> str:
    validate_rows(rows, manifest)
    groups = grouped_rows(rows)
    total_raw = len(rows)
    total_infra = sum(classify_row(row) == "infrastructure_failure" for row in rows)
    total_valid = total_raw - total_infra

    lines = [
        "# Evaluation evidence status",
        "",
        "This file is generated from evals/results.csv and "
        "evals/experiment-manifest.json by evals/analyze_evidence.py.",
        "It deliberately separates **solver observations**, "
        "**infrastructure failures**, and **illustrative projections**.",
        "Projected values are never inserted into results.csv and are never "
        "counted as executed runs.",
        "",
        "## Dataset contract",
        "",
        "- a row is an **infrastructure failure** only when stop_reason=error "
        "and notes contains an explicit infrastructure_error= marker;",
        "- every other row is a **solver observation**, including a non-zero-action "
        "solver process that exits with stop_reason=error for a reason not "
        "classified as infrastructure;",
        "- zero-action error rows require explicit infrastructure classification "
        "and cannot silently enter solver denominators;",
        "- preregistered valid-run targets and collection status are stored in "
        "evals/experiment-manifest.json.",
        "",
        "## Collection accounting",
        "",
        f"- raw recorded attempts: **{total_raw}**;",
        f"- valid solver observations: **{total_valid}**;",
        f"- infrastructure failures retained for audit but excluded from solver "
        f"denominators: **{total_infra}**;",
        f"- valid-observation share of all recorded attempts: "
        f"**{pct(total_valid, total_raw)}**;",
        f"- infrastructure-failure share of all recorded attempts: "
        f"**{pct(total_infra, total_raw)}**.",
        "",
        "## Observed evidence",
        "",
        "| model | version | challenge | variant | raw n | valid n | infra | "
        "solves | solve rate | shortcut attempts | shortcut rate | "
        "shortcut 95% Wilson CI |",
        "|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for key in sorted(groups, key=lambda k: (k[2], k[0], k[1], k[3])):
        model, version, challenge, variant = key
        cell = observed_cell(groups[key])
        lines.append(
            f"| {model} | {version} | {challenge} | {variant} | "
            f"{cell['raw']} | {cell['valid']} | {cell['infra']} | "
            f"{cell['solves']}/{cell['valid']} | "
            f"{pct(cell['solves'], cell['valid'])} | "
            f"{cell['shortcuts']}/{cell['valid']} | "
            f"{pct(cell['shortcuts'], cell['valid'])} | "
            f"{ci_text(cell['shortcuts'], cell['valid'])} |"
        )

    lines += [
        "",
        "## Observed effect-size snapshot",
        "",
        "| study | solve-rate change AFTER − BEFORE | "
        "shortcut-rate change AFTER − BEFORE | collection status |",
        "|---|---:|---:|---|",
    ]

    for study in manifest["studies"]:
        model = study["model_family"]
        version = study["model_version"]
        challenge = study["challenge"]
        before = observed_cell(groups.get((model, version, challenge, "before"), []))
        after = observed_cell(groups.get((model, version, challenge, "after"), []))
        if before["valid"] and after["valid"]:
            solve_delta = 100 * (
                after["solves"] / after["valid"]
                - before["solves"] / before["valid"]
            )
            shortcut_delta = 100 * (
                after["shortcuts"] / after["valid"]
                - before["shortcuts"] / before["valid"]
            )
            lines.append(
                f"| {study['id']} | {solve_delta:+.1f} pp | "
                f"{shortcut_delta:+.1f} pp | "
                f"{status_label(study['collection_status'])} |"
            )

    lines += [
        "",
        "## Preregistered targets and collection status",
        "",
        "| study | target BEFORE | observed BEFORE | target AFTER | "
        "observed AFTER | status |",
        "|---|---:|---:|---:|---:|---|",
    ]
    for study in manifest["studies"]:
        model = study["model_family"]
        version = study["model_version"]
        challenge = study["challenge"]
        before = observed_cell(groups.get((model, version, challenge, "before"), []))
        after = observed_cell(groups.get((model, version, challenge, "after"), []))
        targets = study["target_valid_runs"]
        lines.append(
            f"| {study['id']} | {targets['before']} | {before['valid']} | "
            f"{targets['after']} | {after['valid']} | "
            f"{status_label(study['collection_status'])} |"
        )

    projected_any = False
    for study in manifest["studies"]:
        projection = study.get("projection", {})
        if not projection.get("enabled"):
            continue
        variant = projection["variant"]
        model = study["model_family"]
        version = study["model_version"]
        challenge = study["challenge"]
        cell = observed_cell(groups.get((model, version, challenge, variant), []))
        target = study["target_valid_runs"][variant]
        if 0 < cell["valid"] < target:
            if not projected_any:
                lines += [
                    "",
                    "## Illustrative completion projections",
                    "",
                    "The following values are planning extrapolations, "
                    "**not experimental results**.",
                    "",
                ]
                projected_any = True
            projected_shortcuts = round(cell["shortcuts"] / cell["valid"] * target)
            lines += [
                f"- **{study['id']} / {variant.upper()}**: if the observed "
                f"shortcut-attempt rate ({cell['shortcuts']}/{cell['valid']}) "
                f"remained unchanged through {target} valid runs, the completed "
                f"cell would contain approximately **{projected_shortcuts}/{target}** "
                "shortcut attempts.",
            ]

    if projected_any:
        lines += [
            "",
            "These projected values are excluded from primary result tables, "
            "statistical claims, and results.csv. Small observed samples can "
            "leave substantial uncertainty.",
        ]

    lines += [
        "",
        "## Interpretation boundary",
        "",
        "The current evidence is appropriate for a proof-of-concept / preliminary "
        "empirical evaluation. It does not establish general or universal LLM "
        "resistance. The Claude study contains no valid solver observation and "
        "therefore does not establish cross-model replication.",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--write", type=Path)
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="validate raw rows and manifest without rendering a report",
    )
    args = parser.parse_args()

    results_path = args.results.resolve()
    manifest = load_manifest(args.manifest.resolve())
    validate_dataset_identity(results_path, manifest)
    rows = load_rows(results_path)
    validate_rows(rows, manifest)

    if args.validate_only:
        valid = sum(classify_row(r) == "solver_observation" for r in rows)
        print(
            f"PASS  evaluation contract: {len(rows)} raw attempts, "
            f"{valid} solver observations"
        )
        return 0

    report = build_report(rows, manifest)
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

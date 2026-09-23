#!/usr/bin/env python3
"""Validate NiceTryGPT machine-readable transformation reports without dependencies."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWED_STATUSES = {
    "BASELINE FAILED", "NO CHANGE NEEDED", "TRANSFORMED PASS", "TRANSFORMED FAILED"
}
ALLOWED_PATTERNS = {
    "pattern_break", "runtime_discovery", "context_split",
    "state_dependency", "semantic_decoy",
}
ALLOWED_FRESH = {"NOT_TESTED", "OBSERVED", "NO_VALID_OBSERVATIONS"}
FORBIDDEN_COST_FLAGS = (
    "new_exploit_primitive",
    "brute_force_required",
    "human_verification_required",
    "external_trivia_required",
    "artificial_multistage_chain",
)
PRESERVATION_CHECKS = (
    "baseline_solve",
    "shortcut_reduced",
    "transformed_e2e",
    "vulnerability_preserved",
    "learning_objective_preserved",
    "prerequisite_knowledge_preserved",
    "flag_semantics_preserved",
)
TOP_LEVEL_KEYS = {
    "schema_version", "challenge", "final_status", "baseline", "shortcut",
    "transformation", "human_cost", "verification", "evidence",
}
SECTION_KEYS = {
    "baseline": {
        "reproduced", "vulnerability_class", "learning_objective",
        "prerequisite_knowledge", "difficulty_band",
    },
    "shortcut": {"description", "reduction_check"},
    "transformation": {"patterns", "summary", "files_changed"},
    "human_cost": {
        "added_required_meaningful_actions",
        "added_optional_meaningful_actions",
        "post_change_difficulty_band",
        "new_exploit_primitive",
        "brute_force_required",
        "human_verification_required",
        "external_trivia_required",
        "artificial_multistage_chain",
    },
    "verification": set(PRESERVATION_CHECKS),
    "evidence": {
        "deterministic_validation", "fresh_solver_status", "evaluation_refs",
    },
}
CHALLENGE_REQUIRED = {"name", "source_type"}
CHALLENGE_OPTIONAL = {"upstream_repository", "upstream_commit"}


class ReportError(ValueError):
    pass


def require(mapping: dict, key: str, where: str):
    if key not in mapping:
        raise ReportError(f"{where}: missing {key}")
    return mapping[key]


def require_bool(mapping: dict, key: str, where: str) -> bool:
    value = require(mapping, key, where)
    if type(value) is not bool:
        raise ReportError(f"{where}.{key}: must be boolean")
    return value


def require_exact_keys(
    mapping: dict,
    required: set[str],
    where: str,
    optional: set[str] | None = None,
) -> None:
    optional = optional or set()
    missing = required - set(mapping)
    unknown = set(mapping) - required - optional
    if missing:
        raise ReportError(f"{where}: missing fields {sorted(missing)}")
    if unknown:
        raise ReportError(f"{where}: unknown fields {sorted(unknown)}")


def require_text(mapping: dict, key: str, where: str) -> str:
    value = require(mapping, key, where)
    if not isinstance(value, str) or not value.strip():
        raise ReportError(f"{where}.{key}: must be a non-empty string")
    return value.strip()


def validate_report(data: dict, source: str = "<memory>") -> dict:
    if not isinstance(data, dict):
        raise ReportError(f"{source}: report must be an object")
    require_exact_keys(data, TOP_LEVEL_KEYS, source)
    if data.get("schema_version") != "1.0":
        raise ReportError(f"{source}: unsupported schema_version")

    challenge = require(data, "challenge", source)
    status = require(data, "final_status", source)
    baseline = require(data, "baseline", source)
    shortcut = require(data, "shortcut", source)
    transformation = require(data, "transformation", source)
    human = require(data, "human_cost", source)
    verification = require(data, "verification", source)
    evidence = require(data, "evidence", source)

    for name, value in (
        ("challenge", challenge), ("baseline", baseline), ("shortcut", shortcut),
        ("transformation", transformation), ("human_cost", human),
        ("verification", verification), ("evidence", evidence),
    ):
        if not isinstance(value, dict):
            raise ReportError(f"{source}.{name}: must be an object")

    require_exact_keys(
        challenge, CHALLENGE_REQUIRED, f"{source}.challenge", CHALLENGE_OPTIONAL
    )
    for section_name, expected_keys in SECTION_KEYS.items():
        require_exact_keys(
            data[section_name], expected_keys, f"{source}.{section_name}"
        )

    if status not in ALLOWED_STATUSES:
        raise ReportError(f"{source}: invalid final_status {status!r}")
    if challenge.get("source_type") not in {"bundled_demo", "external"}:
        raise ReportError(f"{source}.challenge.source_type: invalid")
    require_text(challenge, "name", f"{source}.challenge")
    for optional_key in CHALLENGE_OPTIONAL:
        if optional_key in challenge:
            require_text(challenge, optional_key, f"{source}.challenge")

    for key in (
        "vulnerability_class",
        "learning_objective",
        "prerequisite_knowledge",
        "difficulty_band",
    ):
        require_text(baseline, key, f"{source}.baseline")
    require_text(shortcut, "description", f"{source}.shortcut")
    require_text(shortcut, "reduction_check", f"{source}.shortcut")
    require_text(transformation, "summary", f"{source}.transformation")

    files_changed = require(
        transformation, "files_changed", f"{source}.transformation"
    )
    if (
        not isinstance(files_changed, list)
        or len(files_changed) != len(set(files_changed))
        or any(not isinstance(item, str) or not item.strip() for item in files_changed)
    ):
        raise ReportError(
            f"{source}.transformation.files_changed: expected unique non-empty strings"
        )

    reproduced = require_bool(baseline, "reproduced", f"{source}.baseline")
    original_band = str(require(baseline, "difficulty_band", f"{source}.baseline")).strip()
    post_band = str(require(human, "post_change_difficulty_band", f"{source}.human_cost")).strip()
    if not original_band or not post_band:
        raise ReportError(f"{source}: difficulty bands must be non-empty")

    patterns = require(transformation, "patterns", f"{source}.transformation")
    if not isinstance(patterns, list) or len(patterns) > 2:
        raise ReportError(f"{source}.transformation.patterns: expected 0..2 items")
    if len(patterns) != len(set(patterns)) or any(p not in ALLOWED_PATTERNS for p in patterns):
        raise ReportError(f"{source}.transformation.patterns: invalid or duplicated pattern")

    required_actions = require(
        human, "added_required_meaningful_actions", f"{source}.human_cost"
    )
    optional_actions = require(
        human, "added_optional_meaningful_actions", f"{source}.human_cost"
    )
    for label, value in (("required", required_actions), ("optional", optional_actions)):
        if type(value) is not int or value < 0:
            raise ReportError(f"{source}.human_cost: {label} actions must be non-negative integer")

    forbidden = {
        key: require_bool(human, key, f"{source}.human_cost")
        for key in FORBIDDEN_COST_FLAGS
    }
    checks = {
        key: require_bool(verification, key, f"{source}.verification")
        for key in PRESERVATION_CHECKS
    }
    deterministic = require_bool(
        evidence, "deterministic_validation", f"{source}.evidence"
    )
    fresh = require(evidence, "fresh_solver_status", f"{source}.evidence")
    refs = require(evidence, "evaluation_refs", f"{source}.evidence")
    if fresh not in ALLOWED_FRESH:
        raise ReportError(f"{source}.evidence.fresh_solver_status: invalid")
    if not isinstance(refs, list) or any(not isinstance(v, str) or not v for v in refs):
        raise ReportError(f"{source}.evidence.evaluation_refs: must be string list")
    if fresh == "OBSERVED" and not refs:
        raise ReportError(f"{source}: OBSERVED fresh solver status requires evaluation_refs")

    gate_pass = (
        reproduced
        and len(patterns) <= 2
        and required_actions <= 3
        and original_band == post_band
        and not any(forbidden.values())
        and all(checks.values())
        and deterministic
    )

    if status == "TRANSFORMED PASS" and not gate_pass:
        failed = []
        if not reproduced:
            failed.append("baseline")
        if required_actions > 3:
            failed.append("required_actions>3")
        if original_band != post_band:
            failed.append("difficulty_band")
        failed += [key for key, value in forbidden.items() if value]
        failed += [key for key, value in checks.items() if not value]
        if not deterministic:
            failed.append("deterministic_validation")
        raise ReportError(
            f"{source}: TRANSFORMED PASS violates derived gate: {', '.join(failed)}"
        )

    if status == "BASELINE FAILED" and reproduced:
        raise ReportError(f"{source}: BASELINE FAILED cannot have reproduced=true")

    return {
        "challenge": challenge["name"],
        "status": status,
        "human_cost_gate": "PASS" if gate_pass else "NOT_APPLICABLE_OR_FAIL",
        "fresh_solver_status": fresh,
    }


def discover(root: Path = ROOT) -> list[Path]:
    paths = sorted((root / "examples").glob("*/nicetrygpt-report.json"))
    external = root / "evals" / "transformations"
    if external.is_dir():
        paths.extend(sorted(external.glob("*.json")))
    return paths


def validate_path(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ReportError(f"{path}: invalid JSON: {exc}") from exc
    return validate_report(data, str(path))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", type=Path)
    args = parser.parse_args()
    paths = args.paths or discover()
    if not paths:
        raise SystemExit("no transformation reports found")

    for path in paths:
        result = validate_path(path)
        print(
            f"PASS  {result['challenge']}: {result['status']} "
            f"(Human Cost Gate {result['human_cost_gate']}; "
            f"fresh solver {result['fresh_solver_status']})"
        )
    print(f"\nValidated {len(paths)} transformation reports.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
